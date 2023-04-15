import baca
import pytest


def test_dynamics_01():
    """
    baca.dynamics.make_dynamic() Errors on nondynamic input.
    """

    with pytest.raises(Exception):
        baca.dynamics.make_dynamic("text")
