from abjad.tools import contexttools
from baca.specification.AttributeRetrievalIndicator import AttributeRetrievalIndicator
from baca.specification.ContextTree import ContextTree
from baca.specification.ScopedValue import ScopedValue
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
        self.contexts = ContextTree(self.score_template()) 

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
        segment = self.segment_specification_class(self.score_template, name=name)     
        self.segments.append(segment)
        return segment

    def interpret(self):
        self.unpack_directives()
        self.interpret_segment_time_signatures()
        self.interpret_segment_rhythmic_divisions()
        self.interpret_segment_rhythms()
        self.interpret_segment_pitch_classes()
        self.interpret_segment_registration()
        self.interpret_additional_segment_parameters()

    def interpret_additional_segment_parameters(self):
        for segment in self.segments:
            pass

    def interpret_segment_pitch_classes(self):
        for segment in self.segments:
            pass

    def interpret_segment_registration(self):
        for segment in self.segments:
            pass

    def interpret_segment_rhythmic_divisions(self):
        for segment in self.segments:
            pass

    def interpret_segment_rhythms(self):
        for segment in self.segments:
            pass

    def interpret_segment_time_signatures(self):
        for segment in self.segments:
            settings = segment.get_settings(attribute_name='time_signatures')
            if not settings:
                settings = self.persistent_settings.get_settings(attribute_name='time_signatures')
            assert len(settings) == 1
            setting = settings[0]
            assert setting.context_name is None
            assert setting.scope is None
            self.store_setting(setting)

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

    def store_setting(self, setting):
        segment = self[setting.segment_name]
        context_name = setting.context_name or segment.contexts.score_name
        value = self.resolve_setting_source(setting.source)
        scoped_value = ScopedValue(value, setting.scope)
        segment.contexts[context_name][setting.attribute_name] = scoped_value
        if setting.persistent:
            self.contexts[context_name][setting.attribute_name] = scoped_value        

    def unpack_directives(self):
        for segment in self.segments:
            self.settings.extend(segment.unpack_directives())
