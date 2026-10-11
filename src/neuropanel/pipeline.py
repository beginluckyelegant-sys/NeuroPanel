"""Auditable reconstruction of the manuscript-level inference architecture."""
import hashlib
import json
import math
import random
import time
from pathlib import Path
from .schema import diagnosis_output, critic_output
from .retrieval import retrieve
from .voting import aggregate


def fingerprint(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def validate_config(c):
    if c.get('provenance') != 'reconstructed_reference_not_original_trial':
        raise ValueError('Reference implementation requires explicit provenance')
    if c.get('mode') not in ('single', 'full'):
        raise ValueError('mode must be single or full')
    if type(c.get('seed')) is not int:
        raise ValueError('An explicit integer seed is required')
    agents = c.get('agents')
    if not isinstance(agents, list) or not agents:
        raise ValueError('At least one agent is required')
    ids = [a['id'] for a in agents]
    if any(not isinstance(i, str) or not i for i in ids) or len(set(ids)) != len(ids):
        raise ValueError('Agent IDs must be unique nonempty strings')
    settings = [a['generation'] for a in agents] + [c['critic']['generation']]
    for a in agents:
        if a['ordering'] not in ('forward', 'reverse') or not isinstance(a['role'], str):
            raise ValueError('Invalid role or candidate consideration order')
    for s in settings:
        if set(s) != {'temperature', 'top_p', 'max_tokens'}:
            raise ValueError('generation requires exactly temperature, top_p, max_tokens')
        if type(s['max_tokens']) is not int or s['max_tokens'] <= 0:
            raise ValueError('max_tokens must be positive')
        for k in ('temperature', 'top_p'):
            if type(s[k]) not in (int, float) or not math.isfinite(s[k]):
                raise ValueError('Nonfinite generation setting')
        if not 0 <= s['temperature'] <= 2 or not 0 < s['top_p'] <= 1:
            raise ValueError('Generation setting outside reference adapter bounds')
    for name in ('top_k',):
        if type(c['voting'][name]) is not int or c['voting'][name] < 1:
            raise ValueError('Voting top_k must be positive')
    weight = c['voting']['soft_weight']
    if type(weight) not in (int, float) or not math.isfinite(weight) or not 0 <= weight <= 1:
        raise ValueError('soft_weight must be in [0, 1]')
    critic = c['critic']
    if type(critic['max_refinements']) is not int or not 0 <= critic['max_refinements'] <= 10:
        raise ValueError('max_refinements must be between 0 and 10')
    w = critic['section_weights']
    if len(w) != 4 or any(type(x) not in (int, float) or not math.isfinite(x) or x < 0 for x in w) or not math.isclose(sum(w), 1):
        raise ValueError('Four nonnegative critic weights must sum to one')
    for name in ('penalty_weight', 'minimum_reward'):
        if type(critic[name]) not in (int, float) or not math.isfinite(critic[name]) or critic[name] < 0:
            raise ValueError('Invalid critic threshold/penalty')
    r = c['retrieval']
    if type(r['enabled']) is not bool or type(r['top_k']) is not int or r['top_k'] < 0:
        raise ValueError('Invalid retrieval configuration')
    if type(r['min_similarity']) not in (int, float) or not -1 <= r['min_similarity'] <= 1:
        raise ValueError('Invalid similarity threshold')
    if type(c['backend']['timeout_seconds']) not in (int, float) or not 0 < c['backend']['timeout_seconds'] <= 3600:
        raise ValueError('Invalid timeout')
    if type(c['backend']['max_retries']) is not int or not 0 <= c['backend']['max_retries'] <= 5:
        raise ValueError('Invalid retry count')


class Pipeline:
    def __init__(self, config, backend, prompt_dir):
        validate_config(config)
        self.c = config
        self.backend = backend
        self.prompts = {name: (Path(prompt_dir) / (name + '.txt')).read_text()
                        for name in ('generate', 'critique', 'refine')}
        self.trace = {'provenance': config['provenance'], 'config': config,
            'config_sha256': fingerprint(config), 'prompts': self.prompts,
            'prompt_sha256': fingerprint(self.prompts), 'calls': [], 'status': 'initialized'}

    def call(self, stage, payload, settings, validator):
        settings = {**settings, 'seed': self.c['seed'] + len(self.trace['calls'])}
        messages = [{'role': 'system', 'content': self.prompts[stage]},
                    {'role': 'user', 'content': json.dumps(payload, ensure_ascii=False)}]
        entry = {'stage': stage, 'messages': messages, 'settings': settings, 'status': 'pending'}
        self.trace['calls'].append(entry)
        started = time.monotonic()
        try:
            raw = self.backend.complete(messages, settings, stage)
            entry['raw_response'] = raw
            choice = raw['choices'][0]
            if choice.get('finish_reason') != 'stop':
                raise ValueError('Completion did not stop normally; truncation/refusal not accepted')
            content = choice['message']['content']
            # Permit a single JSON Markdown fence, but never repair or infer missing fields.
            if isinstance(content, str) and content.strip().startswith('```'):
                lines = content.strip().splitlines()
                if lines[-1] == '```':
                    content = '\n'.join(lines[1:-1])
            parsed = validator(json.loads(content))
            entry['status'] = 'ok'
            return parsed
        except Exception as exc:
            entry['status'] = 'failed'; entry['error'] = str(exc)
            raise
        finally:
            entry['elapsed_seconds'] = time.monotonic() - started

    def run(self, case, bank=None):
        self.trace['status'] = 'running'
        try:
            if not isinstance(case.get('case_id'), str) or not case['case_id'] or not isinstance(case.get('case_text'), str) or not case['case_text'].strip():
                raise ValueError('Nonempty case_id and case_text are required')
            self.trace['case_sha256'] = fingerprint(case)
            self.trace['case_id'] = case['case_id']
            bank = bank or []
            self.trace['bank_sha256'] = fingerprint(bank)
            exemplars = retrieve(case, bank, self.c['retrieval']) if self.c['mode'] == 'full' else []
            self.trace['retrieved'] = exemplars
            outputs = []
            for index, agent in enumerate(self.c['agents'] if self.c['mode'] == 'full' else self.c['agents'][:1]):
                choices = list(case.get('candidate_diagnoses', []))
                if not all(isinstance(x, str) for x in choices):
                    raise ValueError('candidate_diagnoses must contain strings')
                random.Random(self.c['seed'] + index).shuffle(choices)
                if agent['ordering'] == 'reverse':
                    choices.reverse()
                payload = {'case_text': case['case_text'], 'agent_role': agent['role'],
                           'candidate_consideration_order': choices, 'ordering': agent['ordering'],
                           'retrieved_examples': exemplars}
                answer = self.call('generate', payload, agent['generation'], diagnosis_output)
                history = []
                if self.c['mode'] == 'full':
                    critic = self.c['critic']
                    # Re-critique each refinement, including the final allowed revision.
                    for round_number in range(critic['max_refinements'] + 1):
                        review = self.call('critique', {'case_text': case['case_text'], 'answer': answer},
                                           critic['generation'], critic_output)
                        reward = sum(a * b for a, b in zip(critic['section_weights'], review['coverage'])) - critic['penalty_weight'] * review['contradiction_penalty']
                        needs = review['major_issue'] or reward < critic['minimum_reward']
                        history.append({'round': round_number, 'review': review, 'reward': reward, 'needs_refinement': needs})
                        if not needs or round_number == critic['max_refinements']:
                            break
                        answer = self.call('refine', {**payload, 'previous_answer': answer, 'critique': review},
                                           agent['generation'], diagnosis_output)
                outputs.append(answer)
                self.trace.setdefault('agents', []).append({'id': agent['id'], 'final': answer, 'reviews': history,
                    'unresolved_critic_issue': bool(history and history[-1]['needs_refinement'])})
            result = aggregate(outputs, self.c['voting']) if self.c['mode'] == 'full' else {
                'selected_diagnosis': outputs[0]['differential_diagnosis'][0]['diagnosis'],
                'output': outputs[0], 'score_semantics': 'uncalibrated_model_self_report; not a correctness probability'}
            result.update({'provenance': self.c['provenance'], 'mode': self.c['mode'],
                           'backend': self.c['backend']['kind'], 'call_count': len(self.trace['calls']),
                           'unresolved_critic_issues': any(a['unresolved_critic_issue'] for a in self.trace['agents'])})
            self.trace['status'] = 'complete'; self.trace['result'] = result
            return result
        except Exception as exc:
            self.trace['status'] = 'failed'; self.trace['error'] = str(exc)
            raise
