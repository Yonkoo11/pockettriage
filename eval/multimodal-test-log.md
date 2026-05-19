# Multimodal eval — first live run

Date: 2026-05-19.
Model: `gemma4:e2b` (digest `sha256:4e30e266…`) via Ollama 0.24.0.
Backend: `POCKETTRIAGE_BACKEND=ollama`, timeout 600 s.
Hardware: Apple Silicon, MPS.

## Scenario

`S5-malnutrition-muac-photo` (added in this commit).

- **Input text:** *"2-year-old girl. Mother says child has been less active and not eating well for two weeks. Diarrhoea on and off. CHEW has just taken a MUAC reading — attached photo shows the tape."*
- **Input photo:** [`eval/photos/muac-red-10p8cm.png`](photos/muac-red-10p8cm.png) — a synthetic MUAC tape with the reading needle clearly in the RED zone at **10.8 cm**, with the numeric label "reading: 10.8 cm" rendered prominently and the words "RED ZONE — severe acute malnutrition" written into the image.
- **Expected:** tier `Pink` (MUAC < 11.5 cm = severe acute malnutrition → refer urgently per WHO IMCI Section 6).

## Actual

| Field | Value |
|---|---|
| Tier | **Yellow** (FAIL — expected Pink) |
| Pathway | "Counsel on feeding and ensure adequate intake. Refer for supplementary feeding and nutritional counseling. Follow-up in 14 days." |
| Reasoning | "Section 6, Moderate acute malnutrition (**MUAC 115–125 mm**)." |
| Confidence | 0.95 |
| Safety flags | [] (no override fired) |
| Latency | 121.6 s |

## The honest finding

The model fabricated a plausible-but-incorrect MUAC reading from the photo. The image clearly shows 10.8 cm (RED zone, severe acute malnutrition) but the model reported "115–125 mm" (YELLOW zone, moderate). It then reasoned correctly *from its own fabricated reading* and produced Yellow.

Why this matters for production:
- The classifier protocol knowledge is correct. Gemma 4 knows MUAC < 11.5 cm = severe.
- But the vision capability at the E2B parameter count is not reliable for reading fine numeric / colour-band detail from images.
- **The safety layer did not catch this.** R13 only fires on danger-sign keywords in the text; the symptom text mentions a MUAC photo but no R13 keyword. R14 only fires below confidence 0.4; the model was confidently wrong at 0.95. R15 doesn't apply (paediatric). R16 disclaimer is the last line of defence — user must verify.
- **Net failure mode: silent, high-confidence misclassification on multimodal input.** The classifier appears to work; the answer is plausible; the patient gets Yellow when they need Pink.

## What this means for the v0.1 ship

- The multimodal path is **wired and reachable end-to-end** — `OllamaBackend.generate` did pass the base64 image, the model did accept it, the response came back, the JSON parsed, the safety layer ran, the eval scored it. That part of the architecture works.
- The multimodal **accuracy** at E2B is not field-ready. Photo input should be treated as a supplementary signal only — the text description must independently support the tier classification.
- This matches the README's documented limitation: *"Photo accuracy on darker skin tones. Disclosed in README. Photo is supplementary; text is primary."* This run confirms the limitation extends beyond skin tone to numeric and colour-band reading too.

## v0.2 mitigations

1. **Drop photo-derived confidence.** If a scenario references a photo, halve the reported confidence before R14 evaluates. That would force a 0.95 to 0.475 → still above the 0.4 floor; would need to drop further.
2. **Require text corroboration.** If the photo is the only source of a finding, append "Escalate to medical officer" automatically (a new R17 invariant).
3. **OCR pre-pass.** Run a deterministic OCR step on photos that contain visible numbers (MUAC tape, vitals on a meter screen) and verify the model's reading matches. Disagreement → escalate.
4. **Retest at E4B.** It is plausible (not verified) that the larger model would read the tape correctly. The E4B run is queued — see `notes/model-source.md` and `eval/airplane-test-log.md` for updates.

## Reproduce

```bash
# Requires Ollama running locally with gemma4:e2b pulled
cd laptop
. .venv/bin/activate
POCKETTRIAGE_BACKEND=ollama POCKETTRIAGE_OLLAMA_TIMEOUT_S=600 \
  python eval_runner.py --only S5-malnutrition-muac-photo --json
```
