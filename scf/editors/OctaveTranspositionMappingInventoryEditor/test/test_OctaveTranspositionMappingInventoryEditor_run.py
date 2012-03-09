from abjad.tools import pitchtools
import scf


def test_OctaveTranspositionMappingInventoryEditor_run_01():

    editor = scf.editors.OctaveTranspositionMappingInventoryEditor()
    editor.run(user_input='done')
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory()

    editor = scf.editors.OctaveTranspositionMappingInventoryEditor()
    editor.run(user_input='q')
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory()

    editor = scf.editors.OctaveTranspositionMappingInventoryEditor()
    editor.run(user_input='b')
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory()

    editor = scf.editors.OctaveTranspositionMappingInventoryEditor()
    editor.run(user_input='studio')
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory()


def test_OctaveTranspositionMappingInventoryEditor_run_02():

    editor = scf.editors.OctaveTranspositionMappingInventoryEditor()
    editor.run(user_input='name foo done')
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory(inventory_name='foo')
