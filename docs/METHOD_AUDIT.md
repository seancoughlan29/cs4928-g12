# Audit of the supplied comment smell artefact

Date: 15 October 2026. This is a completed static audit of the supplied version,
not a completed reproduction experiment. Cell numbers below are zero-based
indices in the notebook JSON and can be located by their quoted identifiers.

## Evidence and source identity

All 11 files under `original_artefact/` match the uploaded Figshare ZIP byte for
byte. `evidence/source_audit/audit.json` contains their SHA-256 values, source
cell text, counts and saved-output extraction. The original notebook and
datasets have not been edited.

The RF source paper is *Towards Automated Detection of Inline Code Comment
Smells*, Oztas et al., https://arxiv.org/html/2504.18956v1, Sections 3.3-3.5 and
Tables 1, 2 and 6. Published DOI: https://doi.org/10.1145/3756681.3756988.
The research artefact is Figshare article 27131295 version 2:
https://figshare.com/articles/conference_contribution/Towards_Automated_Detection_of_Inline_Code_Comment_Smells/27131295/2.

The assigned ASE DOI describes a separate LLM detection-and-repair study:
https://doi.org/10.1109/ASE63991.2025.00088. An author-uploaded readable copy is
https://www.researchgate.net/publication/395359325_Automated_Inline_Comment_Smell_Detection_and_Repair_with_Large_Language_Models.

## Findings

| Topic | Documented or intended procedure | What this artefact contains | Consequence |
|---|---|---|---|
| Data size | Paper describes 2,211 augmented entries and 2,189 after filtering | JSON has 2,218; filtering at 30 retains 2,189 | Initial counts differ; identify the precise supplied version |
| Deduplication | Section 3.2 describes removal of repeated comment/label pairs | Dedup function and call are commented out in cells 1 and 4 | Eight duplicate rows remain among the retained entries; applying that rule leaves 2,181 retained rows |
| Class universe | Five smell types plus Not a smell | Cell 6 retains Task, Not a smell, Beautification, Obvious, Commented out code and Vague | The six-class target is supported; minority classes are not being evaluated |
| Feature inputs | Section 3.4 describes TF-IDF of comments; other sections refer to augmented material | Cells 1, 7 and 9 effectively concatenate comment text and available code | Record a text-input interpretation; the column names are swapped, but the resulting concatenation is coherent |
| Stop words | Section 3.4 says stop words are removed | `TfidfVectorizer()` in cell 16 has no stop-word setting | An explicit English stop-word choice is a change from the baseline |
| Outer split | Section 3.5 describes an 80/20 division and stratified CV | Cell 12 uses an 80/20 split with seed 42 and no `stratify` argument | The outer split is unstratified; ten-fold CV itself is stratified |
| Fold vectorization | Fit preprocessing on training data | Cell 16 fits TF-IDF on the training fold and transforms validation separately | This part of the original loop already avoids validation-vocabulary leakage |
| SMOTE | Section 3.5 describes fitting models on oversampled training folds | Cell 16 computes `X_train_resampled`, then fits using `X_train_fold_tfidf` and `y_train_fold` | The recorded-results loop does not use the oversampled values for fitting, despite its log message |
| Held-out evaluation | Section 3.5 describes a final test evaluation | `X_test` and `y_test` are created but never evaluated in the notebook | Saved target scores are CV means on the training partition, not demonstrated held-out performance |
| Alternative pipeline | Oversampling inside a pipeline | Cell 18 contains TF-IDF, SMOTE and the classifier in a pipeline | It would use SMOTE, but has no saved outputs; it must be distinguished from cell 16 |
| Metric pairing | Accuracy and MCC should describe the same predictions | Cell 18 calls `cross_val_score` separately for each metric with stochastic RF | The proposed runner derives both metrics from one set of predictions |
| Randomness | Reproduction requires explicit stochastic controls | Outer split 42 and CV/SMOTE 11 in the recorded loop; RF has no explicit random state | Ten-seed operationalization needs to be recorded before execution |
| Classification report | Overall performance is the target | Cell 16 prints only the last fold's detailed report and matrix | Those details must not be presented as a whole-dataset or held-out report |

The saved cell-16 RF values are accuracy 0.6927564935064935 and MCC
0.44412565794847403. These are **authors' stored outputs**, not newly reproduced
results. Their agreement with the paper does not independently authenticate
how the outputs were generated.

## Interpretation limits

The audit supports a discrepancy between the displayed recorded-loop code and
the SMOTE/held-out procedure described in the paper. It does not establish that
a fresh baseline run will reproduce, or that the alternative will fail.
Deduplication, stop words, split stratification, training data and evaluation
all differ in the paper-informed arm. Its combined change cannot isolate a
causal effect of SMOTE. The full experiment must retain these qualifications.

The source artefact provides snippets, not a newly selected, buildable Java
repair project. Passing Java tests alone would not establish that a comment
is accurate or useful; RQ2 still needs source-context inspection and actual
team judgement.
