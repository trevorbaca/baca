import baca
from abjad import *


def test_InstrumentEditor_make_target_01():

    editor = baca.scf.editors.InstrumentEditor()
    editor.run(user_input='9 q')
    assert editor.target == instrumenttools.ContrabassFlute()
