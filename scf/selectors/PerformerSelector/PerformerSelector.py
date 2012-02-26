from scf.selectors.Selector import Selector


class PerformerSelector(Selector):

    def __init__(self, session=None):
        Selector.__init__(self, session=session)

    ### PUBLIC METHODS ###

    def handle_main_menu_result(self, result):
        self.print_not_yet_implemented()

    def make_main_menu(self):
        self.print_not_yet_implemented()
