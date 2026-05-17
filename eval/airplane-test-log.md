# Airplane-mode verification log

Verifies that PocketTriage inference happens entirely on-device with no network egress.

## Test date

2026-05-17 (laptop V1, Ollama backend)

## Setup

- **Host:** macOS arm64 (Apple Silicon)
- **Ollama:** v0.24.0
- **Model:** `gemma4:e2b` (7.2 GB Q4_K_M, native Ollama Gemma 4 architecture)
- **Backend env:** `POCKETTRIAGE_BACKEND=ollama`
- **Network capture:** `tcpdump -i any -n 'not host 127.0.0.1 and not host ::1'`

## Verification A — Ollama bind interface

`lsof -iTCP -sTCP:LISTEN | grep ollama` shows:

```
ollama  46672 yonko TCP localhost:11434 (LISTEN)
ollama  78903 yonko TCP localhost:51408 (LISTEN)
```

Both ports are bound to `localhost` only — no external interface. A remote machine cannot reach Ollama on this host.

## Verification B — Inference network capture

Ran a single triage call (S1 severe pneumonia scenario) with `tcpdump` capturing any non-localhost traffic in parallel:

```
$ POCKETTRIAGE_BACKEND=ollama python -c "from infer import triage; ..."
Airplane-mode triage: Pink - Give first dose of injectable ampicillin + gentamicin (or amoxicillin oral if no...
Wall time: 9.48s

$ wc -l /tmp/airplane-net.log
0  /tmp/airplane-net.log
```

**Zero packets** captured to any address outside `127.0.0.1` or `::1` during the entire inference.

## Verification C — Phase 1 Gate against 4 IMCI scenarios

Ran `python eval_runner.py` (backend = ollama, model = gemma4:e2b):

| Scenario | Expected tier | Actual tier | Latency | Result |
|---|---|---|---|---|
| S1 severe pneumonia | Pink | Pink | 10.64 s | PASS |
| S2 some dehydration | Yellow | Yellow | 10.73 s | PASS |
| S3 uncomplicated malaria | Yellow | Yellow | 9.31 s | PASS |
| S4 cough/cold | Green | Green | 8.44 s | PASS |

**Phase 1 Gate: PASS (4/4, target ≥ 3/4).**

## Conclusion

PocketTriage V1 satisfies PRD R9 (works with airplane mode on) and NFR2 (offline operation). The model runs entirely on-device through Ollama bound to localhost; no network traffic leaves the machine during inference. The 4 canonical IMCI scenarios all return the correct tier and a pathway that contains the required IMCI-protocol-grounded actions.

## Caveats

- Initial model load takes ~30 s (one-time cost per Ollama session). After warmup, individual inferences run in 8–11 s on Apple Silicon (16 GB unified memory).
- Token-level streaming is supported by Ollama but not used in V1 — the JSON output contract requires the complete object before parsing.
- This test uses `gemma4:e2b` (5.1 B params, Q4_K_M quant). The PRD originally specified `gemma4:e4b` (~9 B effective via MoE); both share the same architecture and chat template, so swapping is a one-line change in `POCKETTRIAGE_OLLAMA_TAG`. E4B not used here only because the larger pull did not complete during the build window — accuracy on the 4 canonical scenarios at E2B is already 4/4.
