# Phase 4.5 sponsor-depth verification

**Date:** 2026-05-17.
**Rule (Skill #4):** apply only to tracks where shipped depth is ≥ 4/5 verified by this document. No "we'd polish it later" framing.

## Verification method

For each track, depth is rated 1–5 against this scale:

- **5/5** — Multiple primitives of this sponsor are load-bearing in V1. Removing the sponsor would break the product. Verifiable in the repo.
- **4/5** — One primitive of this sponsor is load-bearing in V1. Removing it would force a major rebuild. Verifiable in the repo.
- **3/5** — Sponsor is used but not load-bearing. The product would still work without it (e.g. an alt-backend, a stretch feature).
- **2/5** — Sponsor is name-dropped in the README but not actually wired.
- **1/5** — No real use.

Memory rule (`feedback_hackathon_deep_integration`): single-API name-drops are rejected. Memory rule (`feedback_hackathon_final_product_build`): only apply to tracks where V1 actually ships at the depth claimed.

## Main Track — 5/5 → APPLY

This is the umbrella. The product is a real V1 of an on-device WHO IMCI classifier with safety layer, eval evidence, public repo, and drafted distribution outreach. Submission-ready.

## Health & Sciences Impact — 5/5 → APPLY (PRIMARY TRACK)

Impact framing carries the full weight here. Concrete evidence:

- Real WHO protocol (IMCI 2014) encoded in `who-imci/protocol-summary.md`. Not an invented schema.
- Real personas defined in PRD §2 (Adaeze — Nigerian CHEW, Priya — Indian ASHA). Built by a Nigerian medical intern (me) — lived context, not extracted.
- Real distribution outreach drafted: 3 named contacts at WHO Digital Health, India NHM, Nigerian NPHCDA.
- Real safety architecture (R13–R16) that prevents the most dangerous failure modes (model says Green when child has danger sign).
- Real airplane-mode evidence (`eval/airplane-test-log.md`) verifying the offline core claim.

## LiteRT Special Tech (Google AI Edge) — 3/5 → DO NOT APPLY

Honest assessment per Skill Rule #4:

- `litert-community/gemma-4-E4B-it-litert-lm` identified as the target `.task` artifact.
- LiteRT runtime path documented in `notes/model-source.md` Q2 and Q5.
- BUT: no Android APK was built and run on a real Tecno-Spark-class device in V1. The Android directory does not exist in the repo. The LiteRT integration is wired in the architecture but not on-device-validated.

Per `feedback_hackathon_final_product_build`: do not apply to a sponsor track at < 4/5. The honest move is to skip the LiteRT track in this submission cycle and add it to the V2 plan with a real device demo.

Anti-rationalisation note: I will be tempted to apply "because we documented the path." The track rule is shipped-not-described. Skip.

## Ollama Special Tech — 4/5 → APPLY

- V1 laptop backend runs through Ollama (`OllamaBackend` in `laptop/backends.py`).
- `gemma4` native architecture in Ollama 0.23.1+ is load-bearing — it's the reason the V1 runs at all on Apple Silicon (the alternative llama-cpp path is blocked by the iSWA-attention bug, documented in `notes/model-source.md`).
- The HF Space (when deployed) installs Ollama in Docker — published Modelfile + integration is in `huggingface-space/Dockerfile` and `space_entrypoint.sh`.
- 4 / 4 IMCI canonical scenarios pass through this Ollama backend. Verifiable: `eval/airplane-test-log.md` shows the actual Ollama-backed runs.

Apply.

## Unsloth Special Tech — 1/5 → DO NOT APPLY

No fine-tune in V1. Considered, but eval at base Gemma 4 E2B already passes 4/4 canonical scenarios — the marginal value of an Unsloth LoRA on this dataset is not demonstrable in V1. Skip the track honestly.

## Cactus Special Tech — 1/5 → DO NOT APPLY

No E2B / E4B intelligent routing in V1. Single-model deploy. Skip.

## llama.cpp Special Tech — 1/5 → DO NOT APPLY

Hard rule from PRD: depth ceiling 3/5 because the iSWA-attention bug blocks Gemma 4 GGUF on this runtime. Already excluded from PRD §7.4. Confirmed skip.

---

## Final tracks-to-apply list

1. **Main Track** — apply
2. **Health & Sciences Impact** — apply (primary)
3. **Ollama Special Tech** — apply

Do NOT apply: LiteRT (no real device test), Unsloth (no fine-tune shipped), Cactus (no routing shipped), llama.cpp (architecturally blocked).

## What this means for the cover image / writeup / video

- Writeup currently says "Track: Health & Sciences Impact (primary) + LiteRT Special Tech" — must be updated to "Health & Sciences Impact + Ollama Special Tech".
- Video script must NOT show the Android phone clip unless an APK is actually built and demoed before recording. If no APK at recording time, cut that 15-second segment.
- Cover image is generic enough to be fine as-is.
- README must update the LiteRT line in 'What's in the box' from "Phase 3 — pending" to "V2 roadmap — not in V1 submission".

These three follow-on edits are queued in `ai/progress.md`.
