# PocketTriage — Product Requirements Document

**Document version:** 0.1
**Owner:** Mustapha (Nigerian medical intern, builder)
**Status:** V1 in build — submission target 2026-05-18 (deadline as fact; not a scope constraint)
**Distribution:** PRD lives in repo at `/PRD.md`. Authoritative source for what V1 ships.

---

## 0. Executive Summary

PocketTriage is an offline-first Gemma 4 assistant that helps community health workers triage patients in low-resource clinical settings. A worker enters symptoms (text + optional photo) on a device that may have no internet. Gemma 4 E4B running on-device classifies the case against the WHO IMCI (Integrated Management of Childhood Illness) protocol, returns an acuity tier (Pink = emergency / Yellow = priority / Green = home care), and emits a structured referral pathway via Gemma 4's native function-calling. Nothing leaves the device.

The V1 ships two runtimes — Ollama on laptop and LiteRT on Android — both load-bearing in the live demo. The product is positioned as an open-source decision-support tool donated to the global CHW community, not a SaaS or app-store paywall.

**Why this wins the Gemma 4 Good Hackathon:**
- The use case is structurally impossible on cloud LLMs (no internet in target deployments, PHI sensitivity, $0 marginal cost per query). Gemma 4 open weights + on-device E4B is the only viable architecture.
- The founder is a Nigerian medical intern. The video story is lived experience, not market research.
- The submission stacks Main Track + Health & Sciences Impact + LiteRT Special Tech, each with load-bearing depth ≥ 4/5.

---

## 1. Problem Statement

