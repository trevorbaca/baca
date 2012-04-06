from scf import selectors
from scf.wizards.HandlerCreationWizard import HandlerCreationWizard


class TimeTokenMakerCreationWizard(HandlerCreationWizard):

    ### CLASS ATTRIBUTES ###

    handler_class_name_selector = selectors.KaleidClassNameSelector
    handler_editor_class_name_suffix = 'Editor'

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def breadcrumb(self):
        return 'kaleid creation wizard'
