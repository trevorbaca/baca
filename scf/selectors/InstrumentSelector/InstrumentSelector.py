from scf.selectors.Selector import Selector


class InstrumentSelector(Selector):

    def __init__(self, instruments=None, session=None):
        Selector.__init__(self, session=session)
        self.instruments = instruments or []

    ### CLASS ATTRIBUTES ###

    target_human_readable_name = 'instrument'

    ### READ / WRITE ATTRIBUTES ###

    @apply
    def items():
        def fget(self):
            return self.instruments
        def fset(self, items):
            self._instruments = items
        return property(**locals())
