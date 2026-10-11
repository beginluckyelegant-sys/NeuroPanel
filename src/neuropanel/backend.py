"""Explicit OpenAI-compatible HTTP adapter and synthetic demonstration backend."""
import json
import os
import time
import urllib.error
import urllib.request
from urllib.parse import urlparse


class HTTPBackend:
    def __init__(self, config):
        self.config = config
        self.base = config['base_url'].rstrip('/')
        parsed = urlparse(self.base)
        if parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ValueError('Do not embed credentials in base_url')
        if parsed.scheme not in ('http', 'https') or not parsed.hostname:
            raise ValueError('Invalid base_url')
        if parsed.scheme == 'http' and parsed.hostname not in ('localhost', '127.0.0.1', '::1'):
            raise ValueError('Remote endpoints require HTTPS; use a local tunnel for HTTP')

    def complete(self, messages, settings, stage):
        payload = {'model': self.config['model'], 'messages': messages, **settings}
        headers = {'Content-Type': 'application/json'}
        key = os.environ.get(self.config.get('api_key_env', 'NEUROPANEL_API_KEY'))
        if key:
            headers['Authorization'] = 'Bearer ' + key
        attempts = []
        for attempt in range(self.config.get('max_retries', 0) + 1):
            try:
                req = urllib.request.Request(self.base + '/chat/completions',
                    data=json.dumps(payload).encode(), headers=headers)
                with urllib.request.urlopen(req, timeout=self.config['timeout_seconds']) as response:
                    result = json.load(response)
                result['_transport_attempts'] = attempts + [{'attempt': attempt + 1, 'status': 'ok'}]
                return result
            except urllib.error.HTTPError as exc:
                attempts.append({'attempt': attempt + 1, 'http_status': exc.code})
                if exc.code not in (429, 500, 502, 503, 504) or attempt == self.config.get('max_retries', 0):
                    raise RuntimeError(f'HTTP call failed; attempts={attempts}') from None
            except (urllib.error.URLError, TimeoutError):
                attempts.append({'attempt': attempt + 1, 'status': 'network_error'})
                if attempt == self.config.get('max_retries', 0):
                    raise RuntimeError(f'Network call failed; attempts={attempts}') from None
            time.sleep(min(2 ** attempt, 8))


class MockBackend:
    """Deterministic fixtures only. No language model or clinical judgment."""
    def complete(self, messages, settings, stage):
        if stage == 'critique':
            content = {'coverage': [1.0, 1.0, 1.0, 0.5], 'contradiction_penalty': 0.0,
                       'major_issue': True, 'feedback': 'Synthetic fixture: make the conclusion explicit.'}
        else:
            content = {'symptom_analysis': 'Synthetic fixture; no patient information.',
                       'differential_diagnosis': [{'diagnosis': 'Candidate A', 'score': 0.7},
                                                  {'diagnosis': 'Candidate B', 'score': 0.3}],
                       'further_tests': 'No clinical recommendation in this fixture.',
                       'final_conclusion': 'Candidate A (synthetic fixture).'}
        return {'choices': [{'message': {'content': json.dumps(content)}, 'finish_reason': 'stop'}],
                'model': 'mock-fixture', 'usage': {'prompt_tokens': 0, 'completion_tokens': 0}}
