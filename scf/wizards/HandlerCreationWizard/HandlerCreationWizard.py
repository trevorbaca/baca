from abc import ABCMeta
from abc import abstractmethod
from scf.wizards.Wizard import Wizard


class HandlerCreationWizard(Wizard):

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### PUBLIC METHODS ###

    def get_handler_editor(self, handler_class_name, target=None):
        handler_editor_class_name = '{}KaleidEditor'.format(handler_class_name)
        command = 'from scf.editors import {} as handler_editor_class'.format(handler_editor_class_name)
        exec(command)
        handler_editor = handler_editor_class(session=self.session, target=target)
        return handler_editor
