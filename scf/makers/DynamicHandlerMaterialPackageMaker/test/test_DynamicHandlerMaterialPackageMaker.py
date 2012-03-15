from abjad import *
import handlers
import scf


def test_DynamicHandlerMaterialPackageMaker_01():

    studio = scf.studio.Studio()
    assert not studio.package_exists('materials.testdynamichandler')
    try:
        studio.run(user_input=
            'materials maker dynamic testdynamichandler default '
            'testdynamichandler omi reiterated '
            'dynamic f (1, 16) done default '
            'q '
            )
        mpp = scf.makers.DynamicHandlerMaterialPackageMaker('materials.testdynamichandler')
        assert mpp.directory_contents == ['__init__.py', 'output_material.py', 'tags.py']
        handler = handlers.dynamics.ReiteratedDynamicHandler(
            dynamic_name='f',
            minimum_prolated_duration=Duration(1, 16),
            )
        assert mpp.output_material == handler
    finally:
        studio.run(user_input='m testdynamichandler del remove default q')
        assert not studio.package_exists('materials.testdynamichandler')
