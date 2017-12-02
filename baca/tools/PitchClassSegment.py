import abjad
import baca
import inspect


class PitchClassSegment(abjad.PitchClassSegment):
    r'''Pitch-class segment.

    ..  container:: example

        Initializes segment:

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = baca.pitch_class_segment(items=items)
            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice], strict=True)
                \new Voice {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example expression

            >>> expression = baca.pitch_class_segment()
            >>> segment = expression(items=[-2, -1.5, 6, 7, -1.5, 7])
            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice], strict=True)
                \new Voice {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when segment equals `argument`. Otherwise false.

        ..  container:: example

            Works with Abjad pitch-class segments:

            >>> segment_1 = abjad.PitchClassSegment([0, 1, 2, 3])
            >>> segment_2 = baca.PitchClassSegment([0, 1, 2, 3])

            >>> segment_1 == segment_2
            True

            >>> segment_2 == segment_1
            True

        '''
        if (not issubclass(type(argument), type(self)) and
            not issubclass(type(self), type(argument))):
            return False
        return self._collection == argument._collection

    ### PUBLIC METHODS ###

    @abjad.Signature(is_operator=True, method_name='A')
    def alpha(self):
        r'''Gets alpha transform of segment.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = baca.pitch_class_segment(items=items)

            >>> abjad.show(J) # doctest: +SKIP

        ..  container:: example

            Gets alpha transform of segment:

            ..  container:: example

                >>> J.alpha()
                PitchClassSegment([11, 11.5, 7, 6, 11.5, 6])

                >>> segment = J.alpha()
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice], strict=True)
                    \new Voice {
                        b'8
                        bqs'8
                        g'8
                        fs'8
                        bqs'8
                        fs'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = baca.pitch_class_segment(name='J')
                >>> expression = expression.alpha()
                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([11, 11.5, 7, 6, 11.5, 6])

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice], strict=True)
                    \new Voice {
                        b'8
                        bqs'8
                        g'8
                        fs'8
                        bqs'8
                        fs'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Gets alpha transform of alpha transform of segment:

            ..  container:: example

                >>> J.alpha().alpha()
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> segment = J.alpha().alpha()
                >>> abjad.show(segment) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice], strict=True)
                    \new Voice {
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

                >>> segment == J
                True

            ..  container:: example expression

                >>> expression = baca.pitch_class_segment(name='J')
                >>> expression = expression.alpha()
                >>> expression = expression.alpha()

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> expression.get_string()
                'A(A(J))'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice], strict=True)
                    \new Voice {
                        bf'8
                        ^ \markup {
                            \concat
                                {
                                    A
                                    \concat
                                        {
                                            A
                                            \bold
                                                J
                                        }
                                }
                            }
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

                >>> segment == J
                True

        ..  container:: example

            Returns pitch-class segment:

            >>> isinstance(segment, baca.PitchClassSegment)
            True

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        numbers = []
        for pc in self:
            pc = abs(float(pc.number))
            is_integer = True
            if not abjad.mathtools.is_integer_equivalent_number(pc):
                is_integer = False
                fraction_part = pc - int(pc)
                pc = int(pc)
            if abs(pc) % 2 == 0:
                number = (abs(pc) + 1) % 12
            else:
                number = abs(pc) - 1
            if not is_integer:
                number += fraction_part
            else:
                number = int(number)
            numbers.append(number)
        return type(self)(items=numbers)

    def arpeggiate_down(self):
        r"""Arpeggiates pitch-class segment down.

        ..  container:: example

            >>> segment = baca.pitch_class_segment([6, 0, 4, 5, 8])

            >>> segment.arpeggiate_down()
            PitchSegment([42, 36, 28, 17, 8])

            >>> abjad.show(segment.arpeggiate_down()) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.arpeggiate_down().__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=True)
                \new PianoStaff <<
                    \context Staff = "Treble Staff" {
                        \clef "treble"
                        fs''''1 * 1/8
                        c''''1 * 1/8
                        e'''1 * 1/8
                        f''1 * 1/8
                        af'1 * 1/8
                    }
                    \context Staff = "Bass Staff" {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns pitch segment.
        """
        specifier = baca.ArpeggiationSpacingSpecifier(direction=Down)
        result = specifier([self])
        assert len(result) == 1
        segment = result[0]
        assert isinstance(segment, baca.PitchSegment), repr(segment)
        return segment

    def arpeggiate_up(self):
        r'''Arpeggiates pitch-class segment up.

        ..  container:: example

            >>> segment = baca.pitch_class_segment([6, 0, 4, 5, 8])

            >>> segment.arpeggiate_up()
            PitchSegment([6, 12, 16, 17, 20])

            >>> abjad.show(segment.arpeggiate_up()) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.arpeggiate_up().__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=True)
                \new PianoStaff <<
                    \context Staff = "Treble Staff" {
                        \clef "treble"
                        fs'1 * 1/8
                        c''1 * 1/8
                        e''1 * 1/8
                        f''1 * 1/8
                        af''1 * 1/8
                    }
                    \context Staff = "Bass Staff" {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns pitch segment.
        '''
        specifier = baca.ArpeggiationSpacingSpecifier(direction=abjad.Up)
        result = specifier([self])
        assert len(result) == 1
        segment = result[0]
        assert isinstance(segment, baca.PitchSegment), repr(segment)
        return segment

    def chord(self):
        r'''Changes segment to set.

        ..  container:: example

            >>> segment = baca.pitch_class_segment([-2, -1.5, 6, 7])

            >>> segment.chord()
            PitchClassSet([6, 7, 10, 10.5])

            >>> abjad.show(segment.chord()) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.chord().__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice], strict=True)
                \new Voice {
                    <fs' g' bf' bqf'>1
                }

        Returns pitch-class set.
        '''
        return baca.PitchClassSet(
            items=self,
            item_class=self.item_class,
            )

    def get_matching_transforms(
        self,
        segment_2,
        inversion=False,
        multiplication=False,
        retrograde=False,
        rotation=False,
        transposition=False,
        ):
        r'''Gets transforms of segment that match `segment_2`.

        ..  container:: example

            Example segments:

            >>> items = [-2, -1, 6, 7, -1, 7]
            >>> segment_1 = baca.PitchClassSegment(items=items)
            >>> abjad.show(segment) # doctest: +SKIP

            >>> items = [9, 2, 1, 6, 2, 6]
            >>> segment_2 = baca.PitchClassSegment(items=items)
            >>> abjad.show(segment_2) # doctest: +SKIP

        ..  container:: example

            Gets matching transforms:

            >>> transforms = segment_1.get_matching_transforms(
            ...     segment_2,
            ...     inversion=True,
            ...     multiplication=True,
            ...     retrograde=True,
            ...     rotation=False,
            ...     transposition=True,
            ...     )
            >>> for operator, transform in transforms:
            ...     print(str(operator), str(transform))
            ...
            M5T11 PC<9, 2, 1, 6, 2, 6>
            M7T1I PC<9, 2, 1, 6, 2, 6>

            >>> transforms = segment_2.get_matching_transforms(
            ...     segment_1,
            ...     inversion=True,
            ...     multiplication=True,
            ...     retrograde=True,
            ...     rotation=False,
            ...     transposition=True,
            ...     )
            >>> for operator, transform in transforms:
            ...     print(str(operator), str(transform))
            ...
            M5T5 PC<10, 11, 6, 7, 11, 7>
            M7T7I PC<10, 11, 6, 7, 11, 7>

        ..  container:: example

            No matching transforms. Segments of differing lengths never
            transform into each other:

            >>> segment_2 = baca.PitchClassSegment(items=[0, 1, 2])
            >>> segment_2.get_matching_transforms(
            ...     segment_1,
            ...     inversion=True,
            ...     multiplication=True,
            ...     retrograde=True,
            ...     rotation=False,
            ...     transposition=True,
            ...     )
            []

        ..  container:: example

            Returns list of pairs:

            >>> isinstance(transforms, list)
            True

        '''
        result = []
        if not len(self) == len(segment_2):
            return result
        transforms = self.get_transforms(
            inversion=inversion,
            multiplication=multiplication,
            retrograde=retrograde,
            rotation=rotation,
            transposition=transposition,
            )
        for operator, transform in transforms:
            if transform == segment_2:
                result.append((operator, transform))
        return result

    def get_transforms(
        self,
        inversion=False,
        multiplication=False,
        retrograde=False,
        rotation=False,
        show_identity_operators=False,
        transposition=False,
        ):
        r'''Gets transforms of `segment`.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1, 6, 7, -1, 7]
            >>> J = baca.PitchClassSegment(items=items)
            >>> abjad.show(J) # doctest: +SKIP

        ..  container:: example

            Gets identity transform of segment:

            >>> transforms = J.get_transforms()

            >>> for operator, transform in transforms:
            ...     print(str(transform))
            PC<10, 11, 6, 7, 11, 7>

        ..  container:: example

            Gets transpositions of segment:

            >>> transforms = J.get_transforms(transposition=True)

            >>> for i, pair in enumerate(transforms):
            ...     rank = i + 1
            ...     operator, transform = pair
            ...     transform = transform._get_padded_string()
            ...     string = '{:3}:{!s:>4} J:  {!s}'
            ...     string = string.format(rank, operator, transform)
            ...     print(string)
            1:     J:  PC<10, 11,  6,  7, 11,  7>
            2:  T1 J:  PC<11,  0,  7,  8,  0,  8>
            3:  T2 J:  PC< 0,  1,  8,  9,  1,  9>
            4:  T3 J:  PC< 1,  2,  9, 10,  2, 10>
            5:  T4 J:  PC< 2,  3, 10, 11,  3, 11>
            6:  T5 J:  PC< 3,  4, 11,  0,  4,  0>
            7:  T6 J:  PC< 4,  5,  0,  1,  5,  1>
            8:  T7 J:  PC< 5,  6,  1,  2,  6,  2>
            9:  T8 J:  PC< 6,  7,  2,  3,  7,  3>
            10:  T9 J:  PC< 7,  8,  3,  4,  8,  4>
            11: T10 J:  PC< 8,  9,  4,  5,  9,  5>
            12: T11 J:  PC< 9, 10,  5,  6, 10,  6>

        ..  container:: example

            Gets all transforms of segment (without rotation):

            >>> transforms = J.get_transforms(
            ...     inversion=True,
            ...     multiplication=True,
            ...     retrograde=True,
            ...     transposition=True,
            ...     )

            >>> for i, pair in enumerate(transforms):
            ...     rank = i + 1
            ...     operator, transform = pair
            ...     transform = transform._get_padded_string()
            ...     string = '{:3}:{!s:>10} J:  {!s}'
            ...     string = string.format(rank, operator, transform)
            ...     print(string)
            1:           J:  PC<10, 11,  6,  7, 11,  7>
            2:         R J:  PC< 7, 11,  7,  6, 11, 10>
            3:        T1 J:  PC<11,  0,  7,  8,  0,  8>
            4:       RT1 J:  PC< 8,  0,  8,  7,  0, 11>
            5:        T2 J:  PC< 0,  1,  8,  9,  1,  9>
            6:       RT2 J:  PC< 9,  1,  9,  8,  1,  0>
            7:        T3 J:  PC< 1,  2,  9, 10,  2, 10>
            8:       RT3 J:  PC<10,  2, 10,  9,  2,  1>
            9:        T4 J:  PC< 2,  3, 10, 11,  3, 11>
            10:       RT4 J:  PC<11,  3, 11, 10,  3,  2>
            11:        T5 J:  PC< 3,  4, 11,  0,  4,  0>
            12:       RT5 J:  PC< 0,  4,  0, 11,  4,  3>
            13:        T6 J:  PC< 4,  5,  0,  1,  5,  1>
            14:       RT6 J:  PC< 1,  5,  1,  0,  5,  4>
            15:        T7 J:  PC< 5,  6,  1,  2,  6,  2>
            16:       RT7 J:  PC< 2,  6,  2,  1,  6,  5>
            17:        T8 J:  PC< 6,  7,  2,  3,  7,  3>
            18:       RT8 J:  PC< 3,  7,  3,  2,  7,  6>
            19:        T9 J:  PC< 7,  8,  3,  4,  8,  4>
            20:       RT9 J:  PC< 4,  8,  4,  3,  8,  7>
            21:       T10 J:  PC< 8,  9,  4,  5,  9,  5>
            22:      RT10 J:  PC< 5,  9,  5,  4,  9,  8>
            23:       T11 J:  PC< 9, 10,  5,  6, 10,  6>
            24:      RT11 J:  PC< 6, 10,  6,  5, 10,  9>
            25:         I J:  PC< 2,  1,  6,  5,  1,  5>
            26:        RI J:  PC< 5,  1,  5,  6,  1,  2>
            27:       T1I J:  PC< 3,  2,  7,  6,  2,  6>
            28:      RT1I J:  PC< 6,  2,  6,  7,  2,  3>
            29:       T2I J:  PC< 4,  3,  8,  7,  3,  7>
            30:      RT2I J:  PC< 7,  3,  7,  8,  3,  4>
            31:       T3I J:  PC< 5,  4,  9,  8,  4,  8>
            32:      RT3I J:  PC< 8,  4,  8,  9,  4,  5>
            33:       T4I J:  PC< 6,  5, 10,  9,  5,  9>
            34:      RT4I J:  PC< 9,  5,  9, 10,  5,  6>
            35:       T5I J:  PC< 7,  6, 11, 10,  6, 10>
            36:      RT5I J:  PC<10,  6, 10, 11,  6,  7>
            37:       T6I J:  PC< 8,  7,  0, 11,  7, 11>
            38:      RT6I J:  PC<11,  7, 11,  0,  7,  8>
            39:       T7I J:  PC< 9,  8,  1,  0,  8,  0>
            40:      RT7I J:  PC< 0,  8,  0,  1,  8,  9>
            41:       T8I J:  PC<10,  9,  2,  1,  9,  1>
            42:      RT8I J:  PC< 1,  9,  1,  2,  9, 10>
            43:       T9I J:  PC<11, 10,  3,  2, 10,  2>
            44:      RT9I J:  PC< 2, 10,  2,  3, 10, 11>
            45:      T10I J:  PC< 0, 11,  4,  3, 11,  3>
            46:     RT10I J:  PC< 3, 11,  3,  4, 11,  0>
            47:      T11I J:  PC< 1,  0,  5,  4,  0,  4>
            48:     RT11I J:  PC< 4,  0,  4,  5,  0,  1>
            49:           J:  PC<10, 11,  6,  7, 11,  7>
            50:         R J:  PC< 7, 11,  7,  6, 11, 10>
            51:        T1 J:  PC<11,  0,  7,  8,  0,  8>
            52:       RT1 J:  PC< 8,  0,  8,  7,  0, 11>
            53:        T2 J:  PC< 0,  1,  8,  9,  1,  9>
            54:       RT2 J:  PC< 9,  1,  9,  8,  1,  0>
            55:        T3 J:  PC< 1,  2,  9, 10,  2, 10>
            56:       RT3 J:  PC<10,  2, 10,  9,  2,  1>
            57:        T4 J:  PC< 2,  3, 10, 11,  3, 11>
            58:       RT4 J:  PC<11,  3, 11, 10,  3,  2>
            59:        T5 J:  PC< 3,  4, 11,  0,  4,  0>
            60:       RT5 J:  PC< 0,  4,  0, 11,  4,  3>
            61:        T6 J:  PC< 4,  5,  0,  1,  5,  1>
            62:       RT6 J:  PC< 1,  5,  1,  0,  5,  4>
            63:        T7 J:  PC< 5,  6,  1,  2,  6,  2>
            64:       RT7 J:  PC< 2,  6,  2,  1,  6,  5>
            65:        T8 J:  PC< 6,  7,  2,  3,  7,  3>
            66:       RT8 J:  PC< 3,  7,  3,  2,  7,  6>
            67:        T9 J:  PC< 7,  8,  3,  4,  8,  4>
            68:       RT9 J:  PC< 4,  8,  4,  3,  8,  7>
            69:       T10 J:  PC< 8,  9,  4,  5,  9,  5>
            70:      RT10 J:  PC< 5,  9,  5,  4,  9,  8>
            71:       T11 J:  PC< 9, 10,  5,  6, 10,  6>
            72:      RT11 J:  PC< 6, 10,  6,  5, 10,  9>
            73:         I J:  PC< 2,  1,  6,  5,  1,  5>
            74:        RI J:  PC< 5,  1,  5,  6,  1,  2>
            75:       T1I J:  PC< 3,  2,  7,  6,  2,  6>
            76:      RT1I J:  PC< 6,  2,  6,  7,  2,  3>
            77:       T2I J:  PC< 4,  3,  8,  7,  3,  7>
            78:      RT2I J:  PC< 7,  3,  7,  8,  3,  4>
            79:       T3I J:  PC< 5,  4,  9,  8,  4,  8>
            80:      RT3I J:  PC< 8,  4,  8,  9,  4,  5>
            81:       T4I J:  PC< 6,  5, 10,  9,  5,  9>
            82:      RT4I J:  PC< 9,  5,  9, 10,  5,  6>
            83:       T5I J:  PC< 7,  6, 11, 10,  6, 10>
            84:      RT5I J:  PC<10,  6, 10, 11,  6,  7>
            85:       T6I J:  PC< 8,  7,  0, 11,  7, 11>
            86:      RT6I J:  PC<11,  7, 11,  0,  7,  8>
            87:       T7I J:  PC< 9,  8,  1,  0,  8,  0>
            88:      RT7I J:  PC< 0,  8,  0,  1,  8,  9>
            89:       T8I J:  PC<10,  9,  2,  1,  9,  1>
            90:      RT8I J:  PC< 1,  9,  1,  2,  9, 10>
            91:       T9I J:  PC<11, 10,  3,  2, 10,  2>
            92:      RT9I J:  PC< 2, 10,  2,  3, 10, 11>
            93:      T10I J:  PC< 0, 11,  4,  3, 11,  3>
            94:     RT10I J:  PC< 3, 11,  3,  4, 11,  0>
            95:      T11I J:  PC< 1,  0,  5,  4,  0,  4>
            96:     RT11I J:  PC< 4,  0,  4,  5,  0,  1>
            97:        M5 J:  PC< 2,  7,  6, 11,  7, 11>
            98:       RM5 J:  PC<11,  7, 11,  6,  7,  2>
            99:      M5T1 J:  PC< 7,  0, 11,  4,  0,  4>
            100:     RM5T1 J:  PC< 4,  0,  4, 11,  0,  7>
            101:      M5T2 J:  PC< 0,  5,  4,  9,  5,  9>
            102:     RM5T2 J:  PC< 9,  5,  9,  4,  5,  0>
            103:      M5T3 J:  PC< 5, 10,  9,  2, 10,  2>
            104:     RM5T3 J:  PC< 2, 10,  2,  9, 10,  5>
            105:      M5T4 J:  PC<10,  3,  2,  7,  3,  7>
            106:     RM5T4 J:  PC< 7,  3,  7,  2,  3, 10>
            107:      M5T5 J:  PC< 3,  8,  7,  0,  8,  0>
            108:     RM5T5 J:  PC< 0,  8,  0,  7,  8,  3>
            109:      M5T6 J:  PC< 8,  1,  0,  5,  1,  5>
            110:     RM5T6 J:  PC< 5,  1,  5,  0,  1,  8>
            111:      M5T7 J:  PC< 1,  6,  5, 10,  6, 10>
            112:     RM5T7 J:  PC<10,  6, 10,  5,  6,  1>
            113:      M5T8 J:  PC< 6, 11, 10,  3, 11,  3>
            114:     RM5T8 J:  PC< 3, 11,  3, 10, 11,  6>
            115:      M5T9 J:  PC<11,  4,  3,  8,  4,  8>
            116:     RM5T9 J:  PC< 8,  4,  8,  3,  4, 11>
            117:     M5T10 J:  PC< 4,  9,  8,  1,  9,  1>
            118:    RM5T10 J:  PC< 1,  9,  1,  8,  9,  4>
            119:     M5T11 J:  PC< 9,  2,  1,  6,  2,  6>
            120:    RM5T11 J:  PC< 6,  2,  6,  1,  2,  9>
            121:       M5I J:  PC<10,  5,  6,  1,  5,  1>
            122:      RM5I J:  PC< 1,  5,  1,  6,  5, 10>
            123:     M5T1I J:  PC< 3, 10, 11,  6, 10,  6>
            124:    RM5T1I J:  PC< 6, 10,  6, 11, 10,  3>
            125:     M5T2I J:  PC< 8,  3,  4, 11,  3, 11>
            126:    RM5T2I J:  PC<11,  3, 11,  4,  3,  8>
            127:     M5T3I J:  PC< 1,  8,  9,  4,  8,  4>
            128:    RM5T3I J:  PC< 4,  8,  4,  9,  8,  1>
            129:     M5T4I J:  PC< 6,  1,  2,  9,  1,  9>
            130:    RM5T4I J:  PC< 9,  1,  9,  2,  1,  6>
            131:     M5T5I J:  PC<11,  6,  7,  2,  6,  2>
            132:    RM5T5I J:  PC< 2,  6,  2,  7,  6, 11>
            133:     M5T6I J:  PC< 4, 11,  0,  7, 11,  7>
            134:    RM5T6I J:  PC< 7, 11,  7,  0, 11,  4>
            135:     M5T7I J:  PC< 9,  4,  5,  0,  4,  0>
            136:    RM5T7I J:  PC< 0,  4,  0,  5,  4,  9>
            137:     M5T8I J:  PC< 2,  9, 10,  5,  9,  5>
            138:    RM5T8I J:  PC< 5,  9,  5, 10,  9,  2>
            139:     M5T9I J:  PC< 7,  2,  3, 10,  2, 10>
            140:    RM5T9I J:  PC<10,  2, 10,  3,  2,  7>
            141:    M5T10I J:  PC< 0,  7,  8,  3,  7,  3>
            142:   RM5T10I J:  PC< 3,  7,  3,  8,  7,  0>
            143:    M5T11I J:  PC< 5,  0,  1,  8,  0,  8>
            144:   RM5T11I J:  PC< 8,  0,  8,  1,  0,  5>
            145:        M7 J:  PC<10,  5,  6,  1,  5,  1>
            146:       RM7 J:  PC< 1,  5,  1,  6,  5, 10>
            147:      M7T1 J:  PC< 5,  0,  1,  8,  0,  8>
            148:     RM7T1 J:  PC< 8,  0,  8,  1,  0,  5>
            149:      M7T2 J:  PC< 0,  7,  8,  3,  7,  3>
            150:     RM7T2 J:  PC< 3,  7,  3,  8,  7,  0>
            151:      M7T3 J:  PC< 7,  2,  3, 10,  2, 10>
            152:     RM7T3 J:  PC<10,  2, 10,  3,  2,  7>
            153:      M7T4 J:  PC< 2,  9, 10,  5,  9,  5>
            154:     RM7T4 J:  PC< 5,  9,  5, 10,  9,  2>
            155:      M7T5 J:  PC< 9,  4,  5,  0,  4,  0>
            156:     RM7T5 J:  PC< 0,  4,  0,  5,  4,  9>
            157:      M7T6 J:  PC< 4, 11,  0,  7, 11,  7>
            158:     RM7T6 J:  PC< 7, 11,  7,  0, 11,  4>
            159:      M7T7 J:  PC<11,  6,  7,  2,  6,  2>
            160:     RM7T7 J:  PC< 2,  6,  2,  7,  6, 11>
            161:      M7T8 J:  PC< 6,  1,  2,  9,  1,  9>
            162:     RM7T8 J:  PC< 9,  1,  9,  2,  1,  6>
            163:      M7T9 J:  PC< 1,  8,  9,  4,  8,  4>
            164:     RM7T9 J:  PC< 4,  8,  4,  9,  8,  1>
            165:     M7T10 J:  PC< 8,  3,  4, 11,  3, 11>
            166:    RM7T10 J:  PC<11,  3, 11,  4,  3,  8>
            167:     M7T11 J:  PC< 3, 10, 11,  6, 10,  6>
            168:    RM7T11 J:  PC< 6, 10,  6, 11, 10,  3>
            169:       M7I J:  PC< 2,  7,  6, 11,  7, 11>
            170:      RM7I J:  PC<11,  7, 11,  6,  7,  2>
            171:     M7T1I J:  PC< 9,  2,  1,  6,  2,  6>
            172:    RM7T1I J:  PC< 6,  2,  6,  1,  2,  9>
            173:     M7T2I J:  PC< 4,  9,  8,  1,  9,  1>
            174:    RM7T2I J:  PC< 1,  9,  1,  8,  9,  4>
            175:     M7T3I J:  PC<11,  4,  3,  8,  4,  8>
            176:    RM7T3I J:  PC< 8,  4,  8,  3,  4, 11>
            177:     M7T4I J:  PC< 6, 11, 10,  3, 11,  3>
            178:    RM7T4I J:  PC< 3, 11,  3, 10, 11,  6>
            179:     M7T5I J:  PC< 1,  6,  5, 10,  6, 10>
            180:    RM7T5I J:  PC<10,  6, 10,  5,  6,  1>
            181:     M7T6I J:  PC< 8,  1,  0,  5,  1,  5>
            182:    RM7T6I J:  PC< 5,  1,  5,  0,  1,  8>
            183:     M7T7I J:  PC< 3,  8,  7,  0,  8,  0>
            184:    RM7T7I J:  PC< 0,  8,  0,  7,  8,  3>
            185:     M7T8I J:  PC<10,  3,  2,  7,  3,  7>
            186:    RM7T8I J:  PC< 7,  3,  7,  2,  3, 10>
            187:     M7T9I J:  PC< 5, 10,  9,  2, 10,  2>
            188:    RM7T9I J:  PC< 2, 10,  2,  9, 10,  5>
            189:    M7T10I J:  PC< 0,  5,  4,  9,  5,  9>
            190:   RM7T10I J:  PC< 9,  5,  9,  4,  5,  0>
            191:    M7T11I J:  PC< 7,  0, 11,  4,  0,  4>
            192:   RM7T11I J:  PC< 4,  0,  4, 11,  0,  7>
            193:       M11 J:  PC< 2,  1,  6,  5,  1,  5>
            194:      RM11 J:  PC< 5,  1,  5,  6,  1,  2>
            195:     M11T1 J:  PC< 1,  0,  5,  4,  0,  4>
            196:    RM11T1 J:  PC< 4,  0,  4,  5,  0,  1>
            197:     M11T2 J:  PC< 0, 11,  4,  3, 11,  3>
            198:    RM11T2 J:  PC< 3, 11,  3,  4, 11,  0>
            199:     M11T3 J:  PC<11, 10,  3,  2, 10,  2>
            200:    RM11T3 J:  PC< 2, 10,  2,  3, 10, 11>
            201:     M11T4 J:  PC<10,  9,  2,  1,  9,  1>
            202:    RM11T4 J:  PC< 1,  9,  1,  2,  9, 10>
            203:     M11T5 J:  PC< 9,  8,  1,  0,  8,  0>
            204:    RM11T5 J:  PC< 0,  8,  0,  1,  8,  9>
            205:     M11T6 J:  PC< 8,  7,  0, 11,  7, 11>
            206:    RM11T6 J:  PC<11,  7, 11,  0,  7,  8>
            207:     M11T7 J:  PC< 7,  6, 11, 10,  6, 10>
            208:    RM11T7 J:  PC<10,  6, 10, 11,  6,  7>
            209:     M11T8 J:  PC< 6,  5, 10,  9,  5,  9>
            210:    RM11T8 J:  PC< 9,  5,  9, 10,  5,  6>
            211:     M11T9 J:  PC< 5,  4,  9,  8,  4,  8>
            212:    RM11T9 J:  PC< 8,  4,  8,  9,  4,  5>
            213:    M11T10 J:  PC< 4,  3,  8,  7,  3,  7>
            214:   RM11T10 J:  PC< 7,  3,  7,  8,  3,  4>
            215:    M11T11 J:  PC< 3,  2,  7,  6,  2,  6>
            216:   RM11T11 J:  PC< 6,  2,  6,  7,  2,  3>
            217:      M11I J:  PC<10, 11,  6,  7, 11,  7>
            218:     RM11I J:  PC< 7, 11,  7,  6, 11, 10>
            219:    M11T1I J:  PC< 9, 10,  5,  6, 10,  6>
            220:   RM11T1I J:  PC< 6, 10,  6,  5, 10,  9>
            221:    M11T2I J:  PC< 8,  9,  4,  5,  9,  5>
            222:   RM11T2I J:  PC< 5,  9,  5,  4,  9,  8>
            223:    M11T3I J:  PC< 7,  8,  3,  4,  8,  4>
            224:   RM11T3I J:  PC< 4,  8,  4,  3,  8,  7>
            225:    M11T4I J:  PC< 6,  7,  2,  3,  7,  3>
            226:   RM11T4I J:  PC< 3,  7,  3,  2,  7,  6>
            227:    M11T5I J:  PC< 5,  6,  1,  2,  6,  2>
            228:   RM11T5I J:  PC< 2,  6,  2,  1,  6,  5>
            229:    M11T6I J:  PC< 4,  5,  0,  1,  5,  1>
            230:   RM11T6I J:  PC< 1,  5,  1,  0,  5,  4>
            231:    M11T7I J:  PC< 3,  4, 11,  0,  4,  0>
            232:   RM11T7I J:  PC< 0,  4,  0, 11,  4,  3>
            233:    M11T8I J:  PC< 2,  3, 10, 11,  3, 11>
            234:   RM11T8I J:  PC<11,  3, 11, 10,  3,  2>
            235:    M11T9I J:  PC< 1,  2,  9, 10,  2, 10>
            236:   RM11T9I J:  PC<10,  2, 10,  9,  2,  1>
            237:   M11T10I J:  PC< 0,  1,  8,  9,  1,  9>
            238:  RM11T10I J:  PC< 9,  1,  9,  8,  1,  0>
            239:   M11T11I J:  PC<11,  0,  7,  8,  0,  8>
            240:  RM11T11I J:  PC< 8,  0,  8,  7,  0, 11>

        ..  container:: example

            Returns list of pairs:

            >>> isinstance(transforms, list)
            True

        '''
        operators = []
        if transposition:
            for n in range(12):
                operator = abjad.CompoundOperator()
                operator = operator.transpose(n=n)
                operators.append(operator)
        else:
            operator = abjad.CompoundOperator()
            operator = operator.transpose()
            operators.append(operator)
        if inversion:
            operators_ = operators[:]
            for operator in operators:
                operator_ = abjad.CompoundOperator()
                operator_ = operator_.invert()
                foo = list(operator_._operators)
                foo.extend(operator.operators)
                operator_._operators = tuple(foo)
                operators_.append(operator_)
            operators = operators_
        if multiplication:
            operators_ = operators[:]
            for operator in operators:
                operator_ = operator.multiply(n=1)
                operators_.append(operator_)
            for operator in operators:
                operator_ = operator.multiply(n=5)
                operators_.append(operator_)
            for operator in operators:
                operator_ = operator.multiply(n=7)
                operators_.append(operator_)
            for operator in operators:
                operator_ = operator.multiply(n=11)
                operators_.append(operator_)
            operators = operators_
        if retrograde:
            operators_ = []
            for operator in operators:
                operators_.append(operator)
                operator_ = operator.retrograde()
                operators_.append(operator_)
            operators = operators_
        if rotation:
            operators_ = []
            for operator in operators:
                for n in range(len(self)):
                    if rotation is abjad.Left:
                        n *= -1
                    operator_ = operator.rotate(n=n)
                    operators_.append(operator_)
            operators = operators_
        result = []
        for operator in operators:
            transform = operator(self)
            result.append((operator, transform))
        return result

    def has_duplicates(self):
        r'''Is true when pitch-class segment has duplicates.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7]
            >>> segment = baca.pitch_class_segment(items=items)
            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice], strict=True)
                \new Voice {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment.has_duplicates()
            False

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = baca.pitch_class_segment(items=items)
            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice], strict=True)
                \new Voice {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment.has_duplicates()
            True

        Returns true or false.
        '''
        return not len(set(self)) == len(self)

    def has_repeats(self):
        r'''Is true when pitch-class segment has repeats.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = baca.pitch_class_segment(items=items)
            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice], strict=True)
                \new Voice {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment.has_repeats()
            False

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, 7]
            >>> segment = baca.pitch_class_segment(items=items)
            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice], strict=True)
                \new Voice {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment.has_repeats()
            True

        Returns true or false.
        '''
        previous_item = None
        for item in self:
            if item == previous_item:
                return True
            previous_item = item
        return False

    def sequence(self):
        r'''Changes pitch-class segment into a sequence.

        ..  container:: example

            >>> segment = baca.pitch_class_segment([10, 11, 5, 6, 7])
            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice], strict=True)
                \new Voice {
                    bf'8
                    b'8
                    f'8
                    fs'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment.sequence()
            Sequence([NumberedPitchClass(10), NumberedPitchClass(11), NumberedPitchClass(5), NumberedPitchClass(6), NumberedPitchClass(7)])

        Returns sequence.
        '''
        return baca.sequence(self)

    def space_down(self, bass=None, semitones=None, soprano=None):
        r'''Spaces segment down.

        ..  container:: example

            >>> segment = baca.pitch_class_segment([10, 11, 5, 6, 7])
            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice], strict=True)
                \new Voice {
                    bf'8
                    b'8
                    f'8
                    fs'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment.space_down(bass=6, soprano=7)
            PitchSegment([19, 17, 11, 10, 6])

            >>> segment = segment.space_down(bass=6, soprano=7)
            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score], strict=True)
                \new Score \with {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                } <<
                    \new PianoStaff <<
                        \context Staff = "Treble Staff" {
                            \clef "treble"
                            g''1 * 1/8
                            f''1 * 1/8
                            b'1 * 1/8
                            bf'1 * 1/8
                            fs'1 * 1/8
                        }
                        \context Staff = "Bass Staff" {
                            \clef "bass"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                        }
                    >>
                >>

        Returns pitch segment.
        '''
        specifier = baca.ChordalSpacingSpecifier(
            bass=bass,
            direction=Down,
            minimum_semitones=semitones,
            soprano=soprano,
            )
        segments = specifier([self])
        assert len(segments) == 1, repr(segments)
        segment = segments[0]
        if not isinstance(segment, baca.PitchSegment):
            raise TypeError(f'pitch segment only: {segment!r}.')
        return segment

    def space_up(self, bass=None, semitones=None, soprano=None):
        r'''Spaces segment up.

        ..  container:: example

            >>> segment = baca.pitch_class_segment([10, 11, 5, 6, 7])
            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice], strict=True)
                \new Voice {
                    bf'8
                    b'8
                    f'8
                    fs'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment.space_up(bass=6, soprano=7)
            PitchSegment([6, 10, 11, 17, 19])

            >>> segment = segment.space_up(bass=6, soprano=7)
            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score], strict=True)
                \new Score \with {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                } <<
                    \new PianoStaff <<
                        \context Staff = "Treble Staff" {
                            \clef "treble"
                            fs'1 * 1/8
                            bf'1 * 1/8
                            b'1 * 1/8
                            f''1 * 1/8
                            g''1 * 1/8
                        }
                        \context Staff = "Bass Staff" {
                            \clef "bass"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                        }
                    >>
                >>

        Returns pitch segment.
        '''
        specifier = baca.ChordalSpacingSpecifier(
            bass=bass,
            direction=abjad.Up,
            minimum_semitones=semitones,
            soprano=soprano,
            )
        segments = specifier([self])
        assert len(segments) == 1, repr(segments)
        segment = segments[0]
        assert isinstance(segment, baca.PitchSegment)
        return segment


def _pitch_class_segment(items=None, **keywords):
    if items:
        return PitchClassSegment(items=items, **keywords)
    name = keywords.pop('name', None)
    expression = baca.Expression(name=name)
    callback = expression._make_initializer_callback(
        PitchClassSegment,
        module_names=['baca'],
        string_template='{}',
        **keywords
        )
    expression = expression.append_callback(callback)
    return abjad.new(expression, proxy_class=PitchClassSegment)
