# CS4928 G12 — P12 Inline Comment Smell Detection and Repair

Start with [START_HERE.md](START_HERE.md). The supplied project pack requires
50 fixed-prompt LLM classifications, class-wise errors, and 10 repair attempts
checked against current code. This branch prepares that work; the actual model
run and repair validation remain pending. Dylan confirmed no batches had been
sent on 20 October. The [20 October correction](docs/P12_CORRECTION_20261020.md)
retires the constant-baseline success rule and records the remaining checkpoint
questions. Use [these next steps](docs/NEXT_STEPS_20261020.md).

The original [M1_PLAN.md](M1_PLAN.md) and `M1_PLAN` tag are preserved.
[The dated scope amendment](docs/P12_SCOPE_AMENDMENT.md) explains the change
from Random Forest to the assigned LLM task. Record agreement and the exact
sample in the tracker before inference; do not overwrite prior expectations.

| Location | Purpose |
|---|---|
| `docs/P12_SCOPE_AMENDMENT.md` | Proposed RQs, sample rule, evaluation, expectations, limitations and repair/evolution decisions |
| `docs/TRACKER_UPDATE_20261020.txt` | Current copy/paste text for G16/H16/I16/J16; not an assertion it has been entered |
| `docs/P12_CORRECTION_20261020.md` | Current interpretation correction, chronology, limits and unresolved checkpoint |
| `config/p12_reporting_20261020.json` | Retires automatic baseline verdict; source-anchored descriptive reference tables |
| `docs/P12_SOURCE_MAP.md` | Assigned paper sections, provided dataset and explicit source differences |
| `config/p12_llm_protocol.json` | Preserved 17 October input protocol; interpretation is superseded by the reporting correction |
| `prompts/` | Fixed detection and repair instructions |
| `data/p12_v1/sample_manifest.csv`, `freeze.json` | Exact prepared cases and input hashes |
| `data/p12_v1/model_inputs/batch_01.txt` through `batch_05.txt` | Only these packets go to the detection model |
| `data/p12_v1/reference_only/` | Ground truth and historical source; withhold from detection |
| `scripts/p12.py` | Prepare packets and score saved responses; no model API calls |
| `tests/test_p12.py` | Sampling, label separation, metric and evidence checks |
| `design/README.md` | Current-code repair and evolution evidence requirements |
| `docs/CURRENT_CODE_CHECK.md` | Historical Java path absent at the pinned current revision; per-case mapping pending |
| `evidence/` | Source audit, actual feasibility evidence and software-test logs |
| `AI_LOG.md`, `DEVIATIONS.md` | Material AI influence and traceable changes |

`original_artefact/` remains byte-for-byte unchanged. The older RF runner,
protocol, method audit and one-fold feasibility output are supplementary work,
not the assigned main reproduction. `docs/archive/` retains the 15 October
starting instructions, which have been superseded by the P12 amendment.

Sequence: amended M1 record → M2 and pre-Event A freeze → Event A → design and
pre-Event B freeze → Event B → final synthesis. Future events, human reviews,
test passes and model results must be recorded when they actually happen.