### 1.1 The number
- Globally, 4.3 billion people live in countries with severe health worker shortages (WHO State of the World's Nursing 2020). India has 1M+ ASHA community health workers, Nigeria has 70,000+ CHEWs and JCHEWs, Bangladesh has 50,000+ CHWs.
- Childhood mortality in low-resource regions remains concentrated in the under-5 cohort. 1 in 27 children in sub-Saharan Africa die before age 5 (UNICEF 2023). Most deaths are from conditions IMCI explicitly triages: pneumonia, diarrhea, malaria, severe febrile illness, malnutrition.
- IMCI training reduces under-5 mortality but coverage of trained CHWs is patchy and reference materials are paper-based, in English, and not always available at point of care.

### 1.2 The structural gap
- Cloud LLM assistants (ChatGPT, Gemini, Claude) require persistent internet. Target deployments have 2G or no signal.
- Existing CHW tools (mobile decision-support apps from Dimagi CommCare, Living Goods, Ona) are rule-based menu trees, not natural-language tools. A CHW can't describe a presentation in their own words.
- HIPAA-equivalent privacy regulations (Nigerian NDPR, EU GDPR for diaspora deployments, US HIPAA for stateside CHW pilots) block cloud routing of any patient data without BAA / equivalent.
- Gemma 4's open-weight on-device E4B model + native multimodal + native function calling is the first model class where (a) inference fits on a $80 Android, (b) the model can read a symptom photo, and (c) the model emits structured pathway recommendations without prompt-engineering gymnastics.

### 1.3 Why now
Google DeepMind released Gemma 4 in April 2026. The E4B variant is positioned for edge inference. The Google AI Edge LiteRT runtime ships first-party Android tooling for this model class. The hackathon is sponsored by the team that built the model — they want to see exactly this use case demonstrated.

---

## 2. Target Users

### 2.1 Primary persona — Adaeze, Nigerian CHEW
- 28, Community Health Extension Worker in rural Anambra State
- Sees 10–30 patients per day, mostly under-5 children
- Owns a $90 Tecno Spark Android phone, runs Android 12
- Has 2G signal most of the time, no signal in some villages
- IMCI-trained 3 years ago, has access to a paper IMCI chart booklet
- Speaks Igbo natively, English clinically, Hausa rarely
- Doesn't trust cloud apps — has heard of patient data leaks
- Currently calls a supervising medical officer when uncertain, which often means a 2-hour delay

### 2.2 Secondary persona — Priya, Indian ASHA
- 34, ASHA worker in Maharashtra, serves 1,000-person village
- Owns a basic Android phone, primarily uses WhatsApp
- IMCI-trained, but flowcharts are in English which she reads slowly
- Wants Hindi-first interface

### 2.3 Anti-personas (NOT users)
- US clinicians (FDA SaMD regulatory burden, different protocols)
- Hospital systems (have EHRs, different decision support stack)
- Patients themselves (this is a clinician tool, not a self-diagnosis app)

---

## 3. Success Metrics

### 3.1 Judge-criterion metrics (mapped to scoring rubric)
| Criterion | Weight | Target |
|---|---|---|
| Impact & Vision (40 pts) | Video demonstrates real Nigerian clinic context, lived-experience narration, before/after story of a single patient encounter | 38+ / 40 |
| Video Pitch & Storytelling (30 pts) | ≤ 2 min cut, 1080p, subtitles, structured Problem → Solution → Demo → Team, real on-device footage with airplane mode visible | 27+ / 30 |
| Technical Depth (30 pts) | Repo shows load-bearing Gemma 4 E4B + multimodal + function-calling + LiteRT runtime + reproducible eval | 27+ / 30 |
| **Target total** | | **92+ / 100** |

### 3.2 Product metrics (V1 acceptance)
| Metric | Target | Verified by |
|---|---|---|
| Phase 1 Gate IMCI accuracy | ≥ 3/4 canonical scenarios returned with correct tier | `eval/scenarios.json` + manual review |
| Inference latency (laptop, Ollama) | < 8s per case end-to-end | `eval/latency.md` |
| Inference latency (Android, LiteRT) | < 30s per case end-to-end on Tecno Spark or equivalent | `eval/android-bench.md` |
| Network requests during inference | 0 | Chrome DevTools / Android profiler |
| Repo reproducibility | Clean clone → demo running in ≤ 30 min via README steps | One independent reviewer attempt |

### 3.3 Sponsor depth metrics (per Phase 3.5 / 4.5)
| Track | Depth at submission target |
|---|---|
| Gemma 4 model surface | 5/5 — E4B is THE model, no fallback |
| Multimodal | 4/5 — photo input feeds the classifier reasoning |
| Function calling | 4/5 — referral pathway is FC output, parsed and rendered |
| LiteRT runtime | 5/5 — Android demo runs through LiteRT, recorded with airplane mode |
| Ollama runtime | 4/5 — laptop V1 runs through Ollama, public Modelfile |
| Unsloth fine-tune | Stretch — only applied for if shipped at 4/5 |
| Cactus routing | Stretch — only applied for if E2B/E4B routing ships at 4/5 |

---

## 4. Functional Requirements

Requirements are numbered for traceability. V1 = ships at submission. V2 = stretch, applied for only if depth ≥ 4/5 hits.

### 4.1 V1 — core triage flow
- **R1** User enters symptom description in free text (≤ 1000 chars, Latin script V1)
- **R2** User optionally attaches one symptom photo (JPG/PNG, ≤ 5 MB)
- **R3** System loads Gemma 4 E4B via Ollama (laptop) or LiteRT (Android) on first launch
- **R4** System constructs prompt: WHO IMCI protocol summary (system) + symptom text + photo (if present) + function-call schema
- **R5** Model returns a JSON object: `{tier: "Pink"|"Yellow"|"Green", pathway: string, reasoning: string, confidence: 0..1}`
- **R6** UI renders the tier as a color-coded card + the pathway as a numbered checklist + the reasoning as collapsible detail
- **R7** UI displays a fixed disclaimer banner: "Decision support only — does not replace clinical judgment"
- **R8** System logs no patient data anywhere — text and photo are processed in memory and discarded on session end
- **R9** System works with airplane mode on (no network requests, verified by DevTools)

### 4.2 V1 — IMCI coverage
- **R10** WHO IMCI protocol encoded for: cough/difficult breathing, diarrhea, fever, ear problem, malnutrition, and danger signs (the 5 classification axes + 1 cross-cutting check)
- **R11** Protocol encoded as a structured Markdown document loaded as system prompt or RAG context
- **R12** Eval set covers ≥ 4 canonical IMCI scenarios with hand-coded ground truth (Pink/Yellow/Green tier + expected pathway)

### 4.3 V1 — safety
- **R13** Crisis escalation: if model output contains keywords mapping to "danger sign" IMCI categories (convulsions, unconscious, severe respiratory distress, severe dehydration), force tier to Pink regardless of model confidence
- **R14** Confidence floor: if model confidence < 0.4, append "Escalate to medical officer" to pathway regardless of tier
- **R15** Refusal pattern: if symptom description contains adult-only conditions (chest pain in adults, stroke symptoms, pregnancy emergencies), system refuses with "PocketTriage is configured for pediatric IMCI only. Refer to adult emergency protocol."
- **R16** Disclaimer banner R7 is non-dismissable

### 4.4 V1 — Android (LiteRT)
- **R17** Android APK builds from `/android` directory using Android Studio + LiteRT Gradle plugin
- **R18** APK installs on Tecno Spark / equivalent $80–$120 Android phone running Android 12+
- **R19** APK loads Gemma 4 E4B `.task` (or current LiteRT format) on first launch with progress indicator
- **R20** APK runs full R1–R9 flow on-device through LiteRT inference
- **R21** Android demo recorded with phone visible, airplane mode visible in status bar, real clinical scenario typed live

### 4.5 V2 — stretch (apply for track only if shipped at depth ≥ 4/5)
- **R22** Unsloth LoRA fine-tune on synthesized IMCI Q&A corpus, eval shows ≥ 5% accuracy improvement on the 4 canonical scenarios, weights published on Hugging Face
- **R23** Cactus intelligent routing: E2B handles cases with model self-reported confidence > 0.7, E4B handles the rest, demo shows routing decisions per case
- **R24** Hindi or Igbo localization for the system prompt + UI strings, demo recorded with localized flow

### 4.6 V2 — distribution (started during build, scaled after submission)
- **R25** Public GitHub repo with Apache 2.0 LICENSE, README, CONTRIBUTING.md, CODE_OF_CONDUCT.md
- **R26** Hugging Face Space hosting the laptop V1 (free CPU tier), accessible without login
- **R27** Submission post in r/GlobalHealth (or equivalent), with link to Space and ask for CHW pilots
- **R28** Direct outreach to one named contact at: WHO Digital Health Department, India NHM ASHA program, Nigeria FMoH PHC department. Message logged in `outreach/`.
- **R29** Listed in awesome-localllm or awesome-medical-ai GitHub list (one PR opened)

---

## 5. Non-Functional Requirements

- **NFR1 Privacy.** Zero patient data persisted. No analytics calls. No model telemetry. No phone-home.
- **NFR2 Offline.** All R1–R20 work with WiFi off and cellular off.
- **NFR3 Cost.** $0 marginal inference cost. No API keys required. No paid tiers.
- **NFR4 Hardware floor.** Android V2 must run on a $80–$120 Android phone (Tecno Spark, Infinix Smart, Samsung Galaxy A04). 4 GB RAM minimum.
- **NFR5 License.** Apache 2.0 for code, CC-BY 4.0 for documentation, Gemma 4's own license terms inherited for the model weights (Google's Gemma terms).
- **NFR6 Accessibility.** WCAG AA color contrast on the UI. Screen-reader-readable labels.
- **NFR7 Reproducibility.** README's "Run locally" section takes ≤ 30 min from clean machine to working demo for someone familiar with Python + Android Studio.

