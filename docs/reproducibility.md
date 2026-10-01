# Reproducibility guide

## Status

This release supplies documentation and templates. It does not yet support installation, inference, or reproduction of the primary comparisons.

## Establish the study version

Retrieve the original model-loading code, full pipeline, configuration, prompts, dependency records, and historical code version. Identify each artifact as original-trial, revision-comparator, or later reconstruction. Do not infer trial settings from a current deployment.

## Implementation records to collect

- Model and tokenizer identifiers, revisions, checkpoint hashes, precision, adapters, and context limit.
- Agent count, roles, model assignments, call ordering, and all prompts.
- Retrieval corpus/index provenance, embedding model, retrieval limits, thresholds, and test-case exclusion procedure.
- Critic scoring, refinement triggers, maximum rounds, stop rules, and failure behavior.
- Voting weights, diagnosis normalization, tie handling, missing-output policy, and final ranking.
- Per-role generation settings, actual defaults, seeds, retries, and token budgets.
- Calibration score definition, fitting data, fitted parameters, evaluation split, and results, if implemented.

## Reproduction sequence after implementation is supplied

1. Freeze and identify the source, configuration, prompts, and evaluation protocol.
2. Document verified dependencies and hardware requirements from an actual clean-environment run.
3. Verify the synthetic input/output path before using controlled evaluation inputs.
4. Preserve raw model responses and technical failures separately from expert scoring.
5. Run comparisons using their prespecified prompts, budgets, retry rules, and blinded adjudication.
6. Report run completeness, failures, truncation, resource use, and clinical scores separately.
7. Upload final weights and required loading artifacts with checksums; run an end-to-end check against those exact artifacts.
8. Tag a verified release and cite the immutable version in the manuscript.

A documentation check or smoke test does not validate clinical performance. If an essential artifact cannot be shared, describe the restriction and the remaining reproducibility limitation explicitly.
