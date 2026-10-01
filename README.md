# NeuroPanel

**Research repository for neurology-domain language-model assistance in physician diagnosis.**

[中文说明](README.zh-CN.md) · [Reproducibility guide](docs/reproducibility.md) · [Model card](MODEL_CARD.md) · [Release checklist](docs/release_checklist.md)

## Overview

NeuroPanel is the research system described in the manuscript *Neurology-domain large language model assistance for physician diagnosis: a randomized controlled trial*. This repository is being assembled to document the study implementation and support reproducibility of the model-level comparisons.

## Current availability

| Component | Status |
| --- | --- |
| Repository documentation and contribution guidance | Available |
| Configuration and weight-manifest templates | Available; unfilled, not executable |
| Revision-stage single-model comparator prompt | Available with provenance |
| Original study pipeline and agent prompts | Pending source-code reconciliation |
| Inference and evaluation programs | Pending |
| Environment lockfile and verified installation commands | Pending implementation |
| Calibration implementation and results | Pending verification |
| Model weights, adapters, and tokenizer artifacts | Deferred to the final release stage |
| Validated reproduction run or stable hosted interface | Not currently available |

**This is a documentation release, not a runnable model release.** No performance claims are established by these repository materials. There are no installation or inference commands yet because the original implementation and dependencies have not been imported and verified.

## Repository map

```text
configs/          Configuration template; unknown fields remain null
prompts/          Available prompt and experiment-specific provenance
src/              Reserved location for the verified study implementation
evaluation/       Evaluation requirements and adjudication boundaries
examples/         Synthetic format example, not a clinical benchmark
weights/          Final-stage artifact manifest and release instructions
docs/             Reproduction, data access, and release documentation
MODEL_CARD.md     Model identity, availability, intended use, and limitations
```

## Getting started

1. Read the [reproducibility guide](docs/reproducibility.md) and [model card](MODEL_CARD.md).
2. Check the [release checklist](docs/release_checklist.md) for outstanding artifacts.
3. Use templates only to collect verified study settings. A `null` value means unknown, not a recommended default.
4. Once the original implementation is added, the README will provide tested setup and execution commands. Weights will be added in the final stage with version identifiers and checksums.

## Version identity

Original-trial materials and revision-stage comparator experiments must remain distinguishable. A base-model comparator is not the complete NeuroPanel intervention. Newly reconstructed code must be labeled as such and must not silently replace the historical study implementation.

## Data and model access

See [data availability](docs/data_availability.md) and [weight release instructions](weights/README.md). Patient-level data and private run logs are not part of this release. No access service or response deadline is promised at this stage.

## Citation and license

Bibliographic metadata will be finalized when the manuscript reference is confirmed; no publication DOI or publication status is asserted here. In the interim, refer to this repository URL and the exact commit you used.

A software license has not yet been selected by the rights holders. Public visibility does not itself grant an open-source license. Third-party model and dependency terms remain applicable.

## Contributions

See [CONTRIBUTING.md](CONTRIBUTING.md). Research software; not validated here for use in patient care.
