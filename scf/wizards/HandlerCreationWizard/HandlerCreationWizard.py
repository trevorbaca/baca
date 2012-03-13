from abc import ABCMeta
from abc import abstractmethod
from scf.wizards.Wizard import Wizard


class HandlerCreationWizard(Wizard):

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### PUBLIC METHODS ###

    @abstractmethod
    def get_handler_editor(self):
        pass
