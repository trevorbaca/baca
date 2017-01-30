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
            ...     [
            ...         baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...         baca.make_even_run_rhythm_specifier(),
            ...         baca.tools.GlissandoSpecifier(
            ...             patterns=patterntools.select_all(),
            ...             ),
            ...         ],
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, segment_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[Score])
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

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.select.stages(1)),
            ...     [
            ...         baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...         baca.make_even_run_rhythm_specifier(),
            ...         baca.tools.GlissandoSpecifier(
            ...             patterns=[
            ...                 patterntools.select_first(1),
            ...                 patterntools.select_last(2),
            ...                 ],
            ...             ),
            ...         ],
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, segment_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[Score])
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

    '''

    ### CLASS VARIABLES ##

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_patterns',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        patterns=None,
        ):
        if isinstance(patterns, abjad.patterntools.Pattern):
            patterns = (patterns,)
        patterns = patterns or ()
        patterns = tuple(patterns)
        prototype = (
            abjad.patterntools.Pattern,
            abjad.patterntools.CompoundPattern,
            )
        assert all(isinstance(_, prototype) for _ in patterns), repr(patterns)
        self._patterns = patterns

    ### SPECIAL METHODS ###

    def __call__(self, logical_ties):
        r'''Calls glissando specifier on `logical_ties`.

        Returns none.
        '''
        logical_tie_count = len(logical_ties)
        for index, logical_tie in enumerate(logical_ties):
            for pattern in reversed(self.patterns):
                if pattern.matches_index(index, logical_tie_count):
                    self._apply_pattern(pattern, logical_tie)
                    break

    ### PRIVATE METHODS ###

    def _apply_pattern(self , pattern, logical_tie):
        if isinstance(pattern, abjad.rhythmmakertools.SilenceMask):
            return
        make_glissando_prototype = (
            abjad.patterntools.Pattern,
            abjad.rhythmmakertools.SustainMask,
            )
        assert isinstance(pattern, make_glissando_prototype)
        note_or_chord = (abjad.scoretools.Note, abjad.scoretools.Chord)
        if isinstance(pattern, make_glissando_prototype):
            last_leaf = logical_tie.tail
            if not isinstance(last_leaf, note_or_chord):
                return
            next_leaf = abjad.inspect_(last_leaf).get_leaf(1)
            if not isinstance(next_leaf, note_or_chord):
                return
            leaves = [last_leaf, next_leaf]
            abjad.attach(abjad.spannertools.Glissando(), leaves)

    ### PUBLIC PROPERTIES ###

    @property
    def patterns(self):
        r'''Gets patterns.

        ..  container:: example

            ::

                >>> specifier = baca.tools.GlissandoSpecifier(
                ...     patterns=[
                ...         patterntools.Pattern(
                ...             indices=[0, 1],
                ...             period=2,
                ...             ),
                ...         patterntools.Pattern(
                ...             indices=[0],
                ...             ),
                ...         ],
                ...     )
        

            ::

                >>> specifier.patterns
                (Pattern(indices=[0, 1], period=2), Pattern(indices=[0]))

        Set to patterns or none.

        Returns tuple of patterns or none.
        '''
        return self._patterns
