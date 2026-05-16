# Fix Plan — PocketTriage

**Source spec:** `/PRD.md`. Every task acceptance criterion maps to a numbered PRD requirement.

## Phase 0 — Verify open questions before building (PRD §11)

- [ ] **Task 0.1** Verify exact Gemma 4 E4B Ollama tag
  - Acceptance: `ollama pull <tag>` succeeds. Document tag in `notes/model-source.md`.
  - PRD: §11 Q1; RK-1
  - If E4B unavailable, fall back to current Gemma edge model (e.g. Gemma 3n E4B) and update PRD §6 ADR-1 + §11 + Section 4 model references in one save point.

- [ ] **Task 0.2** Verify LiteRT `.task` file URL for Gemma 4 E4B (or current edge variant)
  - Acceptance: `.task` file downloads and `file --mime-type` returns a valid LiteRT artifact. Document URL in `notes/model-source.md`.
  - PRD: §11 Q2; RK-2

- [ ] **Task 0.3** Verify native function-calling works on E4B parameter count
  - Acceptance: Run a smoke prompt asking the model to emit JSON matching `schema.json`; parses cleanly.
  - PRD: §11 Q3; if FC unavailable on E4B, switch to constrained-decoding JSON output and update PRD §6 ADR-4 in same save point.

- [ ] **Task 0.4** Verify multimodal (photo input) works on E4B
  - Acceptance: Send a test medical image to the model with `describe what you see`; output is coherent and references the image.
  - PRD: §11 Q4; if multimodal unavailable on E4B, move photo input to V2 with 26B/31B (likely unaffordable on-device) OR drop photo input from V1 and update PRD R2 + R6.

- [ ] **Task 0.5** Find LiteRT Gemma 4 reference Android app or sample
  - Acceptance: Working sample identified, fork-base for `/android` set up.
  - PRD: §11 Q5

---

## Phase 1 — Core action passes airplane-mode test (PRD §4.1)

- [ ] **Task 1.1** Bare CLI loads Gemma 4 E4B locally
  - Acceptance: `python infer.py "fever 39C, child age 3, lethargic"` returns Gemma's text reply with WiFi off
  - PRD: R3, R9
  - Files: `laptop/infer.py`

- [ ] **Task 1.2** WHO IMCI canonical scenarios for eval
  - Acceptance: `eval/scenarios.json` contains 4 cases with ground-truth tier + pathway, drawn from WHO IMCI chart booklet
  - PRD: R12; §3.2
  - Files: `eval/scenarios.json`, `who-imci/protocol-summary.md`

- [ ] **Task 1.3** System prompt steers Gemma 4 to return tier + pathway
  - Acceptance: Manual eval — 3/4 scenarios return correct Pink/Yellow/Green tier in parseable format
  - PRD: R4, R12, §3.2
  - Files: `laptop/system-prompt.md`, `laptop/infer.py`

- [ ] **Task 1.4** Function-calling schema for referral pathway
  - Acceptance: Model emits JSON matching `{tier, pathway, reasoning, confidence}` on all 4 scenarios
  - PRD: R5, ADR-4
  - Files: `laptop/schema.json`, `laptop/infer.py`

- [ ] **Task 1.5** Airplane-mode integration test
  - Acceptance: WiFi off + cellular off. All 4 scenarios run. 3/4 pass. Zero network requests in DevTools.
  - PRD: R9, NFR2; §3.2
  - Files: `eval/airplane-test-log.md`

**PHASE 1 GATE — do not advance until Task 1.5 passes.**

---

## Phase 2 — Data flows + safety layer (PRD §4.2, §4.3)

- [ ] **Task 2.1** Photo input via Gemma 4 multimodal
  - Acceptance: Upload symptom photo, model output reasoning references the image content
  - PRD: R2, R6
  - Files: `laptop/multimodal.py`

- [ ] **Task 2.2** WHO IMCI retrieval (RAG)
  - Acceptance: Model output cites the relevant IMCI rule for each classification
  - PRD: R10, R11
  - Files: `laptop/rag.py`, `who-imci/protocol-full.md`, `who-imci/danger-signs.md`

- [ ] **Task 2.3** Safety layer — danger-sign force-Pink (R13)
  - Acceptance: Test inputs containing "convulsions" / "unconscious" / "severe respiratory distress" / "severe dehydration" force tier=Pink regardless of model output
  - PRD: R13
  - Files: `laptop/safety.py`, `eval/safety-cases.md`

- [ ] **Task 2.4** Safety layer — confidence floor (R14)
  - Acceptance: Test inputs with model confidence < 0.4 append "Escalate to medical officer" to pathway
  - PRD: R14
  - Files: `laptop/safety.py`, `eval/safety-cases.md`

- [ ] **Task 2.5** Safety layer — adult-condition refusal (R15)
  - Acceptance: Test inputs with adult-specific conditions return refusal text instead of triage
  - PRD: R15
  - Files: `laptop/safety.py`, `eval/safety-cases.md`

- [ ] **Task 2.6** Gradio UI with text + photo + result card + non-dismissable disclaimer banner (R7)
  - Acceptance: Local web UI runs, all R1–R7 fields render
  - PRD: R1, R2, R6, R7
  - Files: `laptop/app.py`

