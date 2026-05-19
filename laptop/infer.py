"""PocketTriage inference module — Gemma 4 via pluggable backends, fully offline.

Public API:
    triage(symptoms: str, photo_b64: str | None = None) -> TriageResult

The function:
1. Builds the chat with system prompt (WHO IMCI protocol).
2. Calls the configured backend (Ollama / MLX / Mock) via `backends.get_backend()`.
3. Parses the JSON response against `schema.json`.
4. Runs the safety layer (R13–R15).
5. Returns a TriageResult.

Backend selection via env var POCKETTRIAGE_BACKEND. Default is Ollama. All
production backends route inference to 127.0.0.1 (localhost) — no remote calls
ever leave the device. See backends.py.

Function-calling: Gemma 4 supports native FC, but for V1 we use structured
JSON output via the system prompt's output-contract. This is more portable
across runtimes (Ollama, LiteRT, MLX) and easier to debug.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import asdict
from typing import Any

from backends import get_backend
from safety import TriageResult, apply_safety_layer
from system_prompt import SYSTEM_PROMPT

log = logging.getLogger("pockettriage.infer")


class InferenceError(RuntimeError):
    """Inference failed in a way the UI should surface to the CHW."""


def _extract_first_json(text: str) -> dict[str, Any] | None:
    """Find the first balanced JSON object in `text` and return it as a dict.

    Gemma sometimes wraps JSON in a code fence, sometimes prepends prose.
    We scan for the first '{' and then track brace depth to find the matching '}'.
    """
    if not text:
        return None
    # Fast path: try direct parse
    stripped = text.strip()
    if stripped.startswith("{"):
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            pass
    # Fallback: locate the first balanced { ... }
    start = text.find("{")
    while start != -1:
        depth = 0
        in_string = False
        escape = False
        for i in range(start, len(text)):
            ch = text[i]
            if in_string:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    in_string = False
                continue
            if ch == '"':
                in_string = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    candidate = text[start : i + 1]
                    try:
                        return json.loads(candidate)
                    except json.JSONDecodeError:
                        break
        start = text.find("{", start + 1)
    return None


def _validate_shape(d: dict[str, Any]) -> dict[str, Any]:
    """Coerce the model dict to the expected shape; raise InferenceError if unrecoverable."""
    if not isinstance(d, dict):
        raise InferenceError("Model did not return a JSON object")
    tier = d.get("tier", "")
    if tier not in {"Pink", "Yellow", "Green"}:
        # Try case normalisation
        if isinstance(tier, str) and tier.capitalize() in {"Pink", "Yellow", "Green"}:
            d["tier"] = tier.capitalize()
        else:
            raise InferenceError(f"Invalid tier: {tier!r}")
    d["pathway"] = str(d.get("pathway", "")).strip()[:240]
    d["reasoning"] = str(d.get("reasoning", "")).strip()[:400]
    try:
        c = float(d.get("confidence", 0.5))
    except (TypeError, ValueError):
        c = 0.3  # unknown confidence → low → safety layer will escalate
    d["confidence"] = max(0.0, min(1.0, c))
    return d


def triage(symptoms: str, photo_b64: str | None = None) -> TriageResult:
    """Triage a patient. Returns a TriageResult with the safety layer applied.

    Routes inference through the configured backend (env var POCKETTRIAGE_BACKEND).
    """
    if not symptoms or not symptoms.strip():
        raise InferenceError("Symptom description is empty")

    user_prompt = (
        "Triage this paediatric patient against the WHO IMCI protocol. "
        "Reply with ONLY the JSON object per the schema.\n\n"
        f"Patient: {symptoms.strip()}"
    )

    backend = get_backend()
    try:
        raw = backend.generate(SYSTEM_PROMPT, user_prompt, image_b64=photo_b64)
    except RuntimeError as e:
        raise InferenceError(str(e)) from e
    log.debug("[backend=%s] raw model output: %s", backend.name, raw)

    parsed = _extract_first_json(raw)
    if parsed is None:
        raise InferenceError(
            f"Model output was not valid JSON. Raw: {raw[:200]!r}"
        )
    shaped = _validate_shape(parsed)
    return apply_safety_layer(symptoms, shaped, had_photo=photo_b64 is not None)


if __name__ == "__main__":
    # CLI smoke test: python infer.py "symptom description"
    import sys

    if len(sys.argv) < 2:
        print("Usage: python infer.py 'symptom description'", file=sys.stderr)
        sys.exit(2)
    symptoms_in = " ".join(sys.argv[1:])
    t0 = time.time()
    result = triage(symptoms_in)
    dt = time.time() - t0
    print(f"--- TriageResult ({dt:.1f}s) ---")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
