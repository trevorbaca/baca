from scf.wizards.Wizard import Wizard
from scf import selectors


class KaleidWizard(Wizard):

    ### READ-ONLY ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'kaleid wizard'

    ### PUBLIC METHODS ###

    def get_kaleid_editor(self, kaleid_class_name):
        wizard_class_name = '{}KaleidEditor'.format(kaleid_class_name)
        command = 'from scf.editors import {} as kaleid_editor_class'.format(wizard_class_name)
        exec(command)
        kaleid_editor = kaleid_editor_class(session=self.session)
        return kaleid_editor

    def run(self, cache=False, clear=True, head=None, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.push_breadcrumb()
            selector = selectors.KaleidSelector(session=self.session)
            kaleid_class_name = selector.run()
            if self.backtrack():
                break
            self.debug(kaleid_class_name)
            #kaleid_editor = self.get_kaleid_editor(kaleid_class_name) 
            #kaleid = kaleid_editor.run()
            break
        self.pop_breadcrumb() 
        self.restore_breadcrumbs(cache=cache) 
        #return kaleid
        #self.target = kaleid
