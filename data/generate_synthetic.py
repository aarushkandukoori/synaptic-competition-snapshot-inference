'''Write SYNTHETIC / MOCK connectomic snapshots to data/synthetic/.

Reference implementation of a PROPOSAL (no experiments have been run).
Everything written here comes from the in-repo toy simulator. No real
connectomic, animal, or laboratory data is used or implied.

Usage: python data/generate_synthetic.py
'''
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402

from src.simulator import (  # noqa: E402
    PARAM_NAMES, SYNTHETIC_LABEL, NoiseConfig, simulate_snapshot,
)

DEFAULT_AGES = (1.0, 3.0, 6.0)
DEFAULT_PHI = (0.8, 0.08, 0.5)  # (sigma_beta, theta, sigma0), arbitrary toy values
DEFAULT_NOISE = NoiseConfig(size_sigma=0.1, p_missed=0.02, p_merge=0.02)
OUT_PATH = Path(__file__).resolve().parent / 'synthetic' / 'snapshots.json'


def generate(path=OUT_PATH, seed=0, ages=DEFAULT_AGES, n_targets=100,
             phi=DEFAULT_PHI, noise=DEFAULT_NOISE):
    '''Simulate snapshots at each age and write them as labeled JSON.'''
    rng = np.random.default_rng(seed)
    snap = simulate_snapshot(rng, ages, n_targets, phi, noise)
    doc = {
        'label': SYNTHETIC_LABEL,
        'seed': seed,
        'ages': list(ages),
        'param_names': list(PARAM_NAMES),
        'phi_true': list(phi),
        'noise': vars(noise),
        'snapshots': [[[float(x) for x in t] for t in age_targets]
                      for age_targets in snap],
    }
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc))
    return path


if __name__ == '__main__':
    print('wrote', generate(), '(' + SYNTHETIC_LABEL + ')')
