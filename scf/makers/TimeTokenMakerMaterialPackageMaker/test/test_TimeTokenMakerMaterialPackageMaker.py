from abjad.tools import timetokentools
import scf


def test_TimeTokenMakerMaterialPackageMaker_01():

    studio = scf.studio.Studio()
    assert not studio.package_exists('materials.testtimetokenmaker')
    try:
        studio.run(user_input=
            'materials maker time testtimetokenmaker default '
            'testtimetokenmaker omi signalfilledtimetokenmaker '
            '[-1, 2, -3, 4] 16 [2, 3] [6] b default '
            'q '
            )
        mpp = scf.makers.TimeTokenMakerMaterialPackageMaker('materials.testtimetokenmaker')
        assert mpp.directory_contents == ['__init__.py', 'output_material.py', 'tags.py']
        maker = timetokentools.SignalFilledTimeTokenMaker(
            [-1, 2, -3, 4],
            16,
            prolation_addenda=[2, 3],
            secondary_divisions=[6])
        assert mpp.output_material == maker
    finally:
        studio.run(user_input='m testtimetokenmaker del remove default q')
        assert not studio.package_exists('materials.testtimetokenmaker')
