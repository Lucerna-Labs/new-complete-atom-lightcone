#!/usr/bin/env python3
"""Reopen ledger coverage credited by curriculum records that changed since a sealed baseline.

A sealed item cites curriculum files by path, not by hash, so changing a cited
record would otherwise leave the item claiming a seal over content that was
never trained or validated. Every item a changed, added or removed record
credits (its domain, subfield and lanes) returns to `authored`, as do the
axes that record declares.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from registry_lib import COVERAGE_LEDGER, COVERAGE_ORDER, ROOT, STATUS_ORDER


def records_at(revision: str | None) -> dict[str, tuple[str, dict[str, Any]]]:
    """record_id -> (curriculum path, record) at a git revision, or in the worktree when None."""
    if revision is None:
        paths = sorted(str(path.relative_to(ROOT)) for path in (ROOT / "curricula").rglob("*.jsonl"))
    else:
        listing = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", revision, "curricula"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        ).stdout.split()
        paths = sorted(path for path in listing if path.endswith(".jsonl"))
    records: dict[str, tuple[str, dict[str, Any]]] = {}
    for path in paths:
        if revision is None:
            text = (ROOT / path).read_text(encoding="utf-8")
        else:
            text = subprocess.run(
                ["git", "show", f"{revision}:{path}"], cwd=ROOT, check=True, capture_output=True, text=True,
            ).stdout
        for line in text.splitlines():
            if line.strip():
                record = json.loads(line)
                if record["record_id"] in records:
                    raise ValueError(f"duplicate record {record['record_id']}")
                records[record["record_id"]] = (path, record)
    return records


def changed_records(
    before: dict[str, tuple[str, dict[str, Any]]],
    after: dict[str, tuple[str, dict[str, Any]]],
) -> list[dict[str, Any]]:
    changes = []
    for record_id in sorted(set(before) | set(after)):
        old = before.get(record_id)
        new = after.get(record_id)
        if old == new:
            continue
        fields = sorted(
            key for key in set(old[1] if old else {}) | set(new[1] if new else {})
            if (old[1].get(key) if old else None) != (new[1].get(key) if new else None)
        )
        changes.append({
            "record_id": record_id,
            "change": "added" if old is None else "removed" if new is None else "changed",
            "fields": fields,
            "versions": [version for version in (old, new) if version is not None],
        })
    return changes


def reopen(ledger: dict[str, Any], changes: list[dict[str, Any]], note: str, evidence: str) -> list[str]:
    targets: dict[tuple[str, str], set[str]] = {}
    for change in changes:
        for _, record in change["versions"]:
            keys = [("domain", record["domain_id"]), ("subfield", record["subject_id"])]
            keys += [("lane", lane) for lane in record["lanes"]]
            for key in keys:
                targets.setdefault(key, set()).update(record.get("coverage_axes", []))
    authored = STATUS_ORDER.index("authored")
    authored_axis = COVERAGE_ORDER.index("authored")
    reopened = []
    for item in ledger["items"]:
        axes = targets.get((item["kind"], item["id"]))
        if axes is None:
            continue
        if item["status"] in STATUS_ORDER and STATUS_ORDER.index(item["status"]) > authored:
            item["status"] = "authored"
        for axis in sorted(axes):
            current = item["coverage"].get(axis)
            if current in COVERAGE_ORDER and COVERAGE_ORDER.index(current) > authored_axis:
                item["coverage"][axis] = "authored"
        # A reopened item cannot keep sealed axes beside its authored status.
        for axis, current in item["coverage"].items():
            if current == "sealed":
                item["coverage"][axis] = "authored"
        if note not in item["notes"]:
            item["notes"].append(note)
        item["evidence"] = sorted({*item["evidence"], evidence})
        reopened.append(f"{item['kind']}:{item['id']}")
    return reopened


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, help="sealed git revision to compare against")
    parser.add_argument("--note", required=True)
    parser.add_argument("--evidence", required=True, help="repository path that explains the reopening")
    parser.add_argument("--report", type=Path, help="write the record diff and reopened items as JSON")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    changes = changed_records(records_at(args.baseline), records_at(None))
    ledger = json.loads(COVERAGE_LEDGER.read_text(encoding="utf-8"))
    reopened = reopen(ledger, changes, args.note, args.evidence)
    summary = {
        "baseline": args.baseline,
        "changed_records": [{key: change[key] for key in ("record_id", "change", "fields")} for change in changes],
        "reopened_items": reopened,
    }
    if args.report:
        args.report.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.apply:
        COVERAGE_LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"changed records: {len(changes)}; reopened items: {len(reopened)}{'' if args.apply else ' (dry run)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
