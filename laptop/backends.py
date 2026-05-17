"""Model backend adapters for PocketTriage.

Three backends share a single interface:
    backend.generate(system: str, user: str, image_b64: str | None) -> str

Selection via env var POCKETTRIAGE_BACKEND:
    "ollama"  → Ollama HTTP at 127.0.0.1:11434 (default, production V1)
    "mlx"     → mlx-vlm (Apple Silicon, alternate runtime)
    "mock"    → canned IMCI responses for CI / offline dev / safety-layer tests

The Mock backend returns deterministic outputs keyed off symptom keywords. It is
explicitly labeled as Mock everywhere so it cannot silently sneak into a live demo.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Protocol

log = logging.getLogger("pockettriage.backends")


class ModelBackend(Protocol):
    """Interface every backend must implement."""

    name: str

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        image_b64: str | None = None,
    ) -> str:
        """Return raw model text. Caller parses JSON. Must raise on failure."""
        ...


# ---------------------------------------------------------------------------
# Ollama backend (default — production V1)
# ---------------------------------------------------------------------------


class OllamaBackend:
    """Calls a local Ollama server at 127.0.0.1:11434."""

    name = "ollama"

    def __init__(
        self,
        model_tag: str = "gemma4:e2b",
        url: str = "http://127.0.0.1:11434/api/chat",
        timeout: float = 180.0,
    ):
        self.model_tag = model_tag
        self.url = url
        self.timeout = timeout

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        image_b64: str | None = None,
    ) -> str:
        import httpx  # local import so the module loads even if httpx is missing

        user_msg: dict[str, Any] = {"role": "user", "content": user_prompt}
        if image_b64:
            user_msg["images"] = [image_b64]

        payload = {
            "model": self.model_tag,
            "messages": [
                {"role": "system", "content": system_prompt},
                user_msg,
            ],
            "stream": False,
            # Gemma 4 splits output into thinking + content channels. For JSON
            # extraction we want only the answer channel.
            "think": False,
            "options": {
                "temperature": 0.2,
                "top_p": 0.9,
                "num_predict": 400,
            },
        }

        try:
            r = httpx.post(self.url, json=payload, timeout=self.timeout)
            r.raise_for_status()
        except httpx.ConnectError as e:
            raise RuntimeError(
                "Ollama not reachable at 127.0.0.1:11434. "
                "Run `ollama serve` in a separate terminal, then `ollama pull gemma4:e4b`."
            ) from e
        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"Ollama returned HTTP {e.response.status_code}: {e.response.text[:200]}"
            ) from e
        except httpx.RequestError as e:
            raise RuntimeError(f"Request to Ollama failed: {e}") from e

        data = r.json()
        msg = data.get("message", {}).get("content", "")
        if not msg:
            raise RuntimeError("Empty response from Ollama")
        return msg


# ---------------------------------------------------------------------------
# MLX backend (Apple Silicon native alternate)
# ---------------------------------------------------------------------------


class MlxBackend:
    """Uses mlx-vlm to run Gemma 4 natively on Apple Silicon.

    Lazy-loads the model on first generate() call to keep startup fast.
    """

    name = "mlx"

    def __init__(self, model_id: str = "mlx-community/gemma-4-e4b-it-4bit"):
        self.model_id = model_id
        self._loaded = False
        self._model = None
        self._processor = None
        self._config = None

    def _ensure_loaded(self):
        if self._loaded:
            return
        from mlx_vlm import load
        from mlx_vlm.utils import load_config
        log.info("Loading MLX model %s...", self.model_id)
        self._model, self._processor = load(self.model_id)
        self._config = load_config(self.model_id)
        self._loaded = True
        log.info("MLX model loaded.")

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        image_b64: str | None = None,
    ) -> str:
        self._ensure_loaded()
        from mlx_vlm import generate as mlx_generate
        from mlx_vlm.prompt_utils import apply_chat_template

        # mlx-vlm uses a single combined prompt; we prepend system into the chat template
        combined = f"{system_prompt}\n\n{user_prompt}"
        formatted = apply_chat_template(
            self._processor,
            self._config,
            combined,
            num_images=1 if image_b64 else 0,
        )
        # MLX vlm path returns generated text directly
        out = mlx_generate(
            self._model,
            self._processor,
            formatted,
            max_tokens=400,
            verbose=False,
        )
        if not out:
            raise RuntimeError("Empty response from MLX")
        return out


# ---------------------------------------------------------------------------
# Mock backend (CI / offline dev / unit tests)
# ---------------------------------------------------------------------------


class MockBackend:
    """Deterministic canned responses keyed off symptom keywords.

    Used in CI and when offline. Output is explicitly labeled '(mock)' in reasoning
    so it cannot be mistaken for real model output during a demo.

    Mapping logic mirrors the WHO IMCI classification:
    - "chest indrawing" or "refuses to drink" -> Pink (severe pneumonia / general danger sign)
    - "diarrhoea" + ("sunken eyes" or "skin pinch") -> Yellow (some dehydration)
    - "rdt positive" or "malaria" + "fever" -> Yellow (uncomplicated malaria)
    - "runny nose" or "cough" + "drinking well" -> Green (cough or cold)
    - default -> Yellow with low confidence
    """

    name = "mock"

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        image_b64: str | None = None,
    ) -> str:
        s = user_prompt.lower()

        def reply(tier: str, pathway: str, reasoning: str, confidence: float) -> str:
            d = {
                "tier": tier,
                "pathway": pathway,
                "reasoning": f"(mock) {reasoning}",
                "confidence": confidence,
            }
            return json.dumps(d)

        _ = system_prompt  # mock ignores; signature parity only
        _ = image_b64

        def has(token: str, phrase: str) -> bool:
            """True if `phrase` appears non-negated in token."""
            i = token.find(phrase)
            while i != -1:
                if not token[max(0, i - 15) : i].rstrip().endswith(("no", "not", "without", "denies")):
                    return True
                i = token.find(phrase, i + 1)
            return False

        # Severe pneumonia — chest indrawing OR sucking in + refuses/refusing to drink
        chest_severe = has(s, "chest indrawing") or has(s, "chest is sucking in") or has(s, "chest sucking in")
        refuses_drink = has(s, "refuses to drink") or has(s, "refusing to drink") or has(s, "not drinking")
        if chest_severe and refuses_drink:
            return reply(
                "Pink",
                "Give first dose injectable ampicillin + gentamicin (or oral amoxicillin if no injectable). Refer urgently to nearest hospital.",
                "Section 2, Severe pneumonia or very severe disease — chest indrawing + general danger sign.",
                0.92,
            )

        # Uncomplicated malaria — RDT-positive fever, no danger signs
        has_malaria_evidence = has(s, "rdt positive") or has(s, "p. falciparum") or has(s, "malaria")
        has_fever = has(s, "fever")
        no_danger = not (has(s, "stiff neck") or has(s, "lethargic") or has(s, "unconscious") or has(s, "convulsion"))
        if has_malaria_evidence and has_fever and no_danger:
            return reply(
                "Yellow",
                "Give artemether-lumefantrine (AL) oral course per weight band. Paracetamol for fever. Follow-up in 3 days.",
                "Section 4, Uncomplicated malaria — fever + RDT positive, no danger signs.",
                0.88,
            )

        # Some dehydration — diarrhoea + (restless AND drinks eagerly) OR (sunken eyes AND slow skin pinch)
        has_diarrhoea = has(s, "diarrhoea") or has(s, "diarrhea")
        dehydration_signs = sum([
            1 if has(s, "restless") and not has(s, "lethargic") else 0,
            1 if has(s, "irritable") else 0,
            1 if has(s, "drinks eagerly") else 0,
            1 if has(s, "sunken eyes") else 0,
            1 if has(s, "skin pinch goes back slowly") or has(s, "skin pinch slow") else 0,
        ])
        if has_diarrhoea and dehydration_signs >= 2:
            return reply(
                "Yellow",
                "Plan B: ORS 75 ml/kg over 4 hours at the post. Zinc 10–20 mg/day for 10–14 days. Continue feeding.",
                "Section 3, Some dehydration — two or more some-dehydration signs present.",
                0.85,
            )

        # Cough or cold — cough/runny nose + no danger + drinking well or playful
        if (has(s, "runny nose") or has(s, "cough")) and (has(s, "drinking well") or has(s, "playful")):
            # Explicit absence of chest indrawing is reassuring
            if not has(s, "chest indrawing") and not has(s, "chest is sucking in"):
                return reply(
                    "Green",
                    "Home care: soothe throat with safe remedy, continue feeding. Return if breathing becomes fast or difficult.",
                    "Section 2, No pneumonia (cough or cold) — no fast breathing, no chest indrawing, no danger signs.",
                    0.80,
                )

        # Default: ambiguous → low-confidence Yellow (safety layer will append escalation via R14)
        return reply(
            "Yellow",
            "Treat at facility. Reassess after stabilisation.",
            "Insufficient information for confident classification.",
            0.30,
        )


# ---------------------------------------------------------------------------
# Selector
# ---------------------------------------------------------------------------


def get_backend() -> ModelBackend:
    name = os.environ.get("POCKETTRIAGE_BACKEND", "ollama").lower()
    if name == "ollama":
        return OllamaBackend(
            model_tag=os.environ.get("POCKETTRIAGE_OLLAMA_TAG", "gemma4:e2b"),
        )
    if name == "mlx":
        return MlxBackend(
            model_id=os.environ.get(
                "POCKETTRIAGE_MLX_MODEL", "mlx-community/gemma-4-e4b-it-4bit"
            )
        )
    if name == "mock":
        return MockBackend()
    raise ValueError(
        f"Unknown POCKETTRIAGE_BACKEND={name!r}. Use 'ollama', 'mlx', or 'mock'."
    )
