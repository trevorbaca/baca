# -*- encoding: utf-8 -*-
import collections
from abjad import *


class ScopeTokenParser(abctools.AbjadObject):
    r'''Scope token-parser.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### PRIVATE METHODS ###

    def _is_stage_pair(self, expr):
        if isinstance(expr, tuple):
            if len(expr) == 2:
                if isinstance(expr[0], int):
                    if isinstance(expr[-1], int):
                        return True
        return False

    def _to_compound_scope(self, scope):
        from baca import makers
        if isinstance(scope, makers.SimpleScope):
            scope = makers.CompoundScope(scope)
        elif isinstance(scope, makers.CompoundScope):
            pass
        # single scope token
        elif isinstance(scope, tuple):
            simple_scopes = self._to_simple_scopes(scope)    
            scope = makers.CompoundScope(*simple_scopes)
        # list of scope tokens
        elif isinstance(scope, list):
            simple_scopes = []
            for scope_token in scope:
                result = self._to_simple_scopes(scope_token)
                simple_scopes.extend(result)
            assert all(
                isinstance(_, makers.SimpleScope) for _ in simple_scopes)
            scope = makers.CompoundScope(*simple_scopes)
        else:
            message = 'must be simple scope, compound scope, scope token,'
            message + ' or list of scope tokens: {!r}.'
            message = message.format(scope)
            raise TypeError(message)
        assert isinstance(scope, makers.CompoundScope), repr(scope)
        compound_scope = scope
        return compound_scope

    def _to_simple_scopes(self, scope_token):
        from baca import makers
        if not isinstance(scope_token, collections.Sequence):
            message = 'scope token {!r} must be sequence.'
            message = message.format(scope_token)
            raise Exception(message)
        if not len(scope_token) == 2:
            message = 'scope {!r} must have length 2.'
            message = message.format(scope_token)
            raise Exception(message)
        context_names, stage_pairs = scope_token
        if isinstance(context_names, str):
            context_names = [context_names]
        if (not isinstance(context_names, collections.Sequence) or
            not all(isinstance(_, str) for _ in context_names)):
            message = 'context names {!r} must be sequence of strings.'
            message = message.format(context_names)
            raise Exception(message)
        if isinstance(stage_pairs, int):
            stage_pairs = [(stage_pairs, stage_pairs)]
        elif self._is_stage_pair(stage_pairs):
            stage_pairs = [stage_pairs]
        elif isinstance(stage_pairs, list):
            stage_pairs_ = []
            for stage_pair in stage_pairs:
                if isinstance(stage_pair, int):
                    stage_pairs_.append((stage_pair, stage_pair))
                elif self._is_stage_pair(stage_pair):
                    stage_pairs_.append(stage_pair)
                else:
                    raise TypeError(stage_pair)
            stage_pairs = stage_pairs_
        else:
            raise TypeError(stage_pairs)
        assert isinstance(stage_pairs, list), stage_pairs
        assert all(
            self._is_stage_pair(_) for _ in stage_pairs), stage_pairs
        simple_scopes = []
        for context_name in context_names:
            for stage_pair in stage_pairs:
                simple_scope = makers.SimpleScope(context_name, stage_pair)
                simple_scopes.append(simple_scope)
        return simple_scopes