from abjad import *
import handlers
import scf


def test_ArticulationHandlerCreationWizard_run_01():

    wizard = scf.wizards.ArticulationHandlerCreationWizard()
    wizard.run(user_input="reit ['^', '.'] (1, 64) (1, 4) c c'''' done")

    handler = handlers.articulations.ReiteratedArticulationHandler(
        articulation_list=['^', '.'],
        minimum_prolated_duration=Duration(1, 64),
        maximum_prolated_duration=Duration(1, 4),
        minimum_written_pitch=pitchtools.NamedChromaticPitch('c'),
        maximum_written_pitch=pitchtools.NamedChromaticPitch("c''''"),
        )

    assert wizard.target == handler
