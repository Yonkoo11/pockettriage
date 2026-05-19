# PocketTriage — Status

**Honest snapshot at the 2026-05-18 hackathon submission.** Read this before the writeup — it tells you what's verified, what's claimed but not yet verified, and what's on the V2 roadmap.

---

## What's verified — runs, logged, reproducible

| Capability | Evidence | Reproduce |
|---|---|---|
| 4 / 4 canonical IMCI scenarios pass on `gemma4:e2b` | [`eval/airplane-test-log.md`](eval/airplane-test-log.md) | `python laptop/eval_runner.py` |
| Zero non-localhost packets during inference | tcpdump capture log | `tcpdump -i any -n 'not host 127.0.0.1 and not host ::1' -w airplane.pcap` |
| Safety layer R13–R16 — 17 unit tests pass | [`laptop/test_safety.py`](laptop/test_safety.py) | `pytest laptop/test_safety.py -v` |
| Live Hugging Face Space returns correct PINK tier + ampicillin pathway for S1 | Probe at 2026-05-17 returned correct tier in 534 s on cpu-basic | Open https://huggingface.co/spaces/yonko11/pockettriage |
| Public GitHub repo, Apache 2.0 | https://github.com/yonkoo11/pockettriage | `gh repo view yonkoo11/pockettriage` |
| Landing page reachable | https://yonkoo11.github.io/pockettriage | HTTP 200 confirmed |

## What's claimed in writeup / landing but not yet verified

These are honest gaps. Each is on the v0.2 roadmap.

| Claim | Reality | v0.2 plan |
|---|---|---|
| "Runs on Gemma 4 E2B / E4B" | Only **E2B** has been run against the eval. E4B is architecturally equivalent (same Ollama family, same chat template) but eval-untested. | Run `eval_runner.py` with `POCKETTRIAGE_OLLAMA_TAG=gemma4:e4b`, log result |
| "Multimodal vision — photo input is wired" | Wired AND now tested. See [`eval/multimodal-test-log.md`](eval/multimodal-test-log.md). E2B model misread a synthetic MUAC tape (returned Yellow on a 10.8 cm photo that should be Pink) with 0.95 confidence. The safety layer did not catch it — silent high-confidence multimodal misclassification. Architecture works; vision accuracy at E2B is not field-ready. | Mitigations queued: photo-derived confidence haircut, OCR pre-pass for numeric photos, retest at E4B |
| "Native function calling" capability advertised | We use prompt-engineered JSON output, not Ollama's tools API. Never benchmarked the two against each other. | Add tools-API backend path + side-by-side validity benchmark |
| "Android V2 with LiteRT" | Not in this repo. No `android/` directory. No APK was built or tested. | Build a minimum-viable Kotlin + LiteRT loader against `gemma-4-E4B-it.litertlm` from `litert-community` |
| R14 confidence floor at 0.4 | Hand-picked threshold. Gemma's self-reported confidence is a token the model chose to emit, not a calibrated probability. | Plot confidence vs correctness on ≥ 50 held-out scenarios; pick the threshold from the data |
| R13 keyword matcher is "negation-aware" | **Verified at v0.2** — 14 adversarial tests added in this push. One real bug was caught: cross-sentence negation carry-forward (e.g. "No vomits everything. Chest indrawing visible." was incorrectly suppressing "chest indrawing"). Fixed in `laptop/safety.py:_is_negated` by resetting the negation window at sentence boundaries (`.!?;\n`). 31/31 tests pass. | Continue adding stress cases as real CHEW notes surface them |
| HF Space is "browser-accessible verification" | True, but cold-start is 8–10 min on free-tier `cpu-basic`. Disclosed in the Space header. | Either upgrade to a paid GPU tier or pre-cache responses for the 4 canonical scenarios |
| Distribution outreach "drafted" (corrected from earlier "started") | 3 letters in `outreach/` with named contacts. **Not yet sent.** | Send immediately post-submission; log each in the contact files |

## What's missing for real CHW deployment in the field

Not technical bugs — gaps between "hackathon submission" and "running in an Anambra primary health centre".

1. **No clinical validation.** 4 chart-booklet scenarios is a development gate, not a clinical trial. A real deployment needs IRB review.
2. **No localisation.** Adaeze speaks Igbo / Pidgin / English. Priya speaks Hindi / Marathi. UI is English-only.
3. **No real device testing.** PRD targets Tecno Spark $80 Android. Never installed on any Android.
4. **No partnerships.** Outreach drafted ≠ WHO / NHM / NPHCDA endorsement.
5. **No regulatory positioning.** Gemma Terms of Use have safety-critical / medical clauses. README disclaims "not a medical device" but no legal review.
6. **No model version pinning** until v0.2 — `gemma4:e2b` is a tag, Ollama could silently update it.
7. **No CI** until v0.2 — anyone can break the safety layer and ship.
8. **No fallback / monitoring.** Some error handling in `laptop/app.py`; not stress-tested against OOM / malformed input / model crash.

## Distinguish: designed vs built vs tested vs proven

The internal honesty rule that drives this document:
- **Designed** — written in the PRD, exists as a plan only.
- **Built** — code exists in the repo, compiles, runs.
- **Tested** — exercised against eval scenarios or unit tests with logged results.
- **Proven** — used by a real CHW in a real clinic on real patients, with outcome data.

PocketTriage v0.1 is **built and tested** for the laptop path (Ollama + Apple Silicon), built-but-not-tested for the multimodal and E4B paths, and not-yet-built for the Android path. It is **not proven** anywhere. The README, landing, and writeup all say so.

---

## Sponsor track applications at submission

| Track | Applied? | Rationale |
|---|---|---|
| Main | Yes | Submission-eligible by default |
| Impact — Health & Sciences | Yes (primary) | WHO IMCI protocol; CHW deployment context; lived expertise of the author |
| Special Tech — Ollama | Yes | V1 backend is Ollama running `gemma4:e2b` locally; the demo + Space both go through this path; Modelfile + integration documented |
| Special Tech — LiteRT | **No** | No real-device APK built. Architecture wired in `notes/model-source.md` but the track rule is shipped-not-described |
| Special Tech — Unsloth | No | No fine-tune |
| Special Tech — Cactus | No | No E2B/E4B routing |
| Special Tech — llama.cpp | No | Architecturally blocked by the iSWA-attention bug on Gemma 4 GGUF |

Rationale doc: [`ai/sponsor-integration.md`](ai/sponsor-integration.md).
