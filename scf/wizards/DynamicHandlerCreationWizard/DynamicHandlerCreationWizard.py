from scf import selectors
from scf.wizards.HandlerCreationWizard import HandlerCreationWizard


class DynamicHandlerCreationWizard(HandlerCreationWizard):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def breadcrumb(self):
        return 'dynamic handler creation wizard'

    ### PUBLIC METHODS ###

    def get_handler_editor(self):
        pass
