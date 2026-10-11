# NeuroPanel model card

## Identity and provenance

| Field | Current record |
| --- | --- |
| System name | NeuroPanel |
| Research task | Neurological diagnostic assistance |
| Base model reported in manuscript | DeepSeek-R1-Distill-Llama-70B |
| Final checkpoint / revision / checksum | Pending verification |
| Final architecture and parameter count | Pending implementation and checkpoint verification |
| Tokenizer / adapters / quantization | Pending verification |
| Trial code version and configuration | Pending verification |
| Weight release | Planned for the final stage; files not yet provided |

The base model name is manuscript-reported provenance, not proof of the identity of a released checkpoint. Compression, training, calibration, and capability-retention claims require supporting implementation and records before inclusion as verified facts.

## Intended use

Research inspection and, once the missing artifacts are supplied, reproduction of the associated model-level comparisons. This repository release is not a clinically validated diagnostic service.

## Inputs and outputs

The available revision-stage comparator prompt requests an English case narrative and three output sections: most likely diagnosis, differential diagnosis, and diagnostic reasoning. The exact original-trial input and output contracts remain to be verified from the implementation. The new reference runner has a separate four-section JSON contract, documented in docs/inference_architecture.md. Synthetic examples validate software mechanics only.

## Development and evaluation evidence

Training provenance, dataset overlap checks, final model selection, environment, calibration, and quantitative results must be linked to their source records when released. No model-performance numbers are reproduced in this card until their scope and version can be established.

## Limitations

A reconstructed executable pipeline and synthetic run instructions are now available. Original-trial pipeline identity, final weights, and historical agent prompts remain unverified. The available comparator prompt cannot reproduce the complete intervention. Clinical correctness requires the study's expert adjudication process; exact text matching alone does not establish diagnostic equivalence.

## Access and licensing

See [data availability](docs/data_availability.md) and [weight release](weights/README.md). Software and artifact licensing remain to be confirmed by the rights holders.
