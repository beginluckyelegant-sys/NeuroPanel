# NeuroPanel-70B QLoRA run — 2026-11-14

Status: **training_completed_release_pending**. This is a new public-data adaptation run. Clinical validation has not been performed.

## Model and data

Base: `unsloth/DeepSeek-R1-Distill-Llama-70B-bnb-4bit` at `32a33c0af1b24136fc477880e0ab4d7b67e6ddd0`. Trainable output is a LoRA adapter; it requires the specified base model. The previously published Q8_0 mirror is a separate artifact. Base-model license and attribution requirements continue to apply; see the pinned base model card.

The prepared split contains 4268 training and 476 validation examples from MedMCQA and FreedomIntelligence medical-o1 datasets. These include exam-derived reference answers and generated answers, tracked separately in preparation. License-pending MedCaseReasoning cases are excluded. The public source dataset cards declare Apache-2.0. No patient-level study data are published here.

Near-verbatim public questions were grouped before splitting (character TF-IDF cosine >= 0.9). The local 360-case study corpus was checked by normalized exact matching and character similarity >= 0.8; no threshold matches were found. This check does not rule out semantic or cross-language overlap. Training/validation group overlap is zero. See data_preparation.json for hashes, methods and counts.

Sequences exceeding 1,024 tokens are excluded rather than truncating away diagnostic information. Validation loss is measured on 64 deterministically hash-selected retained validation examples (2 for the smoke test); it is a technical check, not diagnostic accuracy. The first smoke run takes two optimizer steps, and its adapter is not used to initialize the formal run.

## Training

NF4 QLoRA, BF16 compute, LoRA rank 8 / alpha 16 / dropout 0.05 on q/k/v/o and gate/up/down projections, batch 1, accumulation 8, learning rate 1e-4, one epoch, gradient checkpointing. See qlora.json and environment.txt for exact settings.

`train.py` uses TRL SFTTrainer with completion-only loss. It expects `configs/qlora.json`, `data/train.jsonl`, `data/validation.jsonl`, and a verified `audit/model_manifest.json` under its parent project directory; place it in `scripts/`. Inputs contain prompt/completion chat arrays. Model loading is local-only. The prepared datasets are stored on the research Spark, with hashes recorded here; they are not bundled in this repository. `prepare_data.py` records the original workspace preparation layout and requires the preceding source download batches and local evaluation manifests. It is a run record, not a standalone source-data downloader.

After dependencies and verified base weights are available: `python scripts/train.py --smoke`, followed by `python scripts/train.py`. The scripts refuse to overwrite a completed adapter directory. Training metrics, model hashes and the adapter release are added after successful completion.

## Artifacts

[Download the completed adapter and verification metadata](https://github.com/beginluckyelegant-sys/NeuroPanel/releases/tag/v0.2.0-qlora-20261114). See metrics.json for measured baseline/final validation loss; this run does not establish clinical effectiveness.
