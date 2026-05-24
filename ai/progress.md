# PocketTriage — Progress + Next Steps

**Last session save point:** 2026-05-17.
**Build state:** Phase 1 Gate PASSED. Phase 2 done. Phase 3 mostly done (outreach drafted, HF Space files staged, public repo live). Phase 4 artifacts drafted (writeup, video script, cover, comm-pack checklist, sponsor-depth verification).

## What Changed (Plain English)

This session:

1. **Published the project to GitHub publicly.** Anyone can now view, clone, and use the code at https://github.com/yonkoo11/pockettriage. Apache 2.0 license. No secrets in any file (a `.gitignore` and a `SECURITY.md` were installed first).
2. **Wrote three outreach letters to real, named decision-makers** — at the World Health Organization (Geneva), the Indian National Health Mission, and the Nigerian NPHCDA. Each has a written email body and a shorter LinkedIn / WhatsApp version. They are not sent yet — they go out once the demo link is live.
3. **Wrote the Kaggle entry text.** 1,480 words. Covers what the problem is, what the product does, the evidence that it works (4 out of 4 WHO IMCI scenarios pass with the network turned off), the safety architecture, ethics, and distribution. Under the 1,500 word cap.
4. **Wrote the video plan.** A 2-minute script in 9 frames showing the clinic, the IMCI chart booklet, the laptop running in airplane mode, the four test cases passing, and the team. Includes pronunciation notes for any voice-over. **No Android phone footage in the script** — see point 7 below.
5. **Made the cover image.** A clean typographic 1920×1080 PNG ready to upload with the Kaggle entry. (The original plan was to generate a photorealistic image with Gemini, but the daily image quota was exhausted at build time. The typographic version is better than a slop AI image.)
6. **Wrote the pre-submission checklist** (`writeup/comm-pack-checklist.md`). Every item that needs to be true before you click Submit — banned words scrubbed, links pointing at the right places, tracks selected correctly, etc.
7. **Honesty pivot on the LiteRT track.** The original plan was to apply for the LiteRT (Android) special-tech track in addition to Health & Sciences. After Phase 4.5 verification (`ai/sponsor-integration.md`), the LiteRT depth scored only 3 out of 5 — the architecture is documented and the right model artifact is identified, but no Android APK was actually built and tested on a real phone. Per the rule "apply only to tracks where shipped depth is ≥ 4/5", **we skip the LiteRT track** in this submission. The writeup, video script, README, and checklist were all updated to match.

**Tracks applied for:** Main + Health & Sciences Impact + Ollama Special Tech. That's it. No fake claims.

## What's Still On You (the human)

These three actions require you, because they need your accounts / your face / your finger on the Submit button.

### 1. Live demo (Hugging Face) — ALREADY DONE

Live and verified: https://huggingface.co/spaces/yonko11/pockettriage

End-to-end probe on 2026-05-17: the S1 severe-pneumonia scenario returned the correct PINK tier and the correct WHO IMCI severe-pneumonia pathway. Full container latency was 534 seconds (~9 minutes) on the free `cpu-basic` tier — this is the price of running 5 B parameters on 2 vCPU with no GPU. The Space header openly tells visitors so.

**Visit it once in a private window to confirm it loads for you.** If it says "Sleeping" (HF Spaces sleep after 48 h idle on free tier), click "Restart". First call after a sleep adds ~30 s of model reload on top of the inference time.

### 2. Record the 2-minute video

Open `writeup/video-script.md` and follow the 9-frame plan. Tools:

- **Screen recording** of the Gradio app on your laptop, with airplane mode visibly on (turn off Wi-Fi and Bluetooth from the menu bar — the airplane icon will appear).
- **Phone camera** for the clinic / chart-booklet shots (or use stock IMCI photos with attribution).
- **No music with vocals.** Free instrumental tracks at incompetech.com or fugue.co.
- **Subtitles burned in.** Use the script as the caption source.

When the video is done, upload to YouTube as Unlisted, copy the URL, and paste it here. I'll add it to the writeup and the checklist.

### 3. Send the outreach (after the demo URL is live)

The three letters in `outreach/` are written. Once the Hugging Face Space URL is green, paste it into the three letters where it says `<Hugging Face Space URL — pending Phase 3 deploy>`, and send them:

- WHO: email to `digitalhealth@who.int` + LinkedIn DM to Dr. Alain Labrique.
- India NHM: email to `as-nhm@nic.in` + LinkedIn DM to Maharashtra NHM mission director.
- Nigeria NPHCDA: email to `info@nphcda.gov.ng` + WhatsApp to your Anambra SPHCDA contact + LinkedIn DM to Dr. Muyi Aina.

