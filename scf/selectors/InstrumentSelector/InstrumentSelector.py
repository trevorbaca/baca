from scf.selectors.Selector import Selector


class InstrumentSelector(Selector):

    def __init__(self, instruments=None, session=None):
        Selector.__init__(self, session=session)
        self.instruments = instruments or []

    ### CLASS ATTRIBUTES ###

    target_human_readable_name = 'instrument'

    ### PUBLIC METHODS ###

    def make_menu_tokens(self, head=None):
        tokens = []
        for instrument in self.instruments:
            token = (None, self.get_one_line_menuing_summary(instrument), None, instrument)
            tokens.append(token)
        return tokens
