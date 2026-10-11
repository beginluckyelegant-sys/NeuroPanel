"""Hard/soft vote aggregation. Self-reported scores are not probabilities."""
import re
import unicodedata


def normalize(name):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', name).strip()).casefold()


def aggregate(outputs, config):
    if not outputs:
        raise ValueError('Cannot vote without agents')
    aliases = {normalize(k): normalize(v) for k, v in config.get('aliases', {}).items()}
    # Require one-hop canonical mappings rather than silently following chains.
    if any(v in aliases and aliases[v] != v for v in aliases.values()):
        raise ValueError('Alias targets must be canonical (no chains/cycles)')
    totals = {}
    for output in outputs:
        unique = {}
        for item in output['differential_diagnosis']:
            key = normalize(item['diagnosis']); key = aliases.get(key, key)
            if key not in unique:
                unique[key] = item['score']
            else:
                unique[key] = max(unique[key], item['score'])
        for rank, (key, score) in enumerate(unique.items()):
            row = totals.setdefault(key, {'diagnosis': key, 'hard_votes': 0, 'soft_sum': 0.0})
            row['hard_votes'] += int(rank < config['top_k'])
            row['soft_sum'] += score
    for row in totals.values():
        row['vote_score'] = row['hard_votes'] + config['soft_weight'] * row['soft_sum']
        row['mean_self_reported_score'] = row['soft_sum'] / len(outputs)
    # Explicit deterministic tie policy: total score, hard count, canonical name.
    ranked = sorted(totals.values(), key=lambda r: (-r['vote_score'], -r['hard_votes'], r['diagnosis']))
    return {'selected_diagnosis': ranked[0]['diagnosis'], 'ranking': ranked,
            'score_semantics': 'uncalibrated_model_self_report; not a correctness probability',
            'agent_count': len(outputs)}
