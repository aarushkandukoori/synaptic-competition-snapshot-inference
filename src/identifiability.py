'''Numerical checks of the two snapshot symmetries from the proposal.

(1) scaling: (eta, a) -> (c*eta, a/c); (2) shift: a_i -> a_i + c.
Reference implementation of a PROPOSAL; uses SYNTHETIC random inputs only.
'''
import numpy as np

from src.simulator import shares_at


def _draw(rng, n):
    p0 = np.exp(rng.normal(0, 0.5, n))
    return p0 / p0.sum(), rng.normal(0, 1, n)


def scaling_symmetry_gap(rng, n=4, eta=0.7, c=3.0, t=2.0):
    '''Max |p(t) difference| between (eta, a) and (c*eta, a/c). Expect ~0.'''
    p0, a = _draw(rng, n)
    return float(np.abs(shares_at(p0, eta * a, t)
                        - shares_at(p0, (c * eta) * (a / c), t)).max())


def shift_symmetry_gap(rng, n=4, eta=0.7, c=1.5, t=2.0):
    '''Max |p(t) difference| between a and a + c. Expect ~0.'''
    p0, a = _draw(rng, n)
    return float(np.abs(shares_at(p0, eta * a, t)
                        - shares_at(p0, eta * (a + c), t)).max())
