from abjad.tools import contexttools
from baca.specification.AttributeRetrievalIndicator import AttributeRetrievalIndicator
from baca.specification.SegmentSpecification import SegmentSpecification
from baca.specification.Selection import Selection
from baca.specification.Specification import Specification
from baca.specification.StatalServerRequest import StatalServerRequest
from baca.specification.SettingReservoirs import SettingReservoirs


class ScoreSpecification(Specification):

    ### INITIALIZER ###

    def __init__(self, score_template, segment_specification_class=None, segments=None, settings=None):
        Specification.__init__(self, settings=settings)
        self.score_template = score_template
        self.segment_specification_class = segment_specification_class or SegmentSpecification
        self.segments = segments or []
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
        time_signatures = self.resolve_attribute(segment, 'time_signatures')
        print time_signatures

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

    def resolve_attribute(self, segment, attribute_name, **kwargs):
        settings = segment.get_settings(attribute_name=attribute_name, **kwargs)
        if not settings:
            #self.
            pass
        return settings
        
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

    def retrieve(self, segment_name, attribute_name, context_names=None, scope=None):
        selection = self.select(segment_name, context_names=context_names, scope=scope)
        return AttributeRetrievalIndicator(selection, attribute_name)

    def select(self, segment_name, context_names=None, scope=None):
        return Selection(segment_name, context_names=context_names, scope=scope)

    def unpack_settings(self):
        for segment in self.segments:
            self.settings.extend(segment.unpack_settings())
