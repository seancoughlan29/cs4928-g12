# G12 tracker update — proposed, not entered

Prepared 17 October 2026. Keep the old RQs in the project history and link
`P12_SCOPE_AMENDMENT.md` so this is a traceable amendment. The coordinator has
seen the earlier tracker according to Dylan; agreement to this change is not
assumed. Do not populate result cells with expectations.

| Tracker item | Proposed entry |
|---|---|
| RQ1 | How accurately does one current LLM, using a fixed prompt, classify the first 50 eligible labelled Java comment occurrences in the supplied dataset, and what class-wise errors occur? |
| RQ2 | For the first ten model-flagged cases, which intervention—no change, comment-only repair or code refactoring—is justified by the code, and how does a later code revision affect the detection errors and repair decisions? |
| Bounded sample | `dataset.json`, SHA-256 `62938c0e53f788f5bdf2e94dd4e5e6e5baa957bea79b4bd1ac7be16926e2a096`; occurrence IDs `dataset:000001`–`dataset:000050`, AnkiDroid `Preferences.java`. Exact locations: `data/p12_v1/sample_manifest.csv`. First ten valid model-flagged smells for repair review; report any shortage. |
| Method and rule | Fixed prompt v1, one recorded current model, five fresh batches of ten; reference labels withheld. Report fixed-ten-label macro F1, accuracy, MCC, class-wise errors and confusion matrix. Compare with always Not a smell; greater macro F1 supports the bounded check, otherwise not. Invalid/incomplete output is inconclusive. No numerical-equivalence claim against the full paper. |
| Expected result | Better primary macro F1 than the fixed negative baseline, uneven class performance; mostly comment-only changes among accepted interventions. These are predictions, not findings. |
| Reproduction result | Not run. Inputs and scoring route prepared; exact model, agreement and pre-run tracker record still required. |
| Evidence | `docs/P12_SCOPE_AMENDMENT.md`, `config/p12_llm_protocol.json`, `data/p12_v1/freeze.json`, `scripts/p12.py`; add actual raw-response and scored-output paths only after execution. |
| Design / verification | Ten-case alternatives and current-code mapping pending. Historical Java path absent at checked current revision; no validated repair or passing Java build claimed. |

Enter the actual repository branch/commit links in the workbook when agreed.
Record the real date of the update before inference; do not backdate it to M1.
