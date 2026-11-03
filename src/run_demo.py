'''End-to-end toy demo on SYNTHETIC/MOCK data.

Reference implementation of a PROPOSAL. Prints whatever the toy estimators
produce on generated data; these are smoke-test outputs, not results.

Usage: python -m src.run_demo
'''
import numpy as np

from data.generate_synthetic import generate
from src.calibration import coverage, sbc_ranks
from src.identifiability import scaling_symmetry_gap, shift_symmetry_gap
from src.inference import abc_rejection, moment_matching
from src.simulator import PARAM_NAMES
from src.summaries import load_synthetic_snapshot, summarize

SEED = 1


def main():
    path = generate(seed=0)
    data = load_synthetic_snapshot(path)
    print('data:', data['label'])
    ages, noise = data['ages'], data['noise']
    n_targets = len(data['snapshot'][0])
    obs = summarize(data['snapshot'])
    rng = np.random.default_rng(SEED)

    post = abc_rejection(obs, rng, ages, n_targets, noise)
    mm = moment_matching(obs, rng, ages, n_targets, noise)
    for i, name in enumerate(PARAM_NAMES):
        print(f'{name}: true={data["phi_true"][i]:.3f} '
              f'abc_mean={post[:, i].mean():.3f} abc_sd={post[:, i].std():.3f} '
              f'moment_matching={mm[i]:.3f}')

    def post_fn(o, r):
        return abc_rejection(o, r, ages, 30, noise, n_sims=100)

    _, truths, samples = sbc_ranks(post_fn, 5, rng, ages, 30, noise)
    print('80% coverage (toy, 5 trials):', coverage(samples, truths).round(2))
    print('scaling gap:', scaling_symmetry_gap(rng))
    print('shift gap:', shift_symmetry_gap(rng))
    print('NOTE: toy smoke test on synthetic data; no benchmark claims.')


if __name__ == '__main__':
    main()