---

## 6. Technical Architecture

### 6.1 Components
```
┌──────────────────┐        ┌──────────────────────────┐
│  Laptop V1       │        │  Android V2              │
│  (Ollama tag)    │        │  (LiteRT runtime)        │
├──────────────────┤        ├──────────────────────────┤
│  Gradio UI       │        │  Kotlin Activity         │
│   ├─ text input  │        │   ├─ text input          │
│   ├─ photo input │        │   ├─ camera/photo input  │
│   └─ result card │        │   └─ result card         │
│        │         │        │         │                │
│  ┌─────▼──────┐  │        │  ┌──────▼─────────────┐  │
│  │  infer.py  │  │        │  │ LiteRT inference   │  │
│  │  - system  │  │        │  │ - load .task model │  │
│  │    prompt  │  │        │  │ - run multimodal   │  │
│  │  - FC      │  │        │  │ - parse FC output  │  │
│  │    schema  │  │        │  └────────────────────┘  │
│  └─────┬──────┘  │        │                          │
│        │         │        │                          │
│  ┌─────▼──────┐  │        │                          │
│  │  Ollama    │  │        │                          │
│  │  gemma4:e4b│  │        │                          │
│  └────────────┘  │        │                          │
└──────────────────┘        └──────────────────────────┘
        │                              │
        └──── reads ───┬─── reads ─────┘
                      │
            ┌─────────▼──────────┐
            │  WHO IMCI protocol │
            │  /who-imci/*.md    │
            └────────────────────┘
```

