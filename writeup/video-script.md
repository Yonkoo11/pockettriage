# PocketTriage — Video Script

**Target duration:** 2 minutes 0 seconds (hard cap 3:00).
**Format:** 1920×1080, 30 fps, subtitles burned in (English).
**Voice:** Mustapha (first person — Nigerian medical intern. Authentic accent kept; no ElevenLabs synthesis. If overdubbed, ElevenLabs voice with phonetic rewrite of brand names per pronunciation rules: "PocketTriage" → "Pocket Triage", "Gemma 4" → "Gemma four", "LiteRT" → "Light R T", "Ollama" → "Oh-lah-mah", "IMCI" → "I M C I", "MUAC" → "M U A C", "NPHCDA" → "N P H C D A", "CHEW" → "chew" → spell "C H E W".)

---

## Frame plan (no repeated screenshots)

| Time | Visual | Voiceover |
|---|---|---|
| 0:00 – 0:08 | Wide shot of a primary health centre exterior in a low-resource setting (real photo from Anambra or stock). Title card lower-third: **PocketTriage — Offline clinic in pocket** | "This is a primary health clinic in rural Nigeria. The internet is patchy. The phone signal is two bars on a good day." |
| 0:08 – 0:18 | Close-up of a CHEW reading the paper WHO IMCI Chart Booklet. Pages 5 and 12 visible. | "The community health worker uses this — the WHO Integrated Management of Childhood Illness chart booklet. It is the global standard for paediatric triage. It works. But it is slow." |
| 0:18 – 0:30 | Cut to laptop screen showing the Gradio UI of PocketTriage. Airplane-mode icon visible in the macOS menu bar (top right). Type the S1 scenario character by character (keyboard-cam optional). | "PocketTriage is the IMCI chart booklet as a phone tool. Gemma 4 runs on the device. Nothing leaves the laptop. Watch — airplane mode is on, top of the screen." |
| 0:30 – 0:45 | UI hits Triage button. Spinner. Then the result card animates in: red Pink badge, pathway text, IMCI reasoning, safety flag. Highlight the danger-sign safety flag with a green check overlay. | "Eleven-month-old. Cough three days. Chest indrawing. Refuses to drink. The model says Pink — severe pneumonia, refer urgently. The keyword safety layer caught the danger sign independently and forced Pink even if the model had been wrong." |
| 0:45 – 1:00 | Cut to the WHO IMCI chart booklet open to the severe pneumonia page side-by-side with the PocketTriage pathway output. Pan from book to screen. | "This is the WHO IMCI chart for severe pneumonia. This is what PocketTriage just returned. Same protocol. Same action. Two seconds, not five minutes." |
| 1:00 – 1:20 | Three quick cuts of the other canonical scenarios running: S2 dehydration → Yellow; S3 malaria → Yellow; S4 cold → Green. Each result card is held for ~5 seconds. Caption: "4 / 4 IMCI canonical scenarios. Airplane mode. Zero network packets." | "I ran the four canonical scenarios from the chart booklet with the network completely off. Four out of four agree with the WHO protocol. Tcpdump captured zero packets." |
| 1:20 – 1:35 | Show the `eval/airplane-test-log.md` file open in an editor, with the verification-B section visible (the `wc -l /tmp/airplane-net.log` → 0 line highlighted). | "This is the verification log in the repo. Zero non-localhost packets during inference. Anyone can reproduce it — clone the repo, turn off the network, run the eval." |
| 1:35 – 1:50 | Final card: about the team. My name + photo + medical-intern context. Logo of the Gemma 4 Good Hackathon. Apache 2.0 badge. | "I am Mustapha, a medical intern in Nigeria. I am from the place this tool is for. The product is open-source under Apache two point oh. Outreach drafted to the WHO, the Indian NHM, and the Nigerian NPHCDA — sent the moment the demo link goes live." |
| 1:50 – 2:00 | Closing card: URL, GitHub, Hugging Face Space, "Built for the Gemma 4 Good Hackathon — Health & Sciences track. May 2026." | "PocketTriage. Offline clinic in pocket. Built on Gemma 4. For the workers who already do this work — just faster." |

---

## Recording checklist (must-haves)

- [ ] Airplane mode visibly ON in every shot of the laptop
- [ ] At least one shot of the real WHO IMCI chart booklet (or a clearly-marked print of the public PDF) side-by-side with the app output
- [ ] At least one shot of a Nigerian / South-Asian primary-health context (NOT a US clinic, NOT a stock-photo Caucasian doctor)
- [ ] At least one shot of the `eval/airplane-test-log.md` evidence
- [ ] Subtitles burned in for the entire voiceover
- [ ] No music with vocals (royalty-free instrumental only)
- [ ] No reuse of the same screenshot across multiple clips (per `feedback_demo_video_distinct_frames`)
- [ ] No phrases: "revolutionary", "game-changing", "disruptive", "AI-powered" (unless contextual), "next-generation"
- [ ] The non-bypassable disclaimer banner visible in at least one full app shot
- [ ] End-card has the live demo URL spelled out, not just a logo
- [ ] **NO Android phone footage.** The LiteRT track is not in this submission. Filming a phone demo would imply a depth we did not ship.

## What I'm explicitly NOT doing in the video

- No staged "this is changing African healthcare" framing. I show the chart booklet next to the screen and let the substitution speak for itself.
- No anonymous testimonials. No fake CHEW endorsement clip.
- No demos of the photo input on a real patient (consent + privacy issue). Photo input is shown via a publicly-licensed dermatology image or an MUAC-tape demo on a mannequin / hand.

## Banned-words scrub before upload

Run before publishing the YouTube unlisted draft:

```
grep -i -E "(thorough|comprehensive|exhaustive|battle-tested|production-ready|game-changing|revolutionary|disruptive|seamless|unleash|leverag)" writeup/video-script.md
```

Expect zero hits.
