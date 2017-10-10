import abjad
import baca


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

    ### PUBLIC PROPERTIES ###

    @property
    def scopes(self):
        r'''Gets scopes.

        Returns tuple.
        '''
        return self._scopes
