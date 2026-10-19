"""Bounded RF reproduction, with a separate feasibility mode and auditable outputs."""
import argparse
import csv
import hashlib
import importlib.metadata
import json
import platform
import sys
import traceback
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, matthews_corrcoef
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import LabelEncoder

ROOT = Path(__file__).resolve().parents[1]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_for_row(row):
    # Equivalent to notebook cells 7/9 despite their swapped column names.
    return row['comment'] if row['code'] == 'NA' else row['comment'] + ' ' + row['code']


def prepare_rows(data, threshold, deduplicate=False):
    selected, seen = [], set()
    for index, row in enumerate(data):
        key = (row['comment'], row['label'])
        if deduplicate and key in seen:
            continue
        seen.add(key)
        selected.append({'case_id': f'augmented:{index:06d}', 'text': text_for_row(row), 'label': row['label']})
    counts = Counter(row['label'] for row in selected)
    return [row for row in selected if counts[row['label']] >= threshold]


def fit_predict(train_text, train_y, eval_text, seed, config, corrected):
    """Vectorization and SMOTE see training rows only; evaluation data is untouched."""
    vectorizer = TfidfVectorizer(stop_words='english' if corrected else None)
    train_x = vectorizer.fit_transform(train_text)
    eval_x = vectorizer.transform(eval_text)
    smote = SMOTE(random_state=config['smote_seed'])
    resampled_x, resampled_y = smote.fit_resample(train_x, train_y)
    forest = RandomForestClassifier(n_estimators=config['random_forest_n_estimators'], random_state=seed)
    # Preserve the recorded loop's actual fit inputs in the baseline arm.
    forest.fit(resampled_x if corrected else train_x, resampled_y if corrected else train_y)
    predicted = forest.predict(eval_x)
    details = {'training_rows_before_smote': len(train_y), 'training_rows_after_smote': len(resampled_y),
               'training_rows_used_by_model': len(resampled_y) if corrected else len(train_y),
               'vocabulary_size': len(vectorizer.vocabulary_), 'smote_used_for_fit': corrected}
    return predicted, details, vectorizer


