# Release checklist

- [x] Create public repository and documentation overview.
- [x] Add configuration and artifact-manifest templates.
- [x] Add revision comparator prompt with provenance.
- [x] Add a synthetic format-only example without patient data.
- [ ] Identify and import the original study source and code version.
- [ ] Verify the final architecture, model loading, tokenizer, and adapters.
- [ ] Add complete original-trial prompts and per-role inference settings.
- [ ] Verify retrieval, critique, refinement, voting, and failure policies.
- [ ] Add actual calibration evidence or document its absence/limitations.
- [ ] Add primary comparison and clinical adjudication/evaluation code.
- [ ] Pin dependencies and validate installation in a clean environment.
- [ ] Run a verified synthetic example and document input/output contracts.
- [ ] Confirm software and model licenses and restricted-data access wording.
- [ ] Upload final model parameters and required loading artifacts.
- [ ] Fill the artifact manifest and verify published checksums and loading.
- [ ] Validate the end-to-end workflow and record reproduction limitations.
- [ ] Tag a release and align the manuscript with the actual released content.

Documentation completion is separate from implementation, model availability, and successful reproduction.
