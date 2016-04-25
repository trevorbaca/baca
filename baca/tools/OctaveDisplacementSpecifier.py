# -*- coding: utf-8 -*-
from abjad.tools import abctools
from abjad.tools import datastructuretools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools import selectiontools


class OctaveDisplacementSpecifier(abctools.AbjadObject):
    r"""Octave displacement specifier.

    ::

        >>> import baca

    ..  container:: example

        **Example 1.**

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.tools.stages(1)),
            ...     [
            ...         baca.pitch.pitches('G4'),
            ...         baca.rhythm.make_even_run_rhythm_specifier(),
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

            >>> score = lilypond_file.score_block.items[0]
            >>> f(score)
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

    def __init__(
        self,
        displacements=None,
        ):
        from abjad.tools import pitchtools
        displacements = tuple(displacements)
        assert self._is_octave_displacement_vector(displacements)
        displacements = datastructuretools.CyclicTuple(displacements)
        self._displacements = displacements

    ### SPECIAL METHODS ###

    def __call__(self, logical_ties):
        r'''Calls displacement specifier.

        Returns none.
        '''
        for i, logical_tie in enumerate(logical_ties):
            assert isinstance(logical_tie, selectiontools.LogicalTie)
            displacement = self.displacements[i]
            interval = pitchtools.NumberedInterval(displacement * 12)
            for note in logical_tie:
                assert isinstance(note, scoretools.Note), repr(note)
                written_pitch = note.written_pitch
                written_pitch += interval
                note.written_pitch = written_pitch

    ### PRIVATE METHODS ###

    def _is_octave_displacement_vector(self, expr):
        if isinstance(expr, (tuple, list)):
            if all(isinstance(_, int) for _ in expr):
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

        Set to integers or none.

        Returns cyclic tuple or none.
        '''
        return self._displacements