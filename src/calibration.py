'''Simulation-based calibration and credible-interval coverage helpers.

Reference implementation of a PROPOSAL. Works on SYNTHETIC/MOCK data only.
'''
import numpy as np

from src.simulator import sample_prior, simulate_snapshot
from src.summaries import summarize


def sbc_ranks(posterior_fn, n_trials, rng, ages, n_targets, noise):
    '''For each trial: draw phi*, simulate, get posterior samples via
    posterior_fn(obs_summary, rng), and record per-parameter ranks of phi*.
    Ranks should be roughly uniform if the posterior is calibrated.'''
    ranks, truths, samples = [], [], []
    for _ in range(n_trials):
        phi = sample_prior(rng)
        obs = summarize(simulate_snapshot(rng, ages, n_targets, phi, noise))
        s = posterior_fn(obs, rng)
        ranks.append((s < phi).sum(axis=0))
        truths.append(phi)
        samples.append(s)
    return np.array(ranks), np.array(truths), samples


def coverage(samples, truths, level=0.8):
    '''Fraction of trials whose truth lies in the central `level` interval,
    per parameter.'''
    a = (1 - level) / 2
    hits = []
    for s, t in zip(samples, truths):
        lo, hi = np.quantile(s, [a, 1 - a], axis=0)
        hits.append((t >= lo) & (t <= hi))
    return np.mean(hits, axis=0)
