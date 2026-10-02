from __future__ import annotations

import unittest

from reopen_coverage import changed_records, reopen


def record(record_id: str, label: str, axes: list[str]) -> dict:
    return {"record_id": record_id, "domain_id": "geometry", "subject_id": "geometry.metric",
            "lanes": ["reasoning.causal"], "label": label, "coverage_axes": axes}


def item(kind: str, item_id: str) -> dict:
    return {"kind": kind, "id": item_id, "status": "sealed",
            "coverage": {"definitions_scope": "sealed", "history_versions": "sealed", "unknown_abstention": "inapplicable"},
            "evidence": ["curricula/geometry/a.jsonl"], "notes": []}


class ReopenCoverageTests(unittest.TestCase):
    def test_changed_added_and_removed_records_are_reported_with_fields(self) -> None:
        before = {"a": ("p", record("a", "Set", [])), "b": ("p", record("b", "B", [])), "c": ("p", record("c", "C", []))}
        after = {"a": ("p", record("a", "Set (mathematics)", [])), "b": ("p", record("b", "B", [])), "d": ("p", record("d", "D", []))}
        changes = changed_records(before, after)
        self.assertEqual([(c["record_id"], c["change"], c["fields"]) for c in changes],
                         [("a", "changed", ["label"]), ("c", "removed", ["coverage_axes", "domain_id", "label", "lanes", "record_id", "subject_id"]),
                          ("d", "added", ["coverage_axes", "domain_id", "label", "lanes", "record_id", "subject_id"])])
        self.assertEqual(changed_records(before, before), [])

    def test_only_credited_items_reopen_and_no_sealed_axis_survives(self) -> None:
        ledger = {"items": [item("domain", "geometry"), item("subfield", "geometry.metric"),
                            item("lane", "reasoning.causal"), item("domain", "sciences")]}
        changes = changed_records({"a": ("p", record("a", "Set", ["definitions_scope"]))},
                                  {"a": ("p", record("a", "Set (mathematics)", ["definitions_scope"]))})
        reopened = reopen(ledger, changes, "reopened for v3", "plans/x.md")
        self.assertEqual(reopened, ["domain:geometry", "subfield:geometry.metric", "lane:reasoning.causal"])
        for row in ledger["items"][:3]:
            self.assertEqual(row["status"], "authored")
            self.assertEqual(row["coverage"], {"definitions_scope": "authored", "history_versions": "authored", "unknown_abstention": "inapplicable"})
            self.assertEqual(row["notes"], ["reopened for v3"])
            self.assertIn("plans/x.md", row["evidence"])
        self.assertEqual(ledger["items"][3]["status"], "sealed")
        self.assertEqual(ledger["items"][3]["coverage"]["definitions_scope"], "sealed")
        self.assertEqual(reopen(ledger, changes, "reopened for v3", "plans/x.md"), reopened)
        self.assertEqual(ledger["items"][0]["notes"], ["reopened for v3"])


if __name__ == "__main__":
    unittest.main()
