# Outreach — Nigerian Federal Ministry of Health / Primary Healthcare

**Status:** Drafted 2026-05-17. Not yet sent.
**Channel:** Email + WhatsApp (Nigeria-appropriate). LinkedIn DM to named NPHCDA leadership (secondary).
**Persona served:** Adaeze — CHEW (Community Health Extension Worker), Anambra State, Tecno Spark, 2G or no signal. Persona file: PRD §2.

---

## Named contacts

**Primary — NPHCDA (National Primary Healthcare Development Agency):**
**Dr. Muyi Aina** — Executive Director / CEO, NPHCDA (the federal body that owns primary healthcare and the CHEW workforce in Nigeria).
- NPHCDA public address: Plot 681/682 Port Harcourt Crescent, Off Gimbiya Street, Area 11, Garki, Abuja.
- NPHCDA contact: https://nphcda.gov.ng/ (Contact us page) / `info[at]nphcda[dot]gov[dot]ng`

**Secondary — Federal Ministry of Health:**
**Coordinating Minister of Health & Social Welfare, Prof. Muhammad Ali Pate** — at FMoH HQ, Abuja.
- FMoH digital health unit: ICT department, Federal Ministry of Health, Federal Secretariat Complex, Abuja.

**Local-context — Anambra State Primary Healthcare Development Agency:**
**Anambra SPHCDA** — Awka. The state agency that directly trains and deploys CHEWs in the Adaeze persona's geography.

## Why these contacts

NPHCDA owns the federal primary-healthcare programme and the CHEW workforce. Anambra SPHCDA is the state-level operational layer where actual deployment would happen. The Coordinating Minister's office sets policy direction for digital-health adoption. As a Nigerian medical intern, I have a credibility advantage at NPHCDA that an external party would not — this is the highest-leverage outreach lane for the product.

## Message — Email (NPHCDA)

> Subject: Open-source on-device WHO IMCI paediatric triage tool, built by Nigerian medical intern, free for NPHCDA / CHEW use
>
> Dear Dr. Aina,
>
> I am Mustapha Alex, a Nigerian medical intern. I have built and open-sourced (Apache 2.0) an on-device WHO IMCI paediatric triage assistant called PocketTriage. It runs Google's Gemma 4 E4B model fully on-device — on a $80 Android phone via Google AI Edge's LiteRT, or on a laptop via Ollama. No internet required during operation. No patient data leaves the device. Free for any NPHCDA, state SPHCDA, or CHEW use forever.
>
> The product is designed for the CHEW persona I see every day in our PHC rotations: a worker in Anambra or Ebonyi with a low-end Android, intermittent 2G, and the printed WHO IMCI chart booklet in her bag. The current paper protocol is excellent but slow, and there is no way to support the worker between facility visits. PocketTriage runs the IMCI 2014 classifier locally and returns the standard Pink/Yellow/Green tier plus a structured referral pathway, with a hard non-dismissable disclaimer that the tool does not replace clinical judgment.
>
> I am asking for three things:
>
> 1. **A 30-minute conversation** with NPHCDA's primary-healthcare-quality or digital-health team about whether the WHO IMCI encoding is faithful to the version NPHCDA trains CHEWs on. The CHEW Standing Orders likely differ in detail from the WHO base protocol; I want to encode the NPHCDA-specific variant if it exists.
> 2. **Permission to pilot** the tool with 5–10 CHEWs in Anambra (I can fund this personally for the pilot) and bring back outcome data.
> 3. **Guidance** on whether NPHCDA's ICT / digital-health unit is the right counterparty for technical co-development or whether Pate's FMoH digital-health unit should lead.
>
> Live demo: <Hugging Face Space URL — pending Phase 3 deploy>
> Source: https://github.com/yonkoo11/pockettriage (Apache 2.0)
> Built for the Google DeepMind Gemma 4 Good Hackathon (Health & Sciences track, May 2026).
>
> I can attend in person in Abuja any time in the next three months at my own cost. I am also happy to demo the working app on a Nigerian-spec Tecno Spark phone in person.
>
> Respectfully,
>
> Mustapha Alex
> Medical intern, Nigeria
> [email] [phone] [LinkedIn]

## Message — WhatsApp (Anambra SPHCDA local contact)

> Good day Sir/Ma. I am Mustapha, medical intern. I have built a free, open-source, offline WHO IMCI triage tool that runs on Android phones with no internet. Designed for our CHEWs. Built for a Google hackathon. Free for SPHCDA use forever. I would like to demo it to your team. May I send a short video and ask for 20 minutes? Repo: github.com/yonkoo11/pockettriage. Thank you.

## Send log

| Date | Channel | Status | Response |
|---|---|---|---|
| pending | Email `info@nphcda.gov.ng` to Dr. Muyi Aina | not sent | — |
| pending | WhatsApp Anambra SPHCDA contact | not sent | — |
| pending | LinkedIn DM Dr. Muyi Aina | not sent | — |

**Next action:** Send within 24 hours of pushing the public GitHub repo and the live demo being up. NPHCDA email is the highest-leverage contact in this set.
