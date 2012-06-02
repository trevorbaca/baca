from abjad.tools import *
from baca.handlers.composites.CompositeRhythmHandler import CompositeRhythmHandler
from baca.handlers.pitch.TimewisePitchClassHandler import TimewisePitchClassHandler
from baca.specification.AttributeRetrievalIndicator import AttributeRetrievalIndicator
from baca.specification.AttributeRetrievalRequest import AttributeRetrievalRequest
from baca.specification.Callback import Callback
from baca.specification.ContextTree import ContextTree
from baca.specification.Directive import Directive
from baca.specification.DivisionRetrievalRequest import DivisionRetrievalRequest
from baca.specification.HandlerRequest import HandlerRequest
from baca.specification.Scope import Scope
from baca.specification.Specification import Specification
from baca.specification.Selection import Selection
from baca.specification.StatalServer import StatalServer
from baca.specification.StatalServerRequest import StatalServerRequest
from handlers.Handler import Handler
import copy
import fractions


class SegmentSpecification(Specification):

    ### INITIALIZER ###

    # store settings?
    # type- and form-check settings?
    def __init__(self, score_template, name, directives=None, settings=None):
        assert isinstance(name, str), name
        Specification.__init__(self, score_template, settings=settings)
        self._score_model = self.score_template()
        self._name = name
        self.directives = directives or []
        self.payload = ContextTree(self.score_template())

    ### SPECIAL METHODS ###

    def __getitem__(self, arg):
        if isinstance(arg, int):
            return self.directives.__getitem__(arg)
        else:
            return self.payload.__getitem__(arg)

    def __getslice__(self, start, stop):
        return self.directives.__getslice__(start, stop)

    def __len__(self):
        return len(self.directives)

    def __repr__(self):
        if self.name is not None:
            return '{}({!r})'.format(self._class_name, self.name)
        return '{}()'.format(self._class_name)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def attribute_name(self):
        return self._attribute_names

    @property
    def duration(self):
        return sum([durationtools.Duration(x) for x in self.time_signatures])        

    @property
    def has_relative_directives(self):
        return bool(self.relative_directives)

    @property
    def name(self):
        return self._name

    @property
    def relative_directives(self):
        result = []
        for directive in self.directives:
            if directive.is_relative:
                result.append(directive)
        return result

    @property
    def score_model(self):
        return self._score_model

    @property
    def time_signatures(self):
        setting = self.context_tree.score_context_proxy.get_setting(attribute_name='time_signatures')
        assert isinstance(setting.value, list), setting.value
        return setting.value

    ### PUBLIC METHODS ###

    def add_time_signatures(self, score):
        time_signatures = self.time_signatures
        measures = measuretools.make_measures_with_full_measure_spacer_skips(time_signatures)
        context = componenttools.get_first_component_in_expr_with_name(score, 'TimeSignatureContext')
        context.extend(measures)

    def annotate_source(self, source, callback=None, count=None, offset=None):
        assert isinstance(callback, (Callback, type(None))), callback
        assert isinstance(count, (int, type(None))), count
        assert isinstance(offset, (int, type(None))), offset
        if isinstance(source, StatalServer):
            if count is not None or offset is not None:
                source = StatalServerRequest(source, count=count, offset=offset)
        elif isinstance(source, Handler):
            if offset is not None:
                assert count is None
                source = HandlerRequest(source, offset=offset)
        elif isinstance(source, AttributeRetrievalIndicator):
            if any([x is not None for x in (callback, count, offset)]):
                source = AttributeRetrievalRequest(source, callback=callback, count=count, offset=offset)
        elif isinstance(source, DivisionRetrievalRequest):
            if any([x is not None for x in (callback, count, offset)]):
                source = copy.copy(source)
                source.callback = callback
                source.count = count
                source.offset = offset
        elif any([x is not None for x in (callback, count, offset)]):
            raise ValueError("'callback', 'count' or 'offset' set on nonstatal source: {!r}.".format(source))
        return source

    def get_directives(self, target_selection=None, attribute_name=None):
        result = []
        for directive in self.directives:
            if target_selection is None or directive.target_selection == target_selection:
                if attribute_name is None or directive.attribute_name == attribute_name:
                    result.append(directive)
        return result

    def get_divisions_value_with_fresh_and_truncate(self, context_name, scope=None):
        '''Return value found in context tree or else default to segment time signatures.
        '''
        value, fresh, truncate = self.get_resolved_value_with_fresh('divisions', context_name, 
            include_truncate=True, scope=scope)
        if value is None:
            value, fresh = self.get_resolved_value_with_fresh('time_signatures', context_name, 
            scope=scope)
            truncate = False
        return value, fresh, truncate