def save_json(path, payload):
    path.write_text(json.dumps(payload, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def run_arm(name, rows, config, seeds, out, feasibility):
    corrected = name == 'paper_informed'
    texts = np.array([r['text'] for r in rows], dtype=object)
    labels = np.array([r['label'] for r in rows])
    ids = np.array([r['case_id'] for r in rows])
    indices = np.arange(len(rows))
    train_idx, test_idx = train_test_split(indices, test_size=config['test_size'], random_state=config['split_seed'],
                                         stratify=labels if corrected else None)
    encoder = LabelEncoder()
    encoder.fit(labels[train_idx] if corrected else labels)
    encoded = encoder.transform(labels)
    cv = StratifiedKFold(n_splits=config['n_splits'], shuffle=True, random_state=config['cv_seed'])
    folds = list(cv.split(texts[train_idx], encoded[train_idx]))
    fold_by_index = {int(train_idx[local]): fold for fold, (_, valid) in enumerate(folds, 1) for local in valid}
    with (out / f'{name}_split.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['case_id', 'label', 'partition', 'validation_fold'])
        train_set = set(train_idx.tolist())
        for index in indices:
            writer.writerow([ids[index], labels[index], 'train_cv' if index in train_set else 'held_out', fold_by_index.get(int(index), '')])
    summaries = []
    with (out / f'{name}_folds.jsonl').open('w', encoding='utf-8') as raw, (out / f'{name}_predictions.csv').open('w', newline='', encoding='utf-8') as predictions:
        writer = csv.writer(predictions)
        writer.writerow(['arm', 'seed', 'partition', 'fold', 'case_id', 'truth', 'prediction'])
        for seed in seeds:
            fold_metrics = []
            for fold, (local_train, local_valid) in enumerate(folds, 1):
                if feasibility and fold > 1:
                    break
                fit_idx, valid_idx = train_idx[local_train], train_idx[local_valid]
                assert not set(fit_idx) & set(valid_idx)
                assert not set(train_idx) & set(test_idx)
                predicted, details, _ = fit_predict(texts[fit_idx], encoded[fit_idx], texts[valid_idx], seed, config, corrected)
                record = {'arm': name, 'seed': seed, 'fold': fold, 'partition': 'cv', 'evaluation_rows': len(valid_idx),
                          'accuracy': float(accuracy_score(encoded[valid_idx], predicted)),
                          'mcc': float(matthews_corrcoef(encoded[valid_idx], predicted)),
                          'class_order': encoder.classes_.tolist(),
                          'confusion_matrix': confusion_matrix(encoded[valid_idx], predicted, labels=np.arange(len(encoder.classes_))).tolist(),
                          **details}
                raw.write(json.dumps(record, allow_nan=False) + '\n'); raw.flush()
                decoded = encoder.inverse_transform(predicted)
                for case, truth, prediction in zip(ids[valid_idx], labels[valid_idx], decoded):
                    writer.writerow([name, seed, 'cv', fold, case, truth, prediction])
                predictions.flush()
                fold_metrics.append(record)
            summary = {'arm': name, 'seed': seed, 'completed_cv_folds': len(fold_metrics),
                       'cv_accuracy_mean': float(np.mean([r['accuracy'] for r in fold_metrics])),
                       'cv_mcc_mean': float(np.mean([r['mcc'] for r in fold_metrics]))}
            if corrected and not feasibility:
                predicted, details, _ = fit_predict(texts[train_idx], encoded[train_idx], texts[test_idx], seed, config, True)
                record = {'arm': name, 'seed': seed, 'fold': None, 'partition': 'held_out', 'evaluation_rows': len(test_idx),
                          'accuracy': float(accuracy_score(encoded[test_idx], predicted)),
                          'mcc': float(matthews_corrcoef(encoded[test_idx], predicted)),
                          'class_order': encoder.classes_.tolist(),
                          'confusion_matrix': confusion_matrix(encoded[test_idx], predicted, labels=np.arange(len(encoder.classes_))).tolist(), **details}
                raw.write(json.dumps(record, allow_nan=False) + '\n'); raw.flush()
                decoded = encoder.inverse_transform(predicted)
                for case, truth, prediction in zip(ids[test_idx], labels[test_idx], decoded):
                    writer.writerow([name, seed, 'held_out', '', case, truth, prediction])
                summary.update(held_out_accuracy=record['accuracy'], held_out_mcc=record['mcc'])
            summaries.append(summary)
            print(f'{name}: seed {seed}, {len(fold_metrics)} CV fold(s) completed', flush=True)
    return {'retained_rows': len(rows), 'training_rows': len(train_idx), 'held_out_rows': len(test_idx), 'runs': summaries}


def summarise(arms, config, feasibility):
    if feasibility:
        return {'status': 'FEASIBILITY_ONLY', 'reason': 'One fold per arm; no reproduction decision is made.'}
    outcome = {}
    for name, arm in arms.items():
        runs = arm['runs']
        complete = len(runs) == len(config['model_seeds']) and all(r['completed_cv_folds'] == config['n_splits'] for r in runs)
        if not complete:
            raise ValueError('Incomplete run cannot receive a reproduction decision')
        metrics = {}
        for key in ['cv_accuracy_mean', 'cv_mcc_mean'] + (['held_out_accuracy', 'held_out_mcc'] if name == 'paper_informed' else []):
            vals = [r[key] for r in runs]
            metrics[key] = {'mean': float(np.mean(vals)), 'sample_sd': float(np.std(vals, ddof=1)), 'min': min(vals), 'max': max(vals)}
        within = lambda value, reference: abs(value - reference) <= config['tolerance'] + 1e-12
        if name == 'as_shipped':
            matches = within(metrics['cv_accuracy_mean']['mean'], config['reference_accuracy']) and within(metrics['cv_mcc_mean']['mean'], config['reference_mcc'])
            decision = 'REPRODUCED' if matches else 'NOT_REPRODUCED'
        else:
            matches = within(metrics['held_out_mcc']['mean'], config['reference_mcc'])
            decision = 'INSIDE_M1_MCC_BAND' if matches else 'OUTSIDE_M1_MCC_BAND'
        outcome[name] = {'metrics': metrics, 'decision': decision}
    return {'status': 'COMPLETED_BOUNDED_RUN', 'arms': outcome,
            'caution': 'Baseline CV and corrected held-out results estimate different quantities. The paper-informed arm is an explicitly documented interpretation, not proof of the authors intended pipeline.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', choices=['feasibility', 'full'], default='feasibility')
    parser.add_argument('--arm', choices=['both', 'as_shipped', 'paper_informed'], default='both')
    parser.add_argument('--config', type=Path, default=ROOT / 'config' / 'rq1_protocol.json')
    parser.add_argument('--output', type=Path, required=True, help='New, empty output directory; previous evidence is never overwritten')
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding='utf-8'))
    data_path = ROOT / config['dataset']
    if sha256(data_path) != config['dataset_sha256']:
        raise ValueError('Input hash differs from the recorded protocol')
    data = json.loads(data_path.read_text(encoding='utf-8'))
    if args.output.exists() and any(args.output.iterdir()):
        raise FileExistsError('Output directory is not empty; preserve it and choose a new directory')
    args.output.mkdir(parents=True, exist_ok=True)
    feasibility = args.stage == 'feasibility'
    metadata = {'started_utc': datetime.now(timezone.utc).isoformat(), 'stage': args.stage,
                'command': sys.argv, 'python': platform.python_version(), 'platform': platform.platform(),
                'packages': {p: importlib.metadata.version(p) for p in ['numpy', 'scipy', 'scikit-learn', 'imbalanced-learn', 'pandas']},
                'dataset_sha256': sha256(data_path), 'script_sha256': sha256(Path(__file__)),
                'protocol_sha256': sha256(args.config), 'protocol': config,
                'milestone_status': 'No coordinator approval or Git tag is inferred by this script.'}
    save_json(args.output / 'run_metadata.json', metadata)
    try:
        arms = {}
        for arm in ['as_shipped', 'paper_informed'] if args.arm == 'both' else [args.arm]:
            rows = prepare_rows(data, config['class_frequency_threshold'], arm == 'paper_informed')
            arms[arm] = run_arm(arm, rows, config, config['model_seeds'][:1] if feasibility else config['model_seeds'], args.output, feasibility)
        save_json(args.output / 'seed_results.json', arms)
        save_json(args.output / 'summary.json', summarise(arms, config, feasibility))
        metadata.update(finished_utc=datetime.now(timezone.utc).isoformat(), status='success')
    except Exception:
        metadata.update(finished_utc=datetime.now(timezone.utc).isoformat(), status='failed')
        (args.output / 'error.txt').write_text(traceback.format_exc(), encoding='utf-8')
        raise
    finally:
        save_json(args.output / 'run_metadata.json', metadata)
    print('Feasibility complete. This is not a reproduction result.' if feasibility else 'Bounded run complete. Inspect summary.json and preserve all raw evidence.')


if __name__ == '__main__':
    main()
