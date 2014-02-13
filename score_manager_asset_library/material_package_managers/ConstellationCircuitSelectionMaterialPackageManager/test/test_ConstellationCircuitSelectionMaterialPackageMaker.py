import pytest
from experimental import *
pytest.skip('FIXME: CC mpm not included in list of mp makers.')


def test_ConstellationCircuitSelectionMaterialPackageManager_01():

    score_manager = scoremanager.score.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanager.materialpackages.testconst')
    try:
        score_manager._run(pending_user_input=
            'materials maker constellation testconst '
            "(1, 18) (2, 48) done b default q "
            )
        mpp = scoremanager.materialpackagemanagers.ListMaterialPackageManager(
            'scoremanager.materialpackages.testconst')
        assert mpp.list_directory() == [
            '__init__.py', 'output_material.py', 'tags.py']
        assert mpp.output_material == [(1, 18), (2, 48)]
    finally:
        score_manager._run(pending_user_input=
            'm testconst del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testconst')
