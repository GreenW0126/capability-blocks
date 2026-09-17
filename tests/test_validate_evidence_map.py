import copy
import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "validate_evidence_map.py"
SPEC = importlib.util.spec_from_file_location("validate_evidence_map", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def valid_map():
    return {
        "schema_version": "1.2",
        "run_id": "synthetic-test",
        "generated_at": "2026-09-13T00:00:00Z",
        "updated_at": "2026-09-13T00:00:00Z",
        "retention": "user_managed",
        "blocks_artifact": {"path": "capability-blocks.md", "version": "test"},
        "experiences": [
            {
                "experience_id": "EXP-TEST",
                "label": "Synthetic project",
                "source_refs": ["synthetic:user-statement-1"],
                "organization_or_project": "Synthetic Project",
                "role_or_relationship": "Project lead",
                "date_range": {
                    "start": "2025-01",
                    "end": "2025-06",
                    "precision": "exact_month",
                },
                "metadata_status": "complete",
            }
        ],
        "evidence_units": [
            {
                "evidence_id": "E-TEST",
                "experience_id": "EXP-TEST",
                "source_type": "user_statement",
                "source_ref": "synthetic:user-statement-1",
                "raw_statement": "I led the project.",
                "normalized_fact": "Led the synthetic project.",
                "information_type": "fact",
                "ownership": "led",
            }
        ],
        "jd_sources": [
            {
                "jd_source_id": "JD-TEST",
                "role_title": "Researcher",
                "source_ref": "https://example.invalid/job",
                "accessed_at": "2026-09-13",
            }
        ],
        "demand_clusters": [
            {
                "demand_cluster_id": "D-TEST",
                "label": "Research delivery",
                "jd_source_refs": ["JD-TEST"],
            }
        ],
        "capability_mappings": [
            {
                "block_id": "CB-TEST",
                "display_label": "A",
                "title": "Research delivery",
                "evidence_links": [
                    {
                        "evidence_id": "E-TEST",
                        "supports": ["action"],
                        "mapping_reason": "The fact supports delivery ownership.",
                    }
                ],
                "demand_cluster_refs": ["D-TEST"],
                "safe_claims": ["Led a research project."],
                "claim_boundaries": [],
            }
        ],
    }


class EvidenceMapMetadataGateTest(unittest.TestCase):
    def test_complete_metadata_passes_handoff(self):
        MODULE.validate(valid_map(), handoff=True)

    def test_partial_metadata_passes_runtime_but_fails_handoff(self):
        data = copy.deepcopy(valid_map())
        experience = data["experiences"][0]
        experience["role_or_relationship"] = None
        experience["metadata_status"] = "partial"
        MODULE.validate(data)
        with self.assertRaisesRegex(ValueError, "CV handoff blocked"):
            MODULE.validate(data, handoff=True)

    def test_complete_status_cannot_mask_missing_metadata(self):
        data = copy.deepcopy(valid_map())
        data["experiences"][0]["date_range"]["start"] = None
        with self.assertRaisesRegex(ValueError, "metadata_status is complete"):
            MODULE.validate(data)


if __name__ == "__main__":
    unittest.main()
