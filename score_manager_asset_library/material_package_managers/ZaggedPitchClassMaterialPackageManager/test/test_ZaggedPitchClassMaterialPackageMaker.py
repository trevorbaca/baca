import pytest
from experimental import *
pytest.skip('REMOVE ME')


def test_ZaggedPitchClassMaterialPackageManager_01():
    '''Empty wrapper.
    '''

    studio = scoremanager.studio.Studio()
    assert not studio.package_exists('materials.testzagged')
    try:
        studio.run(pending_user_input=
            'materials maker zagged testzagged default '
            'q'
            )
        mpp = scoremanager.materialpackagemanagers.ZaggedPitchClassMaterialPackageManager(
            'materials.testzagged')
        assert mpp.directory_contents == ['__init__.py', 'tags.py', 'user_input.py']
        user_input_wrapper = scoremanager.editors.UserInputWrapper([
            ('pc_cells', None),
            ('division_cells', None),
            ('grouping_counts', None)])
        assert mpp.user_input_wrapper_in_memory == user_input_wrapper
    finally:
        studio.run(pending_user_input='m testzagged del remove default q')
        assert not studio.package_exists('materials.testzagged')


def test_ZaggedPitchClassMaterialPackageManager_02():
    '''Populate wrapper.
    '''

    studio = scoremanager.studio.Studio()
    assert not studio.package_exists('materials.testzagged')
    try:
        studio.run(pending_user_input=
            'materials maker zagged testzagged default '
            'testzagged uip 1 [[0, 7, 2, 10], [9, 6, 1, 8]] '
            '[[[1], [1], [1], [1, 1, 1]]] '
            '[1, 1, 2, 3] '
            'q'
            )
        mpp = scoremanager.materialpackagemanagers.ZaggedPitchClassMaterialPackageManager(
            'materials.testzagged')
        assert mpp.directory_contents == ['__init__.py', 'tags.py', 'user_input.py']
        user_input_wrapper = scoremanager.editors.UserInputWrapper([
            ('pc_cells', [[0, 7, 2, 10], [9, 6, 1, 8]]),
            ('division_cells', [[[1], [1], [1], [1, 1, 1]]]),
            ('grouping_counts', [1, 1, 2, 3])])
        assert mpp.user_input_wrapper_in_memory == user_input_wrapper
    finally:
        studio.run(pending_user_input='m testzagged del remove default q')
        assert not studio.package_exists('materials.testzagged')
