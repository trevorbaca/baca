# -*- coding: utf-8 -*-
import abjad
import baca
import collections


class CompoundScope(abjad.abctools.AbjadObject):
    r'''Compound scope.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example
    
        Makes four-part compound scope:

        ::

            >>> scope = baca.CompoundScope([
            ...     baca.SimpleScope('Piano Music Voice', (5, 9)),
            ...     baca.SimpleScope('Clarinet Music Voice', (7, 12)),
            ...     baca.SimpleScope('Violin Music Voice', (8, 12)),
            ...     baca.SimpleScope('Oboe Music Voice', (9, 12)),
            ...     ])

        ::

            >>> f(scope)
            baca.tools.CompoundScope(
                simple_scopes=(
                    baca.tools.SimpleScope(
                        voice_name='Piano Music Voice',
                        stages=(5, 9),
                        ),
                    baca.tools.SimpleScope(
                        voice_name='Clarinet Music Voice',
                        stages=(7, 12),
                        ),
                    baca.tools.SimpleScope(
                        voice_name='Violin Music Voice',
                        stages=(8, 12),
                        ),
                    baca.tools.SimpleScope(
                        voice_name='Oboe Music Voice',
                        stages=(9, 12),
                        ),
                    ),
                )

        ..  container:: example

            Makes empty compound scope:

            ::

                >>> compound_scope = baca.CompoundScope()

            ::

                >>> f(compound_scope)
                baca.tools.CompoundScope()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Segments'

    __slots__ = (
        '_simple_scopes',
        '_timespan_map',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, simple_scopes=None):
        if simple_scopes is not None:
            assert isinstance(simple_scopes, (tuple, list))
            simple_scopes_ = []
            for simple_scope in simple_scopes:
                if not isinstance(simple_scope, baca.SimpleScope):
                    simple_scope = baca.SimpleScope(*simple_scope)
                simple_scopes_.append(simple_scope)
            simple_scopes = simple_scopes_
            simple_scopes = tuple(simple_scopes)
        self._simple_scopes = simple_scopes
        self._timespan_map = None

    ### SPECIAL METHODS ###

    def __contains__(self, component):
        if self._timespan_map is None:
            message = 'must construct timespan map first.'
            raise Exception(message)
        agent = abjad.inspect_(component)
        voice = agent.get_parentage().get_first(abjad.Voice)
        if voice is None:
            voice = agent.get_parentage().get_first(abjad.Context)
        if voice is None:
            message = 'can not finding enclosing voice or context: {!r}.'
            message = message.format(component)
            raise Exception(message)
        component_timespan = agent.get_timespan()
        for voice_name, scope_timespan in self._timespan_map:
            if voice_name != voice.name:
                continue
            if component_timespan.starts_during_timespan(scope_timespan):
                return True
        return False

    ### PRIVATE METHODS ###

    @staticmethod
    def _is_stage_pair(argument):
        if isinstance(argument, baca.StageExpression):
            return True
        if isinstance(argument, tuple):
            if len(argument) == 2:
                if isinstance(argument[0], int):
                    if isinstance(argument[-1], int):
                        return True
        return False

    @classmethod
    def _to_compound_scope(class_, scope, score_template=None):
        if isinstance(scope, baca.SimpleScope):
            scope = baca.CompoundScope(scope)
        elif isinstance(scope, baca.CompoundScope):
            pass
        # single scope token
        elif isinstance(scope, tuple):
            simple_scopes = class_._to_simple_scopes(
                scope,
                score_template=score_template,
                )
            scope = baca.CompoundScope(simple_scopes)
        # list of scope tokens
        elif isinstance(scope, list):
            simple_scopes = []
            for scope_token in scope:
                result = class_._to_simple_scopes(
                    scope_token,
                    score_template=score_template,
                    )
                simple_scopes.extend(result)
            assert all(
                isinstance(_, baca.SimpleScope) for _ in simple_scopes)
            scope = baca.CompoundScope(simple_scopes)
        else:
            message = 'must be simple scope, compound scope, scope token,'
            message + ' or list of scope tokens: {!r}.'
            message = message.format(scope)
            raise TypeError(message)
        assert isinstance(scope, baca.CompoundScope), repr(scope)
        compound_scope = scope
        return compound_scope

    @classmethod
    def _to_simple_scopes(class_, scope_token, score_template=None):
        if not isinstance(scope_token, collections.Sequence):
            message = 'scope token {!r} must be sequence.'
            message = message.format(scope_token)
            raise Exception(message)
        if not len(scope_token) == 2:
            message = 'scope {!r} must have length 2.'
            message = message.format(scope_token)
            raise Exception(message)
        voice_names, stage_pairs = scope_token
        if isinstance(voice_names, str):
            voice_names = [voice_names]
        if (not isinstance(voice_names, collections.Sequence) or
            not all(isinstance(_, str) for _ in voice_names)):
            message = 'voice names {!r} must be sequence of strings.'
            message = message.format(voice_names)
            raise Exception(message)
        if isinstance(stage_pairs, int):
            stage_pairs = [(stage_pairs, stage_pairs)]
        elif class_._is_stage_pair(stage_pairs):
            stage_pairs = [stage_pairs]
        elif isinstance(stage_pairs, baca.StageExpression):
            #start = stage_pairs.start
            #stop = stage_pairs.stop
            #stage_pairs = [(start, stop)]
            pass
        elif isinstance(stage_pairs, list):
            stage_pairs_ = []
            for stage_pair in stage_pairs:
                if isinstance(stage_pair, int):
                    stage_pairs_.append((stage_pair, stage_pair))
                elif class_._is_stage_pair(stage_pair):
                    stage_pairs_.append(stage_pair)
                else:
                    raise TypeError(stage_pair)
            stage_pairs = stage_pairs_
        else:
            raise TypeError(stage_pairs)
        assert isinstance(stage_pairs, list), stage_pairs
        assert all(
            class_._is_stage_pair(_) for _ in stage_pairs), stage_pairs
        simple_scopes = []
        for voice_name in voice_names:
            if (score_template is not None and
                hasattr(score_template, 'voice_abbreviations')):
                voice_name = score_template.voice_abbreviations.get(
                    voice_name,
                    voice_name,
                    )
            for stage_pair in stage_pairs:
                simple_scope = baca.SimpleScope(voice_name, stage_pair)
                simple_scopes.append(simple_scope)
        return simple_scopes

    ### PUBLIC PROPERTIES ###

    @property
    def simple_scopes(self):
        r'''Gets simple scopes that comprise compound scope.

        Set to simple scopes or none.
        '''
        return self._simple_scopes

    ### PUBLIC METHODS ###

    @classmethod
    def from_token(class_, token):
        r'''Makes compound scope from `token`.

        Returns compound scope.
        '''
        return class_._to_compound_scope(token)
