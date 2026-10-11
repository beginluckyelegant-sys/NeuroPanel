# NeuroPanel model card

NeuroPanel is the research team’s neurology-domain trained and fine-tuned model, developed from DeepSeek-R1-Distill-Llama-70B according to the authors’ model description. The October 2026 source release provides a reconstructed inference architecture for this model.

## Identity and provenance

| Field | Current record |
| --- | --- |
| System name | NeuroPanel |
| Model development | Neurology-focused training and fine-tuning by the research team (author-reported) |
| Research task | Neurological diagnostic assistance |
| Base model reported in manuscript | DeepSeek-R1-Distill-Llama-70B |
| Final checkpoint / revision / checksum | Pending verification |
| Final architecture and parameter count | Pending implementation and checkpoint verification |
| Tokenizer / adapters / quantization | Pending verification |
| Trial code version and configuration | Pending verification |
| Fine-tuned weight release | Checkpoint or adapter location and artifact identifiers to be supplied |
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
