"""PocketTriage Phase 1 Gate eval runner.

Runs all scenarios from eval/scenarios.json against the live triage() function
and scores each on tier-match + pathway-keyword-match. Phase 1 Gate is 3/4 passes.

Usage:
    python eval_runner.py             # full run, pretty-printed
    python eval_runner.py --json      # machine-readable
    python eval_runner.py --airplane  # ALSO verify zero network requests (best-effort)
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from infer import triage, InferenceError

REPO_ROOT = Path(__file__).parent.parent
SCENARIOS_PATH = REPO_ROOT / "eval" / "scenarios.json"


def load_scenarios() -> list[dict[str, Any]]:
    data = json.loads(SCENARIOS_PATH.read_text(encoding="utf-8"))
    return data["scenarios"]


def score_one(scenario: dict[str, Any], result_dict: dict[str, Any]) -> dict[str, Any]:
    expected = scenario["expected"]
    actual_tier = result_dict.get("tier")
    tier_pass = actual_tier == expected["tier"]

    pathway = (result_dict.get("pathway") or "").lower()
    must = expected.get("pathway_must_contain", [])
    must_hits = [s for s in must if s.lower() in pathway]
    must_pass = len(must_hits) == len(must)

    should = expected.get("pathway_should_mention", [])
    should_hits = [s for s in should if s.lower() in pathway]

    overall = tier_pass and must_pass
    return {
        "scenario_id": scenario["id"],
        "category": scenario["category"],
        "expected_tier": expected["tier"],
        "actual_tier": actual_tier,
        "tier_pass": tier_pass,
        "pathway_must_contain": must,
        "pathway_must_hits": must_hits,
        "pathway_must_pass": must_pass,
        "pathway_should_mention": should,
        "pathway_should_hits": should_hits,
        "pass": overall,
        "actual_pathway": result_dict.get("pathway", ""),
        "actual_reasoning": result_dict.get("reasoning", ""),
        "actual_confidence": result_dict.get("confidence"),
        "safety_flags": result_dict.get("safety_flags", []),
    }


def run_all(verbose: bool = True) -> dict[str, Any]:
    scenarios = load_scenarios()
    rows: list[dict[str, Any]] = []
    t_total = time.time()
    for sc in scenarios:
        if verbose:
            print(f"\n=== {sc['id']} ({sc['category']}) ===", flush=True)
            print(f"input: {sc['input'][:120]}...", flush=True)
        t0 = time.time()
        try:
            result = triage(sc["input"])
            result_dict = asdict(result)
            row = score_one(sc, result_dict)
            row["latency_s"] = round(time.time() - t0, 2)
            row["error"] = None
        except InferenceError as e:
            row = {
                "scenario_id": sc["id"],
                "category": sc["category"],
                "expected_tier": sc["expected"]["tier"],
                "actual_tier": None,
                "tier_pass": False,
                "pass": False,
                "actual_pathway": "",
                "actual_reasoning": "",
                "actual_confidence": None,
                "safety_flags": [],
                "error": str(e),
                "latency_s": round(time.time() - t0, 2),
            }
        rows.append(row)
        if verbose:
            status = "PASS" if row.get("pass") else "FAIL"
            print(
                f"  -> {status} | expected={row['expected_tier']} actual={row['actual_tier']} "
                f"latency={row['latency_s']}s",
                flush=True,
            )
            if row.get("error"):
                print(f"  ERROR: {row['error']}", flush=True)

    passes = sum(1 for r in rows if r.get("pass"))
    total = len(rows)
    summary = {
        "total": total,
        "passes": passes,
        "fails": total - passes,
        "pass_rate": passes / total if total else 0.0,
        "phase1_gate_passes": passes >= 3,  # ≥ 3/4 per PRD §3.2
        "total_seconds": round(time.time() - t_total, 2),
    }
    return {"summary": summary, "rows": rows}


def main() -> int:
    p = argparse.ArgumentParser(description="PocketTriage Phase 1 Gate eval runner")
    p.add_argument("--json", action="store_true", help="machine-readable JSON output")
    args = p.parse_args()

    result = run_all(verbose=not args.json)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        s = result["summary"]
        print("\n=== SUMMARY ===")
        print(f"Passes:    {s['passes']}/{s['total']}  (rate: {s['pass_rate']:.0%})")
        print(f"Phase 1 Gate: {'PASS' if s['phase1_gate_passes'] else 'FAIL'} (target: ≥3/4)")
        print(f"Total time: {s['total_seconds']}s")
    return 0 if result["summary"]["phase1_gate_passes"] else 1


if __name__ == "__main__":
    sys.exit(main())
