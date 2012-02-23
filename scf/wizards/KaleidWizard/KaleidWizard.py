from scf.wizards.Wizard import Wizard
from scf import selectors


class KaleidWizard(Wizard):

    ### READ-ONLY ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'kaleid creation wizard'

    ### PUBLIC METHODS ###

    def get_kaleid_editor(self, kaleid_class_name, target=None):
        wizard_class_name = '{}KaleidEditor'.format(kaleid_class_name)
        command = 'from scf.editors import {} as kaleid_editor_class'.format(wizard_class_name)
        exec(command)
        kaleid_editor = kaleid_editor_class(session=self.session, target=target)
        return kaleid_editor

    def run(self, cache=False, clear=True, head=None, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        self.push_breadcrumb()
        selector = selectors.KaleidSelector(session=self.session)
        kaleid_class_name = selector.run()
        if not self.backtrack():
            kaleid_editor = self.get_kaleid_editor(kaleid_class_name) 
            kaleid_editor.run(is_autoadvancing=True)
            self.target = kaleid_editor.target
        self.pop_breadcrumb() 
        self.restore_breadcrumbs(cache=cache) 
