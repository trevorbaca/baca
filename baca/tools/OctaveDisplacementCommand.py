import abjad


class OctaveDisplacementCommand(abjad.AbjadObject):
    r"""Octave displacement command.

    ..  container:: example

        Displaces octaves:

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_commands(
            ...     'vn',
            ...     baca.select_stages(1),
            ...     baca.pitches('G4'),
            ...     baca.even_runs(),
            ...     baca.OctaveDisplacementCommand(
            ...         displacements=[0, 0, 1, 1, 0, 0, -1, -1, 2, 2],
            ...         ),
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Score])
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
                            {
                                \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
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

    __documentation_section__ = 'Commands'

    __slots__ = (
        '_displacements',
        '_selector',
        )

    ### INITIALIZER ###

    def __init__(self, displacements=None, selector=None):
        if displacements is not None:
            displacements = tuple(displacements)
            assert self._is_octave_displacement_vector(displacements)
            displacements = abjad.CyclicTuple(displacements)
        self._displacements = displacements
        if selector is not None:
            assert isinstance(selector, abjad.Selector), repr(selector)
        self._selector = selector

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if self.displacements is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        logical_ties = abjad.iterate(argument).by_logical_tie(
            pitched=True,
            with_grace_notes=True,
            )
        for i, logical_tie in enumerate(logical_ties):
            assert isinstance(logical_tie, abjad.LogicalTie)
            displacement = self.displacements[i]
            interval = abjad.NumberedInterval(12 * displacement)
            for leaf in logical_tie:
                if isinstance(leaf, abjad.Note):
                    written_pitch = leaf.written_pitch
                    written_pitch += interval
                    leaf.written_pitch = written_pitch
                elif isinstance(leaf, abjad.Chord):
                    written_pitches = [
                        _ + interval for _ in leaf.written_pitches
                        ]
                    leaf.written_pitches = written_pitches

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

                >>> command = baca.OctaveDisplacementCommand(
                ...     displacements=[0, 0, 0, 1, 1, 0, 0, 0, -1, 1, 1, 2, 2],
                ...     )

            ::

                >>> command.displacements
                CyclicTuple([0, 0, 0, 1, 1, 0, 0, 0, -1, 1, 1, 2, 2])

        Defaults to none.

        Set to integers or none.

        Returns cyclic tuple of integers or none.
        '''
        return self._displacements

    @property
    def selector(self):
        r'''Gets selector.

        Returns selector or none.
        '''
        return self._selector
