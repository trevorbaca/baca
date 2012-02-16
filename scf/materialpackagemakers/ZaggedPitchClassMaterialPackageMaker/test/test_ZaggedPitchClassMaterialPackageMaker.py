from baca.scf.editors import UserInputWrapper
import baca


def test_ZaggedPitchClassMaterialPackageMaker_01():
    '''Emtpy wrapper.'''

    studio = baca.scf.studio.Studio()
    assert not studio.package_exists('baca.materials.testzagged')
    try:
        studio.run(user_input=
            'materials maker zagged testzagged default '
            'q'
            )
        mpp = baca.scf.materialpackagemakers.ZaggedPitchClassMaterialPackageMaker(
            'baca.materials.testzagged')
        assert mpp.directory_contents == ['__init__.py', 'user_input.py']
        user_input_wrapper = UserInputWrapper([
            ('pc_cells', None),
            ('division_cells', None),
            ('grouping_counts', None)])
        assert mpp.user_input_wrapper_in_memory == user_input_wrapper
    finally:
        studio.run(user_input='m testzagged del remove default q')
        assert not studio.package_exists('baca.materials.testzagged')


def test_ZaggedPitchClassMaterialPackageMaker_02():
    '''Populate wrapper.'''

    studio = baca.scf.studio.Studio()
    assert not studio.package_exists('baca.materials.testzagged')
    try:
        studio.run(user_input=
            'materials maker zagged testzagged default '
            'testzagged uip 1 [[0, 7, 2, 10], [9, 6, 1, 8]] '
            '[[[1], [1], [1], [1, 1, 1]]] '
            '[1, 1, 2, 3] '
            'q'
            )
        mpp = baca.scf.materialpackagemakers.ZaggedPitchClassMaterialPackageMaker(
            'baca.materials.testzagged')
        assert mpp.directory_contents == ['__init__.py', 'user_input.py']
        user_input_wrapper = UserInputWrapper([
            ('pc_cells', [[0, 7, 2, 10], [9, 6, 1, 8]]),
            ('division_cells', [[[1], [1], [1], [1, 1, 1]]]),
            ('grouping_counts', [1, 1, 2, 3])])
        assert mpp.user_input_wrapper_in_memory == user_input_wrapper
    finally:
        studio.run(user_input='m testzagged del remove default q')
        assert not studio.package_exists('baca.materials.testzagged')
