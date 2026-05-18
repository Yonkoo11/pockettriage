# PocketTriage — Voiceover Clips (v3 · conversational, dev-teaching)

Framework: senior engineer explaining their project to a technical audience.
- Open with what it is + what problem it solves (per user direction).
- Walk through demo → context → evidence → architecture → close.
- **Full conversational sentences**, not punctuation-heavy fragments.
- No staccato single-word lines (those sound robotic on ElevenLabs).
- Words shaped for natural Brian delivery: connecting words, soft transitions, no abbreviations that synth-read awkwardly.

Voice: Brian (`nPczCjzI2devNBz1zQrb`).
Settings: stability **0.42**, similarity 0.7, style **0.28**, use_speaker_boost true, model **eleven_turbo_v2_5** (more natural cadence than multilingual_v2).
Target: 6 clips, ~85 s speech, ~95 s final video (still well under the 3-min cap).

Frame order updated: intro/problem first, then the live demo. Clip 1 now uses the Anambra scene; the laptop-with-PINK is clip 2.

---

## 01-intro
*Frame: Anambra State context scene — "Where the chart booklet is the only chart".*

> Let me walk you through PocketTriage. It's a paediatric triage assistant built on Gemma 4 that runs entirely on the device. The problem we're solving is real: community health workers in rural Nigeria, where the internet drops out for days at a time, and the only clinical reference is the chart booklet hanging on the wall.

55 words. ~22 s.

## 02-product
*Frame: laptop running PocketTriage, S1 case typed, PINK result rendered.*

> Here's how it works in practice. The worker types in a patient's symptoms, and the model returns one of three tiers — Pink for refer urgently, Yellow for facility care, Green for home care — together with the matching pathway from the WHO IMCI protocol. Same protocol the worker already follows, just considerably faster.

53 words. ~22 s.

## 03-context
*Frame: side-by-side WHO chart booklet ↔ PocketTriage output.*

> And it works completely offline by design. The patient text never leaves the device. There's no server, no analytics, and no fallback to anyone else's cloud.

26 words. ~11 s.

## 04-evidence
*Frame: 4-row Phase 1 Gate table + tcpdump proof.*

> For our gate, I ran four canonical scenarios from the IMCI chart booklet, with the Wi-Fi disabled and tcpdump capturing anything that left the machine. All four cases matched the WHO protocol exactly, and tcpdump recorded zero packets going anywhere other than localhost. The whole thing is reproducible from the repository.

51 words. ~21 s.

## 05-architecture
*Frame: 5-step pipeline (input → model → parse → safety → render).*

> Architecturally it's one narrow path. Ollama runs Gemma 4 locally, the JSON output is validated and coerced, and then a keyword safety layer enforces four invariants — including forcing a Pink classification whenever a general danger sign appears, even when the model has missed it.

44 words. ~19 s.

## 06-close
*Frame: PocketTriage outro card with URLs and hackathon attribution.*

> PocketTriage is open source under Apache 2.0, built by a Nigerian medical intern. The repository is on GitHub. Take a look.

22 words. ~9 s.

---

## ElevenLabs-friendliness notes (anti-slop word list)

Words removed because Brian reads them awkwardly:
- "Here." / "Pink." / "Phase one gate." → expanded into full sentences
- "two G" → replaced with "internet drops out for days at a time" (more natural prose)
- "WiFi off, tcpdump running" → expanded: "with the Wi-Fi disabled and tcpdump capturing..."
- "Repo's on GitHub" → "The repository is on GitHub."

Words kept because they read fine:
- "Gemma 4", "WHO IMCI", "Ollama", "JSON", "Apache 2.0", "tcpdump"

## Adversarial gate

- **Intro names product + problem in first sentence** (per user direction).
- All six clips are complete sentences a senior dev would actually speak.
- Names Gemma 4 (clips 1, 5) + Ollama (clip 5) for the Ollama track.
- Names "WHO IMCI" / "WHO protocol" three times (Health & Sciences track).
- Specific numbers: four out of four, zero packets, three tiers, four invariants.

Words total: 251. ElevenLabs cost ≈ 1,250 characters — fits in the 31K remaining budget.
