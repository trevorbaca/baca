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
            if self._items:
                return self._items
            else:
                return self.instruments
        def fset(self, items):
            self._items = items
        return property(**locals())
