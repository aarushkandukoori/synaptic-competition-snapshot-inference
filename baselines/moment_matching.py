'''Baseline stub: moment matching on innervation-number and log-ratio summaries.

Part of a PROPOSAL's reference implementation; runs on SYNTHETIC/MOCK data only.
'''
from src.inference import moment_matching


def run(obs, rng, ages, n_targets, noise):
    '''Return a point estimate of (sigma_beta, theta, sigma0).'''
    return moment_matching(obs, rng, ages, n_targets, noise)
