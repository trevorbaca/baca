"""
Figures.
"""
import copy
import dataclasses
import math as python_math
import typing
from inspect import currentframe as _frame

import abjad
from abjadext import rmakers

from . import commands as _commands
from . import cursor as _cursor
from . import select as _select
from . import tags as _tags
from .enums import enums as _enums


class Stack:
    """
    Stack.
    """

    __slots__ = ("_commands",)

    # TODO: remove after removal of new()
    _positional_arguments_name = "commands"

    def __init__(self, *commands) -> None:
        commands = commands or ()
        commands_ = tuple(commands)
        self._commands = commands_

    def __call__(self, argument: typing.Any, **keywords) -> typing.Any:
        if not self.commands:
            return argument
        try:
            result: typing.Any = self.commands[0](argument, **keywords)
        except Exception:
            message = "exception while calling:\n"
            message += f"   {self.commands[0]}"
            raise Exception(message)
        for command in self.commands[1:]:
            try:
                result_ = command(result)
            except Exception:
                message = "exception while calling:\n"
                message += f"   {command}"
                raise Exception(message)
            # if result_ is not None:
            if result_ not in (True, False, None):
                result = result_
        if result not in (True, False, None):
            return result

    def __eq__(self, argument) -> bool:
        """
        Compares ``commands``.
        """
        if isinstance(argument, type(self)):
            return self.commands == argument.commands
        return False

    def __hash__(self) -> int:
        """
        Hashes object.
        """
        return hash(str(self))

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        return f"{type(self).__name__}(commands={self.commands})"

    @property
    def commands(self):
        """
        Gets commands.
        """
        return list(self._commands)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class LMR:
    """
    Left-middle-right.

    ..  container:: example

        Left counts equal to a single 1:

        >>> lmr = baca.lmr(
        ...     left_counts=[1],
        ...     left_cyclic=False,
        ...     left_length=3,
        ...     right_length=2,
        ... )

        >>> parts = lmr([1])
        >>> for part in parts: part
        [1]

        >>> parts = lmr([1, 2])
        >>> for part in parts: part
        [1]
        [2]

        >>> parts = lmr([1, 2, 3])
        >>> for part in parts: part
        [1]
        [2, 3]

        >>> parts = lmr([1, 2, 3, 4])
        >>> for part in parts: part
        [1]
        [2, 3]
        [4]

        >>> parts = lmr([1, 2, 3, 4, 5])
        >>> for part in parts: part
        [1]
        [2, 3]
        [4, 5]

        >>> parts = lmr([1, 2, 3, 4, 5, 6])
        >>> for part in parts: part
        [1]
        [2, 3]
        [4]
        [5, 6]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
        >>> for part in parts: part
        [1]
        [2, 3]
        [4, 5]
        [6, 7]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
        >>> for part in parts: part
        [1]
        [2, 3]
        [4, 5, 6]
        [7, 8]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> for part in parts: part
        [1]
        [2, 3]
        [4, 5, 6, 7]
        [8, 9]

    ..  container:: example

        Left counts all equal to 1:

        >>> lmr = baca.lmr(
        ...     left_counts=[1],
        ...     left_cyclic=True,
        ...     left_length=3,
        ...     right_length=2,
        ... )

        >>> parts = lmr([1])
        >>> for part in parts: part
        [1]

        >>> parts = lmr([1, 2])
        >>> for part in parts: part
        [1]
        [2]

        >>> parts = lmr([1, 2, 3])
        >>> for part in parts: part
        [1]
        [2]
        [3]

        >>> parts = lmr([1, 2, 3, 4])
        >>> for part in parts: part
        [1]
        [2]
        [3]
        [4]

        >>> parts = lmr([1, 2, 3, 4, 5])
        >>> for part in parts: part
        [1]
        [2]
        [3]
        [4, 5]

        >>> parts = lmr([1, 2, 3, 4, 5, 6])
        >>> for part in parts: part
        [1]
        [2]
        [3]
        [4]
        [5, 6]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
        >>> for part in parts: part
        [1]
        [2]
        [3]
        [4, 5]
        [6, 7]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
        >>> for part in parts: part
        [1]
        [2]
        [3]
        [4, 5, 6]
        [7, 8]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> for part in parts: part
        [1]
        [2]
        [3]
        [4, 5, 6, 7]
        [8, 9]

    ..  container:: example

        Left length equal to 2:

        >>> lmr = baca.lmr(
        ...     left_length=2,
        ... )

        >>> parts = lmr([1])
        >>> for part in parts: part
        [1]

        >>> parts = lmr([1, 2])
        >>> for part in parts: part
        [1, 2]

        >>> parts = lmr([1, 2, 3])
        >>> for part in parts: part
        [1, 2]
        [3]

        >>> parts = lmr([1, 2, 3, 4])
        >>> for part in parts: part
        [1, 2]
        [3, 4]

        >>> parts = lmr([1, 2, 3, 4, 5])
        >>> for part in parts: part
        [1, 2]
        [3, 4, 5]

        >>> parts = lmr([1, 2, 3, 4, 5, 6])
        >>> for part in parts: part
        [1, 2]
        [3, 4, 5, 6]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
        >>> for part in parts: part
        [1, 2]
        [3, 4, 5, 6, 7]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
        >>> for part in parts: part
        [1, 2]
        [3, 4, 5, 6, 7, 8]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> for part in parts: part
        [1, 2]
        [3, 4, 5, 6, 7, 8, 9]

    ..  container:: example

        Cyclic middle counts equal to [2]:

        >>> lmr = baca.lmr(
        ...     middle_counts=[2],
        ...     middle_cyclic=True,
        ... )

        >>> parts = lmr([1])
        >>> for part in parts: part
        [1]

        >>> parts = lmr([1, 2])
        >>> for part in parts: part
        [1, 2]

        >>> parts = lmr([1, 2, 3])
        >>> for part in parts: part
        [1, 2]
        [3]

        >>> parts = lmr([1, 2, 3, 4])
        >>> for part in parts: part
        [1, 2]
        [3, 4]

        >>> parts = lmr([1, 2, 3, 4, 5])
        >>> for part in parts: part
        [1, 2]
        [3, 4]
        [5]

        >>> parts = lmr([1, 2, 3, 4, 5, 6])
        >>> for part in parts: part
        [1, 2]
        [3, 4]
        [5, 6]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
        >>> for part in parts: part
        [1, 2]
        [3, 4]
        [5, 6]
        [7]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
        >>> for part in parts: part
        [1, 2]
        [3, 4]
        [5, 6]
        [7, 8]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> for part in parts: part
        [1, 2]
        [3, 4]
        [5, 6]
        [7, 8]
        [9]

        Odd parity produces length-1 part at right.

    ..  container:: example

        Reversed cyclic middle counts equal to [2]:

        >>> lmr = baca.lmr(
        ...     middle_counts=[2],
        ...     middle_cyclic=True,
        ...     middle_reversed=True,
        ... )

        >>> parts = lmr([1])
        >>> for part in parts: part
        [1]

        >>> parts = lmr([1, 2])
        >>> for part in parts: part
        [1, 2]

        >>> parts = lmr([1, 2, 3])
        >>> for part in parts: part
        [1]
        [2, 3]

        >>> parts = lmr([1, 2, 3, 4])
        >>> for part in parts: part
        [1, 2]
        [3, 4]

        >>> parts = lmr([1, 2, 3, 4, 5])
        >>> for part in parts: part
        [1]
        [2, 3]
        [4, 5]

        >>> parts = lmr([1, 2, 3, 4, 5, 6])
        >>> for part in parts: part
        [1, 2]
        [3, 4]
        [5, 6]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
        >>> for part in parts: part
        [1]
        [2, 3]
        [4, 5]
        [6, 7]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
        >>> for part in parts: part
        [1, 2]
        [3, 4]
        [5, 6]
        [7, 8]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> for part in parts: part
        [1]
        [2, 3]
        [4, 5]
        [6, 7]
        [8, 9]

        Odd parity produces length-1 part at left.

    ..  container:: example

        Priority to the left:

        >>> lmr = baca.lmr(
        ...     left_length=2,
        ...     right_length=1,
        ... )

        >>> parts = lmr([1])
        >>> for part in parts: part
        [1]

        >>> parts = lmr([1, 2])
        >>> for part in parts: part
        [1, 2]

        >>> parts = lmr([1, 2, 3])
        >>> for part in parts: part
        [1, 2]
        [3]

        >>> parts = lmr([1, 2, 3, 4])
        >>> for part in parts: part
        [1, 2]
        [3]
        [4]

        >>> parts = lmr([1, 2, 3, 4, 5])
        >>> for part in parts: part
        [1, 2]
        [3, 4]
        [5]

        >>> parts = lmr([1, 2, 3, 4, 5, 6])
        >>> for part in parts: part
        [1, 2]
        [3, 4, 5]
        [6]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
        >>> for part in parts: part
        [1, 2]
        [3, 4, 5, 6]
        [7]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
        >>> for part in parts: part
        [1, 2]
        [3, 4, 5, 6, 7]
        [8]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> for part in parts: part
        [1, 2]
        [3, 4, 5, 6, 7, 8]
        [9]

    ..  container:: example

        Priority to the right:

        >>> lmr = baca.lmr(
        ...     left_length=2,
        ...     priority=abjad.RIGHT,
        ...     right_length=1,
        ... )

        >>> parts = lmr([1])
        >>> for part in parts: part
        [1]

        >>> parts = lmr([1, 2])
        >>> for part in parts: part
        [1]
        [2]

        >>> parts = lmr([1, 2, 3])
        >>> for part in parts: part
        [1, 2]
        [3]

        >>> parts = lmr([1, 2, 3, 4])
        >>> for part in parts: part
        [1, 2]
        [3]
        [4]

        >>> parts = lmr([1, 2, 3, 4, 5])
        >>> for part in parts: part
        [1, 2]
        [3, 4]
        [5]

        >>> parts = lmr([1, 2, 3, 4, 5, 6])
        >>> for part in parts: part
        [1, 2]
        [3, 4, 5]
        [6]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
        >>> for part in parts: part
        [1, 2]
        [3, 4, 5, 6]
        [7]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
        >>> for part in parts: part
        [1, 2]
        [3, 4, 5, 6, 7]
        [8]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> for part in parts: part
        [1, 2]
        [3, 4, 5, 6, 7, 8]
        [9]

    ..  container:: example

        Right length equal to 2:

        >>> lmr = baca.lmr(
        ...     right_length=2,
        ... )

        >>> parts = lmr([1])
        >>> for part in parts: part
        [1]

        >>> parts = lmr([1, 2])
        >>> for part in parts: part
        [1, 2]

        >>> parts = lmr([1, 2, 3])
        >>> for part in parts: part
        [1]
        [2, 3]

        >>> parts = lmr([1, 2, 3, 4])
        >>> for part in parts: part
        [1, 2]
        [3, 4]

        >>> parts = lmr([1, 2, 3, 4, 5])
        >>> for part in parts: part
        [1, 2, 3]
        [4, 5]

        >>> parts = lmr([1, 2, 3, 4, 5, 6])
        >>> for part in parts: part
        [1, 2, 3, 4]
        [5, 6]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
        >>> for part in parts: part
        [1, 2, 3, 4, 5]
        [6, 7]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
        >>> for part in parts: part
        [1, 2, 3, 4, 5, 6]
        [7, 8]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> for part in parts: part
        [1, 2, 3, 4, 5, 6, 7]
        [8, 9]

    ..  container:: example

        Right length equal to 2 and left counts equal to [1]:

        >>> lmr = baca.lmr(
        ...     left_counts=[1],
        ...     left_cyclic=False,
        ...     right_length=2,
        ... )

        >>> parts = lmr([1])
        >>> for part in parts: part
        [1]

        >>> parts = lmr([1, 2])
        >>> for part in parts: part
        [1, 2]

        >>> parts = lmr([1, 2, 3])
        >>> for part in parts: part
        [1]
        [2, 3]

        >>> parts = lmr([1, 2, 3, 4])
        >>> for part in parts: part
        [1]
        [2]
        [3, 4]

        >>> parts = lmr([1, 2, 3, 4, 5])
        >>> for part in parts: part
        [1]
        [2, 3]
        [4, 5]

        >>> parts = lmr([1, 2, 3, 4, 5, 6])
        >>> for part in parts: part
        [1]
        [2, 3, 4]
        [5, 6]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
        >>> for part in parts: part
        [1]
        [2, 3, 4, 5]
        [6, 7]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
        >>> for part in parts: part
        [1]
        [2, 3, 4, 5, 6]
        [7, 8]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> for part in parts: part
        [1]
        [2, 3, 4, 5, 6, 7]
        [8, 9]

    """

    left_counts: typing.Sequence[int] = ()
    left_cyclic: bool = False
    left_length: int = 0
    left_reversed: bool = False
    middle_counts: typing.Sequence[int] = ()
    middle_cyclic: bool = False
    middle_reversed: bool = False
    priority: int | None = None
    right_counts: typing.Sequence[int] = ()
    right_cyclic: bool = False
    right_length: int = 0
    right_reversed: bool = False

    def __post_init__(self):
        if self.left_counts is not None:
            assert abjad.math.all_are_positive_integers(self.left_counts)
        assert isinstance(self.left_cyclic, bool), repr(self.left_cyclic)
        if self.left_length is not None:
            assert isinstance(self.left_length, int), repr(self.left_length)
            assert 0 <= self.left_length, repr(self.left_length)
        assert isinstance(self.left_reversed, bool), repr(self.left_reversed)
        if self.middle_counts is not None:
            assert abjad.math.all_are_positive_integers(self.middle_counts)
        assert isinstance(self.middle_cyclic, bool), repr(self.middle_cyclic)
        assert isinstance(self.middle_reversed, bool), repr(self.middle_reversed)
        if self.priority is not None:
            assert self.priority in (abjad.LEFT, abjad.RIGHT)
        if self.right_counts is not None:
            assert abjad.math.all_are_positive_integers(self.right_counts)
        assert isinstance(self.right_cyclic, bool), repr(self.right_cyclic)
        if self.right_length is not None:
            assert isinstance(self.right_length, int), repr(self.right_length)
            assert 0 <= self.right_length, repr(self.right_length)
        assert isinstance(self.right_reversed, bool), repr(self.right_reversed)

    def __call__(self, sequence=None):
        assert isinstance(sequence, list), repr(sequence)
        top_lengths = self._get_top_lengths(len(sequence))
        top_parts = abjad.sequence.partition_by_counts(
            list(sequence), top_lengths, cyclic=False, overhang=abjad.EXACT
        )
        parts = []
        left_part, middle_part, right_part = top_parts
        if left_part:
            if self.left_counts:
                parts_ = abjad.sequence.partition_by_counts(
                    left_part,
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
                parts_ = abjad.sequence.partition_by_counts(
                    middle_part,
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
                parts_ = abjad.sequence.partition_by_counts(
                    right_part,
                    self.right_counts,
                    cyclic=self.right_cyclic,
                    overhang=True,
                    reversed_=self.right_reversed,
                )
                parts.extend(parts_)
            else:
                parts.append(right_part)
        assert isinstance(parts, list), repr(parts)
        assert all(isinstance(_, list) for _ in parts)
        return parts

    def _get_priority(self):
        if self.priority is None:
            return abjad.LEFT
        return self.priority

    def _get_top_lengths(self, total_length):
        left_length, middle_length, right_length = 0, 0, 0
        left_length = self.left_length or 0
        middle_length = 0
        right_length = self.right_length or 0
        if left_length and right_length:
            if self._get_priority() == abjad.LEFT:
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


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Acciaccatura:
    r"""
    Acciaccatura.

    ..  container:: example

        Sixteenth-note acciaccaturas by default:

        >>> stack = baca.stack(
        ...     baca.figure([1], 8, acciaccatura=True),
        ...     rmakers.beam(),
        ... )

        >>> collections = [
        ...     [0],
        ...     [2, 10],
        ...     [18, 16, 15],
        ...     [20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     [20, 19, 9, 0, 2, 10],
        ... ]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/4
                        c'8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            d'16
                        }
                        bf'8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            fs''16
                            [
                            e''16
                            ]
                        }
                        ef''8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            af''16
                            [
                            g''16
                            a'16
                            ]
                        }
                        c'8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            d'16
                            [
                            bf'16
                            fs''16
                            e''16
                            ]
                        }
                        ef''8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            af''16
                            [
                            g''16
                            a'16
                            c'16
                            d'16
                            ]
                        }
                        bf'8
                    }
                }
            >>

    ..  container:: example

        Eighth-note acciaccaturas:

        >>> specifier = baca.Acciaccatura([abjad.Duration(1, 8)])
        >>> stack = baca.stack(
        ...     baca.figure([1], 8, acciaccatura=specifier),
        ...     rmakers.beam(),
        ... )

        >>> collections = [
        ...     [0],
        ...     [2, 10],
        ...     [18, 16, 15],
        ...     [20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     [20, 19, 9, 0, 2, 10],
        ... ]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/4
                        c'8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            d'8
                        }
                        bf'8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            fs''8
                            [
                            e''8
                            ]
                        }
                        ef''8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            af''8
                            [
                            g''8
                            a'8
                            ]
                        }
                        c'8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            d'8
                            [
                            bf'8
                            fs''8
                            e''8
                            ]
                        }
                        ef''8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            af''8
                            [
                            g''8
                            a'8
                            c'8
                            d'8
                            ]
                        }
                        bf'8
                    }
                }
            >>

    ..  container:: example

        As many acciaccaturas as possible per collection:

        >>> stack = baca.stack(
        ...     baca.figure([1], 8, acciaccatura=True),
        ...     rmakers.beam(),
        ... )

        >>> collections = [
        ...     [0],
        ...     [2, 10],
        ...     [18, 16, 15],
        ...     [20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     [20, 19, 9, 0, 2, 10],
        ... ]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/4
                        c'8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            d'16
                        }
                        bf'8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            fs''16
                            [
                            e''16
                            ]
                        }
                        ef''8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            af''16
                            [
                            g''16
                            a'16
                            ]
                        }
                        c'8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            d'16
                            [
                            bf'16
                            fs''16
                            e''16
                            ]
                        }
                        ef''8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            af''16
                            [
                            g''16
                            a'16
                            c'16
                            d'16
                            ]
                        }
                        bf'8
                    }
                }
            >>

    ..  container:: example

        At most two acciaccaturas at the beginning of every collection:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1],
        ...         8,
        ...         acciaccatura=baca.lmr(
        ...             left_length=3,
        ...             right_counts=[1],
        ...             right_cyclic=True,
        ...         ),
        ...     ),
        ...     rmakers.beam(),
        ... )

        >>> collections = [
        ...     [0],
        ...     [2, 10],
        ...     [18, 16, 15],
        ...     [20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     [20, 19, 9, 0, 2, 10],
        ... ]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/2
                        c'8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            d'16
                        }
                        bf'8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            fs''16
                            [
                            e''16
                            ]
                        }
                        ef''8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            af''16
                            [
                            g''16
                            ]
                        }
                        a'8
                        [
                        c'8
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            d'16
                            [
                            bf'16
                            ]
                        }
                        fs''8
                        [
                        e''8
                        ef''8
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            af''16
                            [
                            g''16
                            ]
                        }
                        a'8
                        [
                        c'8
                        d'8
                        bf'8
                        ]
                    }
                }
            >>

    ..  container:: example

        At most two acciaccaturas at the end of every collection:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1],
        ...         8,
        ...         acciaccatura=baca.lmr(
        ...             right_length=3,
        ...             left_counts=[1],
        ...             left_cyclic=True,
        ...         ),
        ...     ),
        ...     rmakers.beam(),
        ... )

        >>> collections = [
        ...     [0],
        ...     [2, 10],
        ...     [18, 16, 15],
        ...     [20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     [20, 19, 9, 0, 2, 10],
        ... ]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/2
                        c'8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            d'16
                        }
                        bf'8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            fs''16
                            [
                            e''16
                            ]
                        }
                        ef''8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        af''8
                        [
                        \acciaccatura {
                            g''16
                            [
                            a'16
                            ]
                        }
                        c'8
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        d'8
                        [
                        bf'8
                        \acciaccatura {
                            fs''16
                            [
                            e''16
                            ]
                        }
                        ef''8
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        af''8
                        [
                        g''8
                        a'8
                        \acciaccatura {
                            c'16
                            [
                            d'16
                            ]
                        }
                        bf'8
                        ]
                    }
                }
            >>

    ..  container:: example

        At most two acciaccaturas at the beginning of every collection and then at
        most two acciaccaturas at the end of every collection:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1],
        ...         8,
        ...         acciaccatura=baca.lmr(
        ...             left_length=3,
        ...             middle_counts=[1],
        ...             middle_cyclic=True,
        ...             right_length=3,
        ...         ),
        ...     ),
        ...     rmakers.beam(),
        ... )

        >>> collections = [
        ...     [0],
        ...     [2, 10],
        ...     [18, 16, 15],
        ...     [20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     [20, 19, 9, 0, 2, 10],
        ... ]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 9/8
                        c'8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            d'16
                        }
                        bf'8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            fs''16
                            [
                            e''16
                            ]
                        }
                        ef''8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            af''16
                            [
                            g''16
                            ]
                        }
                        a'8
                        [
                        c'8
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            d'16
                            [
                            bf'16
                            ]
                        }
                        fs''8
                        [
                        \acciaccatura {
                            e''16
                        }
                        ef''8
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            af''16
                            [
                            g''16
                            ]
                        }
                        a'8
                        [
                        \acciaccatura {
                            c'16
                            [
                            d'16
                            ]
                        }
                        bf'8
                        ]
                    }
                }
            >>

    ..  container:: example

        As many acciaccaturas as possible in the middle of every collection:

        >>> stack = baca.stack(
        ...     baca.figure([1], 8, acciaccatura=baca.lmr(left_length=1)),
        ...     rmakers.beam(),
        ... )

        >>> collections = [
        ...     [0],
        ...     [2, 10],
        ...     [18, 16, 15],
        ...     [20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     [20, 19, 9, 0, 2, 10],
        ... ]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 11/8
                        c'8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        d'8
                        [
                        bf'8
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        fs''8
                        [
                        \acciaccatura {
                            e''16
                        }
                        ef''8
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        af''8
                        [
                        \acciaccatura {
                            g''16
                            [
                            a'16
                            ]
                        }
                        c'8
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        d'8
                        [
                        \acciaccatura {
                            bf'16
                            [
                            fs''16
                            e''16
                            ]
                        }
                        ef''8
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        af''8
                        [
                        \acciaccatura {
                            g''16
                            [
                            a'16
                            c'16
                            d'16
                            ]
                        }
                        bf'8
                        ]
                    }
                }
            >>

    """

    durations: typing.Sequence[abjad.Duration] = (abjad.Duration(1, 16),)
    lmr: LMR = LMR()

    def __post_init__(self):
        #        durations_ = [abjad.Duration(_) for _ in self.durations]
        #        self.durations = durations_
        assert all(isinstance(_, abjad.Duration) for _ in self.durations), repr(
            self.durations
        )
        assert isinstance(self.lmr, LMR), repr(self.lmr)

    def __call__(
        self, collection: list = None
    ) -> tuple[list[abjad.BeforeGraceContainer | None], list]:
        assert isinstance(collection, list), repr(collection)
        segment_parts = self.lmr(collection)
        segment_parts = [_ for _ in segment_parts if _]
        collection = [_[-1] for _ in segment_parts]
        durations = self.durations
        acciaccatura_containers: list[abjad.BeforeGraceContainer | None] = []
        maker = abjad.LeafMaker()
        for segment_part in segment_parts:
            if len(segment_part) <= 1:
                acciaccatura_containers.append(None)
                continue
            grace_token = list(segment_part[:-1])
            grace_leaves = maker(grace_token, durations)
            acciaccatura_container = abjad.BeforeGraceContainer(
                grace_leaves, command=r"\acciaccatura"
            )
            if 1 < len(acciaccatura_container):
                abjad.beam(
                    acciaccatura_container[:],
                    tag=_tags.function_name(_frame(), self),
                )
            acciaccatura_containers.append(acciaccatura_container)
        assert len(acciaccatura_containers) == len(collection)
        assert isinstance(collection, list), repr(collection)
        return acciaccatura_containers, collection


# TODO: frozen=True
@dataclasses.dataclass(order=True, slots=True, unsafe_hash=True)
class Anchor:
    """
    Anchor.

    ``use_remote_stop_offset`` is true when contribution anchors to remote selection stop
    offset; otherwise anchors to remote selection start offset.
    """

    figure_name: str | None = None
    local_selector: typing.Callable | None = None
    remote_selector: typing.Callable | None = None
    remote_voice_name: str | None = None
    use_remote_stop_offset: bool = False

    def __post_init__(self):
        if self.figure_name is not None:
            assert isinstance(self.figure_name, str), repr(self.figure_name)
        if self.local_selector is not None and not callable(self.local_selector):
            raise TypeError(f"must be callable: {self.local_selector!r}.")
        if self.remote_selector is not None and not callable(self.remote_selector):
            raise TypeError(f"must be callable: {self.remote_selector!r}.")
        if self.remote_voice_name is not None:
            assert isinstance(self.remote_voice_name, str), repr(self.remote_voice_name)
        assert isinstance(self.use_remote_stop_offset, bool), repr(
            self.use_remote_stop_offset
        )


class Coat:
    """
    Coat.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_argument",)

    ### INITIALIZER ###

    def __init__(self, argument: int | str | abjad.Pitch) -> None:
        self._argument = argument

    ### PUBLIC PROPERTIES ###

    @property
    def argument(self) -> int | str | abjad.Pitch:
        """
        Gets argument.
        """
        return self._argument


def _matches_pitch(pitched_leaf, pitch_object):
    if isinstance(pitch_object, Coat):
        pitch_object = pitch_object.argument
    if pitch_object is None:
        return False
    if isinstance(pitched_leaf, abjad.Note):
        written_pitches = [pitched_leaf.written_pitch]
    elif isinstance(pitched_leaf, abjad.Chord):
        written_pitches = pitched_leaf.written_pitches
    else:
        raise TypeError(pitched_leaf)
    if isinstance(pitch_object, int | float):
        source = [_.number for _ in written_pitches]
    elif isinstance(pitch_object, abjad.NamedPitch):
        source = written_pitches
    elif isinstance(pitch_object, abjad.NumberedPitch):
        source = [abjad.NumberedPitch(_) for _ in written_pitches]
    elif isinstance(pitch_object, abjad.NamedPitchClass):
        source = [abjad.NamedPitchClass(_) for _ in written_pitches]
    elif isinstance(pitch_object, abjad.NumberedPitchClass):
        source = [abjad.NumberedPitchClass(_) for _ in written_pitches]
    else:
        raise TypeError(f"unknown pitch object: {pitch_object!r}.")
    if not type(source[0]) is type(pitch_object):
        raise TypeError(f"{source!r} type must match {pitch_object!r}.")
    return pitch_object in source


def _trim_matching_chord(logical_tie, pitch_object):
    if isinstance(logical_tie.head, abjad.Note):
        return
    assert isinstance(logical_tie.head, abjad.Chord), repr(logical_tie)
    if isinstance(pitch_object, abjad.PitchClass):
        raise NotImplementedError(logical_tie, pitch_object)
    for chord in logical_tie:
        duration = chord.written_duration
        note = abjad.Note(pitch_object, duration)
        abjad.mutate.replace(chord, [note])


class Imbrication:
    """
    Imbrication.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_allow_unused_pitches",
        "_by_pitch_class",
        "_commands",
        "_hocket",
        "_segment",
        "_selector",
        "_truncate_ties",
        "_voice_name",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        voice_name: str,
        segment: list[int] = None,
        *commands,
        allow_unused_pitches: bool = False,
        by_pitch_class: bool = False,
        hocket: bool = False,
        selector=None,
        truncate_ties: bool = False,
    ) -> None:
        assert isinstance(voice_name, str), repr(voice_name)
        self._voice_name = voice_name
        if segment is not None:
            assert isinstance(segment, list), repr(segment)
        self._segment = segment
        self._commands = commands
        self._allow_unused_pitches = bool(allow_unused_pitches)
        self._by_pitch_class = bool(by_pitch_class)
        self._hocket = bool(hocket)
        if selector is not None:
            if not callable(selector):
                raise TypeError(f"callable or none only: {selector!r}.")
        self._selector = selector
        self._truncate_ties = bool(truncate_ties)

    ### SPECIAL METHODS ###

    def __call__(self, container: abjad.Container = None) -> dict[str, list]:
        """
        Calls imbrication on ``container``.
        """
        original_container = container
        container = copy.deepcopy(container)
        abjad.override(container).TupletBracket.stencil = False
        abjad.override(container).TupletNumber.stencil = False
        segment = abjad.sequence.flatten(self.segment, depth=-1)
        if self.by_pitch_class:
            segment = [abjad.NumberedPitchClass(_) for _ in segment]
        cursor = _cursor.Cursor(
            singletons=True, source=segment, suppress_exception=True
        )
        pitch_number = cursor.next()
        if self.selector is not None:
            selection = self.selector(original_container)
        selected_logical_ties = None
        if self.selector is not None:
            selection = self.selector(container)
            generator = abjad.iterate.logical_ties(selection, pitched=True)
            selected_logical_ties = list(generator)
        original_logical_ties = abjad.select.logical_ties(original_container)
        logical_ties = abjad.select.logical_ties(container)
        pairs = zip(logical_ties, original_logical_ties)
        for logical_tie, original_logical_tie in pairs:
            if (
                selected_logical_ties is not None
                and logical_tie not in selected_logical_ties
            ):
                for leaf in logical_tie:
                    duration = leaf.written_duration
                    skip = abjad.Skip(duration)
                    abjad.mutate.replace(leaf, [skip])
            elif isinstance(logical_tie.head, abjad.Rest):
                for leaf in logical_tie:
                    duration = leaf.written_duration
                    skip = abjad.Skip(duration)
                    abjad.mutate.replace(leaf, [skip])
            elif isinstance(logical_tie.head, abjad.Skip):
                pass
            elif _matches_pitch(logical_tie.head, pitch_number):
                if isinstance(pitch_number, Coat):
                    for leaf in logical_tie:
                        duration = leaf.written_duration
                        skip = abjad.Skip(duration)
                        abjad.mutate.replace(leaf, [skip])
                    pitch_number = cursor.next()
                    continue
                _trim_matching_chord(logical_tie, pitch_number)
                pitch_number = cursor.next()
                if self.truncate_ties:
                    head = logical_tie.head
                    tail = logical_tie.tail
                    for leaf in logical_tie[1:]:
                        duration = leaf.written_duration
                        skip = abjad.Skip(duration)
                        abjad.mutate.replace(leaf, [skip])
                    abjad.detach(abjad.Tie, head)
                    next_leaf = abjad.get.leaf(tail, 1)
                    if next_leaf is not None:
                        abjad.detach(abjad.RepeatTie, next_leaf)
                if self.hocket:
                    for leaf in original_logical_tie:
                        duration = leaf.written_duration
                        skip = abjad.Skip(duration)
                        abjad.mutate.replace(leaf, [skip])
            else:
                for leaf in logical_tie:
                    duration = leaf.written_duration
                    skip = abjad.Skip(duration)
                    abjad.mutate.replace(leaf, [skip])
        if not self.allow_unused_pitches and not cursor.is_exhausted:
            assert cursor.position is not None
            current, total = cursor.position - 1, len(cursor)
            raise Exception(f"{cursor!r} used only {current} of {total} pitches.")
        self._call_commands(container)
        selection = [container]
        if not self.hocket:
            pleaves = _select.pleaves(container)
            assert isinstance(pleaves, list)
            for pleaf in pleaves:
                abjad.attach(_enums.ALLOW_OCTAVE, pleaf)
        return {self.voice_name: selection}

    ### PRIVATE METHODS ###

    def _call_commands(self, container):
        assert isinstance(container, abjad.Container), repr(container)
        nested_selections = None
        commands = self.commands or []
        selections = container[:]
        for command in commands:
            if isinstance(command, Assignment):
                continue
            if isinstance(command, Imbrication):
                continue
            prototype = (
                rmakers.BeamCommand,
                rmakers.FeatherBeamCommand,
                rmakers.BeamGroupsCommand,
                rmakers.UnbeamCommand,
            )
            if isinstance(command, prototype):
                rmakers.unbeam()(selections)
            if isinstance(command, Nest):
                nested_selections = command(selections)
            else:
                command(selections)
        if nested_selections is not None:
            return nested_selections
        return selections

    ### PUBLIC PROPERTIES ###

    @property
    def allow_unused_pitches(self) -> bool | None:
        r"""
        Is true when imbrication allows unused pitches.

        ..  container:: example

            Allows unused pitches:

            >>> score = baca.docs.make_empty_score(2)
            >>> figures = baca.FigureAccumulator(score)

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ... ]
            >>> figures(
            ...     "Music.2",
            ...     collections,
            ...     baca.figure([1], 16),
            ...     rmakers.beam_groups(beam_rests=True),
            ...     baca.imbricate(
            ...         "Music.1",
            ...         [2, 19, 9, 18, 16],
            ...         baca.accent(selector=lambda _: baca.select.pheads(_)),
            ...         rmakers.beam_groups(beam_rests=True),
            ...         allow_unused_pitches=True,
            ...     ),
            ...     baca.staccato(selector=lambda _: baca.select.pheads(_)),
            ... )

            >>> accumulator = baca.CommandAccumulator(
            ...     time_signatures=figures.time_signatures,
            ... )
            >>> baca.interpret.set_up_score(
            ...     score,
            ...     accumulator,
            ...     accumulator.manifests(),
            ...     accumulator.time_signatures,
            ...     docs=True,
            ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 32)),
            ... )
            >>> figures.populate_commands(score, accumulator)

            >>> accumulator(
            ...     "Music.1",
            ...     baca.voice_one(selector=lambda _: abjad.select.leaf(_, 0)),
            ... )

            >>> accumulator(
            ...     "Music.2",
            ...     baca.voice_two(selector=lambda _: abjad.select.leaf(_, 0)),
            ... )

            >>> _, _ = baca.interpret.section(
            ...     score,
            ...     accumulator.manifests(),
            ...     accumulator.time_signatures,
            ...     commands=accumulator.commands,
            ...     move_global_context=True,
            ...     remove_tags=baca.tags.documentation_removal_tags(),
            ... )
            >>> lilypond_file = baca.lilypond.file(
            ...     score,
            ...     includes=["baca.ily"],
            ... )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                {
                    \context Staff = "Staff"
                    <<
                        \context Voice = "Skips"
                        {
                            \baca-new-spacing-section #1 #32
                            \time 5/8
                            s1 * 5/8
                        }
                        \context Voice = "Music.1"
                        {
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1)
                                {
                                    \voiceOne
                                    s16
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    - \accent
                                    s16
                                    s16
                                    s16
                                }
                                \scaleDurations #'(1 . 1)
                                {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
                                    - \accent
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
                                    - \accent
                                    s16
                                    ]
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Music.2"
                        {
                            {
                                \scaleDurations #'(1 . 1)
                                {
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    \voiceTwo
                                    c'16
                                    - \staccato
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16
                                    - \staccato
                                }
                                \scaleDurations #'(1 . 1)
                                {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    c'16
                                    - \staccato
                                    ]
                                }
                            }
                        }
                    >>
                }

        ..  container:: example exception

            Raises exception on unused pitches:

            >>> score = baca.docs.make_empty_score(2)
            >>> figures = baca.FigureAccumulator(score)

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ... ]
            >>> figures(
            ...     "Music.2",
            ...     collections,
            ...     baca.figure([1], 16),
            ...     rmakers.beam_groups(beam_rests=True),
            ...     baca.imbricate(
            ...         "Music.1",
            ...         [2, 19, 9, 18, 16],
            ...         baca.accent(selector=lambda _: baca.select.pheads(_)),
            ...         rmakers.beam_groups(beam_rests=True),
            ...         allow_unused_pitches=False,
            ...     ),
            ...     baca.staccato(selector=lambda _: baca.select.pheads(_)),
            ... )
            Traceback (most recent call last):
                ...
            Exception: Cursor(...) used only 3 of 5 pitches.

        """
        return self._allow_unused_pitches

    @property
    def by_pitch_class(self) -> bool | None:
        """
        Is true when imbrication matches on pitch-class rather than pitch.
        """
        return self._by_pitch_class

    @property
    def commands(self) -> list:
        """
        Gets commands.
        """
        return list(self._commands)

    @property
    def hocket(self) -> bool | None:
        r"""
        Is true when imbrication hockets voices.

        ..  container:: example

            Hockets voices:

            >>> score = baca.docs.make_empty_score(2)
            >>> figures = baca.FigureAccumulator(score)

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ... ]
            >>> figures(
            ...     "Music.2",
            ...     collections,
            ...     baca.figure([1], 16),
            ...     rmakers.beam_groups(beam_rests=True),
            ...     baca.imbricate(
            ...         "Music.1",
            ...         [2, 19, 9, 18, 16],
            ...         baca.accent(selector=lambda _: baca.select.pheads(_)),
            ...         rmakers.beam_groups(beam_rests=True),
            ...         hocket=True,
            ...     ),
            ...     baca.staccato(selector=lambda _: baca.select.pheads(_)),
            ... )

            >>> accumulator = baca.CommandAccumulator(
            ...     time_signatures=figures.time_signatures,
            ... )
            >>> baca.interpret.set_up_score(
            ...     score,
            ...     accumulator,
            ...     accumulator.manifests(),
            ...     accumulator.time_signatures,
            ...     docs=True,
            ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 32)),
            ... )
            >>> figures.populate_commands(score, accumulator)

            >>> accumulator(
            ...     "Music.1",
            ...     baca.voice_one(selector=lambda _: abjad.select.leaf(_, 0)),
            ... )

            >>> accumulator(
            ...     "Music.2",
            ...     baca.voice_two(selector=lambda _: abjad.select.leaf(_, 0)),
            ... )

            >>> _, _ = baca.interpret.section(
            ...     score,
            ...     accumulator.manifests(),
            ...     accumulator.time_signatures,
            ...     commands=accumulator.commands,
            ...     move_global_context=True,
            ...     remove_tags=baca.tags.documentation_removal_tags(),
            ... )
            >>> lilypond_file = baca.lilypond.file(
            ...     score,
            ...     includes=["baca.ily"],
            ... )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                {
                    \context Staff = "Staff"
                    <<
                        \context Voice = "Skips"
                        {
                            \baca-new-spacing-section #1 #32
                            \time 15/16
                            s1 * 15/16
                        }
                        \context Voice = "Music.1"
                        {
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1)
                                {
                                    \voiceOne
                                    s16
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    - \accent
                                    s16
                                    s16
                                    s16
                                }
                                \scaleDurations #'(1 . 1)
                                {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
                                    - \accent
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
                                    - \accent
                                    s16
                                }
                                \scaleDurations #'(1 . 1)
                                {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    - \accent
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16
                                    - \accent
                                    s16
                                    ]
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Music.2"
                        {
                            {
                                \scaleDurations #'(1 . 1)
                                {
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    \voiceTwo
                                    c'16
                                    - \staccato
                                    [
                                    s16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16
                                    - \staccato
                                }
                                \scaleDurations #'(1 . 1)
                                {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16
                                    - \staccato
                                    s16
                                    s16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    c'16
                                    - \staccato
                                }
                                \scaleDurations #'(1 . 1)
                                {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    d'16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    - \staccato
                                    s16
                                    s16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    ef''16
                                    - \staccato
                                    ]
                                }
                            }
                        }
                    >>
                }

        """
        return self._hocket

    @property
    def segment(self) -> list[int] | None:
        """
        Gets to-be-imbricated segment.
        """
        return self._segment

    @property
    def selector(self):
        r"""
        Gets selector.

        ..  container:: example

            Selects last nine notes:

            >>> score = baca.docs.make_empty_score(2)
            >>> figures = baca.FigureAccumulator(score)

            >>> collections = [
            ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
            ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
            ... ]
            >>> figures(
            ...     "Music.2",
            ...     collections,
            ...     baca.figure([1], 16),
            ...     rmakers.beam_groups(beam_rests=True),
            ...     baca.imbricate(
            ...         "Music.1",
            ...         [2, 18, 16, 15],
            ...         baca.accent(selector=lambda _: baca.select.pheads(_)),
            ...         rmakers.beam_groups(beam_rests=True),
            ...         selector=lambda _: baca.select.plts(_)[-9:],
            ...     ),
            ...     baca.staccato(selector=lambda _: baca.select.pheads(_)),
            ... )

            >>> accumulator = baca.CommandAccumulator(
            ...     time_signatures=figures.time_signatures,
            ... )
            >>> baca.interpret.set_up_score(
            ...     score,
            ...     accumulator,
            ...     accumulator.manifests(),
            ...     accumulator.time_signatures,
            ...     docs=True,
            ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 32)),
            ... )
            >>> figures.populate_commands(score, accumulator)

            >>> accumulator(
            ...     "Music.1",
            ...     baca.voice_one(selector=lambda _: abjad.select.leaf(_, 0)),
            ... )

            >>> accumulator(
            ...     "Music.2",
            ...     baca.voice_two(selector=lambda _: abjad.select.leaf(_, 0)),
            ... )

            >>> _, _ = baca.interpret.section(
            ...     score,
            ...     accumulator.manifests(),
            ...     accumulator.time_signatures,
            ...     commands=accumulator.commands,
            ...     move_global_context=True,
            ...     remove_tags=baca.tags.documentation_removal_tags(),
            ... )
            >>> lilypond_file = baca.lilypond.file(
            ...     score,
            ...     includes=["baca.ily"],
            ... )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                {
                    \context Staff = "Staff"
                    <<
                        \context Voice = "Skips"
                        {
                            \baca-new-spacing-section #1 #32
                            \time 9/8
                            s1 * 9/8
                        }
                        \context Voice = "Music.1"
                        {
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1)
                                {
                                    \voiceOne
                                    s16
                                    [
                                    s16
                                    s16
                                    s16
                                    s16
                                }
                                \scaleDurations #'(1 . 1)
                                {
                                    s16
                                    s16
                                    s16
                                    s16
                                }
                                \scaleDurations #'(1 . 1)
                                {
                                    s16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    - \accent
                                    s16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    - \accent
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16
                                    - \accent
                                }
                                \scaleDurations #'(1 . 1)
                                {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16
                                    - \accent
                                    s16
                                    s16
                                    s16
                                    ]
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Music.2"
                        {
                            {
                                \scaleDurations #'(1 . 1)
                                {
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    \voiceTwo
                                    c'16
                                    - \staccato
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16
                                    - \staccato
                                }
                                \scaleDurations #'(1 . 1)
                                {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    a'16
                                    - \staccato
                                }
                                \scaleDurations #'(1 . 1)
                                {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    c'16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16
                                    - \staccato
                                }
                                \scaleDurations #'(1 . 1)
                                {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
                                    - \staccato
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    a'16
                                    - \staccato
                                    ]
                                }
                            }
                        }
                    >>
                }

        """
        return self._selector

    @property
    def truncate_ties(self) -> bool | None:
        r"""
        Is true when imbrication truncates ties.

        ..  container:: example

            Truncates ties:

            >>> score = baca.docs.make_empty_score(2)
            >>> figures = baca.FigureAccumulator(score)

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> figures(
            ...     "Music.2",
            ...     collections,
            ...     baca.figure([5], 32),
            ...     rmakers.beam(),
            ...     baca.imbricate(
            ...         "Music.1",
            ...         [2, 10, 18, 19, 9],
            ...         rmakers.beam_groups(beam_rests=True),
            ...         truncate_ties=True,
            ...     ),
            ... )

            >>> accumulator = baca.CommandAccumulator(
            ...     time_signatures=figures.time_signatures,
            ... )
            >>> baca.interpret.set_up_score(
            ...     score,
            ...     accumulator,
            ...     accumulator.manifests(),
            ...     accumulator.time_signatures,
            ...     docs=True,
            ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 32)),
            ... )
            >>> figures.populate_commands(score, accumulator)

            >>> accumulator(
            ...     "Music.1",
            ...     baca.voice_one(selector=lambda _: abjad.select.leaf(_, 0)),
            ... )

            >>> accumulator(
            ...     "Music.2",
            ...     baca.voice_two(selector=lambda _: abjad.select.leaf(_, 0)),
            ... )

            >>> _, _ = baca.interpret.section(
            ...     score,
            ...     accumulator.manifests(),
            ...     accumulator.time_signatures,
            ...     commands=accumulator.commands,
            ...     move_global_context=True,
            ...     remove_tags=baca.tags.documentation_removal_tags(),
            ... )
            >>> lilypond_file = baca.lilypond.file(
            ...     score,
            ...     includes=["baca.ily"],
            ... )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                {
                    \context Staff = "Staff"
                    <<
                        \context Voice = "Skips"
                        {
                            \baca-new-spacing-section #1 #32
                            \time 45/32
                            s1 * 45/32
                        }
                        \context Voice = "Music.1"
                        {
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1)
                                {
                                    \voiceOne
                                    s8
                                    [
                                    s32
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    d'8
                                    s32
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    bf'8
                                    s32
                                }
                                \scaleDurations #'(1 . 1)
                                {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    fs''8
                                    s32
                                    s8
                                    s32
                                    s8
                                    s32
                                    s8
                                    s32
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    g''8
                                    s32
                                }
                                \scaleDurations #'(1 . 1)
                                {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    a'8
                                    s32
                                    ]
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Music.2"
                        {
                            {
                                \scaleDurations #'(1 . 1)
                                {
                                    \voiceTwo
                                    c'8
                                    [
                                    ~
                                    c'32
                                    d'8
                                    ~
                                    d'32
                                    bf'8
                                    ~
                                    bf'32
                                    ]
                                }
                                \scaleDurations #'(1 . 1)
                                {
                                    fs''8
                                    [
                                    ~
                                    fs''32
                                    e''8
                                    ~
                                    e''32
                                    ef''8
                                    ~
                                    ef''32
                                    af''8
                                    ~
                                    af''32
                                    g''8
                                    ~
                                    g''32
                                    ]
                                }
                                \scaleDurations #'(1 . 1)
                                {
                                    a'8
                                    [
                                    ~
                                    a'32
                                    ]
                                }
                            }
                        }
                    >>
                }

        """
        return self._truncate_ties

    @property
    def voice_name(self) -> str:
        """
        Gets voice name.
        """
        return self._voice_name


class FigureAccumulator:
    """
    Figure-accumulator.

    ..  container:: example exception

        Raises exception on duplicate figure name.

        >>> score = baca.docs.make_empty_score(2)
        >>> figures = baca.FigureAccumulator(score)

        >>> commands = [
        ...     baca.figure([1], 16, signature=16),
        ...     rmakers.beam(),
        ... ]

        >>> figures(
        ...     "Music.1",
        ...     [[0, 1, 2, 3]],
        ...     *commands,
        ...     figure_name='D',
        ... )

        >>> figures(
        ...     "Music.1",
        ...     [[4, 5, 6, 7]],
        ...     *commands,
        ...     figure_name='D',
        ... )
        Traceback (most recent call last):
            ...
        Exception: duplicate figure name: 'D'.

    """

    __slots__ = (
        "_current_offset",
        "_figure_number",
        "_figure_names",
        "_floating_selections",
        "_music_maker",
        "_score_stop_offset",
        "_voice_names",
        "score",
        "time_signatures",
        "voice_abbreviations",
    )

    def __init__(self, score, voice_abbreviations=None):
        assert isinstance(score, abjad.Score), repr(score)
        self.score = score
        self.voice_abbreviations = dict(voice_abbreviations or {})
        voice_names = []
        for voice in abjad.iterate.components(score, abjad.Voice):
            voice_names.append(voice.name)
        self._voice_names = voice_names
        self._current_offset = abjad.Offset(0)
        self._figure_number = 1
        self._figure_names: list[str] = []
        self._floating_selections = self._make_voice_dictionary()
        self._score_stop_offset = abjad.Offset(0)
        self.time_signatures: list[abjad.TimeSignature] = []

    def __call__(
        self,
        voice_name: str,
        collections: typing.Sequence,
        *commands,
        anchor: Anchor = None,
        do_not_label: bool = False,
        figure_name: str = "",
        figure_label_direction: int = None,
        hide_time_signature: bool | None = None,
        signature: int = None,
    ) -> None:
        assert isinstance(figure_name, str), repr(figure_name)
        voice_name = self._abbreviation(voice_name)
        prototype = (
            list,
            str,
            frozenset,
            set,
            abjad.PitchClassSegment,
            abjad.PitchSegment,
        )
        if not isinstance(collections, prototype):
            message = "collections must be coerceable:\n"
            message += f"   {collections!r}"
            raise Exception(collections)
        commands_ = list(commands)
        for command in commands_:
            if isinstance(command, Imbrication):
                voice_name_ = self._abbreviation(command.voice_name)
                command._voice_name = voice_name_
        command = None
        maker = None
        selection: list
        selections: list
        if anchor is not None:
            voice_name_ = self._abbreviation(anchor.remote_voice_name)
            # TODO: do not assign to frozen object
            anchor.remote_voice_name = voice_name_
        if isinstance(collections, str):
            tuplet = abjad.Tuplet((1, 1), collections, hide=True)
            selections = [[tuplet]]
        elif all(isinstance(_, abjad.Component) for _ in collections):
            tuplet = abjad.Tuplet((1, 1), collections, hide=True)
            selections = [[tuplet]]
        elif isinstance(commands[0], FigureMaker):
            maker = commands[0]
            selections = maker(collections)
            selections = abjad.select.flatten(selections)
            commands_ = list(commands[1:])
        else:
            assert isinstance(commands[0], Bind)
            command = commands[0]
            selections = commands[0](collections)
            selections = abjad.select.flatten(selections)
            commands_ = list(commands[1:])
        container = abjad.Container(selections)
        imbricated_selections: dict[str, list] = {}
        for command_ in commands_:
            if isinstance(command_, Imbrication):
                dictionary = command_(container)
                imbricated_selections.update(dictionary)
            else:
                command_(selections)
        leaf = abjad.select.leaf(container, 0)
        abjad.annotate(leaf, "figure_name", figure_name)
        if not do_not_label:
            self._label_figure(container, figure_name, figure_label_direction)
        selection = [container]
        duration = abjad.get.duration(selection)
        if signature is None and maker:
            signature = maker.signature
        if signature is None and command:
            primary_maker = command.assignments[0].maker
            signature = primary_maker.signature
        if signature is not None:
            duration = duration.with_denominator(signature)
        time_signature = abjad.TimeSignature(duration)
        assert isinstance(selection, list)
        voice_to_selection = {voice_name: selection}
        voice_to_selection.update(imbricated_selections)
        for value in voice_to_selection.values():
            assert isinstance(value, list), repr(value)
        contribution = Contribution(
            voice_to_selection,
            anchor=anchor,
            figure_name=figure_name,
            hide_time_signature=hide_time_signature,
            time_signature=time_signature,
        )
        self._cache_figure_name(contribution)
        self._cache_floating_selection(contribution)
        self._cache_time_signature(contribution)
        if not do_not_label:
            self._figure_number += 1

    def _abbreviation(self, voice_name):
        return self.voice_abbreviations.get(voice_name, voice_name)

    def _cache_figure_name(self, contribution):
        if not contribution.figure_name:
            return
        if contribution.figure_name in self._figure_names:
            name = contribution.figure_name
            raise Exception(f"duplicate figure name: {name!r}.")
        self._figure_names.append(contribution.figure_name)

    def _cache_floating_selection(self, contribution):
        for voice_name in contribution:
            voice_name = self.voice_abbreviations.get(voice_name, voice_name)
            selection = contribution[voice_name]
            if not selection:
                continue
            start_offset = self._get_start_offset(selection, contribution)
            stop_offset = start_offset + abjad.get.duration(selection)
            timespan = abjad.Timespan(start_offset, stop_offset)
            floating_selection = abjad.Timespan(
                timespan.start_offset,
                timespan.stop_offset,
                annotation=selection,
            )
            self._floating_selections[voice_name].append(floating_selection)
        self._current_offset = stop_offset
        self._score_stop_offset = max(self._score_stop_offset, stop_offset)

    def _cache_time_signature(self, contribution):
        if contribution.hide_time_signature:
            return
        if (
            contribution.anchor is None
            or contribution.hide_time_signature is False
            or (contribution.anchor and contribution.anchor.remote_voice_name is None)
        ):
            self.time_signatures.append(contribution.time_signature)

    def _get_figure_start_offset(self, figure_name):
        for voice_name in sorted(self._floating_selections.keys()):
            for floating_selection in self._floating_selections[voice_name]:
                leaf_start_offset = floating_selection.start_offset
                leaves = abjad.iterate.leaves(floating_selection.annotation)
                for leaf in leaves:
                    if abjad.get.annotation(leaf, "figure_name") == figure_name:
                        return leaf_start_offset
                    leaf_duration = abjad.get.duration(leaf)
                    leaf_start_offset += leaf_duration
        raise Exception(f"can not find figure {figure_name!r}.")

    def _get_leaf_timespan(self, leaf, floating_selections):
        found_leaf = False
        for floating_selection in floating_selections:
            leaf_start_offset = abjad.Offset(0)
            for leaf_ in abjad.iterate.leaves(floating_selection.annotation):
                leaf_duration = abjad.get.duration(leaf_)
                if leaf_ is leaf:
                    found_leaf = True
                    break
                leaf_start_offset += leaf_duration
            if found_leaf:
                break
        if not found_leaf:
            raise Exception(f"can not find {leaf!r} in floating selections.")
        selection_start_offset = floating_selection.start_offset
        leaf_start_offset = selection_start_offset + leaf_start_offset
        leaf_stop_offset = leaf_start_offset + leaf_duration
        return abjad.Timespan(leaf_start_offset, leaf_stop_offset)

    def _get_start_offset(self, selection, contribution):
        if (
            contribution.anchor is not None
            and contribution.anchor.figure_name is not None
        ):
            figure_name = contribution.anchor.figure_name
            start_offset = self._get_figure_start_offset(figure_name)
            return start_offset
        anchored = False
        if contribution.anchor is not None:
            remote_voice_name = contribution.anchor.remote_voice_name
            remote_selector = contribution.anchor.remote_selector
            use_remote_stop_offset = contribution.anchor.use_remote_stop_offset
            anchored = True
        else:
            remote_voice_name = None
            remote_selector = None
            use_remote_stop_offset = None
        if not anchored:
            return self._current_offset
        if anchored and remote_voice_name is None:
            return self._score_stop_offset
        if remote_selector is None:

            def remote_selector(argument):
                return abjad.select.leaf(argument, 0)

        floating_selections = self._floating_selections[remote_voice_name]
        selections = [_.annotation for _ in floating_selections]
        result = remote_selector(selections)
        selected_leaves = list(abjad.iterate.leaves(result))
        first_selected_leaf = selected_leaves[0]
        timespan = self._get_leaf_timespan(first_selected_leaf, floating_selections)
        if use_remote_stop_offset:
            remote_anchor_offset = timespan.stop_offset
        else:
            remote_anchor_offset = timespan.start_offset
        local_anchor_offset = abjad.Offset(0)
        if contribution.anchor is not None:
            local_selector = contribution.anchor.local_selector
        else:
            local_selector = None
        if local_selector is not None:
            result = local_selector(selection)
            selected_leaves = list(abjad.iterate.leaves(result))
            first_selected_leaf = selected_leaves[0]
            dummy_container = abjad.Container(selection)
            timespan = abjad.get.timespan(first_selected_leaf)
            del dummy_container[:]
            local_anchor_offset = timespan.start_offset
        start_offset = remote_anchor_offset - local_anchor_offset
        return start_offset

    def _label_figure(self, container, figure_name, figure_label_direction):
        figure_number = self._figure_number
        parts = figure_name.split("_")
        if len(parts) == 1:
            body = parts[0]
            figure_label_string = f'"{body}"'
        elif len(parts) == 2:
            body, subscript = parts
            figure_label_string = rf'\concat {{ "{body}" \sub {subscript} }}'
        else:
            raise Exception(f"unrecognized figure name: {figure_name!r}.")
        string = r"\markup"
        string += rf" \concat {{ [ \raise #0.25 \fontsize #-2 ({figure_number})"
        if figure_name:
            string += rf" \hspace #1 {figure_label_string} ] }}"
        else:
            string += r" ] }"
        figure_label_markup = abjad.Markup(string)
        bundle = abjad.bundle(figure_label_markup, r"- \tweak color #blue")
        pleaves = _select.pleaves(container)
        if pleaves:
            leaf = pleaves[0]
        else:
            leaf = abjad.select.leaf(container, 0)
        abjad.attach(
            bundle,
            leaf,
            deactivate=True,
            direction=figure_label_direction,
            tag=_tags.FIGURE_LABEL,
        )

    def _make_voice_dictionary(self):
        return dict([(_, []) for _ in self._voice_names])

    def assemble(self, voice_name) -> list | None:
        floating_selections = self._floating_selections[voice_name]
        total_duration = sum([_.duration for _ in self.time_signatures])
        for floating_selection in floating_selections:
            assert isinstance(floating_selection, abjad.Timespan)
        floating_selections = list(floating_selections)
        floating_selections.sort()
        try:
            first_start_offset = floating_selections[0].start_offset
        except Exception:
            first_start_offset = abjad.Offset(0)
        timespans = abjad.TimespanList(floating_selections)
        if timespans:
            gaps = ~timespans
        else:
            sectionwide_gap = abjad.Timespan(0, total_duration)
            gaps = abjad.TimespanList([sectionwide_gap])
        if 0 < first_start_offset:
            first_gap = abjad.Timespan(0, first_start_offset)
            gaps.append(first_gap)
        if floating_selections:
            final_stop_offset = floating_selections[-1].stop_offset
        else:
            final_stop_offset = total_duration
        if final_stop_offset < total_duration:
            final_gap = abjad.Timespan(final_stop_offset, total_duration)
            gaps.append(final_gap)
        selections = floating_selections + list(gaps)
        selections.sort()
        fused_selection = []
        for selection in selections:
            if (
                isinstance(selection, abjad.Timespan)
                and selection.annotation is not None
            ):
                fused_selection.extend(selection.annotation)
            else:
                assert isinstance(selection, abjad.Timespan)
                skip = abjad.Skip(1, multiplier=selection.duration)
                fused_selection.append(skip)
        return fused_selection

    def populate_commands(self, score, commands):
        for voice_name in sorted(self._floating_selections):
            selection = self.assemble(voice_name)
            if not selection:
                continue
            voice = score[voice_name]
            voice.extend(selection)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Contribution:

    voice_to_selection: dict[str, list]
    anchor: Anchor | None = None
    figure_name: str | None = None
    hide_time_signature: bool | None = None
    time_signature: abjad.TimeSignature | None = None

    def __post_init__(self):
        assert isinstance(self.voice_to_selection, dict), repr(self.voice_to_selection)
        if self.anchor is not None:
            assert isinstance(self.anchor, Anchor), repr(self.anchor)
        if self.figure_name is not None:
            assert isinstance(self.figure_name, str), repr(self.figure_name)
        if self.hide_time_signature is not None:
            assert isinstance(self.hide_time_signature, bool), repr(
                self.hide_time_signature
            )
        if self.time_signature is not None:
            assert isinstance(self.time_signature, abjad.TimeSignature)
        if self.voice_to_selection is not None:
            assert isinstance(self.voice_to_selection, dict), repr(
                self.voice_to_selection
            )
            for value in self.voice_to_selection.values():
                assert isinstance(value, list), repr(value)

    def __getitem__(self, voice_name) -> list:
        """
        Gets ``voice_name`` selection list.
        """
        return self.voice_to_selection.__getitem__(voice_name)

    def __iter__(self) -> typing.Iterator[str]:
        """
        Iterates figure contribution.
        """
        for voice_name in self.voice_to_selection:
            yield voice_name


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Nest:
    r"""
    Nest.

    ..  container:: example

        Augments one sixteenth:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam_groups(),
        ...     baca.nest("+1/16"),
        ... )

        >>> collections = [
        ...     [0, 2, 10, 18],
        ...     [16, 15, 23],
        ...     [19, 13, 9, 8],
        ... ]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 12/11
                    {
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            \time 3/4
                            c'16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            d'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            bf'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            fs''16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            e''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            ef''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            b''16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            g''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            cs''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            a'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 0
                            af'16
                            ]
                        }
                    }
                }
            >>

    ..  container:: example

        With rest affixes:

        >>> affix = baca.rests_around([2], [3])
        >>> stack = baca.stack(
        ...     baca.figure([1], 16, affix=affix),
        ...     rmakers.beam_groups(),
        ...     baca.nest("+1/16"),
        ... )

        >>> collections = [
        ...     [0, 2, 10, 18],
        ...     [16, 15, 23],
        ...     [19, 13, 9, 8],
        ... ]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 17/16
                    {
                        \scaleDurations #'(1 . 1)
                        {
                            \time 17/16
                            r8
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            c'16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            d'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            bf'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            fs''16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            e''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            ef''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            b''16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            g''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            cs''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            a'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 0
                            af'16
                            ]
                            r8.
                        }
                    }
                }
            >>

    """

    treatments: typing.Sequence[int | str]
    lmr: LMR | None = None

    def __post_init__(self):
        assert isinstance(self.treatments, list | tuple)
        for treatment in self.treatments:
            assert _is_treatment(treatment), repr(treatment)
        if self.lmr is not None:
            assert isinstance(self.lmr, LMR), repr(self.lmr)

    def __call__(self, selection) -> list[abjad.Tuplet]:
        treatments = self._get_treatments()
        assert treatments is not None
        tuplets = []
        for item in selection:
            if isinstance(item, abjad.Tuplet):
                tuplets.append(item)
            else:
                assert isinstance(item, list), repr(item)
                assert len(item) == 1, repr(item)
                assert isinstance(item[0], abjad.Tuplet), repr(item)
                tuplet = item[0]
                tuplets.append(tuplet)
        if self.lmr is None:
            tuplet_selections = [tuplets]
        else:
            tuplet_selections = self.lmr(tuplets)
            tuplet_selections = [list(_) for _ in tuplet_selections]
        tuplets = []
        for i, tuplet_selection in enumerate(tuplet_selections):
            assert isinstance(tuplet_selection, list)
            treatment = treatments[i]
            if treatment is None:
                tuplets.extend(tuplet_selection)
            else:
                assert isinstance(tuplet_selection, list)
                for tuplet in tuplet_selection:
                    assert isinstance(tuplet, abjad.Tuplet), repr(tuplet)
                if isinstance(treatment, str):
                    addendum = abjad.Duration(treatment)
                    contents_duration = abjad.get.duration(tuplet_selection)
                    target_duration = contents_duration + addendum
                    multiplier = target_duration / contents_duration
                    tuplet = abjad.Tuplet(multiplier, [])
                    abjad.mutate.wrap(tuplet_selection, tuplet)
                elif treatment.__class__ is abjad.Multiplier:
                    tuplet = abjad.Tuplet(treatment, [])
                    abjad.mutate.wrap(tuplet_selection, tuplet)
                elif treatment.__class__ is abjad.Duration:
                    target_duration = treatment
                    contents_duration = abjad.get.duration(tuplet_selection)
                    multiplier = target_duration / contents_duration
                    tuplet = abjad.Tuplet(multiplier, [])
                    abjad.mutate.wrap(tuplet_selection, tuplet)
                else:
                    raise Exception(f"bad time treatment: {treatment!r}.")
                nested_tuplet = tuplet
                tuplets.append(nested_tuplet)
        return tuplets

    def _get_treatments(self):
        if self.treatments:
            return abjad.CyclicTuple(self.treatments)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class RestAffix:
    r"""
    Rest affix.

    ..  container:: example

        Affixes rests to complete output when pattern is none:

        >>> affix = baca.RestAffix(
        ...     prefix=[1],
        ...     suffix=[2],
        ... )
        >>> stack = baca.stack(
        ...     baca.figure([1], 16, affix=affix, treatments=[1]),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 5/4
                    {
                        \time 15/16
                        r16
                        c'16
                        [
                        d'16
                        bf'16
                        ]
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/5
                    {
                        fs''16
                        [
                        e''16
                        ef''16
                        af''16
                        g''16
                        ]
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 4/3
                    {
                        a'16
                        r8
                    }
                }
            >>

    ..  container:: example

        Affixes rest to complete output when pattern is none:

        >>> affix = baca.RestAffix(
        ...     prefix=[1],
        ...     suffix=[2],
        ... )
        >>> stack = baca.stack(
        ...     baca.figure([1], 16, affix=affix, treatments=[1]),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[18, 16, 15, 20, 19]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/8
                    {
                        \time 9/16
                        r16
                        fs''16
                        [
                        e''16
                        ef''16
                        af''16
                        g''16
                        ]
                        r8
                    }
                }
            >>

    ..  container:: example

        Affixes rests to first and last collections only:

        >>> affix = baca.RestAffix(
        ...     pattern=abjad.Pattern(indices=[0, -1]),
        ...     prefix=[1],
        ...     suffix=[2],
        ... )
        >>> stack = baca.stack(
        ...     baca.figure([1], 16, affix=affix, treatments=[1]),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/6
                    {
                        \time 9/8
                        r16
                        c'16
                        [
                        d'16
                        bf'16
                        ]
                        r8
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/5
                    {
                        fs''16
                        [
                        e''16
                        ef''16
                        af''16
                        g''16
                        ]
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 5/4
                    {
                        r16
                        a'16
                        r8
                    }
                }
            >>

    ..  container:: example

        Affixes rests to every collection:

        >>> affix = baca.RestAffix(
        ...     pattern=abjad.index_all(),
        ...     prefix=[1],
        ...     suffix=[2],
        ... )
        >>> stack = baca.stack(
        ...     baca.figure([1], 16, affix=affix, treatments=[1]),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/6
                    {
                        \time 21/16
                        r16
                        c'16
                        [
                        d'16
                        bf'16
                        ]
                        r8
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/8
                    {
                        r16
                        fs''16
                        [
                        e''16
                        ef''16
                        af''16
                        g''16
                        ]
                        r8
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 5/4
                    {
                        r16
                        a'16
                        r8
                    }
                }
            >>

    ..  container:: example

        >>> affix = baca.RestAffix(prefix=[3])
        >>> stack = baca.stack(
        ...     baca.figure([1], 16, affix=affix),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/4
                        r8.
                        c'16
                        [
                        d'16
                        bf'16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        fs''16
                        [
                        e''16
                        ef''16
                        af''16
                        g''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'16
                    }
                }
            >>

    ..  container:: example

        >>> affix = baca.RestAffix(suffix=[3])
        >>> stack = baca.stack(
        ...     baca.figure([1], 16, affix=affix),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/4
                        c'16
                        [
                        d'16
                        bf'16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        fs''16
                        [
                        e''16
                        ef''16
                        af''16
                        g''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'16
                        r8.
                    }
                }
            >>

    """

    pattern: abjad.Pattern | None = None
    prefix: typing.Sequence[int] = ()
    skips_instead_of_rests: bool = False
    suffix: typing.Sequence[int] = ()

    def __post_init__(self):
        if self.pattern is not None:
            assert isinstance(self.pattern, abjad.Pattern)
        if self.prefix is not None:
            assert all(isinstance(_, int) for _ in self.prefix)
        assert isinstance(self.skips_instead_of_rests, bool), repr(
            self.skips_instead_of_rests
        )
        if self.suffix is not None:
            assert all(isinstance(_, int) for _ in self.suffix)

    def __call__(
        self, collection_index: int, total_collections: int
    ) -> tuple[typing.Sequence[int] | None, typing.Sequence[int] | None]:
        if self.pattern is None:
            if collection_index == 0 and collection_index == total_collections - 1:
                return self.prefix, self.suffix
            if collection_index == 0:
                return self.prefix, None
            if collection_index == total_collections - 1:
                return None, self.suffix
        elif self.pattern.matches_index(collection_index, total_collections):
            return self.prefix, self.suffix
        return None, None


def _add_rest_affixes(
    leaves,
    talea,
    rest_prefix,
    rest_suffix,
    affix_skips_instead_of_rests,
    increase_monotonic,
):
    if rest_prefix:
        durations = [(_, talea.denominator) for _ in rest_prefix]
        maker = abjad.LeafMaker(
            increase_monotonic=increase_monotonic,
            skips_instead_of_rests=affix_skips_instead_of_rests,
        )
        leaves_ = maker([None], durations)
        leaves[0:0] = leaves_
    if rest_suffix:
        durations = [(_, talea.denominator) for _ in rest_suffix]
        maker = abjad.LeafMaker(
            increase_monotonic=increase_monotonic,
            skips_instead_of_rests=affix_skips_instead_of_rests,
        )
        leaves_ = maker([None], durations)
        leaves.extend(leaves_)
    return leaves


def _coerce_collections(collections):
    prototype = (
        abjad.PitchClassSegment,
        abjad.PitchSegment,
        set,
        frozenset,
    )
    if isinstance(collections, prototype):
        return [collections]
    return collections


def _fix_rounding_error(durations, total_duration):
    current_duration = sum(durations)
    if current_duration < total_duration:
        missing_duration = total_duration - current_duration
        if durations[0] < durations[-1]:
            durations[-1] += missing_duration
        else:
            durations[0] += missing_duration
    elif sum(durations) == total_duration:
        return durations
    elif total_duration < current_duration:
        extra_duration = current_duration - total_duration
        if durations[0] < durations[-1]:
            durations[-1] -= extra_duration
        else:
            durations[0] -= extra_duration
    assert sum(durations) == total_duration
    return durations


def _is_treatment(argument):
    if argument is None:
        return True
    elif isinstance(argument, int):
        return True
    elif isinstance(argument, str):
        return True
    elif isinstance(argument, tuple) and len(argument) == 2:
        return True
    elif isinstance(argument, abjad.Ratio):
        return True
    elif isinstance(argument, abjad.Multiplier):
        return True
    elif argument.__class__ is abjad.Duration:
        return True
    elif argument in ("accel", "rit"):
        return True
    return False


def _make_tuplet_with_extra_count(leaf_selection, extra_count, denominator):
    contents_duration = abjad.get.duration(leaf_selection)
    contents_duration = contents_duration.with_denominator(denominator)
    contents_count = contents_duration.numerator
    if 0 < extra_count:
        extra_count %= contents_count
    elif extra_count < 0:
        extra_count = abs(extra_count)
        extra_count %= python_math.ceil(contents_count / 2.0)
        extra_count *= -1
    new_contents_count = contents_count + extra_count
    tuplet_multiplier = abjad.Multiplier(new_contents_count, contents_count)
    if not tuplet_multiplier.normalized():
        message = f"{leaf_selection!r} gives {tuplet_multiplier}"
        message += " with {contents_count} and {new_contents_count}."
        raise Exception(message)
    tuplet = abjad.Tuplet(tuplet_multiplier, leaf_selection)
    return tuplet


@dataclasses.dataclass(slots=True)
class FigureMaker:
    r"""
    Figure-maker.

    ..  container:: example

        Without state manifest:

        >>> stack = baca.stack(
        ...     baca.figure([1, 1, 2], 16),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/4
                        c'16
                        [
                        d'16
                        bf'8
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        fs''16
                        [
                        e''16
                        ef''8
                        af''16
                        g''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'8
                    }
                }
            >>

    ..  container:: example

        With state manifest:

        >>> stack = baca.stack(
        ...     baca.figure([1, 1, 2], 16),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> state = {"_next_attack": 2}
        >>> selections = stack(collections, state=state)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/4
                        c'8
                        [
                        d'16
                        bf'16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        fs''8
                        [
                        e''16
                        ef''16
                        af''8
                        g''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'16
                    }
                }
            >>

    ..  container:: example

        As many acciaccaturas as possible per collection:

        >>> stack = baca.stack(
        ...     baca.figure([1], 8, acciaccatura=True),
        ...     rmakers.beam(),
        ... )

        >>> collections = [
        ...     [0],
        ...     [2, 10],
        ...     [18, 16, 15],
        ...     [20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     [20, 19, 9, 0, 2, 10],
        ... ]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/4
                        c'8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            d'16
                        }
                        bf'8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            fs''16
                            [
                            e''16
                            ]
                        }
                        ef''8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            af''16
                            [
                            g''16
                            a'16
                            ]
                        }
                        c'8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            d'16
                            [
                            bf'16
                            fs''16
                            e''16
                            ]
                        }
                        ef''8
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            af''16
                            [
                            g''16
                            a'16
                            c'16
                            d'16
                            ]
                        }
                        bf'8
                    }
                }
            >>

    ..  container:: example

        Graced quarters:

        >>> stack = baca.stack(
        ...     baca.figure([1], 4, acciaccatura=True),
        ...     rmakers.beam(),
        ... )

        >>> collections = [
        ...     [0],
        ...     [2, 10],
        ...     [18, 16, 15],
        ...     [20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     [20, 19, 9, 0, 2, 10],
        ... ]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/2
                        c'4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            d'16
                        }
                        bf'4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            fs''16
                            [
                            e''16
                            ]
                        }
                        ef''4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            af''16
                            [
                            g''16
                            a'16
                            ]
                        }
                        c'4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            d'16
                            [
                            bf'16
                            fs''16
                            e''16
                            ]
                        }
                        ef''4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \acciaccatura {
                            af''16
                            [
                            g''16
                            a'16
                            c'16
                            d'16
                            ]
                        }
                        bf'4
                    }
                }
            >>

    ..  container:: example

        Spells nonassignable durations with monontonically decreasing durations by
        default:

        >>> stack = baca.stack(
        ...     baca.figure([4, 4, 5], 32),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 39/32
                        c'8
                        [
                        d'8
                        bf'8
                        ~
                        bf'32
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        fs''8
                        [
                        e''8
                        ef''8
                        ~
                        ef''32
                        af''8
                        g''8
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'8
                        [
                        ~
                        a'32
                        ]
                    }
                }
            >>

    ..  container:: example

        Spells nonassignable durations with monontonically increasing durations:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [4, 4, 5],
        ...         32,
        ...         spelling=rmakers.Spelling(increase_monotonic=True),
        ...     ),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 39/32
                        c'8
                        [
                        d'8
                        bf'32
                        ~
                        bf'8
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        fs''8
                        [
                        e''8
                        ef''32
                        ~
                        ef''8
                        af''8
                        g''8
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'32
                        [
                        ~
                        a'8
                        ]
                    }
                }
            >>

    ..  container:: example

        Sixteenths and eighths:

        >>> stack = baca.stack(
        ...     baca.figure([1, 1, 2], 16),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10, 8]]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 5/16
                        c'16
                        [
                        d'16
                        bf'8
                        af'16
                        ]
                    }
                }
            >>

        >>> collections = [[18, 16, 15, 20, 19]]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/8
                        fs''16
                        [
                        e''16
                        ef''8
                        af''16
                        g''16
                        ]
                    }
                }
            >>

        >>> collections = [[9]]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 1/16
                        a'16
                    }
                }
            >>

        >>> collections = [[0, 2, 10, 8], [18, 16, 15, 20, 19], [9]]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 13/16
                        c'16
                        [
                        d'16
                        bf'8
                        af'16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        fs''16
                        [
                        e''8
                        ef''16
                        af''16
                        g''8
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'16
                    }
                }
            >>

    ..  container:: example

        Works with rests:

        >>> stack = baca.stack(
        ...     baca.figure([3, -1, 2, 2], 16),
        ...     rmakers.beam(
        ...         beam_rests=True,
        ...         stemlet_length=1.5,
        ...     ),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \override Staff.Stem.stemlet-length = 1.5
                        \time 3/2
                        c'8.
                        [
                        r16
                        d'8
                        \revert Staff.Stem.stemlet-length
                        bf'8
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \override Staff.Stem.stemlet-length = 1.5
                        fs''8.
                        [
                        r16
                        e''8
                        ef''8
                        af''8.
                        r16
                        \revert Staff.Stem.stemlet-length
                        g''8
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'8
                    }
                }
            >>

    ..  container:: example

        Works with large counts:

        >>> stack = baca.stack(
        ...     baca.figure([29], 64),
        ...     rmakers.beam(),
        ...     rmakers.force_repeat_tie(),
        ... )

        >>> collections = [[0, 2]]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 29/32
                        c'4..
                        c'64
                        \repeatTie
                        d'4..
                        d'64
                        \repeatTie
                    }
                }
            >>

    ..  container:: example

        One extra count per division:

        >>> stack = baca.stack(
        ...     baca.figure([1, 1, 2], 16, treatments=[1]),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 5/4
                    {
                        \time 15/16
                        c'16
                        [
                        d'16
                        bf'8
                        ]
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/6
                    {
                        fs''16
                        [
                        e''16
                        ef''8
                        af''16
                        g''16
                        ]
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/2
                    {
                        a'8
                    }
                }
            >>

    ..  container:: example

        One missing count per division:

        >>> stack = baca.stack(
        ...     baca.figure([1, 1, 2], 16, treatments=[-1]),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/4
                    {
                        \time 5/8
                        c'16
                        [
                        d'16
                        bf'8
                        ]
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 5/6
                    {
                        fs''16
                        [
                        e''16
                        ef''8
                        af''16
                        g''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'8
                    }
                }
            >>

    ..  container:: example

        Accelerandi:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16, treatments=["accel"]),
        ...     rmakers.beam(),
        ... )

        >>> collections = [
        ...     [0],
        ...     [2, 10],
        ...     [18, 16, 15],
        ...     [20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     [20, 19, 9, 0, 2, 10],
        ... ]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 21/16
                        c'16
                    }
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                        {
                            \context Score = "Score"
                            \with
                            {
                                \override SpacingSpanner.spacing-increment = 0.5
                                proportionalNotationDuration = ##f
                            }
                            <<
                                \context RhythmicStaff = "Rhythmic_Staff"
                                \with
                                {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = 5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.minimum-length = 4
                                    \override TupletBracket.padding = 1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                    \override TupletNumber.font-size = 0
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                }
                                {
                                    c'8
                                }
                            >>
                            \layout
                            {
                                indent = 0
                                ragged-right = ##t
                            }
                        }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Beam.grow-direction = #right
                        d'16 * 1328/1024
                        [
                        bf'16 * 720/1024
                        ]
                    }
                    \revert TupletNumber.text
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                        {
                            \context Score = "Score"
                            \with
                            {
                                \override SpacingSpanner.spacing-increment = 0.5
                                proportionalNotationDuration = ##f
                            }
                            <<
                                \context RhythmicStaff = "Rhythmic_Staff"
                                \with
                                {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = 5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.minimum-length = 4
                                    \override TupletBracket.padding = 1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                    \override TupletNumber.font-size = 0
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                }
                                {
                                    c'8.
                                }
                            >>
                            \layout
                            {
                                indent = 0
                                ragged-right = ##t
                            }
                        }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Beam.grow-direction = #right
                        fs''16 * 1552/1024
                        [
                        e''16 * 832/1024
                        ef''16 * 688/1024
                        ]
                    }
                    \revert TupletNumber.text
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                        {
                            \context Score = "Score"
                            \with
                            {
                                \override SpacingSpanner.spacing-increment = 0.5
                                proportionalNotationDuration = ##f
                            }
                            <<
                                \context RhythmicStaff = "Rhythmic_Staff"
                                \with
                                {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = 5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.minimum-length = 4
                                    \override TupletBracket.padding = 1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                    \override TupletNumber.font-size = 0
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                }
                                {
                                    c'4
                                }
                            >>
                            \layout
                            {
                                indent = 0
                                ragged-right = ##t
                            }
                        }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Beam.grow-direction = #right
                        af''16 * 1728/1024
                        [
                        g''16 * 928/1024
                        a'16 * 768/1024
                        c'16 * 672/1024
                        ]
                    }
                    \revert TupletNumber.text
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                        {
                            \context Score = "Score"
                            \with
                            {
                                \override SpacingSpanner.spacing-increment = 0.5
                                proportionalNotationDuration = ##f
                            }
                            <<
                                \context RhythmicStaff = "Rhythmic_Staff"
                                \with
                                {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = 5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.minimum-length = 4
                                    \override TupletBracket.padding = 1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                    \override TupletNumber.font-size = 0
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                }
                                {
                                    c'4
                                    ~
                                    c'16
                                }
                            >>
                            \layout
                            {
                                indent = 0
                                ragged-right = ##t
                            }
                        }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Beam.grow-direction = #right
                        d'16 * 1872/1024
                        [
                        bf'16 * 1008/1024
                        fs''16 * 832/1024
                        e''16 * 736/1024
                        ef''16 * 672/1024
                        ]
                    }
                    \revert TupletNumber.text
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                        {
                            \context Score = "Score"
                            \with
                            {
                                \override SpacingSpanner.spacing-increment = 0.5
                                proportionalNotationDuration = ##f
                            }
                            <<
                                \context RhythmicStaff = "Rhythmic_Staff"
                                \with
                                {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = 5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.minimum-length = 4
                                    \override TupletBracket.padding = 1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                    \override TupletNumber.font-size = 0
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                }
                                {
                                    c'4.
                                }
                            >>
                            \layout
                            {
                                indent = 0
                                ragged-right = ##t
                            }
                        }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Beam.grow-direction = #right
                        af''16 * 2000/1024
                        [
                        g''16 * 1088/1024
                        a'16 * 896/1024
                        c'16 * 784/1024
                        d'16 * 720/1024
                        bf'16 * 656/1024
                        ]
                    }
                    \revert TupletNumber.text
                }
            >>

    ..  container:: example

        Ritardandi:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16, treatments=["rit"]),
        ...     rmakers.beam(),
        ... )

        >>> collections = [
        ...     [0],
        ...     [2, 10],
        ...     [18, 16, 15],
        ...     [20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     [20, 19, 9, 0, 2, 10],
        ... ]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 21/16
                        c'16
                    }
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                        {
                            \context Score = "Score"
                            \with
                            {
                                \override SpacingSpanner.spacing-increment = 0.5
                                proportionalNotationDuration = ##f
                            }
                            <<
                                \context RhythmicStaff = "Rhythmic_Staff"
                                \with
                                {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = 5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.minimum-length = 4
                                    \override TupletBracket.padding = 1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                    \override TupletNumber.font-size = 0
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                }
                                {
                                    c'8
                                }
                            >>
                            \layout
                            {
                                indent = 0
                                ragged-right = ##t
                            }
                        }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Beam.grow-direction = #left
                        d'16 * 656/1024
                        [
                        bf'16 * 1392/1024
                        ]
                    }
                    \revert TupletNumber.text
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                        {
                            \context Score = "Score"
                            \with
                            {
                                \override SpacingSpanner.spacing-increment = 0.5
                                proportionalNotationDuration = ##f
                            }
                            <<
                                \context RhythmicStaff = "Rhythmic_Staff"
                                \with
                                {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = 5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.minimum-length = 4
                                    \override TupletBracket.padding = 1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                    \override TupletNumber.font-size = 0
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                }
                                {
                                    c'8.
                                }
                            >>
                            \layout
                            {
                                indent = 0
                                ragged-right = ##t
                            }
                        }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Beam.grow-direction = #left
                        fs''16 * 512/1024
                        [
                        e''16 * 1072/1024
                        ef''16 * 1488/1024
                        ]
                    }
                    \revert TupletNumber.text
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                        {
                            \context Score = "Score"
                            \with
                            {
                                \override SpacingSpanner.spacing-increment = 0.5
                                proportionalNotationDuration = ##f
                            }
                            <<
                                \context RhythmicStaff = "Rhythmic_Staff"
                                \with
                                {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = 5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.minimum-length = 4
                                    \override TupletBracket.padding = 1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                    \override TupletNumber.font-size = 0
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                }
                                {
                                    c'4
                                }
                            >>
                            \layout
                            {
                                indent = 0
                                ragged-right = ##t
                            }
                        }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Beam.grow-direction = #left
                        af''16 * 432/1024
                        [
                        g''16 * 896/1024
                        a'16 * 1232/1024
                        c'16 * 1536/1024
                        ]
                    }
                    \revert TupletNumber.text
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                        {
                            \context Score = "Score"
                            \with
                            {
                                \override SpacingSpanner.spacing-increment = 0.5
                                proportionalNotationDuration = ##f
                            }
                            <<
                                \context RhythmicStaff = "Rhythmic_Staff"
                                \with
                                {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = 5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.minimum-length = 4
                                    \override TupletBracket.padding = 1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                    \override TupletNumber.font-size = 0
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                }
                                {
                                    c'4
                                    ~
                                    c'16
                                }
                            >>
                            \layout
                            {
                                indent = 0
                                ragged-right = ##t
                            }
                        }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Beam.grow-direction = #left
                        d'16 * 368/1024
                        [
                        bf'16 * 784/1024
                        fs''16 * 1072/1024
                        e''16 * 1328/1024
                        ef''16 * 1568/1024
                        ]
                    }
                    \revert TupletNumber.text
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                        {
                            \context Score = "Score"
                            \with
                            {
                                \override SpacingSpanner.spacing-increment = 0.5
                                proportionalNotationDuration = ##f
                            }
                            <<
                                \context RhythmicStaff = "Rhythmic_Staff"
                                \with
                                {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = 5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.minimum-length = 4
                                    \override TupletBracket.padding = 1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                    \override TupletNumber.font-size = 0
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                }
                                {
                                    c'4.
                                }
                            >>
                            \layout
                            {
                                indent = 0
                                ragged-right = ##t
                            }
                        }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Beam.grow-direction = #left
                        af''16 * 336/1024
                        [
                        g''16 * 704/1024
                        a'16 * 960/1024
                        c'16 * 1184/1024
                        d'16 * 1392/1024
                        bf'16 * 1568/1024
                        ]
                    }
                    \revert TupletNumber.text
                }
            >>

    ..  container:: example

        Accelerandi followed by ritardandi:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1], 16, treatments=["accel", "rit"]
        ...     ),
        ...     rmakers.beam(),
        ... )

        >>> collections = [
        ...     [0, 2, 10, 18, 16],
        ...     [15, 20, 19, 9, 0, 2],
        ...     [10, 18, 16, 15, 20],
        ...     [19, 9, 0, 2, 10, 18],
        ... ]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                        {
                            \context Score = "Score"
                            \with
                            {
                                \override SpacingSpanner.spacing-increment = 0.5
                                proportionalNotationDuration = ##f
                            }
                            <<
                                \context RhythmicStaff = "Rhythmic_Staff"
                                \with
                                {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = 5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.minimum-length = 4
                                    \override TupletBracket.padding = 1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                    \override TupletNumber.font-size = 0
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                }
                                {
                                    c'4
                                    ~
                                    c'16
                                }
                            >>
                            \layout
                            {
                                indent = 0
                                ragged-right = ##t
                            }
                        }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Beam.grow-direction = #right
                        \time 11/8
                        c'16 * 1872/1024
                        [
                        d'16 * 1008/1024
                        bf'16 * 832/1024
                        fs''16 * 736/1024
                        e''16 * 672/1024
                        ]
                    }
                    \revert TupletNumber.text
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                        {
                            \context Score = "Score"
                            \with
                            {
                                \override SpacingSpanner.spacing-increment = 0.5
                                proportionalNotationDuration = ##f
                            }
                            <<
                                \context RhythmicStaff = "Rhythmic_Staff"
                                \with
                                {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = 5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.minimum-length = 4
                                    \override TupletBracket.padding = 1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                    \override TupletNumber.font-size = 0
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                }
                                {
                                    c'4.
                                }
                            >>
                            \layout
                            {
                                indent = 0
                                ragged-right = ##t
                            }
                        }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Beam.grow-direction = #left
                        ef''16 * 336/1024
                        [
                        af''16 * 704/1024
                        g''16 * 960/1024
                        a'16 * 1184/1024
                        c'16 * 1392/1024
                        d'16 * 1568/1024
                        ]
                    }
                    \revert TupletNumber.text
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                        {
                            \context Score = "Score"
                            \with
                            {
                                \override SpacingSpanner.spacing-increment = 0.5
                                proportionalNotationDuration = ##f
                            }
                            <<
                                \context RhythmicStaff = "Rhythmic_Staff"
                                \with
                                {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = 5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.minimum-length = 4
                                    \override TupletBracket.padding = 1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                    \override TupletNumber.font-size = 0
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                }
                                {
                                    c'4
                                    ~
                                    c'16
                                }
                            >>
                            \layout
                            {
                                indent = 0
                                ragged-right = ##t
                            }
                        }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Beam.grow-direction = #right
                        bf'16 * 1872/1024
                        [
                        fs''16 * 1008/1024
                        e''16 * 832/1024
                        ef''16 * 736/1024
                        af''16 * 672/1024
                        ]
                    }
                    \revert TupletNumber.text
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                        {
                            \context Score = "Score"
                            \with
                            {
                                \override SpacingSpanner.spacing-increment = 0.5
                                proportionalNotationDuration = ##f
                            }
                            <<
                                \context RhythmicStaff = "Rhythmic_Staff"
                                \with
                                {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = 5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.minimum-length = 4
                                    \override TupletBracket.padding = 1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                    \override TupletNumber.font-size = 0
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                }
                                {
                                    c'4.
                                }
                            >>
                            \layout
                            {
                                indent = 0
                                ragged-right = ##t
                            }
                        }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Beam.grow-direction = #left
                        g''16 * 336/1024
                        [
                        a'16 * 704/1024
                        c'16 * 960/1024
                        d'16 * 1184/1024
                        bf'16 * 1392/1024
                        fs''16 * 1568/1024
                        ]
                    }
                    \revert TupletNumber.text
                }
            >>

    ..  container:: example

        Mixed accelerandi, ritardandi and prolation:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16, treatments=["accel", -2, "rit"]),
        ...     rmakers.beam(),
        ... )

        >>> collections = [
        ...     [0, 2, 10, 18, 16],
        ...     [15, 20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     [20, 19, 9, 0, 2],
        ...     [10, 18, 16, 15, 20],
        ...     [19, 9, 0, 2, 10],
        ... ]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                        {
                            \context Score = "Score"
                            \with
                            {
                                \override SpacingSpanner.spacing-increment = 0.5
                                proportionalNotationDuration = ##f
                            }
                            <<
                                \context RhythmicStaff = "Rhythmic_Staff"
                                \with
                                {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = 5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.minimum-length = 4
                                    \override TupletBracket.padding = 1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                    \override TupletNumber.font-size = 0
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                }
                                {
                                    c'4
                                    ~
                                    c'16
                                }
                            >>
                            \layout
                            {
                                indent = 0
                                ragged-right = ##t
                            }
                        }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Beam.grow-direction = #right
                        \time 13/8
                        c'16 * 1872/1024
                        [
                        d'16 * 1008/1024
                        bf'16 * 832/1024
                        fs''16 * 736/1024
                        e''16 * 672/1024
                        ]
                    }
                    \revert TupletNumber.text
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/5
                    {
                        ef''16
                        [
                        af''16
                        g''16
                        a'16
                        c'16
                        ]
                    }
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                        {
                            \context Score = "Score"
                            \with
                            {
                                \override SpacingSpanner.spacing-increment = 0.5
                                proportionalNotationDuration = ##f
                            }
                            <<
                                \context RhythmicStaff = "Rhythmic_Staff"
                                \with
                                {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = 5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.minimum-length = 4
                                    \override TupletBracket.padding = 1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                    \override TupletNumber.font-size = 0
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                }
                                {
                                    c'4
                                    ~
                                    c'16
                                }
                            >>
                            \layout
                            {
                                indent = 0
                                ragged-right = ##t
                            }
                        }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Beam.grow-direction = #left
                        d'16 * 368/1024
                        [
                        bf'16 * 784/1024
                        fs''16 * 1072/1024
                        e''16 * 1328/1024
                        ef''16 * 1568/1024
                        ]
                    }
                    \revert TupletNumber.text
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                        {
                            \context Score = "Score"
                            \with
                            {
                                \override SpacingSpanner.spacing-increment = 0.5
                                proportionalNotationDuration = ##f
                            }
                            <<
                                \context RhythmicStaff = "Rhythmic_Staff"
                                \with
                                {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = 5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.minimum-length = 4
                                    \override TupletBracket.padding = 1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                    \override TupletNumber.font-size = 0
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                }
                                {
                                    c'4
                                    ~
                                    c'16
                                }
                            >>
                            \layout
                            {
                                indent = 0
                                ragged-right = ##t
                            }
                        }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Beam.grow-direction = #right
                        af''16 * 1872/1024
                        [
                        g''16 * 1008/1024
                        a'16 * 832/1024
                        c'16 * 736/1024
                        d'16 * 672/1024
                        ]
                    }
                    \revert TupletNumber.text
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/5
                    {
                        bf'16
                        [
                        fs''16
                        e''16
                        ef''16
                        af''16
                        ]
                    }
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                        {
                            \context Score = "Score"
                            \with
                            {
                                \override SpacingSpanner.spacing-increment = 0.5
                                proportionalNotationDuration = ##f
                            }
                            <<
                                \context RhythmicStaff = "Rhythmic_Staff"
                                \with
                                {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = 5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.minimum-length = 4
                                    \override TupletBracket.padding = 1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                    \override TupletNumber.font-size = 0
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                }
                                {
                                    c'4
                                    ~
                                    c'16
                                }
                            >>
                            \layout
                            {
                                indent = 0
                                ragged-right = ##t
                            }
                        }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Beam.grow-direction = #left
                        g''16 * 368/1024
                        [
                        a'16 * 784/1024
                        c'16 * 1072/1024
                        d'16 * 1328/1024
                        bf'16 * 1568/1024
                        ]
                    }
                    \revert TupletNumber.text
                }
            >>

    ..  container:: example

        Specified by tuplet multiplier:

        >>> stack = baca.stack(
        ...     baca.figure([1], 8, treatments=["3:2"]),
        ...     rmakers.beam(),
        ... )

        >>> collections = [
        ...     [0],
        ...     [2, 10],
        ...     [18, 16, 15],
        ...     [20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     [20, 19, 9, 0, 2, 10],
        ... ]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.override(staff).Beam.positions = "#'(-6 . -6)"
        >>> abjad.override(staff).Stem.direction = abjad.DOWN
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                \with
                {
                    \override Beam.positions = #'(-6 . -6)
                    \override Stem.direction = #down
                }
                {
                    \tweak edge-height #'(0.7 . 0)
                    \times 2/3
                    {
                        \time 7/4
                        c'8
                    }
                    \tweak edge-height #'(0.7 . 0)
                    \times 2/3
                    {
                        d'8
                        [
                        bf'8
                        ]
                    }
                    \times 2/3
                    {
                        fs''8
                        [
                        e''8
                        ef''8
                        ]
                    }
                    \tweak edge-height #'(0.7 . 0)
                    \times 2/3
                    {
                        af''8
                        [
                        g''8
                        a'8
                        c'8
                        ]
                    }
                    \tweak edge-height #'(0.7 . 0)
                    \times 2/3
                    {
                        d'8
                        [
                        bf'8
                        fs''8
                        e''8
                        ef''8
                        ]
                    }
                    \times 2/3
                    {
                        af''8
                        [
                        g''8
                        a'8
                        c'8
                        d'8
                        bf'8
                        ]
                    }
                }
            >>

    ..  container:: example

        Segment durations equal to a quarter:

        >>> stack = baca.stack(
        ...     baca.figure([1], 8, treatments=[(1, 4)]),
        ...     rmakers.denominator((1, 16)),
        ...     rmakers.beam(),
        ... )

        >>> collections = [
        ...     [0],
        ...     [2, 10],
        ...     [18, 16, 15],
        ...     [20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     [20, 19, 9, 0, 2, 10],
        ... ]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.override(staff).Beam.positions = "#'(-6 . -6)"
        >>> abjad.override(staff).Stem.direction = abjad.DOWN
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                \with
                {
                    \override Beam.positions = #'(-6 . -6)
                    \override Stem.direction = #down
                }
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/2
                        c'4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        d'8
                        [
                        bf'8
                        ]
                    }
                    \times 4/6
                    {
                        fs''8
                        [
                        e''8
                        ef''8
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        af''16
                        [
                        g''16
                        a'16
                        c'16
                        ]
                    }
                    \times 4/5
                    {
                        d'16
                        [
                        bf'16
                        fs''16
                        e''16
                        ef''16
                        ]
                    }
                    \times 4/6
                    {
                        af''16
                        [
                        g''16
                        a'16
                        c'16
                        d'16
                        bf'16
                        ]
                    }
                }
            >>

    ..  container:: example

        Collection durations alternating between a quarter and a dotted quarter:

        >>> stack = baca.stack(
        ...     baca.figure([1, 1, 2], 8, treatments=[(1, 4), (3, 8)]),
        ...     rmakers.denominator((1, 16)),
        ...     rmakers.beam(),
        ... )

        >>> collections = [
        ...     [0, 2, 10, 18, 16],
        ...     [15, 20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     [20, 19, 9, 0, 2],
        ...     [10, 18, 16, 15, 20],
        ...     [19, 9, 0, 2, 10],
        ... ]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.override(staff).Beam.positions = "#'(-6 . -6)"
        >>> abjad.override(staff).Stem.direction = abjad.DOWN
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                \with
                {
                    \override Beam.positions = #'(-6 . -6)
                    \override Stem.direction = #down
                }
                {
                    \times 4/6
                    {
                        \time 15/8
                        c'16
                        [
                        d'16
                        bf'8
                        fs''16
                        e''16
                        ]
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7
                    {
                        ef''8
                        [
                        af''16
                        g''16
                        a'8
                        c'16
                        ]
                    }
                    \times 4/7
                    {
                        d'16
                        [
                        bf'8
                        fs''16
                        e''16
                        ef''8
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        af''16
                        [
                        g''16
                        a'8
                        c'16
                        d'16
                        ]
                    }
                    \times 4/7
                    {
                        bf'8
                        [
                        fs''16
                        e''16
                        ef''8
                        af''16
                        ]
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7
                    {
                        g''16
                        [
                        a'8
                        c'16
                        d'16
                        bf'8
                        ]
                    }
                }
            >>

        Time treatments defined equal to integers; positive multipliers; positive
        durations; and the strings ``'accel'`` and ``'rit'``.

    """

    talea: rmakers.Talea
    acciaccatura: Acciaccatura | None = None
    affix: RestAffix | None = None
    restart_talea: bool = False
    signature: int | None = None
    spelling: rmakers.Spelling | None = None
    treatments: typing.Sequence = ()
    _next_attack: int = dataclasses.field(default=0, init=False, repr=False)
    _next_segment: int = dataclasses.field(default=0, init=False, repr=False)
    _state: dict = dataclasses.field(default_factory=dict, init=False, repr=False)

    _state_variables = ("_next_attack", "_next_segment")

    def __post_init__(self):
        if self.acciaccatura is not None:
            assert isinstance(self.acciaccatura, Acciaccatura), repr(self.acciaccatura)
        if self.affix is not None:
            assert isinstance(self.affix, RestAffix), repr(self.affix)
        assert isinstance(self.restart_talea, bool), repr(self.restart_talea)
        if self.signature is not None:
            assert isinstance(self.signature, int), repr(self.signature)
        if self.spelling is not None:
            assert isinstance(self.spelling, rmakers.Spelling), repr(self.spelling)
        assert isinstance(self.talea, rmakers.Talea), repr(self.talea)
        if self.treatments is not None:
            self._check_treatments(self.treatments)

    def __call__(
        self,
        collections: typing.Sequence,
        collection_index: int = None,
        state: dict = None,
        total_collections: int = None,
    ) -> list[abjad.Tuplet]:
        collections = _coerce_collections(collections)
        self._state = state or {}
        self._apply_state(state=state)
        tuplets: list[abjad.Tuplet] = []
        if not self.restart_talea:
            selection_ = self._make_music(
                collections,
                collection_index=collection_index,
                total_collections=total_collections,
            )
            tuplets.extend(selection_)
        else:
            total_collections = len(collections)
            for i, collection in enumerate(collections):
                self._apply_state(state=None)
                selection_ = self._make_music(
                    [collection],
                    collection_index=i,
                    total_collections=total_collections,
                )
                tuplets.extend(selection_)
        assert all(isinstance(_, abjad.Tuplet) for _ in tuplets)
        return tuplets

    def _apply_state(self, state=None):
        for name in self._state_variables:
            value = setattr(self, name, 0)
        state = state or {}
        assert isinstance(state, dict), repr(state)
        for key in state:
            value = state[key]
            setattr(self, key, value)

    def _check_treatments(self, treatments):
        for treatment in treatments:
            if not _is_treatment(treatment):
                raise Exception(f"bad time treatment: {treatment!r}.")

    def _get_acciaccatura_specifier(self, collection_index, total_collections):
        if not self.acciaccatura:
            return
        pattern = self.acciaccatura._get_pattern()
        if pattern.matches_index(collection_index, total_collections):
            return self.acciaccatura

    def _get_spelling_specifier(self):
        if self.spelling is not None:
            return self.spelling
        return rmakers.Spelling()

    def _get_talea(self):
        if self.talea is not None:
            return self.talea
        return rmakers.Talea()

    def _get_treatments(self):
        if not self.treatments:
            return abjad.CyclicTuple([0])
        return abjad.CyclicTuple(self.treatments)

    @classmethod
    def _make_accelerando(class_, leaf_selection, accelerando_indicator):
        assert accelerando_indicator in ("accel", "rit")
        tuplet = abjad.Tuplet((1, 1), leaf_selection, hide=True)
        if len(tuplet) == 1:
            return tuplet
        durations = [abjad.get.duration(_) for _ in leaf_selection]
        if accelerando_indicator == "accel":
            exponent = 0.625
        elif accelerando_indicator == "rit":
            exponent = 1.625
        multipliers = class_._make_accelerando_multipliers(durations, exponent)
        assert len(leaf_selection) == len(multipliers)
        for multiplier, leaf in zip(multipliers, leaf_selection):
            leaf.multiplier = multiplier
        if rmakers.FeatherBeamCommand._is_accelerando(leaf_selection):
            abjad.override(leaf_selection[0]).Beam.grow_direction = abjad.RIGHT
        elif rmakers.FeatherBeamCommand._is_ritardando(leaf_selection):
            abjad.override(leaf_selection[0]).Beam.grow_direction = abjad.LEFT
        duration = abjad.get.duration(tuplet)
        notes = abjad.LeafMaker()([0], [duration])
        string = abjad.illustrators.selection_to_score_markup_string(notes)
        string = rf"\markup \scale #'(0.75 . 0.75) {string}"
        abjad.override(tuplet).TupletNumber.text = string
        return tuplet

    @classmethod
    def _make_accelerando_multipliers(class_, durations, exponent):
        r"""
        Makes accelerando multipliers.

        ..  container:: example

            Set exponent less than 1 for decreasing durations:

            >>> class_ = baca.FigureMaker
            >>> durations = 4 * [abjad.Duration(1)]
            >>> result = class_._make_accelerando_multipliers(durations, 0.5)
            >>> for multiplier in result: multiplier
            ...
            NonreducedFraction(2048, 1024)
            NonreducedFraction(848, 1024)
            NonreducedFraction(651, 1024)
            NonreducedFraction(549, 1024)

        ..  container:: example

            Set exponent to 1 for trivial multipliers:

            >>> class_ = baca.FigureMaker
            >>> durations = 4 * [abjad.Duration(1)]
            >>> result = class_._make_accelerando_multipliers(durations, 1)
            >>> for multiplier in result: multiplier
            ...
            NonreducedFraction(1024, 1024)
            NonreducedFraction(1024, 1024)
            NonreducedFraction(1024, 1024)
            NonreducedFraction(1024, 1024)

        ..  container:: example

            Set exponent greater than 1 for increasing durations:

            >>> class_ = baca.FigureMaker
            >>> durations = 4 * [abjad.Duration(1)]
            >>> result = class_._make_accelerando_multipliers(
            ...     durations,
            ...     0.5,
            ... )
            >>> for multiplier in result: multiplier
            ...
            NonreducedFraction(2048, 1024)
            NonreducedFraction(848, 1024)
            NonreducedFraction(651, 1024)
            NonreducedFraction(549, 1024)

        Set exponent greater than 1 for ritardando.

        Set exponent less than 1 for accelerando.
        """
        sums = abjad.math.cumulative_sums(durations)
        generator = abjad.sequence.nwise(sums, n=2)
        pairs = list(generator)
        total_duration = pairs[-1][-1]
        start_offsets = [_[0] for _ in pairs]
        start_offsets = [_ / total_duration for _ in start_offsets]
        start_offsets_ = []
        rhythm_maker_class = rmakers.AccelerandoRhythmMaker
        for start_offset in start_offsets:
            start_offset_ = rhythm_maker_class._interpolate_exponential(
                0, total_duration, start_offset, exponent
            )
            start_offsets_.append(start_offset_)
        start_offsets_.append(float(total_duration))
        durations_ = abjad.math.difference_series(start_offsets_)
        durations_ = rhythm_maker_class._round_durations(durations_, 2**10)
        durations_ = _fix_rounding_error(durations_, total_duration)
        multipliers = []
        assert len(durations) == len(durations_)
        for duration_, duration in zip(durations_, durations):
            multiplier = duration_ / duration
            multiplier = abjad.Multiplier(multiplier)
            multiplier = multiplier.with_denominator(2**10)
            multipliers.append(multiplier)
        return multipliers

    def _make_music(
        self, collections, collection_index=None, total_collections=None
    ) -> list[abjad.Tuplet]:
        segment_count = len(collections)
        tuplets = []
        if collection_index is None:
            for i, segment in enumerate(collections):
                if self.affix is not None:
                    result = self.affix(i, segment_count)
                    rest_prefix, rest_suffix = result
                    affix_skips_instead_of_rests = self.affix.skips_instead_of_rests
                else:
                    rest_prefix, rest_suffix = None, None
                    affix_skips_instead_of_rests = None
                tuplet = self._make_tuplet(
                    segment,
                    rest_prefix=rest_prefix,
                    rest_suffix=rest_suffix,
                    affix_skips_instead_of_rests=affix_skips_instead_of_rests,
                )
                tuplets.append(tuplet)
        else:
            assert len(collections) == 1, repr(collections)
            segment = collections[0]
            if self.affix is not None:
                result = self.affix(collection_index, total_collections)
                rest_prefix, rest_suffix = result
                affix_skips_instead_of_rests = self.affix.skips_instead_of_rests
            else:
                rest_prefix, rest_suffix = None, None
                affix_skips_instead_of_rests = None
            tuplet = self._make_tuplet(
                segment,
                rest_prefix=rest_prefix,
                rest_suffix=rest_suffix,
                affix_skips_instead_of_rests=affix_skips_instead_of_rests,
            )
            tuplets.append(tuplet)
        assert all(isinstance(_, abjad.Tuplet) for _ in tuplets)
        return tuplets

    def _make_tuplet(
        self,
        segment,
        rest_prefix=None,
        rest_suffix=None,
        affix_skips_instead_of_rests=None,
    ):
        self._next_segment += 1
        talea = self._get_talea()
        leaves = []
        spelling = self._get_spelling_specifier()
        current_selection = self._next_segment - 1
        treatment = self._get_treatments()[current_selection]
        if treatment is None:
            treatment = 0
        before_grace_containers = None
        if self.acciaccatura is not None:
            if isinstance(segment, set | frozenset):
                message = "decide how to model chords with acciaccatura."
                raise NotImplementedError(message)
            before_grace_containers, segment = self.acciaccatura(segment)
            assert len(before_grace_containers) == len(segment)
        if isinstance(segment, set | frozenset):
            segment = [segment]
        for pitch_expression in segment:
            is_chord = False
            if isinstance(pitch_expression, set | frozenset):
                is_chord = True
            prototype = abjad.NumberedPitchClass
            if isinstance(pitch_expression, prototype):
                pitch_expression = pitch_expression.number
            count = self._next_attack
            while talea[count] < 0:
                self._next_attack += 1
                duration = -talea[count]
                maker = abjad.LeafMaker(increase_monotonic=spelling.increase_monotonic)
                leaves_ = maker([None], [duration])
                leaves.extend(leaves_)
                count = self._next_attack
            self._next_attack += 1
            duration = talea[count]
            assert 0 < duration, repr(duration)
            skips_instead_of_rests = False
            if (
                isinstance(pitch_expression, tuple)
                and len(pitch_expression) == 2
                and pitch_expression[-1] in (None, "skip")
            ):
                multiplier = pitch_expression[0]
                duration = abjad.Duration(1, talea.denominator)
                duration *= multiplier
                if pitch_expression[-1] == "skip":
                    skips_instead_of_rests = True
                pitch_expression = None
            maker = abjad.LeafMaker(
                increase_monotonic=spelling.increase_monotonic,
                skips_instead_of_rests=skips_instead_of_rests,
            )
            if is_chord:
                leaves_ = maker([tuple(pitch_expression)], [duration])
            else:
                leaves_ = maker([pitch_expression], [duration])
            leaves.extend(leaves_)
            count = self._next_attack
            while talea[count] < 0 and not count % len(talea) == 0:
                self._next_attack += 1
                duration = -talea[count]
                maker = abjad.LeafMaker(increase_monotonic=spelling.increase_monotonic)
                leaves_ = maker([None], [duration])
                leaves.extend(leaves_)
                count = self._next_attack
        leaves = _add_rest_affixes(
            leaves,
            talea,
            rest_prefix,
            rest_suffix,
            affix_skips_instead_of_rests,
            spelling.increase_monotonic,
        )
        leaf_selection = list(leaves)
        if isinstance(treatment, int):
            tuplet = _make_tuplet_with_extra_count(
                leaf_selection, treatment, talea.denominator
            )
        elif treatment in ("accel", "rit"):
            tuplet = self._make_accelerando(leaf_selection, treatment)
        elif isinstance(treatment, abjad.Ratio):
            numerator, denominator = treatment.numbers
            multiplier = abjad.NonreducedFraction((denominator, numerator))
            tuplet = abjad.Tuplet(multiplier, leaf_selection)
        elif isinstance(treatment, str) and ":" in treatment:
            numerator, denominator = treatment.split(":")
            numerator, denominator = int(numerator), int(denominator)
            tuplet = abjad.Tuplet((denominator, numerator), leaf_selection)
        elif isinstance(treatment, abjad.Multiplier):
            tuplet = abjad.Tuplet(treatment, leaf_selection)
        elif treatment.__class__ is abjad.Duration:
            tuplet_duration = treatment
            contents_duration = abjad.get.duration(leaf_selection)
            multiplier = tuplet_duration / contents_duration
            tuplet = abjad.Tuplet(multiplier, leaf_selection)
            if not abjad.Multiplier(tuplet.multiplier).normalized():
                tuplet.normalize_multiplier()
        elif isinstance(treatment, tuple) and len(treatment) == 2:
            tuplet_duration = abjad.Duration(treatment)
            contents_duration = abjad.get.duration(leaf_selection)
            multiplier = tuplet_duration / contents_duration
            tuplet = abjad.Tuplet(multiplier, leaf_selection)
            if not abjad.Multiplier(tuplet.multiplier).normalized():
                tuplet.normalize_multiplier()
        else:
            raise Exception(f"bad time treatment: {treatment!r}.")
        assert isinstance(tuplet, abjad.Tuplet)
        tag = _tags.function_name(_frame(), self)
        if before_grace_containers is not None:
            logical_ties = abjad.iterate.logical_ties(tuplet)
            pairs = zip(before_grace_containers, logical_ties)
            for before_grace_container, logical_tie in pairs:
                if before_grace_container is None:
                    continue
                abjad.attach(before_grace_container, logical_tie.head, tag=tag)
        if tuplet.trivial():
            tuplet.hide = True
        assert isinstance(tuplet, abjad.Tuplet), repr(tuplet)
        return tuplet


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Assignment:
    """
    Assignment.
    """

    maker: FigureMaker
    pattern: abjad.Pattern | None = None

    def __post_init__(self):
        assert isinstance(self.maker, FigureMaker)
        if self.pattern is not None:
            assert isinstance(self.pattern, abjad.Pattern)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Bind:
    """
    Bind.
    """

    assignments: typing.Sequence[Assignment] = ()

    def __post_init__(self):
        for assignment in self.assignments:
            if not isinstance(assignment, Assignment):
                raise Exception("must be assignment:\n   {assignment!r}")

    def __call__(self, collections: typing.Sequence) -> list[abjad.Tuplet]:
        collection_count = len(collections)
        matches = []
        for i, collection in enumerate(collections):
            for assignment in self.assignments:
                if assignment.pattern is None or assignment.pattern.matches_index(
                    i, collection_count
                ):
                    match = rmakers.Match(assignment, collection)
                    matches.append(match)
                    break
            else:
                raise Exception(f"no maker match for collection {i}.")
        assert len(collections) == len(matches)
        groups = abjad.sequence.group_by(matches, lambda _: _.assignment.maker)
        tuplets: list[abjad.Tuplet] = []
        for group in groups:
            maker = group[0].assignment.maker
            collections_ = [match.payload for match in group]
            selection = maker(
                collections_,
                collection_index=None,
                state=None,
                total_collections=None,
            )
            tuplets.extend(selection)
        assert all(isinstance(_, abjad.Tuplet) for _ in tuplets)
        return tuplets


def anchor(
    remote_voice_name: str,
    remote_selector=None,
    local_selector=None,
) -> Anchor:
    """
    Anchors music in this figure (filtered by ``local_selector``) to start offset of
    ``remote_voice_name`` (filtered by ``remote_selector``).
    """
    return Anchor(
        local_selector=local_selector,
        remote_selector=remote_selector,
        remote_voice_name=remote_voice_name,
    )


def anchor_after(
    remote_voice_name: str,
    remote_selector=None,
    local_selector=None,
) -> Anchor:
    """
    Anchors music in this figure (filtered by ``local_selector``) to stop offset of
    ``remote_voice_name`` (filtered by ``remote_selector``).
    """
    return Anchor(
        local_selector=local_selector,
        remote_selector=remote_selector,
        remote_voice_name=remote_voice_name,
        use_remote_stop_offset=True,
    )


def anchor_to_figure(figure_name: str) -> Anchor:
    """
    Anchors music in this figure to start of ``figure_name``.
    """
    return Anchor(figure_name=figure_name)


def assign(maker: FigureMaker, pattern: abjad.Pattern = None) -> Assignment:
    """
    Makes assignment.
    """
    assert isinstance(maker, FigureMaker), repr(maker)
    return Assignment(maker, pattern=pattern)


def bind(assignments):
    """
    Makes bind.
    """
    assert isinstance(assignments, tuple | list)
    return Bind(assignments)


def coat(pitch: int | str | abjad.Pitch) -> Coat:
    r"""
    Coats ``pitch``.

    ..  container:: example

        Coats pitches:

        >>> score = baca.docs.make_empty_score(2)
        >>> figures = baca.FigureAccumulator(score)

        >>> figures(
        ...     "Music.2",
        ...     3 * [[0, 2, 10]],
        ...     baca.figure(
        ...         [1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.imbricate(
        ...         "Music.1",
        ...         [baca.coat(0), baca.coat(2), 10, 0, 2],
        ...         rmakers.beam_groups(),
        ...     ),
        ... )

        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=figures.time_signatures,
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 32)),
        ... )
        >>> figures.populate_commands(score, accumulator)

        >>> accumulator(
        ...     "Music.1",
        ...     baca.voice_one(selector=lambda _: abjad.select.leaf(_, 0)),
        ... )

        >>> accumulator(
        ...     "Music.2",
        ...     baca.voice_two(selector=lambda _: abjad.select.leaf(_, 0)),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #32
                        \time 3/4
                        s1 * 3/4
                    }
                    \context Voice = "Music.1"
                    {
                        {
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \times 4/5
                            {
                                \voiceOne
                                s8
                                s16
                                s16
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                bf'16
                                [
                            }
                            \times 2/3
                            {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                c'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                d'16
                                ]
                                s16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/7
                            {
                                s16
                                s16
                                s16
                                s4
                            }
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }
                    }
                    \context Voice = "Music.2"
                    {
                        {
                            \times 4/5
                            {
                                \voiceTwo
                                r8
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \times 2/3
                            {
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/7
                            {
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                                r4
                            }
                        }
                    }
                >>
            }

    ..  container:: example

        Skips wrapped pitches:

        >>> score = baca.docs.make_empty_score(2)
        >>> figures = baca.FigureAccumulator(score)

        >>> collections = [
        ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
        ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
        ... ]
        >>> segment = [
        ...     0,
        ...     baca.coat(10),
        ...     baca.coat(18),
        ...     10, 18,
        ... ]
        >>> figures(
        ...     "Music.2",
        ...     collections,
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.imbricate(
        ...         "Music.1",
        ...         segment,
        ...         baca.accent(selector=lambda _: baca.select.pheads(_)),
        ...         rmakers.beam_groups(beam_rests=True),
        ...     ),
        ... )

        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=figures.time_signatures,
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 32)),
        ... )
        >>> figures.populate_commands(score, accumulator)

        >>> accumulator(
        ...     "Music.1",
        ...     baca.voice_one(selector=lambda _: abjad.select.leaf(_, 0)),
        ... )

        >>> accumulator(
        ...     "Music.2",
        ...     baca.voice_two(selector=lambda _: abjad.select.leaf(_, 0)),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #32
                        \time 9/8
                        s1 * 9/8
                    }
                    \context Voice = "Music.1"
                    {
                        {
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \scaleDurations #'(1 . 1)
                            {
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                \voiceOne
                                c'16
                                - \accent
                                [
                                s16
                                s16
                                s16
                                s16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                s16
                                s16
                                s16
                                s16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                s16
                                s16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                - \accent
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16
                                - \accent
                                s16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                s16
                                s16
                                s16
                                s16
                                ]
                            }
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }
                    }
                    \context Voice = "Music.2"
                    {
                        {
                            \scaleDurations #'(1 . 1)
                            {
                                \voiceTwo
                                c'16
                                [
                                d'16
                                bf'16
                                fs''16
                                e''16
                                ]
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                ef''16
                                [
                                af''16
                                g''16
                                a'16
                                ]
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                c'16
                                [
                                d'16
                                bf'16
                                fs''16
                                e''16
                                ]
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                ef''16
                                [
                                af''16
                                g''16
                                a'16
                                ]
                            }
                        }
                    }
                >>
            }

    """
    return Coat(pitch)


def extend_beam(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    r"""
    Attaches RIGHT_BROKEN_BEAM to selector output.

    ..  container:: example

        Extends beam:

        >>> score = baca.docs.make_empty_score(2)
        >>> figures = baca.FigureAccumulator(score)

        >>> figures(
        ...     "Music.2",
        ...     [[0, 2, 10, 18], [16, 15, 23]],
        ...     baca.figure([1], 16),
        ...     rmakers.beam_groups(),
        ...     baca.imbricate(
        ...         "Music.1",
        ...         [2, 10],
        ...         baca.staccato(selector=lambda _: baca.select.pheads(_)),
        ...         rmakers.beam_groups(beam_rests=True),
        ...         baca.extend_beam(selector=lambda _: abjad.select.leaf(_, -1)),
        ...     ),
        ... )

        >>> figures(
        ...     "Music.2",
        ...     [[19, 13, 9, 8]],
        ...     baca.figure([1], 16),
        ...     rmakers.beam_groups(),
        ...     baca.imbricate(
        ...         "Music.1",
        ...         [13, 9],
        ...         baca.staccato(selector=lambda _: baca.select.pheads(_)),
        ...         rmakers.beam_groups(beam_rests=True),
        ...     ),
        ... )

        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=figures.time_signatures,
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 32)),
        ... )
        >>> figures.populate_commands(score, accumulator)

        >>> accumulator(
        ...     "Music.1",
        ...     baca.voice_one(selector=lambda _: abjad.select.leaf(_, 0)),
        ... )

        >>> accumulator(
        ...     "Music.2",
        ...     baca.voice_two(selector=lambda _: abjad.select.leaf(_, 0)),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #32
                        \time 7/16
                        s1 * 7/16
                        \baca-new-spacing-section #1 #32
                        \time 1/4
                        s1 * 1/4
                    }
                    \context Voice = "Music.1"
                    {
                        {
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \scaleDurations #'(1 . 1)
                            {
                                \voiceOne
                                s16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16
                                - \staccato
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                - \staccato
                                s16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                s16
                                s16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                s16
                            }
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }
                        {
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \scaleDurations #'(1 . 1)
                            {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                s16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                cs''16
                                - \staccato
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16
                                - \staccato
                                s16
                                ]
                            }
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }
                    }
                    \context Voice = "Music.2"
                    {
                        {
                            \scaleDurations #'(1 . 1)
                            {
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                \voiceTwo
                                c'16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                fs''16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                e''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                ef''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                b''16
                                ]
                            }
                        }
                        {
                            \scaleDurations #'(1 . 1)
                            {
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                g''16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                cs''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                af'16
                                ]
                            }
                        }
                    }
                >>
            }

    """
    return _commands.IndicatorCommand(
        indicators=[_enums.RIGHT_BROKEN_BEAM], selector=selector
    )


def imbricate(
    voice_name: str,
    segment: list,
    *specifiers: typing.Any,
    allow_unused_pitches: bool = False,
    by_pitch_class: bool = False,
    hocket: bool = False,
    selector=None,
    truncate_ties: bool = False,
):
    r"""
    Imbricates ``segment`` in voice with ``voice_name``.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(2)
        >>> figures = baca.FigureAccumulator(score)

        >>> collections = [
        ...     [0, 2, 10, 18, 16],
        ...     [15, 20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ... ]
        >>> figures(
        ...     "Music.2",
        ...     collections,
        ...     baca.figure([1], 16),
        ...     rmakers.beam_groups(),
        ...     baca.imbricate(
        ...         "Music.1",
        ...         [2, 19, 9, 18, 16],
        ...         rmakers.beam_groups(),
        ...     ),
        ... )

        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=figures.time_signatures,
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 32)),
        ... )
        >>> figures.populate_commands(score, accumulator)

        >>> accumulator(
        ...     "Music.1",
        ...     baca.voice_one(selector=lambda _: abjad.select.leaf(_, 0)),
        ... )

        >>> accumulator(
        ...     "Music.2",
        ...     baca.voice_two(selector=lambda _: abjad.select.leaf(_, 0)),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #32
                        \time 15/16
                        s1 * 15/16
                    }
                    \context Voice = "Music.1"
                    {
                        {
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \scaleDurations #'(1 . 1)
                            {
                                \voiceOne
                                s16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16
                                s16
                                s16
                                s16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                s16
                                s16
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                g''16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                a'16
                                ]
                                s16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                s16
                                s16
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                fs''16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                e''16
                                ]
                                s16
                            }
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }
                    }
                    \context Voice = "Music.2"
                    {
                        {
                            \scaleDurations #'(1 . 1)
                            {
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                \voiceTwo
                                c'16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                e''16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                ef''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                af''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                g''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                c'16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                d'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                e''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                ef''16
                                ]
                            }
                        }
                    }
                >>
            }

    ..  container:: example

        Multiple imbricated voices:

        >>> score = baca.docs.make_empty_score(3)
        >>> figures = baca.FigureAccumulator(score)

        >>> collections = [
        ...     [0, 2, 10, 18, 16],
        ...     [15, 20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ... ]
        >>> figures(
        ...     "Music.2",
        ...     collections,
        ...     baca.figure([1], 16),
        ...     baca.imbricate(
        ...         "Music.1",
        ...         [2, 19, 9],
        ...         rmakers.beam_groups(beam_rests=True),
        ...         baca.beam_positions(6),
        ...         baca.staccato(selector=lambda _: baca.select.pheads(_)),
        ...         ),
        ...     baca.imbricate(
        ...         "Music.3",
        ...         [16, 10, 18],
        ...         rmakers.beam_groups(beam_rests=True),
        ...         baca.beam_positions(8),
        ...         baca.accent(selector=lambda _: baca.select.pheads(_)),
        ...         ),
        ...     rmakers.beam_groups(),
        ... )

        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=figures.time_signatures,
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 32)),
        ... )
        >>> figures.populate_commands(score, accumulator)
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #32
                        \time 15/16
                        s1 * 15/16
                    }
                    \context Voice = "Music.1"
                    {
                        {
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \scaleDurations #'(1 . 1)
                            {
                                \override Beam.positions = #'(6 . 6)
                                s16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16
                                - \staccato
                                s16
                                s16
                                s16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                s16
                                s16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                g''16
                                - \staccato
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16
                                - \staccato
                                s16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                s16
                                s16
                                s16
                                s16
                                s16
                                ]
                                \revert Beam.positions
                            }
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }
                    }
                    \context Voice = "Music.2"
                    {
                        {
                            \scaleDurations #'(1 . 1)
                            {
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                c'16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                e''16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                ef''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                af''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                g''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                c'16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                d'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                e''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                ef''16
                                ]
                            }
                        }
                    }
                    \context Voice = "Music.3"
                    {
                        {
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \scaleDurations #'(1 . 1)
                            {
                                \override Beam.positions = #'(8 . 8)
                                s16
                                [
                                s16
                                s16
                                s16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                e''16
                                - \accent
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                s16
                                s16
                                s16
                                s16
                                s16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                s16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                - \accent
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16
                                - \accent
                                s16
                                s16
                                ]
                                \revert Beam.positions
                            }
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }
                    }
                >>
            }

    ..  container:: example

        Hides tuplet brackets above imbricated voice:

        >>> score = baca.docs.make_empty_score(2)
        >>> figures = baca.FigureAccumulator(score)

        >>> collections = [
        ...     [0, 2, 10, 18, 16],
        ...     [15, 20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ... ]
        >>> figures(
        ...     "Music.2",
        ...     collections,
        ...     baca.figure([1], 16, treatments=[1]),
        ...     rmakers.beam_groups(beam_rests=True),
        ...     baca.imbricate(
        ...         "Music.1",
        ...         [2, 19, 9, 18, 16],
        ...         baca.accent(selector=lambda _: baca.select.pheads(_)),
        ...         rmakers.beam_groups(beam_rests=True),
        ...     ),
        ...     baca.staccato(selector=lambda _: baca.select.pheads(_)),
        ... )

        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=figures.time_signatures,
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 32)),
        ... )
        >>> figures.populate_commands(score, accumulator)

        >>> accumulator(
        ...     "Music.1",
        ...     baca.voice_one(selector=lambda _: abjad.select.leaf(_, 0)),
        ... )

        >>> accumulator(
        ...     "Music.2",
        ...     baca.voice_two(selector=lambda _: abjad.select.leaf(_, 0)),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #32
                        \time 9/8
                        s1 * 9/8
                    }
                    \context Voice = "Music.1"
                    {
                        {
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5
                            {
                                \voiceOne
                                s16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16
                                - \accent
                                s16
                                s16
                                s16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5
                            {
                                s16
                                s16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                g''16
                                - \accent
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16
                                - \accent
                                s16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5
                            {
                                s16
                                s16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16
                                - \accent
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                e''16
                                - \accent
                                s16
                                ]
                            }
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }
                    }
                    \context Voice = "Music.2"
                    {
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5
                            {
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                \voiceTwo
                                c'16
                                - \staccato
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16
                                - \staccato
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                - \staccato
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16
                                - \staccato
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                e''16
                                - \staccato
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5
                            {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                ef''16
                                - \staccato
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                af''16
                                - \staccato
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                g''16
                                - \staccato
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16
                                - \staccato
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                c'16
                                - \staccato
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5
                            {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                d'16
                                - \staccato
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                - \staccato
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16
                                - \staccato
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                e''16
                                - \staccato
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                ef''16
                                - \staccato
                                ]
                            }
                        }
                    }
                >>
            }

    ..  container:: example

        Works with pitch-classes:

        >>> score = baca.docs.make_empty_score(2)
        >>> figures = baca.FigureAccumulator(score)

        >>> segment = [
        ...     abjad.NumberedPitchClass(10),
        ...     abjad.NumberedPitchClass(6),
        ...     abjad.NumberedPitchClass(4),
        ...     abjad.NumberedPitchClass(3),
        ... ]
        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> figures(
        ...     "Music.2",
        ...     collections,
        ...     baca.figure([3], 16),
        ...     rmakers.beam(),
        ...     baca.imbricate(
        ...         "Music.1",
        ...         segment,
        ...         baca.accent(selector=lambda _: baca.select.pheads(_)),
        ...         rmakers.beam_groups(beam_rests=True),
        ...     ),
        ... )

        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=figures.time_signatures,
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ... )
        >>> figures.populate_commands(score, accumulator)

        >>> accumulator(
        ...     "Music.1",
        ...     baca.voice_one(selector=lambda _: abjad.select.leaf(_, 0)),
        ... )

        >>> accumulator(
        ...     "Music.2",
        ...     baca.voice_two(selector=lambda _: abjad.select.leaf(_, 0)),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \time 27/16
                        s1 * 27/16
                    }
                    \context Voice = "Music.1"
                    {
                        {
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \scaleDurations #'(1 . 1)
                            {
                                \voiceOne
                                s8.
                                [
                                s8.
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 1
                                bf'8.
                                - \accent
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 1
                                fs''8.
                                - \accent
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 1
                                e''8.
                                - \accent
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 1
                                ef''8.
                                - \accent
                                s8.
                                s8.
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                s8.
                                ]
                            }
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }
                    }
                    \context Voice = "Music.2"
                    {
                        {
                            \scaleDurations #'(1 . 1)
                            {
                                \voiceTwo
                                c'8.
                                [
                                d'8.
                                bf'8.
                                ]
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                fs''8.
                                [
                                e''8.
                                ef''8.
                                af''8.
                                g''8.
                                ]
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                a'8.
                            }
                        }
                    }
                >>
            }

    ..  container:: example

        Works with chords:

        >>> score = baca.docs.make_empty_score(2)
        >>> figures = baca.FigureAccumulator(score)

        >>> collections = [
        ...     {0, 2, 10, 18, 16},
        ...     [15, 20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ... ]
        >>> figures(
        ...     "Music.2",
        ...     collections,
        ...     baca.figure([1], 16),
        ...     rmakers.beam_groups(),
        ...     baca.imbricate(
        ...         "Music.1",
        ...         [2, 19, 9, 18, 16],
        ...         rmakers.beam_groups(),
        ...     ),
        ... )

        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=figures.time_signatures,
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 32)),
        ... )
        >>> figures.populate_commands(score, accumulator)

        >>> accumulator(
        ...     "Music.1",
        ...     baca.voice_one(selector=lambda _: abjad.select.leaf(_, 0)),
        ... )

        >>> accumulator(
        ...     "Music.2",
        ...     baca.voice_two(selector=lambda _: abjad.select.leaf(_, 0)),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #32
                        \time 11/16
                        s1 * 11/16
                    }
                    \context Voice = "Music.1"
                    {
                        {
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \scaleDurations #'(1 . 1)
                            {
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                \voiceOne
                                d'16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                s16
                                s16
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                g''16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                a'16
                                ]
                                s16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                s16
                                s16
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                fs''16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                e''16
                                ]
                                s16
                            }
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }
                    }
                    \context Voice = "Music.2"
                    {
                        {
                            \scaleDurations #'(1 . 1)
                            {
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                \voiceTwo
                                <c' d' bf' e'' fs''>16
                                [
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                ef''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                af''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                g''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                c'16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                d'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                e''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                ef''16
                                ]
                            }
                        }
                    }
                >>
            }

    ..  container:: example

        Works with rests:

        >>> score = baca.docs.make_empty_score(2)
        >>> figures = baca.FigureAccumulator(score)

        >>> collections = [
        ...     [0, 2, 10, 18, 16],
        ...     [15, 20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ... ]
        >>> figures(
        ...     "Music.2",
        ...     collections,
        ...     baca.figure([1], 16, affix=baca.rests_around([2], [2])),
        ...     rmakers.beam_groups(),
        ...     baca.imbricate(
        ...         "Music.1",
        ...         [2, 19, 9, 18, 16],
        ...         rmakers.beam_groups(),
        ...     ),
        ... )

        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=figures.time_signatures,
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 32)),
        ... )
        >>> figures.populate_commands(score, accumulator)

        >>> accumulator(
        ...     "Music.1",
        ...     baca.voice_one(selector=lambda _: abjad.select.leaf(_, 0)),
        ... )

        >>> accumulator(
        ...     "Music.2",
        ...     baca.voice_two(selector=lambda _: abjad.select.leaf(_, 0)),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #32
                        \time 19/16
                        s1 * 19/16
                    }
                    \context Voice = "Music.1"
                    {
                        {
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \scaleDurations #'(1 . 1)
                            {
                                \voiceOne
                                s8
                                s16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16
                                s16
                                s16
                                s16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                s16
                                s16
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                g''16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                a'16
                                ]
                                s16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                s16
                                s16
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                fs''16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                e''16
                                ]
                                s16
                                s8
                            }
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }
                    }
                    \context Voice = "Music.2"
                    {
                        {
                            \scaleDurations #'(1 . 1)
                            {
                                \voiceTwo
                                r8
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                c'16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                e''16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                ef''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                af''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                g''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                c'16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                d'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                e''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                ef''16
                                ]
                                r8
                            }
                        }
                    }
                >>
            }

    """
    return Imbrication(
        voice_name,
        segment,
        *specifiers,
        allow_unused_pitches=allow_unused_pitches,
        by_pitch_class=by_pitch_class,
        hocket=hocket,
        selector=selector,
        truncate_ties=truncate_ties,
    )


def lmr(
    *,
    left_counts: typing.Sequence[int] = (),
    left_cyclic: bool = False,
    left_length: int = 0,
    left_reversed: bool = False,
    middle_counts: typing.Sequence[int] = (),
    middle_cyclic: bool = False,
    middle_reversed: bool = False,
    priority: int | None = None,
    right_counts: typing.Sequence[int] = (),
    right_cyclic: bool = False,
    right_length: int = 0,
    right_reversed: bool = False,
) -> LMR:
    """
    Makes left-middle-right.

    ..  container:: example

        Default LMR:

        >>> lmr = baca.lmr()

        >>> parts = lmr([1])
        >>> for part in parts: part
        [1]

        >>> parts =lmr([1, 2])
        >>> for part in parts: part
        [1, 2]

        >>> parts = lmr([1, 2, 3])
        >>> for part in parts: part
        [1, 2, 3]

        >>> parts = lmr([1, 2, 3, 4])
        >>> for part in parts: part
        [1, 2, 3, 4]

        >>> parts = lmr([1, 2, 3, 4, 5])
        >>> for part in parts: part
        [1, 2, 3, 4, 5]

        >>> parts = lmr([1, 2, 3, 4, 5, 6])
        >>> for part in parts: part
        [1, 2, 3, 4, 5, 6]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
        >>> for part in parts: part
        [1, 2, 3, 4, 5, 6, 7]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
        >>> for part in parts: part
        [1, 2, 3, 4, 5, 6, 7, 8]

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> for part in parts: part
        [1, 2, 3, 4, 5, 6, 7, 8, 9]

    """
    return LMR(
        left_counts=left_counts,
        left_cyclic=left_cyclic,
        left_length=left_length,
        left_reversed=left_reversed,
        middle_counts=middle_counts,
        middle_cyclic=middle_cyclic,
        middle_reversed=middle_reversed,
        priority=priority,
        right_counts=right_counts,
        right_cyclic=right_cyclic,
        right_length=right_length,
        right_reversed=right_reversed,
    )


def nest(treatments: typing.Sequence, *, lmr: LMR = None) -> Nest:
    r"""
    Nests music.

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.nest("+4/16"),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 13/11
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10
                        {
                            \override TupletBracket.staff-padding = 2
                            \time 13/8
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10
                        {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5
                        {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding
                        }
                    }
                }
            >>

    """
    assert treatments is not None
    if not isinstance(treatments, list):
        treatments = [treatments]
    return Nest(lmr=lmr, treatments=treatments)


def figure(
    counts: typing.Sequence[int],
    denominator: int,
    *,
    acciaccatura: bool | Acciaccatura | LMR | None = None,
    affix: RestAffix = None,
    restart_talea: bool = False,
    signature: int = None,
    spelling: rmakers.Spelling = None,
    treatments: typing.Sequence = (),
) -> FigureMaker:
    """
    Makes figure-maker.
    """
    if acciaccatura is True:
        acciaccatura = Acciaccatura()
    elif isinstance(acciaccatura, LMR):
        acciaccatura = Acciaccatura(lmr=acciaccatura)
    if acciaccatura is not None:
        assert isinstance(acciaccatura, Acciaccatura), repr(acciaccatura)
    return FigureMaker(
        rmakers.Talea(counts=counts, denominator=denominator),
        acciaccatura=acciaccatura,
        affix=affix,
        restart_talea=restart_talea,
        signature=signature,
        spelling=spelling,
        treatments=treatments,
    )


def rests_after(counts: typing.Sequence[int]) -> RestAffix:
    r"""
    Makes rests after music.

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_after([2]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/8
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 9/8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 2/3
                    {
                        a'16
                        r8
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return RestAffix(suffix=counts)


def rests_around(prefix: list[int], suffix: list[int]) -> RestAffix:
    r"""
    Makes rests around music.

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [2]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 5/4
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 2/3
                    {
                        a'16
                        r8
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Works together with negative-valued talea:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [3]),
        ...         treatments=[1],
        ...     ),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.override(staff).TupletBracket.staff_padding = 4
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.staff-padding = 4
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/8
                    {
                        \time 13/8
                        r8
                        c'16
                        r16
                        d'16
                        r16
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 11/10
                    {
                        fs''16
                        r16
                        e''16
                        r16
                        ef''16
                        r16
                        af''16
                        r16
                        g''16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/5
                    {
                        a'16
                        r16
                        r8.
                    }
                }
            >>

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [-1, 1],
        ...         16,
        ...         affix=baca.rests_around([2], [3]),
        ...         treatments=[1],
        ...     ),
        ...     rmakers.beam(),
        ... )
        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.override(staff).TupletBracket.staff_padding = 4
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.staff-padding = 4
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/8
                    {
                        \time 13/8
                        r8
                        r16
                        c'16
                        r16
                        d'16
                        r16
                        bf'16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 11/10
                    {
                        r16
                        fs''16
                        r16
                        e''16
                        r16
                        ef''16
                        r16
                        af''16
                        r16
                        g''16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/5
                    {
                        r16
                        a'16
                        r8.
                    }
                }
            >>

    ..  container:: example

        With time treatments:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1],
        ...         16,
        ...         affix=baca.rests_around([1], [1]),
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/4
                    {
                        \time 9/16
                        r16
                        c'16
                        [
                        d'16
                        bf'16
                        ]
                    }
                    \times 4/5
                    {
                        fs''16
                        [
                        e''16
                        ef''16
                        af''16
                        g''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'16
                        r16
                    }
                }
            >>

    """
    return RestAffix(prefix=prefix, suffix=suffix)


def rests_before(counts: list[int]) -> RestAffix:
    r"""
    Makes rests before music.

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_before([2]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 19/16
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'16
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return RestAffix(prefix=counts)


def resume() -> Anchor:
    """
    Resumes music at next offset across all voices in score.
    """
    return Anchor()


def resume_after(remote_voice_name) -> Anchor:
    """
    Resumes music after remote selection.
    """
    return Anchor(
        remote_selector=lambda _: abjad.select.leaf(_, -1),
        remote_voice_name=remote_voice_name,
        use_remote_stop_offset=True,
    )


def skips_after(counts: list[int]) -> RestAffix:
    r"""
    Makes skips after music.

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.skips_after([2]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/8
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 9/8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 2/3
                    {
                        a'16
                        s8
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return RestAffix(skips_instead_of_rests=True, suffix=counts)


def skips_around(prefix: list[int], suffix: list[int]) -> RestAffix:
    r"""
    Makes skips around music.

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.skips_around([2], [2]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 5/4
                        s8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 2/3
                    {
                        a'16
                        s8
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return RestAffix(prefix=prefix, skips_instead_of_rests=True, suffix=suffix)


def skips_before(counts: list[int]) -> RestAffix:
    r"""
    Makes skips before music.

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.skips_before([2]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 19/16
                        s8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'16
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return RestAffix(prefix=counts, skips_instead_of_rests=True)


def stack(*commands) -> Stack:
    r"""
    Stack examples.

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure([1, 1, 2], 8, treatments=[(1, 4), (3, 8)]),
        ...     rmakers.denominator((1, 16)),
        ...     rmakers.beam(),
        ... )

        >>> collections = [
        ...     [0, 2, 10, 18, 16],
        ...     [15, 20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     [20, 19, 9, 0, 2],
        ...     [10, 18, 16, 15, 20],
        ...     [19, 9, 0, 2, 10],
        ... ]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.override(staff).Beam.positions = "#'(-6 . -6)"
        >>> abjad.override(staff).Stem.direction = abjad.DOWN
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                \with
                {
                    \override Beam.positions = #'(-6 . -6)
                    \override Stem.direction = #down
                }
                {
                    \times 4/6
                    {
                        \time 15/8
                        c'16
                        [
                        d'16
                        bf'8
                        fs''16
                        e''16
                        ]
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7
                    {
                        ef''8
                        [
                        af''16
                        g''16
                        a'8
                        c'16
                        ]
                    }
                    \times 4/7
                    {
                        d'16
                        [
                        bf'8
                        fs''16
                        e''16
                        ef''8
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        af''16
                        [
                        g''16
                        a'8
                        c'16
                        d'16
                        ]
                    }
                    \times 4/7
                    {
                        bf'8
                        [
                        fs''16
                        e''16
                        ef''8
                        af''16
                        ]
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7
                    {
                        g''16
                        [
                        a'8
                        c'16
                        d'16
                        bf'8
                        ]
                    }
                }
            >>

    """
    return Stack(*commands)
