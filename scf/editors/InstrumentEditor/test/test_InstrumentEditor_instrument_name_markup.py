from abjad import *
import baca


def test_InstrumentEditor_instrument_name_markup_01():
    '''Quit, back & studio all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 setup performers 1 1 inm q')
    assert studio.ts == (13, (1, 7, 9))

    studio.run(user_input='1 setup performers 1 1 inm b q')
    assert studio.ts == (15, (1, 7, 9), (10, 13))

    studio.run(user_input='1 setup performers 1 1 inm studio q')
    assert studio.ts == (15, (0, 13), (1, 7, 9))
