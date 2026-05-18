# PocketTriage — Voiceover Clips (v2 · conversational)

Framework: PAS, inverted — open with a case + result, walk through what / where / evidence / how, close. Reads as one continuous talk, not six press-release sentences. Senior-engineer Demo-Day cadence — short fragments, specific numbers, no buzzwords.

Voice: Brian (ElevenLabs `nPczCjzI2devNBz1zQrb`).
Settings: stability **0.55**, similarity 0.65, style **0.15** — characterful, not flat-corporate.
Target: 6 clips, ~57s total speech, ~67s final video (≤ 3 min hackathon cap).

Mentions Gemma 4 + Ollama explicitly (we're applying for the Ollama track).

---

## 01-hook
*Frame: laptop running PocketTriage, S1 symptom typed, PINK result rendered, airplane-mode badge visible.*

> Here. Eleven-month-old. Cough. Chest indrawing. Refusing to drink. The model returns Pink, refer urgently. Ten seconds. Wi-Fi is off.

21 words. ~9 s.

## 02-context
*Frame: side-by-side — WHO IMCI chart-booklet page on the left, PocketTriage output on the right.*

> PocketTriage is the WHO IMCI chart booklet, as a phone tool. Gemma 4, locally, on Ollama. Same protocol, same Pink-Yellow-Green tiers. Just faster.

26 words. ~10 s.

## 03-where
*Frame: textured panel evoking a rural Nigerian primary-health-centre context, with "Anambra State · Nigeria · 2026" metadata.*

> Why offline. Anambra State, hours without power, two G if you're lucky. The chart booklet on the wall is still the only chart.

23 words. ~9 s.

## 04-evidence
*Frame: 4-row Phase 1 Gate table + airplane-mode tcpdump proof.*

> Phase one gate. Four canonical IMCI scenarios. Wi-Fi off, tcpdump running. Four out of four match the WHO protocol. Zero non-localhost packets. Reproducible from the repo.

27 words. ~11 s.

## 05-architecture
*Frame: 5-step pipeline — input, model, parse, safety, render — with "NOTHING LEAVES THE DEVICE" legend.*

> One path. Ollama runs Gemma 4 locally. Patient text never leaves the device. No server, no analytics. A keyword safety layer catches danger signs even when the model misses them.

30 words. ~12 s.

## 06-close
*Frame: PocketTriage outro card with URL and hackathon attribution.*

> PocketTriage. Open source, Apache 2.0. Built by a Nigerian medical intern. Repo's on GitHub. Take it.

17 words. ~7 s.

---

## Adversarial gate

- Hook opens with a concrete case + result, not a problem statement.
- Conversational fragments ("Here.", "Why offline.", "Phase one gate.") instead of slide-style declarative sentences.
- **Names "Ollama" twice** (clip 2 + clip 5) — Ollama Special Tech track is a $10K target.
- Specific numbers: 11 months, 4/4, zero packets, 10 seconds. No "leverages", "innovative", or "AI-powered".
- No failure modes / caveats in the video. Honesty lives in the README.

Words total: 144 → ~57 s speech → ~67 s with transitions (still ≤ 3 min hackathon cap).
ElevenLabs cost: ~720 chars ≪ 31K-char remaining budget.