### 6.2 Architecture Decision Records (concise)
- **ADR-1** Gemma 4 E4B is the only model class shipped. No cloud fallback. No alternate model. Reason: the product's reason-to-exist is on-device Gemma 4; fallback to cloud destroys the depth story.
- **ADR-2** Ollama for laptop V1, LiteRT for Android V2. Both load-bearing. Reason: applying for both tracks requires the runtime to be load-bearing on each demo path. Both ship; neither is a wrapper around the other.
- **ADR-3** WHO IMCI protocol loaded as system prompt + retrieval. Reason: IMCI is the legible clinical anchor — judges and CHWs both recognize it. Replacing IMCI with a generic medical prompt destroys the lived-context wedge.
- **ADR-4** Function calling for pathway output, not freeform text. Reason: the UI renders structured pathways; freeform text would fail R6 and produces an inferior demo.
- **ADR-5** Apache 2.0 license. Reason: maximum compatibility with downstream CHW orgs adopting and modifying.
- **ADR-6** No user authentication, no analytics, no server-side anything. Reason: privacy is the headline; any backend would force a HIPAA-equivalent compliance scope outside hackathon timeline.

### 6.3 Repo layout
```
pockettriage/
├── PRD.md                          (this file)
├── README.md                       (reproduce-this instructions)
├── LICENSE                         (Apache 2.0)
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── CLAUDE.md
├── .claudeignore
│
├── laptop/                         (V1 — Ollama + Gradio)
│   ├── app.py                      (Gradio UI)
│   ├── infer.py                    (prompt build + FC parse)
│   ├── schema.json                 (FC schema for pathway)
│   ├── system-prompt.md
│   ├── multimodal.py               (photo handling)
│   ├── rag.py                      (IMCI retrieval)
│   ├── Modelfile                   (Ollama Modelfile)
│   └── requirements.txt
│
├── android/                        (V2 — Kotlin + LiteRT)
│   ├── app/
│   │   ├── build.gradle
│   │   ├── src/main/
│   │   │   ├── AndroidManifest.xml
│   │   │   ├── java/com/pockettriage/
│   │   │   │   ├── MainActivity.kt
│   │   │   │   ├── LiteRtInference.kt
│   │   │   │   └── ImciSchema.kt
│   │   │   └── res/
│   │   └── ...
│   └── README-android.md           (Build instructions)
│
├── who-imci/                       (Protocol reference)
│   ├── protocol-summary.md         (system prompt source)
│   ├── protocol-full.md            (RAG corpus)
│   └── danger-signs.md             (R13 keyword source)
│
├── eval/
│   ├── scenarios.json              (4 canonical IMCI cases + ground truth)
│   ├── airplane-test-log.md
│   ├── latency.md
│   ├── android-bench.md
│   └── safety-cases.md             (R13–R15 test cases)
│
├── ai/                             (Claude session memory)
│   ├── memory.md
│   └── progress.md
│
├── .ralph/                         (Builder agent fix plan)
│   └── @fix_plan.md
│
├── writeup/
│   ├── kaggle-writeup.md           (≤ 1500 words, submission body)
│   ├── cover-image.png
│   └── video-script.md
│
└── outreach/                       (Distribution log, R28)
    ├── who-digital-health.md
    ├── india-nhm-asha.md
    └── nigeria-fmoh-phc.md
```

