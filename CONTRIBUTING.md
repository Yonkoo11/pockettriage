# Contributing to PocketTriage

PocketTriage is open infrastructure for community health workers. We want it adopted, modified, and translated, not sold.

## What we're looking for

In rough priority order:

1. **Localization** — the system prompt and UI strings need to land in the languages CHWs actually speak. Hindi, Igbo, Hausa, Swahili, Yoruba, Bangla, French (West Africa), Portuguese (Lusophone Africa), Amharic.
2. **Eval scenarios from regional training material** — `eval/scenarios.json` covers 4 canonical IMCI cases. Real CHW programmes have richer presentations.
3. **Android V2** — the LiteRT-based Android implementation lives in `android/`. Improvements to the inference path, camera capture flow, and APK build are all welcome.
4. **Deployment feedback** — if you ran PocketTriage in a real clinical setting, please open an issue tagged `field-report` with what worked, what failed, and which IMCI categories the model got wrong.

## What we will not accept

- Cloud-routing patches. PocketTriage is on-device by architecture; any change that introduces a remote inference call is out of scope.
- Telemetry, analytics, crash reporters, or any other phone-home behaviour.
- Feature creep into adult medicine. PocketTriage is paediatric IMCI (2 months – 5 years). Adult tools are different products.
- Removal of the disclaimer banner R7.
- Patches that weaken the R13–R15 safety layer without an equivalent or stronger replacement.

## Development setup

```bash
git clone https://github.com/yonkoo11/pockettriage
cd pockettriage/laptop
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pytest

# Run the unit tests
pytest test_safety.py -v

# Run the eval suite (requires Ollama + gemma4:e4b)
python eval_runner.py
```

## Pull request checklist

- [ ] `pytest test_safety.py` passes
- [ ] `python eval_runner.py` Phase 1 Gate still passes (≥ 3/4 scenarios)
- [ ] No new direct network calls outside `127.0.0.1:11434`
- [ ] Disclaimer banner R7 still rendered in UI
- [ ] Safety layer R13–R15 still enforced
- [ ] If touching the system prompt: list of changes in PR description with rationale
- [ ] If touching scenarios: cite the WHO IMCI source section for new expected outcomes

## Code of conduct

We follow the Contributor Covenant 2.1. See `CODE_OF_CONDUCT.md`.

## License

By contributing you agree your work is licensed under Apache 2.0 (see `LICENSE`).
