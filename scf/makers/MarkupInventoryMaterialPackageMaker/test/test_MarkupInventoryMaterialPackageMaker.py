from abjad import *
import py
import scf


def test_MarkupInventoryMaterialPackageMaker_01():
    py.test.skip('write this test.')

    studio = scf.studio.Studio()
    assert not studio.package_exists('materials.testmarkupinventory')
    try:
        studio.run(user_input=
            'materials maker articulation testmarkupinventory default '
            'testmarkupinventory omi reiterated '
            "['^', '.'] (1, 64) (1, 4) c c'''' done default "
            'q '
            )
        mpp = scf.makers.ArticulationHandlerMaterialPackageMaker('materials.testmarkupinventory')
        assert mpp.directory_contents == ['__init__.py', 'output_material.py', 'tags.py']
        handler = handlers.articulations.ReiteratedArticulationHandler(
            articulation_list=['^', '.'],
            minimum_prolated_duration=Duration(1, 64),
            maximum_prolated_duration=Duration(1, 4),
            minimum_written_pitch=pitchtools.NamedChromaticPitch('c'),
            maximum_written_pitch=pitchtools.NamedChromaticPitch("c''''"),
            )
        assert mpp.output_material == handler
    finally:
        studio.run(user_input='m testmarkupinventory del remove default q')
        assert not studio.package_exists('materials.testmarkupinventory')
