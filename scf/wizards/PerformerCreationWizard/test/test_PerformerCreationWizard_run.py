from abjad import *
import scf


def test_PerformerCreationWizard_run_01():

    wizard = scf.wizards.PerformerCreationWizard()
    assert wizard.run(user_input='q') is None

    wizard = scf.wizards.PerformerCreationWizard()
    assert wizard.run(user_input='b') is None

    wizard = scf.wizards.PerformerCreationWizard()
    assert wizard.run(user_input='studio') is None


def test_PerformerCreationWizard_run_02():

    wizard = scf.wizards.PerformerCreationWizard()
    assert wizard.run(user_input='vn default') == scoretools.Performer(
        name='violinist', instruments=[instrumenttools.Violin()])


def test_PerformerCreationWizard_run_03():
    '''Ranged.
    '''

    wizard = scf.wizards.PerformerCreationWizard(is_ranged=True)
    assert wizard.run(user_input='vn, va 1 1') == [
        scoretools.Performer(name='violinist', instruments=[instrumenttools.Violin()]),
        scoretools.Performer(name='violist', instruments=[instrumenttools.Viola()])]
