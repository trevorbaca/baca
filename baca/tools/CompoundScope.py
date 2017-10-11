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

    ### PUBLIC PROPERTIES ###

    @property
    def scopes(self):
        r'''Gets scopes.

        Returns tuple.
        '''
        return self._scopes
