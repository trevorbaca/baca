from abjad import *
from experimental.tools import handlertools
import scf


def test_DynamicHandlerCreationWizard_run_01():

    wizard = scf.wizards.DynamicHandlerCreationWizard()
    wizard.run(user_input='reit f (1, 16) done')

    handler = handlertools.dynamics.ReiteratedDynamicHandler(
        dynamic_name='f',
        minimum_duration=Duration(1, 16),
        )

    assert wizard.target == handler
