import abjad
import baca
from .Command import Command


class OverrideCommand(Command):
    r'''Override command.

    >>> from abjad import rhythmmakertools as rhythmos

    ..  container:: example

        With music-maker:

        >>> music_maker = baca.MusicMaker(
        ...     baca.beam_positions(6),
        ...     baca.stems_up(),
        ...     )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker('Voice 1', collections)
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            \override Beam.positions = #'(6 . 6)
                            \override Stem.direction = #up
                            c'16 [
                            d'16
                            bf'16 ]
                        }
                        {
                            fs''16 [
                            e''16
                            ef''16
                            af''16
                            g''16 ]
                        }
                        {
                            a'16
                            \revert Beam.positions
                            \revert Stem.direction
                        }
                    }
                }
            >>

    ..  container:: example

        With segment-maker:

        >>> segment_maker = baca.SegmentMaker(
        ...     score_template=baca.ViolinSoloScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> segment_maker(
        ...     baca.scope('Violin Music Voice', 1),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.beam_positions(6),
        ...     baca.rests_up(),
        ...     baca.stems_up(),
        ...     baca.RhythmBuilder(
        ...         rhythm_maker=rhythmos.TaleaRhythmMaker(
        ...             talea=rhythmos.Talea(
        ...                 counts=[1, 1, 1, -1],
        ...                 denominator=8,
        ...                 ),
        ...             ),
        ...         ),
        ...     )

        >>> result = segment_maker.run(docs=True)
        >>> lilypond_file, metadata = result
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context GlobalContext = "Global Context" <<
                    \context GlobalRests = "Global Rests" {
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                    }
                    \context GlobalSkips = "Global Skips" {
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            \set ViolinMusicStaff.instrumentName = \markup { Violin }
                            \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                            \clef "treble"
                            \override Beam.positions = #'(6 . 6)
                            \override Stem.direction = #up
                            e'8 [
                            d''8
                            f'8 ]
                            \override Rest.direction = #up
                            r8
                            e''8 [
                            g'8
                            f''8 ]
                            r8
                            e'8 [
                            d''8
                            f'8 ]
                            r8
                            \revert Rest.direction
                            e''8 [
                            g'8 ]
                            \bar "|"
                            \revert Beam.positions
                            \revert Stem.direction
                        }
                    }
                >>
            >>

    ..  container:: example

        >>> baca.OverrideCommand()
        OverrideCommand(selector=baca.leaves())

    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_attribute_name',
        '_attribute_value',
        '_context_name',
        '_grob_name',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        context_name=None,
        grob_name=None,
        attribute_name=None,
        attribute_value=None,
        selector='baca.leaves()',
        ):
        Command.__init__(self, selector=selector)
        if context_name is not None:
            assert isinstance(context_name, str), repr(context_name)
        self._context_name = context_name
        if grob_name is not None:
            assert isinstance(grob_name, str), repr(grob_name)
        self._grob_name = grob_name
        if attribute_name is not None:
            assert isinstance(attribute_name, str), repr(attribute_name)
        self._attribute_name = attribute_name
        self._attribute_value = attribute_value

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        context_name = self.context_name
        grob_name = self.grob_name
        attribute_name = self.attribute_name
        attribute_value = self.attribute_value
        string = abjad.LilyPondFormatManager.make_lilypond_override_string(
            grob_name,
            attribute_name,
            attribute_value,
            context_name=context_name,
            is_once=False,
            )
        string = string.replace('\\', '')
        override = abjad.LilyPondCommand(string)
        string = abjad.LilyPondFormatManager.make_lilypond_revert_string(
            grob_name,
            attribute_name,
            context_name=context_name,
            )
        string = string.replace('\\', '')
        revert = abjad.LilyPondCommand(string, format_slot='after')
        leaves = abjad.select(argument).leaves(grace_notes=False)
        abjad.attach(override, leaves[0])
        abjad.attach(revert, leaves[-1])

    ### PUBLIC PROPERTIES ###

    @property
    def attribute_name(self):
        r'''Gets attribute name.

        Set to string or none.
        '''
        return self._attribute_name

    @property
    def attribute_value(self):
        r'''Gets attribute value.

        Set to string or none.
        '''
        return self._attribute_value

    @property
    def context_name(self):
        r'''Gets context name.

        Defaults to none.

        Set to string or none.

        Returns string or none.
        '''
        return self._context_name

    @property
    def grob_name(self):
        r'''Gets grob name.

        Set to string or none.
        '''
        return self._grob_name
