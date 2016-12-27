# -*- coding: utf-8 -*-
import abjad


class Alpha(abjad.abctools.AbjadValueObject):
    r'''Alpha.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example:

        ::

            >>> baca.tools.Alpha()
            Alpha()

    Object model of twelve-tone alpha operator.

    Alpha operator switches between the two whole-tone sets:
    ``(1 0 3 2 5 4 7 6 9 8 11 10)``.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        )

    _permutation = (1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10)

    ### SPECIAL METHODS ###

    def __add__(self, operator):
        r'''Composes alpha and `operator`.

        ..  container:: example

            Example segment:

            ::

                >>> items = [0, 2, 4, 5]
                >>> J = abjad.PitchClassSegment(items=items)
                >>> show(J) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = J.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    c'8
                    d'8
                    e'8
                    f'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }
    
            Example operators:

            ::

                >>> alpha = baca.tools.Alpha()
                >>> transposition = abjad.Transposition(n=3)

        ..  container:: example

            Transposition followed by alpha:

            ::

                >>> operator = alpha + transposition
                >>> str(operator)
                'AT3'

            ::

                >>> segment = operator(J)
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    d'8
                    e'8
                    fs'8
                    a'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Alpha followed by transposition:

            ::

                >>> operator = transposition + alpha
                >>> str(operator)
                'T3A'

            ::

                >>> segment = operator(J)
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    e'8
                    fs'8
                    af'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns compound operator:

            ::

                >>> f(operator)
                pitchtools.CompoundOperator(
                    operators=[
                        baca.tools.Alpha(),
                        pitchtools.Transposition(
                            n=3,
                            ),
                        ],
                    )

        '''
        return abjad.pitchtools.CompoundOperator._compose_operators(
            self,
            operator,
            )

    def __call__(self, argment):
        r'''Calls alpha on `argment`.

        ..  container:: example

            Calls alpha on pitch-class:

            ::

                >>> alpha = baca.tools.Alpha()
                >>> alpha(abjad.NumberedPitchClass(6))
                NumberedPitchClass(7)

        ..  container:: example

            Calls alpha on pitch-class segment:

            ::

                >>> pitch_classes = abjad.PitchClassSegment([0, 1, 4, 7])
                >>> alpha(pitch_classes)
                PitchClassSegment([1, 0, 5, 6])

        Returns new object of `argment` type.
        '''
        row = abjad.TwelveToneRow(items=self._permutation)
        if isinstance(argment, abjad.pitchtools.PitchClass):
            argment = abjad.NumberedPitchClass(argment)
            return row([argment])[0]
        elif isinstance(argment, abjad.pitchtools.Pitch):
            argment = abjad.NumberedPitch(argment)
            return row([argment])[0]
        else:
            return row(argment)

    def __str__(self):
        r'''Gets string representation of operator.

        ..  container:: example

            ::

                >>> str(baca.tools.Alpha())
                'A'

        '''
        return 'A'

    ### PRIVATE METHODS ###

    def _get_markup(self, direction=None):
        from abjad.tools import markuptools
        return markuptools.Markup('A', direction=direction)

    def _is_identity_operator(self):
        return False
