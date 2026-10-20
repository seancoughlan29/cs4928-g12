CS4928 G12/P12 - Claude Opus 5.5 detection run - corrected 20 October 2026

PRE-RUN CHECKPOINT: this replaces the earlier operator guide. The prompts are
unchanged, but the automatic baseline-success interpretation has been retired.
Dylan confirmed on 20 October that no batches had been sent. Record the corrected
tracker update and the agreed source-comparison/checkpoint decision before the
main run. If that decision is still pending, complete the setup only and return
to the planning chat; do not treat this pack as course approval.

Purpose: collect 50 classifications using the five unchanged prompt files.
No reference answers, scores or repaired examples are included in this pack.
These instructions use Claude's website. No Python installation or API key is
needed to collect the responses. Only the contents of a prompts/batch_XX.txt
file should be pasted into Claude, not this guide or RUN_LOG.txt.

1. EXTRACT AND PREPARE

Extract the ZIP. Inside p12-claude-run you will find:
  prompts/       Five complete requests, with ten comment cases in each.
  responses/     Save Claude's responses here.
  evidence/      Save setup screenshots here.
  RUN_LOG.txt    Fill this in using a text editor, such as Windows Notepad.
  manifest.json  Records the original prompt-file hashes and source revision.

Keep the prompts unchanged. Do not give Claude the project ZIP, repository
link, dataset, reference labels or this planning conversation. Each prompt
already contains all the instructions and code context for that batch.

2. RECORD THE SETUP BEFORE SENDING THE FIRST REQUEST

Open RUN_LOG.txt and fill the setup fields marked TO_FILL. The selected model
is Claude Opus 5.5, provider Anthropic, using Claude's website. Check that this
matches the actual displayed model. Record your own name as the operator.

Open a new Claude chat OUTSIDE any project. Click the ghost icon at the top
right to enter Incognito. Check for the "Incognito chat" label. Select Claude
Opus 5.5. Use the default available thinking/effort setting and record its
exact displayed name before the first request. If the control is not shown,
write not_exposed; do not invent a temperature, seed or thinking setting.
Keep the model and all these settings unchanged for the five batches.

Incognito excludes existing memory, but profile preferences and custom styles
can still apply. Use the default style and no extra personal instructions for
this experiment. Preserve a copy of any personal settings before changing
them so you can restore them afterwards. If you cannot establish this setup,
ask in the planning chat before sending the first batch.

Do not add attachments, project knowledge, web search or connected tools.
The fixed prompt already says not to browse or run tools. If a tool is used
despite that instruction, preserve the response and record what happened.

Save a screenshot showing the model and Incognito label in evidence/. Save
another screenshot of any thinking/effort controls. Record the screenshot
filenames in the log. Set the log's confirmation fields to true only after
checking that they accurately describe your setup.

For a real timestamp on Windows, open Command Prompt and paste this command:

powershell -NoProfile -Command "Get-Date -Format o"

Copy the resulting timestamp, including its timezone offset, into the relevant
log field. Run the command again for each new start/end time; do not reuse an
old timestamp. The command only displays the computer's current date/time.
If using another operating system, record the actual ISO 8601 timestamp with
its timezone offset. Do not backdate any run to the tracker-update date.

The older tracker update was incomplete: H16 still had the RF expectation and
J16 was blank in the uploaded copy inspected on 20 October. Record the actual
time of the corrected G16/H16/I16/J16 entry; do not reuse the 19 October report
as proof that the correction was recorded. Record the real interpretation-plan
reference/time and actual checkpoint response. The historical input-freeze
timestamp remains supplied from the frozen manifest.

3. SEND BATCH 01

Open prompts/batch_01.txt in Notepad or another plain-text editor.
Press Ctrl+A, then Ctrl+C. Paste the ENTIRE text into the empty Claude chat.
Do not add an introduction, extra instructions or examples.

Immediately before clicking Send, obtain a current timestamp and put it in
both [run] started_at and [batch_01] started_at. Save the log.
Click Send once. After submission, set [run] status to IN_PROGRESS and
[batch_01] attempts to 1. Preserve a genuine failure rather than hiding it.

Wait for the response to finish. Obtain a new timestamp and record it in
[batch_01] completed_at. Copy the complete response unchanged. In Notepad,
save it as responses/batch_01.txt, using UTF-8 and "All files" if Save As
offers a file-type choice. Check that it was not saved as batch_01.txt.txt.

Save any refusal, error or truncated response too. Do not fix its JSON,
correct labels, ask for an improved answer, regenerate it, or request repairs.
If Markdown fences or extra text appear, preserve them exactly as returned.
The requested output is a JSON array of ten classification objects.

Copy/save the response BEFORE closing Incognito: closed Incognito chats
cannot be reopened from the chat history.

4. CHECK THE FIRST BATCH, THEN CONTINUE

Send the saved batch_01.txt response, RUN_LOG.txt and setup screenshots back
to the planning chat for a format/provenance check before batches 02-05.
Batch 01 is the first part of the real run; it is not a disposable practice
run. No reference-label feedback or accuracy calculation is needed at this
stage. A valid first response stays in the final analysis.

If a format/execution problem occurs, keep the original output and document
the problem before agreeing any recovery. Do not silently redo the batch.

After the format check, repeat the same steps with a NEW Incognito chat for
each of prompts/batch_02.txt, batch_03.txt, batch_04.txt and batch_05.txt.
Use the same model/settings and paste only that batch's complete text.
Record start/end timestamps and attempts in the corresponding log section.
Save each response in responses/ with the matching batch filename.
Do not supply earlier responses to later conversations.

5. RETURN THE EVIDENCE

When all five responses have been saved, set [run] completed_at to the final
batch's completion time. Set status to COMPLETED only if all five responses
were received and preserved. Record any deviation, including an error,
refusal, retry, tool use, setting change or accidental extra context.

Return RUN_LOG.txt, all five responses and setup screenshots to the planning
chat. A ZIP of the completed p12-claude-run folder is convenient. We will
convert the factual log to run_record.json, check raw responses, calculate
descriptive metrics and identify the first ten valid model-flagged cases.
Five batches are one pass over fifty cases, not five repeated experiments.
Neither a baseline improvement nor a successful script establishes reproduction
of the paper. Begin repair review after detection using actual current-code
mapping, alternatives and verification; do not postpone all repairs to M4 by
assumption. No detection or repair success is claimed in advance.

If stopped early, keep status IN_PROGRESS and report what actually happened.
Missing metadata or invalid output must remain visible, not be invented.

SOURCE NOTES

Frozen inputs: seancoughlan29/cs4928-g12 commit
1c14b4c8848ecb25d4c01aec1dbbf79fae35252d, data/p12_v1/model_inputs/.
The bundled prompt files must match their original hashes in manifest.json.

Claude Incognito guidance, consulted 19 October 2026:
https://support.claude.com/en/articles/12260368-use-incognito-chats
This explains memory isolation, profile preferences and saving before closing.

Claude model information, consulted 19 October 2026:
https://www.anthropic.com/claude/opus

This guide is for the human operator. Do not paste it into the detection chat.
