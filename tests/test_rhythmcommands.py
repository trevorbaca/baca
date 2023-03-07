import abjad
import baca


def test__make_accelerando_multipliers():
    """
    Set exponent less than 1 for decreasing durations:
    """

    durations = 4 * [abjad.Duration(1)]
    multipliers = baca.figures._make_accelerando_multipliers(durations, 0.5)
    assert multipliers == [(2048, 1024), (848, 1024), (651, 1024), (549, 1024)]

    """
    Set exponent to 1 for trivial multipliers:
    """

    durations = 4 * [abjad.Duration(1)]
    multipliers = baca.figures._make_accelerando_multipliers(durations, 1)
    assert multipliers == [(1024, 1024), (1024, 1024), (1024, 1024), (1024, 1024)]

    """
    Set exponent greater than 1 for increasing durations:
    """

    durations = 4 * [abjad.Duration(1)]
    multipliers = baca.figures._make_accelerando_multipliers(durations, 0.5)
    assert multipliers == [(2048, 1024), (848, 1024), (651, 1024), (549, 1024)]
