import abjad
import baca
from .Command import Command


class TagCommand(Command):
    r'''Tag command.

    ..  container:: example

        >>> baca.TagCommand()
        TagCommand(selector=baca.leaves())

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitches('E4 F4'),
        ...     baca.tag('ViolinI', baca.leaves()[:2]),
        ...     baca.tag('ViolinI.ViolinII', baca.leaves()[2:]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')

        >>> abjad.f(lilypond_file[abjad.Score], strict=79)
        \context Score = "Score" <<
            \context GlobalContext = "GlobalContext" <<
                \context GlobalSkips = "GlobalSkips" {
        <BLANKLINE>
                    %%% GlobalSkips [measure 1] %%%
                    \time 4/8
                    \bar ""                                                            %%! EMPTY_START_BAR
                    s1 * 1/2
                    - \markup {                                                        %%! STAGE_NUMBER_MARKUP
                        \fontsize                                                      %%! STAGE_NUMBER_MARKUP
                            #-3                                                        %%! STAGE_NUMBER_MARKUP
                            \with-color                                                %%! STAGE_NUMBER_MARKUP
                                #(x11-color 'DarkCyan)                                 %%! STAGE_NUMBER_MARKUP
                                [1]                                                    %%! STAGE_NUMBER_MARKUP
                        }                                                              %%! STAGE_NUMBER_MARKUP
        <BLANKLINE>
                    %%% GlobalSkips [measure 2] %%%
                    \time 3/8
                    s1 * 3/8
        <BLANKLINE>
                    %%% GlobalSkips [measure 3] %%%
                    \time 4/8
                    s1 * 1/2
        <BLANKLINE>
                    %%% GlobalSkips [measure 4] %%%
                    \time 3/8
                    s1 * 3/8
        <BLANKLINE>
                }
            >>
            \context MusicContext = "MusicContext" <<
                \context Staff = "MusicStaff" {
                    \context Voice = "MusicVoice" {
                        \tag ViolinI
                        {
        <BLANKLINE>
                            %%% MusicVoice [measure 1] %%%
                            e'2
        <BLANKLINE>
                            %%% MusicVoice [measure 2] %%%
                            f'4.
                        }
                        \tag ViolinI.ViolinII
                        {
        <BLANKLINE>
                            %%% MusicVoice [measure 3] %%%
                            e'2
        <BLANKLINE>
                            %%% MusicVoice [measure 4] %%%
                            f'4.
                            \bar "|"
        <BLANKLINE>
                        }
                    }
                }
            >>
        >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_tag',
        )

    ### INITIALIZER ###

    def __init__(self, selector='baca.leaves()', tag=None):
        Command.__init__(self, selector=selector)
        if tag is not None:
            assert isinstance(tag, str), repr(tag)
        self._tag = tag

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Applies command to result of selector called on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        leaves = baca.select(argument).leaves()
        container = abjad.Container()
        abjad.mutate(leaves).wrap(container)
        string = rf'\tag {self.tag}'
        literal = abjad.LilyPondLiteral(string, 'before')
        abjad.attach(literal, container)

    ### PUBLIC PROPERTIES ###

    @property
    def tag(self):
        r'''Gets tag.

        Returns string.
        '''
        return self._tag
