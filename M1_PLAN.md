# M1_PLAN – G12 / P12: Inline Comment Smell Detection and Repair

Frozen preregistration (Week 5). Do not edit after tagging `M1_PLAN`. If anything changes, add a dated note at the bottom explaining what and why.

Team: Tommy Quinn, Dylan Perry, Sean Coughlan
Paper: "Towards Automated Detection of Inline Code Comment Smells" (EASE 2025, arXiv 2504.18956)
Artefact: figshare 27131295 (unmodified copy in `original_artefact/`)

## RQs

**RQ1:** Can the supplied notebook reproduce its recorded Random Forest accuracy and Matthews correlation coefficient on the six retained comment classes, and does its implementation match the documented preprocessing and evaluation procedure?

**RQ2:** For confirmed inline comment smells in a separate Java project, when is comment only repair sufficient, and when is code refactoring justified compared with making no change, considering comment correctness, code clarity and preservation of behaviour?

## Bounded sample / case IDs

- RQ1: Authors' `augmented_dataset.json` filtered as in `models.ipynb`: 2,189 comments, 6 classes (Not a smell, Obvious, Task, Vague, Beautification, Commented out code). Random Forest only; other classifiers and GPT-4 scripts out of scope. Comparison of the as-shipped pipeline (cell 16) vs the paper-described pipeline.
- RQ2: 20 inline comments from Apache Commons Lang (Java, not in the paper's dataset), flagged by our trained RF and confirmed as smells by at least 2 of 3 team members.

## Method / metric / decision rule

**RQ1**
- (a) Run cell 16 as shipped across 10 seeds; report mean ± SD accuracy and MCC. Reproduced = within ±0.03 of reported 0.69 accuracy / 0.44 MCC; outside = non-reproduction.
- (b) Audit code vs paper: SMOTE use, deduplication, stop-word removal, stratified split, use of the 20% held-out test set.
- (c) Run a corrected pipeline matching the paper's description (dedup, stop words removed, SMOTE inside training folds only, final evaluation on held-out test set) across 10 seeds. Paper's claim holds if corrected MCC is within ±0.03 of 0.44.

**RQ2** – for each confirmed smell choose one:
- (a) No change: comment adds value or is a false positive.
- (b) Comment-only repair: code is clear, only the comment is wrong/noisy.
- (c) Code refactoring (rename / extract method / extract variable): only if the comment compensates for unclear code and the refactor removes the need for it.
- Every change must pass the full existing test suite before and after.

## Expected result (before execution)

- RQ1 (a): As-shipped reproduces within ±0.03.
- RQ1 (b): Initial code reading suggests SMOTE is computed but not used in the reported pipeline (cell 16 fits on non-resampled data), the 20% test split is never evaluated, and deduplication is disabled.
- RQ1 (c): Corrected pipeline will not reproduce: accuracy falls and MCC differs from 0.44 by more than 0.03, direction uncertain.
- RQ2: Most confirmed smells (Obvious, Commented out code, Task) need comment-only repair or deletion; code refactoring justified in a minority (<25%), mainly Vague. All changes preserve behaviour (tests pass).

## What counts as non-reproduction

RF accuracy or MCC outside ±0.03 of reported values (mean over 10 seeds).

## Change log
(empty)
