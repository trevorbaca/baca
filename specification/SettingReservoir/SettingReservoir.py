from abjad.tools.abctools.AbjadObject import AbjadObject


class SettingReservoir(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, settings=None):
        self.settings = settings or []

    ### PUBLIC METHODS ###

    def get_setting(self, 
        attribute_name=None, context_name=None, persistent=None, scope=None, segment_name=None):
        settings = self.get_settings(attribute_name=attribute_name, 
            context_name=context_name, persistent=persistent, scope=scope, segment_name=segment_name)
        if not settings:
            raise Exception(
                'no settings for {!r} found in segment {!r}.'.format(attribute_name, segment_name))
        elif 1 < len(settings):
            raise Exception(
                'multiple settings for {!r} found in segment {!r}.'.format(attribute_name, segment_name))
        assert len(settings) == 1
        return settings[0]

    def get_settings(self, 
        attribute_name=None, context_name=None, persistent=None, scope=None, segment_name=None):
        settings = []
        for setting in self.settings:
            if (
                (attribute_name is None or setting.attribute_name == attribute_name) and
                (context_name is None or setting.context_name == context_name) and
                (persistent is None or setting.persistent == persistent) and
                (scope is None or setting.scope == scope) and
                (segment_name is None or setting.segment_name == segment_name)):
                settings.append(setting)
        return settings
