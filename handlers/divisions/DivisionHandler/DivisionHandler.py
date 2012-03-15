from abc import ABCMeta
from abc import abstractmethod
from abjad.tools import durationtools
from abjad.tools import pitchtools
from handlers.Handler import Handler


class DivisionHandler(Handler):

    ### CLASS ATTRIBUTES ##

    __metaclass__ = ABCMeta

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self):
        pass

    ### PRIVATE READ-ONLY ATTRIBUTES ###

    @property
    def _tools_package(self):
        return 'handlers.divisions'
