from experimental import *


def test_ConstellationCircuitSelectionMaterialPackageMaker_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'experimental.tools.scoremanagertools.materialpackages.testconst')
    try:
        score_manager._run(pending_user_input=
            'materials maker constellation testconst '
            "(1, 18) (2, 48) done b default q "
            )
        mpp = scoremanagertools.materialpackagemakers.ListMaterialPackageMaker(
            'experimental.tools.scoremanagertools.materialpackages.testconst')
        assert mpp.list_directory() == ['__init__.py', 'output_material.py', 'tags.py']
        assert mpp.output_material == [(1, 18), (2, 48)]
    finally:
        score_manager._run(pending_user_input='m testconst del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'experimental.tools.scoremanagertools.materialpackages.testconst')