#    # this function will eventually replace get_divisions_value_with_fresh_and_truncate
#    def get_divisions_resolved_setting(self, context_name, scope=None):
#        '''Return resolved divisions setting or else default to resolve time signature setting.
#        '''
#        pass

    def get_resolved_value_with_fresh(self, attribute_name, context_name, include_truncate=False, scope=None):
        '''Return value from resolved setting because context proxy stores resolved settings.
        '''
        #self._debug((attribute_name, context_name))
        context = componenttools.get_first_component_in_expr_with_name(self.score_model, context_name)
        for component in componenttools.get_improper_parentage_of_component(context):
            #self._debug(component)
            context_proxy = self.context_tree[component.name]
            settings = context_proxy.get_settings(attribute_name=attribute_name, scope=scope)
            #self._debug(settings, 'settings')
            if not settings:
                continue
            elif len(settings) == 1:
                setting = settings[0]
                assert setting.value is not None # TODO: change to isinstance(setting, ResolvedSetting)
                if include_truncate:
                    return setting.value, setting.fresh, setting.truncate
                else:
                    return setting.value, setting.fresh
            else:
                raise Exception('multiple {!r} settings found.'.format(attribute_name))
        if include_truncate:
            return None, None, False
        else:
            return None, None
    
    def get_rhythm_value(self, context_name, scope=None):
        '''Default to rest-filled tokens if explicit rhythm not found.
        '''
        import baca.library as library
        value, fresh = self.get_resolved_value_with_fresh('rhythm', context_name, scope=scope)
        if value is not None:
            return value, fresh
        return library.rest_filled_tokens, True

    def get_setting(self, **kwargs):
        '''Return unresolved setting.
        '''
        return Specification.get_setting(self, segment_name=self.name, **kwargs)

    def get_settings(self, **kwargs):
        '''Return unresolved setting.
        '''
        return Specification.get_settings(self, segment_name=self.name, **kwargs)

    def parse_context_token(self, context_token):
        if context_token in self.context_names:
            context_names = [context_token]
        elif self.context_tree.all_are_context_names(context_token):
            context_names = context_token
        elif isinstance(context_token, type(self)):
            context_names = None
        else:
            raise ValueError('invalid context token: {!r}'.format(context_token))
        return context_names
            
    def parse_selection_token(self, selection_token):
        if isinstance(selection_token, Selection):
            selection = selection_token
        elif isinstance(selection_token, type(self)):
            selection = self.select()
        elif isinstance(selection_token, str) and selection_token in self.context_tree:
            selection = self.select(context_names=[selection_token])
        elif self.context_tree.all_are_context_names(selection_token):
            selection = self.select(context_names=selection_token)
        else:
            raise ValueError('invalid selection token: {!r}.'.format(selection_token))
        return selection

    def retrieve(self, attribute_name, **kwargs):
        return Specification.retrieve(self, attribute_name, self.name, **kwargs)

    def retrieve_resolved_value(self, attribute_name, **kwargs):
        return Specification.retrieve_resolved_value(self, attribute_name, self.name, **kwargs)

    def select(self, context_names=None, segment_name=None, scope=None):
        assert context_names is None or self.context_tree.all_are_context_names(context_names)
        assert isinstance(segment_name, (str, type(None)))
        assert isinstance(scope, (Scope, type(None)))
        segment_name = segment_name or self.name
        selection = Selection(segment_name, context_names=context_names, scope=scope)
        return selection

    def select_divisions(self, context_token=None, part=None, segment_name=None, start=None, stop=None):
        criterion = 'divisions'
        context_names = self.parse_context_token(context_token)
        scope = Scope(criterion=criterion, part=part, start=start, stop=stop)
        selection = self.select(context_names=context_names, segment_name=segment_name, scope=scope)
        return selection

    def select_measures(self, context_token=None, part=None, segment_name=None, start=None, stop=None):
        criterion = 'measures'
        context_names = self.parse_context_token(context_token)
        scope = Scope(criterion=criterion, part=part, start=start, stop=stop)
        selection = self.select(context_names=context_names, segment_name=segment_name, scope=scope)
        return selection
    
    def select_notes_and_chords(self, context_token=None, part=None, segment_name=None, start=None, stop=None):
        criterion = (chordtools.Chord, notetools.Note)
        context_names = self.parse_context_token(context_token)
        scope = Scope(criterion=criterion, part=part, start=start, stop=stop)
        selection = self.select(context_names=context_names, scope=scope)
        return selection

    def set_aggregate(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'aggregate'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_articulations(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'articulations'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_attribute(self, attribute_name, target_token, source, 
        callback=None, count=None, offset=None, persistent=True, truncate=False):
        assert attribute_name in self.attribute_names, attribute_name
        assert isinstance(count, (int, type(None))), count
        assert isinstance(persistent, type(True)), persistent
        assert isinstance(truncate, type(True)), truncate
        target_selection = self.parse_selection_token(target_token)
        source = self.annotate_source(source, callback=callback, count=count, offset=offset)
        directive = Directive(target_selection, attribute_name, source, 
            persistent=persistent, truncate=truncate)
        self.directives.append(directive)
        return directive

    def set_chord_treatment(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'chord_treatment'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_divisions(self, target_token, source, 
        callback=None, count=None, offset=None, persistent=True, truncate=False):
        attribute_name = 'divisions'
        return self.set_attribute(attribute_name, target_token, source, 
            callback=callback, count=count, offset=offset, persistent=persistent, truncate=truncate)

    def set_divisions_rotated_by_count(self, target_token, source, n, 
        count=None, offset=None, persistent=True, truncate=True):
        assert isinstance(n, int)
        string = 'lambda x: sequencetools.rotate_sequence(x, {})'.format(n)
        callback = Callback(eval(string), string)
        return self.set_divisions(target_token, source, 
            callback=callback, count=count, offset=offset, persistent=persistent, truncate=truncate)

    def set_duration_in_seconds(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'duration_in_seconds'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_dynamics(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'dynamics'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_marks(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'marks'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_markup(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'markup'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_pitch_classes(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'pitch_classes'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_pitch_class_application(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'pitch_class_application'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_pitch_class_transform(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'pitch_class_transform'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_register(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'register'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_rhythm(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'rhythm'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_tempo(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'tempo'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_time_signatures(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'time_signatures'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def set_written_duration(self, target_token, source, 
        count=None, persistent=True, offset=None):
        attribute_name = 'written_duration'
        return self.set_attribute(attribute_name, target_token, source, 
            count=count, persistent=persistent, offset=offset)

    def unpack_directives(self):
        for directive in self.directives:
            self.settings.extend(directive.unpack())
        return self.settings
