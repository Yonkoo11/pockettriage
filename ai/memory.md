# PocketTriage — Memory

**Authoritative spec:** `/PRD.md`. This file is the session memory; the PRD is the source of truth.

## Phase 1 Gate (must pass before anything else)

**Core Action:** Community Health Worker enters patient symptoms (with airplane mode ON), and Gemma 4 E4B running on-device returns a WHO IMCI tier (Pink/Yellow/Green) + referral pathway in under 30 seconds.

**Success Test:** Run the 4 canonical IMCI scenarios from `eval/scenarios.json` with WiFi off. At least 3/4 return correct tier + pathway. Zero network requests observed in DevTools / Android profiler.

**Min Tech (V1):**
- Gemma 4 E4B (identifier verified in fix-plan Task 1)
- Ollama (laptop V1) + LiteRT (Android V2) — both load-bearing
- Gradio frontend with text + photo input
- WHO IMCI protocol as system prompt + RAG (per PRD R10–R12)
- Function-calling schema for `{tier, pathway, reasoning, confidence}`
- Safety layer R13–R16 (danger-sign keyword force-Pink, confidence floor, adult-condition refusal, non-dismissable disclaimer)

**NOT Phase 1:** Adult conditions, multi-language UI, voice, server-side anything, EHR, vitals capture, fine-tuning, intelligent routing, regulatory clearance, polish (all explicitly out-of-scope per PRD §8).

**Status:** [ ] NOT STARTED

---

## Hackathon Context (facts only)

- Event: The Gemma 4 Good Hackathon (Kaggle / Google DeepMind)
- URL: https://www.kaggle.com/competitions/gemma-4-good-hackathon
- Deadline: May 18, 2026, 11:59 PM UTC
- Total prize pool: $200,000 / 14 prize slots
- Judging weights: Impact 40 / Video 30 / Tech Depth 30
- Required deliverables: Writeup ≤ 1500 words + YouTube ≤ 3 min + public repo + live demo URL + cover image

## Tracks Applied For (per PRD §7)

| Track | Depth target | Status |
|---|---|---|
| Main Track | 5/5 | Apply |
| Impact: Health & Sciences | 5/5 | Apply (primary impact framing) |
| Special Tech: LiteRT | 5/5 | Apply |
| Special Tech: Ollama | 4/5 | Phase 4.5 decision |
| Special Tech: Unsloth | 4/5 | Phase 4.5 decision (stretch) |
| Special Tech: Cactus | 4/5 | Phase 4.5 decision (stretch) |
| Special Tech: llama.cpp | 3/5 ceiling | DO NOT APPLY |

---

## Chosen Idea — PocketTriage

**Pitch (3-5 words):** "Offline clinic in pocket"

**Audience (per PRD §2):** Community Health Workers in low-resource settings — primary persona Adaeze (Nigerian CHEW, Anambra State, $90 Tecno Spark, 2G or no signal), secondary persona Priya (Indian ASHA, Maharashtra, Hindi-first). Anti-personas: US clinicians, hospital systems, patients themselves.

**Mechanism:** CHW captures patient vitals + symptom description + optional photo on a phone or laptop with airplane mode on. Gemma 4 E4B running locally via LiteRT (Android) or Ollama (laptop) classifies the case against the WHO IMCI protocol (cough/diarrhea/fever/ear/malnutrition/danger signs), returns an acuity tier (Pink/Yellow/Green) and a structured referral pathway via Gemma 4's native function-calling. Nothing leaves the device.

**Distribution path (per PRD R25–R29 — STARTED DURING BUILD, not after):**
- Public Hugging Face Space (R26)
- Public GitHub with Apache 2.0 license (R25)
- r/GlobalHealth submission post (R27)
- Direct outreach: WHO Digital Health, India NHM ASHA, Nigeria FMoH PHC (R28, logged in `outreach/`)
- awesome-localllm or awesome-medical-ai GitHub list PR (R29)

---

## Sponsor Depth Plan (PRD §3.3)

| Gemma 4 surface | V1 depth | V2 depth |
|---|---|---|
| Gemma 4 E4B model | 5/5 (Ollama tag) | 5/5 (LiteRT .task) |
| Multimodal (vision) | 4/5 (symptom photo input) | 4/5 |
| Native function calling | 4/5 (referral pathway FC schema) | 4/5 |
| LiteRT runtime | Stretch | 5/5 (Android demo, real device) |
| Ollama runtime | 4/5 (Modelfile + integration) | 4/5 |
| Unsloth fine-tune | Not in V1 | 4/5 if shipped, else don't apply |
| Cactus routing | Not in V1 | 4/5 if shipped, else don't apply |

---

## Competitive Landscape (named precedents per PRD §0)

- **Guardian/Atlas** (Meta Llama Impact London 2024) — NHS clinical triage, $50K + $500K grant pathway. Same archetype.
- **Hearti** (TreeHacks 2025) — CV/ML for congenital heart disease. Healthcare track winner.
- **postvisit.ai** (Anthropic Built with Opus 4.6, 3rd) — patient post-visit understanding, built by cardiologist.
- **CrossBeam** (Anthropic Built with Opus 4.6, 1st) — domain-expert attorney shipping AI regulatory tool.

## Fatal Flaws (mitigated per PRD §9 Risk Register)

1. Liability for missed diagnoses → mitigated by R7 non-dismissable disclaimer + R13 danger-sign force-Pink + R14 confidence floor + Apache 2.0 warranty disclaimer
2. FDA SaMD / regulatory → mitigated by targeting non-US CHW context (WHO programs); no clinical claims in writeup
3. Photo accuracy on darker skin tones → explicitly disclosed in README + writeup; photo framed as supplementary signal
4. Phantom-validation risk → the WHO IMCI corpus is real and public; the model is a real open weight; the Android device is real; no simulation

---

## Architecture Notes (per PRD §6)

- **V1 laptop stack:** Python + Gradio + Ollama running Gemma 4 E4B (tag TBD Task 1) + WHO IMCI RAG + Pillow + JSON FC schema
- **V2 Android stack:** Kotlin + LiteRT (Google AI Edge) loading Gemma 4 E4B `.task` file + CameraX + same JSON FC schema
- **No backend, no server, no analytics, no telemetry, no phone-home.**

---

## Communication Pack (Phase 4.7 — pre-submission per PRD §10)

- 3-5 word pitch: "Offline clinic in pocket"
- Tagline (≤ 12 words): "Gemma 4 turns a $80 Android into an offline triage assistant for community health workers."
- Video structure (≤ 2 min ideal, ≤ 3 min cap): Problem (Nigerian clinic, no signal, paper IMCI chart) → Solution (Gemma 4 E4B on-device) → Demo (airplane mode visible, real IMCI scenario typed, photo attached, structured pathway returned) → Team (Nigerian medical intern, lived context)
- Anti-slop: no "revolutionary / game-changing / disruptive"; no reused screenshots across clips; subtitles on; ElevenLabs voice rewrite for any narration phonetic per `feedback_elevenlabs_pronunciation.md`
- Distribution post timed with the YouTube link going live
