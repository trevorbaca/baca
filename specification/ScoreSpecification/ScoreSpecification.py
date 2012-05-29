from abjad.tools import *
from baca.specification.AttributeRetrievalRequest import AttributeRetrievalRequest
from baca.specification.ContextTree import ContextTree
from baca.specification.DivisionsRetrievalRequest import DivisionsRetrievalRequest
from baca.specification.ScopedValue import ScopedValue
from baca.specification.SegmentSpecification import SegmentSpecification
from baca.specification.Selection import Selection
from baca.specification.Specification import Specification
from baca.specification.StatalServerRequest import StatalServerRequest
from baca.specification.SettingReservoir import SettingReservoir
import collections
import copy


Token = collections.namedtuple('Token', ['value', 'duration'])
VerboseToken = collections.namedtuple('VerboseToken', ['value', 'fresh', 'duration'])
RhythmToken = collections.namedtuple('RhythmToken', ['value', 'fresh'])

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
        return '{}({!r})'.format(self._class_name, self.segments)

    ### PUBLIC METHODS ###

    def add_divisions(self):
        for voice in voicetools.iterate_voices_forward_in_expr(self.score):
            divisions = self.make_divisions_for_voice(voice)
            marktools.Annotation('divisions', divisions)(voice)

    def add_rhythms(self):
        for voice in voicetools.iterate_voices_forward_in_expr(self.score):
            self.add_rhythms_to_voice(voice)

    def add_rhythms_to_voice(self, voice):
        mapping = []
        for segment in self.segments:
            value, fresh = segment.get_rhythm_value(voice.name)
            mapping.append(RhythmToken(value, fresh))
        result = []
        parts = self.partition_voice_divisions_by_segment_durations(voice)
        mapping, parts = self.massage_rhythm_mapping_and_parts(mapping, parts)
        for token, part in zip(mapping, parts):
            maker = token.value
            assert isinstance(maker, timetokentools.TimeTokenMaker)
            leaf_lists = maker(part)
            containers = [containertools.Container(x) for x in leaf_lists]
            voice.extend(containers)
            if getattr(maker, 'beam', False):
                durations = [x.preprolated_duration for x in containers]
                beamtools.DuratedComplexBeamSpanner(containers, durations=durations, span=1)

    def add_time_signatures(self):
        for segment in self.segments:
            segment.add_time_signatures(self.score)

    def append_segment(self, name=None):
        segment = self.segment_specification_class(self.score_template, name=name)     
        self.segments.append(segment)
        return segment

    def apply_segment_pitch_classes(self):
        pass

    def apply_segment_registration(self):
        pass

    def apply_additional_segment_parameters(self):
        pass 

    def calculate_segment_offset_pairs(self):
        segment_durations = [segment.duration for segment in self]
        assert sequencetools.all_are_numbers(segment_durations)
        self.segment_durations = segment_durations
        self.score_duration = sum(self.segment_durations)
        self.segment_offset_pairs = mathtools.cumulative_sums_zero_pairwise(self.segment_durations)
    
    def change_attribute_retrieval_indicator_to_setting(self, indicator):
        segment = self[indicator.segment_name]
        context_proxy = segment.context_tree[indicator.context_name]
        setting = context_proxy.get_setting(attribute_name=indicator.attribute_name, scope=indicator.scope)
        return setting

    def handle_divisions_retrieval_request(self, request):
        voice = componenttools.get_first_component_in_expr_with_name(self.score, request.voice_name)
        assert isinstance(voice, voicetools.Voice), voice
        divisions = marktools.get_value_of_annotation_attached_to_component(voice, 'divisions')
        assert isinstance(divisions, list), divisions
        start_offset, stop_offset = self.segment_name_to_offsets(request.start_segment_name, n=request.n)
        total_amount = stop_offset - start_offset
        divisions = [mathtools.NonreducedFraction(x) for x in divisions]
        divisions = sequencetools.split_sequence_once_by_weights_with_overhang(divisions, [0, total_amount])
        divisions = divisions[1]
        if request.callback is not None:
            divisions = request.callback(divisions)
        divisions = self.apply_offset_and_count(request, divisions)
        return divisions

    def request_divisions(self, voice_name, start_segment_name, n=1):
        return DivisionsRetrievalRequest(voice_name, start_segment_name, n=n)

    def segment_name_to_offsets(self, segment_name, n=1):
        start_segment_index = self.segment_name_to_index(segment_name)        
        stop_segment_index = start_segment_index + n - 1
        start_offset_pair = self.segment_offset_pairs[start_segment_index]
        stop_offset_pair = self.segment_offset_pairs[stop_segment_index]
        return start_offset_pair[0], stop_offset_pair[1]

    def segment_name_to_index(self, segment_name):
        segment = self[segment_name]
        return self.index(segment)

    def index(self, segment):
        return self.segments.index(segment)

    def instantiate_score(self):
        self.score = self.score_template()
        context = contexttools.Context(name='TimeSignatureContext', context_name='TimeSignatureContext')
        self.score.insert(0, context)
        
    def interpret(self):
        self.instantiate_score()
        self.unpack_directives()
        self.interpret_segment_time_signatures()
        self.add_time_signatures()
        self.calculate_segment_offset_pairs()
        self.interpret_segment_divisions()
        self.add_divisions()
        self.interpret_segment_rhythms()
        self.add_rhythms()
        self.interpret_segment_pitch_classes()
        self.apply_segment_pitch_classes()
        self.interpret_segment_registration()
        self.apply_segment_registration()
        self.interpret_additional_segment_parameters()
        self.apply_additional_segment_parameters()
        return self.score

    def interpret_additional_segment_parameters(self):
        for segment in self.segments:
            pass

    def interpret_segment_divisions(self):
        for segment in self.segments:
            settings = segment.get_settings(attribute_name='divisions')
            if not settings:
                settings = []
                existing_settings = self.context_tree.get_settings(attribute_name='divisions')
                for existing_setting in existing_settings:
                    setting = existing_setting.copy(segment_name=segment.name, fresh=False)
                    settings.append(setting)
            self.store_settings(settings)

    def interpret_segment_pitch_classes(self):
        for segment in self.segments:
            pass

    def interpret_segment_registration(self):
        for segment in self.segments:
            pass

    def interpret_segment_rhythms(self):
        for segment in self.segments:
            settings = segment.get_settings(attribute_name='rhythm')
            if not settings:
                settings = []
                existing_settings = self.context_tree.get_settings(attribute_name='rhythm')
                for existing_setting in existing_settings:
                    setting = existing_setting.copy(segment_name=segment.name, fresh=False)
                    settings.append(setting)
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

    def make_divisions_for_voice(self, voice):
        mapping = []
        self._debug('')
        self._debug(voice)
        for segment in self.segments:
            value, fresh = segment.get_divisions_value(voice.name)
            if isinstance(value, DivisionsRetrievalRequest):
                value = self.handle_divisions_retrieval_request(value)
            mapping.append(VerboseToken(value, fresh, segment.duration))
        print ''
        self._debug(mapping, 'mapping')
        mapping = self.massage_divisions_mapping(mapping)
        divisions = self.make_divisions_from_mapping(mapping)
        self._debug(divisions)
        return divisions

    def make_divisions_from_mapping(self, mapping):
        result = []
        for token in mapping:
            divisions = [mathtools.NonreducedFraction(x) for x in token.value]
            divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, token.duration)
            divisions = [x.pair for x in divisions]
            result.extend(divisions)
        return result

    def massage_divisions_mapping(self, mapping):
        if not mapping:
            return
        result = []
        assert mapping[0].fresh
        for verbose_token in mapping:
            if verbose_token.fresh:
                result.append(Token(verbose_token.value, verbose_token.duration))
            else:
                last_token = result[-1]
                assert verbose_token.value == last_token.value
                new_token = Token(last_token.value, last_token.duration + verbose_token.duration)
                result[-1] = new_token
        return result

    def massage_rhythm_mapping_and_parts(self, mapping, parts):
        if not mapping:
            return
        assert len(mapping) == len(parts)
        assert mapping[0].fresh
        new_mapping, new_parts = [mapping[0]], [parts[0][:]]
        for token, part in zip(mapping[1:], parts[1:]):
            if token.value == new_mapping[-1].value and not token.fresh:
                new_parts[-1].extend(part)
            else:
                new_mapping.append(token)
                new_parts.append(part[:])
        return new_mapping, new_parts

    def partition_voice_divisions_by_segment_durations(self, voice):
        divisions = marktools.get_value_of_annotation_attached_to_component(voice, 'divisions')
        divisions = [mathtools.NonreducedFraction(x) for x in divisions] 
        assert sum(divisions) == self.score_duration
        parts = sequencetools.partition_sequence_by_backgrounded_weights(divisions, self.segment_durations)
        return parts

    # TODO: ok to implement callback on attribute retrieval request;
    #       but what's really needed is callback on actual objects (like divisions)
    def resolve_attribute_retrieval_request(self, request):
        setting = self.change_attribute_retrieval_indicator_to_setting(request.indicator)
        value = setting.value
        assert value is not None, repr(value)
        if request.callback is not None:
            #self._debug(value, 'value before callback')
            value = request.callback(value)
            #self._debug(value, 'value after callback')
        result = self.apply_offset_and_count(request, value)
        return result

    def apply_offset_and_count(self, request, value):
        if request.offset is not None or request.count is not None:
            original_value_type = type(value)
            offset = request.offset or 0
            count = request.count or 0
            value = sequencetools.CyclicTuple(value)
            if offset < 0:
                offset = len(value) - -offset
            result = value[offset:offset+count]
            result = original_value_type(result)
            return result
        else:
            return value

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
