'''Tests for the scaling and shift symmetries (SYNTHETIC random inputs only).'''
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np  # noqa: E402

from src.identifiability import scaling_symmetry_gap, shift_symmetry_gap  # noqa: E402


def test_scaling_symmetry():
    assert scaling_symmetry_gap(np.random.default_rng(0)) < 1e-9


def test_shift_symmetry():
    assert shift_symmetry_gap(np.random.default_rng(0)) < 1e-9
