from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.abctools.AbjadObject import AbjadObject


class Specification(AbjadObject):

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### INITIALIZER ###
    
    @abstractmethod
    def __init__(self, settings=None):
        self.settings = settings or []

    ### PUBLIC METHODS ###

    def get_setting(
        self, segment_name=None, context_name=None, attribute_name=None, persistent=None, scope=None):
        settings = self.get_settings(segment_name=segment_name, context_name=context_name,
            attribute_name=attribute_name, persistent=persistent, scope=scope)
        if not settings:
            raise Exception(
                'no settings for {!r} found in segment {!r}.'.format(attribute_name, segment_name))
        elif 1 < len(settings):
            raise Exception(
                'multiple settings for {!r} found in segment {!r}.'.format(attribute_name, segment_name))
        assert len(settings) == 1
        return settings[0]

    def get_settings(self,
        segment_name=None, context_name=None, attribute_name=None, persistent=None, scope=None):
        settings = []
        for setting in self.settings:
            if ((segment_name is None or setting.segment_name == segment_name) and
                (context_name is None or setting.context_name == context_name) and
                (attribute_name is None or setting.attribute_name == attribute_name) and
                (persistent is None or setting.persistent == persistent) and
                (scope is None or setting.scope == scope)):
                settings.append(setting)
        return settings
