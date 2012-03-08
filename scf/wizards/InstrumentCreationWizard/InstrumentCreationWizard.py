from abjad.tools import instrumenttools
from scf.wizards.Wizard import Wizard
from scf import selectors


class InstrumentCreationWizard(Wizard):

    def __init__(self, is_ranged=False, session=None, target=None):
        Wizard.__init__(self, session=session, target=target)
        self.is_ranged = is_ranged
        
    ### READ-ONLY ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'instrument creation wiard'

    ### PUBLIC METHODS ###

    def change_instrument_name_to_instrument(self, instrument_name):
        instrument_name = instrument_name.title()
        instrument_name = instrument_name.replace(' ', '')
        command = 'instrument = instrumenttools.{}()'.format(instrument_name)
        exec(command)
        return instrument

    def name_untuned_percussion(self, instrument):
        if isinstance(instrument, instrumenttools.UntunedPercussion):
            selector = selectors.InstrumentToolsUntunedPercussionNameSelector(session=self.session)
            self.push_backtrack()
            instrument_name = selector.run()
            self.pop_backtrack()
            if self.backtrack():
                return
            instrument.instrument_name = instrument_name

    def run(self, cache=False, clear=True, head=None, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        self.push_breadcrumb()
        selector = selectors.InstrumentToolsInstrumentNameSelector(
            session=self.session, is_ranged=self.is_ranged)
        result = selector.run()
        if self.backtrack():
            return
        if isinstance(result, list):
            instrument_names = result
        else:
            instrument_names = [result]
        instruments = []
        for instrument_name in instrument_names:
            instrument = self.change_instrument_name_to_instrument(instrument_name)
            self.name_untuned_percussion(instrument)
            instruments.append(instrument)
        if self.is_ranged:
            result = instruments[:]
        else:
            result = instruments[0]
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)
        return result
