# -*- coding: utf-8 -*-
import fractions
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Interpolation(AbjadValueObject):
    r'''Interpolation.
    
    ..  container:: example

        ::

            >>> import baca

    '''

    ### INITIALIZER ###

    def __init__(
        self,
        ):
        pass

    ### SPECIAL METHODS ###

    def __call__(self, numbers=None):
        r'''Calls interpolation on `numbers`.

        Returns list of numbers.
        '''
        pass

    ### PUBLIC PROPERTIES ###

    ### PUBLIC METHODS ###

    @staticmethod
    def interpolate_linear(start, stop, count=2):
        r'''Interpolates `count` values linearly from `start` to `stop`.

        ..  container:: example

            **Example 1.** Interpolates linearly from -5 up to 5:

            ::

                >>> Interpolation = baca.tools.Interpolation
                >>> interpolate_linear = baca.tools.Interpolation.interpolate_linear
                >>> for count in range(8):
                ...     result = Interpolation.interpolate_linear(-5, 5, count)
                ...     print(count, result)
                0 []
                1 [-5]
                2 [-5, 5]
                3 [-5, 0, 5]
                4 [-5, Fraction(-5, 3), Fraction(5, 3), 5]
                5 [-5, Fraction(-5, 2), 0, Fraction(5, 2), 5]
                6 [-5, -3, -1, 1, 3, 5]
                7 [-5, Fraction(-10, 3), Fraction(-5, 3), 0, Fraction(5, 3), Fraction(10, 3), 5]

        ..  container:: example

            **Example 2.** Interpolates linearly from 2 down to 1:

            ::

                >>> Interpolation = baca.tools.Interpolation
                >>> interpolate_linear = baca.tools.Interpolation.interpolate_linear
                >>> for count in range(8):
                ...     result = Interpolation.interpolate_linear(2, 1, count)
                ...     print(count, result)
                0 []
                1 [2]
                2 [2, 1]
                3 [2, Fraction(3, 2), 1]
                4 [2, Fraction(5, 3), Fraction(4, 3), 1]
                5 [2, Fraction(7, 4), Fraction(3, 2), Fraction(5, 4), 1]
                6 [2, Fraction(9, 5), Fraction(8, 5), Fraction(7, 5), Fraction(6, 5), 1]
                7 [2, Fraction(11, 6), Fraction(5, 3), Fraction(3, 2), Fraction(4, 3), Fraction(7, 6), 1]

        Returns list of numbers.
        '''
        import numbers
        assert isinstance(start, numbers.Number), repr(start)
        assert isinstance(stop, numbers.Number), repr(stop)
        assert isinstance(count, int), repr(count)
        assert 0 <= count, repr(count)
        result = []
        step = 0
        if 1 < count:
            step = fractions.Fraction(stop-start, count-1)
        for i in range(count):
            addend = i * step
            number = start + addend
            if int(number) == number:
                result.append(int(number))
            else:
                result.append(number)
        return result