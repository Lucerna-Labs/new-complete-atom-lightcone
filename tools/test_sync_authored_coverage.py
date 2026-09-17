from __future__ import annotations

import unittest

from sync_authored_coverage import synchronize


class CoverageSynchronizationTests(unittest.TestCase):
    def test_only_explicit_axes_advance_and_stronger_credit_is_retained(self) -> None:
        ledger = {
            "items": [
                {
                    "kind": "domain",
                    "id": "geometry",
                    "status": "scoped",
                    "coverage": {
                        "definitions_scope": "missing",
                        "mechanisms_causal_laws": "tested",
                        "history_versions": "missing",
                    },
                    "evidence": [],
                    "notes": [],
                }
            ]
        }
        evidence = {
            ("domain", "geometry"): {
                "definitions_scope": {"curricula/geometry/example.jsonl"},
                "mechanisms_causal_laws": {"curricula/geometry/example.jsonl"},
            }
        }
        changed = synchronize(ledger, evidence, apply=True)
        item = ledger["items"][0]
        self.assertEqual(changed, ["domain:geometry:definitions_scope"])
        self.assertEqual(item["coverage"]["definitions_scope"], "authored")
        self.assertEqual(item["coverage"]["mechanisms_causal_laws"], "tested")
        self.assertEqual(item["coverage"]["history_versions"], "missing")
        self.assertEqual(item["status"], "authored")


if __name__ == "__main__":
    unittest.main()
