# Phase 4.7 Communication Pack — pre-submission checklist

Runs before clicking Submit on Kaggle. Every box must be true.

## Identity / pitch

- [x] 3-5 word pitch defined: **"Offline clinic in pocket"** (`ai/memory.md` §Communication Pack)
- [x] Tagline (≤ 12 words) defined: "Gemma 4 turns a $80 Android into an offline triage assistant for community health workers."
- [x] Audience defined in PRD §2 (Adaeze + Priya) — verified, not invented
- [x] Anti-personas explicit: US clinicians, hospital systems, patients themselves

## Artifacts present in repo

- [x] LICENSE (Apache 2.0)
- [x] README with Run-locally section, architecture diagram, safety arch, known limitations
- [x] CONTRIBUTING.md
- [x] CODE_OF_CONDUCT.md
- [x] .gitignore (covers `.env*`, `*.key`, `*.pem`, `keystore/`, `secrets/`)
- [x] SECURITY.md (canonical playbook from `hackathon-security-bootstrap.sh`)
- [x] PRD.md (source of truth)
- [x] CLAUDE.md (vibecoder + security blocks)
- [x] eval/scenarios.json (4 canonical IMCI cases)
- [x] eval/airplane-test-log.md (verified PASS 4/4 + zero packets)
- [x] outreach/who-digital-health.md
- [x] outreach/india-nhm-asha.md
- [x] outreach/nigeria-fmoh-phc.md
- [x] writeup/kaggle-writeup.md (1,419 words, under 1500 cap)
- [x] writeup/video-script.md
- [ ] writeup/cover-image.png — pending (spec in `writeup/cover-image.md`)
- [x] huggingface-space live URL — https://huggingface.co/spaces/yonko11/pockettriage (Docker Space, BUILDING at 16:37 UTC 2026-05-17)
- [ ] android/ APK build artifact — pending

## Banned-words scrub

Run on every submission-bound text file:

```bash
grep -i -E "(thorough|comprehensive|exhaustive|battle-tested|production-ready|bulletproof|rock-solid|game-changing|revolutionary|disruptive|seamless|unleash|leverag)" \
  writeup/kaggle-writeup.md writeup/video-script.md README.md outreach/*.md
```

- [x] Kaggle writeup — only hit is inside this checklist's own scrub command, not in the writeup body
- [x] Video script — only hits are inside the script's own scrub command + a recording-rule line that explicitly says NOT to use those words
- [x] README — clean (zero hits in the prose; "Apache 2.0" and "WHO IMCI 2014" are factual, not banned)
- [x] Outreach drafts — clean

## Link-checker

- [x] https://github.com/yonkoo11/pockettriage — returns 200 (verified `gh repo view yonkoo11/pockettriage`)
- [x] Hugging Face Space URL — https://huggingface.co/spaces/yonko11/pockettriage (verify it shows the Gradio UI after build completes; cold boot is 5-10 min)
- [ ] YouTube unlisted link — set after upload
- [x] WHO IMCI Chart Booklet (referenced in writeup) — public WHO PDF, current 2014 edition
- [x] LiteRT artifacts: `litert-community/gemma-4-E4B-it-litert-lm`, `litert-community/gemma-4-E2B-it-litert-lm` — public HF repos

## Demo CTA in incognito / fresh browser

- [ ] Open Hugging Face Space URL in a private window. No login wall. Result renders within 30 s of model warmup.
- [ ] GitHub README "Run locally" section: actually clone in a fresh terminal, follow the steps, app launches in ≤ 30 minutes. (Verified locally on 2026-05-17 during Phase 1 Gate work.)

## ElevenLabs phonetic rewrites (if synth narration used)

- [x] "PocketTriage" → "Pocket Triage"
- [x] "Gemma 4" → "Gemma four"
- [x] "LiteRT" → "Light R T"
- [x] "Ollama" → "Oh-lah-mah"
- [x] "IMCI" → spelled "I M C I"
- [x] "MUAC" → spelled "M U A C"
- [x] "NPHCDA" → spelled "N P H C D A"
- [x] "CHEW" → "chew" (rhymes with "few")

## Distribution timing

- [x] Outreach drafts written (3 named contacts each in `outreach/`)
- [ ] Outreach sent — trigger is the YouTube link going live AND the HF Space URL being green
- [ ] r/GlobalHealth post drafted — write before submit; post at the same time as Kaggle submission

## What I'm explicitly NOT claiming at submission

- "Production-ready" — replaced with "V1 of a real product, with verified Phase 1 Gate + safety layer + on-laptop demo. Android device validation pending."
- "Comprehensive" — replaced with "covers the 4 canonical IMCI scenarios + danger-sign keyword force + confidence floor + adult-condition refusal."
- "Validated for clinical use" — explicitly not. The README and writeup both say so.

## Submission-day operational

- [ ] `git status` clean before final push
- [ ] All commits pushed to `origin/master`
- [ ] HF Space rebuild triggered + verified green
- [ ] YouTube video set to "Unlisted" with the GitHub URL in the description
- [ ] Kaggle entry fields: title, tagline, GitHub URL, HF Space URL, YouTube URL, cover image upload
- [ ] Kaggle entry: select **Main + Health & Sciences Impact + Ollama Special Tech** (per `ai/sponsor-integration.md` Phase 4.5 verification)
- [ ] Kaggle entry: do **NOT** select LiteRT (no real-device APK in V1), Unsloth (no fine-tune), Cactus (no routing), llama.cpp (architecturally blocked)
- [ ] Save submission-confirmation.png after the Submit click
