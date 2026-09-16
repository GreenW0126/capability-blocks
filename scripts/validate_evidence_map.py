#!/usr/bin/env python3
"""Validate cross-reference invariants in a capability evidence map."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def fail(message: str) -> None:
    raise ValueError(message)


def unique_ids(records: list[dict], key: str) -> set[str]:
    values = [record.get(key) for record in records]
    if any(not isinstance(value, str) or not value for value in values):
        fail(f"every {key} must be a non-empty string")
    if len(values) != len(set(values)):
        fail(f"duplicate {key}")
    return set(values)


def require_pattern(value: str, pattern: str, label: str) -> None:
    if not re.fullmatch(pattern, value):
        fail(f"invalid {label}: {value}")


def metadata_is_complete(experience: dict) -> bool:
    if experience.get("metadata_status") != "complete":
        return False
    if not isinstance(experience.get("organization_or_project"), str) or not experience[
        "organization_or_project"
    ].strip():
        return False
    if not isinstance(experience.get("role_or_relationship"), str) or not experience[
        "role_or_relationship"
    ].strip():
        return False
    date_range = experience.get("date_range")
    if not isinstance(date_range, dict):
        return False
    if not isinstance(date_range.get("start"), str) or not date_range["start"].strip():
        return False
    if not isinstance(date_range.get("end"), str) or not date_range["end"].strip():
        return False
    return date_range.get("precision") in {"exact_month", "exact_year", "approximate"}


def validate(data: dict, handoff: bool = False) -> None:
    required = {
        "schema_version",
        "run_id",
        "generated_at",
        "updated_at",
        "retention",
        "blocks_artifact",
        "experiences",
        "evidence_units",
        "jd_sources",
        "demand_clusters",
        "capability_mappings",
    }
    missing = sorted(required - data.keys())
    if missing:
        fail(f"missing top-level fields: {', '.join(missing)}")
    if data["schema_version"] != "1.1":
        fail("schema_version must be 1.1")
    if data["retention"] != "runtime_only":
        fail("retention must be runtime_only")
    blocks_artifact = data["blocks_artifact"]
    if not isinstance(blocks_artifact, dict):
        fail("blocks_artifact must be an object")
    if not blocks_artifact.get("path") or not blocks_artifact.get("version"):
        fail("blocks_artifact requires path and version")

    for key in (
        "experiences",
        "evidence_units",
        "jd_sources",
        "demand_clusters",
        "capability_mappings",
    ):
        if not isinstance(data[key], list) or not data[key]:
            fail(f"{key} must be a non-empty array")

    experience_ids = unique_ids(data["experiences"], "experience_id")
    evidence_ids = unique_ids(data["evidence_units"], "evidence_id")
    jd_ids = unique_ids(data["jd_sources"], "jd_source_id")
    demand_ids = unique_ids(data["demand_clusters"], "demand_cluster_id")
    block_ids = unique_ids(data["capability_mappings"], "block_id")

    for value in experience_ids:
        require_pattern(value, r"EXP-[A-Za-z0-9_-]+", "experience_id")
    for value in evidence_ids:
        require_pattern(value, r"E-[A-Za-z0-9_-]+", "evidence_id")
    for value in jd_ids:
        require_pattern(value, r"JD-[A-Za-z0-9_-]+", "jd_source_id")
    for value in demand_ids:
        require_pattern(value, r"D-[A-Za-z0-9_-]+", "demand_cluster_id")
    for value in block_ids:
        require_pattern(value, r"CB-[A-Za-z0-9_-]+", "block_id")

    allowed_metadata_statuses = {
        "complete",
        "partial",
        "user_withheld",
        "not_applicable",
    }
    allowed_date_precisions = {
        "exact_month",
        "exact_year",
        "approximate",
        "unknown",
        "user_withheld",
    }
    experience_by_id = {item["experience_id"]: item for item in data["experiences"]}
    for experience in data["experiences"]:
        for key in (
            "organization_or_project",
            "role_or_relationship",
            "date_range",
            "metadata_status",
        ):
            if key not in experience:
                fail(f"missing {key} in {experience['experience_id']}")
        if experience["metadata_status"] not in allowed_metadata_statuses:
            fail(f"invalid metadata_status in {experience['experience_id']}")
        date_range = experience["date_range"]
        if date_range is not None:
            if not isinstance(date_range, dict):
                fail(f"date_range must be an object or null in {experience['experience_id']}")
            for key in ("start", "end", "precision"):
                if key not in date_range:
                    fail(f"missing date_range.{key} in {experience['experience_id']}")
            if date_range["precision"] not in allowed_date_precisions:
                fail(f"invalid date_range.precision in {experience['experience_id']}")
        if experience["metadata_status"] == "complete" and not metadata_is_complete(experience):
            fail(f"metadata_status is complete but required metadata is unusable in {experience['experience_id']}")

    labels = [mapping.get("display_label") for mapping in data["capability_mappings"]]
    if len(labels) != len(set(labels)):
        fail("duplicate display_label")
    if any(label not in {"A", "B", "C", "D"} for label in labels):
        fail("display_label must be A, B, C, or D")

    evidence_by_id = {item["evidence_id"]: item for item in data["evidence_units"]}
    allowed_source_types = {
        "user_correction",
        "user_confirmation",
        "user_statement",
        "user_file",
        "old_cv",
    }
    allowed_information_types = {"fact", "interpretation", "hypothesis"}
    allowed_ownership = {
        "led",
        "owned",
        "co_led",
        "collaborated",
        "contributed",
        "observed",
        "unspecified",
    }
    for item in data["evidence_units"]:
        if item.get("experience_id") not in experience_ids:
            fail(f"unresolved experience_id in {item['evidence_id']}")
        for key in ("source_ref", "raw_statement", "normalized_fact", "information_type", "ownership"):
            if not item.get(key):
                fail(f"missing {key} in {item['evidence_id']}")
        if item["source_type"] not in allowed_source_types:
            fail(f"invalid source_type in {item['evidence_id']}")
        if item["information_type"] not in allowed_information_types:
            fail(f"invalid information_type in {item['evidence_id']}")
        if item["ownership"] not in allowed_ownership:
            fail(f"invalid ownership in {item['evidence_id']}")

    for cluster in data["demand_clusters"]:
        if not cluster.get("jd_source_refs"):
            fail(f"{cluster['demand_cluster_id']} has no JD source refs")
        for ref in cluster.get("jd_source_refs", []):
            if ref not in jd_ids:
                fail(f"unresolved JD ref {ref} in {cluster['demand_cluster_id']}")

    for mapping in data["capability_mappings"]:
        links = mapping.get("evidence_links", [])
        if not links:
            fail(f"{mapping['block_id']} has no evidence links")
        for link in links:
            ref = link.get("evidence_id")
            if ref not in evidence_ids:
                fail(f"unresolved evidence ref {ref} in {mapping['block_id']}")
            if evidence_by_id[ref].get("information_type") == "hypothesis":
                fail(f"{mapping['block_id']} uses hypothesis {ref} as direct evidence")
            if not link.get("supports") or not link.get("mapping_reason"):
                fail(f"incomplete evidence link {ref} in {mapping['block_id']}")
        for ref in mapping.get("demand_cluster_refs", []):
            if ref not in demand_ids:
                fail(f"unresolved demand ref {ref} in {mapping['block_id']}")
        if not mapping.get("demand_cluster_refs"):
            fail(f"{mapping['block_id']} has no demand cluster refs")
        if not mapping.get("safe_claims"):
            fail(f"{mapping['block_id']} has no safe claims")

    if handoff:
        referenced_experience_ids = {
            evidence_by_id[link["evidence_id"]]["experience_id"]
            for mapping in data["capability_mappings"]
            for link in mapping.get("evidence_links", [])
        }
        incomplete = sorted(
            experience_id
            for experience_id in referenced_experience_ids
            if not metadata_is_complete(experience_by_id[experience_id])
        )
        if incomplete:
            fail(
                "CV handoff blocked by incomplete experience metadata: "
                + ", ".join(incomplete)
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff", action="store_true", help="require CV-ready experience metadata")
    parser.add_argument("path", type=Path, help="path to evidence-map.json")
    args = parser.parse_args()
    path = args.path
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            fail("top-level JSON value must be an object")
        validate(data, handoff=args.handoff)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    if args.handoff:
        print("PASS: evidence map is valid and CV handoff metadata is complete")
    else:
        print("PASS: evidence map cross-references are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
