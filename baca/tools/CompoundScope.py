# -*- coding: utf-8 -*-
import collections
from abjad import *


class CompoundScope(abctools.AbjadObject):
    r'''Compound scope.

    ..  container:: example
    
        **Example 1.** Makes four-part compound scope:

        ::

            >>> import baca

        ::

            >>> scope = baca.tools.CompoundScope([
            ...     baca.tools.SimpleScope('Piano Music Voice', (5, 9)),
            ...     baca.tools.SimpleScope('Clarinet Music Voice', (7, 12)),
            ...     baca.tools.SimpleScope('Violin Music Voice', (8, 12)),
            ...     baca.tools.SimpleScope('Oboe Music Voice', (9, 12)),
            ...     ])

        ::

            >>> print(format(scope, 'storage'))
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

            **Example 2.** Makes empty compound scope:

            ::

                >>> compound_scope = baca.tools.CompoundScope()

            ::

                >>> print(format(compound_scope))
                baca.tools.CompoundScope()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_simple_scopes',
        '_timespan_map',
        )

    ### INITIALIZER ###

    def __init__(self, simple_scopes=None):
        import baca
        if simple_scopes is not None:
            assert isinstance(simple_scopes, (tuple, list))
            simple_scopes_ = []
            for simple_scope in simple_scopes:
                if not isinstance(simple_scope, baca.tools.SimpleScope):
                    simple_scope = baca.tools.SimpleScope(*simple_scope)
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
        voice = inspect_(component).get_parentage().get_first(Voice)
        component_timespan = inspect_(component).get_timespan()
        for voice_name, scope_timespan in self._timespan_map:
            if voice_name == voice.name:
                if component_timespan.starts_during_timespan(scope_timespan):
                    return True
        return False

    ### PRIVATE METHODS ###

    @staticmethod
    def _is_stage_pair(expr):
        import baca
        if isinstance(expr, baca.tools.StageExpression):
            return True
        if isinstance(expr, tuple):
            if len(expr) == 2:
                if isinstance(expr[0], int):
                    if isinstance(expr[-1], int):
                        return True
        return False

    @classmethod
    def _to_compound_scope(class_, scope):
        import baca
        if isinstance(scope, baca.tools.SimpleScope):
            scope = baca.tools.CompoundScope(scope)
        elif isinstance(scope, baca.tools.CompoundScope):
            pass
        # single scope token
        elif isinstance(scope, tuple):
            simple_scopes = class_._to_simple_scopes(scope)    
            scope = baca.tools.CompoundScope(simple_scopes)
        # list of scope tokens
        elif isinstance(scope, list):
            simple_scopes = []
            for scope_token in scope:
                result = class_._to_simple_scopes(scope_token)
                simple_scopes.extend(result)
            assert all(
                isinstance(_, baca.tools.SimpleScope) for _ in simple_scopes)
            scope = baca.tools.CompoundScope(simple_scopes)
        else:
            message = 'must be simple scope, compound scope, scope token,'
            message + ' or list of scope tokens: {!r}.'
            message = message.format(scope)
            raise TypeError(message)
        assert isinstance(scope, baca.tools.CompoundScope), repr(scope)
        compound_scope = scope
        return compound_scope

    @classmethod
    def _to_simple_scopes(class_, scope_token):
        import baca
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
        elif isinstance(stage_pairs, baca.tools.StageExpression):
            #start = stage_pairs.stage_start_number
            #stop = stage_pairs.stage_stop_number
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
            for stage_pair in stage_pairs:
                simple_scope = baca.tools.SimpleScope(voice_name, stage_pair)
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