from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from registry_lib import file_hash
from validate_revocations import validate


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


class RevocationSupersessionTests(unittest.TestCase):
    def test_changed_replacement_requires_hash_bound_supersession(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            write_json(
                root / "sources" / "exclusions.json",
                {"exclusions": [{"source_id": "excluded-source"}]},
            )
            pack = root / "artifacts" / "worlds" / "world" / "1.0.0"
            write_json(pack / "manifest.json", {"fixture": True})
            write_json(
                pack / "sources.json",
                {"sources": [{"source_id": "excluded-source"}]},
            )
            replacement = root / "curricula" / "world" / "foundations.jsonl"
            replacement.parent.mkdir(parents=True)
            replacement.write_text(
                json.dumps({"source_ids": ["safe-source"]}) + "\n",
                encoding="utf-8",
            )
            base = {
                "schema_version": 1,
                "revocation_id": "world-source-rights",
                "world_id": "world",
                "world_version": "1.0.0",
                "manifest_sha256": file_hash(pack / "manifest.json"),
                "revoked_at": "2026-09-03",
                "reason_class": "source_rights_restriction",
                "affected_source_ids": ["excluded-source"],
                "source_evidence": [],
                "decision": "excluded_from_active_world_acceptance",
                "artifact_retained_for_audit": True,
                "replacement_curriculum": "curricula/world/foundations.jsonl",
                "replacement_curriculum_sha256": "0" * 64,
                "replacement_status": "authored",
                "notes": [],
            }
            base_path = root / "receipts" / "revocations" / "base.json"
            write_json(base_path, base)
            supersession = {
                "schema_version": 1,
                "supersession_id": "world-replacement-update",
                "supersedes_revocation": "world-source-rights",
                "superseded_receipt_sha256": file_hash(base_path),
                "world_id": "world",
                "world_version": "1.0.0",
                "created_at": "2026-09-04",
                "reason_class": "replacement_curriculum_evolved",
                "affected_source_ids": ["excluded-source"],
                "decision": "replacement_evidence_rebound",
                "replacement_curriculum": "curricula/world/foundations.jsonl",
                "replacement_curriculum_sha256": file_hash(replacement),
                "replacement_status": "authored",
                "excluded_source_overlap": [],
                "notes": [],
            }
            supersession_path = (
                root / "receipts" / "revocations" / "supersession.json"
            )
            write_json(supersession_path, supersession)
            self.assertEqual(validate(root)[2], [])

            replacement.write_text(
                json.dumps({"source_ids": ["safe-source"], "revision": 2}) + "\n",
                encoding="utf-8",
            )
            chained = {
                **supersession,
                "supersession_id": "world-replacement-update-2",
                "supersedes_revocation": "world-replacement-update",
                "superseded_receipt_sha256": file_hash(supersession_path),
                "created_at": "2026-09-05",
                "replacement_curriculum_sha256": file_hash(replacement),
            }
            chained_path = root / "receipts" / "revocations" / "supersession-2.json"
            write_json(chained_path, chained)
            self.assertEqual(validate(root)[2], [])

            chained["superseded_receipt_sha256"] = "f" * 64
            write_json(chained_path, chained)
            errors = validate(root)[2]
            self.assertTrue(any("superseded receipt hash differs" in error for error in errors))
            self.assertTrue(any("without a valid supersession" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
