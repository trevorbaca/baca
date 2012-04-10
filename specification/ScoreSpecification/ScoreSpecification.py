from abjad.tools import contexttools
from abjad.tools.abctools.AbjadObject import AbjadObject
from baca.specification.SegmentSpecification import SegmentSpecification
from baca.specification.Selection import Selection
from baca.specification.StatalServerRequest import StatalServerRequest
from baca.specification.SettingReservoirs import SettingReservoirs


class ScoreSpecification(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, score_template, context_name_abbreviations=None, 
        segment_specification_class=None, segments=None, settings=None):
        self.context_name_abbreviations = context_name_abbreviations or {}
        self.score_template = score_template
        self.segment_specification_class = segment_specification_class or SegmentSpecification
        self.segments = segments or []
        self.settings = settings or []
        self.initialize_context_name_abbreviations()
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
                    raise KeyError

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

    def get_settings(self, segment_name=None, context_name=None, attribute_name=None, persistent=None):
        settings = []
        for setting in self.settings:
            if ((segment_name is None or setting.segment_name == segment_name) and 
                (context_name is None or setting.context_name == context_name) and
                (attribute_name is None or setting.attribute_name == attribute_name) and
                (persistent is None or setting.persistent == persistent)):
                settings.append(setting)
        return settings

    def initialize_context_name_abbreviations(self):
        for context_name_abbreviation, context_name in self.context_name_abbreviations.iteritems():
            setattr(self, context_name_abbreviation, context_name)

    def initialize_contexts(self):
        self.contexts = {}
        score = self.score_template()
        for context in contexttools.iterate_contexts_forward_in_expr(score):
            assert context.name is not None
            self.contexts[context.name] = {}

    def interpret_segment(self, segment):
        time_signatures = self.resolve_attribute(segment.name, None, None, 'time_signatures')

    def interpret_segment_attribute_directives(self, segment, attribute_name):
        directives = segment.get_directives(attribute_name=attribute_name)
        reservoir = getattr(self.reservoirs, attribute_name)
        for directive in directives:
            source_value = self.resolve_directive_source_value(directive.source)
            reservoir.store_settings(directive.target_selection, source_value, directive.is_persistent)

    def interpret_segments(self):
        self.unpack_settings()
        for segment in self.segments:
            self.interpret_segment(segment)

    def resolve_attribute(self, segment_name, context_name, scope, attribute_name):
        segment = self[segment_name]
        settings = segment.get_settings(context_name=context_name, scope=scope, attribute_name=attribute_name)
        
    def resolve_directive_source_value(self, directive_source):
        if isinstance(directive_source, Selection):
            raise NotImplementedError(repr(directive_source))
        elif isinstance(directive_source, StatalServerRequest):
            return directive_source()
        else:
            return directive_source

    def resolve_segment_time_signatures(self, segment):
        settings = segment.get_settings(attribute_name='time_signatures')
        if settings:
            assert len(settings) == 1
            setting = settings[0]
            assert setting.context_name is None
            assert setting.scope is None
            value = self.resolve_source(setting.source)
            #self.reservoirs.time_signatures.

    def unpack_settings(self):
        for segment in self.segments:
            self.settings.extend(segment.unpack_settings())
