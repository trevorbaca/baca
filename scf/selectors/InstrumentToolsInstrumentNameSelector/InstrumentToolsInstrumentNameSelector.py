from abjad.tools import instrumenttools
from scf.selectors.Selector import Selector


class InstrumentToolsInstrumentNameSelector(Selector):

    ### CLASS ATTRIBUTES ###

    target_human_readable_name = 'instrument'

    ### PUBLIC METHODS ###

    def list_target_items(self):
        return instrumenttools.list_instrument_names()