---

## 7. Sponsor Integration Matrix (one paragraph per applied-for track)

This is the authoritative source for which tracks we apply for and how each is load-bearing.

### 7.1 Main Track
**Apply for:** Yes (eligible by default)
**Depth target:** 5/5 — the entire product is Gemma 4 E4B; nothing else does the cognitive work
**Load-bearing primitives:** Gemma 4 E4B model + multimodal (R2) + function calling (R5)
**Phase 4.5 acceptance:** Live demo on Hugging Face Space runs the full R1–R9 flow with airplane mode visible in screen recording

### 7.2 Impact Track — Health & Sciences
**Apply for:** Yes (primary impact framing)
**Depth target:** 5/5 — the product is "AI helps community health workers triage patients"; the Impact frame IS the product
**Why this Impact track (not Global Resilience):** Both fit. Health & Sciences is more legible — "Bridge the gap between humans and data. Build tools that accelerate discovery or democratize knowledge" maps directly to "democratize WHO IMCI protocol from doctor's binder to CHW's phone." Global Resilience offline aspect is the technical differentiator and is mentioned in the writeup, but the Impact track selection is Health & Sciences.
**Phase 4.5 acceptance:** Video tells a single-patient story from Nigerian clinical context, lived experience narration, before/after framing on a real IMCI scenario

### 7.3 Special Tech Track — LiteRT (Google AI Edge)
**Apply for:** Yes
**Depth target:** 5/5 — Android V2 runs through LiteRT; this is not "we also support LiteRT", this IS the Android path
**Load-bearing primitives:** LiteRT runtime + Gemma 4 E4B `.task` model + on-device inference + multimodal input (camera)
**Phase 4.5 acceptance:** Real Android device (not emulator) running APK, recorded with airplane mode visible, recorded inference time logged, README `android/README-android.md` documents the LiteRT integration with code citations

### 7.4 Stretch tracks — apply for ONLY if depth ≥ 4/5 ships
- **Ollama track** — currently laptop V1 runs through Ollama; depth ceiling 4/5 reachable if we publish a Modelfile + ollama pull recipe + integration code citation in README. Decision at Phase 4.5: apply if shipped.
- **Unsloth track** — depth ceiling 4/5 reachable if we ship a LoRA fine-tune with eval comparison + published weights on Hugging Face. Decision at Phase 4.5: apply only if eval shows ≥ 5% improvement AND weights are public.
- **Cactus track** — depth ceiling 4/5 reachable if we ship intelligent E2B/E4B routing. Decision at Phase 4.5: apply only if routing is in the live demo.
- **llama.cpp track** — depth ceiling 3/5 (not pushing genuinely new ground vs LiteRT). DO NOT APPLY.

---

## 8. Out of Scope (explicit — these do NOT ship in V1)

- Adult clinical conditions (R15 refuses these)
- Multi-language UI beyond English V1 (Hindi / Igbo are V2 R24)
- User accounts, login, or any server-side persistence
- Hospital EHR integration
- Real-time vital sign capture (BP, SpO2, glucose)
- Voice input (text + photo only in V1)
- Multi-patient session management
- Audit log / clinical record export
- Telemedicine call connection to a supervising doctor
- ML model evaluation beyond the 4 IMCI canonical scenarios
- Regulatory clearance (FDA SaMD, MDR, NAFDAC)
- Cloud sync of any kind
- Monetization (free, open-source, donation-only)
- Adversarial robustness testing
- Multilingual photo OCR
- Treatment dose calculation
- Pharmacy/supply chain integration

Each out-of-scope item is a deliberate cut, not a missed feature.

---

