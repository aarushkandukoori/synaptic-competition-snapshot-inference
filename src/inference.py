'''Inference methods: moment matching, ABC rejection, NPE placeholders.

Reference implementation of a PROPOSAL. Both implemented estimators are
deliberately simple, run on SYNTHETIC/MOCK data, and are not tuned. The
neural estimators are stubs and raise NotImplementedError.
'''
import numpy as np

from src.simulator import PRIOR_RANGES, PARAM_NAMES, sample_prior, simulate_snapshot
from src.summaries import summarize

LO = np.array([PRIOR_RANGES[k][0] for k in PARAM_NAMES])
HI = np.array([PRIOR_RANGES[k][1] for k in PARAM_NAMES])


def prior_predictive(rng, n_sims, ages, n_targets, noise):
    '''Draw phi from the prior and simulate summaries. Returns (phis, sums).'''
    phis = np.array([sample_prior(rng) for _ in range(n_sims)])
    sums = np.array([summarize(simulate_snapshot(rng, ages, n_targets, p, noise))
                     for p in phis])
    return phis, sums


def _scale(sums):
    s = sums.std(axis=0)
    s[s == 0] = 1.0
    return s


def abc_rejection(obs, rng, ages, n_targets, noise, n_sims=300, quantile=0.1):
    '''Keep the prior draws whose summaries are closest to `obs`.
    Returns approximate posterior samples, shape (k, 3).'''
    phis, sums = prior_predictive(rng, n_sims, ages, n_targets, noise)
    d = np.sqrt((((sums - obs) / _scale(sums)) ** 2).sum(axis=1))
    k = max(1, int(quantile * n_sims))
    return phis[np.argsort(d)[:k]]


def moment_matching(obs, rng, ages, n_targets, noise, n_pilot=60, rounds=3, n_local=15):
    '''Point estimate: minimize scaled summary distance (pilot search, then
    shrinking random local refinement with a fixed simulation seed).'''
    phis, sums = prior_predictive(rng, n_pilot, ages, n_targets, noise)
    scale = _scale(sums)
    d = np.sqrt((((sums - obs) / scale) ** 2).sum(axis=1))
    best, best_d = phis[np.argmin(d)], float(d.min())
    seed = int(rng.integers(1 << 31))
    step = 0.2 * (HI - LO)
    for _ in range(rounds):
        for _ in range(n_local):
            cand = np.clip(best + rng.normal(0, 1, 3) * step, LO, HI)
            sim = summarize(simulate_snapshot(np.random.default_rng(seed), ages,
                                              n_targets, cand, noise))
            dc = float(np.sqrt((((sim - obs) / scale) ** 2).sum()))
            if dc < best_d:
                best, best_d = cand, dc
        step = step * 0.5
    return best


class NPEHandcrafted:
    '''Placeholder: neural posterior estimation on hand-crafted summaries.'''

    def fit(self, phis, sums):
        raise NotImplementedError('NPE is planned, not implemented in this skeleton')

    def sample(self, obs, n):
        raise NotImplementedError('NPE is planned, not implemented in this skeleton')


class NPEGraphSAGE(NPEHandcrafted):
    '''Placeholder: NPE with a GraphSAGE-style summary network over
    summaries.bipartite_edges output. Not implemented.'''
