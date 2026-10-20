#!/usr/bin/env python3
"""Prepare label-free P12 packets and score saved responses. No model calls."""
import argparse
import collections
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from datetime import datetime, timezone
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
INVALID = "INVALID_OUTPUT"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def new_directory(path):
    if path.exists():
        raise ValueError(f"Output already exists; retain it and choose a new directory: {path}")
    path.mkdir(parents=True)


def normalized_comment(value):
    return re.sub(r"\s+", "", value).replace("//", "").replace("/*", "").replace("*/", "").replace("*", "")


def sample_rows(data, protocol):
    """Assign occurrence IDs before filtering; never rank cases using labels."""
    eligible, exclusions, ordinal = [], [], 0
    for project, files in data.items():
        for file_path, value in files.items():
            source = unquote(value["source_code"])
            lines = source.splitlines()
            for index, comment in enumerate(value["comments"]):
                ordinal += 1
                case_id = f"dataset:{ordinal:06d}"
                begin, end = comment["pos_begin"], comment["pos_end"]
                reason = None
                if not file_path.endswith(".java"):
                    reason = "not_java"
                elif not comment["comment"].strip():
                    reason = "empty_comment"
                elif comment["label"] not in protocol["labels"]:
                    reason = "unsupported_label"
                elif not (isinstance(begin, int) and isinstance(end, int) and 1 <= begin <= end <= len(lines)):
                    reason = "invalid_line_range"
                if reason:
                    exclusions.append({"case_id": case_id, "reason": reason})
                    continue
                lo = max(1, begin - protocol["context_before"])
                hi = min(len(lines), end + protocol["context_after"])
                eligible.append({
                    "case_id": case_id, "source_position": ordinal, "project": project,
                    "file_path": file_path, "comment_index_zero_based": index,
                    "line_start": begin, "line_end": end,
                    "comment": comment["comment"], "reference_label": comment["label"],
                    "context_start": lo, "context_end": hi,
                    "code_context": "\n".join(f"{i}: {lines[i-1]}" for i in range(lo, hi+1)),
                    "source_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
                    "comment_matches_lines": normalized_comment(comment["comment"]) in normalized_comment("\n".join(lines[begin-1:end])),
                    "_full_source": source,
                })
    eligible.sort(key=lambda x: (x["case_id"], x["file_path"], x["comment_index_zero_based"]))
    return eligible[:protocol["sample_size"]], eligible, exclusions, ordinal


