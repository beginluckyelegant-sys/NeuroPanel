# Configurations

- `reference.demo.json`: offline mock demonstration, 2 agents, synthetic frozen vectors, one refinement per agent at most.
- `reference.http.json`: real endpoint adapter example; replace the served model identifier and review settings. Retrieval is disabled until a real bank is supplied.
- `study.template.json`: historical-study inventory; null remains unknown. This template is not runnable.

All runnable reference settings are newly selected examples, not recovered trial values. See [architecture](../docs/inference_architecture.md) for exact semantics.
