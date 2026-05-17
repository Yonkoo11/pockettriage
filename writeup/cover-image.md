# Cover image — specification

**Target:** 1920×1080 PNG (16:9), submitted as the Kaggle entry cover.
**Status:** Not generated yet (Gemini image-gen free-tier quota exhausted at 14:50 UTC on 2026-05-17). Two paths:

## Path A — regenerate with nano-banana-pro (recommended, no shoot needed)

Once quota resets (~24h) or with a paid Gemini API key, run the prompt below. Output path: `writeup/cover-image.png`.

```
A photorealistic, dignified scene: a young Black African community health
worker (woman, mid-30s, in a simple blue uniform) sits at a wooden table
outside a rural primary health centre at golden hour. She holds a low-end
Android smartphone in both hands, looking at the screen with focused
concentration. The phone screen displays a clean medical app interface
with a red "PINK" badge visible. Next to her on the table: a printed
WHO IMCI chart booklet, a stethoscope, a MUAC arm-circumference tape.
In the soft background: simple clinic wall, a mother holding a small
child seated on a bench waiting. Warm natural light, documentary
photography style, no text overlays except what is on the phone screen,
no logos, authentic Nigerian rural primary care aesthetic.

Aspect: 16:9. Resolution: 2K. Style: documentary, no AI artifacts.
```

## Path B — real photograph

If quota is unavailable and time permits, the strongest option is an actual photo from a Nigerian primary health centre with the CHEW's consent.

Constraints if shot for real:
- The phone screen must show the actual PocketTriage UI (Pink badge, pathway visible).
- The chart booklet must be the WHO IMCI 2014 (public, available as PDF).
- Faces of patients or children must be obscured or replaced with a mannequin / role-played adult.
- Written model release from the CHEW required for the public submission.

## Anti-slop checklist before upload

- [ ] No "AI-generated" watermark visible
- [ ] No fake or implausible medical detail (e.g. stethoscope held wrongly, MUAC tape sized wrongly)
- [ ] No US-clinic / Caucasian-doctor aesthetic
- [ ] Phone is a budget Android (NOT an iPhone, NOT a flagship)
- [ ] Image is not reused from anywhere else in the submission (video uses different frames)

## Fallback if neither path lands before submission

Generate a typographic cover instead: black background, large white serif "PocketTriage", subhead "Offline clinic in pocket", sub-subhead "Gemma 4 · WHO IMCI · Apache 2.0". This is acceptable per the Kaggle entry requirements (no image-style mandate) and is better than a slop-looking AI image.
