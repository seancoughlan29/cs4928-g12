# Deviations from the original artefact

| # | Date | Deviation | Reason | Evidence |
|---|------|-----------|--------|----------|
| D1 | 2026-10-06 | Environment rebuilt: Python 3.10; removed `pywin32` and `sklearn==0.0` from requirements; added `imbalanced-learn`, `pandas`, `seaborn`, `matplotlib` | `pywin32` is Windows-only; `sklearn==0.0` is a deprecated package that errors on install; notebook imports packages not listed | `original_artefact/requirements.txt` vs `requirements.txt` |
