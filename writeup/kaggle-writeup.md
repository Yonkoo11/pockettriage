# PocketTriage — offline WHO IMCI triage on Gemma 4

**Track:** Health & Sciences Impact (primary) + Ollama Special Tech
**Pitch:** Offline clinic in pocket.
**Repo:** https://github.com/yonkoo11/pockettriage
**Demo:** https://huggingface.co/spaces/yonkoo11/pockettriage (browser verification)
**License:** Apache 2.0

---

## The problem

The WHO IMCI (Integrated Management of Childhood Illness) protocol is the global standard for paediatric triage in low-resource settings. It is the chart on the wall in every primary health centre from Anambra to Maharashtra. A community health worker (CHW) follows it case by case: ask about cough, diarrhoea, fever, ear, malnutrition, general danger signs; classify the child into Pink (refer urgently) / Yellow (treat at facility) / Green (home care); record the pathway.

The protocol works. The bottleneck is application speed and consistency in the field. The Adaeze persona — a Nigerian CHEW with a Tecno Spark phone, intermittent 2G, and the paper IMCI chart booklet in her bag — does roughly 30 paediatric visits a week. Each one is ~10 minutes of cross-referencing the chart, recording vitals, writing a referral note by hand. Cloud-based decision-support does not help her: there is no signal in the village. Paper does not help her either: it is slow, and the chart booklet is too long to memorise reliably.

What she needs is the chart booklet as a fast, deterministic, on-device tool. That is the entire product.

## The solution

PocketTriage is an open-source on-device implementation of the WHO IMCI 2014 paediatric classifier, built on Gemma 4. The CHW types a symptom description and optionally attaches a photo (rash, oedema, MUAC tape). Gemma 4 E2B / E4B classifies the case against the IMCI protocol and returns a Pink/Yellow/Green tier and a structured pathway via JSON output. A non-bypassable safety layer enforces three invariants regardless of model output: WHO danger-sign keywords force Pink; confidence below 0.4 appends "Escalate to medical officer"; adult conditions return a refusal. A non-dismissable disclaimer banner says PocketTriage does not replace clinical judgment and is paediatric only (2 months – 5 years).

Two deployment surfaces:

1. **Laptop V1 (shipped, this submission).** Python + Gradio + Ollama running `gemma4:e2b` on a developer or clinic laptop. Verified airplane-mode operation: tcpdump captured zero non-localhost packets during inference.
2. **Android V2 (roadmap, NOT in this submission).** Kotlin + LiteRT (Google AI Edge) loading the `gemma-4-E4B-it.litertlm` artifact from `litert-community` on a target $80 Android phone. The artifact is identified and the architecture is wired in `notes/model-source.md` Q2 / Q5, but no APK was built and tested on a real device in V1. The LiteRT track is therefore NOT in the applied-tracks list (see `ai/sponsor-integration.md`).

Same JSON output contract designed for both surfaces.

## Architecture

CHW symptom text (+ optional photo) → `infer.py` builds the WHO-IMCI-grounded chat → Ollama backend on `127.0.0.1:11434` runs `gemma4:e2b` → raw model output → `_extract_first_json` + `_validate_shape` coerce to `{tier, pathway, reasoning, confidence}` → safety layer (R13–R16) → Gradio renders the tier card. No server. No analytics. No telemetry. Patient text lives in process memory and is discarded at session end.

## Evidence — Phase 1 Gate

The product was gated on a verifiable airplane-mode test before any polish work. Four canonical IMCI scenarios drawn from the WHO IMCI Chart Booklet 2014, run with Wi-Fi and cellular off, output captured in `eval/airplane-test-log.md`:

| Scenario | Expected tier | Actual tier | Latency |
|---|---|---|---|
| S1 severe pneumonia (chest indrawing + refusing to drink) | Pink | Pink | 10.6 s |
| S2 some dehydration (diarrhoea + restless + drinks eagerly + slow skin pinch) | Yellow | Yellow | 10.7 s |
| S3 uncomplicated malaria (RDT+ fever, no danger signs) | Yellow | Yellow | 9.3 s |
| S4 cough or cold (cough + drinking well + no chest indrawing) | Green | Green | 8.4 s |

4 / 4 pass. Zero outbound packets to any non-localhost address during the run.

## Sponsor integrations — what carries load

**Gemma 4 model.** The classifier IS Gemma 4. V1 ships on `gemma4:e2b` (5.1B params, Q4_K_M) because the larger E4B pull did not complete during the build window; the swap is a single env var (`POCKETTRIAGE_OLLAMA_TAG=gemma4:e4b`). The product would not exist without an open-weight model in the 5–9B class that runs offline on a budget phone.

