#!/usr/bin/env python3
"""Audit per-(item, axis) record density across the curricula.

The coverage ledger tracks whether an axis is authored/tested/sealed; it
does not track HOW MUCH source-bound evidence stands behind each axis.
This tool measures depth: it credits every curriculum record to the
(domain, subfield, lane) items exactly the way `sync_authored_coverage.py`
does, counts records per (item, axis) pair, and reports the density
matrix.  Depth is the honest completeness metric for a model that is
expected to use the catalog thoroughly: an axis held up by one record is
not the same power as an axis held up by forty.

Report-only by default.  `--min-per-pair N` turns it into a gate that
fails while any mandatory, non-inapplicable (item, axis) pair carries
fewer than N records.  `--write` persists the deterministic report to
plans/coverage-density-v1.json.
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path
from typing import Any

from registry_lib import COVERAGE_AXES, COVERAGE_LEDGER, ROOT, load_json

REPORT = ROOT / "plans" / "coverage-density-v1.json"

# Axes closed by runtime receipts rather than curriculum records.  The
# coverage-closure world deliberately never claims adapter accessibility;
# it is credited by adapter conformance receipts, so record density does
# not apply to it.
RECEIPT_BACKED_AXES = {"adapter_accessibility"}


def collect_pair_counts(
    skip: Path | None = None,
) -> tuple[dict[tuple[str, str], dict[str, int]], list[str], int]:
    """Credit every record to its (domain, subfield, lane) targets.

    Mirrors sync_authored_coverage.collect_explicit_evidence so the
    density metric and the ledger credit rule can never drift apart.
    `skip` excludes one file (generators exclude their own output so
    regeneration stays idempotent).
    """
    counts: dict[tuple[str, str], dict[str, int]] = collections.defaultdict(
        lambda: collections.Counter()
    )
    axis_ids = {axis["id"] for axis in load_json(COVERAGE_AXES)["axes"]}
    errors: list[str] = []
    scanned = 0
    for path in sorted((ROOT / "curricula").rglob("*.jsonl")):
        if skip is not None and path == skip:
            continue
        location = str(path.relative_to(ROOT))
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if not line.strip():
                continue
            scanned += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                errors.append(f"{location}:{line_number}: {error}")
                continue
            unknown_axes = sorted(set(record.get("coverage_axes", [])) - axis_ids)
            if unknown_axes:
                errors.append(
                    f"{location}:{line_number}: unknown coverage axes {unknown_axes}"
                )
                continue
            targets = [
                ("domain", record["domain_id"]),
                ("subfield", record["subject_id"]),
                *(("lane", lane) for lane in record["lanes"]),
            ]
            for kind, item_id in targets:
                for axis in record["coverage_axes"]:
                    counts[(kind, item_id)][axis] += 1
    return {key: dict(value) for key, value in counts.items()}, errors, scanned


def build_report(min_per_pair: int) -> dict[str, Any]:
    ledger = load_json(COVERAGE_LEDGER)
    counts, errors, scanned = collect_pair_counts()
    axis_ids = sorted(load_json(COVERAGE_AXES)["axes"], key=lambda axis: axis["id"])
    axis_ids = [axis["id"] for axis in axis_ids]

    per_axis_totals: dict[str, int] = {axis: 0 for axis in axis_ids}
    credited_pairs = 0
    below: list[dict[str, Any]] = []
    mandatory_pairs = 0
    exempt_pairs = 0
    for item in ledger["items"]:
        kind = item["kind"]
        item_id = item["id"]
        for axis in axis_ids:
            if item["coverage"][axis] == "inapplicable" or not item.get("mandatory"):
                exempt_pairs += 1
                continue
            if axis in RECEIPT_BACKED_AXES:
                exempt_pairs += 1
                continue
            mandatory_pairs += 1
            count = counts.get((kind, item_id), {}).get(axis, 0)
            per_axis_totals[axis] += count
            if count > 0:
                credited_pairs += 1
            if count < min_per_pair:
                below.append(
                    {
                        "kind": kind,
                        "id": item_id,
                        "axis": axis,
                        "records": count,
                    }
                )

    below.sort(key=lambda row: (row["records"], row["kind"], row["id"], row["axis"]))
    return {
        "schema_version": 1,
        "tool": "audit_coverage_density",
        "min_per_pair": min_per_pair,
        "records_scanned": scanned,
        "mandatory_pairs": mandatory_pairs,
        "exempt_pairs": exempt_pairs,
        "credited_pairs": credited_pairs,
        "zero_pairs": sum(1 for row in below if row["records"] == 0),
        "pairs_below_min": len(below),
        "per_axis_totals": dict(
            sorted(per_axis_totals.items(), key=lambda kv: kv[1])
        ),
        "below_min": below,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--min-per-pair",
        type=int,
        default=4,
        help="fail while any mandatory non-inapplicable pair carries fewer records (0 disables)",
    )
    parser.add_argument("--write", action="store_true", help="persist the report")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report(args.min_per_pair)
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

    failed = bool(report["errors"]) or (
        args.min_per_pair > 0 and report["pairs_below_min"] > 0
    )
    result = {key: value for key, value in report.items() if key != "below_min"}
    result["report_path"] = str(REPORT.relative_to(ROOT)) if args.write else None
    result["density_ok"] = not failed
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"records scanned: {report['records_scanned']}")
        print(
            f"mandatory (item, axis) pairs: {report['mandatory_pairs']} "
            f"(exempt: {report['exempt_pairs']})"
        )
        print(
            f"credited pairs: {report['credited_pairs']}/{report['mandatory_pairs']} "
            f"({100 * report['credited_pairs'] / max(1, report['mandatory_pairs']):.1f}%)"
        )
        print(f"zero-record pairs: {report['zero_pairs']}")
        print(f"pairs below min {args.min_per_pair}: {report['pairs_below_min']}")
        print("per-axis record totals (ascending):")
        for axis, total in report["per_axis_totals"].items():
            print(f"  {axis:45s} {total:8d}")
        for error in report["errors"]:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"density_ok: {result['density_ok']}")
        if args.write:
            print(f"report: {result['report_path']}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