These are real people. You will hear back from some of them.

### 4. Submit on Kaggle

Open `writeup/comm-pack-checklist.md`. Walk down the list. Every box that says `[ ]` is something to check or do. When it's all green, go to the Kaggle competition page, fill the form, attach the writeup + GitHub URL + HF Space URL + YouTube URL + cover image, select **Main + Health & Sciences Impact + Ollama Special Tech**, click Submit, screenshot the confirmation.

## What I Did / What I Did NOT Do / Confidence Level

**What I Did (verifiable in the repo, all commits pushed to `origin/master`):**

- Created public GitHub repo at github.com/yonkoo11/pockettriage and pushed all V1 code.
- Installed the security baseline (`.gitignore`, `SECURITY.md`, CLAUDE.md security block) before pushing public.
- Drafted 3 outreach letters with real named contacts and full message bodies.
- Drafted the HF Space deploy (Dockerfile, entrypoint, requirements, README with HF frontmatter).
- Drafted the Kaggle writeup at 1,480 words, under the 1,500 cap.
- Drafted the 2-minute video script and recording checklist.
- Generated the cover image (1920×1080 PNG) via Pillow.
- Drafted the Phase 4.7 communication-pack checklist.
- Performed the Phase 4.5 sponsor-depth verification and cascaded the LiteRT-out decision through every submission artifact.
- Verified `git ls-files | grep -E "(api_key|secret|private_key|...)"` returns zero hits — no secrets in any committed file.

**What I Did NOT Do (literally impossible right now without you):**

- Log into Hugging Face and deploy the Space (needs your HF token).
- Record or upload the YouTube video (needs your camera + face + voice).
- Send the three outreach emails (needs your accounts).
- Click Submit on Kaggle (needs your Kaggle account + your judgment that the artifacts are final).
- Build and test an Android APK on a real Tecno Spark phone (needs Android Studio, an actual phone, a USB cable). This is the reason the LiteRT track is dropped from V1.

**Confidence levels:**

- Phase 1 Gate (4/4 IMCI airplane mode pass): **HIGH** — directly verified in `eval/airplane-test-log.md` and the previous commit.
- Safety layer (17 unit tests): **HIGH** — verified in `laptop/test_safety.py` last session.
- Public GitHub: **HIGH** — verified via `gh repo view`.
- Writeup accuracy: **MEDIUM-HIGH** — claims are sourced from this repo, but a final read-through with the user is wise.
- HF Space will actually run when deployed: **MEDIUM** — Docker config is conventional, but `gemma4:e2b` is 7 GB and the free-tier Space has 16 GB RAM + 2 vCPU; cold-boot may be 10+ minutes; per-inference latency may be 30–60 s. Disclosed in `huggingface-space/README.md`.
- Outreach will get a response: **LOW** — these are real cold emails to senior people. The fact that the sender is a Nigerian medical intern with a working open-source product helps, but no promises.
- Submission wins a track: **UNKNOWN** — out of scope of this build session.

---

## 2026-05-24 — E4B local verification attempt

**What Changed (Plain English):** Tried to verify the app works the same on the bigger model (E4B) as it does on the smaller one (E2B). The bigger model downloaded and installed fine, but this laptop has only 8 GB of memory and the model needs more than 10 GB. The model loads but the app freezes the moment it tries to use it. Updated STATUS.md to say the bigger-model claim still hasn't been proven on this hardware and would need a stronger computer or a one-off cloud run to settle.

**What I Did:**

- Reinstalled the Ollama runtime (it had been removed in cleanup).
- Pulled `gemma4:e4b` (10.5 GB) successfully after one network retry.
- Sent a 5-token test request directly to the model API — got zero bytes back after 4 minutes (model is page-thrashing on 8 GB RAM).
- Ran the eval scenarios — every scenario killed at the 5-minute timeout.
- Unloaded the model from memory to free RAM.
- Rewrote the E4B row in STATUS.md to say "not eval-runnable on this hardware" instead of "unverified."

**What I Did NOT Do:**

- Did not get any E4B accuracy numbers. The hardware ceiling is a hard stop here, not a thing I can code around.
- Did not try a cloud GPU. That's a $5-ish spot run on Modal or Replicate; worth doing only if the user wants that signal.

**Confidence Level:** HIGH that E4B does not run usefully on an 8 GB Mac (direct evidence: 240 s timeout returning zero tokens). HIGH that the eval code path itself works (it ships green on E2B, same backend). UNKNOWN on whether E4B and E2B agree on the 4 IMCI scenarios — that is the question I could not answer this session.