- [ ] **Task 2.7** Error handling — model load fails, malformed input
  - Acceptance: Test cases for model-not-found / corrupted-input / oversized-photo return user-friendly error, not crash
  - PRD: §9 RK-9; Skill Rule #4 (final-product error handling)
  - Files: `laptop/app.py`, `eval/error-cases.md`

---

## Phase 3 — Product complete: ship the V1 (PRD §4.4, §4.6)

- [ ] **Task 3.1** Public GitHub repo with Apache 2.0 LICENSE, README, CONTRIBUTING.md, CODE_OF_CONDUCT.md
  - Acceptance: Repo public on github.com, all 4 files present, README has "Run locally" section ≤ 30 min from clean clone
  - PRD: R25, NFR7; Skill Rule #4
  - Files: `LICENSE`, `README.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`

- [ ] **Task 3.2** Live demo on Hugging Face Spaces
  - Acceptance: Public URL returns the same output as local, no login required, runs the full R1–R9 flow
  - PRD: R26; Skill Rule #4
  - Files: `huggingface-space/`

- [ ] **Task 3.3** Android APK build through LiteRT (PRD R17–R21)
  - Acceptance: APK installs on Tecno Spark or equivalent Android 12+ phone, loads Gemma 4 E4B via LiteRT, runs R1–R9 flow on-device, airplane-mode test passes on 1 scenario
  - PRD: R17, R18, R19, R20, R21; track LiteRT
  - Files: `android/app/`, `android/README-android.md`

- [ ] **Task 3.4** Distribution outreach — START during build (per Skill Rule #4)
  - Acceptance: 3 specific outreach messages sent, logged in `outreach/`. WHO Digital Health, India NHM ASHA, Nigeria FMoH PHC — one named contact each.
  - PRD: R28; Skill Rule #4
  - Files: `outreach/who-digital-health.md`, `outreach/india-nhm-asha.md`, `outreach/nigeria-fmoh-phc.md`

- [ ] **Task 3.5** awesome-localllm or awesome-medical-ai PR
  - Acceptance: One PR opened against a public awesome-list repo with PocketTriage entry
  - PRD: R29

- [ ] **Task 3.6** Eval expanded — latency + airplane-mode logs
  - Acceptance: `eval/latency.md` (laptop < 8s per case), `eval/android-bench.md` (Android < 30s per case), `eval/airplane-test-log.md` (full 4 scenarios, zero network requests)
  - PRD: §3.2

- [ ] **Task 3.7** Phase 4.5 sponsor depth verification
  - Acceptance: `ai/sponsor-integration.md` re-scores each track at actual shipped depth. Any track < 4/5 dropped from submission.
  - PRD: §7; Skill Rule #4

---

## Phase 3 stretch — apply for additional tracks only if shipped at ≥ 4/5

- [ ] **Task 3.S1** Ollama track — publish Modelfile + integration documented in README
  - Acceptance at Phase 4.5: depth ≥ 4/5; if not, do not apply for Ollama track
  - PRD: §7.4

- [ ] **Task 3.S2** Unsloth track — LoRA fine-tune on synthesized IMCI Q&A corpus
  - Acceptance at Phase 4.5: weights published on HF, eval shows ≥ 5% accuracy improvement on 4 canonical scenarios; if not, do not apply
  - PRD: R22; §7.4

- [ ] **Task 3.S3** Cactus track — E2B/E4B intelligent routing
  - Acceptance at Phase 4.5: routing visible in live demo; if not, do not apply
  - PRD: R23; §7.4

---

## Phase 4 — Polish + submit (PRD §10 Submission Checklist)

- [ ] **Task 4.1** Video script + recording
  - Acceptance: Script ≤ 2 min target, ≤ 3 min cap; recorded with phone visible, airplane mode visible in status bar, real IMCI scenario, lived-context narration
  - PRD: §3.1, §10
  - Files: `writeup/video-script.md`, YouTube link

- [ ] **Task 4.2** Kaggle Writeup ≤ 1500 words
  - Acceptance: All sections (problem, solution, architecture, sponsor integrations one-paragraph-each, ethical considerations, distribution) covered. Under track "Health & Sciences".
  - PRD: §10
  - Files: `writeup/kaggle-writeup.md`

- [ ] **Task 4.3** Cover image
  - Acceptance: 1920×1080 PNG showing the product in clinical context (real or stylized)
  - PRD: §10
  - Files: `writeup/cover-image.png`

- [ ] **Task 4.4** Phase 4.7 Communication Pack checklist
  - Acceptance: All boxes true. Banned-words scrub passes. Link-checker returns 200 on every URL. Demo CTA tested in incognito.
  - PRD: §10
  - Files: `writeup/comm-pack-checklist.md`

- [ ] **Task 4.5** Final submit on Kaggle
  - Acceptance: Writeup saved, attachments attached (YouTube, GitHub, HF Space, Android APK link), "Submit" clicked, confirmation screenshot saved
  - PRD: §10
  - Files: `writeup/submission-confirmation.png`

---

## Completed
(builder fills this in as tasks ship)
