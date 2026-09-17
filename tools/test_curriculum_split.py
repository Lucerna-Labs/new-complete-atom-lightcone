from __future__ import annotations

import unittest

from curriculum_split import RelationSplitter


class RelationSplitterTests(unittest.TestCase):
    def test_planned_cross_preserves_validation_and_sealed_examples(self) -> None:
        splitter = RelationSplitter(
            ["supports"] * 6,
            cross_plan=[False, False, False, False, False, True],
        )
        observed = [splitter.split("supports") for _ in range(6)]
        self.assertEqual(
            observed,
            ["train", "train", "train", "validation", "sealed_test", "cross_domain_holdout"],
        )

    def test_first_relation_remains_training_support(self) -> None:
        splitter = RelationSplitter(
            ["supports", "supports"],
            cross_plan=[True, True],
        )
        self.assertEqual(
            splitter.split("supports"),
            "train",
        )

    def test_cross_plan_length_must_match(self) -> None:
        with self.assertRaisesRegex(ValueError, "one-for-one"):
            RelationSplitter(["supports"], cross_plan=[])


if __name__ == "__main__":
    unittest.main()
