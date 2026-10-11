# NeuroPanel model card

NeuroPanel is the research team’s neurology-domain trained and fine-tuned model, developed from DeepSeek-R1-Distill-Llama-70B according to the authors’ model description. The October 2026 source release provides a reconstructed inference architecture for this model.

## Identity and provenance

| Field | Current record |
| --- | --- |
| System name | NeuroPanel |
| Model distribution name | TriageMaster-70B (research-team supplied) |
| Model homepage | [mengxiangbin/clinic-research-TriageMaster-70B](https://huggingface.co/mengxiangbin/clinic-research-TriageMaster-70B) |
| Inspected Hugging Face revision | `8f14be5698e7bf534a1ed9ab3f0551c92f59b1a5` |
| Model development | Neurology-focused training and fine-tuning by the research team (author-reported) |
| Research task | Neurological diagnostic assistance |
| Base model reported in manuscript | DeepSeek-R1-Distill-Llama-70B |
| Final checkpoint / revision / checksum | Pending verification |
| Final architecture and parameter count | Pending implementation and checkpoint verification |
| Tokenizer / adapters / quantization | Pending verification |
| Trial code version and configuration | Pending verification |
| Fine-tuned weight release | Public model homepage available; inspected revision contains `.gitattributes` and `README.md` only |
| Separate base-model artifacts | Unsloth DeepSeek-R1-Distill-Llama-70B GGUF Q8_0 mirror |

The model-development description above is supplied by the research team. The fine-tuned checkpoint or adapter will be linked to its exact revision and checksums when supplied. The separately prepared Q8_0 files match the upstream Unsloth base-model hashes and are catalogued as base-model artifacts. Compression details, training records, calibration, and capability-retention results are tracked in their respective evidence records.

## Intended use

Research inspection and, once the missing artifacts are supplied, reproduction of the associated model-level comparisons. This repository release is not a clinically validated diagnostic service.

## Inputs and outputs

The available revision-stage comparator prompt requests an English case narrative and three output sections: most likely diagnosis, differential diagnosis, and diagnostic reasoning. The exact original-trial input and output contracts remain to be verified from the implementation. The new reference runner has a separate four-section JSON contract, documented in docs/inference_architecture.md. Synthetic examples validate software mechanics only.

## Development and evaluation evidence

Training provenance, dataset overlap checks, final model selection, environment, calibration, and quantitative results must be linked to their source records when released. No model-performance numbers are reproduced in this card until their scope and version can be established.

## Limitations

A reconstructed executable pipeline and synthetic run instructions are now available. The model/configuration inventory tracks historical artifacts separately from the October 2026 reconstruction. The preserved comparator prompt belongs to its own experiment workflow. Clinical correctness requires the study's expert adjudication process; exact text matching alone does not establish diagnostic equivalence.

## Access and licensing

See [data availability](docs/data_availability.md) and [weight release](weights/README.md). Software and artifact licensing remain to be confirmed by the rights holders.

## Public model repository inspection

On 2026-10-11, the Hugging Face API reported this repository as public and ungated. Its inspected revision contains two metadata files; checkpoint/adapter binaries and inference source files are not listed. The card metadata names `deepseek-ai/DeepSeek-R1` as the base model, while the manuscript identifies `DeepSeek-R1-Distill-Llama-70B`. Resolve this identity difference from the training configuration before publishing loading commands. The generated platform loading snippet is a placeholder, not a verified model-loading procedure. See [source inventory](weights/triagemaster.source.json).
