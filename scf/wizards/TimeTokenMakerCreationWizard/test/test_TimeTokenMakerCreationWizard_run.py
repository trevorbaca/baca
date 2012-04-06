from abjad.tools import timetokentools
import scf


def test_TimeTokenMakerCreationWizard_run_01():

    wizard = scf.wizards.TimeTokenMakerCreationWizard()
    wizard.run(user_input='signalfilledtimetokenmaker [-1, 2, -3, 4] 16 [2, 3] [6] b')

    maker = timetokentools.SignalFilledTimeTokenMaker(
        [-1, 2, -3, 4], 
        16,
        prolation_addenda=[2, 3],
        secondary_divisions=[6],
        )

    assert wizard.target == maker
