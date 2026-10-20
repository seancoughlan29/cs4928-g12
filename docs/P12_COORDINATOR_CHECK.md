# G12/P12 checkpoint request — ready to copy

Subject: G12/P12 — M1 amendment and M2 comparison clarification

Hello,

Our original M1_PLAN records Random Forest reproduction of the supplied
notebook's 0.69 accuracy and 0.44 MCC. We have preserved that plan and tag.

On checking the P12 pack, we found that its bounded task explicitly specifies
a fixed LLM prompt on 50 labelled comments, class-wise errors and ten repair
attempts checked against current code. We prepared an LLM amendment on
17 October and updated part of our tracker on 19 October. We are now recording
the correction transparently. As confirmed on 20 October, no detection batches
have been sent.

Our proposed route uses the first 50 eligible Java occurrences, one current
LLM and one adapted fixed prompt, in five independent batches of ten. This is
one pass over fifty cases, not the paper's five repetitions. We will report
accuracy, MCC, clearly defined macro F1 and class-wise errors, comparing the
findings descriptively with sections III-D/E and Tables II/IV of the assigned
ASE paper. We will not claim numerical equivalence or reproduction merely
because the model beats a constant-label baseline.

Could you confirm:
1. Is this declared bounded replication the intended M2 route? If a categorical
   reproduction verdict is required, which original claim/comparison and
   decision rule should the 50-case, current-model exercise use? Should the
   preserved RF work remain supplementary or also be completed for M2?
2. Which of the ten repair attempts and current-code verification must be in
   M2, and which belongs to the later design milestone? The historical Java
   file is absent at the checked current revision, so case mapping is pending.

Please also confirm the recorded M1/checkpoint status so we can represent it
accurately.

Repository: https://github.com/seancoughlan29/cs4928-g12
Correction: docs/P12_CORRECTION_20261020.md
Original M1 tag: M1_PLAN (54880a2294321635a1eaf834cc5877a3ca90786c)

Thank you,
Dylan Perry
G12 / P12

---
This is a prepared message, not evidence that it was sent or answered.