**Multimodal vision.** Gemma 4's native vision capability accepts a photo of the child (skin rash, eye, MUAC tape) on the same chat call as the text symptom description. The `OllamaBackend.generate` method passes the base64 image in the `images` field of the chat message; the Android LiteRT path uses the equivalent multimodal hook. Photo input is supplementary — the pathway must always be groundable in the text description alone, because dermatology accuracy on darker skin tones is a known weak point for image models and we refuse to depend on it.

**Native function calling / structured JSON.** Gemma 4 supports tools and structured output natively. V1 uses a JSON output contract specified in the system prompt rather than the tool-call API, for portability across runtimes (Ollama on laptop, LiteRT on Android, MLX as alternate). The JSON contract is enforced by `_extract_first_json` and `_validate_shape` with a deterministic fallback so a malformed response cannot crash the UI.

**Ollama.** V1 laptop runtime. `gemma4` architecture is native in Ollama 0.23.1+, which avoids the iSWA-attention bug present in older `llama-cpp` GGUF distributions of Gemma 4. The Modelfile + Ollama integration is documented in the README; the HF Space deploys Ollama in a Docker container for a clean cross-platform reference. Ollama is load-bearing for V1 — without the native `gemma4` architecture support there is no working laptop deployment path on Apple Silicon today.

**LiteRT (Google AI Edge) — V2 roadmap, not in this submission.** The Android deployment loads `gemma-4-E4B-it.litertlm` from the official `litert-community` Hugging Face org; the chipset-specific variants (`qcs8275`, `sm8750`) match the Snapdragon SoC families on the budget Android segment. This path is wired in `notes/model-source.md` Q2 / Q5 but no APK was built and tested on a real device in V1. The LiteRT track is therefore NOT in the applied-tracks list — see `ai/sponsor-integration.md`.

## Safety design

PocketTriage will be wrong sometimes. So will any classifier. The architecture treats the model as a powerful but fallible signal and never lets it have the final word:

- **R13 danger-sign force-Pink.** A keyword matcher (negation-aware, see `laptop/safety.py:_danger_signs_present`) inspects the raw symptom text for WHO IMCI general danger signs (unable to drink, vomits everything, convulsions, lethargic, unconscious, stiff neck, chest indrawing). If any match, the tier is forced to Pink even if the model said Green.
- **R14 confidence floor.** If the model's self-reported confidence is below 0.4, "Escalate to medical officer" is appended to the pathway.
- **R15 adult-condition refusal.** Adult-specific terms (chest pain in adult, pregnancy emergency, stroke in adult) trigger a refusal and refer to adult emergency protocol.
- **R16 disclaimer.** The disclaimer ribbon "Does NOT replace clinical judgment. Paediatric only" is rendered as part of the Gradio layout, not as a popup that can be dismissed.

17 unit tests cover the safety layer (`laptop/test_safety.py`).

## Ethical considerations

- **No clinical claim.** PocketTriage is decision-support, not a medical device. The README, the UI banner, and the LICENSE all say so.
- **Photo accuracy on darker skin.** Disclosed in README. Photo is supplementary; text is primary.
- **Data minimisation.** Patient symptom text never leaves the device. There is no cloud, no analytics, no telemetry, no error reporting service. Process memory is discarded on session end.
- **Non-US context by design.** Targeting CHW workflows in WHO programmes (not US clinics) avoids FDA SaMD framing while still delivering real value.

## Distribution — started during the build

Per the production discipline this hackathon enforces, distribution outreach is part of V1, not a post-submission afterthought. Drafted in repo under `outreach/`:

- WHO Digital Health & Innovation (Dr. Alain Labrique, Geneva)
- India National Health Mission / ASHA programme (Add. Secretary NHM, NHSRC, Maharashtra state)
- Nigerian NPHCDA / FMoH (Dr. Muyi Aina, plus Anambra SPHCDA at state level)

Each file is a named contact, the rationale, a full email body, and a shorter LinkedIn / WhatsApp variant. Send queued for immediately after submission.

## What's verified vs not

**Verified:** Phase 1 Gate (4/4 IMCI scenarios, airplane mode, zero network egress), safety layer (17 unit tests), backend abstraction (Ollama path), Gradio UI flow, repo + license + CONTRIBUTING + CODE_OF_CONDUCT.

**Not yet verified at submission time:** Android LiteRT APK on real Tecno-Spark-class hardware (artifact + architecture identified; NOT applied for the LiteRT track because no on-device demo); HF Space cold-boot latency (Docker config written, deploy pending); outreach responses (sent post-submission, with the live demo URL).

That is an honest snapshot. The laptop V1 is real. The Android V2 path is wired but not yet on-device-validated, and we have explicitly excluded the LiteRT track from this submission because of that. We say so here, in the repo, and in `ai/sponsor-integration.md`.

## Word count

~1,420 words.
