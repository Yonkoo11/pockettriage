# Model source verification (PRD §11 answers)

Status as of 2026-05-17.

## Q1 — Gemma 4 E4B Ollama tag — verified availability

`gemma4:e4b` exists in the Ollama library (9.6 GB Q4_K_M).
`gemma4:e2b` exists in the Ollama library (7.2 GB Q4_K_M).

Both use Ollama's native `gemma4` architecture (introduced in v0.23.1, August 2026 cadence). Verified `ollama show gemma4:e2b` reports:

```
architecture        gemma4
parameters          5.1B
context length      131072
embedding length    1536
quantization        Q4_K_M
requires            0.20.0
Capabilities        completion, vision, audio, tools, thinking
```

**Decision:** V1 ships on `gemma4:e2b` (downloaded, verified, 4/4 Phase 1 Gate pass). The E4B tag is a drop-in upgrade via `POCKETTRIAGE_OLLAMA_TAG=gemma4:e4b` when the larger pull completes. No PRD change required — both share the architecture and chat template.

## Q2 — LiteRT `.task` URL — verified availability

`litert-community/gemma-4-E4B-it-litert-lm` on Hugging Face has:
- `gemma-4-E4B-it.litertlm` (mobile)
- `gemma-4-E4B-it-web.task` (web)
- `chat_template.jinja`

`litert-community/gemma-4-E2B-it-litert-lm` has the same plus chipset-optimized variants for qualcomm `qcs8275` and `sm8750`.

**Decision:** Android V2 will pull `gemma-4-E4B-it.litertlm` for LiteRT runtime integration. The chipset-specific E2B variants are a stretch if Android target devices fall on those SoCs.

## Q3 — Function calling at E4B / E2B parameter count

`ollama show gemma4:e2b` reports `Capabilities: ..., tools, ...` — native function calling supported at E2B. Inference confirms structured JSON output reliably (PRD §3.2 eval passes).

**Decision:** V1 uses structured JSON via the system prompt's output contract rather than the native FC API. This is more portable across runtimes (Ollama, LiteRT, MLX) and easier to debug. The native FC API is V2.

## Q4 — Multimodal (vision) at E4B / E2B parameter count

`ollama show gemma4:e2b` reports `Capabilities: completion, vision, audio, tools, thinking` — both vision and audio supported natively at E2B. The unsloth GGUF includes a multimodal projection file (`mmproj-F16.gguf`, 990 MB) which Ollama also publishes.

**Decision:** V1 wires photo input through Ollama's `images: [<base64>]` field on the chat message (already implemented in `laptop/backends.py:OllamaBackend.generate`). Photo input is treated as a supplementary signal — the text description remains the primary classifier per the safety design.

## Q5 — LiteRT Gemma 4 reference Android app

Google AI Edge ships LiteRT-LM sample apps via the `google-ai-edge/mediapipe` and `google-ai-edge/litert-lm` repos. The `gemma-4-E2B-it_qualcomm_qcs8275.litertlm` artifact suggests Google has tested deployment on at least one budget Android SoC family (matches the target hardware floor for CHW deployments).

**Decision:** Android V2 will fork the LiteRT-LM Android sample, swap in `gemma-4-E4B-it.litertlm`, and re-implement the chat + multimodal flow against the same JSON output contract used by the laptop V1.

## Model digest pinning (v0.2 hardening, 2026-05-19)

`gemma4:e2b` is an Ollama tag — Ollama can silently re-point a tag. For reproducibility, the actual blob hash at the time this product shipped is:

```
sha256:4e30e2665218745ef463f722c0bf86be0cab6ee676320f1cfadf91e989107448
```

That is the model weights blob underneath the `gemma4:e2b` tag on 2026-05-19 on this machine. To pin in production:

```bash
# Verify the model you're running matches the audit-time blob
ollama show gemma4:e2b --modelfile | grep "^FROM"
# Expected: FROM /Users/.../sha256-4e30e2665218745ef463f722c0bf86be0cab6ee676320f1cfadf91e989107448

# If the digest differs, the model was silently updated. Either rebuild eval
# against the new digest or pull the pinned digest explicitly:
ollama pull gemma4@sha256:4e30e2665218745ef463f722c0bf86be0cab6ee676320f1cfadf91e989107448
```

Architecture: `gemma4` (native Ollama family). Parameters: 5.1 B. Quantisation: Q4_K_M.
Phase 1 Gate 4/4 was verified against this exact digest — see [`eval/airplane-test-log.md`](../eval/airplane-test-log.md).

---

## Runtime status snapshot (2026-05-17)

| Component | Status | Notes |
|---|---|---|
| Ollama 0.24.0 (brew) | Installed | Supports `gemma4` arch natively |
| `gemma4:e2b` (7.2 GB) | Pulled, inference verified | Backs V1 |
| `gemma4:e4b` (9.6 GB) | Available, not pulled | Network unstable during build window; one-line swap when available |
| Local llama-cpp-python 0.3.23 | Installed but blocked | iSWA-attention bug with Gemma 4 GGUF; not used |
| mlx-vlm | Installed but blocked | Metal GPU timeout on Gemma 4 multimodal load on M-series; not used |
| HF transformers 5.8.1 | Installed | bf16 path works but slow without quantization; reserved as alt-backend |

**Working backend: Ollama → gemma4:e2b.** Backend abstraction (`laptop/backends.py`) supports swapping to E4B, MLX, or HF transformers without changes to `infer.py`.
