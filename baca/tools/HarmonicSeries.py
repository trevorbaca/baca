import abjad
import typing
from .Partial import Partial


class HarmonicSeries(abjad.AbjadObject):
    r'''Harmonic series.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_fundamental',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        fudamental: typing.Union[str, abjad.NamedPitch] = 'C1',
        ) -> None:
        fundamental = abjad.NamedPitch(fundamental)
        self._fundamental = fundamental

    ### SPECIAL METHODS ###

    def __illustrate__(self) -> abjad.LilyPondFile:
        r'''Illustrates harmonic series.
        '''
        staff = abjad.Staff()
        for n in range(1, 20 + 1):
            partial = self.partial(n)
            pitch = partial.pitch
            note = abjad.Note(pitch, (1, 4))
            staff.append(note)
        lilypond_file = abjad.LilyPondFile.new(staff)
        return lilypond_file

    ### PUBLIC PROPERTIES ###

    @property
    def fundamental(self) -> abjad.NamedPitch:
        r'''Gets fundamental.
        '''
        return self._fundamental

    ### PUBLIC METHODS ###

    def partial(self, n: int) -> Partial:
        r'''Gets partial `n`.
        '''
        return Partial()
