from experimental import *


def test_ConstellationCircuitSelectionMaterialPackageMaker_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not packagepathtools.package_exists('materials.testconst')
    try:
        score_manager.run(user_input=
            'materials maker constellation testconst '
            "(1, 18) (2, 48) done b default q "
            )
        mpp = scoremanagertools.materialpackagemakers.ListMaterialPackageMaker('system_materials.testconst')
        assert mpp.directory_contents == ['__init__.py', 'output_material.py', 'tags.py']
        assert mpp.output_material == [(1, 18), (2, 48)]
    finally:
        score_manager.run(user_input='m testconst del remove default q')
        assert not packagepathtools.package_exists('materials.testconst')
