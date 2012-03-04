from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty
from scf.core.SCFObject import SCFObject


class Wizard(SCFObject):

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        SCFObject.__init__(self, session=session)
        self.target = target
    
    ### READ-ONLY PUBLIC PROPERTIES ###

    @abstractproperty
    def breadcrumb(self):
        pass

    ### PUBLIC METHODS ###

    @abstractmethod
    def run(self, cache=False, clear=True, head=None, user_input=None):
        pass
