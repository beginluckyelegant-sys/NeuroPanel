# Run the reference architecture

Python 3.10+ is required. Runtime uses only the Python standard library. Run the commands below from the repository root; no package installation is required. These commands run the October 2026 reconstructed reference implementation.

## Offline synthetic demonstration

```sh
PYTHONPATH=src python3 -m neuropanel \
  --config configs/reference.demo.json \
  --case examples/reference_case.json \
  --bank examples/reference_bank.json \
  --output outputs/demo-run-001
```

Expected: a result selecting the arbitrary label `candidate a`, eight mock calls, and an unresolved critic flag because the deliberately critical fixture remains critical after the allowed revision. `examples/reference_expected.json` records the expected structured result. No model is called and no diagnosis is validated.

Outputs are `result.json` and `trace.json`. Choose a new output path for each run; existing run directories are never overwritten.

## Connect an existing model server

1. Start or obtain access to an OpenAI-compatible chat-completions endpoint using your independently verified weights and serving configuration. This repository does not install a server or load model weights.
2. Copy `configs/reference.http.json` to a local run configuration. Set `backend.base_url` (ending in `/v1`) and `backend.model` to the exact served identifier. Review roles, decoding limits and critic/voting choices; supplied values are configurable demonstration settings.
3. If authentication is required, set `NEUROPANEL_API_KEY` in your environment. Never store the key in a config or URL. Local HTTP is accepted; remote endpoints require HTTPS. Ensure the selected endpoint is approved for the input data before supplying real cases.
4. Prepare an input JSON object with nonempty `case_id` and `case_text`. For an initial interface test use the synthetic example.
5. Run:

```sh
PYTHONPATH=src python3 -m neuropanel \
  --config configs/reference.http.json \
  --case examples/reference_case.json \
  --output outputs/http-run-001
```

The HTTP example disables retrieval until a real frozen embedding bank is supplied. To enable it, set `retrieval.enabled` to true, provide a nonempty embedding revision, add the matching query vector to the case, and pass a bank JSON array using `--bank`. The synthetic bank is not an acceptable research demonstration bank.

The server must return JSON content matching the supplied prompts and a `finish_reason` of `stop`. If the model instead emits prose, unsupported structure, or a truncated completion, the run fails explicitly and stores the response for inspection. Do not tune a locked evaluation after inspecting case-level outcomes.

## Single-agent control

In a separate copied configuration, set `mode` to `single`. This invokes only the first configured agent and bypasses retrieval, critic/refinement, and voting. Both modes use the same configured endpoint/model, but model identity and resource matching need independent verification. This control uses newly written reference prompts, not the preserved revision comparator prompt.

## Tests

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Tests cover bounded refinement and re-critique, single mode, strict output failure, retrieval exclusions/revision checks, vote deduplication/ties, and the HTTP adapter contract. Passing these tests is software validation with synthetic data, not clinical validation.
