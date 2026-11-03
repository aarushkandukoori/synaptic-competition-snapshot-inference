'''Unit tests for the SYNTHETIC/MOCK simulator (reference implementation of a proposal).'''
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np  # noqa: E402

from src.simulator import (  # noqa: E402
    NoiseConfig, elimination_time_two, euler_shares, shares_at, simulate_target,
)


def test_closed_form_matches_euler():
    p0 = np.array([0.5, 0.3, 0.2])
    eta, a, t = 0.8, np.array([1.0, 0.2, -0.5]), 2.0
    closed = shares_at(p0, eta * (a - (p0 * a).sum()) * 0 + eta * a, t)
    assert np.abs(closed - euler_shares(p0, eta, a, t)).max() < 5e-3


def test_elimination_time_hits_threshold():
    p0, theta = np.array([0.6, 0.4]), 0.05
    rate_diff = 1.0  # beta = (+0.5, -0.5)
    t_star = elimination_time_two(np.log(1.5), theta, rate_diff)
    p = shares_at(p0, np.array([0.5, -0.5]), t_star)
    assert abs(p[1] - theta) < 1e-9


def test_simulate_target_valid_and_deterministic():
    noise = NoiseConfig(0.1, 0.1, 0.1)
    phi = (0.8, 0.1, 0.5)
    a = simulate_target(np.random.default_rng(3), 4.0, phi, noise)
    b = simulate_target(np.random.default_rng(3), 4.0, phi, noise)
    assert len(a) >= 1 and (a > 0).all()
    assert np.array_equal(a, b)
