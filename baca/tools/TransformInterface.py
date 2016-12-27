# -*- coding: utf-8 -*-
import abjad


class TransformInterface(object):
    r'''Transform interface.

    ::

        >>> import abjad
        >>> import baca

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Interfaces'

    ### PUBLIC METHODS ###

    @staticmethod
    def helianthate(sequence, n=0, m=0):
        '''Helianthates `sequence` by outer index of rotation `n` and inner
        index of rotation `m`.

        ..  container:: example

            Helianthates list of lists:

            ::

                >>> sequence = [[1, 2, 3], [4, 5], [6, 7, 8]]
                >>> sequence = baca.transforms.helianthate(sequence, n=-1, m=1)
                >>> for item in sequence:
                ...     item
                [1, 2, 3]
                [4, 5]
                [6, 7, 8]
                [5, 4]
                [8, 6, 7]
                [3, 1, 2]
                [7, 8, 6]
                [2, 3, 1]
                [4, 5]
                [1, 2, 3]
                [5, 4]
                [6, 7, 8]
                [4, 5]
                [8, 6, 7]
                [3, 1, 2]
                [7, 8, 6]
                [2, 3, 1]
                [5, 4]

        ..  container:: example

            Helianthates list of segments:

            ::

                >>> J = abjad.PitchClassSegment(items=[0, 2, 4], name='J')
                >>> K = abjad.PitchClassSegment(items=[5, 6], name='K')
                >>> L = abjad.PitchClassSegment(items=[7, 9, 11], name='L')
                >>> sequence = baca.transforms.helianthate([J, K, L], n=-1, m=1)
                >>> for item in sequence:
                ...     item
                PitchClassSegment([0, 2, 4], name='J')
                PitchClassSegment([5, 6], name='K')
                PitchClassSegment([7, 9, 11], name='L')
                PitchClassSegment([6, 5], name='r1(K)')
                PitchClassSegment([11, 7, 9], name='r1(L)')
                PitchClassSegment([4, 0, 2], name='r1(J)')
                PitchClassSegment([9, 11, 7], name='r2(L)')
                PitchClassSegment([2, 4, 0], name='r2(J)')
                PitchClassSegment([5, 6], name='r2(K)')
                PitchClassSegment([0, 2, 4], name='r3(J)')
                PitchClassSegment([6, 5], name='r3(K)')
                PitchClassSegment([7, 9, 11], name='r3(L)')
                PitchClassSegment([5, 6], name='r4(K)')
                PitchClassSegment([11, 7, 9], name='r4(L)')
                PitchClassSegment([4, 0, 2], name='r4(J)')
                PitchClassSegment([9, 11, 7], name='r5(L)')
                PitchClassSegment([2, 4, 0], name='r5(J)')
                PitchClassSegment([6, 5], name='r5(K)')

        ..  container:: example

            Trivial helianthation:

            ::

                >>> sequence = [[1, 2, 3], [4, 5], [6, 7, 8]]
                >>> baca.transforms.helianthate(sequence)
                [[1, 2, 3], [4, 5], [6, 7, 8]]

        Returns new object with type equal to that of `sequence`.
        '''
        sequence_type = type(sequence)
        start = list(sequence[:])
        result = list(sequence[:])
        assert isinstance(n, int), repr(n)
        assert isinstance(m, int), repr(m)
        original_n = n
        original_m = m
        def _generalized_rotate(object_, n=0):
            if hasattr(object_, 'rotate'):
                return object_.rotate(n=n)
            return abjad.sequencetools.rotate_sequence(object_, n=n)
        while True:
            inner = [_generalized_rotate(_, m) for _ in sequence]
            candidate = _generalized_rotate(inner, n)
            if candidate == start:
                break
            result.extend(candidate)
            n += original_n
            m += original_m
        result = sequence_type(result)
        return result
