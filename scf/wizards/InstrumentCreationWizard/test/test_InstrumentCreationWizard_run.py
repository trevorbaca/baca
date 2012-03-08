from abjad.tools import instrumenttools
import scf


def test_InstrumentCreationWizard_run_01():

    wizard = scf.wizards.InstrumentCreationWizard()
    result = wizard.run(user_input='violin')
    violin = instrumenttools.Violin()
    assert result == violin


def test_InstrumentCreationWizard_run_02():

    wizard = scf.wizards.InstrumentCreationWizard()
    result = wizard.run(user_input='untuned vibraslap') 
    vibraslap = instrumenttools.UntunedPercussion()
    vibraslap.instrument_name = 'vibraslap'
    assert result == vibraslap


def test_InstrumentCreationWizard_run_03():

    wizard = scf.wizards.InstrumentCreationWizard(is_ranged=True)
    violin, viola = instrumenttools.Violin(), instrumenttools.Viola()
    result = wizard.run(user_input='violin, viola')
    result == [violin, viola]


#def test_InstrumentCreationWizard_run_04():
#    '''Eventually make this work.
#    '''
#
#    wizard = scf.wizards.InstrumentCreationWizard(is_ranged=True)
#    result = wizard.run(user_input='violin, viola, untuned vibraslap')
#    violin, viola = instrumenttools.Violin(), instrumenttools.Viola()
#    vibraslap = instrumenttools.UntunedPercussion()
#    vibraslap.instrument_name = 'vibraslap'
#    assert result == [violin, viola, vibraslap]
