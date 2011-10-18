import baca
from abjad import *


def test_PerformerEditor_remove_performer_name_01():
    '''Create performer, name performer, remove performer name.
    '''

    editor = baca.scf.editors.PerformerEditor()
    editor.run(user_input='name foo rpn q')
    assert editor.target == scoretools.Performer()
