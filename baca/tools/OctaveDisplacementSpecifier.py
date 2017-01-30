# -*- coding: utf-8 -*-
import abjad


class OctaveDisplacementSpecifier(abjad.abctools.AbjadObject):
    r"""Octave displacement specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Displaces octaves:

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.select.stages(1)),
            ...     [
            ...         baca.pitches('G4'),
            ...         baca.make_even_run_rhythm_specifier(),
            ...         baca.tools.OctaveDisplacementSpecifier(
            ...             displacements=[0, 0, 1, 1, 0, 0, -1, -1, 2, 2],
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
                                g'8 [
                                g'8
                                g''8
                                g''8 ]
                            }
                            {
                                g'8 [
                                g'8
                                g8 ]
                            }
                            {
                                g8 [
                                g'''8
                                g'''8
                                g'8 ]
                            }
                            {
                                g'8 [
                                g''8
                                g''8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    """

    ### CLASS VARIABLES ##

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_displacements',
        )

    ### INITIALIZER ###

    def __init__(self, displacements=None):
        if displacements is not None:
            displacements = tuple(displacements)
            assert self._is_octave_displacement_vector(displacements)
            displacements = abjad.datastructuretools.CyclicTuple(displacements)
        self._displacements = displacements

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls specifier on `argument`.

        Returns none.
        '''
        if self.displacements is None:
            return
        logical_ties = abjad.iterate(argument).by_logical_tie(
            with_grace_notes=True,
            )
        for i, logical_tie in enumerate(logical_ties):
            assert isinstance(logical_tie, abjad.selectiontools.LogicalTie)
            displacement = self.displacements[i]
            interval = abjad.NumberedInterval(12*displacement)
            for note in logical_tie:
                assert isinstance(note, abjad.scoretools.Note), repr(note)
                written_pitch = note.written_pitch
                written_pitch += interval
                note.written_pitch = written_pitch

    ### PRIVATE METHODS ###

    def _is_octave_displacement_vector(self, argument):
        if isinstance(argument, (tuple, list)):
            if all(isinstance(_, int) for _ in argument):
                return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def displacements(self):
        r'''Gets displacements.

        ..  container:: example

            ::

        
                >>> specifier = baca.tools.OctaveDisplacementSpecifier(
                ...     displacements=[0, 0, 0, 1, 1, 0, 0, 0, -1, 1, 1, 2, 2],
                ...     )

            ::

                >>> specifier.displacements
                CyclicTuple([0, 0, 0, 1, 1, 0, 0, 0, -1, 1, 1, 2, 2])

        Defaults to none.

        Set to integers or none.

        Returns cyclic tuple of integers or none.
        '''
        return self._displacements
