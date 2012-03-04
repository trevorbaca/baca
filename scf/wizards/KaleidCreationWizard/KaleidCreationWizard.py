from scf import selectors
from scf.wizards.HandlerCreationWizard import HandlerCreationWizard


class KaleidCreationWizard(HandlerCreationWizard):

    ### CLASS ATTRIBUTES ###

    handler_class_name_selector = selectors.KaleidClassNameSelector
    handler_editor_class_name_suffix = 'KaleidEditor'

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def breadcrumb(self):
        return 'kaleid creation wizard'
