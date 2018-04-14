import abjad
import math
import typing


class Partial(abjad.AbjadObject):
    r'''Partial.

    ..  container:: example

        >>> baca.Partial('C1', 7)
        Partial(fundamental=NamedPitch('c,,'), number=7)

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_approximation',
        '_deviation',
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
        hertz = number * fundamental.hertz
        approximation = abjad.NamedPitch.from_hertz(hertz)
        self._approximation = approximation
        deviation_multiplier = hertz / approximation.hertz
        semitone_base = 2 ** abjad.Fraction(1, 12)
        deviation_semitones = math.log(deviation_multiplier, semitone_base)
        deviation_cents = 100 * deviation_semitones
        deviation = round(deviation_cents)
        self._deviation = deviation

    ### PUBLIC PROPERTIES ###

    @property
    def approximation(self) -> abjad.NamedPitch:
        r'''Gets approximation.

        ..  container:: example

            >>> baca.Partial('C1', 7).approximation
            NamedPitch('bf')

        '''
        return self._approximation

    @property
    def deviation(self) -> int:
        r'''Gets deviation in cents.

        ..  container:: example

            >>> baca.Partial('C1', 7).deviation
            -31

        '''
        return self._deviation

    @property
    def fundamental(self) -> abjad.NamedPitch:
        r'''Gets fundamental.

        ..  container:: example

            >>> baca.Partial('C1', 7).fundamental
            NamedPitch('c,,')

        '''
        return self._fundamental

    @property
    def number(self) -> int:
        r'''Gets number.

        ..  container:: example

            >>> baca.Partial('C1', 7).number
            7

        '''
        return self._number
