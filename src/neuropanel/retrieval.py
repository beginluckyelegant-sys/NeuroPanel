"""Cosine retrieval on caller-supplied frozen embeddings; no hidden embedder."""
import hashlib
import math
import re


def text_key(text):
    return hashlib.sha256(re.sub(r'\s+', ' ', text).strip().casefold().encode()).hexdigest()


def vector(v):
    if not isinstance(v, list) or not v or any(type(x) not in (int, float) or not math.isfinite(x) for x in v):
        raise ValueError('Embedding must be a finite numeric vector')
    norm = math.hypot(*v)
    if norm == 0 or not math.isfinite(norm):
        raise ValueError('Invalid embedding norm')
    return [x / norm for x in v]


def retrieve(case, bank, config):
    if not config['enabled']:
        return []
    if case.get('embedding_revision') != config['embedding_revision'] or not config['embedding_revision']:
        raise ValueError('Query embedding revision must match the frozen bank')
    query = vector(case.get('embedding'))
    candidates = []
    seen = set()
    excluded = set(config.get('excluded_case_ids', [])) | {case['case_id']}
    for row in bank:
        if not isinstance(row.get('case_id'), str) or not isinstance(row.get('case_text'), str):
            raise ValueError('Bank entries require case_id and case_text strings')
        if row['case_id'] in seen:
            raise ValueError('Duplicate bank case_id')
        seen.add(row['case_id'])
        if row.get('embedding_revision') != config['embedding_revision']:
            raise ValueError('Mixed embedding revisions in bank')
        if row['case_id'] in excluded or text_key(row['case_text']) == text_key(case['case_text']):
            continue
        if any(case.get(k) is not None and row.get(k) == case[k] for k in ('patient_id', 'group_id')):
            continue
        candidate = vector(row.get('embedding'))
        if len(candidate) != len(query):
            raise ValueError('Embedding dimension mismatch')
        score = sum(a * b for a, b in zip(query, candidate))
        if score >= config['min_similarity']:
            candidates.append({'case_id': row['case_id'], 'case_text': row['case_text'],
                'example_output': row.get('example_output'), 'similarity': score})
    candidates.sort(key=lambda x: (-x['similarity'], x['case_id']))
    return candidates[:config['top_k']]
