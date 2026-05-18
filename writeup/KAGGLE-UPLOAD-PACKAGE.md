# Kaggle submission — copy-paste package

Everything you need is below. Open https://www.kaggle.com/competitions/gemma-4-good-hackathon → click **New Writeup**. Walk the form top to bottom; the labels below match the form labels exactly.

---

## 1. Verify identity

Click the "Verify now" banner first. The Submit button stays disabled until ID is verified.

## 2. Title  (0 / 80)

```
PocketTriage — offline WHO IMCI paediatric triage on Gemma 4
```

(58 / 80 chars.)

## 3. Subtitle  (0 / 140)

```
Gemma 4 runs on the device. Pink / Yellow / Green tier + referral pathway. Nothing leaves the device. Built by a Nigerian medical intern.
```

(140 / 140 — at the limit. If Kaggle rejects, drop the last sentence.)

## 4. Card and Thumbnail Image  (560 × 280)

Upload: **`writeup/card-thumbnail.png`** (already 560 × 280, 24 KB).

A photoreal alternative is in `writeup/cover-image.md` — paste that prompt into ChatGPT / Gemini / Midjourney if you want to regenerate with real photography. For submission the typographic card above is competition-ready and disambiguates at 120 × 68 thumbnail size.

## 5. Submission Tracks

Tick exactly these three:

- [x] **Main Track**
- [x] **Impact Track — Health & Sciences**
- [x] **Special Technology Track — Ollama**

Do **NOT** tick LiteRT (no Android device demo shipped), Unsloth (no fine-tune), Cactus (no routing), llama.cpp (architecturally blocked). Rationale in `ai/sponsor-integration.md`.

## 6. Media Gallery — Video

Upload the YouTube link. The MP4 to upload is **`video/pockettriage-demo-final.mp4`** (58 s, 3 MB, 1920 × 1080).

YouTube upload steps:
1. Go to https://studio.youtube.com → **Create → Upload videos**
2. Pick `video/pockettriage-demo-final.mp4`
3. Title: `PocketTriage — Offline WHO IMCI paediatric triage on Gemma 4`
4. Description (paste):

   ```
   PocketTriage is an open-source, on-device paediatric triage assistant for community health workers. Built on Gemma 4. WHO IMCI 2014 protocol. Apache 2.0.

   Repo:        https://github.com/yonkoo11/pockettriage
   Live demo:   https://huggingface.co/spaces/yonko11/pockettriage
   Landing:     https://yonkoo11.github.io/pockettriage

   Submitted to The Gemma 4 Good Hackathon (Google DeepMind, May 2026) under the Health & Sciences Impact track.

   Built by Mustapha Alex, medical intern, Nigeria.
   ```

5. Visibility: **Unlisted** (judges can open via link; hides from public discovery)
6. Custom thumbnail: upload **`video/youtube-thumbnail.png`** (1280 × 720)
7. Audience: "No, it's not made for kids"
8. Save the URL. Paste it into the Kaggle "Video" slot.

## 7. Content — Project Description

Paste the contents of **`writeup/kaggle-writeup.md`** into the Project Description box (Kaggle's rich text editor). Word count = 1,493 / 1,500.

If the editor strips Markdown tables, the evidence table is the one part to manually re-create. Use this plain-text version:

```
| Scenario | Expected | Actual | Latency | Result |
| S1  severe pneumonia                          | Pink   | Pink   | 10.6 s | PASS |
| S2  some dehydration                          | Yellow | Yellow | 10.7 s | PASS |
| S3  uncomplicated malaria                     | Yellow | Yellow |  9.3 s | PASS |
| S4  cough or cold                             | Green  | Green  |  8.4 s | PASS |
```

## 8. Content — Project Links

Click **+ Add link** four times. Paste:

| Label | URL |
|---|---|
| GitHub Repository | `https://github.com/yonkoo11/pockettriage` |
| Live Demo (Hugging Face Space) | `https://huggingface.co/spaces/yonko11/pockettriage` |
| Landing Page | `https://yonkoo11.github.io/pockettriage` |
| YouTube Video | _(paste from step 6 once uploaded)_ |

## 9. Save Draft → Submit

- Save Draft first to verify the checklist (right rail) flips to 7 / 7 ✓.
- Then click **Submit**. Screenshot the confirmation.

---

## Files referenced in this package

- `video/pockettriage-demo-final.mp4` — 58 s, 1920 × 1080, ElevenLabs Brian voice, music mixed at −22 dB, +6 % contrast color grade
- `video/youtube-thumbnail.png` — 1280 × 720, custom (NOT auto-generated frame)
- `writeup/card-thumbnail.png` — 560 × 280, Kaggle card thumbnail
- `writeup/kaggle-writeup.md` — 1,493 words, paste body into Project Description

## SECURITY — DO THIS NOW

You pasted an ElevenLabs API key in chat. It is saved at `~/.config/pockettriage/eleven.key` (0600) and was used to generate the 6 voice clips. Rotate it now: https://elevenlabs.io/app/settings/api-keys → revoke the `triage` token. The keyfile can be removed too:

```bash
rm ~/.config/pockettriage/eleven.key
```

Audio files are already mixed into the final MP4 — you don't need the key again unless you want to regenerate the voiceover.
