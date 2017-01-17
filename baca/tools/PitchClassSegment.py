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
                >>> f(lilypond_file[Voice])
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
                >>> f(lilypond_file[Voice])
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
                    >>> f(lilypond_file[Voice])
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
                    >>> f(lilypond_file[Voice])
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
                    >>> f(lilypond_file[Voice])
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
                    >>> f(lilypond_file[Voice])
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
