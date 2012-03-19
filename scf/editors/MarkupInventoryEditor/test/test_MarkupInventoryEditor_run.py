from abjad import *
import scf


def test_MarkupInventoryEditor_run_01():

    editor = scf.editors.MarkupInventoryEditor()
    editor.run(user_input='add foo~bar add more~foo~bar done')
    inventory = markuptools.MarkupInventory(['foo bar', 'more foo bar'])

    assert editor.target == inventory
