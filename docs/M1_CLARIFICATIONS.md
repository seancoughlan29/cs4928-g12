# M1 execution details requiring agreement

**Historical RF proposal, superseded for the main task by P12_SCOPE_AMENDMENT.md on 17 October 2026.** GitHub access and the original M1 tag have since been verified; see evidence/access-20261017.json.

Date: 15 October 2026. Status: proposed clarification, not a retrospective
replacement of the supplied M1 plan. No full reproduction has been run.

## Existing records

The uploaded repository ZIP comment identifies source commit
`54880a2294321635a1eaf834cc5877a3ca90786c`. This is archive metadata, not an
independent verification of a live remote ref. The source audit preserves the
SHA-256 of the unchanged `M1_PLAN.md`.

The tracker and repository agree on the RQ wording, but differ on sample scope:

| Record | RQ1 material | RQ2 material |
|---|---|---|
| Supplied tracker row | First 50 labelled comments, with dataset/order not fully specified | Select 10 detected smells for repair |
| Repository M1 plan | 2,189 retained entries; Random Forest only | 20 inline comments in Apache Commons Lang, confirmed by at least 2 of 3 members |

The proposed runner implements the repository's more explicit RQ1 design.
Whether that agrees with the recorded M1 checkpoint remains unresolved. The
first 50 raw augmented entries include one excluded minority-class item, so
selecting before versus after filtering also changes the sample. There is a
manifest for reviewing this issue; no 50-case detection result is claimed.

## Source anchor

The assigned DOI, https://doi.org/10.1109/ASE63991.2025.00088, is the ASE paper
on LLM detection and repair by Caglar, Caglar and Tuzun. The linked artefact
belongs to Oztas, Torun and Tuzun's different EASE paper, available at
https://arxiv.org/html/2504.18956v1 and published under
https://doi.org/10.1145/3756681.3756988.

RQ1's 0.69 accuracy and 0.44 MCC targets are anchored to the EASE study's Table 6
and the saved output of notebook cell 16. Retain the assigned ASE paper as a
separate source. Confirm whether the pack deliberately combines these studies;
do not describe them as the same paper or silently change the assignment.

## Proposed bounded operational decisions

- Keep `M1_PLAN.md` and its expectations unchanged. Record agreement, date and
  any necessary deviation here before the full run.
- Use model seeds 42 through 51, declared in advance. Keep the original outer
  split seed 42, CV seed 11 and SMOTE seed 11 fixed in both arms. Changing only
  RF randomness is explicit operationalization of the otherwise unspecified
  ten-seed statement. This does not estimate sensitivity to different splits.
- The original RF has `random_state=None`; set an explicit RF seed in the
  bounded runner. Other classifiers are excluded as the repository M1 requires.
  Therefore this is a method-preserving bounded transcription of the RF path,
  not a byte-for-byte execution of every notebook cell and classifier.
- Baseline: keep duplicates, default TF-IDF, unstratified 80/20 split, stratified
  ten-fold CV on the 80%, and compute SMOTE while fitting on the unresampled
  fold. Keep the unused 20% unused for the baseline decision.
- Paper-informed arm: deduplicate on `(comment, label)`, keeping the first
  occurrence; apply the >=30 class filter after deduplication; remove English
  stop words; stratify the 80/20 split; fit vectorization and SMOTE within each
  training fold; refit on the training partition and evaluate the held-out 20%.
- Use the notebook's effective comment-plus-code text in both arms. The paper
  alternates between descriptions of comment text and the augmented dataset;
  this is a documented interpretation, not a claim that every intended detail
  of the authors' method is uniquely reconstructable.
- Derive accuracy and MCC from the same predictions. Do not run independent
  stochastic fits for each metric as notebook cell 18 does.
- Use unweighted means over CV folds, matching cell 16. For ten seeds report
  arithmetic mean, sample SD (`ddof=1`), minimum and maximum. Do not treat 100
  correlated folds as 100 independent experiments.
- Baseline reproduced: both ten-seed means lie in the inclusive bands
  accuracy [0.66, 0.72] and MCC [0.41, 0.47]. No selection of favourable seeds.
- For the paper-informed arm, the repository plan specifies a corrected MCC
  band. Use held-out mean MCC for that check, and report CV mean MCC separately.
  Saved notebook CV and new held-out evaluation are different estimands; a
  difference alone cannot prove the original empirical claim false.

## Remaining confirmations

- Coordinator M1 READY status and actual Git tag: unconfirmed.
- Agreed RQ1 sample and the role of the tracker's 50 cases: unconfirmed.
- RQ2 case count, exact source revision and team confirmation procedure: pending.
- Full execution of either arm: not started; feasibility outputs are separate.
- No earlier prediction, human review or approval has been invented.
