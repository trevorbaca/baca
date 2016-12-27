# -*- coding: utf-8 -*-
import abjad


class LMRSpecifier(abjad.abctools.AbjadObject):
    r'''Left-middle-right specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Default LMR specifier:

        ::

            >>> lmr_specifier = baca.tools.LMRSpecifier()

        ::

            >>> parts = lmr_specifier([1])
            >>> for part in parts: part
            Sequence([1])

        ::

            >>> parts =lmr_specifier([1, 2])
            >>> for part in parts: part
            Sequence([1, 2])

        ::

            >>> parts = lmr_specifier([1, 2, 3])
            >>> for part in parts: part
            Sequence([1, 2, 3])

        ::

            >>> parts = lmr_specifier([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1, 2, 3, 4])

        ::

            >>> parts = lmr_specifier([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1, 2, 3, 4, 5])

        ::

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1, 2, 3, 4, 5, 6])


        ::

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1, 2, 3, 4, 5, 6, 7])

        ::

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1, 2, 3, 4, 5, 6, 7, 8])

        ::

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1, 2, 3, 4, 5, 6, 7, 8, 9])

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_left_counts',
        '_left_cyclic',
        '_left_length',
        '_left_reversed',
        '_middle_counts',
        '_middle_cyclic',
        '_middle_reversed',
        '_priority',
        '_right_counts',
        '_right_cyclic',
        '_right_length',
        '_right_reversed',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        left_counts=None,
        left_cyclic=None,
        left_length=None,
        left_reversed=None,
        middle_counts=None,
        middle_cyclic=None,
        middle_reversed=None,
        priority=None,
        right_counts=None,
        right_cyclic=None,
        right_length=None,
        right_reversed=None,
        ):
        if left_counts is not None:
            assert abjad.mathtools.all_are_positive_integers(left_counts)
        self._left_counts = left_counts
        if left_cyclic is not None:
            left_cyclic = bool(left_cyclic)
        self._left_cyclic = left_cyclic
        if left_length is not None:
            left_length = int(left_length)
            assert 0 <= left_length, repr(left_length)
        self._left_length = left_length
        if left_reversed is not None:
            left_reversed = bool(left_reversed)
        self._left_reversed = left_reversed
        if middle_counts is not None:
            assert abjad.mathtools.all_are_positive_integers(middle_counts)
        self._middle_counts = middle_counts
        if middle_cyclic is not None:
            middle_cyclic = bool(middle_cyclic)
        self._middle_cyclic = middle_cyclic
        if middle_reversed is not None:
            middle_reversed = bool(middle_reversed)
        self._middle_reversed = middle_reversed
        if priority is not None:
            assert priority in (Left, Right)
        self._priority = priority
        if right_counts is not None:
            assert abjad.mathtools.all_are_positive_integers(right_counts)
        self._right_counts = right_counts
        if right_cyclic is not None:
            right_cyclic = bool(right_cyclic)
        self._right_cyclic = right_cyclic
        if right_length is not None:
            right_length = int(right_length)
            assert 0 <= right_length, repr(right_length)
        self._right_length = right_length
        if right_reversed is not None:
            right_reversed = bool(right_reversed)
        self._right_reversed = right_reversed

    ### SPECIAL METHODS ###

    def __call__(self, sequence):
        r'''Calls LMR specifier on `sequence`.

        Returns list of subsequences.
        '''
        top_lengths = self._get_top_lengths(len(sequence))
        top_parts = abjad.sequence(sequence).partition_by_counts(
            top_lengths,
            cyclic=False,
            overhang=Exact,
            )
        parts = []
        left_part, middle_part, right_part = top_parts
        if left_part:
            if self.left_counts:
                parts_ = abjad.sequence(left_part).partition_by_counts(
                    self.left_counts,
                    cyclic=self.left_cyclic,
                    overhang=True,
                    reversed_=self.left_reversed,
                    )
                parts.extend(parts_)
            else:
                parts.append(left_part)
        if middle_part:
            if self.middle_counts:
                parts_ = abjad.sequence(middle_part).partition_by_counts(
                    self.middle_counts,
                    cyclic=self.middle_cyclic,
                    overhang=True,
                    reversed_=self.middle_reversed,
                    )
                parts.extend(parts_)
            else:
                parts.append(middle_part)
        if right_part:
            if self.right_counts:
                parts_ = abjad.sequence(right_part).partition_by_counts(
                    self.right_counts,
                    cyclic=self.right_cyclic,
                    overhang=True,
                    reversed_=self.right_reversed,
                    )
                parts.extend(parts_)
            else:
                parts.append(right_part)
        return parts

    ### PRIVATE METHODS ###

    def _get_top_lengths(self, total_length):
        left_length, middle_length, right_length = 0, 0, 0
        left_length = self.left_length or 0
        middle_length = 0
        right_length = self.right_length or 0
        if left_length and right_length:
            if self._get_priority() is Left:
                left_length = self.left_length or 0
                left_length = min([left_length, total_length])
                remaining_length = total_length - left_length
                if self.right_length is None:
                    right_length = remaining_length
                    middle_length = 0
                else:
                    right_length = self.right_length or 0
                    right_length = min([right_length, remaining_length])
                    remaining_length = total_length - (left_length + right_length)
                    middle_length = remaining_length
            else:
                right_length = self.right_length or 0
                right_length = min([right_length, total_length])
                remaining_length = total_length - right_length
                if self.left_length is None:
                    left_length = remaining_length
                    middle_length = 0
                else:
                    left_length = self.left_length or 0
                    left_length = min([left_length, remaining_length])
                    remaining_length = total_length - (right_length + left_length)
                    middle_length = remaining_length
        elif left_length and not right_length:
            left_length = min([left_length, total_length])
            remaining_length = total_length - left_length
            right_length = remaining_length
        elif not left_length and right_length:
            right_length = min([right_length, total_length])
            remaining_length = total_length - right_length
            left_length = remaining_length
        elif not left_length and not right_length:
            middle_length = total_length
        return left_length, middle_length, right_length

    def _get_priority(self):
        if self.priority is None:
            return Left
        return self.priority

    ### PUBLIC PROPERTIES ###

    @property
    def left_counts(self):
        r'''Gets left counts.

        ..  container:: example

            Left counts equal to a single 1:

            ::

                >>> lmr_specifier = baca.tools.LMRSpecifier(
                ...     left_counts=[1],
                ...     left_cyclic=False,
                ...     left_length=3,
                ...     right_length=2,
                ...     )

            ::

                >>> parts = lmr_specifier([1])
                >>> for part in parts: part
                Sequence([1])

            ::

                >>> parts = lmr_specifier([1, 2])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2])

            ::

                >>> parts = lmr_specifier([1, 2, 3])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2, 3])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2, 3])
                Sequence([4])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2, 3])
                Sequence([4, 5])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2, 3])
                Sequence([4])
                Sequence([5, 6])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2, 3])
                Sequence([4, 5])
                Sequence([6, 7])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2, 3])
                Sequence([4, 5, 6])
                Sequence([7, 8])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2, 3])
                Sequence([4, 5, 6, 7])
                Sequence([8, 9])

        ..  container:: example

            Left counts all equal to 1:

            ::

                >>> lmr_specifier = baca.tools.LMRSpecifier(
                ...     left_counts=[1],
                ...     left_cyclic=True,
                ...     left_length=3,
                ...     right_length=2,
                ...     )

            ::

                >>> parts = lmr_specifier([1])
                >>> for part in parts: part
                Sequence([1])

            ::

                >>> parts = lmr_specifier([1, 2])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2])

            ::

                >>> parts = lmr_specifier([1, 2, 3])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2])
                Sequence([3])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2])
                Sequence([3])
                Sequence([4])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2])
                Sequence([3])
                Sequence([4, 5])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2])
                Sequence([3])
                Sequence([4])
                Sequence([5, 6])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2])
                Sequence([3])
                Sequence([4, 5])
                Sequence([6, 7])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2])
                Sequence([3])
                Sequence([4, 5, 6])
                Sequence([7, 8])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2])
                Sequence([3])
                Sequence([4, 5, 6, 7])
                Sequence([8, 9])

        Defaults to none.

        Set to positive integers or none.

        Returns tuple of positive integers or none.
        '''
        return self._left_counts

    @property
    def left_cyclic(self):
        r'''Is true when specifier reads left counts cyclically.
        Otherwise false.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._left_cyclic
        
    @property
    def left_length(self):
        r'''Gets left length.

        ..  container:: example

            Left length equal to 2:

            ::

                >>> lmr_specifier = baca.tools.LMRSpecifier(
                ...     left_length=2,
                ...     )

            ::

                >>> parts = lmr_specifier([1])
                >>> for part in parts: part
                Sequence([1])

            ::

                >>> parts = lmr_specifier([1, 2])
                >>> for part in parts: part
                Sequence([1, 2])

            ::

                >>> parts = lmr_specifier([1, 2, 3])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4, 5])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4, 5, 6])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4, 5, 6, 7])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4, 5, 6, 7, 8])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4, 5, 6, 7, 8, 9])

        Defaults to none.

        Set to nonnegative integer or none.

        Returns nonnegative integer or none.
        '''
        return self._left_length

    @property
    def left_reversed(self):
        r'''Is true when specifier reverses left partition.
        Otherwise false.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._left_reversed

    @property
    def middle_counts(self):
        r'''Gets middle counts.

        Defaults to none.

        Set to positive integers or none.

        Returns positive integers or none.
        '''
        return self._middle_counts

    @property
    def middle_cyclic(self):
        r'''Is true when specifier reads middle counts cyclically.
        Otherwise false.

        ..  container:: example

            Cyclic middle counts equal to [2]:

            ::

                >>> lmr_specifier = baca.tools.LMRSpecifier(
                ...     middle_counts=[2],
                ...     middle_cyclic=True,
                ...     )

            ::

                >>> parts = lmr_specifier([1])
                >>> for part in parts: part
                Sequence([1])

            ::

                >>> parts = lmr_specifier([1, 2])
                >>> for part in parts: part
                Sequence([1, 2])

            ::

                >>> parts = lmr_specifier([1, 2, 3])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4])
                Sequence([5])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4])
                Sequence([5, 6])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4])
                Sequence([5, 6])
                Sequence([7])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4])
                Sequence([5, 6])
                Sequence([7, 8])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4])
                Sequence([5, 6])
                Sequence([7, 8])
                Sequence([9])

            Odd parity produces length-1 part at right.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._middle_cyclic

    @property
    def middle_reversed(self):
        r'''Is true when specifier reverses middle partition.
        Otherwise false.

        ..  container:: example

            Reversed cyclic middle counts equal to [2]:

            ::

                >>> lmr_specifier = baca.tools.LMRSpecifier(
                ...     middle_counts=[2],
                ...     middle_cyclic=True,
                ...     middle_reversed=True,
                ...     )

            ::

                >>> parts = lmr_specifier([1])
                >>> for part in parts: part
                Sequence([1])

            ::

                >>> parts = lmr_specifier([1, 2])
                >>> for part in parts: part
                Sequence([1, 2])

            ::

                >>> parts = lmr_specifier([1, 2, 3])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2, 3])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2, 3])
                Sequence([4, 5])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4])
                Sequence([5, 6])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2, 3])
                Sequence([4, 5])
                Sequence([6, 7])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4])
                Sequence([5, 6])
                Sequence([7, 8])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2, 3])
                Sequence([4, 5])
                Sequence([6, 7])
                Sequence([8, 9])

            Odd parity produces length-1 part at left.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._middle_reversed

    @property
    def priority(self):
        r'''Gets priority.

        ..  container:: example

            Priority to the left:

            ::

                >>> lmr_specifier = baca.tools.LMRSpecifier(
                ...     left_length=2,
                ...     right_length=1,
                ...     )

            ::

                >>> parts = lmr_specifier([1])
                >>> for part in parts: part
                Sequence([1])

            ::

                >>> parts = lmr_specifier([1, 2])
                >>> for part in parts: part
                Sequence([1, 2])

            ::

                >>> parts = lmr_specifier([1, 2, 3])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3])
                Sequence([4])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4])
                Sequence([5])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4, 5])
                Sequence([6])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4, 5, 6])
                Sequence([7])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4, 5, 6, 7])
                Sequence([8])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4, 5, 6, 7, 8])
                Sequence([9])

        ..  container:: example

            Priority to the right:

            ::

                >>> lmr_specifier = baca.tools.LMRSpecifier(
                ...     left_length=2,
                ...     priority=Right,
                ...     right_length=1,
                ...     )

            ::

                >>> parts = lmr_specifier([1])
                >>> for part in parts: part
                Sequence([1])

            ::

                >>> parts = lmr_specifier([1, 2])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2])

            ::

                >>> parts = lmr_specifier([1, 2, 3])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3])
                Sequence([4])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4])
                Sequence([5])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4, 5])
                Sequence([6])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4, 5, 6])
                Sequence([7])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4, 5, 6, 7])
                Sequence([8])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4, 5, 6, 7, 8])
                Sequence([9])

        Defaults to none.

        Set to left, right or none.

        Returns left, right or none.
        '''
        return self._priority

    @property
    def right_counts(self):
        r'''Gets right counts.

        Defaults to none.

        Set to positive integers or none.

        Returns positive integers or none.
        '''
        return self._right_counts

    @property
    def right_cyclic(self):
        r'''Is true when specifier reads right counts cyclically.
        Otherwise false.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._right_cyclic
        
    @property
    def right_length(self):
        r'''Gets right length.

        ..  container:: example

            Right length equal to 2:

            ::

                >>> lmr_specifier = baca.tools.LMRSpecifier(
                ...     right_length=2,
                ...     )

            ::

                >>> parts = lmr_specifier([1])
                >>> for part in parts: part
                Sequence([1])

            ::

                >>> parts = lmr_specifier([1, 2])
                >>> for part in parts: part
                Sequence([1, 2])

            ::

                >>> parts = lmr_specifier([1, 2, 3])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2, 3])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4])
                >>> for part in parts: part
                Sequence([1, 2])
                Sequence([3, 4])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5])
                >>> for part in parts: part
                Sequence([1, 2, 3])
                Sequence([4, 5])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
                >>> for part in parts: part
                Sequence([1, 2, 3, 4])
                Sequence([5, 6])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
                >>> for part in parts: part
                Sequence([1, 2, 3, 4, 5])
                Sequence([6, 7])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
                >>> for part in parts: part
                Sequence([1, 2, 3, 4, 5, 6])
                Sequence([7, 8])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
                >>> for part in parts: part
                Sequence([1, 2, 3, 4, 5, 6, 7])
                Sequence([8, 9])

        ..  container:: example

            Right length equal to 2 and left counts equal to [1]:

            ::

                >>> lmr_specifier = baca.tools.LMRSpecifier(
                ...     left_counts=[1],
                ...     left_cyclic=False,
                ...     right_length=2,
                ...     )

            ::

                >>> parts = lmr_specifier([1])
                >>> for part in parts: part
                Sequence([1])

            ::

                >>> parts = lmr_specifier([1, 2])
                >>> for part in parts: part
                Sequence([1, 2])

            ::

                >>> parts = lmr_specifier([1, 2, 3])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2, 3])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2])
                Sequence([3, 4])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2, 3])
                Sequence([4, 5])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2, 3, 4])
                Sequence([5, 6])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2, 3, 4, 5])
                Sequence([6, 7])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2, 3, 4, 5, 6])
                Sequence([7, 8])

            ::

                >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
                >>> for part in parts: part
                Sequence([1])
                Sequence([2, 3, 4, 5, 6, 7])
                Sequence([8, 9])

        Defaults to none.

        Set to nonnegative integer or none.

        Returns nonnegative integer or none.
        '''
        return self._right_length

    @property
    def right_reversed(self):
        r'''Is true when specifier reverses right partition.
        Otherwise false.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._right_reversed
