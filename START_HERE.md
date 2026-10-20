# Start here — P12, corrected 20 October 2026

The assigned task is **50 fixed-prompt LLM classifications and 10 repair
attempts validated against current code**. Dylan confirmed on 20 October that
no batches had been sent. Preparation is available; the M2 comparison rule and
checkpoint record need resolution before the main run.

Follow [the current next steps](docs/NEXT_STEPS_20261020.md). The
[20 October correction](docs/P12_CORRECTION_20261020.md) supersedes the earlier
baseline-success rule and unconditional readiness advice. Use
`docs/TRACKER_UPDATE_20261020.txt` for G16/H16/I16/J16 and
`docs/P12_COORDINATOR_CHECK.md` for the two concrete checkpoint questions.

## What is ready

- A dated scope amendment preserving the original M1 text and Git tag.
- The first 50 eligible Java occurrences, with exact IDs, file/line locations,
  source hashes and a recorded selection rule.
- Five model-input packets without reference labels; one fixed prompt.
- A scorer for saved raw responses, class-wise errors, accuracy, macro F1,
  MCC, confusion matrices and deterministic ten-case repair selection.
- A proposed tracker update, repair/evolution procedure and current-source
  feasibility evidence. Tests check the preparation and scoring boundaries.

## Do these before the main run

1. Review `docs/P12_SCOPE_AMENDMENT.md` and `docs/P12_CORRECTION_20261020.md`
   with your team. The dated amendment changes the RF plan
   to the supplied P12 task. Record the real scope agreement/checkpoint status.
   Your coordinator having read the earlier tracker is recorded accurately.
2. Enter the agreed wording and exact sample link into the workbook using
   `docs/TRACKER_UPDATE_20261020.txt`. Record when you entered it, before inference.
   Record the actual accepted source claim/comparison and checkpoint response.
3. Choose one LLM you can access. Record its exact displayed model name,
   provider and interface. Keep the same model for all five packets. No paid
   API setup is required by the prepared manual route.
4. Fill the corrected operator pack's `RUN_LOG.txt` before starting. It includes
   the new interpretation-plan reference/time and checkpoint fields. We can
   convert the factual log to `run_record.json` after collection; the old frozen
   JSON template alone does not contain the reporting-correction fields.

The input files are already prepared in `data/p12_v1/`. Do not regenerate them
to change case order or improve class balance. The first 50 happen to come
from one historical AnkiDroid file; that limitation is documented.

## Run the five packets

Use an isolated fresh model session for each packet, with no access to this
planning conversation, reference labels, earlier packet responses or project
history. If the chosen interface shares previous-chat context, disable that
for the experiment or choose an isolated route and record the actual setting.

Send the entire contents of `data/p12_v1/model_inputs/batch_01.txt` as one
request. Save the complete first response unchanged as `batch_01.txt` inside
your run directory. Repeat for `batch_02.txt` through `batch_05.txt`, using a
fresh session each time. Record the actual model and start/end time per batch.

**Do not upload the project ZIP or `reference_only/` to the detection model.**
Those contain the reference answers. Do not correct the model's labels or ask
it to try again after scoring. Keep failed/refused/truncated outputs and record
the failure before deciding on any recovery. The expected response is a JSON
array; raw JSON fences are accepted by the scorer without changing labels.

There is no model API connection in this working environment. The assistant
has already inspected the reference labels, so its answers in this planning
conversation would not be a clean experimental run. Bring the five saved
responses back here and we can score them and examine the actual errors.

## Score saved responses

The new P12 route uses Python 3.10+ and the standard library only. It does not
need the old RF packages. On Windows, open Command Prompt in this repository.
For a run stored in `runs\detection-01`, after its metadata is complete:

```bat
py -3 -m unittest discover -s tests -p test_p12.py -v
py -3 scripts\p12.py score --prepared data\p12_v1 --responses runs\detection-01 --output results\detection-01
```

Keep raw responses and the run record. The scorer rejects altered frozen
inputs, missing/duplicate IDs and incomplete provenance. Unknown label strings
are counted as errors. It never declares any repair validated. Each scoring
attempt needs a new output directory; earlier outputs are not overwritten.
It now reports descriptive baselines and source comparisons, with no automatic
SUPPORTED/REPRODUCED verdict. Course acceptance is not determined by the scorer.

To independently rebuild the preparation for comparison, use a NEW directory:

```bat
py -3 scripts\p12.py prepare --output data\p12-rebuilt
```

The sample and prompt bytes are deterministic. The updated run-record template,
script hash and freeze timestamp differ from the 17 October preparation. Keep
the original prepared files for the agreed run; never replace their freeze.

## Repairs and work that remains

Start the ten-case review immediately after detection; confirm how much repair
evidence is due at M2 instead of assuming it all belongs to M4. The scorer
selects up to ten cases into `repair_candidates.csv`. Use
`design/README.md` to compare no change, comment-only repair and refactoring.
The historical `Preferences.java` path is absent from the checked current
AnkiDroid revision; mapping to current code must precede any validated repair.
See `docs/CURRENT_CODE_CHECK.md`. Do not substitute easy cases or claim a build
ran when only a snippet was reviewed.

The labs remain relevant to project checkpoints, feedback and peer review.
Event A/B responses need their actual released material and pre-event records;
they cannot honestly be completed now. No event material has been used here.

| Later item | Time in the supplied screenshots |
|---|---|
| Event A release | 23 October 2026, 12:30 pm |
| M2 deadline | 23 October 2026, 6 pm |
| Event A response | 30 October 2026, 6 pm |
| Event B release / cross-team review deadline | 6 November 2026, 12:30 pm / 6 pm |
| Event B response | 13 November 2026, 6 pm |

Freeze the relevant pre-event state before reading its event. The original
`M1_PLAN` tag exists; the amended plan is separate. No `M2_REPRO`,
`PRE_EVENT_A`, `PRE_EVENT_B` or `FINAL` completion is claimed by this preparation.
