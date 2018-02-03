import abjad
import baca
from .Command import Command
from .Typing import Selector


class LilyPondTagCommand(Command):
    r'''LilyPond tag command.

    ..  container:: example

        >>> baca.LilyPondTagCommand()
        LilyPondTagCommand(selector=baca.leaves())

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.lilypond_tag('ViolinI', baca.leaves()[:2]),
        ...     baca.lilypond_tag('ViolinI.ViolinII', baca.leaves()[2:]),
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
                        {   %*% ViolinI.ViolinII
        <BLANKLINE>
                            % [MusicVoice measure 3]                                             %! SM4
                            e'2
        <BLANKLINE>
                            % [MusicVoice measure 4]                                             %! SM4
                            f'4.
        <BLANKLINE>
                        }   %*% ViolinI.ViolinII
                    }
                }
            >>
        >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bracket_comment',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        bracket_comment: str = None,
        selector: Selector = 'baca.leaves()',
        ):
        Command.__init__(self, selector=selector)
        self._bracket_comment = bracket_comment

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Applies command to result of selector called on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        container = abjad.Container(bracket_comment=self.bracket_comment)
        components = baca.select(argument).leaves().top()
        abjad.mutate(components).wrap(container)

    ### PUBLIC PROPERTIES ###

    @property
    def bracket_comment(self) -> str:
        r'''Gets bracket comment.
        '''
        return self._bracket_comment