## 9. Risks & Mitigations

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| RK-1 | Gemma 4 E4B weights not yet downloadable under that exact name | Medium | Critical (blocks Phase 1 Gate) | Verify in fix-plan Task 1; fall back to whichever current Gemma edge model is shipping (e.g. Gemma 3n E4B) and update PRD accordingly |
| RK-2 | LiteRT Android tooling lags behind, .task file format changes | Medium | High (kills Android V2 demo) | If LiteRT path blocks, ship laptop V1 only and apply for Ollama track instead of LiteRT (Phase 4.5 decision) |
| RK-3 | Model inaccuracy on real CHW scenarios beyond the 4 canonical | High | Medium | V1 disclaims as decision-support; R13 hard-codes danger-sign escalation; R14 forces "escalate" when confidence is low |
| RK-4 | Photo input fails on dark-skin tones | High | Medium | Document the limitation explicitly in README + writeup. Frame photo as supplementary signal, not primary. |
| RK-5 | Sponsor-track depth slipping below 4/5 at Phase 4.5 | Medium | High | Drop track from submission rather than submit shallow. Per rule #4, submitting to a track at depth < 4 is BANNED. |
| RK-6 | Liability for missed-diagnosis framing | Low (mitigated) | High if realized | Apache 2.0 license disclaims warranty; UI banner R7 is non-dismissable; positioning is decision-support, not diagnosis. No clinical claims in the writeup. |
| RK-7 | WHO IMCI protocol is large; full encoding overruns model context | Medium | Medium | RAG retrieval (R11) instead of full system prompt for V1 if context becomes tight |
| RK-8 | Distribution outreach gets no responses | High | Low (still satisfies R28) | R28 acceptance is "outreach started", not "response received". Submission stands either way. |
| RK-9 | Reproducibility README fails for an independent reviewer | Medium | Medium | Have one independent reviewer attempt clean-clone-to-demo in the final 24h; fix README gaps |

---

## 10. Submission Checklist (Phase 4.7 Communication Pack mapped to deliverables)

- [ ] Kaggle Writeup (≤ 1500 words) submitted under "Health & Sciences" track
- [ ] YouTube video (public, ≤ 3 min, ideally ≤ 2 min) linked in Writeup
- [ ] Public GitHub repo with Apache 2.0 LICENSE, README, CONTRIBUTING.md
- [ ] Live demo URL (Hugging Face Space) linked in Writeup
- [ ] Cover image in Media Gallery
- [ ] Android APK linked or buildable from `/android` per README
- [ ] All R1–R21 verified shipped (R22–R24 stretch verified IF applied for)
- [ ] All Phase 4.5 sponsor-depth re-scores logged in `ai/sponsor-integration.md`
- [ ] Phase 4.7 link-checker output passes (every URL returns 200)
- [ ] Phase 4.7 banned-words scrub passes
- [ ] Distribution outreach R28 logged in `outreach/`

---

## 11. Open Questions (must answer in fix-plan Task 1)

1. What is the exact current Gemma 4 E4B model identifier in Ollama? (`ollama pull <tag>`)
2. What is the LiteRT `.task` file URL for Gemma 4 E4B? (Kaggle competition discussion should link it)
3. Does Gemma 4 E4B support native function calling at the E4B parameter count, or is FC limited to 26B/31B? If E4B doesn't FC natively, fall back to constrained-decoding JSON output.
4. Does multimodal photo input work at the E4B parameter count, or is multimodal also restricted to the larger variants?
5. Is there a Gemma 4 reference Android app or LiteRT sample we can fork the integration code from?

If any of these resolve negatively, update the PRD before continuing the build.

---

## 12. Authority and change log

- This PRD is the source of truth. CLAUDE.md and ai/memory.md derive from it.
- Any scope change requires updating Sections 4 (FRs), 7 (Sponsor Matrix), or 8 (Out of Scope) AND recording the change in the change log below.
- 2026-05-16 v0.1 — Initial PRD. Pivoted Impact track from Global Resilience to Health & Sciences. Locked Main + Health & Sciences + LiteRT as the apply-for set; Ollama / Unsloth / Cactus are Phase 4.5 decisions; llama.cpp explicitly excluded.
