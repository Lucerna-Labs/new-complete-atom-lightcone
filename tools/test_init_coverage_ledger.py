from __future__ import annotations

import unittest

from init_coverage_ledger import merge_existing


class CoverageLedgerMergeTests(unittest.TestCase):
    def test_merge_preserves_existing_evidence_and_adds_new_item(self) -> None:
        existing_item = {
            "kind": "domain",
            "id": "geometry",
            "status": "authored",
            "coverage": {"definitions_scope": "authored"},
            "evidence": ["curricula/geometry/foundations.jsonl"],
        }
        new_item = {
            "kind": "subfield",
            "id": "geometry.shadow-projection",
            "status": "discovered",
            "coverage": {"definitions_scope": "missing"},
            "evidence": [],
        }
        merged = merge_existing(
            {"items": [existing_item]},
            [existing_item.copy(), new_item],
        )
        by_id = {item["id"]: item for item in merged["items"]}
        self.assertEqual(by_id["geometry"]["status"], "authored")
        self.assertEqual(
            by_id["geometry"]["evidence"],
            ["curricula/geometry/foundations.jsonl"],
        )
        self.assertEqual(
            by_id["geometry.shadow-projection"]["status"],
            "discovered",
        )

    def test_merge_rejects_catalog_removal(self) -> None:
        with self.assertRaisesRegex(ValueError, "absent from catalogs"):
            merge_existing(
                {"items": [{"kind": "domain", "id": "removed"}]},
                [],
            )


if __name__ == "__main__":
    unittest.main()
