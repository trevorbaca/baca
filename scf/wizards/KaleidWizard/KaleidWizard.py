from scf.core.SCFObject import SCFObject
from scf.wizards.Wizard import Wizard
from scf import selectors


class KaleidWizard(Wizard):

    ### READ-ONLY ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'kaleid wizard'

    ### PUBLIC METHODS ###

    def get_kaleid_wizard(self, kaleid_class_name):
        pass

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
            #kaleid_wizard = self.get_kaleid_wizard(kaleid_class_name) 
            #kaleid = kaleid_wizard.run()
            break
        self.pop_breadcrumb() 
        self.restore_breadcrumbs(cache=cache) 
        #return kaleid
        #self.target = kaleid
