import abjad
import baca
import collections


class CompoundScope(abjad.AbjadObject):
    r'''Compound scope.

    ..  container:: example

        ::

            >>> scope = baca.compound([
            ...     baca.scope('Piano Music Voice', 5, 9),
            ...     baca.scope('Clarinet Music Voice', 7, 12),
            ...     baca.scope('Violin Music Voice', 8, 12),
            ...     baca.scope('Oboe Music Voice', 9, 12),
            ...     ])

        ::

            >>> f(scope)
            baca.CompoundScope(
                scopes=(
                    baca.SimpleScope(
                        voice_name='Piano Music Voice',
                        stages=baca.StageSpecifier(
                            start=5,
                            stop=9,
                            ),
                        ),
                    baca.SimpleScope(
                        voice_name='Clarinet Music Voice',
                        stages=baca.StageSpecifier(
                            start=7,
                            stop=12,
                            ),
                        ),
                    baca.SimpleScope(
                        voice_name='Violin Music Voice',
                        stages=baca.StageSpecifier(
                            start=8,
                            stop=12,
                            ),
                        ),
                    baca.SimpleScope(
                        voice_name='Oboe Music Voice',
                        stages=baca.StageSpecifier(
                            start=9,
                            stop=12,
                            ),
                        ),
                    ),
                )

        ..  container:: example

            ::

                >>> baca.CompoundScope()
                CompoundScope()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        '_scopes',
        '_timespan_map',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, scopes=None):
        if scopes is not None:
            assert isinstance(scopes, (tuple, list))
            scopes_ = []
            for scope in scopes:
                if not isinstance(scope, baca.SimpleScope):
                    scope = baca.SimpleScope(*scope)
                scopes_.append(scope)
            scopes = scopes_
            scopes = tuple(scopes)
        self._scopes = scopes
        self._timespan_map = None

    ### SPECIAL METHODS ###

    def __contains__(self, component):
        if self._timespan_map is None:
            raise Exception('must construct timespan map first.')
        agent = abjad.inspect(component)
        voice = agent.get_parentage().get_first(abjad.Voice)
        if voice is None:
            voice = agent.get_parentage().get_first(abjad.Context)
        if voice is None:
            raise Exception(f'missing voice or context: {component!r}.')
        component_timespan = agent.get_timespan()
        for voice_name, scope_timespan in self._timespan_map:
            if voice_name != voice.name:
                continue
            if component_timespan.starts_during_timespan(scope_timespan):
                return True
        return False

    ### PRIVATE METHODS ###

    # TODO: remove
    @staticmethod
    def _is_stage_pair(argument):
        if isinstance(argument, baca.StageSpecifier):
            return True
        if isinstance(argument, tuple):
            if len(argument) == 2:
                if isinstance(argument[0], int):
                    if isinstance(argument[-1], int):
                        return True
        return False

    # TODO: remove
    @classmethod
    def _to_simple_scopes(class_, scope_token):
        if not isinstance(scope_token, collections.Sequence):
            raise Exception(f'{scope_token!r} must be sequence.')
        if not len(scope_token) == 2:
            raise Exception(f'scope {scope_token!r} must have length 2.')
        voice_names, stage_pairs = scope_token
        if isinstance(voice_names, str):
            voice_names = [voice_names]
        if (not isinstance(voice_names, collections.Sequence) or
            not all(isinstance(_, str) for _ in voice_names)):
            raise Exception(f'{voice_name!r} must be sequence of strings.')
        if isinstance(stage_pairs, int):
            stage_pairs = [(stage_pairs, stage_pairs)]
        elif class_._is_stage_pair(stage_pairs):
            stage_pairs = [stage_pairs]
        elif isinstance(stage_pairs, baca.StageSpecifier):
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
        scopes = []
        for voice_name in voice_names:
            for stage_pair in stage_pairs:
                scope = baca.SimpleScope(voice_name, stage_pair)
                scopes.append(scope)
        return scopes

    ### PUBLIC PROPERTIES ###

    @property
    def scopes(self):
        r'''Gets scopes.

        Returns tuple.
        '''
        return self._scopes
