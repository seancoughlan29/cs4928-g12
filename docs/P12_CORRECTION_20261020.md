# P12 method correction — 20 October 2026

Status: correction prepared before experimental inference, according to Dylan's
confirmation in this conversation on 20 October that no batches have been sent.
This is a user report, not an independent inspection of every team account.
Course checkpoint/acceptance remains unconfirmed.

## What changed and why

P12 explicitly assigns a fixed LLM prompt on 50 labelled comments, class-wise
errors, and ten detected-smell repair attempts validated against current code.
The RF plan is preserved at M1_PLAN (54880a2294321635a1eaf834cc5877a3ca90786c).
It investigates the supplied earlier detection artefact; it does not, on its
own, carry out P12's stated LLM task.

The 17 October amendment remains an unchanged historical proposal. This dated
correction supersedes its baseline success interpretation and readiness advice.
The input sample, labels, prompt text, five batch files and selection order do
not change. No results motivated resampling or prompt tuning.

## Chronology and evidence

| Date | Event | Evidence and limits |
|---|---|---|
| 6 October | Original RF M1 recorded | M1_PLAN tag at 54880a2; this is still the historical M1 |
| 17 October | LLM amendment and input freeze prepared | docs/P12_SCOPE_AMENDMENT.md; data/p12_v1/freeze.json; preparation commit 62336bc |
| 19 October | Prepared files uploaded to GitHub | ea984e0 and 1c14b4c |
| 19 October | Dylan reported updating the tracker | This report did not establish that every required cell was updated |
| 20 October | Uploaded tracker independently checked | C16/D16/F16/G16 contain the new route; H16 retains the RF prediction; J16 is blank |
| 20 October | Dylan explicitly confirmed no batches sent | Direct answer to the batch-status question in this conversation |
| 20 October | Interpretation and instructions corrected | This document and config/p12_reporting_20261020.json |

No proposal date is treated as a coordinator approval, workbook save time,
experiment date or completed milestone. Do not backdate the remaining entries.

## Course rules applied

- P12, "Your bounded starting task": 50 labelled comments, a fixed LLM prompt,
  class-wise errors, ten repair attempts against current code.
- P12, "Week 5", items 1–3: identify the original section/result; record exact
  IDs; freeze the method, expected result and non-reproduction condition.
- Lab 3, sections 1–2 and 7–8: assigned RQs/source anchor, M1 checkpoint and
  preserved, explained deviations. Lab 3 says to copy assigned RQs exactly;
  P12 also permits refinement. Keep the exact pack questions alongside the
  operational questions and take both to the checkpoint.
- Lab 4, sections 3–6: record material deviations before the new run, preserve
  failures, and compare with the original claim after valid execution.
- Project Brief, sections 2, 4 and FAQ: bounded reproduction plus design work;
  necessary RQ changes remain traceable; negative results can be valid evidence.

These rules support a dated correction; they do not say that every ordinary
deviation needs a separate written permission. The required coordinator
checkpoint and exact M2 interpretation still need an accurate record.

## Assigned and operational RQs

Exact pack RQ1: How accurately can a current LLM detect selected inline comment smells?
Exact pack RQ2: How does software evolution change error rates?

Operational RQ1: How accurately does one current LLM, using a fixed prompt,
classify the first 50 eligible labelled Java comment occurrences in the supplied
dataset, and what class-wise errors occur?

Operational RQ2: For the first ten model-flagged inline comments, which
option—no change, comment-only repair or code refactoring—is justified by comment
correctness, code clarity and preservation of behaviour, and how does a later
code revision affect detection errors and repair decisions?

The coordinator should see these as explicit refinements, not be told they are
verbatim pack wording. No third RQ or extra model comparison has been added.

## Source anchor and proposed bounded analysis

Assigned paper: Caglar et al., DOI 10.1109/ASE63991.2025.00088.
Use sections III-D and III-E for detection input/output and metric procedure;
use IV RQ1 and Table II for the class-wise error comparison. Table IV supplies
model/prompt-specific repeated-run metrics.

The proposed bounded work repeats the code-comment-to-label evaluation workflow
on the pack's first 50 eligible items. It estimates this model's agreement with
the supplied labels. It is a changed-model, changed-sample methodological
replication, not numerical equivalence to a published configuration.

