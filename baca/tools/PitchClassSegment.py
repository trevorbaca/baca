# -*- coding: utf-8 -*-
import abjad
import baca
import inspect


class PitchClassSegment(abjad.PitchClassSegment):
    r'''Pitch-class segment.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Initializes segment:

        ..  container:: example

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = baca.pitch_class_segment(items=items)
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[abjad.Voice])
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

            ::

                >>> expression = baca.pitch_class_segment()
                >>> segment = expression(items=[-2, -1.5, 6, 7, -1.5, 7])
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[abjad.Voice])
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

    __documentation_section__ = 'Utilities'

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when segment equals `argument`. Otherwise false.

        ..  container:: example

            Works with Abjad pitch-class segments:

            ::

                >>> segment_1 = abjad.PitchClassSegment([0, 1, 2, 3])
                >>> segment_2 = baca.PitchClassSegment([0, 1, 2, 3])

            ::

                >>> segment_1 == segment_2
                True

            ::

                >>> segment_2 == segment_1
                True

        '''
        if (not issubclass(type(argument), type(self)) and
            not issubclass(type(self), type(argument))):
            return False
        return self._collection == argument._collection

    ### PUBLIC METHODS ###

    @abjad.expressiontools.Signature(is_operator=True, method_name='A')
    def alpha(self):
        r'''Gets alpha transform of segment.

        ..  container:: example

            Example segment:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> J = baca.pitch_class_segment(items=items)

            ::

                >>> show(J) # doctest: +SKIP

        ..  container:: example

            Gets alpha transform of segment:

            ..  container:: example

                ::

                    >>> J.alpha()
                    PitchClassSegment([11, 11.5, 7, 6, 11.5, 6])

                ::

                    >>> segment = J.alpha()
                    >>> show(segment) # doctest: +SKIP

                ..  doctest::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> f(lilypond_file[abjad.Voice])
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

                ::

                    >>> expression = baca.pitch_class_segment(name='J')
                    >>> expression = expression.alpha()
                    >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                    PitchClassSegment([11, 11.5, 7, 6, 11.5, 6])

                ::

                    >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                    >>> show(segment) # doctest: +SKIP

                ..  doctest::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> f(lilypond_file[abjad.Voice])
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

                ::

                    >>> J.alpha().alpha()
                    PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                ::

                    >>> segment = J.alpha().alpha()
                    >>> show(segment) # doctest: +SKIP

                ..  doctest::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> f(lilypond_file[abjad.Voice])
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

                ::

                    >>> segment == J
                    True

            ..  container:: example expression

                ::

                    >>> expression = baca.pitch_class_segment(name='J')
                    >>> expression = expression.alpha()
                    >>> expression = expression.alpha()

                ::

                    >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                    PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                ::

                    >>> expression.get_string()
                    'A(A(J))'

                ::

                    >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                    >>> markup = expression.get_markup()
                    >>> show(segment, figure_name=markup) # doctest: +SKIP

                ..  doctest::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> f(lilypond_file[abjad.Voice])
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

                ::

                    >>> segment == J
                    True

        ..  container:: example

            Returns pitch-class segment:

            ::

                >>> isinstance(segment, baca.PitchClassSegment)
                True

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        numbers = []
        for pc in self:
            pc = abs(float(pc))
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

    def chord(self):
        r'''Changes segment to set.

        ..  container:: example

            ::

                >>> segment = baca.pitch_class_segment([-2, -1.5, 6, 7])

            ::

                >>> segment.chord()
                PitchClassSet([6, 7, 10, 10.5])

            ::

                >>> show(segment.chord()) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.chord().__illustrate__()
                >>> f(lilypond_file[abjad.Voice])
                \new Voice {
                    <fs' g' bf' bqf'>1
                }

        Returns pitch-class set.
        '''
        return baca.PitchClassSet(
            items=self,
            item_class=self.item_class,
            )
        
    def has_duplicates(self):
        r'''Is true when pitch-class segment has duplicates.

        ..  container:: example

            ::

                >>> items = [-2, -1.5, 6, 7]
                >>> segment = baca.pitch_class_segment(items=items)
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[abjad.Voice])
                \new Voice {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            ::

                >>> segment.has_duplicates()
                False

        ..  container:: example

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = baca.pitch_class_segment(items=items)
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[abjad.Voice])
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

            ::

                >>> segment.has_duplicates()
                True

        Returns true or false.
        '''
        return not len(set(self)) == len(self)

    def has_repeats(self):
        r'''Is true when pitch-class segment has repeats.

        ..  container:: example

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = baca.pitch_class_segment(items=items)
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[abjad.Voice])
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

            ::

                >>> segment.has_repeats()
                False                

        ..  container:: example

            ::

                >>> items = [-2, -1.5, 6, 7, 7]
                >>> segment = baca.pitch_class_segment(items=items)
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[abjad.Voice])
                \new Voice {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            ::

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

    def space_down(self, bass=None, semitones=None, soprano=None):
        r'''Spaces segment down.

        ..  container:: example

            ::

                >>> segment = baca.pitch_class_segment([10, 11, 5, 6, 7])
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[abjad.Voice])
                \new Voice {
                    bf'8
                    b'8
                    f'8
                    fs'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            ::

                >>> segment.space_down(bass=6, soprano=7)
                PitchSegment([19, 17, 11, 10, 6])

            ::

                >>> segment = segment.space_down(bass=6, soprano=7)
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                } <<
                    \new PianoStaff <<
                        \context Staff = "treble" {
                            \clef "treble"
                            g''1 * 1/8
                            f''1 * 1/8
                            b'1 * 1/8
                            bf'1 * 1/8
                            fs'1 * 1/8
                        }
                        \context Staff = "bass" {
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
        specifier = baca.tools.ChordalSpacingSpecifier(
            bass=bass,
            direction=Down,
            minimum_semitones=semitones,
            soprano=soprano,
            )
        segments = specifier([self])
        assert len(segments) == 1, repr(segments)
        segment = segments[0]
        if not isinstance(segment, baca.PitchSegment):
            message = 'must be pitch segment: {!r}.'
            message = message.format(segment)
            raise TypeError(message)
        return segment

    def space_up(self, bass=None, semitones=None, soprano=None):
        r'''Spaces segment up.

        ..  container:: example

            ::

                >>> segment = baca.pitch_class_segment([10, 11, 5, 6, 7])
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[abjad.Voice])
                \new Voice {
                    bf'8
                    b'8
                    f'8
                    fs'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            ::

                >>> segment.space_up(bass=6, soprano=7)
                PitchSegment([6, 10, 11, 17, 19])

            ::

                >>> segment = segment.space_up(bass=6, soprano=7)
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                } <<
                    \new PianoStaff <<
                        \context Staff = "treble" {
                            \clef "treble"
                            fs'1 * 1/8
                            bf'1 * 1/8
                            b'1 * 1/8
                            f''1 * 1/8
                            g''1 * 1/8
                        }
                        \context Staff = "bass" {
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
        specifier = baca.tools.ChordalSpacingSpecifier(
            bass=bass,
            direction=Up,
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
        markup_expression=abjad.Expression().markup(),
        module_names=['baca'],
        string_template='{}',
        **keywords
        )
    expression = expression.append_callback(callback)
    return abjad.new(expression, proxy_class=PitchClassSegment)
