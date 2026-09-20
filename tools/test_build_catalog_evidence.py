from __future__ import annotations

import unittest

from build_catalog_evidence import pack_version, predict_sealed_ledger


class CatalogSealPredictionTests(unittest.TestCase):
    def test_catalog_revision_selects_new_immutable_pack_versions(self) -> None:
        self.assertEqual(pack_version("geometry-foundation-v0", 1), "0.1.0")
        self.assertEqual(pack_version("foundation-lanes-v0", 1), "0.2.0")
        self.assertEqual(pack_version("geometry-foundation-v0", 2), "0.2.0")
        self.assertEqual(pack_version("foundation-lanes-v0", 2), "0.3.0")

    def test_prediction_matches_explicit_all_axis_transition(self) -> None:
        ledger = {
            "schema_version": 1,
            "items": [
                {
                    "id": "lane",
                    "status": "accelerator_validated",
                    "coverage": {"facts": "tested", "tools": "inapplicable"},
                    "evidence": ["old.json"],
                    "notes": [],
                }
            ],
        }
        result = predict_sealed_ledger(
            ledger,
            ["facts", "tools"],
            "receipts/seals/catalog.json",
            "sealed",
        )
        self.assertEqual(result["items"][0]["status"], "sealed")
        self.assertEqual(result["items"][0]["coverage"], {"facts": "sealed", "tools": "sealed"})
        self.assertEqual(result["items"][0]["evidence"][-1], "receipts/seals/catalog.json")
        self.assertEqual(result["items"][0]["notes"], ["sealed"])
        self.assertEqual(ledger["items"][0]["status"], "accelerator_validated")


if __name__ == "__main__":
    unittest.main()
