"""Synthetic checks for sampling, blinded inputs, metrics and evidence handling."""
import contextlib
import csv
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / "scripts/p12.py"
spec = importlib.util.spec_from_file_location("p12", MODULE)
p12 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p12)


class P12Tests(unittest.TestCase):
    def test_occurrence_ids_precede_filtering_and_keep_duplicate_text(self):
        data = {"p": {"a.py": {"source_code": "# x", "comments": [{"comment": "x", "pos_begin": 1, "pos_end": 1, "label": "Task"}]}, "b.java": {"source_code": "// x\n// x\n// y", "comments": [{"comment": "x", "pos_begin": 1, "pos_end": 1, "label": "Task"}, {"comment": "x", "pos_begin": 2, "pos_end": 2, "label": "Obvious"}, {"comment": "y", "pos_begin": 3, "pos_end": 3, "label": "Task"}]}}}
        protocol = {"labels": ["Task", "Obvious"], "sample_size": 2, "context_before": 1, "context_after": 1}
        selected, eligible, excluded, total = p12.sample_rows(data, protocol)
        self.assertEqual([r["case_id"] for r in selected], ["dataset:000002", "dataset:000003"])
        self.assertEqual([r["reference_label"] for r in selected], ["Task", "Obvious"])
        self.assertEqual((len(eligible), len(excluded), total), (3, 1, 4))

    def test_metrics_known_matrix_including_invalid_output(self):
        result = p12.metrics(["Not a smell", "Obvious", "Task", "Task"], ["Not a smell", "Task", "Task", p12.INVALID], ["Not a smell", "Obvious", "Task"])
        self.assertEqual(result["accuracy"], 0.5)
        self.assertEqual(result["macro_f1_fixed_labels"], 0.5)
        self.assertAlmostEqual(result["mcc"], 0.3)
        self.assertEqual(result["binary_confusion_matrix"]["smell"]["invalid"], 1)

    def test_actual_preparation_is_label_free_and_source_recoverable(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "prepared"
            with contextlib.redirect_stdout(io.StringIO()):
                p12.prepare(output)
            cases = json.loads((output / "model_inputs/cases.json").read_text())
            self.assertEqual(len(cases), 50)
            self.assertTrue(all("reference_label" not in row and "label" not in row for row in cases))
            self.assertEqual(cases[0]["case_id"], "dataset:000001")
            self.assertEqual(cases[-1]["case_id"], "dataset:000050")
            for packet in (output / "model_inputs").glob("batch_*.txt"):
                payload = json.loads(packet.read_text().split("The following JSON is the input data:\n", 1)[1])
                self.assertEqual(len(payload), 10)
                self.assertTrue(all(set(row) == {"case_id", "project", "file_path", "line_start", "line_end", "comment", "code_context"} for row in payload))
            audit = json.loads((output / "reference_only/sample_audit.json").read_text())
            self.assertEqual(audit["selected_comment_line_mismatches"], [])
            with self.assertRaisesRegex(ValueError, "already exists"):
                p12.prepare(output)

    def synthetic_run(self, root):
        prepared, responses = root / "prepared", root / "responses"
        responses.mkdir()
        labels = ["Not a smell", "Obvious", "Task"]
        ids = ["synthetic:1", "synthetic:2"]
        p12.dump(prepared / "protocol.json", {"labels": labels})
        p12.dump(prepared / "batches.json", [{"batch_id": "batch_01", "case_ids": ids, "response_file": "batch_01.txt"}])
        p12.dump(prepared / "model_inputs/cases.json", [{"case_id": x, "project": "SYNTHETIC_TEST", "file_path": "Fake.java", "line_start": i+1, "line_end": i+1} for i, x in enumerate(ids)])
        p12.write_csv(prepared / "reference_only/labels.csv", [{"case_id": ids[0], "reference_label": "Task"}, {"case_id": ids[1], "reference_label": "Not a smell"}], ["case_id", "reference_label"])
        p12.dump(prepared / "freeze.json", {"generated_files": {str(p.relative_to(prepared)): p12.digest(p) for p in prepared.rglob("*") if p.is_file()}})
        p12.dump(responses / "run_record.json", {"status": "COMPLETED", "operator": "SYNTHETIC_TEST", "provider": "SYNTHETIC_TEST", "model": "NO_REAL_MODEL", "interface": "fixture", "scope_agreement_reference": "test fixture only", "reference_labels_withheld": True, "independent_fresh_conversations": True, "inputs_frozen_at": "2000-01-01T00:00:00Z", "tracker_recorded_at": "2000-01-01T00:00:00Z", "started_at": "2000-01-01T01:00:00Z", "completed_at": "2000-01-01T02:00:00Z", "batches": [{"batch_id": "batch_01", "model": "NO_REAL_MODEL", "attempts": 1, "started_at": "2000-01-01T01:00:00Z", "completed_at": "2000-01-01T02:00:00Z"}]})
        p12.dump(responses / "batch_01.txt", [{"case_id": ids[0], "predicted_label": "Task", "context_sufficient": True, "reason": "Synthetic test."}, {"case_id": ids[1], "predicted_label": "unsupported string", "context_sufficient": False, "reason": "Synthetic invalid-output test."}])
        record = json.loads((responses / "run_record.json").read_text())
        record.update({"interpretation_plan_reference": "SYNTHETIC fixture; not a course decision", "interpretation_plan_recorded_at": "2000-01-01T00:00:00Z", "checkpoint_status": "SYNTHETIC_TEST_ONLY"})
        p12.dump(responses / "run_record.json", record)
        return prepared, responses

    def test_saved_response_scoring_and_no_repair_success_claim(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepared, responses = self.synthetic_run(root)
            with contextlib.redirect_stdout(io.StringIO()):
                p12.score(prepared, responses, root / "result")
            summary = json.loads((root / "result/summary.json").read_text())
            self.assertEqual(summary["invalid_outputs"], 1)
            self.assertEqual(summary["response_validity"], "INVALID_LABELS_PRESENT")
            self.assertNotIn("bounded_capability_check", summary)
            self.assertEqual(summary["repair_candidates"], ["synthetic:1"])
            self.assertEqual(summary["repairs_validated"], 0)
            self.assertEqual(summary["repair_shortfall"], 9)
            (prepared / "reference_only/labels.csv").write_text("tampered")
            with self.assertRaisesRegex(ValueError, "Frozen preparation changed"):
                p12.score(prepared, responses, root / "result2")

    def test_perfect_scores_do_not_claim_replication_and_post_output_plan_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepared, responses = self.synthetic_run(root)
            raw = json.loads((responses / "batch_01.txt").read_text())
            raw[1]["predicted_label"] = "Not a smell"
            p12.dump(responses / "batch_01.txt", raw)
            with contextlib.redirect_stdout(io.StringIO()):
                p12.score(prepared, responses, root / "result")
            summary = json.loads((root / "result/summary.json").read_text())
            self.assertEqual(summary["metrics"]["accuracy"], 1.0)
            self.assertNotIn("bounded_capability_check", summary)
            self.assertEqual(summary["paper_numerical_reproduction"], "INCONCLUSIVE_DIFFERENT_DATA_MODEL_SCOPE")
            self.assertEqual(summary["course_m2_acceptance"], "NOT_DETERMINED_BY_SCORER")
            with (root / "result/paper_class_comparison.csv").open() as stream:
                rows = list(csv.DictReader(stream))
            absent = next(r for r in rows if r["label"] == "Obvious")
            self.assertEqual(absent["our_recall"], "NOT_ESTIMABLE")
            record = json.loads((responses / "run_record.json").read_text())
            record["interpretation_plan_recorded_at"] = "2000-01-01T03:00:00Z"
            p12.dump(responses / "run_record.json", record)
            with self.assertRaisesRegex(ValueError, "after inference"):
                p12.score(prepared, responses, root / "late-result")

    def test_duplicate_ids_and_missing_batches_are_not_dropped(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepared, responses = self.synthetic_run(root)
            path = responses / "batch_01.txt"
            raw = json.loads(path.read_text())
            raw[1]["case_id"] = raw[0]["case_id"]
            p12.dump(path, raw)
            with self.assertRaisesRegex(ValueError, "Duplicate or wrong case"):
                p12.score(prepared, responses, root / "result")
            self.assertFalse((root / "result").exists())
            path.unlink()
            with self.assertRaises(FileNotFoundError):
                p12.score(prepared, responses, root / "result")


if __name__ == "__main__":
    unittest.main()
