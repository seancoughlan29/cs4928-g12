"""Read-only source audit. Never executes the supplied notebook or API scripts."""
import argparse
import collections
import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'evidence' / 'source_audit')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    source = ROOT / 'original_artefact'
    data = json.loads((source / 'augmented_dataset.json').read_text(encoding='utf-8'))
    notebook = json.loads((source / 'models.ipynb').read_text(encoding='utf-8'))
    counts = collections.Counter(row['label'] for row in data)
    retained = [(i, row) for i, row in enumerate(data) if counts[row['label']] >= 30]
    seen = set()
    deduplicated = []
    duplicate_ids = []
    for index, row in enumerate(data):
        key = (row['comment'], row['label'])
        if key in seen:
            duplicate_ids.append(f'augmented:{index:06d}')
        else:
            seen.add(key)
            deduplicated.append((index, row))
    dedup_counts = collections.Counter(row['label'] for _, row in deduplicated)
    corrected = [(i, row) for i, row in deduplicated if dedup_counts[row['label']] >= 30]
    saved_text = ''.join(''.join(o.get('text', [])) for o in notebook['cells'][16].get('outputs', []))
    match = re.search(r'Random Forest: \(([^,]+), ([^)]+)\)', saved_text)
    metrics = {'accuracy': float(match[1]), 'mcc': float(match[2])} if match else None
    source_cells = {str(i): ''.join(notebook['cells'][i].get('source', []))
                    for i in [1, 4, 6, 7, 9, 12, 13, 14, 16, 18]}
    audit = {
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'kind': 'static_source_audit_not_a_reproduction',
        'original_file_sha256': {str(p.relative_to(ROOT)): digest(p) for p in sorted(source.rglob('*')) if p.is_file()},
        'preserved_m1_sha256': digest(ROOT / 'M1_PLAN.md'),
        'rows_before_filtering': len(data),
        'class_counts_before_filtering': dict(counts),
        'rows_retained_as_shipped': len(retained),
        'class_counts_retained': dict(collections.Counter(r['label'] for _, r in retained)),
        'duplicate_comment_label_rows_removed': len(duplicate_ids),
        'duplicate_row_ids': duplicate_ids,
        'rows_after_deduplication': len(deduplicated),
        'rows_after_deduplication_and_filtering': len(corrected),
        'first_50_raw_rows_retained_by_class_filter': sum(counts[row['label']] >= 30 for row in data[:50]),
        'stored_notebook_rf_cv_metrics_NOT_NEW_RESULTS': metrics,
        'cell_18_stored_output_count': len(notebook['cells'][18].get('outputs', [])),
        'cell_numbering': 'zero-based indices in the notebook cells array',
        'audited_source_cells': source_cells,
        'limitations': ['Saved output is not independent proof of execution provenance.',
                        'No model was trained by this audit.',
                        'No Event A or Event B material was inspected.']
    }
    (args.output / 'audit.json').write_text(json.dumps(audit, indent=2) + '\n', encoding='utf-8')
    for filename, rows in [('rq1_retained_cases.csv', retained), ('rq1_deduplicated_cases.csv', corrected),
                           ('first_50_raw_cases_for_scope_review.csv', list(enumerate(data[:50])))]:
        with (args.output / filename).open('w', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=['case_id', 'source_index_zero_based', 'label', 'retained_class', 'comment_sha256', 'code_sha256'])
            writer.writeheader()
            for index, row in rows:
                writer.writerow({'case_id': f'augmented:{index:06d}', 'source_index_zero_based': index,
                                 'label': row['label'], 'retained_class': counts[row['label']] >= 30,
                                 'comment_sha256': hashlib.sha256(row['comment'].encode()).hexdigest(),
                                 'code_sha256': hashlib.sha256(row['code'].encode()).hexdigest()})
    print(json.dumps({k: audit[k] for k in ['kind', 'rows_before_filtering', 'rows_retained_as_shipped',
                                           'duplicate_comment_label_rows_removed', 'rows_after_deduplication_and_filtering']}, indent=2))


if __name__ == '__main__':
    main()
