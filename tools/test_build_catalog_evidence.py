from __future__ import annotations

import unittest

from build_catalog_evidence import predict_sealed_ledger


class CatalogSealPredictionTests(unittest.TestCase):
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
