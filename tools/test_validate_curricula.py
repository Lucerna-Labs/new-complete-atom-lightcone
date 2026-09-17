from __future__ import annotations

import unittest

from validate_curricula import worked_example_errors


def example(split: str) -> dict[str, object]:
    return {
        "world_id": "example-world",
        "record_id": f"example.{split}",
        "record_kind": "worked_example",
        "split": split,
    }


class WorkedExampleCoverageTests(unittest.TestCase):
    def test_complete_connected_example_set_passes(self) -> None:
        records = [example(split) for split in ("train", "validation", "sealed_test")]
        records.extend(
            {
                "world_id": "example-world",
                "record_id": f"membership.{split}",
                "record_kind": "relation",
                "split": split,
                "relation": {
                    "source_node": f"example.{split}",
                    "target_node": "root",
                },
            }
            for split in ("train", "validation", "sealed_test")
        )
        self.assertEqual(worked_example_errors(records), [])

    def test_missing_and_disconnected_examples_fail(self) -> None:
        errors = worked_example_errors([example("train")])
        self.assertTrue(any("validation" in error for error in errors))
        self.assertTrue(any("sealed_test" in error for error in errors))
        self.assertTrue(any("disconnected" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
