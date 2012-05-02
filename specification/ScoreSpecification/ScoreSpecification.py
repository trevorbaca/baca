from abjad.tools import contexttools
from baca.specification.AttributeRetrievalIndicator import AttributeRetrievalIndicator
from baca.specification.SegmentSpecification import SegmentSpecification
from baca.specification.Selection import Selection
from baca.specification.Specification import Specification
from baca.specification.StatalServerRequest import StatalServerRequest
from baca.specification.SettingReservoir import SettingReservoir


class ScoreSpecification(Specification):

    ### INITIALIZER ###

    def __init__(self, score_template, segment_specification_class=None, segments=None, settings=None):
        Specification.__init__(self, settings=settings)
        self.score_template = score_template
        self.segment_specification_class = segment_specification_class or SegmentSpecification
        self.segments = segments or []
        self.persistent_settings = SettingReservoir()
        self.initialize_contexts()

    ### SPECIAL METHODS ###

    def __getitem__(self, arg):
        if isinstance(arg, int):
            return self.segments[arg]
        elif isinstance(arg, str):
            for segment in self.segments:
                if segment.name == arg:
                    return segment
            else:
                raise KeyError(repr(arg))

    def __getslice__(self, start, stop):
        return self.segments.__getslice__(start, stop)

    def __len__(self):
        return len(self.segments)

    def __repr__(self):
        return '{}({!r})'.format(type(self).__name__, self.segments)

    ### PUBLIC METHODS ###
    
    def append_segment(self, name=None):
        segment = self.segment_specification_class(self.score_template(), name=name)     
        self.segments.append(segment)
        return segment

    def initialize_contexts(self):
        self.contexts = {}
        score = self.score_template()
        for context in contexttools.iterate_contexts_forward_in_expr(score):
            assert context.name is not None
            self.contexts[context.name] = {}

    def interpret_additional_segment_parameters(self, segment):
        pass

    def interpret_segment(self, segment):
        self.interpret_segment_time_signatures(segment)
        self.interpret_segment_rhythmic_divisions(segment)
        self.interpret_segment_rhythms(segment)
        self.interpret_segment_pitch_classes(segment)
        self.interpret_segment_registration(segment)
        self.interpret_additional_segment_parameters(segment)

    def interpret_segment_pitch_classes(self, segment):
        pass

    def interpret_segment_registration(self, segment):
        pass

    def interpret_segment_rhythmic_divisions(self, segment):
        pass

    def interpret_segment_rhythms(self, segment):
        pass

    def interpret_segment_time_signatures(self, segment):
        settings = segment.get_settings(attribute_name='time_signatures')
        if not settings:
            settings = self.persistent_settings.get_settings(attribute_name='time_signatures')
        assert len(settings) == 1
        setting = settings[0]
        assert setting.context_name is None
        assert setting.scope is None
        self.store_setting(setting)

    def interpret_segments(self):
        self.unpack_directives()
        for segment in self.segments:
            self.interpret_segment(segment)

    def resolve_setting_source(self, setting_source):
        if isinstance(setting_source, Selection):
            raise NotImplementedError(repr(setting_source))
        elif isinstance(setting_source, StatalServerRequest):
            return setting_source()
        else:
            return setting_source

    def retrieve(self, segment_name, attribute_name, context_names=None, scope=None):
        selection = self.select(segment_name, context_names=context_names, scope=scope)
        return AttributeRetrievalIndicator(selection, attribute_name)

    def select(self, segment_name, context_names=None, scope=None):
        return Selection(segment_name, context_names=context_names, scope=scope)

    def store_persistent_setting(self, setting):
        if not setting.persistent:
            return
        raise NotImplementedError

    def store_setting(self, setting):
        self.store_setting_in_context_tree(setting)
        self.store_persistent_setting(setting)

    def store_setting_in_context_tree(self, setting):
        segment = self[setting.segment_name]
        context_name = setting.context_name or segment.score_context_name
        setting_value = self.resolve_setting_source(setting.source)
        print setting_value
        scoped_value = (setting_value, setting.scope) # TODO: implement ScopeValue class
        segment.contexts[context_name][setting.attribute_name] = scoped_value

    def unpack_directives(self):
        for segment in self.segments:
            self.settings.extend(segment.unpack_directives())
