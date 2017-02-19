# -*- coding: utf-8 -*-
import abjad


class GlissandoSpecifier(abjad.abctools.AbjadObject):
    r'''Glissando specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Selects all logical ties:

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.select.stages(1)),
            ...     baca.make_even_run_rhythm_specifier(),
            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...     baca.tools.GlissandoSpecifier(
            ...         pattern=abjad.select_all(),
            ...         ),
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, segment_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context TimeSignatureContext = "Time Signature Context" <<
                    \context TimeSignatureContextMultimeasureRests = "Time Signature Context Multimeasure Rests" {
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
                    \context TimeSignatureContextSkips = "Time Signature Context Skips" {
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
                        \clef "treble"
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                e'8 \glissando [
                                d''8 \glissando
                                f'8 \glissando
                                e''8 ] \glissando
                            }
                            {
                                g'8 \glissando [
                                f''8 \glissando
                                e'8 ] \glissando
                            }
                            {
                                d''8 \glissando [
                                f'8 \glissando
                                e''8 \glissando
                                g'8 ] \glissando
                            }
                            {
                                f''8 \glissando [
                                e'8 \glissando
                                d''8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Selects first and last logical ties:

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> pattern = abjad.select_first(1) | abjad.select_last(2)
            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.select.stages(1)),
            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...     baca.make_even_run_rhythm_specifier(),
            ...     baca.tools.GlissandoSpecifier(
            ...         pattern=pattern,
            ...         ),
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, segment_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context TimeSignatureContext = "Time Signature Context" <<
                    \context TimeSignatureContextMultimeasureRests = "Time Signature Context Multimeasure Rests" {
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
                    \context TimeSignatureContextSkips = "Time Signature Context Skips" {
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
                        \clef "treble"
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                e'8 \glissando [
                                d''8
                                f'8
                                e''8 ]
                            }
                            {
                                g'8 [
                                f''8
                                e'8 ]
                            }
                            {
                                d''8 [
                                f'8
                                e''8
                                g'8 ]
                            }
                            {
                                f''8 [
                                e'8 \glissando
                                d''8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Selects first stage with figure-maker:

        ::

            >>> figure_maker = baca.tools.FigureMaker()

        ::

            >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = figure_maker(
            ...     'Voice 1',
            ...     segments,
            ...     baca.tools.GlissandoSpecifier(
            ...         pattern=abjad.select_first(),
            ...         ),
            ...     )
            >>> lilypond_file = figure_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            c'16 \glissando [
                            d'16 \glissando
                            bf'16 ] \glissando
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
                        }
                    }
                }
            >>

    '''

    ### CLASS VARIABLES ##

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_pattern',
        )

    ### INITIALIZER ###

    def __init__(self, pattern=None):
        prototype = (abjad.Pattern, abjad.patterntools.CompoundPattern)
        if not pattern is None:
            assert isinstance(pattern, prototype), repr(pattern)
        self._pattern = pattern

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls glissando specifier on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        pattern = self.pattern or abjad.select_all()
        if isinstance(argument, list):
            selections = argument
            assert isinstance(selections[0], abjad.Selection), repr(argument) 
            selections = pattern.get_matching_items(selections)
            for selection in selections:
                logical_ties = abjad.iterate(selection).by_logical_tie(
                    pitched=True)
                for logical_tie in logical_ties:
                    self._attach_glissando(logical_tie)
        else:
            selection = argument
            assert isinstance(selection, abjad.Selection), repr(selection)
            logical_ties = pattern.get_matching_items(selection)
            for logical_tie in logical_ties:
                self._attach_glissando(logical_tie)

    ### PRIVATE METHODS ###

    def _attach_glissando(self , logical_tie):
        note_or_chord = (abjad.scoretools.Note, abjad.scoretools.Chord)
        last_leaf = logical_tie.tail
        if not isinstance(last_leaf, note_or_chord):
            return
        next_leaf = abjad.inspect_(last_leaf).get_leaf(1)
        if not isinstance(next_leaf, note_or_chord):
            return
        leaves = [last_leaf, next_leaf]
        abjad.attach(abjad.Glissando(), leaves)

    ### PUBLIC PROPERTIES ###

    @property
    def pattern(self):
        r'''Gets pattern.

        ..  container:: example

            ::

                >>> specifier = baca.tools.GlissandoSpecifier(
                ...     pattern=abjad.select_first(1) | abjad.select_last(2),
                ...     )
        

            ::

                >>> f(specifier.pattern)
                patterntools.CompoundPattern(
                    (
                        patterntools.Pattern(
                            indices=[0],
                            ),
                        patterntools.Pattern(
                            indices=[-2, -1],
                            ),
                        ),
                    operator='or',
                    )

        Set to pattern or none.

        Returns pattern or none.
        '''
        return self._pattern
