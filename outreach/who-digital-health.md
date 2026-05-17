# Outreach — WHO Digital Health Department

**Status:** Drafted 2026-05-17. Not yet sent.
**Channel:** Email + LinkedIn DM (parallel).
**Reason for two channels:** Email goes to the WHO Digital Health and Innovation team inbox (`digitalhealth@who.int`); LinkedIn DM goes to the specific named lead to raise the chance of a human reading it within a week.

---

## Named contact

**Dr. Alain Labrique** — Director, Department of Digital Health & Innovation, WHO HQ Geneva.
- LinkedIn: https://www.linkedin.com/in/alabrique/ (public profile, active)
- WHO bio: https://www.who.int/our-work/science-division/digital-health-and-innovation

Backup contact if Dr. Labrique does not respond within 10 days:
**Dr. Bernardo Mariano Jr.** — Director-General Special Envoy for Health Workforce / former Director Digital Health, WHO.

## Why this contact

WHO Digital Health & Innovation is the WHO unit that runs the Digital Health Atlas, the Digital Health Clearinghouse, and the AI for Health programme. Any on-device clinical decision-support tool aimed at IMCI deployment needs their awareness and (eventually) their imprimatur to be usable in WHO programmes. The DHI department also has the mandate to evaluate AI tools against the WHO AI Ethics & Governance guidance for health.

## Message — Email

> Subject: Open-source on-device WHO IMCI triage classifier (Gemma 4 / LiteRT) — request for technical review
>
> Dear Dr. Labrique,
>
> I am Mustapha Alex, a medical intern based in Nigeria. I have built an open-source, Apache 2.0 reference implementation of an on-device paediatric IMCI triage assistant called PocketTriage. It runs Google's Gemma 4 E4B open-weight model fully on-device (Ollama on laptop, LiteRT on Android) and returns the standard Pink/Yellow/Green tier plus a referral pathway for the WHO IMCI Chart Booklet 2014 protocol. No patient data leaves the device.
>
> The project is built for community health workers operating without reliable connectivity (the Adaeze / Priya personas in CHW research). It is not a clinical product — it is a public, modifiable substrate that local programmes can adopt, localize, and validate. I am writing for three reasons:
>
> 1. **Technical review.** The system prompt and safety layer are derived from the WHO IMCI 2014 chart booklet. I would like a member of your team to look at the IMCI encoding and tell me where it diverges from the WHO source.
> 2. **Digital Health Atlas listing.** PocketTriage meets the criteria for a public-good, open-source classifier. I want to start the registration process.
> 3. **AI for Health alignment.** The README explicitly references the WHO AI Ethics & Governance Guidance for Health (2021). I would like to confirm I have read it correctly.
>
> Live demo: <Hugging Face Space URL — pending Phase 3 deploy>
> Source: https://github.com/yonkoo11/pockettriage (Apache 2.0)
> Submission to Google DeepMind Gemma 4 Good Hackathon under the Health & Sciences track.
>
> Happy to schedule a 20-minute call any time in the next two weeks.
>
> Mustapha Alex
> Medical intern, Nigeria
> [email] [phone] [LinkedIn]

## Message — LinkedIn DM (shorter)

> Dr. Labrique — I am a Nigerian medical intern. I built an Apache 2.0 on-device WHO IMCI paediatric triage assistant on Gemma 4 / LiteRT for community health workers in low-connectivity settings. Nothing leaves the device. I would like 20 minutes of your team's time for technical review against the WHO IMCI Chart Booklet 2014 and to discuss Digital Health Atlas registration. Repo: github.com/yonkoo11/pockettriage. Demo link in profile. Thank you.

## Send log

| Date | Channel | Status | Response |
|---|---|---|---|
| pending | Email `digitalhealth@who.int` | not sent | — |
| pending | LinkedIn DM to Dr. Alain Labrique | not sent | — |

**Next action:** Send both messages within 24 hours of pushing the public GitHub repo, once the live demo URL is up.
