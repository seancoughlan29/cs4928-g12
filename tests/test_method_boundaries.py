"""Small checks for the methodological boundaries that could invalidate results."""
import sys
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from reproduce import fit_predict, prepare_rows, summarise, text_for_row
from verify_outputs import verify


class MethodBoundaryTests(unittest.TestCase):
    def test_absent_code_does_not_add_na_token(self):
        self.assertEqual(text_for_row({'comment': 'read input', 'code': 'NA'}), 'read input')
        self.assertEqual(text_for_row({'comment': 'read input', 'code': 'read();'}), 'read input read();')

    def test_dedup_keeps_first_comment_label_identity_and_original_id(self):
        data = [{'comment': 'same', 'code': 'one', 'label': 'A'},
                {'comment': 'same', 'code': 'two', 'label': 'A'},
                {'comment': 'same', 'code': 'three', 'label': 'B'}]
        result = prepare_rows(data, 1, deduplicate=True)
        self.assertEqual([r['case_id'] for r in result], ['augmented:000000', 'augmented:000002'])
        self.assertEqual([r['label'] for r in result], ['A', 'B'])

    def test_evaluation_text_never_enters_training_vocabulary_and_smote_is_distinct(self):
        text = np.array([f'alpha reading token{i}' for i in range(24)] + [f'beta writing token{i}' for i in range(8)])
        y = np.array([0] * 24 + [1] * 8)
        config = {'smote_seed': 11, 'random_forest_n_estimators': 10}
        for corrected in [False, True]:
            pred, info, vect = fit_predict(text, y, np.array(['evaluationexclusiveword']), 42, config, corrected)
            self.assertNotIn('evaluationexclusiveword', vect.vocabulary_)
            self.assertEqual(len(pred), 1)
            self.assertEqual(info['training_rows_before_smote'], 32)
            self.assertEqual(info['training_rows_after_smote'], 48)
            self.assertEqual(info['training_rows_used_by_model'], 48 if corrected else 32)

    def test_incomplete_runs_cannot_be_called_reproduced(self):
        config = {'model_seeds': list(range(10)), 'n_splits': 10}
        with self.assertRaises(ValueError):
            summarise({'as_shipped': {'runs': [{'completed_cv_folds': 1}]}}, config, False)
        self.assertEqual(summarise({}, config, True)['status'], 'FEASIBILITY_ONLY')

    def test_full_cli_and_held_out_evidence_on_synthetic_data(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            data = [{'comment': f'{label} example token{i:03d}', 'code': 'NA', 'label': label}
                    for label in ['Alpha', 'Beta'] for i in range(50)]
            source = folder / 'synthetic.json'
            source.write_text(json.dumps(data), encoding='utf-8')
            config = json.loads((root / 'config/rq1_protocol.json').read_text())
            config.update(status='Synthetic software validation only', dataset=str(source),
                          dataset_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                          model_seeds=[1, 2], n_splits=2, random_forest_n_estimators=5)
            protocol = folder / 'synthetic_protocol.json'
            protocol.write_text(json.dumps(config), encoding='utf-8')
            output = folder / 'output'
            completed = subprocess.run([sys.executable, str(root / 'scripts/reproduce.py'), '--stage', 'full',
                                        '--config', str(protocol), '--output', str(output)],
                                       capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            report = verify(output)
            self.assertEqual(report['metric_records_recomputed'], 10)
            self.assertEqual(report['individual_predictions_checked'], 360)
            # A second invocation must preserve prior raw evidence, not overwrite it.
            repeated = subprocess.run(completed.args, capture_output=True, text=True)
            self.assertNotEqual(repeated.returncode, 0)
            self.assertIn('Output directory is not empty', repeated.stderr)


if __name__ == '__main__':
    unittest.main()
