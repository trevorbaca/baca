from scf import selectors
from scf.wizards.HandlerCreationWizard import HandlerCreationWizard


class DynamicHandlerCreationWizard(HandlerCreationWizard):

    ### CLASS ATTRIBUTES ###

    handler_class_name_selector = selectors.DynamicHandlerClassNameSelector
    handler_editor_class_name_suffix = 'DynamicHandlerEditor'

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def breadcrumb(self):
        return 'dynamic handler creation wizard'
