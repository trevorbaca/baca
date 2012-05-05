from abjad.tools import contexttools
from abjad.tools import sequencetools
from baca.specification.AttributeRetrievalIndicator import AttributeRetrievalIndicator
from baca.specification.AttributeRetrievalRequest import AttributeRetrievalRequest
from baca.specification.ContextTree import ContextTree
from baca.specification.ScopedValue import ScopedValue
from baca.specification.SegmentSpecification import SegmentSpecification
from baca.specification.Selection import Selection
from baca.specification.Specification import Specification
from baca.specification.StatalServerRequest import StatalServerRequest
from baca.specification.SettingReservoir import SettingReservoir
import copy


class ScoreSpecification(Specification):

    ### INITIALIZER ###

    def __init__(self, score_template, segment_specification_class=None, segments=None, settings=None):
        Specification.__init__(self, settings=settings)
        self.score_template = score_template
        self.segment_specification_class = segment_specification_class or SegmentSpecification
        self.segments = segments or []
        self.context_tree = ContextTree(self.score_template()) 

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

    def change_attribute_retrieval_indicator_to_setting(self, indicator):
        segment = self[indicator.segment_name]
        context_proxy = segment.context_tree[indicator.context_name]
        setting = context_proxy.get_setting(attribute_name=indicator.attribute_name, scope=indicator.scope)
        return setting

    def interpret(self):
        self.unpack_directives()
        self.interpret_segment_time_signatures()
        self.interpret_segment_divisions()
        self.interpret_segment_rhythm()
        self.interpret_segment_pitch_classes()
        self.interpret_segment_registration()
        self.interpret_additional_segment_parameters()

    def interpret_additional_segment_parameters(self):
        for segment in self.segments:
            pass

    def interpret_segment_divisions(self):
        for segment in self.segments:
            settings = segment.get_settings(attribute_name='divisions')
            if not settings:
                settings = self.context_tree.get_settings(attribute_name='divisions')
            self.store_settings(settings)

    def interpret_segment_pitch_classes(self):
        for segment in self.segments:
            pass

    def interpret_segment_registration(self):
        for segment in self.segments:
            pass

    def interpret_segment_rhythm(self):
        for segment in self.segments:
            settings = segment.get_settings(attribute_name='rhythm')
            if not settings:
                settings = self.context_tree.get_settings(attribute_name='rhythm')
            self.store_settings(settings)

    def interpret_segment_time_signatures(self):
        for segment in self.segments:
            settings = segment.get_settings(attribute_name='time_signatures')
            if not settings:
                settings = self.context_tree.get_settings(attribute_name='time_signatures')
            assert len(settings) == 1
            setting = settings[0]
            assert setting.context_name is None
            assert setting.scope is None
            self.store_setting(setting)

    def notate(self):
        segment_score_objects = []
        self.interpret()
        for segment in self:
            segment_score_objects.append(segment.notate())
        return segment_score_objects

    def resolve_attribute_retrieval_request(self, request):
        setting = self.change_attribute_retrieval_indicator_to_setting(request.indicator)
        value = setting.value
        assert value is not None
        if request.offset is not None or request.count is not None:
            original_value_type = type(value)
            offset = request.offset or 0
            count = request.count or 0
            value = sequencetools.CyclicTuple(value)
            if offset < 0:
                offset = len(value) - -offset
            result = value[offset:offset+count]
            result = original_value_type(result)
        else:
            result = value
        return result

    def resolve_setting(self, setting):
        resolved_setting = copy.deepcopy(setting)
        value = self.resolve_setting_source(setting)
        resolved_setting.value = value
        return resolved_setting

    def resolve_setting_source(self, setting):
        if isinstance(setting.source, AttributeRetrievalRequest):
            return self.resolve_attribute_retrieval_request(setting.source)
        elif isinstance(setting.source, StatalServerRequest):
            return setting.source()
        else:
            return setting.source

    def retrieve(self, attribute_name, segment_name, context_name=None, scope=None):
        indicator = AttributeRetrievalIndicator(
            attribute_name, segment_name, context_name=context_name, scope=scope)
        return indicator

    def select(self, segment_name, context_names=None, scope=None):
        return Selection(segment_name, context_names=context_names, scope=scope)

    def store_setting(self, setting):
        segment = self[setting.segment_name]
        context_name = setting.context_name or segment.context_tree.score_name
        resolved_setting = self.resolve_setting(setting)
        segment.context_tree[context_name][setting.attribute_name] = resolved_setting
        if setting.persistent:
            self.context_tree[context_name][setting.attribute_name] = resolved_setting

    def store_settings(self, settings):
        for setting in settings:
            self.store_setting(setting)

    def unpack_directives(self):
        for segment in self.segments:
            self.settings.extend(segment.unpack_directives())