def prepare(output):
    config = ROOT / "config/p12_llm_protocol.json"
    protocol = json.loads(config.read_text(encoding="utf-8"))
    source = ROOT / protocol["dataset"]
    if digest(source) != protocol["dataset_sha256"]:
        raise ValueError("Dataset differs from the declared source; record a new protocol before sampling")
    data = json.loads(source.read_text(encoding="utf-8"))
    rows, eligible, excluded, total = sample_rows(data, protocol)
    new_directory(output)
    fields = ["case_id", "source_position", "project", "file_path", "comment_index_zero_based", "line_start", "line_end", "context_start", "context_end", "source_sha256", "comment_matches_lines"]
    write_csv(output / "sample_manifest.csv", rows, fields)
    write_csv(output / "reference_only/labels.csv", rows, ["case_id", "reference_label"])
    write_csv(output / "reference_only/exclusions.csv", excluded, ["case_id", "reason"])
    clean = [{k: v for k, v in row.items() if k not in {"reference_label", "_full_source"}} for row in rows]
    dump(output / "model_inputs/cases.json", clean)
    prompt = (ROOT / protocol["prompt"]).read_text(encoding="utf-8")
    batches = []
    for start in range(0, len(clean), protocol["batch_size"]):
        number = start // protocol["batch_size"] + 1
        batch_id = f"batch_{number:02d}"
        cases = [{k: r[k] for k in ("case_id", "project", "file_path", "line_start", "line_end", "comment", "code_context")} for r in clean[start:start+protocol["batch_size"]]]
        target = output / f"model_inputs/{batch_id}.txt"
        target.write_bytes((prompt + json.dumps(cases, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        batches.append({"batch_id": batch_id, "case_ids": [r["case_id"] for r in cases], "response_file": f"{batch_id}.txt"})
    dump(output / "batches.json", batches)
    for row in rows:
        name = f"{row['project']}-{row['source_sha256'][:12]}-{Path(row['file_path']).name}"
        target = output / "reference_only/source_snapshots" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(row["_full_source"].encode("utf-8"))
    dump(output / "reference_only/sample_audit.json", {
        "source_total": total, "eligible_total": len(eligible), "selected_total": len(rows),
        "exclusions": dict(collections.Counter(r["reason"] for r in excluded)),
        "selected_label_counts": dict(collections.Counter(r["reference_label"] for r in rows)),
        "selected_project_counts": dict(collections.Counter(r["project"] for r in rows)),
        "selected_file_counts": dict(collections.Counter(r["file_path"] for r in rows)),
        "selected_repeated_text_occurrences_after_first": len(rows) - len({r["comment"] for r in rows}),
        "selected_comment_line_mismatches": [r["case_id"] for r in rows if not r["comment_matches_lines"]],
        "original_revision": "Not supplied; source snapshots are content-hashed, not claimed to be current code",
    })
    dump(output / "protocol.json", protocol)
    dump(output / "run_record_template.json", {
        "status": "NOT_STARTED", "operator": None, "provider": None, "model": None,
        "interface": None, "temperature": "not_exposed", "seed": "not_exposed",
        "inputs_frozen_at": None, "tracker_recorded_at": None,
        "started_at": None, "completed_at": None,
        "scope_agreement_reference": None,
        "interpretation_plan_reference": None,
        "interpretation_plan_recorded_at": None,
        "checkpoint_status": None,
        "independent_fresh_conversations": None,
        "reference_labels_withheld": None,
        "batches": [{**b, "started_at": None, "completed_at": None, "model": None, "attempts": 0} for b in batches],
        "deviations": [],
    })
    generated_hashes = {str(p.relative_to(output)).replace("\\", "/"): digest(p) for p in sorted(output.rglob("*")) if p.is_file()}
    dump(output / "freeze.json", {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "INPUTS_PREPARED_NOT_A_COORDINATOR_APPROVAL_OR_MODEL_RUN",
        "dataset_sha256": digest(source), "protocol_sha256": digest(config),
        "prompt_sha256": digest(ROOT / protocol["prompt"]), "preparation_script_sha256": digest(__file__),
        "generated_files": generated_hashes,
    })
    print(f"Prepared {len(rows)} cases in {len(batches)} packets. No model was called.")


def parse_response(path):
    text = path.read_text(encoding="utf-8-sig").strip()
    if text.startswith("```json\n") and text.endswith("```"):
        text = text[8:-3].strip()
    value = json.loads(text)
    if not isinstance(value, list):
        raise ValueError(f"Expected JSON array in {path}")
    return value


def metrics(truth, predicted, labels):
    if not truth or len(truth) != len(predicted):
        raise ValueError("Metrics require nonempty aligned vectors")
    matrix_labels = list(labels) + ([INVALID] if INVALID in predicted else [])
    matrix = {a: {b: 0 for b in matrix_labels} for a in matrix_labels}
    for actual, prediction in zip(truth, predicted):
        matrix[actual][prediction] += 1
    n = len(truth)
    true_count = collections.Counter(truth)
    pred_count = collections.Counter(predicted)
    correct = sum(a == b for a, b in zip(truth, predicted))
    per_class = []
    for label in labels:
        tp = matrix[label][label]
        fp, fn = pred_count[label] - tp, true_count[label] - tp
        precision = tp / (tp+fp) if tp+fp else 0.0
        recall = tp / (tp+fn) if tp+fn else 0.0
        f1 = 2*tp / (2*tp+fp+fn) if 2*tp+fp+fn else 0.0
        per_class.append({"label": label, "support": true_count[label], "tp": tp, "fp": fp, "fn": fn, "precision": precision, "recall": recall, "f1": f1, "interpretation": "supported" if true_count[label] else "no ground-truth examples; recall is not estimable"})
    denominator = math.sqrt((n*n-sum(v*v for v in pred_count.values())) * (n*n-sum(v*v for v in true_count.values())))
    mcc = (correct*n-sum(true_count[k]*pred_count[k] for k in matrix_labels))/denominator if denominator else 0.0
    supported = [r for r in per_class if r["support"]]
    binary = {a: {b: 0 for b in ["not_smell", "smell", "invalid"]} for a in ["not_smell", "smell"]}
    for a, b in zip(truth, predicted):
        binary["not_smell" if a == "Not a smell" else "smell"]["invalid" if b == INVALID else "not_smell" if b == "Not a smell" else "smell"] += 1
    return {"n": n, "correct": correct, "accuracy": correct/n, "mcc": mcc, "mcc_denominator_zero": denominator == 0, "macro_f1_fixed_labels": sum(r["f1"] for r in per_class)/len(labels), "macro_f1_supported_classes": sum(r["f1"] for r in supported)/len(supported), "per_class": per_class, "matrix_labels": matrix_labels, "confusion_matrix": matrix, "binary_confusion_matrix": binary}


def timestamp(value):
    date = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if date.tzinfo is None:
        raise ValueError("Timestamps must contain a timezone offset")
    return date


def score(prepared, responses, output):
    # The 17 October frozen inputs stay unchanged. This separately versioned
    # reporting correction retires the old constant-baseline success verdict.
    reporting_path = ROOT / "config/p12_reporting_20261020.json"
    reporting = json.loads(reporting_path.read_text(encoding="utf-8"))
    freeze = json.loads((prepared / "freeze.json").read_text(encoding="utf-8"))
    for name, expected in freeze["generated_files"].items():
        if digest(prepared / name) != expected:
            raise ValueError(f"Frozen preparation changed: {name}")
    protocol = json.loads((prepared / "protocol.json").read_text(encoding="utf-8"))
    batches = json.loads((prepared / "batches.json").read_text(encoding="utf-8"))
    record_path = responses / "run_record.json"
    record = json.loads(record_path.read_text(encoding="utf-8"))
    for field in ["operator", "provider", "model", "interface", "scope_agreement_reference", "interpretation_plan_reference", "checkpoint_status"]:
        if not isinstance(record.get(field), str) or not record[field].strip():
            raise ValueError(f"Complete run_record.json truthfully: missing {field}")
    if record.get("status") != "COMPLETED" or record.get("reference_labels_withheld") is not True or record.get("independent_fresh_conversations") is not True:
        raise ValueError("This protocol requires a completed run with labels withheld and fresh conversations; record deviations separately")
    frozen, tracker, start, end = [timestamp(record[k]) for k in ["inputs_frozen_at", "tracker_recorded_at", "started_at", "completed_at"]]
    if not (frozen <= start <= end and tracker <= start):
        raise ValueError("Inputs and tracker entry must precede inference; never backdate records")
    if timestamp(record["interpretation_plan_recorded_at"]) > start:
        raise ValueError("The interpretation plan was recorded after inference; retain the outputs and document a post-output analysis instead of claiming preregistration")
    recorded_batches = record.get("batches", [])
    if len(recorded_batches) != len(batches) or {b["batch_id"] for b in recorded_batches} != {b["batch_id"] for b in batches}:
        raise ValueError("Run record must describe every batch exactly once")
    record_by_id = {b["batch_id"]: b for b in recorded_batches}
    labels = protocol["labels"]
    raw_hashes, all_predictions = {}, {}
    for batch in batches:
        run = record_by_id[batch["batch_id"]]
        if run.get("model") != record["model"] or run.get("attempts") != 1:
            raise ValueError("Model changes/retries need a separately documented amended run; do not silently select outputs")
        if not (start <= timestamp(run["started_at"]) <= timestamp(run["completed_at"]) <= end):
            raise ValueError("Batch timestamps must lie inside the run")
        path = responses / batch["response_file"]
        predictions = parse_response(path)
        if len(predictions) != len(batch["case_ids"]):
            raise ValueError(f"Missing/extra predictions in {path}")
        ids = []
        for prediction in predictions:
            if set(prediction) != {"case_id", "predicted_label", "context_sufficient", "reason"}:
                raise ValueError(f"Unexpected response schema in {path}; preserve the raw response")
            case_id = prediction["case_id"]
            if case_id in all_predictions or case_id not in batch["case_ids"]:
                raise ValueError(f"Duplicate or wrong case ID {case_id}")
            if not isinstance(prediction["predicted_label"], str) or type(prediction["context_sufficient"]) is not bool or not isinstance(prediction["reason"], str):
                raise ValueError(f"Incorrect field types for {case_id}")
            ids.append(case_id)
            all_predictions[case_id] = prediction
        if ids != batch["case_ids"]:
            raise ValueError(f"Case order differs from frozen batch {batch['batch_id']}")
        raw_hashes[batch["response_file"]] = digest(path)
    with (prepared / "reference_only/labels.csv").open(encoding="utf-8", newline="") as stream:
        references = list(csv.DictReader(stream))
    cases = {r["case_id"]: r for r in json.loads((prepared / "model_inputs/cases.json").read_text(encoding="utf-8"))}
    joined = []
    for reference in references:
        raw = all_predictions[reference["case_id"]]
        label = raw["predicted_label"] if raw["predicted_label"] in labels else INVALID
        joined.append({**cases[raw["case_id"]], **reference, **raw, "scored_label": label, "correct": label == reference["reference_label"]})
    truth = [r["reference_label"] for r in joined]
    prediction = [r["scored_label"] for r in joined]
    result = metrics(truth, prediction, labels)
    baseline = metrics(truth, ["Not a smell"] * len(truth), labels)
    counts = collections.Counter(truth)
    majority_label = max(labels, key=lambda label: counts[label])
    majority = metrics(truth, [majority_label] * len(truth), labels)
    invalid_count = prediction.count(INVALID)
    candidates = [r for r in joined if r["scored_label"] not in {"Not a smell", INVALID}][:10]
    new_directory(output)
    columns = ["case_id", "project", "file_path", "line_start", "line_end", "reference_label", "predicted_label", "scored_label", "correct", "context_sufficient", "reason"]
    write_csv(output / "predictions.csv", joined, columns)
    write_csv(output / "errors.csv", [r for r in joined if not r["correct"]], columns)
    write_csv(output / "class_metrics.csv", result["per_class"], list(result["per_class"][0]))
    published_by_label = {r["label"]: r for r in reporting["published_class_metrics"]}
    comparison = []
    for row in result["per_class"]:
        source = published_by_label.get(row["label"])
        if source is None:
            continue
        comparison.append({
            "label": row["label"], "our_support": row["support"],
            "our_precision": row["precision"],
            "our_recall": row["recall"] if row["support"] else "NOT_ESTIMABLE",
            "our_f1_zero_convention": row["f1"],
            "paper_support": source["support"], "paper_precision": source["precision"],
            "paper_recall": source["recall"], "paper_f1": source["f1"],
            "f1_difference_descriptive_only": row["f1"]-source["f1"] if row["support"] else "NOT_ESTIMABLE",
            "source": "Caglar et al. ASE 2025 Table II; selected best o3-mini few-shot run",
            "comparability": "Different sample/model/prompt; no numerical-equivalence conclusion",
        })
    if comparison:
        write_csv(output / "paper_class_comparison.csv", comparison, list(comparison[0]))
    write_csv(output / "published_configuration_references.csv", reporting["published_configurations"], list(reporting["published_configurations"][0]))
    matrix_rows = [{"actual_label": a, **result["confusion_matrix"][a]} for a in result["matrix_labels"]]
    write_csv(output / "confusion_matrix.csv", matrix_rows, ["actual_label"] + result["matrix_labels"])
    repair_fields = ["case_id", "project", "file_path", "line_start", "line_end", "reference_label", "predicted_label", "current_revision", "current_path", "mapping_status", "reviewer", "confirmed_smell", "no_change_option", "comment_only_option", "refactor_option", "chosen_action", "design_pressure", "comment_correctness", "verification_before", "verification_after", "behaviour_preserved", "notes"]
    write_csv(output / "repair_candidates.csv", [{**r, "mapping_status": "UNREVIEWED"} for r in candidates], repair_fields)
    dump(output / "summary.json", {
        "execution_status": "SCORED_SAVED_RESPONSES", "model": record["model"],
        "reporting_version": reporting["version"],
        "response_validity": "INVALID_LABELS_PRESENT" if invalid_count else "ALL_LABELS_VALID",
        "paper_numerical_reproduction": "INCONCLUSIVE_DIFFERENT_DATA_MODEL_SCOPE",
        "course_m2_acceptance": "NOT_DETERMINED_BY_SCORER",
        "checkpoint_status_as_recorded": record["checkpoint_status"],
        "interpretation_plan_reference": record["interpretation_plan_reference"],
        "source_anchors": reporting["source_anchors"],
        "metrics": result, "always_not_a_smell_baseline": baseline,
        "constant_sample_majority_baseline": {"label": majority_label, "metrics": majority},
        "baseline_interpretation": reporting["baseline_policy"],
        "macro_f1_fixed_label_ceiling_on_this_sample": len(counts)/len(labels),
        "published_comparison_note": reporting["published_reference_note"],
        "invalid_outputs": invalid_count, "context_insufficient": sum(not r["context_sufficient"] for r in joined),
        "repair_candidates": [r["case_id"] for r in candidates], "repair_shortfall": 10-len(candidates),
        "repairs_validated": 0, "limitations": ["Single-file stable-order sample", "One model run in batches", "Historical source revision unknown", "Current-source mapping required before repairs", "Zero-support class recall not estimable"],
    })
    dump(output / "provenance.json", {"scored_at": datetime.now(timezone.utc).isoformat(), "freeze_sha256": digest(prepared / "freeze.json"), "run_record_sha256": digest(record_path), "raw_response_sha256": raw_hashes, "scoring_script_sha256": digest(__file__), "reporting_config_sha256": digest(reporting_path), "python": sys.version, "command": sys.argv})
    print(f"Scored {len(joined)} recorded responses; {len(candidates)} repair candidates, none yet validated.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--output", type=Path, required=True)
    p = sub.add_parser("score")
    p.add_argument("--prepared", type=Path, required=True)
    p.add_argument("--responses", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            prepare(args.output)
        else:
            score(args.prepared, args.responses, args.output)
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f"STOP: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