The older supplied Figshare dataset is a course-provided source, but it is not
the later cleaned 2,211-instance repair dataset. The exact ASE prompt templates
were not obtained. Our adapted prompt must remain labelled as adapted. The ASE
package link returned 403 in the available retrieval route; this does not prove
that nobody can access it. Do not use access failure to invent missing contents.

## Reporting correction

Keep accuracy, multiclass MCC, class-wise precision/recall/F1/support, confusion
matrices and exact error cases. Retain both ten-label macro F1 and supported-
class macro F1, clearly distinguished. Zero-support recall is not estimable;
the numerical zero convention must not be mistaken for a measured failure.

The always-Not-a-smell and constant sample-majority baselines are descriptive
sanity checks only. The latter chooses the most common reference label in the
frozen sample before model inference; it is not a trained or out-of-sample
classifier. Neither baseline comparison produces REPRODUCED or SUPPORTED.

Published reference tables are shown beside the observed metrics, with source,
model, prompt, run aggregation and sample differences. Table II is a selected
best o3-mini few-shot output (macro F1 0.47); Table IV's o3-mini few-shot median
macro F1 is 0.41. Do not combine best-run and median results. Zero-shot reference
rows are context for our adapted zero-shot prompt, not matched comparators.

There is currently no defensible agreed numerical reproduction tolerance for
Opus on this 50-item, single-file sample. Do not replace the retired baseline
rule with an invented tolerance, a convenient class ranking or a result-driven
target. The checkpoint question is whether the explicit descriptive comparison
satisfies the bounded M2 task, or which specific published claim/configuration
and decision rule staff require.

Until that is resolved:
- Report real progress and, if collected, descriptive results honestly.
- Mark numerical equivalence INCONCLUSIVE_DIFFERENT_DATA_MODEL_SCOPE.
- Record course M2 interpretation as AWAITING_CHECKPOINT, not REPRODUCED.
- Do not treat a successful scorer or input freeze as milestone completion.

If staff specify a different material comparison, record it before inference.
Keep any initial outputs if execution has already occurred. Do not relabel
post-output changes as preregistered or silently restart.

## Repetitions and limits

Five batches of ten constitute ONE pass over fifty comments. The paper's five
repetitions classify every item five times. This bounded route does not estimate
model run-to-run variability. A single-file, stable-order sample is clustered,
not a random representative sample of Java comments. No population-level
significance or generalisation claim is made. Do not resample to fix imbalance.

## Expected result, recorded before inference

Prediction, not a finding: class-wise performance will be uneven. The LLM may
make both false-positive and false-negative smell decisions. Most justified
interventions are expected to require comment-only changes; refactoring will be
considered only when code evidence identifies a design problem. No numerical
match, refactoring quota or direction of evolution effect is assumed.
The original RF expectation remains in M1_PLAN and the unchanged 17 October
record preserves the initial LLM baseline prediction.

## Ten repair attempts and evolution

Start the ten-case review immediately after valid detection selects the first
ten flagged cases. Do not assume it can all wait for M4. Ask the coordinator
which repair evidence is required at M2 versus the later design milestone.

Retain false positives as justified no-change decisions and document any
shortfall. A case review is not automatically a completed repair. Current-source
mapping, an actual proposal or a justified no-change decision, code inspection
and proportionate before/after verification are required for each claim.

The historical Java path was absent at the 17 October pinned revision. Locate
actual equivalents/history; do not infer deletion from a 404. A Kotlin successor
requires a documented mapping and feasible verification; "Java preferred" is
not an invented absolute prohibition. Keep unresolved cases visible and use the
module contingency if needed. Do not substitute easy cases after predictions.

For evolution, freeze the later revision, correspondence rule, labels/reviewer,
prompt/model settings and paired denominator before the evolution inference.
Report unmatched/removed cases separately. No held-out/Event material is used.

## What remains before the first batch

1. Upload this correction and its code, and record the resulting real commit.
2. Update only G12's G16/H16/I16/J16 using docs/TRACKER_UPDATE_20261020.txt.
3. Record the actual team/checkpoint response and the agreed comparison rule.
4. Record actual model/settings and current timestamps in the new run log.
5. Use the unchanged first batch; preserve its first response for a format check.

Prepared work is not an assertion that any of these human actions occurred.
