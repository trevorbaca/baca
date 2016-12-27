# -*- coding: utf-8 -*-
import abjad
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

    def alpha(self):
        r'''Gets alpha transform of segment.

        ..  container:: example

            Example segment:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> J = baca.pitch_class_segment(items=items, name='J')

            ::

                >>> show(J) # doctest: +SKIP

        ..  container:: example

            Gets alpha transform of segment:

            ..  container:: example

                ::

                    >>> J.alpha()
                    PitchClassSegment([11, 11.5, 7, 6, 11.5, 6], name='A(J)')

                ::

                    >>> segment = J.alpha()
                    >>> show(segment) # doctest: +SKIP

                ..  doctest::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> f(lilypond_file[Voice])
                    \new Voice {
                        b'8
                            ^ \markup {
                                \concat
                                    {
                                        A
                                        \concat
                                            {
                                                \hspace
                                                    #0.4
                                                \bold
                                                    J
                                            }
                                    }
                                }
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
                    PitchClassSegment([11, 11.5, 7, 6, 11.5, 6], name='A(J)')

                ::

                    >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                    >>> show(segment) # doctest: +SKIP

                ..  doctest::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> f(lilypond_file[Voice])
                    \new Voice {
                        b'8
                            ^ \markup {
                                \concat
                                    {
                                        A
                                        \concat
                                            {
                                                \hspace
                                                    #0.4
                                                \bold
                                                    J
                                            }
                                    }
                                }
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
                    PitchClassSegment([10, 10.5, 6, 7, 10.5, 7], name='A(A(J))')

                ::

                    >>> segment = J.alpha().alpha()
                    >>> show(segment) # doctest: +SKIP

                ..  doctest::

                    >>> lilypond_file = segment.__illustrate__()
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
                                                \concat
                                                    {
                                                        \hspace
                                                            #0.4
                                                        \bold
                                                            J
                                                    }
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

            ..  container:: example expression

                ::

                    >>> expression = baca.pitch_class_segment(name='J')
                    >>> expression = expression.alpha()
                    >>> expression = expression.alpha()
                    >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                    PitchClassSegment([10, 10.5, 6, 7, 10.5, 7], name='A(A(J))')

                ::

                    >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                    >>> show(segment) # doctest: +SKIP

                ..  doctest::

                    >>> lilypond_file = segment.__illustrate__()
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
                                                \concat
                                                    {
                                                        \hspace
                                                            #0.4
                                                        \bold
                                                            J
                                                    }
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
        if self._frozen_expression:
            return self._make_callback(inspect.currentframe())
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
        template = 'A({})'
        expression = abjad.Expression()
        expression = expression.wrap_in_list()
        expression = expression.markup_list()
        expression = expression.insert(0, 'A')
        expression = expression.concat()
        segment = abjad.new(self, items=numbers, name=self._name)
        abjad.Expression._track_expression(
            self,
            segment,
            'alpha',
            formula_markup_expression=expression,
            formula_string_template=template,
            )
        return segment


def _pitch_class_segment(items=None, **keywords):
    if items:
        return PitchClassSegment(items=items, **keywords)
    expression = abjad.Expression()
    return expression._initialize(
        PitchClassSegment,
        formula_string_template='pcs({})',
        module_names=['baca'],
        **keywords
        )
