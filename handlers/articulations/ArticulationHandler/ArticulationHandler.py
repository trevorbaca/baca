from abc import ABCMeta
from abc import abstractmethod
from abjad.tools import durationtools
from abjad.tools import pitchtools
from experimental.tools.handlertools.Handler import Handler


class ArticulationHandler(Handler):

    ### CLASS ATTRIBUTES ##

    __metaclass__ = ABCMeta

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self, 
        minimum_duration=None, 
        maximum_duration=None,
        minimum_written_pitch=None, 
        maximum_written_pitch=None):
        if minimum_duration is None:
            self.minimum_duration = minimum_duration
        else:
            self.minimum_duration = durationtools.Duration(
                *durationtools.duration_token_to_duration_pair(minimum_duration))
        if maximum_duration is None:
            self.maximum_duration = maximum_duration
        else:
            self.maximum_duration = durationtools.Duration(
                *durationtools.duration_token_to_duration_pair(maximum_duration))
        if minimum_written_pitch is None:
            self.minimum_written_pitch = minimum_written_pitch
        else:
            self.minimum_written_pitch = pitchtools.NamedChromaticPitch(minimum_written_pitch)
        if maximum_written_pitch is None:
            self.maximum_written_pitch = maximum_written_pitch
        else:
            self.maximum_written_pitch = pitchtools.NamedChromaticPitch(maximum_written_pitch)

    ### PRIVATE READ-ONLY ATTRIBUTES ###

    @property
    def _tools_package_name(self):
        return 'handlertools.articulations'
