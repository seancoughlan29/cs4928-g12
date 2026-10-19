# Sources for the bounded P12 work

Checked 15–17 October 2026. The user-supplied project pack controls the task.

| Source | Role and precise anchor |
|---|---|
| Çağlar et al., [assigned ASE paper](https://doi.org/10.1109/ASE63991.2025.00088) | Section III-D: fixed detection/repair prompts; III-E: evaluation; IV RQ1 and Table II: detection and class-wise errors; III-B and IV RQ2: repair. |
| [Author-uploaded full text](https://www.researchgate.net/publication/395359325_Automated_Inline_Comment_Smell_Detection_and_Repair_with_Large_Language_Models) | Readable alternative to the inaccessible DOI landing page during the initial review. |
| [Provided Figshare package 27131295](https://figshare.com/articles/conference_contribution/Towards_Automated_Detection_of_Inline_Code_Comment_Smells/27131295) | Version 2 in the prior access record; the uploaded ZIP's bytes are preserved under `original_artefact/`. Source hash: `evidence/provenance.json`. |
| `original_artefact/dataset.json` | Source locations, code, comment text and labels for the prepared 50 cases. |
| `original_artefact/OpenAI_augmented.py` | Supplied taxonomy and fixed-prompt precedent; not executed. Its GPT-4-era route is distinct from the new experiment. |
| [ASE paper's repair-package link](https://figshare.com/s/b71935b0c12dd3330251) | Footnote 1. Web retrieval failed and a direct request returned HTTP 403 on 15 October. Its exact templates and later repair dataset have not been obtained. |

The assigned ASE study evaluates four LLMs, zero/few-shot configurations and
five repetitions, using accuracy, macro F1 and MCC for detection. Its later
dataset includes reference repairs. Our single-model, single-run 50-case
exercise reproduces a bounded detection workflow, with the changes listed in
`P12_SCOPE_AMENDMENT.md`; it is not that complete experiment.

The supplied package instead accompanies Oztas et al.'s earlier
[detection study](https://arxiv.org/html/2504.18956v1). Its RF notebook remains
useful methodological background. The package title and the assigned paper
title must not be treated as interchangeable.

The new detection prompt is a documented adaptation of the supplied taxonomy,
with JSON output and an explicit context-sufficiency flag. It is not presented
as an exact recovered ASE template. No API key, authors' model output or
reference repair has been invented to fill the access gap.
