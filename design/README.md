# Ten-case repair and evolution evidence

No repair or passing Java test result is claimed yet. Use the first ten valid
model-flagged cases selected by `scripts/p12.py score`, in frozen order. Keep
false positives for a possible no-change decision. If fewer than ten are
flagged, report the shortfall. The earlier 20-case Commons Lang proposal is
superseded by `docs/P12_SCOPE_AMENDMENT.md`.

For each selected case:

1. Pin the current revision and trace the historical comment/method to current
   code. Save the old/new path, exact context and mapping evidence. Mark a
   missing or uncertain mapping honestly; do not invent a replacement.
2. Review whether it is still a smell. Distinguish the dataset label, model
   prediction and human judgement. Record actual reviewer names and reasons;
   the assistant cannot supply independent team-member votes.
3. Compare **no change**, **comment-only repair** and **code refactoring**.
   State the actual design pressure: for example, a misleading name, mixed
   responsibilities or duplicated logic. Apply a module concept where it
   explains the decision. No pattern or refactor is compulsory.
4. Preserve the AI proposal and record accept/modify/reject with evidence.
   A task comment may document unresolved work; a removal policy alone does
   not justify deleting it. Use `prompts/p12_repair_v1.txt` for proposed repairs.
5. For a chosen intervention, keep the exact diff and baseline test/build
   command and log. Re-run the existing relevant/full suite afterwards as
   agreed in the method. Add a targeted behaviour check where a real gap
   exists. Record environment failures as failures, not passing verification.
6. Check the new comment's claims against the code separately from testing.
   Comment-only edits should also be checked for accidental code changes.
   Passing tests provide bounded evidence of behaviour preservation, not proof
   of semantic equivalence or of comment correctness.

The scorer generates `repair_candidates.csv` with all review fields blank.
Complete those fields from real investigation. `case_review_template.csv`
is the earlier empty template retained for history; it is not filled evidence.

For evolution, preserve baseline labels/predictions and locate matched cases
at a later pinned revision. Review current labels before examining new model
outputs. Keep the prompt/model/settings fixed where possible and explicitly
log a model change if unavoidable. Report paired errors as a count and rate
over matched cases, plus how many cases disappeared or could not be mapped.
Do not compare error rates using different silently changing denominators.

The current-source feasibility check found a Kotlin preferences directory
where the historical Java file was expected. See `docs/CURRENT_CODE_CHECK.md`.
An unresolved case contributes evidence about the limitation, not a validated
repair. Use the module contingency if the bounded route cannot be completed.
