"""Strict JSON contracts; invalid output is not silently salvaged."""
import math


def unit_number(value):
    return type(value) in (int, float) and math.isfinite(value) and 0 <= value <= 1


def diagnosis_output(value):
    if not isinstance(value, dict):
        raise ValueError('Diagnosis output must be an object')
    for key in ('symptom_analysis', 'further_tests', 'final_conclusion'):
        if not isinstance(value.get(key), str):
            raise ValueError('Missing string section: ' + key)
    ddx = value.get('differential_diagnosis')
    if not isinstance(ddx, list) or not ddx:
        raise ValueError('A nonempty ranked differential_diagnosis list is required')
    for item in ddx:
        if not isinstance(item, dict) or not isinstance(item.get('diagnosis'), str) or not item['diagnosis'].strip():
            raise ValueError('Each candidate requires a nonempty diagnosis')
        if not unit_number(item.get('score')):
            raise ValueError('Candidate score must be finite and in [0, 1]')
    return value


def critic_output(value):
    if not isinstance(value, dict):
        raise ValueError('Critic output must be an object')
    coverage = value.get('coverage')
    if not isinstance(coverage, list) or len(coverage) != 4 or not all(unit_number(x) for x in coverage):
        raise ValueError('Critic coverage requires four values in [0, 1]')
    if not unit_number(value.get('contradiction_penalty')) or type(value.get('major_issue')) is not bool:
        raise ValueError('Invalid critic penalty/major_issue')
    if not isinstance(value.get('feedback'), str):
        raise ValueError('Critic feedback must be a string')
    return value
