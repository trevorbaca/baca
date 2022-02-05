import collections
import copy
import itertools
import typing

import abjad


class Sequence(abjad.Sequence):
    r"""
    Sequence.

    ..  container:: example

        Initializes from numbers:

        >>> baca.Sequence([1, 2, 3, 4, 5, 6])
        Sequence([1, 2, 3, 4, 5, 6])

    ..  container:: example

        Initializes from collection:

        >>> items = [-2, -1.5, 6, 7, -1.5, 7]
        >>> collection = abjad.PitchClassSegment(items=items)
        >>> lilypond_file = abjad.illustrate(collection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> voice = lilypond_file["Voice"]
            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                bf'8
                bqf'8
                fs'8
                g'8
                bqf'8
                g'8
                \bar "|."
                \override Score.BarLine.transparent = ##f
            }

        >>> baca.Sequence(collection)
        Sequence([NumberedPitchClass(10), NumberedPitchClass(10.5), NumberedPitchClass(6), NumberedPitchClass(7), NumberedPitchClass(10.5), NumberedPitchClass(7)])

    ..  container:: example

        Maps transposition to multiple collections:

        >>> items = [-2, -1.5, 6, 7, -1.5, 7]
        >>> collection = abjad.PitchClassSegment(items=items)
        >>> collections = [
        ...     abjad.PitchClassSegment(items=[-2, -1.5, 6]),
        ...     abjad.PitchClassSegment(items=[7, -1.5, 7]),
        ...     ]

        >>> sequence = baca.Sequence(collections)
        >>> sequence = sequence.map(lambda _: _.transpose(n=1))
        >>> sequence.join()
        Sequence([PitchClassSegment(items=[11, 11.5, 7, 8, 11.5, 8], item_class=NumberedPitchClass)])

        >>> collection = sequence.join()[0]
        >>> lilypond_file = abjad.illustrate(collection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> voice = lilypond_file["Voice"]
            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                b'8
                bqs'8
                g'8
                af'8
                bqs'8
                af'8
                \bar "|."
                \override Score.BarLine.transparent = ##f
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PUBLIC METHODS ###

    def accumulate(self, operands=None, count=None):
        r"""
        Accumulates ``operands`` calls against sequence to identity.

        ..  container:: example

            Accumulates identity operator:

            >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
            >>> collection_2 = baca.PitchClassSegment([4, 5])
            >>> baca.Sequence([collection_1, collection_2])
            Sequence([PitchClassSegment(items=[0, 1, 2, 3], item_class=NumberedPitchClass), PitchClassSegment(items=[4, 5], item_class=NumberedPitchClass)])

            >>> sequence = baca.Sequence([collection_1, collection_2])
            >>> for item in sequence.accumulate():
            ...     item
            ...
            Sequence([PitchClassSegment(items=[0, 1, 2, 3], item_class=NumberedPitchClass), PitchClassSegment(items=[4, 5], item_class=NumberedPitchClass)])

        ..  container:: example

            Accumulates alpha:

            >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
            >>> collection_2 = baca.PitchClassSegment([4, 5])
            >>> baca.Sequence([collection_1, collection_2])
            Sequence([PitchClassSegment(items=[0, 1, 2, 3], item_class=NumberedPitchClass), PitchClassSegment(items=[4, 5], item_class=NumberedPitchClass)])

            >>> sequence = baca.Sequence([collection_1, collection_2])
            >>> for item in sequence.accumulate([lambda _: _.alpha()]):
            ...     item
            ...
            Sequence([PitchClassSegment(items=[0, 1, 2, 3], item_class=NumberedPitchClass), PitchClassSegment(items=[4, 5], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[1, 0, 3, 2], item_class=NumberedPitchClass), PitchClassSegment(items=[5, 4], item_class=NumberedPitchClass)])

        ..  container:: example

            Accumulates transposition:

            >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
            >>> collection_2 = baca.PitchClassSegment([4, 5])
            >>> baca.Sequence([collection_1, collection_2])
            Sequence([PitchClassSegment(items=[0, 1, 2, 3], item_class=NumberedPitchClass), PitchClassSegment(items=[4, 5], item_class=NumberedPitchClass)])

            >>> sequence = baca.Sequence([collection_1, collection_2])
            >>> for item in sequence.accumulate([lambda _: _.transpose(n=3)]):
            ...     item
            ...
            Sequence([PitchClassSegment(items=[0, 1, 2, 3], item_class=NumberedPitchClass), PitchClassSegment(items=[4, 5], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[3, 4, 5, 6], item_class=NumberedPitchClass), PitchClassSegment(items=[7, 8], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[6, 7, 8, 9], item_class=NumberedPitchClass), PitchClassSegment(items=[10, 11], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[9, 10, 11, 0], item_class=NumberedPitchClass), PitchClassSegment(items=[1, 2], item_class=NumberedPitchClass)])

        ..  container:: example

            Accumulates alpha followed by transposition:

            >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
            >>> collection_2 = baca.PitchClassSegment([4, 5])
            >>> baca.Sequence([collection_1, collection_2])
            Sequence([PitchClassSegment(items=[0, 1, 2, 3], item_class=NumberedPitchClass), PitchClassSegment(items=[4, 5], item_class=NumberedPitchClass)])

            >>> sequence = baca.Sequence([collection_1, collection_2])
            >>> for item in sequence.accumulate(
            ...     [lambda _: _.alpha(), lambda _: _.transpose(n=3)]):
            ...     item
            ...
            Sequence([PitchClassSegment(items=[0, 1, 2, 3], item_class=NumberedPitchClass), PitchClassSegment(items=[4, 5], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[1, 0, 3, 2], item_class=NumberedPitchClass), PitchClassSegment(items=[5, 4], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[4, 3, 6, 5], item_class=NumberedPitchClass), PitchClassSegment(items=[8, 7], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[5, 2, 7, 4], item_class=NumberedPitchClass), PitchClassSegment(items=[9, 6], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[8, 5, 10, 7], item_class=NumberedPitchClass), PitchClassSegment(items=[0, 9], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[9, 4, 11, 6], item_class=NumberedPitchClass), PitchClassSegment(items=[1, 8], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[0, 7, 2, 9], item_class=NumberedPitchClass), PitchClassSegment(items=[4, 11], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[1, 6, 3, 8], item_class=NumberedPitchClass), PitchClassSegment(items=[5, 10], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[4, 9, 6, 11], item_class=NumberedPitchClass), PitchClassSegment(items=[8, 1], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[5, 8, 7, 10], item_class=NumberedPitchClass), PitchClassSegment(items=[9, 0], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[8, 11, 10, 1], item_class=NumberedPitchClass), PitchClassSegment(items=[0, 3], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[9, 10, 11, 0], item_class=NumberedPitchClass), PitchClassSegment(items=[1, 2], item_class=NumberedPitchClass)])

        ..  container:: example

            Accumulates permutation:

            >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
            >>> collection_2 = baca.PitchClassSegment([4, 5])
            >>> baca.Sequence([collection_1, collection_2])
            Sequence([PitchClassSegment(items=[0, 1, 2, 3], item_class=NumberedPitchClass), PitchClassSegment(items=[4, 5], item_class=NumberedPitchClass)])

            >>> row = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
            >>> sequence = baca.Sequence([collection_1, collection_2])
            >>> for item in sequence.accumulate([lambda _: _.permute(row)]):
            ...     item
            ...
            Sequence([PitchClassSegment(items=[0, 1, 2, 3], item_class=NumberedPitchClass), PitchClassSegment(items=[4, 5], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[10, 0, 2, 6], item_class=NumberedPitchClass), PitchClassSegment(items=[8, 7], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[4, 10, 2, 5], item_class=NumberedPitchClass), PitchClassSegment(items=[1, 3], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[8, 4, 2, 7], item_class=NumberedPitchClass), PitchClassSegment(items=[0, 6], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[1, 8, 2, 3], item_class=NumberedPitchClass), PitchClassSegment(items=[10, 5], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[0, 1, 2, 6], item_class=NumberedPitchClass), PitchClassSegment(items=[4, 7], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[10, 0, 2, 5], item_class=NumberedPitchClass), PitchClassSegment(items=[8, 3], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[4, 10, 2, 7], item_class=NumberedPitchClass), PitchClassSegment(items=[1, 6], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[8, 4, 2, 3], item_class=NumberedPitchClass), PitchClassSegment(items=[0, 5], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[1, 8, 2, 6], item_class=NumberedPitchClass), PitchClassSegment(items=[10, 7], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[0, 1, 2, 5], item_class=NumberedPitchClass), PitchClassSegment(items=[4, 3], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[10, 0, 2, 7], item_class=NumberedPitchClass), PitchClassSegment(items=[8, 6], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[4, 10, 2, 3], item_class=NumberedPitchClass), PitchClassSegment(items=[1, 5], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[8, 4, 2, 6], item_class=NumberedPitchClass), PitchClassSegment(items=[0, 7], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[1, 8, 2, 5], item_class=NumberedPitchClass), PitchClassSegment(items=[10, 3], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[0, 1, 2, 7], item_class=NumberedPitchClass), PitchClassSegment(items=[4, 6], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[10, 0, 2, 3], item_class=NumberedPitchClass), PitchClassSegment(items=[8, 5], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[4, 10, 2, 6], item_class=NumberedPitchClass), PitchClassSegment(items=[1, 7], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[8, 4, 2, 5], item_class=NumberedPitchClass), PitchClassSegment(items=[0, 3], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[1, 8, 2, 7], item_class=NumberedPitchClass), PitchClassSegment(items=[10, 6], item_class=NumberedPitchClass)])

        ..  container:: example

            Accumulates permutation followed by transposition:

            >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
            >>> collection_2 = baca.PitchClassSegment([4, 5])
            >>> baca.Sequence([collection_1, collection_2])
            Sequence([PitchClassSegment(items=[0, 1, 2, 3], item_class=NumberedPitchClass), PitchClassSegment(items=[4, 5], item_class=NumberedPitchClass)])

            >>> row = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
            >>> sequence = baca.Sequence([collection_1, collection_2])
            >>> for item in sequence.accumulate(
            ...     [lambda _: _.permute(row), lambda _: _.transpose(n=3)],
            ...     ):
            ...     item
            ...
            Sequence([PitchClassSegment(items=[0, 1, 2, 3], item_class=NumberedPitchClass), PitchClassSegment(items=[4, 5], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[10, 0, 2, 6], item_class=NumberedPitchClass), PitchClassSegment(items=[8, 7], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[1, 3, 5, 9], item_class=NumberedPitchClass), PitchClassSegment(items=[11, 10], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[0, 6, 7, 9], item_class=NumberedPitchClass), PitchClassSegment(items=[11, 4], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[3, 9, 10, 0], item_class=NumberedPitchClass), PitchClassSegment(items=[2, 7], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[6, 9, 4, 10], item_class=NumberedPitchClass), PitchClassSegment(items=[2, 3], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[9, 0, 7, 1], item_class=NumberedPitchClass), PitchClassSegment(items=[5, 6], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[9, 10, 3, 0], item_class=NumberedPitchClass), PitchClassSegment(items=[7, 5], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[0, 1, 6, 3], item_class=NumberedPitchClass), PitchClassSegment(items=[10, 8], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[10, 0, 5, 6], item_class=NumberedPitchClass), PitchClassSegment(items=[4, 1], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[1, 3, 8, 9], item_class=NumberedPitchClass), PitchClassSegment(items=[7, 4], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[0, 6, 1, 9], item_class=NumberedPitchClass), PitchClassSegment(items=[3, 8], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[3, 9, 4, 0], item_class=NumberedPitchClass), PitchClassSegment(items=[6, 11], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[6, 9, 8, 10], item_class=NumberedPitchClass), PitchClassSegment(items=[5, 11], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[9, 0, 11, 1], item_class=NumberedPitchClass), PitchClassSegment(items=[8, 2], item_class=NumberedPitchClass)])
            Sequence([PitchClassSegment(items=[9, 10, 11, 0], item_class=NumberedPitchClass), PitchClassSegment(items=[1, 2], item_class=NumberedPitchClass)])

        Returns sequence of accumulated sequences.

        Returns sequence of length ``count`` + 1 with integer ``count``.

        Returns sequence of orbit length with ``count`` set to identity.
        """
        if count is None:
            count = abjad.Exact
        operands = operands or [lambda _: _]
        if not isinstance(operands, list):
            operands = [operands]
        items = [self]
        if count == abjad.Exact:
            for i in range(1000):
                sequence = items[-1]
                for operand in operands:
                    sequence = sequence.map(operand)
                    items.append(sequence)
                if sequence == items[0]:
                    items.pop(-1)
                    break
            else:
                message = "1000 iterations without identity:"
                message += f" {items[0]!r} to {items[-1]!r}."
                raise Exception(message)
        else:
            for i in range(count - 1):
                sequence = items[-1]
                for operand in operands:
                    sequence = sequence.map(operand)
                    items.append(sequence)
        return type(self)(items=items)

    def boustrophedon(self, count=2):
        r"""
        Iterates sequence boustrophedon.

        ..  container:: example

            Iterates atoms boustrophedon:

            >>> sequence = baca.Sequence([1, 2, 3, 4, 5])

            >>> sequence.boustrophedon(count=0)
            Sequence([])

            >>> sequence.boustrophedon(count=1)
            Sequence([1, 2, 3, 4, 5])

            >>> sequence.boustrophedon(count=2)
            Sequence([1, 2, 3, 4, 5, 4, 3, 2, 1])

            >>> sequence.boustrophedon(count=3)
            Sequence([1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 5])

        ..  container:: example

            Iterates collections boustrophedon:

            >>> collections = [
            ...     baca.PitchClassSegment([1, 2, 3]),
            ...     baca.PitchClassSegment([4, 5, 6]),
            ... ]
            >>> sequence = baca.Sequence(collections)

            >>> sequence.boustrophedon(count=0)
            Sequence([])

            >>> for collection in sequence.boustrophedon(count=1):
            ...     collection
            ...
            PitchClassSegment(items=[1, 2, 3], item_class=NumberedPitchClass)
            PitchClassSegment(items=[4, 5, 6], item_class=NumberedPitchClass)

            >>> for collection in sequence.boustrophedon(count=2):
            ...     collection
            ...
            PitchClassSegment(items=[1, 2, 3], item_class=NumberedPitchClass)
            PitchClassSegment(items=[4, 5, 6], item_class=NumberedPitchClass)
            PitchClassSegment(items=[5, 4], item_class=NumberedPitchClass)
            PitchClassSegment(items=[3, 2, 1], item_class=NumberedPitchClass)

            >>> for collection in sequence.boustrophedon(count=3):
            ...     collection
            ...
            PitchClassSegment(items=[1, 2, 3], item_class=NumberedPitchClass)
            PitchClassSegment(items=[4, 5, 6], item_class=NumberedPitchClass)
            PitchClassSegment(items=[5, 4], item_class=NumberedPitchClass)
            PitchClassSegment(items=[3, 2, 1], item_class=NumberedPitchClass)
            PitchClassSegment(items=[2, 3], item_class=NumberedPitchClass)
            PitchClassSegment(items=[4, 5, 6], item_class=NumberedPitchClass)

        ..  container:: example

            Iterates mixed items boustrophedon:

            >>> collection = baca.PitchClassSegment([1, 2, 3])
            >>> sequence = baca.Sequence([collection, 4, 5])
            >>> for item in sequence.boustrophedon(count=3):
            ...     item
            ...
            PitchClassSegment(items=[1, 2, 3], item_class=NumberedPitchClass)
            4
            5
            4
            PitchClassSegment(items=[3, 2, 1], item_class=NumberedPitchClass)
            PitchClassSegment(items=[2, 3], item_class=NumberedPitchClass)
            4
            5

        Returns new sequence.
        """
        result = []
        for i in range(count):
            if i == 0:
                for item in self:
                    result.append(copy.copy(item))
            elif i % 2 == 0:
                if isinstance(self[0], collections.abc.Iterable):
                    result.append(self[0][1:])
                else:
                    pass
                for item in self[1:]:
                    result.append(copy.copy(item))
            else:
                if isinstance(self[-1], collections.abc.Iterable):
                    item = type(self[-1])(list(reversed(self[-1]))[1:])
                    result.append(item)
                else:
                    pass
                for item in reversed(self[:-1]):
                    if isinstance(item, collections.abc.Iterable):
                        item = type(item)(list(reversed(item)))
                        result.append(item)
                    else:
                        result.append(item)
        return type(self)(items=result)

    def degree_of_rotational_symmetry(self):
        """
        Gets degree of rotational symmetry.

        ..  container:: example

            >>> baca.Sequence([1, 1, 1, 1, 1, 1]).degree_of_rotational_symmetry()
            6

            >>> baca.Sequence([1, 2, 1, 2, 1, 2]).degree_of_rotational_symmetry()
            3

            >>> baca.Sequence([1, 2, 3, 1, 2, 3]).degree_of_rotational_symmetry()
            2

            >>> baca.Sequence([1, 2, 3, 4, 5, 6]).degree_of_rotational_symmetry()
            1

            >>> baca.Sequence().degree_of_rotational_symmetry()
            1

        Returns positive integer.
        """
        degree_of_rotational_symmetry = 0
        for index in range(len(self)):
            rotation = self[index:] + self[:index]
            if rotation == self:
                degree_of_rotational_symmetry += 1
        degree_of_rotational_symmetry = degree_of_rotational_symmetry or 1
        return degree_of_rotational_symmetry

    # TODO: remove ``counts`` in favor of partition-then-``indices`` recipe
    # TODO: generalize ``indices`` to pattern
    def fuse(
        self,
        counts: typing.List[int] = None,
        *,
        cyclic: bool = None,
        indices: typing.Sequence[int] = None,
    ):
        r"""
        Fuses sequence by ``counts``.

        ..  container:: example

            Fuses items:

            >>> divisions = baca.fractions([(7, 8), (3, 8), (5, 8)])
            >>> divisions = baca.Sequence(divisions).fuse()
            >>> divisions = divisions.flatten(depth=-1)
            >>> divisions
            Sequence([NonreducedFraction(15, 8)])

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions)

            >>> lilypond_file = abjad.illustrators.selection(music, divisions)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    {
                        \time 15/8
                        c'1...
                    }
                >>

        ..  container:: example

            Fuses first two items and then remaining items:

            >>> divisions = baca.fractions([(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)])
            >>> divisions = baca.Sequence(divisions).fuse([2])
            >>> for division in divisions:
            ...     division
            NonreducedFraction(4, 8)
            NonreducedFraction(12, 8)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions)

            >>> lilypond_file = abjad.illustrators.selection(music)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    {
                        \time 2/1
                        c'2
                        c'1.
                    }
                >>

        ..  container:: example

            Fuses items two at a time:

            >>> divisions = baca.fractions([(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)])
            >>> divisions = baca.Sequence(divisions).fuse([2], cyclic=True)
            >>> for division in divisions:
            ...     division
            NonreducedFraction(4, 8)
            NonreducedFraction(8, 8)
            NonreducedFraction(2, 4)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions)

            >>> lilypond_file = abjad.illustrators.selection(music)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    {
                        \time 2/1
                        c'2
                        c'1
                        c'2
                    }
                >>

        ..  container:: example

            Splits each item by ``3/8``;  then flattens; then fuses into differently
            sized groups:

            >>> divisions = baca.fractions([(7, 8), (3, 8), (5, 8)])
            >>> divisions = baca.Sequence(divisions).map(
            ...     lambda _: baca.Sequence(_).split_divisions([(3, 8)], cyclic=True)
            ... )
            >>> divisions = divisions.flatten(depth=-1)
            >>> divisions = divisions.fuse([2, 3, 1])
            >>> for division in divisions:
            ...     division
            NonreducedFraction(6, 8)
            NonreducedFraction(7, 8)
            NonreducedFraction(2, 8)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions)

            >>> lilypond_file = abjad.illustrators.selection(music)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    {
                        \time 15/8
                        c'2.
                        c'2..
                        c'4
                    }
                >>

        ..  container:: example

            Splits into sixteenths; partitions; then fuses every other part:

            >>> divisions = baca.fractions([(7, 8), (3, 8), (5, 8)])
            >>> divisions = baca.Sequence(divisions)
            >>> divisions = divisions.fuse()
            >>> divisions = divisions.map(
            ...     lambda _: baca.Sequence(_).split_divisions([(1, 16)], cyclic=True)
            ... )
            >>> divisions = divisions.flatten(depth=-1)
            >>> divisions = divisions.partition_by_ratio_of_lengths((1, 1, 1, 1, 1, 1))
            >>> divisions = divisions.fuse(indices=[1, 3, 5])
            >>> divisions = divisions.flatten(depth=-1)
            >>> for division in divisions:
            ...     division
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(5, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(5, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(5, 16)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions)

            >>> lilypond_file = abjad.illustrators.selection(music)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    {
                        \time 15/8
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'4
                        ~
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'4
                        ~
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'4
                        ~
                        c'16
                    }
                >>

        """
        if indices is not None:
            assert all(isinstance(_, int) for _ in indices), repr(indices)
        if indices and counts:
            raise Exception("do not set indices and counts together.")
        if not indices:
            counts = counts or []
            sequence = self.partition_by_counts(counts, cyclic=cyclic, overhang=True)
        else:
            sequence = self
        items_ = []
        for i, item in enumerate(sequence):
            if indices and i not in indices:
                item_ = item
            else:
                # item_ = _divisions(item).sum()
                item_ = Sequence(item).sum()
            items_.append(item_)
        # sequence = _divisions(items_)
        sequence = Sequence(items_)
        sequence = sequence.flatten(depth=-1)
        return sequence

    def group_by_sign(self, sign=(-1, 0, 1)):
        r"""
        Groups sequence by sign of items.

        >>> sequence = baca.Sequence([0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6])

        ..  container:: example

            >>> for item in sequence.group_by_sign():
            ...     item
            ...
            Sequence([0, 0])
            Sequence([-1, -1])
            Sequence([2, 3])
            Sequence([-5])
            Sequence([1, 2, 5])
            Sequence([-5, -6])

        ..  container:: example

            >>> for item in sequence.group_by_sign([-1]):
            ...     item
            ...
            Sequence([0])
            Sequence([0])
            Sequence([-1, -1])
            Sequence([2])
            Sequence([3])
            Sequence([-5])
            Sequence([1])
            Sequence([2])
            Sequence([5])
            Sequence([-5, -6])

        ..  container:: example

            >>> for item in sequence.group_by_sign([0]):
            ...     item
            ...
            Sequence([0, 0])
            Sequence([-1])
            Sequence([-1])
            Sequence([2])
            Sequence([3])
            Sequence([-5])
            Sequence([1])
            Sequence([2])
            Sequence([5])
            Sequence([-5])
            Sequence([-6])

        ..  container:: example

            >>> for item in sequence.group_by_sign([1]):
            ...     item
            ...
            Sequence([0])
            Sequence([0])
            Sequence([-1])
            Sequence([-1])
            Sequence([2, 3])
            Sequence([-5])
            Sequence([1, 2, 5])
            Sequence([-5])
            Sequence([-6])

        ..  container:: example

            >>> for item in sequence.group_by_sign([-1, 0]):
            ...     item
            ...
            Sequence([0, 0])
            Sequence([-1, -1])
            Sequence([2])
            Sequence([3])
            Sequence([-5])
            Sequence([1])
            Sequence([2])
            Sequence([5])
            Sequence([-5, -6])

        ..  container:: example

            >>> for item in sequence.group_by_sign([-1, 1]):
            ...     item
            ...
            Sequence([0])
            Sequence([0])
            Sequence([-1, -1])
            Sequence([2, 3])
            Sequence([-5])
            Sequence([1, 2, 5])
            Sequence([-5, -6])

        ..  container:: example

            >>> for item in sequence.group_by_sign([0, 1]):
            ...     item
            ...
            Sequence([0, 0])
            Sequence([-1])
            Sequence([-1])
            Sequence([2, 3])
            Sequence([-5])
            Sequence([1, 2, 5])
            Sequence([-5])
            Sequence([-6])

        ..  container:: example

            >>> for item in sequence.group_by_sign([-1, 0, 1]):
            ...     item
            ...
            Sequence([0, 0])
            Sequence([-1, -1])
            Sequence([2, 3])
            Sequence([-5])
            Sequence([1, 2, 5])
            Sequence([-5, -6])

        Groups negative elements when ``-1`` in ``sign``.

        Groups zero-valued elements When ``0`` in ``sign``.

        Groups positive elements when ``1`` in ``sign``.

        Returns nested sequence.
        """
        items = []
        pairs = itertools.groupby(self, abjad.math.sign)
        for current_sign, group in pairs:
            if current_sign in sign:
                items.append(type(self)(group))
            else:
                for item in group:
                    items.append(type(self)([item]))
        return type(self)(items=items)

    def helianthate(self, n=0, m=0):
        r"""
        Helianthates sequence.

        ..  container:: example

            Helianthates list of lists:

            >>> sequence = baca.Sequence([[1, 2, 3], [4, 5], [6, 7, 8]])
            >>> sequence = sequence.helianthate(n=-1, m=1)
            >>> for item in sequence:
            ...     item
            ...
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

            Helianthates list of collections:

            >>> J = baca.PitchClassSegment(items=[0, 2, 4])
            >>> K = baca.PitchClassSegment(items=[5, 6])
            >>> L = baca.PitchClassSegment(items=[7, 9, 11])
            >>> sequence = baca.Sequence([J, K, L])
            >>> sequence = sequence.helianthate(n=-1, m=1)
            >>> for collection in sequence:
            ...     collection
            ...
            PitchClassSegment(items=[0, 2, 4], item_class=NumberedPitchClass)
            PitchClassSegment(items=[5, 6], item_class=NumberedPitchClass)
            PitchClassSegment(items=[7, 9, 11], item_class=NumberedPitchClass)
            PitchClassSegment(items=[6, 5], item_class=NumberedPitchClass)
            PitchClassSegment(items=[11, 7, 9], item_class=NumberedPitchClass)
            PitchClassSegment(items=[4, 0, 2], item_class=NumberedPitchClass)
            PitchClassSegment(items=[9, 11, 7], item_class=NumberedPitchClass)
            PitchClassSegment(items=[2, 4, 0], item_class=NumberedPitchClass)
            PitchClassSegment(items=[5, 6], item_class=NumberedPitchClass)
            PitchClassSegment(items=[0, 2, 4], item_class=NumberedPitchClass)
            PitchClassSegment(items=[6, 5], item_class=NumberedPitchClass)
            PitchClassSegment(items=[7, 9, 11], item_class=NumberedPitchClass)
            PitchClassSegment(items=[5, 6], item_class=NumberedPitchClass)
            PitchClassSegment(items=[11, 7, 9], item_class=NumberedPitchClass)
            PitchClassSegment(items=[4, 0, 2], item_class=NumberedPitchClass)
            PitchClassSegment(items=[9, 11, 7], item_class=NumberedPitchClass)
            PitchClassSegment(items=[2, 4, 0], item_class=NumberedPitchClass)
            PitchClassSegment(items=[6, 5], item_class=NumberedPitchClass)

        ..  container:: example

            Trivial helianthation:

            >>> items = [[1, 2, 3], [4, 5], [6, 7, 8]]
            >>> sequence = baca.Sequence(items)
            >>> sequence.helianthate()
            Sequence([[1, 2, 3], [4, 5], [6, 7, 8]])

        """
        start = list(self[:])
        result = list(self[:])
        assert isinstance(n, int), repr(n)
        assert isinstance(m, int), repr(m)
        original_n = n
        original_m = m

        def _generalized_rotate(argument, n=0):
            if hasattr(argument, "rotate"):
                return argument.rotate(n=n)
            argument_type = type(argument)
            argument = type(self)(argument).rotate(n=n)
            argument = argument_type(argument)
            return argument

        i = 0
        while True:
            inner = [_generalized_rotate(_, m) for _ in self]
            candidate = _generalized_rotate(inner, n)
            if candidate == start:
                break
            result.extend(candidate)
            n += original_n
            m += original_m
            i += 1
            if i == 1000:
                message = "1000 iterations without identity."
                raise Exception(message)
        return type(self)(items=result)

    def partition(self, counts=None):
        r"""
        Partitions sequence cyclically by ``counts`` with overhang.

        ..  container:: example

            >>> sequence = baca.Sequence(range(16))
            >>> parts = sequence.partition([3])

            >>> for part in parts:
            ...     part
            Sequence([0, 1, 2])
            Sequence([3, 4, 5])
            Sequence([6, 7, 8])
            Sequence([9, 10, 11])
            Sequence([12, 13, 14])
            Sequence([15])

        Returns new sequence.
        """
        return self.partition_by_counts(counts=counts, cyclic=True, overhang=True)

    def period_of_rotation(self):
        """
        Gets period of rotation.

        ..  container:: example

            >>> baca.Sequence([1, 2, 3, 4, 5, 6]).period_of_rotation()
            6

            >>> baca.Sequence([1, 2, 3, 1, 2, 3]).period_of_rotation()
            3

            >>> baca.Sequence([1, 2, 1, 2, 1, 2]).period_of_rotation()
            2

            >>> baca.Sequence([1, 1, 1, 1, 1, 1]).period_of_rotation()
            1

            >>> baca.Sequence().period_of_rotation()
            0

        Defined equal to length of sequence divided by degree of rotational symmetry of
        sequence.

        Returns positive integer.
        """
        return len(self) // self.degree_of_rotational_symmetry()

    def quarters(
        self,
        *,
        compound: abjad.DurationTyping = None,
        remainder: abjad.VerticalAlignment = None,
    ):
        r"""
        Splits sequence into quarter-note durations.

        ..  container:: example

            >>> list_ = baca.fractions([(2, 4), (6, 4)])
            >>> for item in baca.Sequence(list_).quarters():
            ...     item
            ...
            Sequence([NonreducedFraction(1, 4)])
            Sequence([NonreducedFraction(1, 4)])
            Sequence([NonreducedFraction(1, 4)])
            Sequence([NonreducedFraction(1, 4)])
            Sequence([NonreducedFraction(1, 4)])
            Sequence([NonreducedFraction(1, 4)])
            Sequence([NonreducedFraction(1, 4)])
            Sequence([NonreducedFraction(1, 4)])

        ..  container:: example

            >>> list_ = baca.fractions([(6, 4)])
            >>> for item in baca.Sequence(list_).quarters(compound=(3, 2)):
            ...     item
            ...
            Sequence([NonreducedFraction(3, 8)])
            Sequence([NonreducedFraction(3, 8)])
            Sequence([NonreducedFraction(3, 8)])
            Sequence([NonreducedFraction(3, 8)])

        ..  container:: example

            Maps to each division: splits by ``1/4`` with remainder on right:

            >>> divisions = baca.fractions([(7, 8), (3, 8), (5, 8)])
            >>> divisions = baca.Sequence(divisions).map(
            ...     lambda _: baca.Sequence(_).quarters()
            ... )
            >>> for sequence in divisions:
            ...     print("sequence:")
            ...     for division in sequence:
            ...         print(f"\t{repr(division)}")
            sequence:
                Sequence([NonreducedFraction(2, 8)])
                Sequence([NonreducedFraction(2, 8)])
                Sequence([NonreducedFraction(2, 8)])
                Sequence([NonreducedFraction(1, 8)])
            sequence:
                Sequence([NonreducedFraction(2, 8)])
                Sequence([NonreducedFraction(1, 8)])
            sequence:
                Sequence([NonreducedFraction(2, 8)])
                Sequence([NonreducedFraction(2, 8)])
                Sequence([NonreducedFraction(1, 8)])

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))

            >>> lilypond_file = abjad.illustrators.selection(music)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    {
                        \time 15/8
                        c'4
                        c'4
                        c'4
                        c'8
                        c'4
                        c'8
                        c'4
                        c'4
                        c'8
                    }
                >>

        """
        sequence = self.split_divisions(
            [(1, 4)], cyclic=True, compound=compound, remainder=remainder
        )
        return sequence

    def ratios(
        self,
        ratios: typing.Sequence[abjad.RatioTyping],
        *,
        rounded: bool = None,
    ):
        r"""
        Splits sequence by ``ratios``.

        ..  container:: example

            Splits sequence by exact ``2:1`` ratio:

            >>> time_signatures = baca.fractions([(5, 8), (6, 8)])
            >>> divisions = baca.Sequence(time_signatures)
            >>> divisions = divisions.ratios([(2, 1)])
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                NonreducedFraction(5, 8)
                NonreducedFraction(7, 24)
            sequence:
                NonreducedFraction(11, 24)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))

            >>> lilypond_file = abjad.illustrators.selection(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    {
                        \time 5/8
                        c'2
                        ~
                        c'8
                        \tweak edge-height #'(0.7 . 0)
                        \times 16/24
                        {
                            \time 6/8
                            c'4..
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 16/24
                        {
                            c'2
                            ~
                            c'8.
                        }
                    }
                >>

            Splits divisions by rounded ``2:1`` ratio:

            >>> time_signatures = baca.fractions([(5, 8), (6, 8)])
            >>> divisions = baca.Sequence(time_signatures)
            >>> divisions = divisions.ratios([(2, 1)], rounded=True)
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                NonreducedFraction(5, 8)
                NonreducedFraction(2, 8)
            sequence:
                NonreducedFraction(4, 8)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))

            >>> lilypond_file = abjad.illustrators.selection(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    {
                        \time 5/8
                        c'2
                        ~
                        c'8
                        \time 6/8
                        c'4
                        c'2
                    }
                >>

        ..  container:: example

            Splits each division by exact ``2:1`` ratio:

            >>> time_signatures = baca.fractions([(5, 8), (6, 8)])
            >>> divisions = baca.Sequence(time_signatures).map(
            ...     lambda _: baca.Sequence(_).ratios([(2, 1)])
            ... )
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                Sequence([NonreducedFraction(10, 24)])
                Sequence([NonreducedFraction(5, 24)])
            sequence:
                Sequence([NonreducedFraction(4, 8)])
                Sequence([NonreducedFraction(2, 8)])

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))

            >>> lilypond_file = abjad.illustrators.selection(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    {
                        \tweak edge-height #'(0.7 . 0)
                        \times 16/24
                        {
                            \time 5/8
                            c'2
                            ~
                            c'8
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 16/24
                        {
                            c'4
                            ~
                            c'16
                        }
                        \time 6/8
                        c'2
                        c'4
                    }
                >>

            Splits each division by rounded ``2:1`` ratio:

            >>> time_signatures = baca.fractions([(5, 8), (6, 8)])
            >>> divisions = baca.Sequence(time_signatures).map(
            ...     lambda _: baca.Sequence(_).ratios([(2, 1)], rounded=True)
            ... )
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                Sequence([NonreducedFraction(3, 8)])
                Sequence([NonreducedFraction(2, 8)])
            sequence:
                Sequence([NonreducedFraction(4, 8)])
                Sequence([NonreducedFraction(2, 8)])

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))

            >>> lilypond_file = abjad.illustrators.selection(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    {
                        \time 5/8
                        c'4.
                        c'4
                        \time 6/8
                        c'2
                        c'4
                    }
                >>

        ..  container:: example

            Splits divisions with alternating exact ``2:1`` and ``1:1:1`` ratios:

            >>> ratios = abjad.CyclicTuple([(2, 1), (1, 1, 1)])
            >>> time_signatures = baca.fractions([(5, 8), (6, 8)])
            >>> divisions = []
            >>> for i, time_signature in enumerate(time_signatures):
            ...     ratio = ratios[i]
            ...     sequence = baca.Sequence(time_signature)
            ...     sequence = sequence.ratios([ratio])
            ...     divisions.append(sequence)
            ...
            >>> divisions = baca.Sequence(divisions)
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                Sequence([NonreducedFraction(10, 24)])
                Sequence([NonreducedFraction(5, 24)])
            sequence:
                Sequence([NonreducedFraction(2, 8)])
                Sequence([NonreducedFraction(2, 8)])
                Sequence([NonreducedFraction(2, 8)])

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))

            >>> lilypond_file = abjad.illustrators.selection(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    {
                        \tweak edge-height #'(0.7 . 0)
                        \times 16/24
                        {
                            \time 5/8
                            c'2
                            ~
                            c'8
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 16/24
                        {
                            c'4
                            ~
                            c'16
                        }
                        \time 6/8
                        c'4
                        c'4
                        c'4
                    }
                >>

            Splits divisions with alternating rounded ``2:1`` and ``1:1:1`` ratios:

            >>> ratios = abjad.CyclicTuple([(2, 1), (1, 1, 1)])
            >>> time_signatures = baca.fractions([(5, 8), (6, 8)])
            >>> divisions = []
            >>> for i, time_signature in enumerate(time_signatures):
            ...     ratio = ratios[i]
            ...     sequence = baca.Sequence(time_signature)
            ...     sequence = sequence.ratios([ratio], rounded=True)
            ...     divisions.append(sequence)
            ...
            >>> divisions = baca.Sequence(divisions)
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                Sequence([NonreducedFraction(3, 8)])
                Sequence([NonreducedFraction(2, 8)])
            sequence:
                Sequence([NonreducedFraction(2, 8)])
                Sequence([NonreducedFraction(2, 8)])
                Sequence([NonreducedFraction(2, 8)])

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))

            >>> lilypond_file = abjad.illustrators.selection(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    {
                        \time 5/8
                        c'4.
                        c'4
                        \time 6/8
                        c'4
                        c'4
                        c'4
                    }
                >>

        """
        ratios_ = abjad.CyclicTuple([abjad.Ratio(_) for _ in ratios])
        if rounded is not None:
            rounded = bool(rounded)
        weight = sum(self)
        assert isinstance(weight, abjad.NonreducedFraction)
        numerator, denominator = weight.pair
        ratio = ratios_[0]
        if rounded is True:
            numerators = ratio.partition_integer(numerator)
            divisions = [
                abjad.NonreducedFraction((numerator, denominator))
                for numerator in numerators
            ]
        else:
            divisions = []
            ratio_weight = sum(ratio)
            for number in ratio:
                multiplier = abjad.Fraction(number, ratio_weight)
                division = multiplier * weight
                divisions.append(division)
        sequence = self.split(divisions)
        sequence = Sequence(sequence)
        return sequence

    def repeat_by(self, counts=None, cyclic=None):
        r"""
        Repeat sequence elements at ``counts``.

        ..  container:: example

            With no counts:

            ..  container:: example

                >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).repeat_by()
                Sequence([[1, 2, 3], 4, [5, 6]])

        ..  container:: example

            With acyclic counts:

            >>> sequence = baca.Sequence([[1, 2, 3], 4, [5, 6]])

            ..  container:: example

                >>> sequence.repeat_by([0])
                Sequence([4, [5, 6]])

                >>> sequence.repeat_by([1])
                Sequence([[1, 2, 3], 4, [5, 6]])

                >>> sequence.repeat_by([2])
                Sequence([[1, 2, 3], [1, 2, 3], 4, [5, 6]])

                >>> sequence.repeat_by([3])
                Sequence([[1, 2, 3], [1, 2, 3], [1, 2, 3], 4, [5, 6]])

            ..  container:: example

                >>> sequence.repeat_by([1, 0])
                Sequence([[1, 2, 3], [5, 6]])

                >>> sequence.repeat_by([1, 1])
                Sequence([[1, 2, 3], 4, [5, 6]])

                >>> sequence.repeat_by([1, 2])
                Sequence([[1, 2, 3], 4, 4, [5, 6]])

                >>> sequence.repeat_by([1, 3])
                Sequence([[1, 2, 3], 4, 4, 4, [5, 6]])

            ..  container:: example

                >>> sequence.repeat_by([1, 1, 0])
                Sequence([[1, 2, 3], 4])

                >>> sequence.repeat_by([1, 1, 1])
                Sequence([[1, 2, 3], 4, [5, 6]])

                >>> sequence.repeat_by([1, 1, 2])
                Sequence([[1, 2, 3], 4, [5, 6], [5, 6]])

                >>> sequence.repeat_by([1, 1, 3])
                Sequence([[1, 2, 3], 4, [5, 6], [5, 6], [5, 6]])

        ..  container:: example

            With cyclic counts:

            ..  container:: example

                >>> sequence.repeat_by([0], cyclic=True)
                Sequence([])

                >>> sequence.repeat_by([1], cyclic=True)
                Sequence([[1, 2, 3], 4, [5, 6]])

                >>> sequence.repeat_by([2], cyclic=True)
                Sequence([[1, 2, 3], [1, 2, 3], 4, 4, [5, 6], [5, 6]])

                >>> sequence.repeat_by([3], cyclic=True)
                Sequence([[1, 2, 3], [1, 2, 3], [1, 2, 3], 4, 4, 4, [5, 6], [5, 6], [5, 6]])

            ..  container:: example

                >>> sequence.repeat_by([2, 0], cyclic=True)
                Sequence([[1, 2, 3], [1, 2, 3], [5, 6], [5, 6]])

                >>> sequence.repeat_by([2, 1], cyclic=True)
                Sequence([[1, 2, 3], [1, 2, 3], 4, [5, 6], [5, 6]])

                >>> sequence.repeat_by([2, 2], cyclic=True)
                Sequence([[1, 2, 3], [1, 2, 3], 4, 4, [5, 6], [5, 6]])

                >>> sequence.repeat_by([2, 3], cyclic=True)
                Sequence([[1, 2, 3], [1, 2, 3], 4, 4, 4, [5, 6], [5, 6]])

        Raises exception on negative counts.

        Returns new sequence.
        """
        if counts is None:
            return type(self)(self)
        counts = counts or [1]
        assert isinstance(counts, collections.abc.Iterable)
        if cyclic is True:
            counts = abjad.CyclicTuple(counts)
        items = []
        for i, item in enumerate(self):
            try:
                count = counts[i]
            except IndexError:
                count = 1
            items.extend(count * [item])
        return type(self)(items)

    def reveal(self, count=None):
        r"""
        Reveals contents of sequence.

        ..  container:: example

            With no count:

            ..  container:: example

                >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal()
                Sequence([[1, 2, 3], 4, [5, 6]])

        ..  container:: example

            With zero count:

            ..  container:: example

                >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=0)
                Sequence([])

        ..  container:: example

            With positive count:

            ..  container:: example

                >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=1)
                Sequence([[1]])

                >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=2)
                Sequence([[1, 2]])

                >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=3)
                Sequence([[1, 2, 3]])

                >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=4)
                Sequence([[1, 2, 3], 4])

                >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=5)
                Sequence([[1, 2, 3], 4, [5]])

                >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=6)
                Sequence([[1, 2, 3], 4, [5, 6]])

                >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=99)
                Sequence([[1, 2, 3], 4, [5, 6]])

        ..  container:: example

            With negative count:

            ..  container:: example

                >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=-1)
                Sequence([[6]])

                >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=-2)
                Sequence([[5, 6]])

                >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=-3)
                Sequence([4, [5, 6]])

                >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=-4)
                Sequence([[3], 4, [5, 6]])

                >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=-5)
                Sequence([[2, 3], 4, [5, 6]])

                >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=-6)
                Sequence([[1, 2, 3], 4, [5, 6]])

                >>> baca.Sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=-99)
                Sequence([[1, 2, 3], 4, [5, 6]])

        Returns new sequence.
        """
        if count is None:
            return type(self)(items=self)
        if count == 0:
            return type(self)()
        if count < 0:
            result = self.reverse(recurse=True)
            result = result.reveal(count=abs(count))
            result = result.reverse(recurse=True)
            return result
        current = 0
        items_ = []
        for item in self:
            if isinstance(item, collections.abc.Iterable):
                subitems_ = []
                for subitem in item:
                    subitems_.append(subitem)
                    current += 1
                    if current == count:
                        item_ = type(item)(subitems_)
                        items_.append(item_)
                        return type(self)(items=items_)
                item_ = type(item)(subitems_)
                items_.append(item_)
            else:
                items_.append(item)
                current += 1
                if current == count:
                    return type(self)(items=items_)
        return type(self)(items=items_)

    def split_divisions(
        self,
        durations: typing.List[abjad.DurationTyping],
        *,
        compound: abjad.DurationTyping = None,
        cyclic: bool = None,
        remainder: abjad.HorizontalAlignment = None,
        remainder_fuse_threshold: abjad.DurationTyping = None,
    ):
        r"""
        Splits sequence divisions by ``durations``.

        ..  container:: example

            Splits every five sixteenths:

            >>> divisions = baca.fractions(10 * [(1, 8)])
            >>> divisions = baca.Sequence(divisions)
            >>> divisions = divisions.split_divisions([(5, 16)], cyclic=True)
            >>> for i, sequence_ in enumerate(divisions):
            ...     print(f"sequence {i}")
            ...     for division in sequence_:
            ...         print("\t" + repr(division))
            sequence 0
                NonreducedFraction(1, 8)
                NonreducedFraction(1, 8)
                NonreducedFraction(1, 16)
            sequence 1
                NonreducedFraction(1, 16)
                NonreducedFraction(1, 8)
                NonreducedFraction(1, 8)
            sequence 2
                NonreducedFraction(1, 8)
                NonreducedFraction(1, 8)
                NonreducedFraction(1, 16)
            sequence 3
                NonreducedFraction(1, 16)
                NonreducedFraction(1, 8)
                NonreducedFraction(1, 8)

        ..  container:: example

            Fuses divisions and then splits by ``1/4`` with remainder on right:

            >>> divisions = [(7, 8), (3, 8), (5, 8)]
            >>> divisions = [abjad.NonreducedFraction(_) for _ in divisions]
            >>> divisions = baca.Sequence(divisions).fuse()
            >>> divisions = divisions.split_divisions([(1, 4)], cyclic=True)
            >>> for item in divisions:
            ...     item
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(1, 8)])

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))

            >>> lilypond_file = abjad.illustrators.selection(music)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    {
                        \time 15/8
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                        c'8
                    }
                >>

            Fuses remainder:

            >>> divisions = [(7, 8), (3, 8), (5, 8)]
            >>> divisions = [abjad.NonreducedFraction(_) for _ in divisions]
            >>> divisions = baca.Sequence(divisions).fuse()
            >>> divisions = divisions.split_divisions(
            ...     [(1, 4)],
            ...     cyclic=True,
            ...     remainder_fuse_threshold=(1, 8),
            ... )
            >>> for item in divisions:
            ...     item
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(3, 8)])

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))

            >>> lilypond_file = abjad.illustrators.selection(music)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    {
                        \time 15/8
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4.
                    }
                >>

        ..  container:: example

            Fuses divisions and then splits by ``1/4`` with remainder on left:

            >>> divisions = [(7, 8), (3, 8), (5, 8)]
            >>> divisions = [abjad.NonreducedFraction(_) for _ in divisions]
            >>> divisions = baca.Sequence(divisions).fuse()
            >>> divisions = divisions.split_divisions(
            ...     [(1, 4)],
            ...     cyclic=True,
            ...     remainder=abjad.Left,
            ... )
            >>> for item in divisions:
            ...     item
            Sequence([NonreducedFraction(1, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))

            >>> lilypond_file = abjad.illustrators.selection(music)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    {
                        \time 15/8
                        c'8
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                    }
                >>

            Fuses remainder:

            >>> divisions = [(7, 8), (3, 8), (5, 8)]
            >>> divisions = [abjad.NonreducedFraction(_) for _ in divisions]
            >>> divisions = baca.Sequence(divisions).fuse()
            >>> divisions = divisions.split_divisions(
            ...     [(1, 4)],
            ...     cyclic=True,
            ...     remainder=abjad.Left,
            ...     remainder_fuse_threshold=(1, 8),
            ... )
            >>> for item in divisions:
            ...     item
            Sequence([NonreducedFraction(3, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))

            >>> lilypond_file = abjad.illustrators.selection(music)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    {
                        \time 15/8
                        c'4.
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                    }
                >>

        ..  container:: example

            Splits each division into quarters and positions remainder at right:

            >>> def quarters(sequence):
            ...     sequence = baca.Sequence(sequence)
            ...     sequence = sequence.quarters()
            ...     sequence = sequence.flatten(depth=-1)
            ...     return sequence

            >>> time_signatures = baca.fractions([(7, 8), (7, 8), (7, 16)])
            >>> time_signatures = [abjad.NonreducedFraction(_) for _ in time_signatures]
            >>> divisions = baca.Sequence(time_signatures).map(quarters)
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                NonreducedFraction(2, 8)
                NonreducedFraction(2, 8)
                NonreducedFraction(2, 8)
                NonreducedFraction(1, 8)
            sequence:
                NonreducedFraction(2, 8)
                NonreducedFraction(2, 8)
                NonreducedFraction(2, 8)
                NonreducedFraction(1, 8)
            sequence:
                NonreducedFraction(4, 16)
                NonreducedFraction(3, 16)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))

            >>> lilypond_file = abjad.illustrators.selection(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    {
                        \time 7/8
                        c'4
                        c'4
                        c'4
                        c'8
                        \time 7/8
                        c'4
                        c'4
                        c'4
                        c'8
                        \time 7/16
                        c'4
                        c'8.
                    }
                >>

        ..  container:: example

            Splits each division into quarters and positions remainder at left:

            >>> def quarters(sequence):
            ...     sequence = baca.Sequence(sequence)
            ...     sequence = sequence.quarters(remainder=abjad.Left)
            ...     sequence = sequence.flatten(depth=-1)
            ...     return sequence

            >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
            >>> time_signatures = [abjad.NonreducedFraction(_) for _ in time_signatures]
            >>> divisions = baca.Sequence(time_signatures).map(quarters)
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                NonreducedFraction(1, 8)
                NonreducedFraction(2, 8)
                NonreducedFraction(2, 8)
                NonreducedFraction(2, 8)
            sequence:
                NonreducedFraction(1, 8)
                NonreducedFraction(2, 8)
                NonreducedFraction(2, 8)
                NonreducedFraction(2, 8)
            sequence:
                NonreducedFraction(3, 16)
                NonreducedFraction(4, 16)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))

            >>> lilypond_file = abjad.illustrators.selection(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    {
                        \time 7/8
                        c'8
                        c'4
                        c'4
                        c'4
                        \time 7/8
                        c'8
                        c'4
                        c'4
                        c'4
                        \time 7/16
                        c'8.
                        c'4
                    }
                >>

        ..  container:: example

            Splits each division into quarters and fuses remainder less than or equal to
            ``1/8`` to the right:

            >>> def quarters(sequence):
            ...     sequence = baca.Sequence(sequence)
            ...     sequence = sequence.split_divisions(
            ...         [(1, 4)],
            ...         cyclic=True,
            ...         remainder_fuse_threshold=(1, 8),
            ...     )
            ...     sequence = sequence.flatten(depth=-1)
            ...     return sequence

            >>> time_signatures = [abjad.NonreducedFraction(5, 8)]
            >>> divisions = baca.Sequence(time_signatures).map(quarters)
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                NonreducedFraction(2, 8)
                NonreducedFraction(3, 8)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))

            >>> lilypond_file = abjad.illustrators.selection(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    {
                        \time 5/8
                        c'4
                        c'4.
                    }
                >>

        ..  container:: example

            Splits each division into quarters and fuses remainder less than or equal to
            ``1/8`` to the left:

            >>> def quarters(sequence):
            ...     sequence = baca.Sequence(sequence)
            ...     sequence = sequence.split_divisions(
            ...         [(1, 4)],
            ...         cyclic=True,
            ...         remainder=abjad.Left,
            ...         remainder_fuse_threshold=(1, 8),
            ...     )
            ...     sequence = sequence.flatten(depth=-1)
            ...     return sequence

            >>> time_signatures = [abjad.NonreducedFraction(5, 8)]
            >>> divisions = baca.Sequence(time_signatures).map(quarters)
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                NonreducedFraction(3, 8)
                NonreducedFraction(2, 8)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))

            >>> lilypond_file = abjad.illustrators.selection(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    {
                        \time 5/8
                        c'4.
                        c'4
                    }
                >>

        ..  container:: example

            Splits each division into compound quarters:

            >>> def quarters(sequence):
            ...     sequence = baca.Sequence(sequence)
            ...     sequence = sequence.quarters(compound=(3, 2))
            ...     sequence = sequence.flatten(depth=-1)
            ...     return sequence

            >>> time_signatures = baca.fractions([(3, 4), (6, 8)])
            >>> divisions = baca.Sequence(time_signatures)
            >>> divisions = divisions.map(quarters)
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                NonreducedFraction(1, 4)
                NonreducedFraction(1, 4)
                NonreducedFraction(1, 4)
            sequence:
                NonreducedFraction(3, 8)
                NonreducedFraction(3, 8)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))

            >>> lilypond_file = abjad.illustrators.selection(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    {
                        \time 3/4
                        c'4
                        c'4
                        c'4
                        \time 6/8
                        c'4.
                        c'4.
                    }
                >>

        ..  container:: example

            Splits each division by durations and rotates durations one to the left at
            each new division:

            >>> durations = baca.Sequence([(1, 16), (1, 8), (1, 4)])
            >>> time_signatures = baca.fractions([(7, 16), (7, 16), (7, 16)])
            >>> divisions = []
            >>> for i, time_signature in enumerate(time_signatures):
            ...     durations_ = durations.rotate(n=-i)
            ...     sequence = baca.Sequence(time_signature)
            ...     sequence = sequence.split_divisions(durations_)
            ...     sequence = sequence.flatten(depth=-1)
            ...     divisions.append(sequence)
            ...
            >>> divisions = baca.Sequence(divisions)
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                NonreducedFraction(1, 16)
                NonreducedFraction(2, 16)
                NonreducedFraction(4, 16)
            sequence:
                NonreducedFraction(2, 16)
                NonreducedFraction(4, 16)
                NonreducedFraction(1, 16)
            sequence:
                NonreducedFraction(4, 16)
                NonreducedFraction(1, 16)
                NonreducedFraction(2, 16)

            >>> rhythm_maker = rmakers.note()
            >>> divisions = divisions.flatten(depth=-1)
            >>> music = rhythm_maker(divisions)

            >>> lilypond_file = abjad.illustrators.selection(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff"
                    {
                        \time 7/16
                        c'16
                        c'8
                        c'4
                        \time 7/16
                        c'8
                        c'4
                        c'16
                        \time 7/16
                        c'4
                        c'16
                        c'8
                    }
                >>

        """
        durations = [abjad.Duration(_) for _ in durations]
        if compound is not None:
            compound = abjad.Multiplier(compound)
        if compound is not None:
            divisions = self.flatten(depth=-1)
            meters = [abjad.Meter(_) for _ in divisions]
            if all(_.is_compound for _ in meters):
                durations = [compound * _ for _ in durations]
        if cyclic is not None:
            cyclic = bool(cyclic)
        if remainder is not None:
            assert remainder in (abjad.Left, abjad.Right), repr(remainder)
        if remainder_fuse_threshold is not None:
            remainder_fuse_threshold = abjad.Duration(remainder_fuse_threshold)
        sequence = abjad.Sequence.split(self, durations, cyclic=cyclic, overhang=True)
        without_overhang = abjad.Sequence.split(
            self, durations, cyclic=cyclic, overhang=False
        )
        if sequence != without_overhang:
            items = list(sequence)
            remaining_item = items.pop()
            if remainder == abjad.Left:
                if remainder_fuse_threshold is None:
                    items.insert(0, remaining_item)
                elif sum(remaining_item) <= remainder_fuse_threshold:
                    fused_value = Sequence([remaining_item, items[0]])
                    fused_value_ = fused_value.flatten(depth=-1)
                    fused_value = Sequence(fused_value_).fuse()
                    items[0] = fused_value
                else:
                    items.insert(0, remaining_item)
            else:
                if remainder_fuse_threshold is None:
                    items.append(remaining_item)
                elif sum(remaining_item) <= remainder_fuse_threshold:
                    fused_value = Sequence([items[-1], remaining_item])
                    fused_value_ = fused_value.flatten(depth=-1)
                    fused_value = Sequence(fused_value_).fuse()
                    items[-1] = fused_value
                else:
                    items.append(remaining_item)
            sequence = Sequence(items)
        return sequence
