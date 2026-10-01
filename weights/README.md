# Model artifacts — final release stage

Model parameters will be supplied after the code, prompts, configuration, and evaluation materials have been reconciled. This directory currently contains only a manifest template.

For each required checkpoint shard, adapter, tokenizer, architecture configuration, or custom loading file, record its artifact role, exact filename, byte size, SHA-256 checksum, immutable source revision, download location, and applicable license. State whether the release is a full checkpoint or requires a separately obtained base model.

Choose a distribution mechanism suitable for the final artifact sizes; the manifest may reference externally hosted immutable artifacts. Do not commit large weights into ordinary Git history by default. No destination or completed upload is asserted here.

Before release, verify checksums and loading against the published files, fill the manifest, and record the code commit and configuration used for the end-to-end test. `manifest.template.json` is not a completed manifest.
