# What the current evidence establishes

## P12 preparation on 17 October 2026

`access-20261017.json` records repository access, the M1 tag and current-source
feasibility. `../data/p12_v1/` contains cases, label-free packets, withheld labels
and hashes. `p12_tests.txt` records software checks. These establish preparation,
not an LLM result or validated repair. The original M1 remains unchanged.

The evidence below is supplementary RF work retained for chronology.

The source audit and feasibility check were performed on 15 October 2026.

| Evidence | What it establishes | What it does not establish |
|---|---|---|
| `source_audit/audit.json` | Source hashes, retained classes, duplicates, audited code and authors' stored RF values | A fresh reproduction of those values |
| `source_audit/*cases.csv` | Locatable source indices and hashes for the bounded inputs | Agreement that the tracker scope has been changed |
| `method_tests.txt` | Method-boundary checks, including a full CLI test on artificial data | Results on the assigned study |
| `feasibility-20261015/` | One actual CV fold runs for each arm with the recorded package versions | Ten-seed completion, M2 success or coordinator approval |
| `feasibility-20261015/verification.json` | Both raw metric records independently recalculate from 351 saved predictions; case IDs match source labels and recorded partitions | A proof of generalization or the final reproduction conclusion |

The artificial-data software test uses two classes, two seeds and two folds
only to exercise the CLI, held-out output, verifier and overwrite protection.
Its temporary data and outputs are discarded, and its scores are not research
results. The real-data feasibility run remains separate and immutable.

`run_metadata.json` preserves the exact input, code and proposed-protocol
hashes, command, environment and timestamps. `summary.json` intentionally says
`FEASIBILITY_ONLY`; do not relabel it as a completed reproduction.
