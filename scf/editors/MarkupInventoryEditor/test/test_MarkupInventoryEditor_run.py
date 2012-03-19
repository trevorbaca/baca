from abjad import *
import scf


def test_MarkupInventoryEditor_run_01():

    editor = scf.editors.MarkupInventoryEditor()
    editor.run(user_input="add arg r'\\italic~{~serenamente~possibile~}' 3 serenamente done done")

    inventory = markuptools.MarkupInventory([
        markuptools.Markup('\\italic { serenamente possibile }', markup_name='serenamente')
        ])

    assert editor.target == inventory
