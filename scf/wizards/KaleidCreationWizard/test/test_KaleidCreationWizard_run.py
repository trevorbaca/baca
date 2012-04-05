import handlers
import scf


def test_KaleidCreationWizard_run_01():

    wizard = scf.wizards.KaleidCreationWizard()
    wizard.run(user_input='patternedtokens [-1, 2, -3, 4] 16 [2, 3] [6] b')

    handler = handlers.kaleids.SignalFilledTimeTokenMaker(
        [-1, 2, -3, 4], 
        16,
        prolation_addenda=[2, 3],
        secondary_divisions=[6],
        )

    assert wizard.target == handler
