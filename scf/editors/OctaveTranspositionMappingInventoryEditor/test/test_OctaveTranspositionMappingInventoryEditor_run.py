from abjad.tools import pitchtools
import scf


def test_OctaveTranspositionMappingInventoryEditor_run_01():
    '''Empty inventories.
    '''

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
    '''Empty named inventory.
    '''

    editor = scf.editors.OctaveTranspositionMappingInventoryEditor()
    editor.run(user_input='name foo done')
    assert editor.target == pitchtools.OctaveTranspositionMappingInventory(inventory_name='foo')


def test_OctaveTranspositionMappingInventoryEditor_run_03():
    '''Named inventory with named mapping.
    '''

    editor = scf.editors.OctaveTranspositionMappingInventoryEditor()
    editor.run(user_input=
        'name mapping~inventory '
        'add name piccolo~strict~first~octave '
        'add source [A0, C8] target 14 '
        'done done done '
        )

    inventory = pitchtools.OctaveTranspositionMappingInventory(
        [pitchtools.OctaveTranspositionMapping(
            [('[A0, C8]', 14)], 
            inventory_name='piccolo strict first octave')], 
        inventory_name='mapping inventory'
        )

    assert editor.target == inventory
