#!/usr/bin/env python3
"""Package the unchanged P12 prompts and a human log; never include answers."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE_COMMIT = "1c14b4c8848ecb25d4c01aec1dbbf79fae35252d"
PREFIX = "p12-claude-run/"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def from_git(path):
    return subprocess.check_output(
        ["git", "show", f"{SOURCE_COMMIT}:{path}"], cwd=ROOT
    )


def build(output):
    prepared = ROOT / "data/p12_v1"
    frozen_bytes = from_git("data/p12_v1/freeze.json")
    if (prepared / "freeze.json").read_bytes() != frozen_bytes:
        raise ValueError("The input freeze differs from the pinned GitHub commit")
    freeze = json.loads(frozen_bytes)
    batches_bytes = (prepared / "batches.json").read_bytes()
    if digest(batches_bytes) != freeze["generated_files"]["batches.json"]:
        raise ValueError("The frozen batch order has changed")
    batches = json.loads(batches_bytes)
    if len(batches) != 5:
        raise ValueError("Expected exactly five frozen batches")

    members = {
        "READ_ME_FIRST.txt": (ROOT / "docs/operator/READ_ME_FIRST.txt").read_bytes(),
        "RUN_LOG.txt": (ROOT / "docs/operator/RUN_LOG_TEMPLATE.txt").read_bytes(),
    }
    packet_records = []
    all_ids = []
    allowed_fields = {
        "case_id", "project", "file_path", "line_start", "line_end",
        "comment", "code_context",
    }
    for batch in batches:
        name = batch["batch_id"] + ".txt"
        source_name = "model_inputs/" + name
        data = (prepared / source_name).read_bytes()
        if digest(data) != freeze["generated_files"][source_name]:
            raise ValueError(f"Frozen prompt changed: {name}")
        if data != from_git("data/p12_v1/" + source_name):
            raise ValueError(f"Prompt differs from the pinned commit: {name}")
        payload = json.loads(data.decode("utf-8").split(
            "The following JSON is the input data:\n", 1
        )[1])
        if len(payload) != 10 or any(set(row) != allowed_fields for row in payload):
            raise ValueError(f"Unexpected fields or case count in {name}")
        ids = [row["case_id"] for row in payload]
        if ids != batch["case_ids"]:
            raise ValueError(f"Case order differs in {name}")
        all_ids.extend(ids)
        members["prompts/" + name] = data
        packet_records.append({
            "path": "prompts/" + name, "sha256": digest(data),
            "bytes": len(data), "case_ids": ids,
        })
    if len(all_ids) != 50 or len(set(all_ids)) != 50:
        raise ValueError("Expected fifty distinct frozen case IDs")

    manifest = {
        "purpose": "Frozen model inputs and uncompleted human operator log",
        "operator_guide_version": "2026-10-20-method-correction",
        "readiness": "Requires corrected tracker and actual source-comparison/checkpoint record before inference",
        "input_repository": "https://github.com/seancoughlan29/cs4928-g12",
        "input_commit": SOURCE_COMMIT,
        "input_freeze_sha256": digest(frozen_bytes),
        "inputs_frozen_at": freeze["created_at"],
        "preparation_script_sha256": digest(Path(__file__).read_bytes()),
        "readme_sha256": digest(members["READ_ME_FIRST.txt"]),
        "initial_run_log_sha256": digest(members["RUN_LOG.txt"]),
        "planned_provider": "Anthropic",
        "planned_model": "Claude Opus 5.5",
        "model_run_performed_by_pack_builder": False,
        "reference_answers_included": False,
        "packets": packet_records,
    }
    members["manifest.json"] = (
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in members.items():
            archive.writestr(PREFIX + name, data)
        archive.writestr(PREFIX + "responses/", b"")
        archive.writestr(PREFIX + "evidence/", b"")
    print(f"Created {output}")
    print("Verified: 5 unchanged packets, 50 cases, no reference-answer files.")
    print(f"ZIP SHA-256: {digest(output.read_bytes())}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build(args.output)
