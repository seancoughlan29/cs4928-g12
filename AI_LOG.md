# AI use log

Only material AI contributions that affected an engineering/research decision.

| # | Date | Tool | What AI suggested | How we verified | Accepted? |
|---|------|------|-------------------|-----------------|-----------|
| A1 | 2026-10-06 | Claude | Audit of `models.ipynb`: cell 16 computes SMOTE but fits on non-resampled data; 20% test split unused; dedup commented out; stop words not removed; requirements.txt not installable on macOS | Sean manually inspected `models.ipynb` cell 16: SMOTE output (`X_train_resampled`) is computed but `model.fit()` uses `X_train_fold_tfidf`. Stored output RF MCC 0.4441 / acc 0.6928 matches the paper's reported values, confirming cell 16 produced the reported results. | Accepted (verified). Remaining points (unused test split, dedup disabled, no stop-word removal, requirements) to be verified during M2 audit. |