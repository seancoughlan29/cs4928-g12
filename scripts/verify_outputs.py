"""Independently recompute fold metrics and check case/partition provenance."""
import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, matthews_corrcoef

ROOT = Path(__file__).resolve().parents[1]


def verify(directory):
    meta = json.loads((directory / 'run_metadata.json').read_text())
    if meta.get('status') != 'success':
        raise ValueError('Run did not complete successfully')
    source_path = ROOT / meta['protocol']['dataset']
    if hashlib.sha256(source_path.read_bytes()).hexdigest() != meta['dataset_sha256']:
        raise ValueError('Source data changed')
    source = json.loads(source_path.read_text())
    seed_results = json.loads((directory / 'seed_results.json').read_text())
    feasibility = meta['stage'] == 'feasibility'
    expected_seeds = set(meta['protocol']['model_seeds'][:1] if feasibility else meta['protocol']['model_seeds'])
    expected_cv_folds = {1} if feasibility else set(range(1, meta['protocol']['n_splits'] + 1))
    checked_records = checked_predictions = 0
    for arm, info in seed_results.items():
        with (directory / f'{arm}_split.csv').open(newline='') as f:
            split = {row['case_id']: row for row in csv.DictReader(f)}
        groups = defaultdict(list)
        with (directory / f'{arm}_predictions.csv').open(newline='') as f:
            for row in csv.DictReader(f):
                index = int(row['case_id'].split(':')[1])
                if source[index]['label'] != row['truth']:
                    raise AssertionError('Prediction truth does not match source data')
                if row['arm'] != arm:
                    raise AssertionError('Arm mismatch')
                key = (int(row['seed']), row['partition'], int(row['fold']) if row['fold'] else None)
                groups[key].append(row)
        expected_keys = {(s, 'cv', f) for s in expected_seeds for f in expected_cv_folds}
        if arm == 'paper_informed' and not feasibility:
            expected_keys |= {(s, 'held_out', None) for s in expected_seeds}
        if set(groups) != expected_keys:
            raise AssertionError('Prediction groups are missing, duplicated or unexpected')
        records = [json.loads(line) for line in (directory / f'{arm}_folds.jsonl').read_text().splitlines()]
        record_keys = [(r['seed'], r['partition'], r['fold']) for r in records]
        if set(record_keys) != expected_keys or len(record_keys) != len(expected_keys):
            raise AssertionError('Raw metric records do not cover exactly the intended runs')
        by_seed = defaultdict(list)
        for record in records:
            key = (record['seed'], record['partition'], record['fold'])
            predictions = groups[key]
            observed_ids = [p['case_id'] for p in predictions]
            expected_ids = {case for case, row in split.items() if
                            (record['partition'] == 'held_out' and row['partition'] == 'held_out') or
                            (record['partition'] == 'cv' and row['partition'] == 'train_cv' and row['validation_fold'] == str(record['fold']))}
            if set(observed_ids) != expected_ids or len(observed_ids) != len(expected_ids):
                raise AssertionError('Evaluation IDs do not match their recorded partition')
            truth = [p['truth'] for p in predictions]
            pred = [p['prediction'] for p in predictions]
            assert len(pred) == record['evaluation_rows']
            assert abs(accuracy_score(truth, pred) - record['accuracy']) < 1e-12
            assert abs(matthews_corrcoef(truth, pred) - record['mcc']) < 1e-12
            assert confusion_matrix(truth, pred, labels=record['class_order']).tolist() == record['confusion_matrix']
            if record['partition'] == 'cv':
                by_seed[record['seed']].append(record)
            checked_records += 1
            checked_predictions += len(predictions)
        for run in info['runs']:
            rows = by_seed[run['seed']]
            assert len(rows) == run['completed_cv_folds']
            assert abs(np.mean([r['accuracy'] for r in rows]) - run['cv_accuracy_mean']) < 1e-12
            assert abs(np.mean([r['mcc'] for r in rows]) - run['cv_mcc_mean']) < 1e-12
    return {'status': 'PASS', 'scope': meta['stage'], 'metric_records_recomputed': checked_records,
            'individual_predictions_checked': checked_predictions,
            'reproduction_claim': 'NONE: feasibility only' if feasibility else 'Consult summary.json and approved protocol'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    result = verify(args.directory)
    print(json.dumps(result, indent=2))
    (args.directory / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
