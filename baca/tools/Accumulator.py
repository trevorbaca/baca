# -*- coding: utf-8 -*-
import abjad
import copy


class Accumulator(abjad.abctools.AbjadObject):
    r'''Accumulator.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> accumulator = baca.tools.Accumulator(
            ...     [abjad.Transposition(n=3)],
            ...     )

        ::

            >>> f(accumulator)
            Accumulator(expressions=[Transposition(n=3)])

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        '_expressions',
        '_length',
        )

    ### INITIALIZER ###

    def __init__(self, expressions=None, length=None):
        self._expressions = expressions
        self._length = length

    ### SPECIAL METHODS ###

    def __call__(self, input_):
        r'''Calls accumulator on `input_`.

        ..  container:: example

            Transposes by three semitones until identity:

            ::

                >>> accumulator = baca.tools.Accumulator(
                ...     [abjad.Transposition(n=3)],
                ...     )

            ::

                >>> segment = abjad.PitchClassSegment([0, 10, 9])
                >>> results = accumulator(segment)
                >>> for result in results:
                ...     result
                PitchClassSegment([0, 10, 9])
                PitchClassSegment([3, 1, 0])
                PitchClassSegment([6, 4, 3])
                PitchClassSegment([9, 7, 6])

            ::

                >>> segment = abjad.PitchClassSegment([9, 10, 11, 0])
                >>> results = accumulator(segment)
                >>> for result in results:
                ...     result
                PitchClassSegment([9, 10, 11, 0])
                PitchClassSegment([0, 1, 2, 3])
                PitchClassSegment([3, 4, 5, 6])
                PitchClassSegment([6, 7, 8, 9])

        Calls accumulator expressions on `input_` until identity.

        Truncates or stretches to length when length is not none.

        Returns list of accumulated results.
        '''
        original_input = input_
        results = []
        results.append(copy.deepcopy(input_))
        expressions = self._get_expressions()
        while True:
            result = results[-1]
            for expression in expressions:
                result = expression(result)
            if result == original_input:
                break
            results.append(result)
        return results

    def __repr__(self):
        r'''Gets interpreter representation of accumulator.

        ..  container:: example

            ::

                >>> baca.tools.Accumulator(
                ...     [abjad.Transposition(n=3)],
                ...     )
                Accumulator(expressions=[Transposition(n=3)])

        Returns string.
        '''
        superclass = super(Accumulator, self)
        return superclass.__repr__()

    ### PRIVATE METHODS ###

    def _get_expressions(self):
        if self._expressions:
            return self._expressions
        return [self._identity]

    @staticmethod
    def _identity(input_):
        return input_

    ### PUBLIC PROPERTIES ###

    @property
    def expressions(self):
        r'''Gets expressions.

        Defaults to none.

        Set to expressions or none.

        Returns list of expressions or none.
        '''
        return self._expression

    @property
    def length(self):
        r'''Gets length.

        Defaults to none.

        Set to nonnegative integer or none.

        Returns nonnegative integer or none.
        '''
        return self._length


def _accumulate(expressions=None, length=None):
    return Accumulator(
        expressions=expressions,
        length=length,
        )
