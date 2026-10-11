# Model artifacts

NeuroPanel is described by the research team as a neurology-domain trained and fine-tuned model derived from DeepSeek-R1-Distill-Llama-70B. Its checkpoint or adapter location, revision, and hashes will be entered in the manifest when supplied. This directory currently contains a manifest template.

The DeepSeek GGUF Q8_0 artifact inventory records the Unsloth source revision and original-file checksums. If the model is distributed as a LoRA adapter, reproduction requires both the specified base checkpoint and the matching adapter.

For each required checkpoint shard, adapter, tokenizer, architecture configuration, or custom loading file, record its artifact role, exact filename, byte size, SHA-256 checksum, immutable source revision, download location, and applicable license. State whether the release is a full checkpoint or requires a separately obtained base model.

Choose a distribution mechanism suitable for the final artifact sizes; the manifest may reference externally hosted immutable artifacts. Do not commit large weights into ordinary Git history by default. No destination or completed upload is asserted here.

Before release, verify checksums and loading against the published files, fill the manifest, and record the code commit and configuration used for the end-to-end test. `manifest.template.json` is not a completed manifest.


## Artifact inventory

The machine-readable [source inventory](triagemaster.source.json) records the inspected repository revision and available files.
