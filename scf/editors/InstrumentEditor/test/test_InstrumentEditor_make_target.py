import baca
from abjad import *


def test_InstrumentEditor_make_target_01():
    '''Make instrument.
    '''

    instrument_editor = baca.scf.editors.InstrumentEditor()
    instrument_editor.session.user_input = '9 q'
    instrument_editor.run()
    assert instrument_editor.target == instrumenttools.ContrabassFlute()
