from abjad.tools import pitchtools
from baca.scf.editors import UserInputWrapper
import baca


def test_PitchRangeInventoryMaterialPackageMaker_01():
    '''Empty wrapper.'''

    studio = baca.scf.studiopackage.Studio()
    assert not studio.package_exists('baca.materials.testpir')
    try:
        studio.run(user_input=
            'materials maker pitch testpir default '
            'q'
            )
        mpp = baca.scf.materialpackagemakers.PitchRangeInventoryMaterialPackageMaker(
            'baca.materials.testpir')
        # TODO: mpp.directory_contents == ['__init__.py']
        assert mpp.directory_contents == ['__init__.py', 'user_input.py']
        assert mpp.output_material is None
        assert mpp.user_input_wrapper_in_memory.is_empty
    finally:
        studio.run(user_input='m testpir del remove default q')
        assert not studio.package_exists('baca.materials.testpir')


def test_PitchRangeInventoryMaterialPackageMaker_02():
    '''Populate wrapper.'''

    studio = baca.scf.studiopackage.Studio()
    assert not studio.package_exists('baca.materials.testpir')
    try:
        studio.run(user_input=
            'materials maker pitch testpir default '
            'testpir omi add [A0, C8] add [C2, F#5] add [C2, G5] '
            'del 1 move 1 2 b default '
            'q'
            )
        mpp = baca.scf.materialpackagemakers.PitchRangeInventoryMaterialPackageMaker(
            'baca.materials.testpir')
        # TODO: mpp.directory_contents == ['__init__.py', 'output_material.py']
        assert mpp.directory_contents == ['__init__.py', 'output_material.py', 'user_input.py']
        pitch_range_inventory = pitchtools.PitchRangeInventory([
            pitchtools.PitchRange('[C2, G5]'), pitchtools.PitchRange('[C2, F#5]')])
        assert mpp.output_material == pitch_range_inventory
        assert mpp.user_input_wrapper_in_memory.is_empty
    finally:
        studio.run(user_input='m testpir del remove default q')
        assert not studio.package_exists('baca.materials.testpir')
