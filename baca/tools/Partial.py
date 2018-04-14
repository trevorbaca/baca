import abjad
import typing


class Partial(abjad.AbjadObject):
    r'''Partial.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_fundamental',
        '_number',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        fundamental: typing.Union[str, abjad.NamedPitch] = 'C1',
        number: int = 1,
        ) -> None:
        fundamental = abjad.NamedPitch(fundamental)
        self._fundamental = fundamental
        assert isinstance(number, int), repr(number)
        assert 1 <= number, repr(number)
        self._number = number
        pitch = abjad.NamedPitch(fundamental)
        self._pitch = pitch
        # TODO:
        deviation = 0
        self._deviation = deviation

    ### PUBLIC PROPERTIES ###

    @property
    def deviation(self) -> int:
        r'''Gets deviation in cents.
        '''
        return self._deviation

    @property
    def fundamental(self) -> abjad.NamedPitch:
        r'''Gets fundamental.
        '''
        return self._fundamental

    @property
    def number(self) -> int:
        r'''Gets number.
        '''
        return self._number

    @property
    def pitch(self) -> abjad.NamedPitch:
        r'''Gets pitch.
        '''
        return self._pitch
