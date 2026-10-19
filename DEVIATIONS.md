# Deviations from the original artefact

| # | Date | Deviation | Reason | Evidence |
|---|------|-----------|--------|----------|
| D1 | 2026-10-06 | Environment rebuilt: Python 3.10; removed `pywin32` and `sklearn==0.0` from requirements; added `imbalanced-learn`, `pandas`, `seaborn`, `matplotlib` | `pywin32` is Windows-only; `sklearn==0.0` is a deprecated package that errors on install; notebook imports packages not listed | `original_artefact/requirements.txt` vs `requirements.txt` |

## Additions recorded on 15 October 2026

The D1 entry above was supplied in the uploaded repository. Its earlier date and
execution history have not been independently verified or backdated here.

| ID | Change or clarification | Scope and reason | Evidence/status |
|---|---|---|---|
| D2 | Separate minimal runner environment, Python 3.10.22 | Preserve supplied core versions; pin joblib and threadpoolctl to the original artefact's versions; omit unneeded Jupyter from this CLI route | `requirements-reproduction.txt`, `requirements-tested-linux.txt`, feasibility metadata |
| D3 | Explicit RF seeds 42-51; fixed split/CV/SMOTE seeds | Make the repository's ten-seed statement executable; original RF randomness is unspecified | Proposed in `config/rq1_protocol.json`; full run pending agreement |
| D4 | Paper-informed interpretation is a separate arm | Deduplication, stop words, stratification, SMOTE use and held-out evaluation differ from the recorded loop; no single-cause attribution | `docs/METHOD_AUDIT.md`, `docs/M1_CLARIFICATIONS.md` |
| D5 | Tracker/repository scope conflict preserved | Avoid silently replacing 50/10 cases with 2,189/20 cases | Pending group/coordinator clarification; original M1 unchanged |

## P12 correction recorded on 17 October 2026

| ID | Change or clarification | Reason and evidence |
|---|---|---|
| D6 | Main task amended from RF/20 separate-project cases to LLM/50 detection/10 repair attempts | Supplied P12 pack; docs/P12_SCOPE_AMENDMENT.md. Prior M1 and verified tag unchanged. Record real agreement before inference. |
| D7 | Located occurrences in supplied dataset.json | Augmented file lacks locations. First 50 eligible Java occurrences in declared source order, including repeated text at distinct locations. Different from later cleaned ASE dataset. |
| D8 | One current model, one adapted prompt, five batches of ten, one run | Bounded manual route with raw responses; differs from multi-model, multi-run paper and one-case requests. No numerical-equivalence claim. Model pending. |
| D9 | Fixed local source window | 20 lines before/30 after; context uncertainty recorded. Historical full source retained for audit. |
| D10 | Current-source mapping unresolved | Historical Preferences.java absent at checked head; Kotlin preferences directory observed. No silent sample/project substitution. |

D5 is resolved at the level of the assignment's instructions. The amended
method still needs a real team/workbook checkpoint record. D3/D4 are retained
RF proposals, now supplementary rather than the P12 main experiment.
