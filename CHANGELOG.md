# Changelog

## Model description update — 2026-10-11

- Added the research team’s description of NeuroPanel as a neurology-domain trained and fine-tuned model.
- Separated the fine-tuned checkpoint inventory from the upstream DeepSeek Q8_0 base-model mirror.


## Reconstructed reference inference — 2026-10-11

- Added executable retrieval, agent, critic/refinement, voting, and single-control modules.
- Added HTTP and mock backends, explicit JSON contracts, private run traces, synthetic examples, and tests.
- Added architecture and run documentation, including historical provenance gaps and uncalibrated score semantics.
- Verified the mock software workflow and local HTTP contract; recorded the validation scope and version provenance.

## Documentation preparation — 2026-10-01

- Added English and Chinese repository overviews, model card, and reproducibility guidance.
- Added configuration and weight-manifest templates with explicit unknown fields.
- Preserved the revision-stage comparator prompt with its limited provenance.
- Added synthetic format example and source/evaluation handoff documentation.
- No executable model implementation or model weights released in this update.
