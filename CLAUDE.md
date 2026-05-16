# PocketTriage — CLAUDE.md

**Source of truth:** `/PRD.md`. This file derives from it. If they disagree, the PRD wins.

## Vibecoder Mode

### Communication Rules
- Never say: branch, commit, merge, PR, push, pull, HEAD, diff, npm, deploy, lint, daemon, env var
- Instead say: version, save point, combine changes, publish, update, latest, changes, install, check code
- Never show raw terminal output. Summarize in one sentence.
- Never show error messages directly. Say what happened and what you're doing to fix it.
- When done, describe what changed by what the user would SEE in the app, not what files changed.

### Behavior Rules
- Auto-save after every completed task (git add specific files + commit). Never ask "should I commit?"
- If you need to create a version, just do it silently.
- If tests fail, fix them without explaining test frameworks.
- After each task: update ai/progress.md with a "What Changed (Plain English)" section.
- Keep all explanations to 1-3 sentences. If the user wants more detail, they'll ask.

---

## Final-Product Build (Enforced — Skill Rule #4)

This project ships as the V1 of a real product. NOT a hackathon prototype. Banned phrasing anywhere in the build or submission: "hackathon prototype", "demo-grade", "we'd polish for production", "POC scope", "MVP for the demo", "ship it later", "fake data for now".

Required production artifacts at submission:
- Apache 2.0 LICENSE in repo root
- README with reproduce-this instructions (clean clone → demo in ≤ 30 min)
- CONTRIBUTING.md + CODE_OF_CONDUCT.md
- Live demo URL (Hugging Face Space) accessible without login
- Working APK on real Android device for LiteRT track
- Real distribution outreach started (specific messages sent to specific communities, logged in `outreach/`)
- Safety layer per PRD R13–R16 active in live demo
- Error handling for offline / model-load-fail / malformed-input verified

## Phase 1 Gate (must pass before anything else)

**Core Action:** A community health worker enters patient symptoms (with airplane mode ON), and Gemma 4 E4B running on-device returns a WHO IMCI tier (Pink/Yellow/Green) + referral pathway in under 30 seconds.

**Success Test:** Four canonical IMCI scenarios run with WiFi off. At least 3/4 return the correct tier and pathway. Zero network requests observed.

**Status:** NOT STARTED

---

## Build Order (no skipping)

1. **Phase 1 — Core action.** Gemma 4 E4B running locally + minimal text-only Gradio that returns IMCI tier for 4 canonical scenarios. Airplane-mode test passes.
2. **Phase 2 — Data flows.** WHO IMCI protocol fully loaded (cough, diarrhea, fever, ear, malnutrition, danger signs). Photo input wired. Function-call schema returns structured JSON. Safety layer R13–R16 active.
3. **Phase 3 — Product complete.** Public Hugging Face Space live. Public GitHub with Apache 2.0 + README + CONTRIBUTING. Android V2 APK runs on a real phone via LiteRT, B-roll recorded. Distribution outreach started (3 logged messages in `outreach/`).
4. **Phase 4 — Polish + submit.** Video edit ≤ 3 min, Kaggle Writeup ≤ 1500 words under Health & Sciences track, cover image, Phase 4.7 Communication Pack checklist passes.

---

## Hackathon Context (facts only, no scoping language)

- Event: The Gemma 4 Good Hackathon (Kaggle / Google DeepMind)
- Deadline: May 18, 2026, 11:59 PM UTC
- Total prize pool: $200,000 across 14 prize slots
- Judging weights: Impact 40 / Video 30 / Tech Depth 30

## Tracks Applied For (commit per Phase 3.5)

| Track | Depth target | Status |
|---|---|---|
| Main Track | 5/5 | Apply — eligible by default |
| Impact: Health & Sciences | 5/5 | Apply — primary impact framing |
| Special Tech: LiteRT (Google AI Edge) | 5/5 | Apply — Android V2 is load-bearing |
| Special Tech: Ollama | 4/5 reachable | Phase 4.5 decision — apply if Modelfile + integration shipped |
| Special Tech: Unsloth | 4/5 reachable | Phase 4.5 decision — apply if LoRA + eval shipped |
| Special Tech: Cactus | 4/5 reachable | Phase 4.5 decision — apply if E2B/E4B routing shipped |
| Special Tech: llama.cpp | 3/5 ceiling | DO NOT APPLY |

Per Skill Rule #4: apply only to tracks where shipped depth is ≥ 4/5 verified at Phase 4.5.

## Research Base

- `~/Projects/IDEAS-SUMMARY.md` — file #57 (healthcare navigation), #46 (caregiver), #111 (insurance appeal — adjacent)
- `~/Projects/hackathon-winners/ARCHETYPES.md` — B4 (Accessibility Healthcare), B6 (AI Regulatory), A4 (Open-Source Public Good)
- Named precedents: Guardian/Atlas (NHS Llama Impact), Hearti (TreeHacks 2025 Healthcare), postvisit.ai (Anthropic Opus 4.6 3rd), CrossBeam (Opus 4.6 1st)
