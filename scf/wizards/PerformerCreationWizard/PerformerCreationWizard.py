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
        self.push_backtrack()
        performer_editor.set_initial_configuration_interactively()
        self.pop_backtrack()
        self.pop_breadcrumb()
        return performer
        
    def run(self, cache=False, clear=True, head=None, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        self.push_breadcrumb()
        kwargs = {'session': self.session, 'is_ranged': self.is_ranged}
        selector = selectors.ScoreToolsPerformerNameSelector(**kwargs)
        self.push_backtrack()
        result = selector.run()
        self.pop_backtrack()
        if self.backtrack():
            self.pop_breadcrumb()
            self.restore_breadcrumbs(cache=cache)
            return
        if isinstance(result, list):
            performer_names = result
        else:
            performer_names = [result]
        performers = []
        for performer_name in performer_names:
            self.push_breadcrumb()
            performer = self.initialize_performer_interactively(performer_name)
            self.pop_breadcrumb()
            if self.backtrack():
                continue
            performers.append(performer)
        if self.is_ranged:
            result = performers[:]
        else:
            result = performers[0]
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)
        return result
