# P12 scope amendment — 17 October 2026

Status: prepared for team agreement and tracker entry before the main LLM run.
This records a change of direction, not a retrospective rewrite of M1.

## Why the plan changes

The project pack supplied by Dylan explicitly requires **50 labelled inline
comments, a fixed LLM prompt, class-wise errors, and 10 detected-smell repair
attempts checked against current code**. The earlier repository M1 instead
specified Random Forest on 2,189 entries and 20 separate-project comments.
The earlier tracker mixed those RF questions with the 50/10 sample description.

The assistant initially developed the RF route too far. Its audit and one-fold
feasibility run remain supplementary evidence. There is no completed RF M2
result and no LLM result. The original `M1_PLAN.md` is unchanged. On 17 October,
the actual remote `M1_PLAN` tag was verified at
`54880a2294321635a1eaf834cc5877a3ca90786c`.

Dylan reports that the coordinator has read the tracker. This establishes
neither rejection nor explicit approval of this new amendment. Record the actual team/coordinator response; do not invent
an in-person READY check. Lab 3's checkpoint requirement still needs an accurate
status, but preparation can proceed now.

## Proposed two research questions

**RQ1.** How accurately does one current LLM, using a fixed prompt, classify
the first 50 eligible labelled Java comment occurrences in the supplied
dataset, and what class-wise errors occur?

**RQ2.** For the first ten model-flagged cases, which intervention—no change,
comment-only repair or code refactoring—is justified by the code, and how does
a later code revision affect the detection errors and repair decisions?

RQ2 keeps the requested design decision and makes the pack's evolution concern
explicit. The baseline detection unit is one comment occurrence; a repair
decision uses its code context; an evolution comparison uses a traceably
matched occurrence across two revisions. These are different denominators.

## Sample and source decisions made before inference

- Use `original_artefact/dataset.json` from the supplied Figshare package. It
  has 2,448 labelled occurrences, project/file paths and source line ranges.
  The augmented file lacks those location identifiers. This is a deliberate
  source choice, not a claim to use the ASE paper's later 2,211-item dataset.
- The original source provides no case IDs or chronological IDs. Assign
  `dataset:000001` etc to all occurrences in the file's stored
  project/file/comment traversal order, before filtering. Sort by this ID,
  then path, then source comment index. The SHA-256 pins that order. A source
  ordinal is not a fabricated chronological timestamp.
- Eligible means a Java file, nonempty labelled comment in the declared
  ten-label vocabulary, and a valid inclusive line range. Take the first 50.
  Do not balance the sample, drop difficult cases or use model outcomes to
  choose examples. Distinct locations remain distinct occurrences even if
  their comment text repeats.
- This selects `dataset:000001`–`dataset:000050`, all in AnkiDroid
  `/AnkiDroid/src/main/java/com/ichi2/anki/Preferences.java`. The sample includes
  six supported categories. Four categories have no examples; their recall
  cannot be estimated. Single-file clustering seriously limits generalisation.
- Code context is always the target's lines plus 20 lines before and 30 after,
  clipped at file boundaries. The full decoded historical file is retained for
  audit. Window boundaries can hide necessary context; uncertainty is recorded
  without dropping cases. The historical commit is not supplied.

## Fixed detection procedure

The precise settings are in `config/p12_llm_protocol.json`. Use one current
model and the unchanged `prompts/p12_detection_v1.txt`. The practical manual
route is five batches of ten cases, each in a fresh conversation. No reference
labels, repair suggestions, earlier responses or project ZIP go to that model.
Do not use this planning conversation as the experimental session: it has seen
the reference labels. This does not eliminate possible training-data exposure.

Record the exact displayed model/provider/interface and exposed settings before
the first request, together with the input freeze, tracker entry and real scope
agreement. Keep the first complete response to every batch and the actual
timestamps. Do not ask for a better answer after seeing labels. Preserve failed
attempts and document any changed protocol before restarting as a separate run.

One run, batching, the current model, the local context window and the older
provided dataset are bounded deviations. They do not estimate run-to-run
variance or reproduce the paper's complete model comparison.

## Metrics and decision rule

Report accuracy, multiclass MCC, all ten classes' support/precision/recall/F1,
a confusion matrix and the exact error cases. The primary macro F1 averages
the fixed ten labels with zero division set to zero; also report macro F1 over
the classes with ground-truth support. Clearly mark unsupported classes and
explain the difference between the two averages. Report binary smell errors.

Compare against the fixed **always Not a smell** baseline on these same cases.
With all 50 valid outputs and complete provenance, primary macro F1 strictly
above that baseline supports this bounded capability check; at or below does
not. This is a descriptive check, not statistical evidence of generalisation.
An invalid label is counted as an error and makes the check inconclusive;
missing, duplicate or unparseable responses must not disappear from the record.

The full paper's numerical reproduction status remains **inconclusive under
this changed data/model/scope**. Do not use the RF 0.69/0.44 target or relabel a
successful script execution as reproduced research. If the coordinator wants
a numerical tolerance against a matched published configuration, agree that
configuration and rule before inference; do not invent a tolerance afterwards.

Expected result, not an observation: the fixed prompt is expected to beat the
negative baseline on primary macro F1, with uneven class performance. Most
accepted interventions are expected to involve only comments; no refactoring
quota is imposed. Evolution may invalidate labels or remove cases; its
direction of effect is not assumed.

## Repair and evolution procedure

Select the first ten valid predicted smells in frozen order. Retain false
positives and justify no change; do not replace them with convenient examples.
If fewer than ten are flagged, record the shortfall. For each, pin and locate
the current code, compare all three interventions, and retain the proposed
diff, reviewer, code evidence and before/after verification. Preserve useful
warnings and unresolved work unless evidence justifies changing them.

The sampled historical Java path is absent at the current AnkiDroid revision
checked on 17 October; see `docs/CURRENT_CODE_CHECK.md`. Mapping is pending.
Do not patch historical snippets and call that current-code validation. If
mapping or a build fails, keep the failed evidence and use the module's
contingency with the coordinator; do not quietly substitute another project.

For a later revision, independently review the current labels before its model
outputs are examined. Use unchanged prompts/model settings where possible.
Report matched-case error changes and mapping attrition separately. The
released Change Events may add specific constraints; their material has not
been read and their responses cannot be completed in advance.

## Record before starting the model run

Team agreement, date, exact model and settings, tracker sample link, real
checkpoint status, and a commit recording this amendment. Preserve the original
M1 tag. `data/p12_v1/freeze.json` freezes prepared input bytes; it is not a claim
of coordinator approval or completion of a milestone.
