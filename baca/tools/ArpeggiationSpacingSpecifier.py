# -*- coding: utf-8 -*-
import abjad
import baca


class ArpeggiationSpacingSpecifier(abjad.abctools.AbjadValueObject):
    r'''Arpeggiation spacing specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> specifier = baca.tools.ArpeggiationSpacingSpecifier()
            >>> specifier([[6, 0, 4, 5, 8]])
            SegmentList([<6, 12, 16, 17, 20>])

    ..  container:: example

        ::

            >>> specifier = baca.tools.ArpeggiationSpacingSpecifier()
            >>> specifier([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
            SegmentList([<0, 2, 10>, <6, 16, 27, 32, 43>, <9>])

    ..  container:: example

        ::

            >>> baca.tools.ArpeggiationSpacingSpecifier()
            ArpeggiationSpacingSpecifier()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_direction',
        '_pattern',
        '_start',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, direction=None, pattern=None, start=None):
        if direction is not None:
            assert direction in (Up, Down), repr(direction)
        self._direction = direction
        if pattern is not None:
            assert isinstance(pattern, abjad.Pattern), repr(pattern)
        self._pattern = pattern
        self._start = start

    ### SPECIAL METHODS ###

    def __call__(self, segments=None):
        r'''Calls specifier on `segments`.

        ..  container:: example

            ::

                >>> specifier = baca.tools.ArpeggiationSpacingSpecifier()
                >>> specifier([])
                PitchSegment([])

        ..  container:: example

            ::

                >>> specifier = baca.tools.ArpeggiationSpacingSpecifier()
                >>> specifier() is None
                True

        Returns pitch segment or none.
        '''
        if segments is None:
            return
        if segments == []:
            return abjad.PitchSegment(item_class=abjad.NumberedPitch)
        if not isinstance(segments, baca.SegmentList):
            segments = baca.SegmentList(segments)
        pitch_class_segments = segments.to_pitch_classes()
        pattern = self.pattern or abjad.patterntools.select_all()
        segments_ = []
        total_length = len(segments)
        class_ = baca.tools.ChordalSpacingSpecifier
        direction = self.direction or Up
        for i in range(total_length):
            if pattern.matches_index(i, total_length):
                pitch_classes = pitch_class_segments[i]
                pitch_classes = list(pitch_classes)
                start = self.start or pitch_classes[0]
                if direction is Up:
                    pitches = class_._to_tightly_spaced_pitches_ascending(
                        pitch_classes,
                        )
                else:
                    pitches = class_._to_tightly_spaced_pitches_descending(
                        pitch_classes,
                        )
                segment_ = abjad.PitchSegment(pitches)
                segments_.append(segment_)
            else:
                segments_.append(segments[i])
        return baca.SegmentList(segments_)

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self):
        r"""Gets direction.

        ..  container:: example

            ::

                >>> figure_maker = baca.tools.FigureMaker()

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker(
                ...     'Voice 1',
                ...     segments,
                ...     baca.tools.ArpeggiationSpacingSpecifier(
                ...         direction=Up,
                ...         ),
                ...     baca.tools.RegisterToOctaveSpecifier(octave_number=2),
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c,16 [
                                d,16
                                bf,16 ]
                            }
                            {
                                fs,16 [
                                e16
                                ef'16
                                af'16
                                g''16 ]
                            }
                            {
                                a,16
                            }
                        }
                    }
                >>

        ..  container:: example

            ::

                >>> figure_maker = baca.tools.FigureMaker()

            ::

                >>> segments = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
                >>> contribution = figure_maker(
                ...     'Voice 1',
                ...     segments,
                ...     baca.tools.ArpeggiationSpacingSpecifier(
                ...         direction=Down,
                ...         ),
                ...     baca.tools.RegisterToOctaveSpecifier(octave_number=2),
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                c'16 [
                                d16
                                bf,16 ]
                            }
                            {
                                fs16 [
                                e16
                                ef16
                                af,16
                                g,16 ]
                            }
                            {
                                a,16
                            }
                        }
                    }
                >>

        Set to up, down or none.

        Returns up, down or none.
        """
        return self._direction

    @property
    def pattern(self):
        r'''Gets pattern.

        Set to pattern or none.

        Returns pattern or none.
        '''
        return self._pattern

    @property
    def start(self):
        r'''Gets start.

        Set to up, down or none.

        Returns up, down or none.
        '''
        return self._start
