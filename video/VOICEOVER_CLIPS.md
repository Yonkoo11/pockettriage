# PocketTriage — Voiceover Clips

Framework: PAS (Problem-Agitation-Solution), inverted — hook with solution working, then context, then evidence/architecture, then CTA.

Voice: Brian (ElevenLabs `nPczCjzI2devNBz1zQrb`).
Settings: stability 0.82, similarity 0.65, style 0.03 (deliberate pacing).
Target: 6 clips, ~55s total speech, ~65s final video.

---

## 01-hook
*Frame: laptop running PocketTriage, S1 symptom typed, PINK result rendered, Airplane Mode badge visible.*

> Severe pneumonia. WHO IMCI protocol. Pink. Refer urgently. The model is Gemma 4 on this laptop. Wi-Fi off.

18 words.

## 02-context
*Frame: side-by-side — WHO IMCI chart-booklet page on the left, the same PocketTriage output on the right.*

> PocketTriage is the WHO IMCI chart booklet as a phone tool. Gemma 4 runs on the device. Same protocol. Same action. Faster.

23 words.

## 03-where
*Frame: textured panel evoking a rural Nigerian primary-health-centre context, with "Anambra State · Nigeria · 2026" metadata.*

> Anambra State, Nigeria. Patchy two-G. Hours without power. This is where the chart booklet still rules.

19 words.

## 04-evidence
*Frame: 4-row Phase 1 Gate table — S1 Pink, S2 Yellow, S3 Yellow, S4 Green, all PASS — and the airplane-mode tcpdump proof underneath.*

> Four canonical scenarios from the chart booklet. Wi-Fi off. Tcpdump running. Four out of four agree with the WHO protocol. Zero packets.

23 words.

## 05-architecture
*Frame: 5-step pipeline — input, model, parse, safety, render — with "NOTHING LEAVES THE DEVICE" legend.*

> One narrow path. The model runs locally. The patient text never leaves the device. No server. No analytics. No fallback to anyone's cloud.

24 words.

## 06-close
*Frame: PocketTriage outro card with URL and hackathon attribution.*

> PocketTriage. Built by a Nigerian medical intern. Open source. On GitHub now.

13 words.

---

## Adversarial gate

- Hook leads with the product working (PINK + refer urgently), not a hypothetical problem.
- No buzzwords ("revolutionary", "AI-powered", "leverage").
- No caveats or failure modes.
- Every clip is technically verifiable: every Pink/Yellow/Green claim maps to `eval/airplane-test-log.md` and `laptop/safety.py`.
- Single CTA in clip 6, no "thank you" / "we hope you enjoyed".

Words total: 120. ElevenLabs cost: ~600 characters across all 6 clips → well inside the 31K-char remaining budget.
