import abjad
import baca
from .ScoreTemplate import ScoreTemplate


class ViolinSoloScoreTemplate(ScoreTemplate):
    r'''Violin solo score template.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.ViolinSoloScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        %%% GlobalSkips [measure 1] %%%
                        \time 4/8
                        \bar "" % SEGMENT:EMPTY-BAR
                        s1 * 1/2
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
                    \tag violin
                    \context ViolinMusicStaff = "ViolinMusicStaff" {
                        \context ViolinMusicVoice = "ViolinMusicVoice" {
            <BLANKLINE>
                            %%% ViolinMusicVoice [measure 1] %%%
                            \set ViolinMusicStaff.instrumentName = \markup {
                                \hcenter-in
                                    #16
                                    Violin
                                }
                            \set ViolinMusicStaff.shortInstrumentName = \markup {
                                \hcenter-in
                                    #10
                                    Vn.
                                }
                            \clef "treble"
                            R1 * 1/2
            <BLANKLINE>
                            %%% ViolinMusicVoice [measure 2] %%%
                            R1 * 3/8
            <BLANKLINE>
                            %%% ViolinMusicVoice [measure 3] %%%
                            R1 * 1/2
            <BLANKLINE>
                            %%% ViolinMusicVoice [measure 4] %%%
                            R1 * 3/8
                            \bar "|"
            <BLANKLINE>
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls violin solo score template.

        Returns score.
        '''
        global_context = self._make_global_context()
        instrument_tags = (
            'violin',
            )
        tag_string = '.'.join(instrument_tags)
        tag_string = f'tag {tag_string}'
        tag_command = abjad.LilyPondCommand(
            tag_string,
            'before',
            )
        abjad.attach(tag_command, global_context)
        # VIOLIN
        violin_music_voice = abjad.Voice(
            [],
            context_name='ViolinMusicVoice',
            name='ViolinMusicVoice',
            )
        violin_music_staff = abjad.Staff(
            [violin_music_voice],
            context_name='ViolinMusicStaff',
            name='ViolinMusicStaff',
            )
        violin = abjad.instrumenttools.Violin(
            name_markup=baca.markup.instrument('Violin'),
            short_name_markup=baca.markup.short_instrument('Vn.'),
            )
        abjad.annotate(
            violin_music_staff,
            'default_instrument',
            violin,
            )
        abjad.annotate(
            violin_music_staff,
            'default_clef',
            abjad.Clef('treble'),
            )
        self._attach_tag('violin', violin_music_staff)
        # SCORE
        music_context = abjad.Context(
            [
                violin_music_staff,
                ],
            context_name='MusicContext',
            is_simultaneous=True,
            name='MusicContext',
            )
        score = abjad.Score(
            [
                global_context,
                music_context,
                ],
            name='Score',
            )
        return score
