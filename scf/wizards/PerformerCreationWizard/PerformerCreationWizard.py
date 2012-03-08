from abjad.tools import scoretools
from scf import selectors
from scf.wizards.Wizard import Wizard


class PerformerCreationWizard(Wizard):

    def __init__(self, is_ranged=False, session=None, target=None):
        Wizard.__init__(self, session=session, target=target)
        self.is_ranged = is_ranged

    ### READ-ONLY ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'instrument creation wizard'

    ### PUBLIC METHODS ###

    def initialize_performer_interactively(self, performer_name):
        from scf import editors
        performer = scoretools.Performer(performer_name)
        performer_editor = editors.PerformerEditor(session=self.session, target=performer)
        self.push_breadcrumb('add performers')
        performer_editor.set_initial_configuration_interactively()
        self.pop_breadcrumb()
        if self.backtrack():
            return
        else:
            return performer
        
    def run(self, cache=False, clear=True, head=None, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        try_again = False
        performers = []
        while True:
            self.push_breadcrumb()
            kwargs = {'session': self.session, 'is_ranged': self.is_ranged}
            selector = selectors.ScoreToolsPerformerNameSelector(**kwargs)
            self.push_backtrack()
            result = selector.run()
            self.pop_backtrack()
            if self.backtrack():
                break
            if isinstance(result, list):
                performer_names = result
            else:
                performer_names = [result]
            performers = []
            for performer_name in performer_names:
                self.push_breadcrumb()
                self.push_backtrack()
                performer = self.initialize_performer_interactively(performer_name)
                self.pop_backtrack()
                self.pop_breadcrumb()
                was_backtracking_locally = self.session.is_backtracking_locally
                if self.backtrack():
                    if was_backtracking_locally:
                        try_again = True
                    else:
                        try_again = False
                        performers = []
                    break
                performers.append(performer)
            if not try_again:
                break
            else:
                try_again = False
                self.pop_breadcrumb()
        if self.is_ranged and performers:
            final_result = performers[:]
        elif self.is_ranged and not performers:
            final_result = []
        elif not self.is_ranged and performers:
            final_result = performers[0]
        elif not self.is_ranged and not performers:
            final_result = None
        else:
            raise ValueError
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)
        return final_result
