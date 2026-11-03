'''Baseline stub: ABC rejection sampling.

Part of a PROPOSAL's reference implementation; runs on SYNTHETIC/MOCK data only.
'''
from src.inference import abc_rejection


def run(obs, rng, ages, n_targets, noise, n_sims=300):
    '''Return approximate posterior samples, shape (k, 3).'''
    return abc_rejection(obs, rng, ages, n_targets, noise, n_sims=n_sims)
