'''Hand-crafted snapshot summaries, bipartite-graph builder, synthetic loader.

Reference implementation of a PROPOSAL. Operates on SYNTHETIC/MOCK data only.
'''
import json
from pathlib import Path

import numpy as np

from src.simulator import NoiseConfig


def summarize(snapshot):
    '''Per age: mean innervation number, fraction singly innervated, mean
    log(largest/second-largest) over multiply innervated targets.'''
    out = []
    for targets in snapshot:
        counts = np.array([len(t) for t in targets], dtype=float)
        ratios = [np.log(t[0] / t[1]) for t in targets if len(t) >= 2]
        out += [counts.mean(), float((counts == 1).mean()),
                float(np.mean(ratios)) if ratios else 0.0]
    return np.array(out)


def bipartite_edges(targets):
    '''Edge list (axon_id, target_id, size) for one age. Axon ids are local
    labels only; the proposal has no cross-target axon identity here.'''
    edges, axon = [], 0
    for j, sizes in enumerate(targets):
        for s in sizes:
            edges.append((axon, j, float(s)))
            axon += 1
    return edges


def load_synthetic_snapshot(path):
    '''Load a file written by data/generate_synthetic.py; refuses unlabeled data.'''
    doc = json.loads(Path(path).read_text())
    if not str(doc.get('label', '')).startswith('SYNTHETIC'):
        raise ValueError('refusing to load data not labeled SYNTHETIC')
    snap = [[np.array(t) for t in age_targets] for age_targets in doc['snapshots']]
    return {'ages': tuple(doc['ages']), 'snapshot': snap,
            'phi_true': np.array(doc['phi_true']),
            'noise': NoiseConfig(**doc['noise']), 'label': doc['label']}
