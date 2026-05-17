# Outreach — India National Health Mission / ASHA programme

**Status:** Drafted 2026-05-17. Not yet sent.
**Channel:** Email (primary). LinkedIn DM to named state-level lead (secondary).
**Persona served:** Priya — ASHA worker, Maharashtra, Hindi-first. Persona file: PRD §2.

---

## Named contacts

**Primary — central NHM:**
**Smt. Roli Singh, IAS** — Additional Secretary & Mission Director, National Health Mission, Ministry of Health & Family Welfare, Government of India.
- Public address: Nirman Bhawan, New Delhi
- NHM public contact: `as-nhm[at]nic[dot]in` (Additional Secretary office)

**Secondary — state-level (Maharashtra, target deployment context):**
**Maharashtra State Health Society — NHM Maharashtra**, Mission Director's office, Mumbai.
- Public contact via mahaarogya.gov.in / NHM Maharashtra portal.

**Programme-level — ASHA programme owner:**
**National ASHA Mentoring Group**, c/o NHSRC (National Health Systems Resource Centre), New Delhi.
- NHSRC: https://nhsrcindia.org/

## Why these contacts

The NHM is the central body that funds, trains, and coordinates the ~1 million ASHA (Accredited Social Health Activist) workforce in India. ASHA workers run paediatric outreach in villages with patchy connectivity, often on entry-level Android phones — the exact deployment context PocketTriage is built for. NHSRC is the technical-resource arm of the NHM and is the right entry point for an open-source classifier intended for ASHA workflow integration.

## Message — Email

> Subject: Open-source on-device paediatric IMCI triage tool for ASHA workers — request for technical conversation
>
> Respected Madam Roli Singh,
>
> I am Mustapha Alex, a medical intern based in Nigeria. I have built and open-sourced (Apache 2.0) a reference implementation of an on-device WHO IMCI paediatric triage assistant called PocketTriage. It runs Google's Gemma 4 E4B open-weight model fully on-device on entry-level Android phones via Google AI Edge's LiteRT runtime. No patient data leaves the device. No internet required during operation.
>
> The product is designed for community health workers in low-connectivity settings. The Indian ASHA workforce is one of the two primary deployment personas I have studied (the persona file calls her "Priya — ASHA, Maharashtra"). I would like to start a conversation with the NHM team about whether this open-source substrate is useful to ASHA paediatric outreach workflows, and what changes (localization to Hindi/Marathi, integration with HMIS/ANMOL, alignment with the IMNCI India variant of the WHO IMCI protocol) would be necessary.
>
> Specifically I am asking for:
>
> 1. A 30-minute conversation with the technical-architecture team (likely NHSRC) about the IMCI encoding and what would need to change for IMNCI India.
> 2. Guidance on whether NHSRC's mAdvisor / Kilkari teams would be appropriate technical partners.
> 3. Permission to translate the README and system prompt into Hindi and Marathi using ASHA-relevant terminology.
>
> Live demo: <Hugging Face Space URL — pending Phase 3 deploy>
> Source: https://github.com/yonkoo11/pockettriage (Apache 2.0, free for any government use)
> Built for the Google DeepMind Gemma 4 Good Hackathon (Health & Sciences track).
>
> I am happy to travel to Delhi at my own cost for a meeting, or to attend online any time in the next month.
>
> Respectfully,
>
> Mustapha Alex
> Medical intern, Nigeria
> [email] [phone] [LinkedIn]

## Message — LinkedIn DM (shorter, sent to Maharashtra NHM Mission Director)

> Respected Sir/Madam — I am a Nigerian medical intern. I have open-sourced an on-device WHO IMCI paediatric triage assistant on Gemma 4 / LiteRT, runs offline on entry-level Android, no patient data leaves the device. Designed for ASHA-style community health workers. Apache 2.0, free for any NHM use. Repo: github.com/yonkoo11/pockettriage. Would value 20 minutes of your technical team's time. Thank you.

## Send log

| Date | Channel | Status | Response |
|---|---|---|---|
| pending | Email `as-nhm@nic.in` | not sent | — |
| pending | LinkedIn DM Maharashtra NHM | not sent | — |
| pending | NHSRC contact form | not sent | — |

**Next action:** Send within 24 hours of pushing the public GitHub repo and the live demo being up.
