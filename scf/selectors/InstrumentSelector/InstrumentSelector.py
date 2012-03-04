from scf.selectors.Selector import Selector


class InstrumentSelector(Selector):

    def __init__(self, instruments=None, session=None):
        Selector.__init__(self, session=session)
        self.instruments = instruments or []

    ### CLASS ATTRIBUTES ###

    target_human_readable_name = 'instrument'

    ### PUBLIC METHODS ###

    def list_target_items(self):
        return self.instruments[:]
