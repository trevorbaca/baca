import kaleids
import scf


def test_KaleidMaterialPackageMaker_01():

    studio = scf.studio.Studio()
    assert not studio.package_exists('materials.testkaleid')
    try:
        studio.run(user_input=
            'materials maker kaleid testkaleid default '
            'testkaleid omi patternedtokens '
            'pattern [-1, 2, -3, 4] 16 [2, 3] [6] b default '
            'q '
            )
        mpp = scf.makers.KaleidMaterialPackageMaker('materials.testkaleid')
        assert mpp.directory_contents == ['__init__.py', 'output_material.py', 'tags.py']
        kaleid = kaleids.PatternedTokens(
            [-1, 2, -3, 4],
            16,
            prolation_addenda=[2, 3],
            secondary_divisions=[6])
        assert mpp.output_material == kaleid
    finally:
        studio.run(user_input='m testkaleid del remove default q')
        assert not studio.package_exists('materials.testkaleid')
