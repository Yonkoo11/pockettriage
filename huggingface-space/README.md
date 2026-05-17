---
title: PocketTriage
emoji: 🩺
colorFrom: green
colorTo: red
sdk: docker
app_port: 7860
pinned: true
license: apache-2.0
short_description: Offline WHO IMCI paediatric triage on Gemma 4 E2B
---

# PocketTriage — Hugging Face Space

This is the **browser-accessible demo** of PocketTriage. It runs the same `laptop/` code path as the local-install version of the product, with Ollama + `gemma4:e2b` inside the Space container.

**The Space is NOT the product.** The product is the on-device deployment:

- Laptop V1: clone the GitHub repo and run locally with Ollama
- Android V2: install the LiteRT APK on a real low-end Android (target hardware: Tecno Spark, $80 segment)

The Space exists so a reviewer can verify that the IMCI classifier behaves correctly on the 4 canonical scenarios without installing anything. It is a transparency layer, not the deployment layer.

## How it works

1. The Docker container installs Ollama, pulls `gemma4:e2b` on first boot (~7 GB, slow), starts Ollama on `127.0.0.1:11434`, and launches the Gradio app on port 7860.
2. The user types a paediatric symptom description (and optionally uploads a photo).
3. The Gradio app sends the chat to Ollama. The model returns structured JSON: `{tier, pathway, reasoning, confidence}`.
4. The R13–R16 safety layer runs on the model output and renders the final card.

## Repo

Source: https://github.com/yonkoo11/pockettriage (Apache 2.0).
Built for: The Gemma 4 Good Hackathon (Google DeepMind, May 2026), Health & Sciences Impact track.

## First-boot caveat

The Space takes 5–10 minutes on first start to pull the 7 GB model file. Subsequent boots are fast (~30 s). If the model is still pulling when you load the page, you will see "Model unavailable: Ollama not reachable" — refresh after a minute.

## Latency — measured, not estimated

This Space runs on `cpu-basic` (2 vCPU, no GPU). End-to-end probe on 2026-05-17 with the S1 "severe pneumonia" canonical scenario returned the correct **PINK — Refer Urgently** tier with the correct WHO IMCI pathway in **534 seconds (~9 minutes)**. After the first call the model stays resident (`OLLAMA_KEEP_ALIVE=24h`); the second call is faster but still in the same order of magnitude.

The product is built for Apple Silicon laptops (8–11 s per triage on M-series) and Android phones via LiteRT. The Space is a courtesy demo so reviewers can verify the IMCI classifier behaviour in a browser — **for fast eval, run locally** following the GitHub README. A clean clone to first triage is about 15 minutes.
