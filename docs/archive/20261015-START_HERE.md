# G12 project starting point

Prepared on 15 October 2026 from the uploaded group repository and Figshare ZIP.
The group can now inspect the audit and run the reproducible execution route.
The full reproduction remains pending the M1 checkpoint and scope clarification.

## Completed in this working copy

- Verified that all 11 original artefact files match the uploaded Figshare ZIP.
- Preserved the supplied `M1_PLAN.md` without changing its predictions or scope.
- Recorded stable case IDs, class counts, duplicate IDs and source file hashes.
- Implemented separate recorded-loop and paper-informed RF execution arms.
- Added evidence verification and tests of important methodological boundaries.
- Recorded a feasibility execution on one CV fold per arm. This proves that the
  route executes in the recorded environment; it does not answer RQ1.

Read `docs/METHOD_AUDIT.md` for findings. See `evidence/` for actual machine
outputs. Do not copy the saved authors' metrics into the reproduction-results
column as if they were new results from this project.

## Three points to settle

1. Has the coordinator confirmed M1 READY? The uploaded plan says frozen, but the
   ZIP cannot verify a tag or an in-person checkpoint. Lab 3 requires that check
   before substantial execution. Do not backdate a freeze or claim it happened.
2. Which sample description was agreed? The tracker says 50 detection cases and
   10 repairs; the repository says all 2,189 retained rows for RQ1 and 20 comments
   from Apache Commons Lang for RQ2. Preserve both records and document the
   agreed interpretation before execution. Do not silently rewrite the tracker.
3. Does the GitHub connection have access to the exact group repository? The
   connected account is `dylanwperry04-creator`; the repository lookup returned
   404. This does not establish whether the repository is private, moved or
   outside the connection's access. No push or remote tag was attempted.

RQ2 also needs the precise Apache Commons Lang release/commit and independent
team reviews. Those have not been invented or selected in this copy.

## Run setup checks on Windows

Use **Command Prompt**, opened inside the extracted `cs4928-g12-main` folder.
These commands do not require virtual-environment activation. Python 3.10 is
needed for the recorded setup; first check that `py -3.10 --version` works.

```bat
py -3.10 --version
py -3.10 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-reproduction.txt
.venv\Scripts\python.exe scripts\audit_artefact.py
.venv\Scripts\python.exe -m unittest discover -s tests -v
.venv\Scripts\python.exe scripts\reproduce.py --stage feasibility --output evidence\feasibility-windows
.venv\Scripts\python.exe scripts\verify_outputs.py evidence\feasibility-windows
```

The supplied feasibility output was produced on Linux using Python 3.10.22.
`requirements-tested-linux.txt` records every installed package. The smaller
`requirements-reproduction.txt` pins the relevant packages for a Windows setup;
record the actual installed environment in each run's metadata.

Each execution needs a new output directory. The runner refuses to overwrite
earlier results. Keep failed runs and their `error.txt` rather than deleting
awkward evidence. The original requirements and notebook remain unchanged.

## Execute M2 after the plan is settled

Review and agree `config/rq1_protocol.json` and `docs/M1_CLARIFICATIONS.md`.
Record any adjustment before running. Preserve the old M1 text and make the
chronology visible. Confirm the genuine M1 Git tag and coordinator check in the
real repository; this ZIP does not create either.

```bat
.venv\Scripts\python.exe scripts\reproduce.py --stage full --output raw\rq1-10seeds-01
.venv\Scripts\python.exe scripts\verify_outputs.py raw\rq1-10seeds-01
```

This executes 10 RF seeds with 10 CV folds per arm, plus one held-out evaluation
per seed in the paper-informed arm. It produces predictions, fold metrics,
split manifests, seed summaries, environment/source hashes and a decision
summary. The two arms use different preprocessing and evaluation settings;
their differences do not isolate the effect of SMOTE alone.

Before showing M2, verify the results, write the concise interpretation and
limitations, link the evidence in G12's tracker row, and make the genuine
`M2_REPRO` and `PRE_EVENT_A` tags. Do not claim the script alone completes the
coordinator checkpoint or the submission.

## Dates visible in the supplied screenshots

| Item | Time shown |
|---|---|
| Event A release | 23 October 2026, 12:30 pm |
| M2 deadline | 23 October 2026, 6 pm |
| Event A response deadline | 30 October 2026, 6 pm |
| Event B release | 6 November 2026, 12:30 pm |
| Cross-team review deadline | 6 November 2026, 6 pm |
| Event B response deadline | 13 November 2026, 6 pm |

Freeze the relevant pre-event state before opening the released event. Record
each prediction before executing that event's analysis. No event material was
used to prepare this working copy.
