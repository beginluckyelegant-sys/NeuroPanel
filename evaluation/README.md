# Evaluation materials

Evaluation programs have not yet been imported. The release should include:

- The primary model-comparison protocol and experiment/version identifiers.
- Input and output schemas, case identifiers, and split provenance without public patient data.
- Prespecified prompt, budget, repeat, retry, and invalid-output rules.
- Expert adjudication instructions, diagnostic-equivalence rules, and blinded review records where shareable.
- Scoring and aggregation code tied to the manuscript's actual endpoints.
- Paired comparison methods and uncertainty estimates where applicable.
- Separate technical QC (completion, truncation, failures) and clinical scoring.

Do not silently drop failed cases or equate exact string matching with clinical diagnostic correctness. Do not substitute revision-stage experiments for the original study comparisons.
