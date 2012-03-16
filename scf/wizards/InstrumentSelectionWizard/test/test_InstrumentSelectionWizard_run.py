from abjad import *
import scf


def test_InstrumentSelectionWizard_run_01():

    wizard = scf.wizards.InstrumentSelectionWizard()
    wizard.session.current_score_package_short_name = 'betoerung'
    
    assert wizard.run(user_input='hor') == instrumenttools.FrenchHorn()
    assert wizard.run(user_input='other xyl') == instrumenttools.Xylophone()


def test_InstrumentSelectionWizard_run_02():

    wizard = scf.wizards.InstrumentSelectionWizard()
    wizard.session.current_score_package_short_name = 'betoerung'
    whistle = instrumenttools.UntunedPercussion()
    whistle.instrument_name = 'whistle'

    assert wizard.run(user_input='other untuned whis') == whistle
