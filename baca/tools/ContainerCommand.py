import abjad
import baca
from .Command import Command
from .Typing import Selector


class ContainerCommand(Command):
    r'''Container command.

    ..  container:: example

        >>> baca.ContainerCommand()
        ContainerCommand(selector=baca.leaves())

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.container('ViolinI', baca.leaves()[:2]),
        ...     baca.container('ViolinII', baca.leaves()[2:]),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')

        >>> abjad.f(lilypond_file[abjad.Score], strict=89)
        \context Score = "Score"
        <<
            \context GlobalContext = "GlobalContext"
            <<
                \context GlobalSkips = "GlobalSkips"
                {
        <BLANKLINE>
                    % [GlobalSkips measure 1]                                                    %! SM4
                    \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                    \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                    s1 * 1/2
        <BLANKLINE>
                    % [GlobalSkips measure 2]                                                    %! SM4
                    \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                    \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                    s1 * 3/8
        <BLANKLINE>
                    % [GlobalSkips measure 3]                                                    %! SM4
                    \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                    \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                    s1 * 1/2
        <BLANKLINE>
                    % [GlobalSkips measure 4]                                                    %! SM4
                    \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                    \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                    s1 * 3/8
                    \override Score.BarLine.transparent = ##f                                    %! SM5
                    \bar "|"                                                                     %! SM5
        <BLANKLINE>
                }
            >>
            \context MusicContext = "MusicContext"
            <<
                \context Staff = "MusicStaff"
                {
                    \context Voice = "MusicVoice"
                    {
                        {   %*% ViolinI
        <BLANKLINE>
                            % [MusicVoice measure 1]                                             %! SM4
                            e'2
        <BLANKLINE>
                            % [MusicVoice measure 2]                                             %! SM4
                            f'4.
                        }   %*% ViolinI
                        {   %*% ViolinII
        <BLANKLINE>
                            % [MusicVoice measure 3]                                             %! SM4
                            e'2
        <BLANKLINE>
                            % [MusicVoice measure 4]                                             %! SM4
                            f'4.
        <BLANKLINE>
                        }   %*% ViolinII
                    }
                }
            >>
        >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_identifier',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        identifier: str = None,
        selector: Selector = 'baca.leaves()',
        ) -> None:
        Command.__init__(self, selector=selector)
        assert abjad.String(identifier).is_lilypond_identifier()
        self._identifier: str = identifier

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        r'''Inserts ``selector`` output in container.
        '''
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if self.identifier.startswith('%*%'):
            identifier = self.identifier
        else:
            identifier = f'%*% {self.identifier}'
        container = abjad.Container(identifier=identifier)
        components = baca.select(argument).leaves().top()
        abjad.mutate(components).wrap(container)

    ### PUBLIC PROPERTIES ###

    @property
    def identifier(self) -> str:
        r'''Gets identifier.
        '''
        return self._identifier
