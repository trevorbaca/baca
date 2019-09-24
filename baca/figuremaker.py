import abjad
import collections
import copy
import math
import typing
from abjadext import rmakers
from . import classes
from . import commandclasses
from . import pitchcommands
from . import pitchclasses
from . import rhythmcommands
from . import scoping
from . import spannercommands
from . import typings


### CLASSES ###


class Stack(object):
    """
    Stack.
    """

    ### CLASS ATTRIBUTES ###

    __slots__ = ("_commands",)

    # to make sure abjad.new() copies commands
    _positional_arguments_name = "commands"

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, *commands) -> None:
        commands = commands or ()
        commands_ = tuple(commands)
        self._commands = commands_

    ### SPECIAL METHODS ###

    def __call__(self, argument: typing.Any, **keywords) -> typing.Any:
        """
        Calls stack on ``argument``.
        """
        if not self.commands:
            return result
        try:
            result: typing.Any = self.commands[0](argument, **keywords)
        except:
            message = "exception while calling:\n"
            message += f"   {format(self.commands[0])}"
            raise Exception(message)
        for command in self.commands[1:]:
            try:
                result_ = command(result)
            except:
                message = "exception while calling:\n"
                message += f"   {format(command)}"
                raise Exception(message)
            if result_ is not None:
                result = result_
        return result

    def __eq__(self, argument) -> bool:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __format__(self, format_specification="") -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __hash__(self) -> int:
        """
        Delegates to format manager.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        manager = abjad.StorageFormatManager(self)
        return abjad.FormatSpecification(
            self, storage_format_args_values=self.commands
        )

    ### PUBLIC PROPERTIES ###

    @property
    def commands(self):
        """
        Gets commands.
        """
        return list(self._commands)


class LMR(object):
    """
    Left-middle-right.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_left_counts",
        "_left_cyclic",
        "_left_length",
        "_left_reversed",
        "_middle_counts",
        "_middle_cyclic",
        "_middle_reversed",
        "_priority",
        "_right_counts",
        "_right_cyclic",
        "_right_length",
        "_right_reversed",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        left_counts: typing.Sequence[int] = None,
        left_cyclic: bool = None,
        left_length: int = None,
        left_reversed: bool = None,
        middle_counts: typing.Sequence[int] = None,
        middle_cyclic: bool = None,
        middle_reversed: bool = None,
        priority: abjad.HorizontalAlignment = None,
        right_counts: typing.Sequence[int] = None,
        right_cyclic: bool = None,
        right_length: int = None,
        right_reversed: bool = None,
    ) -> None:
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
            assert priority in (abjad.Left, abjad.Right)
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

    def __call__(
        self, sequence: typing.Union[list, abjad.Segment] = None
    ) -> typing.List[abjad.Sequence]:
        """
        Calls LMR on ``sequence``.
        """
        assert isinstance(sequence, (list, abjad.Segment)), repr(sequence)
        top_lengths = self._get_top_lengths(len(sequence))
        top_parts = abjad.sequence(sequence).partition_by_counts(
            top_lengths, cyclic=False, overhang=abjad.Exact
        )
        parts: typing.List[abjad.Sequence] = []
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
        assert isinstance(parts, list), repr(parts)
        assert all(isinstance(_, abjad.Sequence) for _ in parts)
        return parts

    def __eq__(self, argument) -> bool:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __format__(self, format_specification="") -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __hash__(self) -> int:
        """
        Delegates to format manager.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_priority(self):
        if self.priority is None:
            return abjad.Left
        return self.priority

    def _get_top_lengths(self, total_length):
        left_length, middle_length, right_length = 0, 0, 0
        left_length = self.left_length or 0
        middle_length = 0
        right_length = self.right_length or 0
        if left_length and right_length:
            if self._get_priority() == abjad.Left:
                left_length = self.left_length or 0
                left_length = min([left_length, total_length])
                remaining_length = total_length - left_length
                if self.right_length is None:
                    right_length = remaining_length
                    middle_length = 0
                else:
                    right_length = self.right_length or 0
                    right_length = min([right_length, remaining_length])
                    remaining_length = total_length - (
                        left_length + right_length
                    )
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
                    remaining_length = total_length - (
                        right_length + left_length
                    )
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

    ### PUBLIC PROPERTIES ###

    @property
    def left_counts(self) -> typing.Optional[abjad.IntegerSequence]:
        """
        Gets left counts.

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
            Sequence([1])

            >>> parts = lmr([1, 2])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])

            >>> parts = lmr([1, 2, 3])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])

            >>> parts = lmr([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4])

            >>> parts = lmr([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5])

            >>> parts = lmr([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4])
            Sequence([5, 6])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5])
            Sequence([6, 7])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5, 6])
            Sequence([7, 8])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5, 6, 7])
            Sequence([8, 9])

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
            Sequence([1])

            >>> parts = lmr([1, 2])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])

            >>> parts = lmr([1, 2, 3])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3])

            >>> parts = lmr([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3])
            Sequence([4])

            >>> parts = lmr([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3])
            Sequence([4, 5])

            >>> parts = lmr([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3])
            Sequence([4])
            Sequence([5, 6])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3])
            Sequence([4, 5])
            Sequence([6, 7])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3])
            Sequence([4, 5, 6])
            Sequence([7, 8])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3])
            Sequence([4, 5, 6, 7])
            Sequence([8, 9])

        """
        return self._left_counts

    @property
    def left_cyclic(self) -> typing.Optional[bool]:
        """
        Is true when specifier reads left counts cyclically.
        """
        return self._left_cyclic

    @property
    def left_length(self) -> typing.Optional[int]:
        """
        Gets left length.

        ..  container:: example

            Left length equal to 2:

            >>> lmr = baca.lmr(
            ...     left_length=2,
            ... )

            >>> parts = lmr([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr([1, 2])
            >>> for part in parts: part
            Sequence([1, 2])

            >>> parts = lmr([1, 2, 3])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3])

            >>> parts = lmr([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])

            >>> parts = lmr([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5])

            >>> parts = lmr([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6, 7])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6, 7, 8])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6, 7, 8, 9])

        """
        return self._left_length

    @property
    def left_reversed(self) -> typing.Optional[bool]:
        """
        Is true when specifier reverses left partition.
        """
        return self._left_reversed

    @property
    def middle_counts(self) -> typing.Optional[abjad.IntegerSequence]:
        """
        Gets middle counts.
        """
        return self._middle_counts

    @property
    def middle_cyclic(self) -> typing.Optional[bool]:
        """
        Is true when specifier reads middle counts cyclically.

        ..  container:: example

            Cyclic middle counts equal to [2]:

            >>> lmr = baca.lmr(
            ...     middle_counts=[2],
            ...     middle_cyclic=True,
            ... )

            >>> parts = lmr([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr([1, 2])
            >>> for part in parts: part
            Sequence([1, 2])

            >>> parts = lmr([1, 2, 3])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3])

            >>> parts = lmr([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])

            >>> parts = lmr([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5])

            >>> parts = lmr([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5, 6])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5, 6])
            Sequence([7])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5, 6])
            Sequence([7, 8])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5, 6])
            Sequence([7, 8])
            Sequence([9])

            Odd parity produces length-1 part at right.

        """
        return self._middle_cyclic

    @property
    def middle_reversed(self) -> typing.Optional[bool]:
        """
        Is true when specifier reverses middle partition.

        ..  container:: example

            Reversed cyclic middle counts equal to [2]:

            >>> lmr = baca.lmr(
            ...     middle_counts=[2],
            ...     middle_cyclic=True,
            ...     middle_reversed=True,
            ... )

            >>> parts = lmr([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr([1, 2])
            >>> for part in parts: part
            Sequence([1, 2])

            >>> parts = lmr([1, 2, 3])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])

            >>> parts = lmr([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])

            >>> parts = lmr([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5])

            >>> parts = lmr([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5, 6])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5])
            Sequence([6, 7])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5, 6])
            Sequence([7, 8])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5])
            Sequence([6, 7])
            Sequence([8, 9])

            Odd parity produces length-1 part at left.

        """
        return self._middle_reversed

    @property
    def priority(self) -> typing.Optional[abjad.HorizontalAlignment]:
        """
        Gets priority.

        ..  container:: example

            Priority to the left:

            >>> lmr = baca.lmr(
            ...     left_length=2,
            ...     right_length=1,
            ... )

            >>> parts = lmr([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr([1, 2])
            >>> for part in parts: part
            Sequence([1, 2])

            >>> parts = lmr([1, 2, 3])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3])

            >>> parts = lmr([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3])
            Sequence([4])

            >>> parts = lmr([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5])

            >>> parts = lmr([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5])
            Sequence([6])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6])
            Sequence([7])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6, 7])
            Sequence([8])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6, 7, 8])
            Sequence([9])

        ..  container:: example

            Priority to the right:

            >>> lmr = baca.lmr(
            ...     left_length=2,
            ...     priority=abjad.Right,
            ...     right_length=1,
            ... )

            >>> parts = lmr([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr([1, 2])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])

            >>> parts = lmr([1, 2, 3])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3])

            >>> parts = lmr([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3])
            Sequence([4])

            >>> parts = lmr([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5])

            >>> parts = lmr([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5])
            Sequence([6])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6])
            Sequence([7])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6, 7])
            Sequence([8])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6, 7, 8])
            Sequence([9])

        """
        return self._priority

    @property
    def right_counts(self) -> typing.Optional[abjad.IntegerSequence]:
        """
        Gets right counts.
        """
        return self._right_counts

    @property
    def right_cyclic(self) -> typing.Optional[bool]:
        """
        Is true when specifier reads right counts cyclically.
        """
        return self._right_cyclic

    @property
    def right_length(self) -> typing.Optional[int]:
        """
        Gets right length.

        ..  container:: example

            Right length equal to 2:

            >>> lmr = baca.lmr(
            ...     right_length=2,
            ... )

            >>> parts = lmr([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr([1, 2])
            >>> for part in parts: part
            Sequence([1, 2])

            >>> parts = lmr([1, 2, 3])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])

            >>> parts = lmr([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])

            >>> parts = lmr([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1, 2, 3])
            Sequence([4, 5])

            >>> parts = lmr([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1, 2, 3, 4])
            Sequence([5, 6])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1, 2, 3, 4, 5])
            Sequence([6, 7])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1, 2, 3, 4, 5, 6])
            Sequence([7, 8])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1, 2, 3, 4, 5, 6, 7])
            Sequence([8, 9])

        ..  container:: example

            Right length equal to 2 and left counts equal to [1]:

            >>> lmr = baca.lmr(
            ...     left_counts=[1],
            ...     left_cyclic=False,
            ...     right_length=2,
            ... )

            >>> parts = lmr([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr([1, 2])
            >>> for part in parts: part
            Sequence([1, 2])

            >>> parts = lmr([1, 2, 3])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])

            >>> parts = lmr([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3, 4])

            >>> parts = lmr([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5])

            >>> parts = lmr([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3, 4])
            Sequence([5, 6])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3, 4, 5])
            Sequence([6, 7])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3, 4, 5, 6])
            Sequence([7, 8])

            >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3, 4, 5, 6, 7])
            Sequence([8, 9])

        """
        return self._right_length

    @property
    def right_reversed(self) -> typing.Optional[bool]:
        """
        Is true when specifier reverses right partition.
        """
        return self._right_reversed


class Acciaccatura(object):
    """
    Acciaccatura.

    ..  container:: example

        >>> baca.Acciaccatura()
        Acciaccatura(durations=[Duration(1, 16)], lmr=LMR())

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_durations", "_lmr")

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        durations: typing.Sequence[abjad.DurationTyping] = [(1, 16)],
        lmr: LMR = LMR(),
    ) -> None:
        durations_ = [abjad.Duration(_) for _ in durations]
        self._durations = durations_
        assert isinstance(lmr, LMR), repr(lmr)
        self._lmr = lmr

    ### SPECIAL METHODS ###

    def __call__(
        self, collection: typing.Union[list, abjad.Segment] = None
    ) -> typing.Tuple[
        typing.List[typing.Optional[abjad.BeforeGraceContainer]], list
    ]:
        """
        Calls acciaccatura on ``collection``.

        :param collection: collection.
        """
        prototype = (list, abjad.Segment)
        assert isinstance(collection, prototype), repr(collection)
        segment_parts = self.lmr(collection)
        segment_parts = [_ for _ in segment_parts if _]
        collection = [_[-1] for _ in segment_parts]
        durations = self.durations
        acciaccatura_containers: typing.List[
            typing.Union[abjad.BeforeGraceContainer, None]
        ] = []
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
                abjad.beam(acciaccatura_container[:], tag="Acciaccatura")
            acciaccatura_containers.append(acciaccatura_container)
        assert len(acciaccatura_containers) == len(collection)
        assert isinstance(collection, list), repr(collection)
        return acciaccatura_containers, collection

    def __eq__(self, argument) -> bool:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Delegates to format manager.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __format__(self, format_specification="") -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __repr__(self) -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def durations(self) -> typing.List[abjad.Duration]:
        r"""
        Gets durations.

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
            >>> selections = stack(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                }
                <<
                    \new GlobalContext
                    {
                        \time 3/4
                        s1 * 3/4
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16
                                [                                                                        %! Acciaccatura
                                e''16
                                ]                                                                        %! Acciaccatura
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! Acciaccatura
                                g''16
                                a'16
                                ]                                                                        %! Acciaccatura
                            }
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                                [                                                                        %! Acciaccatura
                                bf'16
                                fs''16
                                e''16
                                ]                                                                        %! Acciaccatura
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! Acciaccatura
                                g''16
                                a'16
                                c'16
                                d'16
                                ]                                                                        %! Acciaccatura
                            }
                            bf'8
                        }
                    }
                >>

        ..  container:: example

            Eighth-note acciaccaturas:

            >>> specifier = baca.Acciaccatura(durations=[(1, 8)])
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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                }
                <<
                    \new GlobalContext
                    {
                        \time 3/4
                        s1 * 3/4
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'8
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''8
                                [                                                                        %! Acciaccatura
                                e''8
                                ]                                                                        %! Acciaccatura
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''8
                                [                                                                        %! Acciaccatura
                                g''8
                                a'8
                                ]                                                                        %! Acciaccatura
                            }
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'8
                                [                                                                        %! Acciaccatura
                                bf'8
                                fs''8
                                e''8
                                ]                                                                        %! Acciaccatura
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''8
                                [                                                                        %! Acciaccatura
                                g''8
                                a'8
                                c'8
                                d'8
                                ]                                                                        %! Acciaccatura
                            }
                            bf'8
                        }
                    }
                >>

        """
        return self._durations

    @property
    def lmr(self) -> LMR:
        r"""
        Gets LMR. 

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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                }
                <<
                    \new GlobalContext
                    {
                        \time 3/4
                        s1 * 3/4
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16
                                [                                                                        %! Acciaccatura
                                e''16
                                ]                                                                        %! Acciaccatura
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! Acciaccatura
                                g''16
                                a'16
                                ]                                                                        %! Acciaccatura
                            }
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                                [                                                                        %! Acciaccatura
                                bf'16
                                fs''16
                                e''16
                                ]                                                                        %! Acciaccatura
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! Acciaccatura
                                g''16
                                a'16
                                c'16
                                d'16
                                ]                                                                        %! Acciaccatura
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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                }
                <<
                    \new GlobalContext
                    {
                        \time 3/2
                        s1 * 3/2
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16
                                [                                                                        %! Acciaccatura
                                e''16
                                ]                                                                        %! Acciaccatura
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! Acciaccatura
                                g''16
                                ]                                                                        %! Acciaccatura
                            }
                            a'8
                            [
                            c'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                                [                                                                        %! Acciaccatura
                                bf'16
                                ]                                                                        %! Acciaccatura
                            }
                            fs''8
                            [
                            e''8
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! Acciaccatura
                                g''16
                                ]                                                                        %! Acciaccatura
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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                }
                <<
                    \new GlobalContext
                    {
                        \time 3/2
                        s1 * 3/2
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16
                                [                                                                        %! Acciaccatura
                                e''16
                                ]                                                                        %! Acciaccatura
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            af''8
                            [
                            \acciaccatura {
                                g''16
                                [                                                                        %! Acciaccatura
                                a'16
                                ]                                                                        %! Acciaccatura
                            }
                            c'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            d'8
                            [
                            bf'8
                            \acciaccatura {
                                fs''16
                                [                                                                        %! Acciaccatura
                                e''16
                                ]                                                                        %! Acciaccatura
                            }
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            af''8
                            [
                            g''8
                            a'8
                            \acciaccatura {
                                c'16
                                [                                                                        %! Acciaccatura
                                d'16
                                ]                                                                        %! Acciaccatura
                            }
                            bf'8
                            ]
                        }
                    }
                >>

        ..  container:: example

            At most two acciaccaturas at the beginning of every collection and
            then at most two acciaccaturas at the end of every collection:

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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                }
                <<
                    \new GlobalContext
                    {
                        \time 9/8
                        s1 * 9/8
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16
                                [                                                                        %! Acciaccatura
                                e''16
                                ]                                                                        %! Acciaccatura
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! Acciaccatura
                                g''16
                                ]                                                                        %! Acciaccatura
                            }
                            a'8
                            [
                            c'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                                [                                                                        %! Acciaccatura
                                bf'16
                                ]                                                                        %! Acciaccatura
                            }
                            fs''8
                            [
                            \acciaccatura {
                                e''16
                            }
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! Acciaccatura
                                g''16
                                ]                                                                        %! Acciaccatura
                            }
                            a'8
                            [
                            \acciaccatura {
                                c'16
                                [                                                                        %! Acciaccatura
                                d'16
                                ]                                                                        %! Acciaccatura
                            }
                            bf'8
                            ]
                        }
                    }
                >>

        ..  container:: example

            As many acciaccaturas as possible in the middle of every
            collection:

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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                }
                <<
                    \new GlobalContext
                    {
                        \time 11/8
                        s1 * 11/8
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            d'8
                            [
                            bf'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''8
                            [
                            \acciaccatura {
                                e''16
                            }
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            af''8
                            [
                            \acciaccatura {
                                g''16
                                [                                                                        %! Acciaccatura
                                a'16
                                ]                                                                        %! Acciaccatura
                            }
                            c'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            d'8
                            [
                            \acciaccatura {
                                bf'16
                                [                                                                        %! Acciaccatura
                                fs''16
                                e''16
                                ]                                                                        %! Acciaccatura
                            }
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            af''8
                            [
                            \acciaccatura {
                                g''16
                                [                                                                        %! Acciaccatura
                                a'16
                                c'16
                                d'16
                                ]                                                                        %! Acciaccatura
                            }
                            bf'8
                            ]
                        }
                    }
                >>

        """
        return self._lmr


class Anchor(object):
    """
    Anchor.

    ..  container:: example

        >>> baca.Anchor()
        Anchor()

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_figure_name",
        "_local_selector",
        "_remote_selector",
        "_remote_voice_name",
        "_use_remote_stop_offset",
    )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        figure_name: str = None,
        local_selector: abjad.SelectorTyping = None,
        remote_selector: abjad.SelectorTyping = None,
        remote_voice_name: str = None,
        use_remote_stop_offset: bool = None,
    ) -> None:
        if figure_name is not None:
            assert isinstance(figure_name, str), repr(figure_name)
        self._figure_name = figure_name
        if local_selector is not None and not isinstance(
            local_selector, abjad.Expression
        ):
            raise TypeError(f"must be selector: {local_selector!r}.")
        self._local_selector = local_selector
        if remote_selector is not None and not isinstance(
            remote_selector, abjad.Expression
        ):
            raise TypeError(f"must be selector: {remote_selector!r}.")
        self._remote_selector = remote_selector
        if remote_voice_name is not None and not isinstance(
            remote_voice_name, str
        ):
            raise TypeError(f"must be string: {remote_voice_name!r}.")
        self._remote_voice_name = remote_voice_name
        if use_remote_stop_offset is not None:
            use_remote_stop_offset = bool(use_remote_stop_offset)
        self._use_remote_stop_offset = use_remote_stop_offset

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __format__(self, format_specification="") -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __hash__(self) -> int:
        """
        Delegates to format manager.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def figure_name(self) -> typing.Optional[str]:
        """
        Gets figure name.
        """
        return self._figure_name

    @property
    def local_selector(self) -> typing.Optional[abjad.Expression]:
        """
        Gets local selector.
        """
        return self._local_selector

    @property
    def remote_selector(self) -> typing.Optional[abjad.Expression]:
        """
        Gets remote selector.
        """
        return self._remote_selector

    @property
    def remote_voice_name(self) -> typing.Optional[str]:
        """
        Gets remote voice name.
        """
        return self._remote_voice_name

    @property
    def use_remote_stop_offset(self) -> typing.Optional[bool]:
        """
        Is true when contribution anchors to remote selection stop offset.

        Otherwise anchors to remote selection start offset.
        """
        return self._use_remote_stop_offset


class Coat(object):
    """
    Coat.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_argument",)

    ### INITIALIZER ###

    def __init__(self, argument: typing.Union[int, str, abjad.Pitch]) -> None:
        self._argument = argument

    ### PUBLIC PROPERTIES ###

    @property
    def argument(self) -> typing.Union[int, str, abjad.Pitch]:
        """
        Gets argument.
        """
        return self._argument


class Imbrication(object):
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
        segment: typing.List[int] = None,
        *commands,
        allow_unused_pitches: bool = None,
        by_pitch_class: bool = None,
        hocket: bool = None,
        selector: abjad.SelectorTyping = None,
        truncate_ties: bool = None,
    ) -> None:
        assert isinstance(voice_name, str), repr(voice_name)
        self._voice_name = voice_name
        if segment is not None:
            assert isinstance(segment, list), repr(segment)
        self._segment = segment
        self._commands = commands
        if allow_unused_pitches is not None:
            allow_unused_pitches = bool(allow_unused_pitches)
        self._allow_unused_pitches = allow_unused_pitches
        if by_pitch_class is not None:
            by_pitch_class = bool(by_pitch_class)
        self._by_pitch_class = by_pitch_class
        if hocket is not None:
            hocket = bool(hocket)
        self._hocket = hocket
        if selector is not None:
            if not isinstance(selector, abjad.Expression):
                raise TypeError(f"selector or none only: {selector!r}.")
        self._selector = selector
        if truncate_ties is not None:
            truncate_ties = bool(truncate_ties)
        self._truncate_ties = truncate_ties

    ### SPECIAL METHODS ###

    def __call__(
        self, container: abjad.Container = None
    ) -> typing.Dict[str, abjad.Selection]:
        """
        Calls imbrication on ``container``.

        :param container: container.
        """
        original_container = container
        container = copy.deepcopy(container)
        abjad.override(container).tuplet_bracket.stencil = False
        abjad.override(container).tuplet_number.stencil = False
        segment = classes.Sequence(self.segment).flatten(depth=-1)
        if self.by_pitch_class:
            segment = [abjad.NumberedPitchClass(_) for _ in segment]
        cursor = classes.Cursor(
            singletons=True, source=segment, suppress_exception=True
        )
        pitch_number = cursor.next()
        if self.selector is not None:
            selection = self.selector(original_container)
        selected_logical_ties = None
        if self.selector is not None:
            selection = self.selector(container)
            agent = abjad.iterate(selection)
            selected_logical_ties = agent.logical_ties(pitched=True)
            selected_logical_ties = list(selected_logical_ties)
        selector = abjad.select(original_container)
        original_logical_ties = selector.logical_ties()
        logical_ties = abjad.select(container).logical_ties()
        pairs = zip(logical_ties, original_logical_ties)
        for logical_tie, original_logical_tie in pairs:
            if (
                selected_logical_ties is not None
                and logical_tie not in selected_logical_ties
            ):
                for leaf in logical_tie:
                    duration = leaf.written_duration
                    skip = abjad.Skip(duration)
                    abjad.mutate(leaf).replace([skip])
            elif isinstance(logical_tie.head, abjad.Rest):
                for leaf in logical_tie:
                    duration = leaf.written_duration
                    skip = abjad.Skip(duration)
                    abjad.mutate(leaf).replace([skip])
            elif isinstance(logical_tie.head, abjad.Skip):
                pass
            elif self._matches_pitch(logical_tie.head, pitch_number):
                if isinstance(pitch_number, Coat):
                    for leaf in logical_tie:
                        duration = leaf.written_duration
                        skip = abjad.Skip(duration)
                        abjad.mutate(leaf).replace([skip])
                    pitch_number = cursor.next()
                    continue
                self._trim_matching_chord(logical_tie, pitch_number)
                pitch_number = cursor.next()
                if self.truncate_ties:
                    head = logical_tie.head
                    tail = logical_tie.tail
                    for leaf in logical_tie[1:]:
                        duration = leaf.written_duration
                        skip = abjad.Skip(duration)
                        abjad.mutate(leaf).replace([skip])
                    abjad.detach(abjad.Tie, head)
                    next_leaf = abjad.inspect(tail).leaf(1)
                    if next_leaf is not None:
                        abjad.detach(abjad.RepeatTie, next_leaf)
                if self.hocket:
                    for leaf in original_logical_tie:
                        duration = leaf.written_duration
                        skip = abjad.Skip(duration)
                        abjad.mutate(leaf).replace([skip])
            else:
                for leaf in logical_tie:
                    duration = leaf.written_duration
                    skip = abjad.Skip(duration)
                    abjad.mutate(leaf).replace([skip])
        if not self.allow_unused_pitches and not cursor.is_exhausted:
            current, total = cursor.position - 1, len(cursor)
            message = f"{cursor!r} used only {current} of {total} pitches."
            raise Exception(message)
        self._call_commands(container)
        selection = abjad.select(container)
        if not self.hocket:
            pleaves = classes.Selection(container).pleaves()
            assert isinstance(pleaves, abjad.Selection)
            for pleaf in pleaves:
                abjad.attach(abjad.tags.ALLOW_OCTAVE, pleaf)
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
            if isinstance(command, rhythmcommands.RhythmCommand):
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

    @staticmethod
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
        if isinstance(pitch_object, (int, float)):
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

    @staticmethod
    def _trim_matching_chord(logical_tie, pitch_object):
        if isinstance(logical_tie.head, abjad.Note):
            return
        assert isinstance(logical_tie.head, abjad.Chord), repr(logical_tie)
        if isinstance(pitch_object, abjad.PitchClass):
            raise NotImplementedError(logical_tie, pitch_object)
        for chord in logical_tie:
            duration = chord.written_duration
            note = abjad.Note(pitch_object, duration)
            abjad.mutate(chord).replace([note])

    ### PUBLIC PROPERTIES ###

    @property
    def allow_unused_pitches(self) -> typing.Optional[bool]:
        r"""
        Is true when imbrication allows unused pitches.

        ..  container:: example

            Allows unused pitches:

            >>> template = baca.TwoVoiceStaffScoreTemplate()
            >>> accumulator = baca.Accumulator(template)

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ... ]
            >>> accumulator(
            ...     "Music_Voice_Two",
            ...     collections,
            ...     baca.figure([1], 16),
            ...     rmakers.beam_groups(beam_rests=True),
            ...     baca.imbricate(
            ...         "Music_Voice_One",
            ...         [2, 19, 9, 18, 16],
            ...         baca.accent(selector=baca.pheads()),
            ...         rmakers.beam_groups(beam_rests=True),
            ...         allow_unused_pitches=True,
            ...     ),
            ...     baca.staccato(selector=baca.pheads()),
            ... )

            >>> maker = baca.SegmentMaker(
            ...     ignore_repeat_pitch_classes=True,
            ...     score_template=baca.TwoVoiceStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 32)),
            ...     time_signatures=accumulator.time_signatures,
            ... )
            >>> accumulator.populate_segment_maker(maker)
            >>> lilypond_file = maker.run(environment="docs")
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                <BLANKLINE>
                \context Score = "Score"                                                                 %! baca.TwoVoiceStaffScoreTemplate.__call__
                <<                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                    \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                    <<                                                                                   %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                        \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                        {                                                                                %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                            % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \baca-new-spacing-section #1 #32                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 5/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            s1 * 5/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                            \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                            \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                            \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                            \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                            s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                            \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                            \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                <BLANKLINE>
                        }                                                                                %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                    >>                                                                                   %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                    \context MusicContext = "Music_Context"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                    <<                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                        \context MusicStaff = "Music_Staff"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                        <<                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                            \context MusicVoiceOne = "Music_Voice_One"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                            {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                                {
                                    \override TupletBracket.stencil = ##f
                                    \override TupletNumber.stencil = ##f
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [Music_Voice_One measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                        s16
                                        [
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        d'16
                                        - \accent                                                        %! baca.accent():IndicatorCommand
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                    }
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        g''16
                                        - \accent                                                        %! baca.accent():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        a'16
                                        - \accent                                                        %! baca.accent():IndicatorCommand
                <BLANKLINE>
                                        s16
                                        ]
                <BLANKLINE>
                                    }
                                    \revert TupletBracket.stencil
                                    \revert TupletNumber.stencil
                <BLANKLINE>
                                }
                <BLANKLINE>
                                <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                    \context Voice = "Music_Voice_One"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                        % [Music_Voice_One measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                        \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                        c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                    \context Voice = "Rest_Voice_One"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                        % [Rest_Voice_One measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                        \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                        \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                        \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                            }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                            \context MusicVoiceTwo = "Music_Voice_Two"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                            {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                                {
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [Music_Voice_Two measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                        \set stemLeftBeamCount = 0
                                        \set stemRightBeamCount = 2
                                        c'16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                                        [
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        d'16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        bf'!16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        fs''!16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 1
                                        e''16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                    }
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 2
                                        ef''!16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        af''!16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        g''16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        a'16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 0
                                        c'16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                                        ]
                <BLANKLINE>
                                    }
                <BLANKLINE>
                                }
                <BLANKLINE>
                                <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                    \context Voice = "Music_Voice_Two"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                        % [Music_Voice_Two measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                        \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                        c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                    \context Voice = "Rest_Voice_Two"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                        % [Rest_Voice_Two measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                        \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                        \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                        \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                            }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                        >>                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                    >>                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                >>                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__

        ..  container:: example exception

            Raises exception on unused pitches:

            >>> template = baca.TwoVoiceStaffScoreTemplate()
            >>> accumulator = baca.Accumulator(template)
            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ... ]
            >>> accumulator(
            ...     "Music_Voice_Two",
            ...     collections,
            ...     baca.figure([1], 16),
            ...     rmakers.beam_groups(beam_rests=True),
            ...     baca.imbricate(
            ...         "Music_Voice_One",
            ...         [2, 19, 9, 18, 16],
            ...         baca.accent(selector=baca.pheads()),
            ...         rmakers.beam_groups(beam_rests=True),
            ...         allow_unused_pitches=False,
            ...     ),
            ...     baca.staccato(selector=baca.pheads()),
            ... )
            Traceback (most recent call last):
                ...
            Exception: Cursor(source=Sequence(items=(2, 19, 9, 18, 16)),
            position=4, singletons=True, suppress_exception=True) used only 3
            of 5 pitches.

        """
        return self._allow_unused_pitches

    @property
    def by_pitch_class(self) -> typing.Optional[bool]:
        """
        Is true when imbrication matches on pitch-class rather than pitch.
        """
        return self._by_pitch_class

    @property
    def commands(self) -> typing.List:
        """
        Gets commands.
        """
        return list(self._commands)

    @property
    def hocket(self) -> typing.Optional[bool]:
        r"""
        Is true when imbrication hockets voices.

        ..  container:: example

            Hockets voices:

            >>> template = baca.TwoVoiceStaffScoreTemplate()
            >>> accumulator = baca.Accumulator(template)

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ... ]
            >>> accumulator(
            ...     "Music_Voice_Two",
            ...     collections,
            ...     baca.figure([1], 16),
            ...     rmakers.beam_groups(beam_rests=True),
            ...     baca.imbricate(
            ...         "Music_Voice_One",
            ...         [2, 19, 9, 18, 16],
            ...         baca.accent(selector=baca.pheads()),
            ...         rmakers.beam_groups(beam_rests=True),
            ...         hocket=True,
            ...     ),
            ...     baca.staccato(selector=baca.pheads()),
            ... )

            >>> maker = baca.SegmentMaker(
            ...     ignore_repeat_pitch_classes=True,
            ...     score_template=baca.TwoVoiceStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 32)),
            ...     time_signatures=accumulator.time_signatures,
            ... )
            >>> accumulator.populate_segment_maker(maker)
            >>> lilypond_file = maker.run(environment="docs")
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                <BLANKLINE>
                \context Score = "Score"                                                                 %! baca.TwoVoiceStaffScoreTemplate.__call__
                <<                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                    \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                    <<                                                                                   %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                        \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                        {                                                                                %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                            % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \baca-new-spacing-section #1 #32                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 15/16                                                                  %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            s1 * 15/16                                                                   %! baca.SegmentMaker._make_global_skips(1)
                            \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                            \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                            \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                            \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                            s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                            \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                            \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                <BLANKLINE>
                        }                                                                                %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                    >>                                                                                   %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                    \context MusicContext = "Music_Context"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                    <<                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                        \context MusicStaff = "Music_Staff"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                        <<                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                            \context MusicVoiceOne = "Music_Voice_One"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                            {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                                {
                                    \override TupletBracket.stencil = ##f
                                    \override TupletNumber.stencil = ##f
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [Music_Voice_One measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                        s16
                                        [
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        d'16
                                        - \accent                                                        %! baca.accent():IndicatorCommand
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                    }
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        g''16
                                        - \accent                                                        %! baca.accent():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        a'16
                                        - \accent                                                        %! baca.accent():IndicatorCommand
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                    }
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        fs''!16
                                        - \accent                                                        %! baca.accent():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        e''16
                                        - \accent                                                        %! baca.accent():IndicatorCommand
                <BLANKLINE>
                                        s16
                                        ]
                <BLANKLINE>
                                    }
                                    \revert TupletBracket.stencil
                                    \revert TupletNumber.stencil
                <BLANKLINE>
                                }
                <BLANKLINE>
                                <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                    \context Voice = "Music_Voice_One"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                        % [Music_Voice_One measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                        \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                        c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                    \context Voice = "Rest_Voice_One"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                        % [Rest_Voice_One measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                        \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                        \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                        \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                            }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                            \context MusicVoiceTwo = "Music_Voice_Two"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                            {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                                {
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [Music_Voice_Two measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                        \set stemLeftBeamCount = 0
                                        \set stemRightBeamCount = 2
                                        c'16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                                        [
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        bf'!16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        fs''!16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 1
                                        e''16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                    }
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 2
                                        ef''!16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        af''!16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 1
                                        c'16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                    }
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 2
                                        d'16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        bf'!16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 0
                                        ef''!16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                                        ]
                <BLANKLINE>
                                    }
                <BLANKLINE>
                                }
                <BLANKLINE>
                                <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                    \context Voice = "Music_Voice_Two"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                        % [Music_Voice_Two measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                        \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                        c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                    \context Voice = "Rest_Voice_Two"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                        % [Rest_Voice_Two measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                        \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                        \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                        \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                            }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                        >>                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                    >>                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                >>                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__

        """
        return self._hocket

    @property
    def segment(self) -> typing.Optional[typing.List[int]]:
        """
        Gets to-be-imbricated segment.
        """
        return self._segment

    @property
    def selector(self) -> typing.Optional[abjad.Expression]:
        r"""
        Gets selector.

        ..  container:: example

            Selects last nine notes:

            >>> template = baca.TwoVoiceStaffScoreTemplate()
            >>> accumulator = baca.Accumulator(template)

            >>> collections = [
            ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
            ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
            ... ]
            >>> accumulator(
            ...     "Music_Voice_Two",
            ...     collections,
            ...     baca.figure([1], 16),
            ...     rmakers.beam_groups(beam_rests=True),
            ...     baca.imbricate(
            ...         "Music_Voice_One",
            ...         [2, 18, 16, 15],
            ...         baca.accent(selector=baca.pheads()),
            ...         rmakers.beam_groups(beam_rests=True),
            ...         selector=baca.plts()[-9:],
            ...     ),
            ...     baca.staccato(selector=baca.pheads()),
            ... )

            >>> maker = baca.SegmentMaker(
            ...     score_template=template,
            ...     spacing=baca.minimum_duration((1, 32)),
            ...     time_signatures=accumulator.time_signatures,
            ... )
            >>> accumulator.populate_segment_maker(maker)
            >>> lilypond_file = maker.run(environment="docs")
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                <BLANKLINE>
                \context Score = "Score"                                                                 %! baca.TwoVoiceStaffScoreTemplate.__call__
                <<                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                    \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                    <<                                                                                   %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                        \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                        {                                                                                %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                            % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \baca-new-spacing-section #1 #32                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 9/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            s1 * 9/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                            \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                            \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                            \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                            \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                            s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                            \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                            \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                <BLANKLINE>
                        }                                                                                %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                    >>                                                                                   %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                    \context MusicContext = "Music_Context"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                    <<                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                        \context MusicStaff = "Music_Staff"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                        <<                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                            \context MusicVoiceOne = "Music_Voice_One"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                            {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                                {
                                    \override TupletBracket.stencil = ##f
                                    \override TupletNumber.stencil = ##f
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [Music_Voice_One measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                        s16
                                        [
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                    }
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                    }
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        d'16
                                        - \accent                                                        %! baca.accent():IndicatorCommand
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        fs''!16
                                        - \accent                                                        %! baca.accent():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 1
                                        e''16
                                        - \accent                                                        %! baca.accent():IndicatorCommand
                <BLANKLINE>
                                    }
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 2
                                        ef''!16
                                        - \accent                                                        %! baca.accent():IndicatorCommand
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        s16
                                        ]
                <BLANKLINE>
                                    }
                                    \revert TupletBracket.stencil
                                    \revert TupletNumber.stencil
                <BLANKLINE>
                                }
                <BLANKLINE>
                                <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                    \context Voice = "Music_Voice_One"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                        % [Music_Voice_One measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                        \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                        c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                    \context Voice = "Rest_Voice_One"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                        % [Rest_Voice_One measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                        \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                        \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                        \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                            }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                            \context MusicVoiceTwo = "Music_Voice_Two"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                            {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                                {
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [Music_Voice_Two measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                        \set stemLeftBeamCount = 0
                                        \set stemRightBeamCount = 2
                                        c'16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                                        [
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        d'16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        bf'!16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        fs''!16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 1
                                        e''16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                    }
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 2
                                        ef''!16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        af''!16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        g''16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 1
                                        a'16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                    }
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 2
                                        c'16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        d'16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        bf'!16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        fs''!16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 1
                                        e''16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                    }
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 2
                                        ef''!16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        af''!16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        g''16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 0
                                        a'16
                                        - \staccato                                                      %! baca.staccato():IndicatorCommand
                                        ]
                <BLANKLINE>
                                    }
                <BLANKLINE>
                                }
                <BLANKLINE>
                                <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                    \context Voice = "Music_Voice_Two"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                        % [Music_Voice_Two measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                        \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                        c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                    \context Voice = "Rest_Voice_Two"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                        % [Rest_Voice_Two measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                        \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                        \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                        \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                            }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                        >>                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                    >>                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                >>                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__

        """
        return self._selector

    @property
    def truncate_ties(self) -> typing.Optional[bool]:
        r"""
        Is true when imbrication truncates ties.

        ..  container:: example

            Truncates ties:

            >>> template = baca.TwoVoiceStaffScoreTemplate()
            >>> accumulator = baca.Accumulator(template)

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> accumulator(
            ...     "Music_Voice_Two",
            ...     collections,
            ...     baca.figure([5], 32),
            ...     rmakers.beam(),
            ...     baca.imbricate(
            ...         "Music_Voice_One",
            ...         [2, 10, 18, 19, 9],
            ...         rmakers.beam_groups(beam_rests=True),
            ...         truncate_ties=True,
            ...     ),
            ... )

            >>> maker = baca.SegmentMaker(
            ...     score_template=template,
            ...     spacing=baca.minimum_duration((1, 32)),
            ...     time_signatures=accumulator.time_signatures,
            ... )
            >>> accumulator.populate_segment_maker(maker)
            >>> lilypond_file = maker.run(environment="docs")
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                <BLANKLINE>
                \context Score = "Score"                                                                 %! baca.TwoVoiceStaffScoreTemplate.__call__
                <<                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                    \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                    <<                                                                                   %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                        \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                        {                                                                                %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                            % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \baca-new-spacing-section #1 #32                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 45/32                                                                  %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            s1 * 45/32                                                                   %! baca.SegmentMaker._make_global_skips(1)
                            \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                            \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                            \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                            \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                            s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                            \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                            \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                <BLANKLINE>
                        }                                                                                %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                    >>                                                                                   %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                    \context MusicContext = "Music_Context"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                    <<                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                        \context MusicStaff = "Music_Staff"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                        <<                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                            \context MusicVoiceOne = "Music_Voice_One"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                            {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                                {
                                    \override TupletBracket.stencil = ##f
                                    \override TupletNumber.stencil = ##f
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [Music_Voice_One measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                        s8
                                        [
                <BLANKLINE>
                                        s32
                <BLANKLINE>
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 1
                                        d'8
                <BLANKLINE>
                                        s32
                <BLANKLINE>
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 1
                                        bf'!8
                <BLANKLINE>
                                        s32
                <BLANKLINE>
                                    }
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 1
                                        fs''!8
                <BLANKLINE>
                                        s32
                <BLANKLINE>
                                        s8
                <BLANKLINE>
                                        s32
                <BLANKLINE>
                                        s8
                <BLANKLINE>
                                        s32
                <BLANKLINE>
                                        s8
                <BLANKLINE>
                                        s32
                <BLANKLINE>
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 1
                                        g''8
                <BLANKLINE>
                                        s32
                <BLANKLINE>
                                    }
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 1
                                        a'8
                <BLANKLINE>
                                        s32
                                        ]
                <BLANKLINE>
                                    }
                                    \revert TupletBracket.stencil
                                    \revert TupletNumber.stencil
                <BLANKLINE>
                                }
                <BLANKLINE>
                                <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                    \context Voice = "Music_Voice_One"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                        % [Music_Voice_One measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                        \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                        c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                    \context Voice = "Rest_Voice_One"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                        % [Rest_Voice_One measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                        \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                        \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                        \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                            }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                            \context MusicVoiceTwo = "Music_Voice_Two"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                            {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                                {
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [Music_Voice_Two measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                        c'8
                                        ~
                                        [
                <BLANKLINE>
                                        c'32
                <BLANKLINE>
                                        d'8
                                        ~
                <BLANKLINE>
                                        d'32
                <BLANKLINE>
                                        bf'!8
                                        ~
                <BLANKLINE>
                                        bf'!32
                                        ]
                <BLANKLINE>
                                    }
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        fs''!8
                                        ~
                                        [
                <BLANKLINE>
                                        fs''!32
                <BLANKLINE>
                                        e''8
                                        ~
                <BLANKLINE>
                                        e''32
                <BLANKLINE>
                                        ef''!8
                                        ~
                <BLANKLINE>
                                        ef''!32
                <BLANKLINE>
                                        af''!8
                                        ~
                <BLANKLINE>
                                        af''!32
                <BLANKLINE>
                                        g''8
                                        ~
                <BLANKLINE>
                                        g''32
                                        ]
                <BLANKLINE>
                                    }
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        a'8
                                        ~
                                        [
                <BLANKLINE>
                                        a'32
                                        ]
                <BLANKLINE>
                                    }
                <BLANKLINE>
                                }
                <BLANKLINE>
                                <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                    \context Voice = "Music_Voice_Two"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                        % [Music_Voice_Two measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                        \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                        c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                    \context Voice = "Rest_Voice_Two"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                        % [Rest_Voice_Two measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                        \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                        \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                        \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                            }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                        >>                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                    >>                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                <BLANKLINE>
                >>                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__

        """
        return self._truncate_ties

    @property
    def voice_name(self) -> str:
        """
        Gets voice name.
        """
        return self._voice_name


class Accumulator(object):
    """
    Accumulator.

    ..  container:: example exception

        Raises exception on duplicate figure name.

        >>> template = baca.StringTrioScoreTemplate()
        >>> accumulator = baca.Accumulator(template)

        >>> commands = [
        ...     baca.figure([1], 16, signature=16),
        ...     rmakers.beam(),
        ... ]

        >>> accumulator(
        ...     'Violin_Music_Voice',
        ...     [[0, 1, 2, 3]],
        ...     *commands,
        ...     figure_name='D',
        ... )

        >>> accumulator(
        ...     'Violin_Music_Voice',
        ...     [[4, 5, 6, 7]],
        ...     *commands,
        ...     figure_name='D',
        ... )
        Traceback (most recent call last):
            ...
        Exception: duplicate figure name: 'D'.

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_current_offset",
        "_figure_index",
        "_figure_names",
        "_floating_selections",
        "_music_maker",
        "_score_stop_offset",
        "_score_template",
        "_time_signatures",
        "_voice_names",
    )

    ### INITIALIZER ###

    def __init__(self, score_template: abjad.ScoreTemplate) -> None:
        self._score_template = score_template
        voice_names = []
        dummy_score = score_template()
        for voice in abjad.iterate(dummy_score).components(abjad.Voice):
            voice_names.append(voice.name)
        self._voice_names = voice_names
        self._current_offset = abjad.Offset(0)
        self._figure_index = 0
        self._figure_names: typing.List[str] = []
        self._floating_selections = self._make_voice_dictionary()
        self._score_stop_offset = abjad.Offset(0)
        self._time_signatures: typing.List[abjad.TimeSignature] = []

    ### SPECIAL METHODS ###

    def __call__(
        self,
        voice_name: str,
        collections: typing.Sequence,
        *commands,
        anchor: Anchor = None,
        figure_name: str = None,
        hide_time_signature: bool = None,
        signature: int = None,
    ) -> None:
        r"""
        Calls music-accumulator.

        :param voice_name: voice name.

        :param collections: collections.

        :param anchor: anchor.

        :param figure_name: figure name.

        :param hide_time_signature: hide time signature.

        :param signature: signature
        """
        voice_name = self._abbreviation(voice_name)
        self._check_collections(collections)
        commands_ = list(commands)
        for command in commands_:
            if isinstance(command, Imbrication):
                voice_name_ = self._abbreviation(command.voice_name)
                command._voice_name = voice_name_
        command = None
        maker = None
        selection: typing.Union[list, abjad.Selection]
        selections: typing.Union[list, abjad.Selection]
        if anchor is not None:
            voice_name_ = self._abbreviation(anchor.remote_voice_name)
            anchor._remote_voice_name = voice_name_
        if isinstance(collections, str):
            tuplet = abjad.Tuplet((1, 1), collections, hide=True)
            selections = [abjad.select(tuplet)]
        elif all(isinstance(_, abjad.Component) for _ in collections):
            tuplet = abjad.Tuplet((1, 1), collections, hide=True)
            selections = [abjad.select(tuplet)]
        elif isinstance(commands[0], FigureMaker):
            maker = commands[0]
            selections = maker(collections)
            selections = abjad.select(selections).flatten()
            commands_ = list(commands[1:])
        else:
            assert isinstance(commands[0], Bind)
            command = commands[0]
            selections = commands[0](collections)
            selections = abjad.select(selections).flatten()
            commands_ = list(commands[1:])
        container = abjad.Container(selections)
        imbricated_selections = {}
        for command_ in commands_:
            if isinstance(command_, Imbrication):
                imbricated_selections.update(command_(container))
            else:
                command_(selections)
        if figure_name is not None:
            figure_name = str(figure_name)
            self._label_figure_name_(container, figure_name)
        selection = abjad.select([container])
        duration = abjad.inspect(selection).duration()
        if signature is None and maker:
            signature = maker.signature
        if signature is None and command:
            primary_maker = command.assignments[0].maker
            signature = primary_maker.signature
        if signature is not None:
            duration = duration.with_denominator(signature)
        time_signature = abjad.TimeSignature(duration)
        assert isinstance(selection, abjad.Selection)
        voice_to_selection = {voice_name: selection}
        voice_to_selection.update(imbricated_selections)
        for value in voice_to_selection.values():
            assert isinstance(value, abjad.Selection), repr(value)
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
        self._figure_index += 1

    ### PRIVATE METHODS ###

    def _abbreviation(self, voice_name):
        return self.score_template.voice_abbreviations.get(
            voice_name, voice_name
        )

    def _cache_figure_name(self, contribution):
        if contribution.figure_name is None:
            return
        if contribution.figure_name in self._figure_names:
            name = contribution.figure_name
            raise Exception(f"duplicate figure name: {name!r}.")
        self._figure_names.append(contribution.figure_name)

    def _cache_floating_selection(self, contribution):
        for voice_name in contribution:
            voice_name = self.score_template.voice_abbreviations.get(
                voice_name, voice_name
            )
            selection = contribution[voice_name]
            if not selection:
                continue
            start_offset = self._get_start_offset(selection, contribution)
            stop_offset = start_offset + abjad.inspect(selection).duration()
            timespan = abjad.Timespan(start_offset, stop_offset)
            floating_selection = abjad.AnnotatedTimespan(
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
            or (
                contribution.anchor
                and contribution.anchor.remote_voice_name is None
            )
        ):
            self.time_signatures.append(contribution.time_signature)

    @staticmethod
    def _check_collections(collections):
        prototype = (
            list,
            str,
            abjad.Segment,
            abjad.Sequence,
            abjad.Set,
            pitchclasses.CollectionList,
        )
        if not isinstance(collections, prototype):
            message = "collections must be coerceable:\n"
            message += f"   {format(collections)}"
            raise Exception(collections)

    def _get_figure_start_offset(self, figure_name):
        for voice_name in sorted(self._floating_selections.keys()):
            for floating_selection in self._floating_selections[voice_name]:
                leaf_start_offset = floating_selection.start_offset
                leaves = abjad.iterate(floating_selection.annotation).leaves()
                for leaf in leaves:
                    markup = abjad.inspect(leaf).indicators(abjad.Markup)
                    for markup_ in markup:
                        if isinstance(
                            markup_._annotation, str
                        ) and markup_._annotation.startswith("figure name: "):
                            figure_name_ = markup_._annotation
                            figure_name_ = figure_name_.replace(
                                "figure name: ", ""
                            )
                            if figure_name_ == figure_name:
                                return leaf_start_offset
                    leaf_duration = abjad.inspect(leaf).duration()
                    leaf_start_offset += leaf_duration
        raise Exception(f"can not find figure {figure_name!r}.")

    def _get_leaf_timespan(self, leaf, floating_selections):
        found_leaf = False
        for floating_selection in floating_selections:
            leaf_start_offset = abjad.Offset(0)
            for leaf_ in abjad.iterate(floating_selection.annotation).leaves():
                leaf_duration = abjad.inspect(leaf_).duration()
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
        remote_selector = remote_selector or classes.Expression().select().leaf(
            0
        )
        floating_selections = self._floating_selections[remote_voice_name]
        selections = [_.annotation for _ in floating_selections]
        result = remote_selector(selections)
        selected_leaves = list(abjad.iterate(result).leaves())
        first_selected_leaf = selected_leaves[0]
        timespan = self._get_leaf_timespan(
            first_selected_leaf, floating_selections
        )
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
            selected_leaves = list(abjad.iterate(result).leaves())
            first_selected_leaf = selected_leaves[0]
            dummy_container = abjad.Container(selection)
            timespan = abjad.inspect(first_selected_leaf).timespan()
            del dummy_container[:]
            local_anchor_offset = timespan.start_offset
        start_offset = remote_anchor_offset - local_anchor_offset
        return start_offset

    @staticmethod
    def _insert_skips(floating_selections, voice_name):
        for floating_selection in floating_selections:
            assert isinstance(floating_selection, abjad.AnnotatedTimespan)
        floating_selections = list(floating_selections)
        floating_selections.sort()
        try:
            first_start_offset = floating_selections[0].start_offset
        except:
            raise Exception(floating_selections, voice_name)
        timespans = abjad.TimespanList(floating_selections)
        gaps = ~timespans
        if 0 < first_start_offset:
            first_gap = abjad.Timespan(0, first_start_offset)
            gaps.append(first_gap)
        selections = floating_selections + list(gaps)
        selections.sort()
        fused_selection = []
        for selection in selections:
            if isinstance(selection, abjad.AnnotatedTimespan):
                fused_selection.extend(selection.annotation)
            else:
                assert isinstance(selection, abjad.Timespan)
                skip = abjad.Skip(1, multiplier=selection.duration)
                fused_selection.append(skip)
        fused_selection = abjad.select(fused_selection)
        return fused_selection

    def _label_figure_name_(self, container, figure_name):
        figure_index = self._figure_index
        original_figure_name = figure_name
        parts = figure_name.split("_")
        if len(parts) == 1:
            body = parts[0]
            figure_name = abjad.Markup(body)
        elif len(parts) == 2:
            body, subscript = parts
            figure_name = abjad.Markup.concat(
                [abjad.Markup(body), abjad.Markup(subscript).sub()]
            )
        else:
            raise Exception(f"unrecognized figure name: {figure_name!r}.")
        figure_index = f" ({figure_index})"
        figure_index = abjad.Markup(figure_index).fontsize(-2).raise_(0.25)
        figure_name_markup = abjad.Markup.concat(
            ["[", figure_name, abjad.Markup.hspace(1), figure_index, "]"]
        )
        figure_name_markup = figure_name_markup.fontsize(2)
        figure_name_markup = abjad.Markup(
            figure_name_markup, direction=abjad.Up
        )
        annotation = f"figure name: {original_figure_name}"
        figure_name_markup._annotation = annotation
        leaf = abjad.select(container).leaf(0)
        abjad.attach(
            figure_name_markup,
            leaf,
            deactivate=True,
            tag=abjad.const.FIGURE_NAME,
        )

    def _make_voice_dictionary(self):
        return dict([(_, []) for _ in self._voice_names])

    ### PUBLIC PROPERTIES ###

    @property
    def score_template(self) -> abjad.ScoreTemplate:
        """
        Gets score template.
        """
        return self._score_template

    @property
    def time_signatures(self) -> typing.List[abjad.TimeSignature]:
        """
        Gets time signatures.
        """
        return self._time_signatures

    ### PUBLIC METHODS ###

    def assemble(self, voice_name) -> typing.Optional[abjad.Selection]:
        """
        Assembles complete selection for ``voice_name``.
        """
        floating_selections = self._floating_selections[voice_name]
        if not floating_selections:
            return None
        selection = self._insert_skips(floating_selections, voice_name)
        assert isinstance(selection, abjad.Selection), repr(selection)
        return selection

    def populate_segment_maker(self, segment_maker) -> None:
        """
        Populates ``segment_maker``.
        """
        for voice_name in sorted(self._floating_selections):
            selection = self.assemble(voice_name)
            if not selection:
                continue
            segment_maker(
                (voice_name, 1),
                rhythmcommands.music(
                    selection, do_not_check_total_duration=True, tag=None
                ),
            )


class Contribution(object):
    """
    Contribution.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_anchor",
        "_figure_name",
        "_hide_time_signature",
        "_tag",
        "_time_signature",
        "_voice_to_selection",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        voice_to_selection: typing.Dict[str, abjad.Selection],
        *,
        anchor: Anchor = None,
        figure_name: str = None,
        hide_time_signature: bool = None,
        time_signature: abjad.TimeSignature = None,
    ):
        assert isinstance(voice_to_selection, dict), repr(voice_to_selection)
        self._voice_to_selection = voice_to_selection
        if anchor is not None and not isinstance(anchor, Anchor):
            raise TypeError(f"anchor only: {anchor!r}.")
        self._anchor = anchor
        if figure_name is not None:
            figure_name = str(figure_name)
        self._figure_name = figure_name
        if hide_time_signature is not None:
            hide_time_signature = bool(hide_time_signature)
        self._hide_time_signature = hide_time_signature
        if time_signature is not None:
            assert isinstance(time_signature, abjad.TimeSignature)
        self._time_signature = time_signature

    ### SPECIAL METHODS ###

    def __getitem__(self, voice_name) -> abjad.Selection:
        """
        Gets ``voice_name`` selection list.
        """
        return self.voice_to_selection.__getitem__(voice_name)

    def __iter__(self) -> typing.Generator:
        """
        Iterates figure contribution.
        """
        for voice_name in self.voice_to_selection:
            yield voice_name

    def __repr__(self) -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def anchor(self) -> typing.Optional[Anchor]:
        """
        Gets anchor.
        """
        return self._anchor

    @property
    def figure_name(self) -> typing.Optional[str]:
        """
        Gets figure name.
        """
        return self._figure_name

    @property
    def hide_time_signature(self) -> typing.Optional[bool]:
        """
        Is true when contribution hides time signature.
        """
        return self._hide_time_signature

    @property
    def time_signature(self) -> typing.Optional[abjad.TimeSignature]:
        """
        Gets time signature.
        """
        return self._time_signature

    @property
    def voice_to_selection(self) -> typing.Dict[str, abjad.Selection]:
        """
        Gets voice-to-selection dictionary.
        """
        if self._voice_to_selection is not None:
            assert isinstance(self._voice_to_selection, dict), repr(
                self.voice_to_selection
            )
            for value in self._voice_to_selection.values():
                assert isinstance(value, abjad.Selection), repr(value)
        return self._voice_to_selection


class Nest(object):
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 3/4
                    s1 * 3/4
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 12/11 {
                        \scaleDurations #'(1 . 1) {
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
                        \scaleDurations #'(1 . 1) {
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
                        \scaleDurations #'(1 . 1) {
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

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_lmr", "_treatments")

    ### INITIALIZER ###

    def __init__(
        self,
        treatments: typing.Sequence[typing.Union[int, str]],
        *,
        lmr: LMR = None,
    ) -> None:
        assert isinstance(treatments, (list, tuple))
        is_treatment = FigureMaker._is_treatment
        for treatment in treatments:
            assert is_treatment(treatment), repr(treatment)
        self._treatments = treatments
        if lmr is not None:
            assert isinstance(lmr, LMR), repr(lmr)
        self._lmr = lmr

    ### SPECIAL METHODS ###

    def __call__(self, selection: abjad.Selection) -> abjad.Selection:
        r"""
        Calls nesting command on ``selection``.

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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 17/16
                        s1 * 17/16
                    }
                    \new Staff
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 17/16 {
                            \scaleDurations #'(1 . 1) {
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
                            \scaleDurations #'(1 . 1) {
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
                            \scaleDurations #'(1 . 1) {
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
        treatments = self._get_treatments()
        assert treatments is not None
        tuplets = []
        for item in selection:
            if isinstance(item, abjad.Tuplet):
                tuplets.append(item)
            else:
                assert isinstance(item, abjad.Selection), repr(item)
                assert len(item) == 1, repr(item)
                assert isinstance(item[0], abjad.Tuplet), repr(item)
                tuplet = item[0]
                tuplets.append(tuplet)
        if self.lmr is None:
            tuplet_selections = [abjad.select(tuplets)]
        else:
            tuplet_selections = self.lmr(tuplets)
            tuplet_selections = [
                abjad.select(list(_)) for _ in tuplet_selections
            ]
        tuplets = []
        for i, tuplet_selection in enumerate(tuplet_selections):
            assert isinstance(tuplet_selection, abjad.Selection)
            treatment = treatments[i]
            if treatment is None:
                tuplets.extend(tuplet_selection)
            else:
                nested_tuplet = self._make_nested_tuplet(
                    tuplet_selection, treatment
                )
                tuplets.append(nested_tuplet)
        selection = abjad.select(tuplets)
        return selection

    def __eq__(self, argument) -> bool:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __format__(self, format_specification="") -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __hash__(self) -> int:
        """
        Delegates to format manager.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_treatments(self):
        if self.treatments:
            return abjad.CyclicTuple(self.treatments)

    @staticmethod
    def _make_nested_tuplet(tuplet_selection, treatment):
        assert isinstance(tuplet_selection, abjad.Selection)
        for tuplet in tuplet_selection:
            assert isinstance(tuplet, abjad.Tuplet), repr(tuplet)
        if isinstance(treatment, str):
            addendum = abjad.Duration(treatment)
            contents_duration = abjad.inspect(tuplet_selection).duration()
            target_duration = contents_duration + addendum
            multiplier = target_duration / contents_duration
            tuplet = abjad.Tuplet(multiplier, [])
            abjad.mutate(tuplet_selection).wrap(tuplet)
        elif treatment.__class__ is abjad.Multiplier:
            tuplet = abjad.Tuplet(treatment, [])
            abjad.mutate(tuplet_selection).wrap(tuplet)
        elif treatment.__class__ is abjad.Duration:
            target_duration = treatment
            contents_duration = abjad.inspect(tuplet_selection).duration()
            multiplier = target_duration / contents_duration
            tuplet = abjad.Tuplet(multiplier, [])
            abjad.mutate(tuplet_selection).wrap(tuplet)
        else:
            raise Exception(f"bad time treatment: {treatment!r}.")
        return tuplet

    ### PUBLIC PROPERTIES ###

    @property
    def lmr(self) -> typing.Optional[LMR]:
        """
        Gets LMR.
        """
        return self._lmr

    @property
    def treatments(self) -> typing.Optional[typing.Sequence]:
        """
        Gets treatments.
        """
        return self._treatments


class RestAffix(object):
    r"""
    Rest affix.

    ..  container:: example

        >>> baca.RestAffix()
        RestAffix()

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_pattern", "_prefix", "_skips_instead_of_rests", "_suffix")

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        pattern: abjad.Pattern = None,
        prefix: typing.Sequence[int] = None,
        skips_instead_of_rests: bool = None,
        suffix: typing.Sequence[int] = None,
    ):
        if pattern is not None and not isinstance(pattern, abjad.Pattern):
            raise TypeError(f"pattern or none: {pattern!r}.")
        self._pattern = pattern
        if prefix is not None:
            assert all(isinstance(_, int) for _ in prefix)
        self._prefix = prefix
        if skips_instead_of_rests is not None:
            skips_instead_of_rests = bool(skips_instead_of_rests)
        self._skips_instead_of_rests = skips_instead_of_rests
        if suffix is not None:
            assert all(isinstance(_, int) for _ in suffix)
        self._suffix = suffix

    ### SPECIAL METHODS ###

    def __call__(
        self, collection_index: int, total_collections: int
    ) -> typing.Tuple[
        typing.Optional[abjad.IntegerSequence],
        typing.Optional[abjad.IntegerSequence],
    ]:
        r"""
        Calls rest affix.

        :param collection_index: collection index.

        :param total_collections: total collections.
        """
        if self.pattern is None:
            if (
                collection_index == 0
                and collection_index == total_collections - 1
            ):
                return self.prefix, self.suffix
            if collection_index == 0:
                return self.prefix, None
            if collection_index == total_collections - 1:
                return None, self.suffix
        elif self.pattern.matches_index(collection_index, total_collections):
            return self.prefix, self.suffix
        return None, None

    def __eq__(self, argument) -> bool:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __format__(self, format_specification="") -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __hash__(self) -> int:
        """
        Delegates to format manager.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def pattern(self) -> typing.Optional[abjad.Pattern]:
        r"""
        Gets pattern.

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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 15/16
                        s1 * 15/16
                    }
                    \new Staff
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            r16
                            c'16
                            [
                            d'16
                            bf'16
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/5 {
                            fs''16
                            [
                            e''16
                            ef''16
                            af''16
                            g''16
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 4/3 {
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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 9/16
                        s1 * 9/16
                    }
                    \new Staff
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/8 {
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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 9/8
                        s1 * 9/8
                    }
                    \new Staff
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            r16
                            c'16
                            [
                            d'16
                            bf'16
                            ]
                            r8
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/5 {
                            fs''16
                            [
                            e''16
                            ef''16
                            af''16
                            g''16
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 21/16
                        s1 * 21/16
                    }
                    \new Staff
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            r16
                            c'16
                            [
                            d'16
                            bf'16
                            ]
                            r8
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/8 {
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
                        \times 5/4 {
                            r16
                            a'16
                            r8
                        }
                    }
                >>

        """
        return self._pattern

    @property
    def prefix(self) -> typing.Optional[abjad.IntegerSequence]:
        r"""
        Gets prefix.

        ..  container:: example

            >>> affix = baca.RestAffix(prefix=[3])
            >>> stack = baca.stack(
            ...     baca.figure([1], 16, affix=affix),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selection = stack(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 3/4
                        s1 * 3/4
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            r8.
                            c'16
                            [
                            d'16
                            bf'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''16
                            [
                            e''16
                            ef''16
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'16
                        }
                    }
                >>

        """
        return self._prefix

    @property
    def skips_instead_of_rests(self) -> typing.Optional[bool]:
        """
        Is true when command affixes skips instead of rests.
        """
        return self._skips_instead_of_rests

    @property
    def suffix(self) -> typing.Optional[abjad.IntegerSequence]:
        r"""
        Gets suffix.

        ..  container:: example

            >>> affix = baca.RestAffix(suffix=[3])
            >>> stack = baca.stack(
            ...     baca.figure([1], 16, affix=affix),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selection = stack(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 3/4
                        s1 * 3/4
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            d'16
                            bf'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''16
                            [
                            e''16
                            ef''16
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'16
                            r8.
                        }
                    }
                >>

        """
        return self._suffix


class FigureMaker(object):
    """
    figure-maker.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Classes"

    __slots__ = (
        "_acciaccatura",
        "_affix",
        "_next_attack",
        "_next_segment",
        "_restart_talea",
        "_signature",
        "_spelling",
        "_state",
        "_talea",
        "_treatments",
    )

    _state_variables = ("_next_attack", "_next_segment")

    ### INITIALIZER ###

    def __init__(
        self,
        talea: rmakers.Talea,
        acciaccatura: Acciaccatura = None,
        affix: RestAffix = None,
        restart_talea: bool = None,
        signature: int = None,
        spelling: rmakers.Spelling = None,
        treatments: typing.Sequence = None,
    ):
        if acciaccatura is not None:
            assert isinstance(acciaccatura, Acciaccatura), repr(acciaccatura)
        self._acciaccatura = acciaccatura
        if affix is not None:
            if not isinstance(affix, RestAffix):
                message = "must be rest affix:\n"
                message += f"   {repr(affix)}"
                raise Exception(message)
        self._affix = affix
        self._next_attack = 0
        self._next_segment = 0
        if restart_talea is not None:
            restart_talea = bool(restart_talea)
        self._restart_talea = restart_talea
        if signature is not None:
            assert isinstance(signature, int), repr(signature)
        self._signature = signature
        if spelling is not None:
            assert isinstance(spelling, rmakers.Spelling)
        self._spelling = spelling
        self._state = abjad.OrderedDict()
        if not isinstance(talea, rmakers.Talea):
            raise TypeError(f"must be talea: {talea!r}.")
        self._talea = talea
        if treatments is not None:
            self._check_treatments(treatments)
        self._treatments = treatments

    ### SPECIAL METHODS ###

    def __call__(
        self,
        collections: typing.Sequence,
        collection_index: int = None,
        state: abjad.OrderedDict = None,
        total_collections: int = None,
    ) -> abjad.Selection:
        r"""
        Calls figure-maker.

        :param collections: collections.

        :param collection_index: collection index.

        :param state: state.

        :param total_collections: total collections.

        ..  container:: example

            Without state manifest:

            >>> stack = baca.stack(
            ...     baca.figure([1, 1, 2], 16),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections = stack(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 3/4
                        s1 * 3/4
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
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
            >>> state = {'_next_attack': 2}
            >>> selections = stack(collections, state=state)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 3/4
                        s1 * 3/4
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            c'8
                            [
                            d'16
                            bf'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''8
                            [
                            e''16
                            ef''16
                            af''8
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'16
                        }
                    }
                >>

        """
        collections = self._coerce_collections(collections)
        self._state = state or abjad.OrderedDict()
        self._apply_state(state=state)
        tuplets: typing.List[abjad.Tuplet] = []
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
        selection = abjad.select(tuplets)
        return selection

    def __eq__(self, argument) -> bool:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Delegates to format manager.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __format__(self, format_specification="") -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __repr__(self) -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    @staticmethod
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
            if not self._is_treatment(treatment):
                raise Exception(f"bad time treatment: {treatment!r}.")

    @staticmethod
    def _coerce_collections(collections) -> pitchclasses.CollectionList:
        prototype = (abjad.Segment, abjad.Set)
        if isinstance(collections, prototype):
            return pitchclasses.CollectionList(collections=[collections])
        item_class: typing.Type = abjad.NumberedPitch
        for collection in collections:
            for item in collection:
                if isinstance(item, str):
                    item_class = abjad.NamedPitch
                    break
        return pitchclasses.CollectionList(
            collections=collections, item_class=item_class
        )

    @staticmethod
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

    @staticmethod
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

    @classmethod
    def _make_accelerando(class_, leaf_selection, accelerando_indicator):
        assert accelerando_indicator in ("accel", "rit")
        tuplet = abjad.Tuplet((1, 1), leaf_selection, hide=True)
        if len(tuplet) == 1:
            return tuplet
        durations = [abjad.inspect(_).duration() for _ in leaf_selection]
        if accelerando_indicator == "accel":
            exponent = 0.625
        elif accelerando_indicator == "rit":
            exponent = 1.625
        multipliers = class_._make_accelerando_multipliers(durations, exponent)
        assert len(leaf_selection) == len(multipliers)
        for multiplier, leaf in zip(multipliers, leaf_selection):
            leaf.multiplier = multiplier
        if rmakers.FeatherBeamCommand._is_accelerando(leaf_selection):
            abjad.override(leaf_selection[0]).beam.grow_direction = abjad.Right
        elif rmakers.FeatherBeamCommand._is_ritardando(leaf_selection):
            abjad.override(leaf_selection[0]).beam.grow_direction = abjad.Left
        duration = abjad.inspect(tuplet).duration()
        duration = abjad.Duration(duration)
        markup = duration.to_score_markup()
        markup = markup.scale((0.75, 0.75))
        abjad.override(tuplet).tuplet_number.text = markup
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
            ...     )
            >>> for multiplier in result: multiplier
            ...
            NonreducedFraction(2048, 1024)
            NonreducedFraction(848, 1024)
            NonreducedFraction(651, 1024)
            NonreducedFraction(549, 1024)

        Set exponent greater than 1 for ritardando.

        Set exponent less than 1 for accelerando.
        """
        pairs = abjad.mathtools.cumulative_sums_pairwise(durations)
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
        durations_ = abjad.mathtools.difference_series(start_offsets_)
        durations_ = rhythm_maker_class._round_durations(durations_, 2 ** 10)
        durations_ = class_._fix_rounding_error(durations_, total_duration)
        multipliers = []
        assert len(durations) == len(durations_)
        for duration_, duration in zip(durations_, durations):
            multiplier = duration_ / duration
            multiplier = abjad.Multiplier(multiplier)
            multiplier = multiplier.with_denominator(2 ** 10)
            multipliers.append(multiplier)
        return multipliers

    def _make_music(
        self, collections, collection_index=None, total_collections=None
    ) -> typing.List[abjad.Tuplet]:
        segment_count = len(collections)
        tuplets = []
        if collection_index is None:
            for i, segment in enumerate(collections):
                if self.affix is not None:
                    result = self.affix(i, segment_count)
                    rest_prefix, rest_suffix = result
                    affix_skips_instead_of_rests = (
                        self.affix.skips_instead_of_rests
                    )
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
                affix_skips_instead_of_rests = (
                    self.affix.skips_instead_of_rests
                )
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
        collection_index = self._next_segment
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
            if isinstance(segment, (set, abjad.Set)):
                message = "decide how to model chords with acciaccatura."
                raise NotImplementError(message)
            before_grace_containers, segment = self.acciaccatura(segment)
            assert len(before_grace_containers) == len(segment)
        if isinstance(segment, (set, abjad.Set)):
            segment = [segment]
        for pitch_expression in segment:
            is_chord = False
            if isinstance(pitch_expression, (set, abjad.Set)):
                is_chord = True
            prototype = abjad.NumberedPitchClass
            if isinstance(pitch_expression, prototype):
                pitch_expression = pitch_expression.number
            count = self._next_attack
            while talea[count] < 0:
                self._next_attack += 1
                duration = -talea[count]
                maker = abjad.LeafMaker(
                    increase_monotonic=spelling.increase_monotonic
                )
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
                maker = abjad.LeafMaker(
                    increase_monotonic=spelling.increase_monotonic
                )
                leaves_ = maker([None], [duration])
                leaves.extend(leaves_)
                count = self._next_attack
        leaves = self._add_rest_affixes(
            leaves,
            talea,
            rest_prefix,
            rest_suffix,
            affix_skips_instead_of_rests,
            spelling.increase_monotonic,
        )
        leaf_selection = abjad.select(leaves)
        if isinstance(treatment, int):
            tuplet = self._make_tuplet_with_extra_count(
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
            contents_duration = abjad.inspect(leaf_selection).duration()
            multiplier = tuplet_duration / contents_duration
            tuplet = abjad.Tuplet(multiplier, leaf_selection)
            if not tuplet.multiplier.normalized():
                tuplet.normalize_multiplier()
        elif isinstance(treatment, tuple) and len(treatment) == 2:
            tuplet_duration = abjad.Duration(treatment)
            contents_duration = abjad.inspect(leaf_selection).duration()
            multiplier = tuplet_duration / contents_duration
            tuplet = abjad.Tuplet(multiplier, leaf_selection)
            if not tuplet.multiplier.normalized():
                tuplet.normalize_multiplier()
        else:
            raise Exception(f"bad time treatment: {treatment!r}.")
        assert isinstance(tuplet, abjad.Tuplet)
        if before_grace_containers is not None:
            logical_ties = abjad.iterate(tuplet).logical_ties()
            pairs = zip(before_grace_containers, logical_ties)
            for before_grace_container, logical_tie in pairs:
                if before_grace_container is None:
                    continue
                abjad.attach(
                    before_grace_container, logical_tie.head, tag="PFRM_1"
                )
        if tuplet.trivial():
            tuplet.hide = True
        assert isinstance(tuplet, abjad.Tuplet), repr(tuplet)
        return tuplet

    @staticmethod
    def _make_tuplet_with_extra_count(
        leaf_selection, extra_count, denominator
    ):
        contents_duration = abjad.inspect(leaf_selection).duration()
        contents_duration = contents_duration.with_denominator(denominator)
        contents_count = contents_duration.numerator
        if 0 < extra_count:
            extra_count %= contents_count
        elif extra_count < 0:
            extra_count = abs(extra_count)
            extra_count %= math.ceil(contents_count / 2.0)
            extra_count *= -1
        new_contents_count = contents_count + extra_count
        tuplet_multiplier = abjad.Multiplier(
            new_contents_count, contents_count
        )
        if not tuplet_multiplier.normalized():
            message = f"{leaf_selection!r} gives {tuplet_multiplier}"
            message += " with {contents_count} and {new_contents_count}."
            raise Exception(message)
        tuplet = abjad.Tuplet(tuplet_multiplier, leaf_selection)
        return tuplet

    @staticmethod
    def _normalize_multiplier(multiplier):
        assert 0 < multiplier, repr(multiplier)
        while multiplier <= abjad.Multiplier(1, 2):
            multiplier *= 2
        while abjad.Multiplier(2) <= multiplier:
            multiplier /= 2
        return multiplier

    ### PUBLIC PROPERTIES ###

    @property
    def acciaccatura(self) -> typing.Optional[Acciaccatura]:
        r"""
        Gets acciaccatura.

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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                }
                <<
                    \new GlobalContext
                    {
                        \time 3/4
                        s1 * 3/4
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16
                                [                                                                        %! Acciaccatura
                                e''16
                                ]                                                                        %! Acciaccatura
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! Acciaccatura
                                g''16
                                a'16
                                ]                                                                        %! Acciaccatura
                            }
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                                [                                                                        %! Acciaccatura
                                bf'16
                                fs''16
                                e''16
                                ]                                                                        %! Acciaccatura
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! Acciaccatura
                                g''16
                                a'16
                                c'16
                                d'16
                                ]                                                                        %! Acciaccatura
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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                }
                <<
                    \new GlobalContext
                    {
                        \time 3/2
                        s1 * 3/2
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            c'4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16
                                [                                                                        %! Acciaccatura
                                e''16
                                ]                                                                        %! Acciaccatura
                            }
                            ef''4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! Acciaccatura
                                g''16
                                a'16
                                ]                                                                        %! Acciaccatura
                            }
                            c'4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                                [                                                                        %! Acciaccatura
                                bf'16
                                fs''16
                                e''16
                                ]                                                                        %! Acciaccatura
                            }
                            ef''4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! Acciaccatura
                                g''16
                                a'16
                                c'16
                                d'16
                                ]                                                                        %! Acciaccatura
                            }
                            bf'4
                        }
                    }
                >>

        """
        return self._acciaccatura

    @property
    def affix(self) -> typing.Optional["RestAffix"]:
        """
        Gets affix.
        """
        return self._affix

    @property
    def restart_talea(self) -> typing.Optional[bool]:
        r"""
        Is true when maker restarts talea for each collection.
        """
        return self._restart_talea

    @property
    def signature(self) -> typing.Optional[int]:
        r"""
        Gets (time) signature (denominator).
        """
        return self._signature

    @property
    def spelling(self) -> typing.Optional[rmakers.Spelling]:
        r"""
        Gets spelling.

        ..  container:: example

            Spells nonassignable durations with monontonically decreasing
            durations by default:

            >>> stack = baca.stack(
            ...     baca.figure([4, 4, 5], 32),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections = stack(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 39/32
                        s1 * 39/32
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            c'8
                            [
                            d'8
                            bf'8
                            ~
                            bf'32
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
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
                        \scaleDurations #'(1 . 1) {
                            a'8
                            ~
                            [
                            a'32
                            ]
                        }
                    }
                >>

        ..  container:: example

            Spells nonassignable durations with monontonically increasing
            durations:

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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 39/32
                        s1 * 39/32
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            c'8
                            [
                            d'8
                            bf'32
                            ~
                            bf'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
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
                        \scaleDurations #'(1 . 1) {
                            a'32
                            ~
                            [
                            a'8
                            ]
                        }
                    }
                >>

        """
        return self._spelling

    @property
    def talea(self) -> rmakers.Talea:
        r"""
        Gets talea.

        ..  container:: example

            Sixteenths and eighths:

            >>> stack = baca.stack(
            ...     baca.figure([1, 1, 2], 16),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10, 8]]
            >>> selections = stack(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 5/16
                        s1 * 5/16
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 3/8
                        s1 * 3/8
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 1/16
                        s1 * 1/16
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            a'16
                        }
                    }
                >>

            >>> collections = [[0, 2, 10, 8], [18, 16, 15, 20, 19], [9]]
            >>> selections = stack(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 13/16
                        s1 * 13/16
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            d'16
                            bf'8
                            af'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''16
                            [
                            e''8
                            ef''16
                            af''16
                            g''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 3/2
                        s1 * 3/2
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            \override Staff.Stem.stemlet-length = 1.5
                            c'8.
                            [
                            r16
                            d'8
                            \revert Staff.Stem.stemlet-length
                            bf'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
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
                        \scaleDurations #'(1 . 1) {
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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 29/32
                        s1 * 29/32
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            c'4..
                            c'64
                            \repeatTie
                            d'4..
                            d'64
                            \repeatTie
                        }
                    }
                >>

        """
        return self._talea

    @property
    def treatments(
        self
    ) -> typing.Optional[
        typing.Sequence[typing.Union[int, str, abjad.Duration]]
    ]:
        r"""
        Gets treatments.

        ..  container:: example

            One extra count per division:

            >>> stack = baca.stack(
            ...     baca.figure([1, 1, 2], 16, treatments=[1]),
            ...     rmakers.beam(),
            ... )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections = stack(collections)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 15/16
                        s1 * 15/16
                    }
                    \new Staff
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 5/8
                        s1 * 5/8
                    }
                    \new Staff
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/6 {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 21/16
                        s1 * 21/16
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            c'16
                        }
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score
                                        \with
                                        {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        }
                                        <<
                                            \new RhythmicStaff
                                            \with
                                            {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.minimum-length = #4
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                                \override TupletNumber.font-size = #0
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            }
                                            {
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \scaleDurations #'(1 . 1) {
                            \once \override Beam.grow-direction = #right
                            d'16 * 1328/1024
                            [
                            bf'16 * 720/1024
                            ]
                        }
                        \revert TupletNumber.text
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score
                                        \with
                                        {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        }
                                        <<
                                            \new RhythmicStaff
                                            \with
                                            {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.minimum-length = #4
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                                \override TupletNumber.font-size = #0
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            }
                                            {
                                                c'8.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \scaleDurations #'(1 . 1) {
                            \once \override Beam.grow-direction = #right
                            fs''16 * 1552/1024
                            [
                            e''16 * 832/1024
                            ef''16 * 688/1024
                            ]
                        }
                        \revert TupletNumber.text
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score
                                        \with
                                        {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        }
                                        <<
                                            \new RhythmicStaff
                                            \with
                                            {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.minimum-length = #4
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                                \override TupletNumber.font-size = #0
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            }
                                            {
                                                c'4
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \scaleDurations #'(1 . 1) {
                            \once \override Beam.grow-direction = #right
                            af''16 * 1728/1024
                            [
                            g''16 * 928/1024
                            a'16 * 768/1024
                            c'16 * 672/1024
                            ]
                        }
                        \revert TupletNumber.text
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score
                                        \with
                                        {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        }
                                        <<
                                            \new RhythmicStaff
                                            \with
                                            {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.minimum-length = #4
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                                \override TupletNumber.font-size = #0
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            }
                                            {
                                                c'4
                                                ~
                                                c'16
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \scaleDurations #'(1 . 1) {
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
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score
                                        \with
                                        {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        }
                                        <<
                                            \new RhythmicStaff
                                            \with
                                            {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.minimum-length = #4
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                                \override TupletNumber.font-size = #0
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            }
                                            {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \scaleDurations #'(1 . 1) {
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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 21/16
                        s1 * 21/16
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            c'16
                        }
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score
                                        \with
                                        {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        }
                                        <<
                                            \new RhythmicStaff
                                            \with
                                            {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.minimum-length = #4
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                                \override TupletNumber.font-size = #0
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            }
                                            {
                                                c'8
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \scaleDurations #'(1 . 1) {
                            \once \override Beam.grow-direction = #left
                            d'16 * 656/1024
                            [
                            bf'16 * 1392/1024
                            ]
                        }
                        \revert TupletNumber.text
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score
                                        \with
                                        {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        }
                                        <<
                                            \new RhythmicStaff
                                            \with
                                            {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.minimum-length = #4
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                                \override TupletNumber.font-size = #0
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            }
                                            {
                                                c'8.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \scaleDurations #'(1 . 1) {
                            \once \override Beam.grow-direction = #left
                            fs''16 * 512/1024
                            [
                            e''16 * 1072/1024
                            ef''16 * 1488/1024
                            ]
                        }
                        \revert TupletNumber.text
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score
                                        \with
                                        {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        }
                                        <<
                                            \new RhythmicStaff
                                            \with
                                            {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.minimum-length = #4
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                                \override TupletNumber.font-size = #0
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            }
                                            {
                                                c'4
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \scaleDurations #'(1 . 1) {
                            \once \override Beam.grow-direction = #left
                            af''16 * 432/1024
                            [
                            g''16 * 896/1024
                            a'16 * 1232/1024
                            c'16 * 1536/1024
                            ]
                        }
                        \revert TupletNumber.text
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score
                                        \with
                                        {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        }
                                        <<
                                            \new RhythmicStaff
                                            \with
                                            {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.minimum-length = #4
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                                \override TupletNumber.font-size = #0
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            }
                                            {
                                                c'4
                                                ~
                                                c'16
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \scaleDurations #'(1 . 1) {
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
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score
                                        \with
                                        {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        }
                                        <<
                                            \new RhythmicStaff
                                            \with
                                            {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.minimum-length = #4
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                                \override TupletNumber.font-size = #0
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            }
                                            {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \scaleDurations #'(1 . 1) {
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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 11/8
                        s1 * 11/8
                    }
                    \new Staff
                    {
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score
                                        \with
                                        {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        }
                                        <<
                                            \new RhythmicStaff
                                            \with
                                            {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.minimum-length = #4
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                                \override TupletNumber.font-size = #0
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            }
                                            {
                                                c'4
                                                ~
                                                c'16
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \scaleDurations #'(1 . 1) {
                            \once \override Beam.grow-direction = #right
                            c'16 * 1872/1024
                            [
                            d'16 * 1008/1024
                            bf'16 * 832/1024
                            fs''16 * 736/1024
                            e''16 * 672/1024
                            ]
                        }
                        \revert TupletNumber.text
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score
                                        \with
                                        {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        }
                                        <<
                                            \new RhythmicStaff
                                            \with
                                            {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.minimum-length = #4
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                                \override TupletNumber.font-size = #0
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            }
                                            {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \scaleDurations #'(1 . 1) {
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
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score
                                        \with
                                        {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        }
                                        <<
                                            \new RhythmicStaff
                                            \with
                                            {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.minimum-length = #4
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                                \override TupletNumber.font-size = #0
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            }
                                            {
                                                c'4
                                                ~
                                                c'16
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \scaleDurations #'(1 . 1) {
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
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score
                                        \with
                                        {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        }
                                        <<
                                            \new RhythmicStaff
                                            \with
                                            {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.minimum-length = #4
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                                \override TupletNumber.font-size = #0
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            }
                                            {
                                                c'4.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \scaleDurations #'(1 . 1) {
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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 13/8
                        s1 * 13/8
                    }
                    \new Staff
                    {
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score
                                        \with
                                        {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        }
                                        <<
                                            \new RhythmicStaff
                                            \with
                                            {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.minimum-length = #4
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                                \override TupletNumber.font-size = #0
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            }
                                            {
                                                c'4
                                                ~
                                                c'16
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \scaleDurations #'(1 . 1) {
                            \once \override Beam.grow-direction = #right
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
                        \times 3/5 {
                            ef''16
                            [
                            af''16
                            g''16
                            a'16
                            c'16
                            ]
                        }
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score
                                        \with
                                        {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        }
                                        <<
                                            \new RhythmicStaff
                                            \with
                                            {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.minimum-length = #4
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                                \override TupletNumber.font-size = #0
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            }
                                            {
                                                c'4
                                                ~
                                                c'16
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \scaleDurations #'(1 . 1) {
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
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score
                                        \with
                                        {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        }
                                        <<
                                            \new RhythmicStaff
                                            \with
                                            {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.minimum-length = #4
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                                \override TupletNumber.font-size = #0
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            }
                                            {
                                                c'4
                                                ~
                                                c'16
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \scaleDurations #'(1 . 1) {
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
                        \times 3/5 {
                            bf'16
                            [
                            fs''16
                            e''16
                            ef''16
                            af''16
                            ]
                        }
                        \override TupletNumber.text = \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score
                                        \with
                                        {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        }
                                        <<
                                            \new RhythmicStaff
                                            \with
                                            {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.minimum-length = #4
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                                \override TupletNumber.font-size = #0
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            }
                                            {
                                                c'4
                                                ~
                                                c'16
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                        \scaleDurations #'(1 . 1) {
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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> staff = lilypond_file[abjad.Score]
            >>> abjad.override(staff).beam.positions = (-6, -6)
            >>> abjad.override(staff).stem.direction = abjad.Down
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override Beam.positions = #'(-6 . -6)
                    \override Stem.direction = #down
                }
                <<
                    \new GlobalContext
                    {
                        \time 7/4
                        s1 * 7/4
                    }
                    \new Staff
                    {
                        \tweak edge-height #'(0.7 . 0)
                        \times 2/3 {
                            c'8
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 2/3 {
                            d'8
                            [
                            bf'8
                            ]
                        }
                        \times 2/3 {
                            fs''8
                            [
                            e''8
                            ef''8
                            ]
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 2/3 {
                            af''8
                            [
                            g''8
                            a'8
                            c'8
                            ]
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 2/3 {
                            d'8
                            [
                            bf'8
                            fs''8
                            e''8
                            ef''8
                            ]
                        }
                        \times 2/3 {
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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> staff = lilypond_file[abjad.Score]
            >>> abjad.override(staff).beam.positions = (-6, -6)
            >>> abjad.override(staff).stem.direction = abjad.Down
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override Beam.positions = #'(-6 . -6)
                    \override Stem.direction = #down
                }
                <<
                    \new GlobalContext
                    {
                        \time 3/2
                        s1 * 3/2
                    }
                    \new Staff
                    {
                        \scaleDurations #'(1 . 1) {
                            c'4
                        }
                        \scaleDurations #'(1 . 1) {
                            d'8
                            [
                            bf'8
                            ]
                        }
                        \times 4/6 {
                            fs''8
                            [
                            e''8
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            af''16
                            [
                            g''16
                            a'16
                            c'16
                            ]
                        }
                        \times 4/5 {
                            d'16
                            [
                            bf'16
                            fs''16
                            e''16
                            ef''16
                            ]
                        }
                        \times 4/6 {
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

            Collection durations alternating between a quarter and a dotted
            quarter:

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
            >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
            >>> staff = lilypond_file[abjad.Score]
            >>> abjad.override(staff).beam.positions = (-6, -6)
            >>> abjad.override(staff).stem.direction = abjad.Down
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override Beam.positions = #'(-6 . -6)
                    \override Stem.direction = #down
                }
                <<
                    \new GlobalContext
                    {
                        \time 15/8
                        s1 * 15/8
                    }
                    \new Staff
                    {
                        \times 4/6 {
                            c'16
                            [
                            d'16
                            bf'8
                            fs''16
                            e''16
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            ef''8
                            [
                            af''16
                            g''16
                            a'8
                            c'16
                            ]
                        }
                        \times 4/7 {
                            d'16
                            [
                            bf'8
                            fs''16
                            e''16
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            af''16
                            [
                            g''16
                            a'8
                            c'16
                            d'16
                            ]
                        }
                        \times 4/7 {
                            bf'8
                            [
                            fs''16
                            e''16
                            ef''8
                            af''16
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
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

        Time treatments defined equal to integers; positive multipliers;
        positive durations; and the strings ``'accel'`` and ``'rit'``.
        """
        return self._treatments


class Assignment(object):
    """
    Assignment.
    """

    ### CLASS ATTRIBUTES ###

    __slots__ = ("_maker", "_pattern")

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self, maker: FigureMaker, *, pattern: abjad.Pattern = None
    ) -> None:
        assert isinstance(maker, FigureMaker)
        self._maker = maker
        if pattern is not None:
            assert isinstance(pattern, abjad.Pattern)
        self._pattern = pattern

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __format__(self, format_specification="") -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __hash__(self) -> int:
        """
        Delegates to format manager.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def maker(self) -> FigureMaker:
        """
        Gets maker.
        """
        return self._maker

    @property
    def pattern(self) -> typing.Optional[abjad.Pattern]:
        """
        Gets pattern.
        """
        return self._pattern


class Bind(object):
    """
    Bind.
    """

    ### CLASS ATTRIBUTES ###

    __slots__ = ("_assignments",)

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, *assignments: Assignment) -> None:
        for assignment in assignments:
            if not isinstance(assignment, Assignment):
                message = "must be assignment:\n"
                message += f"   {format(assignment)}"
                raise Exception(message)
        self._assignments = list(assignments)

    ### SPECIAL METHODS ###

    def __call__(self, collections: typing.Sequence) -> abjad.Selection:
        """
        Calls bind.

        :param collections: collections.
        """
        collection_count = len(collections)
        matches = []
        for i, collection in enumerate(collections):
            for assignment in self.assignments:
                if (
                    assignment.pattern is None
                    or assignment.pattern.matches_index(i, collection_count)
                ):
                    match = rmakers.Match(assignment, collection)
                    matches.append(match)
                    break
            else:
                raise Exception(f"no maker match for collection {i}.")
        assert len(collections) == len(matches)
        groups = abjad.sequence(matches).group_by(
            lambda match: match.assignment.maker
        )
        tuplets: typing.List[abjad.Tuplet] = []
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
        selection = abjad.select(tuplets)
        return selection

    def __eq__(self, argument) -> bool:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __format__(self, format_specification="") -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __hash__(self) -> int:
        """
        Delegates to format manager.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Delegates to format manager.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def assignments(self) -> typing.List[Assignment]:
        """
        Gets assignments.
        """
        return self._assignments


### FACTORY FUNCTIONS ###


def anchor(
    remote_voice_name: str,
    remote_selector: abjad.SelectorTyping = None,
    local_selector: abjad.SelectorTyping = None,
) -> Anchor:
    """
    Anchors music in this figure (filtered by ``local_selector``) to
    start offset of ``remote_voice_name`` (filtered by
    ``remote_selector``).

    :param remote_voice_name: remote voice name.

    :param remote_selector: remote selector.

    :param local_selector: local selector.
    """
    return Anchor(
        local_selector=local_selector,
        remote_selector=remote_selector,
        remote_voice_name=remote_voice_name,
    )


def anchor_after(
    remote_voice_name: str,
    remote_selector: abjad.SelectorTyping = None,
    local_selector: abjad.SelectorTyping = None,
) -> Anchor:
    """
    Anchors music in this figure (filtered by ``local_selector``) to
    stop offset of ``remote_voice_name`` (filtered by ``remote_selector``).

    :param remote_voice_name: remote voice name.

    :param remote_selector: remote selector.

    :param local_selector: local selector.
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

    :param figure_name: figure name.
    """
    return Anchor(figure_name=figure_name)


def assign(maker: FigureMaker, pattern: abjad.Pattern = None) -> Assignment:
    """
    Makes assignment.
    """
    assert isinstance(maker, FigureMaker), repr(maker)
    return Assignment(maker, pattern=pattern)


def bind(*assignments: Assignment) -> Bind:
    """
    Makes bind.
    """
    return Bind(*assignments)


def coat(pitch: typing.Union[int, str, abjad.Pitch]) -> Coat:
    r"""
    Coats ``pitch``.

    :param pitch: pitch.

    ..  container:: example

        Coats pitches:

        >>> template = baca.TwoVoiceStaffScoreTemplate()
        >>> accumulator = baca.Accumulator(template)

        >>> accumulator(
        ...     "Music_Voice_Two",
        ...     3 * [[0, 2, 10]],
        ...     baca.figure(
        ...         [1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.imbricate(
        ...         "Music_Voice_One",
        ...         [baca.coat(0), baca.coat(2), 10, 0, 2],
        ...         rmakers.beam_groups(),
        ...     ),
        ... )

        >>> maker = baca.SegmentMaker(
        ...     score_template=template,
        ...     spacing=baca.minimum_duration((1, 32)),
        ...     time_signatures=accumulator.time_signatures,
        ... )
        >>> accumulator.populate_segment_maker(maker)
        >>> lilypond_file = maker.run(environment="docs")
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.TwoVoiceStaffScoreTemplate.__call__
            <<                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #32                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/4                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/4                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                <<                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context MusicStaff = "Music_Staff"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                    <<                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context MusicVoiceOne = "Music_Voice_One"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                        {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
            <BLANKLINE>
                                \times 4/5 {
            <BLANKLINE>
                                    % [Music_Voice_One measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                    s8
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    bf'!16
                                    [
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \times 2/3 {
            <BLANKLINE>
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    c'16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    d'16
                                    ]
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \tweak text #tuplet-number::calc-fraction-text
                                \times 6/7 {
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s4
            <BLANKLINE>
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
            <BLANKLINE>
                            }
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice_One"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice_One measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice_One"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice_One measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context MusicVoiceTwo = "Music_Voice_Two"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                        {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                            {
            <BLANKLINE>
                                \times 4/5 {
            <BLANKLINE>
                                    % [Music_Voice_Two measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                    r8
            <BLANKLINE>
                                    c'16
                                    [
            <BLANKLINE>
                                    d'16
            <BLANKLINE>
                                    bf'!16
                                    ]
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \times 2/3 {
            <BLANKLINE>
                                    c'16
                                    [
            <BLANKLINE>
                                    d'16
            <BLANKLINE>
                                    bf'!16
                                    ]
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \tweak text #tuplet-number::calc-fraction-text
                                \times 6/7 {
            <BLANKLINE>
                                    c'16
                                    [
            <BLANKLINE>
                                    d'16
            <BLANKLINE>
                                    bf'!16
                                    ]
            <BLANKLINE>
                                    r4
            <BLANKLINE>
                                }
            <BLANKLINE>
                            }
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice_Two"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice_Two measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice_Two"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice_Two measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                    >>                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__

    ..  container:: example

        Skips wrapped pitches:

        >>> template = baca.TwoVoiceStaffScoreTemplate()
        >>> accumulator = baca.Accumulator(template)

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
        >>> accumulator(
        ...     "Music_Voice_Two",
        ...     collections,
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.imbricate(
        ...         "Music_Voice_One",
        ...         segment,
        ...         baca.accent(selector=baca.pheads()),
        ...         rmakers.beam_groups(beam_rests=True),
        ...     ),
        ... )

        >>> maker = baca.SegmentMaker(
        ...     score_template=template,
        ...     spacing=baca.minimum_duration((1, 32)),
        ...     time_signatures=accumulator.time_signatures,
        ... )
        >>> accumulator.populate_segment_maker(maker)
        >>> lilypond_file = maker.run(environment="docs")
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.TwoVoiceStaffScoreTemplate.__call__
            <<                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #32                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 9/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 9/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                <<                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context MusicStaff = "Music_Staff"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                    <<                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context MusicVoiceOne = "Music_Voice_One"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                        {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    % [Music_Voice_One measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16
                                    - \accent                                                        %! baca.accent():IndicatorCommand
                                    [
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'!16
                                    - \accent                                                        %! baca.accent():IndicatorCommand
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''!16
                                    - \accent                                                        %! baca.accent():IndicatorCommand
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
                                    ]
            <BLANKLINE>
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
            <BLANKLINE>
                            }
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice_One"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice_One measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice_One"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice_One measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context MusicVoiceTwo = "Music_Voice_Two"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                        {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                            {
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    % [Music_Voice_Two measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                    c'16
                                    [
            <BLANKLINE>
                                    d'16
            <BLANKLINE>
                                    bf'!16
            <BLANKLINE>
                                    fs''!16
            <BLANKLINE>
                                    e''16
                                    ]
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    ef''!16
                                    [
            <BLANKLINE>
                                    af''!16
            <BLANKLINE>
                                    g''16
            <BLANKLINE>
                                    a'16
                                    ]
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    c'16
                                    [
            <BLANKLINE>
                                    d'16
            <BLANKLINE>
                                    bf'!16
            <BLANKLINE>
                                    fs''!16
            <BLANKLINE>
                                    e''16
                                    ]
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    ef''!16
                                    [
            <BLANKLINE>
                                    af''!16
            <BLANKLINE>
                                    g''16
            <BLANKLINE>
                                    a'16
                                    ]
            <BLANKLINE>
                                }
            <BLANKLINE>
                            }
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice_Two"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice_Two measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice_Two"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice_Two measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                    >>                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__

    """
    return Coat(pitch)


def extend_beam(
    selector: abjad.SelectorTyping = classes.Expression().select().leaf(-1)
) -> commandclasses.IndicatorCommand:
    r"""
    Attaches RIGHT_BROKEN_BEAM to selector output.

    ..  container:: example

        Extends beam:

        >>> template = baca.TwoVoiceStaffScoreTemplate()
        >>> accumulator = baca.Accumulator(template)

        >>> accumulator(
        ...     "Music_Voice_Two",
        ...     [[0, 2, 10, 18], [16, 15, 23]],
        ...     baca.figure([1], 16),
        ...     rmakers.beam_groups(),
        ...     baca.imbricate(
        ...         "Music_Voice_One",
        ...         [2, 10],
        ...         baca.staccato(selector=baca.pheads()),
        ...         rmakers.beam_groups(beam_rests=True),
        ...         baca.extend_beam(),
        ...     ),
        ... )

        >>> accumulator(
        ...     "Music_Voice_Two",
        ...     [[19, 13, 9, 8]],
        ...     baca.figure([1], 16),
        ...     rmakers.beam_groups(),
        ...     baca.imbricate(
        ...         "Music_Voice_One",
        ...         [13, 9],
        ...         baca.staccato(selector=baca.pheads()),
        ...         rmakers.beam_groups(beam_rests=True),
        ...     ),
        ... )

        >>> maker = baca.SegmentMaker(
        ...     ignore_repeat_pitch_classes=True,
        ...     score_template=baca.TwoVoiceStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 32)),
        ...     time_signatures=accumulator.time_signatures,
        ... )
        >>> accumulator.populate_segment_maker(maker)
        >>> lilypond_file = maker.run(environment="docs")
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.TwoVoiceStaffScoreTemplate.__call__
            <<                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #32                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 7/16                                                                   %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 7/16                                                                    %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #32                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                <<                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context MusicStaff = "Music_Staff"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                    <<                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context MusicVoiceOne = "Music_Voice_One"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                        {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    % [Music_Voice_One measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                    s16
                                    [
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    - \staccato                                                      %! baca.staccato():IndicatorCommand
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'!16
                                    - \staccato                                                      %! baca.staccato():IndicatorCommand
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    s16
            <BLANKLINE>
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
            <BLANKLINE>
                            }
            <BLANKLINE>
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    % [Music_Voice_One measure 2]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    s16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    cs''!16
                                    - \staccato                                                      %! baca.staccato():IndicatorCommand
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
                                    - \staccato                                                      %! baca.staccato():IndicatorCommand
            <BLANKLINE>
                                    s16
                                    ]
            <BLANKLINE>
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
            <BLANKLINE>
                            }
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice_One"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice_One measure 3]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice_One"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice_One measure 3]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context MusicVoiceTwo = "Music_Voice_Two"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                        {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                            {
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    % [Music_Voice_Two measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16
                                    [
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    fs''!16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    e''16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    ef''!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    b''16
                                    ]
            <BLANKLINE>
                                }
            <BLANKLINE>
                            }
            <BLANKLINE>
                            {
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    % [Music_Voice_Two measure 2]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    g''16
                                    [
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    cs''!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    af'!16
                                    ]
            <BLANKLINE>
                                }
            <BLANKLINE>
                            }
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice_Two"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice_Two measure 3]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice_Two"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice_Two measure 3]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                    >>                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__

    """
    return commandclasses.IndicatorCommand(
        indicators=[abjad.tags.RIGHT_BROKEN_BEAM], selector=selector
    )


def imbricate(
    voice_name: str,
    segment: typing.List,
    *specifiers: typing.Any,
    allow_unused_pitches: bool = None,
    by_pitch_class: bool = None,
    hocket: bool = None,
    selector: abjad.SelectorTyping = None,
    truncate_ties: bool = None,
):
    r"""
    Imbricates ``segment`` in voice with ``voice_name``.

    ..  container:: example

        >>> template = baca.TwoVoiceStaffScoreTemplate()
        >>> accumulator = baca.Accumulator(template)

        >>> collections = [
        ...     [0, 2, 10, 18, 16],
        ...     [15, 20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ... ]
        >>> accumulator(
        ...     "Music_Voice_Two",
        ...     collections,
        ...     baca.figure([1], 16),
        ...     rmakers.beam_groups(),
        ...     baca.imbricate(
        ...         "Music_Voice_One",
        ...         [2, 19, 9, 18, 16],
        ...         rmakers.beam_groups(),
        ...     ),
        ... )

        >>> maker = baca.SegmentMaker(
        ...     score_template=template,
        ...     spacing=baca.minimum_duration((1, 32)),
        ...     time_signatures=accumulator.time_signatures,
        ... )
        >>> accumulator.populate_segment_maker(maker)
        >>> lilypond_file = maker.run(environment="docs")
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.TwoVoiceStaffScoreTemplate.__call__
            <<                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #32                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 15/16                                                                  %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 15/16                                                                   %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                <<                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context MusicStaff = "Music_Staff"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                    <<                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context MusicVoiceOne = "Music_Voice_One"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                        {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    % [Music_Voice_One measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                    s16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    g''16
                                    [
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    a'16
                                    ]
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    fs''!16
                                    [
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    e''16
                                    ]
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
            <BLANKLINE>
                            }
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice_One"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice_One measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice_One"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice_One measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context MusicVoiceTwo = "Music_Voice_Two"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                        {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                            {
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    % [Music_Voice_Two measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16
                                    [
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    c'16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    d'16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    ef''!16
                                    ]
            <BLANKLINE>
                                }
            <BLANKLINE>
                            }
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice_Two"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice_Two measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice_Two"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice_Two measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                    >>                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__

    ..  container:: example

        Multiple imbricated voices:

        >>> template = baca.ThreeVoiceStaffScoreTemplate()
        >>> accumulator = baca.Accumulator(template)

        >>> collections = [
        ...     [0, 2, 10, 18, 16],
        ...     [15, 20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ... ]
        >>> accumulator(
        ...     "Music_Voice_Two",
        ...     collections,
        ...     baca.figure([1], 16),
        ...     baca.imbricate(
        ...         "Music_Voice_One",
        ...         [2, 19, 9],
        ...         rmakers.beam_groups(beam_rests=True),
        ...         baca.beam_positions(6),
        ...         baca.staccato(selector=baca.pheads()),
        ...         ),
        ...     baca.imbricate(
        ...         "Music_Voice_Three",
        ...         [16, 10, 18],
        ...         rmakers.beam_groups(beam_rests=True),
        ...         baca.beam_positions(8),
        ...         baca.accent(selector=baca.pheads()),
        ...         ),
        ...     rmakers.beam_groups(),
        ... )

        >>> maker = baca.SegmentMaker(
        ...     score_template=template,
        ...     spacing=baca.minimum_duration((1, 32)),
        ...     time_signatures=accumulator.time_signatures,
        ... )
        >>> accumulator.populate_segment_maker(maker)
        >>> lilypond_file = maker.run(environment="docs")
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.ThreeVoiceStaffScoreTemplate.__call__
            <<                                                                                       %! baca.ThreeVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #32                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 15/16                                                                  %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 15/16                                                                   %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.ThreeVoiceStaffScoreTemplate.__call__
                <<                                                                                   %! baca.ThreeVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context MusicStaff = "Music_Staff"                                              %! baca.ThreeVoiceStaffScoreTemplate.__call__
                    <<                                                                               %! baca.ThreeVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context MusicVoiceOne = "Music_Voice_One"                                   %! baca.ThreeVoiceStaffScoreTemplate.__call__
                        {                                                                            %! baca.ThreeVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    % [Music_Voice_One measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                    \override Beam.positions = #'(6 . 6)                             %! baca.beam_positions():OverrideCommand(1)
                                    s16
                                    [
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    - \staccato                                                      %! baca.staccato():IndicatorCommand
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
                                    - \staccato                                                      %! baca.staccato():IndicatorCommand
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
                                    - \staccato                                                      %! baca.staccato():IndicatorCommand
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
                                    ]
                                    \revert Beam.positions                                           %! baca.beam_positions():OverrideCommand(2)
            <BLANKLINE>
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
            <BLANKLINE>
                            }
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice_One"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice_One measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice_One"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice_One measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.ThreeVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context MusicVoiceTwo = "Music_Voice_Two"                                   %! baca.ThreeVoiceStaffScoreTemplate.__call__
                        {                                                                            %! baca.ThreeVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                            {
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    % [Music_Voice_Two measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16
                                    [
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    c'16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    d'16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    ef''!16
                                    ]
            <BLANKLINE>
                                }
            <BLANKLINE>
                            }
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice_Two"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice_Two measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice_Two"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice_Two measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.ThreeVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context MusicVoiceThree = "Music_Voice_Three"                               %! baca.ThreeVoiceStaffScoreTemplate.__call__
                        {                                                                            %! baca.ThreeVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    % [Music_Voice_Three measure 1]                                  %! baca.SegmentMaker._comment_measure_numbers()
                                    \override Beam.positions = #'(8 . 8)                             %! baca.beam_positions():OverrideCommand(1)
                                    s16
                                    [
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16
                                    - \accent                                                        %! baca.accent():IndicatorCommand
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'!16
                                    - \accent                                                        %! baca.accent():IndicatorCommand
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''!16
                                    - \accent                                                        %! baca.accent():IndicatorCommand
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
                                    ]
                                    \revert Beam.positions                                           %! baca.beam_positions():OverrideCommand(2)
            <BLANKLINE>
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
            <BLANKLINE>
                            }
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice_Three"                                 %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice_Three measure 2]                                  %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice_Three"                                  %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice_Three measure 2]                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.ThreeVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                    >>                                                                               %! baca.ThreeVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.ThreeVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.ThreeVoiceStaffScoreTemplate.__call__

    ..  container:: example

        Hides tuplet brackets above imbricated voice:

        >>> template = baca.TwoVoiceStaffScoreTemplate()
        >>> accumulator = baca.Accumulator(template)

        >>> collections = [
        ...     [0, 2, 10, 18, 16],
        ...     [15, 20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ... ]
        >>> accumulator(
        ...     "Music_Voice_Two",
        ...     collections,
        ...     baca.figure([1], 16, treatments=[1]),
        ...     rmakers.beam_groups(beam_rests=True),
        ...     baca.imbricate(
        ...         "Music_Voice_One",
        ...         [2, 19, 9, 18, 16],
        ...         baca.accent(selector=baca.pheads()),
        ...         rmakers.beam_groups(beam_rests=True),
        ...     ),
        ...     baca.staccato(selector=baca.pheads()),
        ... )

        >>> maker = baca.SegmentMaker(
        ...     score_template=template,
        ...     spacing=baca.minimum_duration((1, 32)),
        ...     time_signatures=accumulator.time_signatures,
        ... )
        >>> accumulator.populate_segment_maker(maker)
        >>> lilypond_file = maker.run(environment="docs")
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.TwoVoiceStaffScoreTemplate.__call__
            <<                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #32                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 9/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 9/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                <<                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context MusicStaff = "Music_Staff"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                    <<                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context MusicVoiceOne = "Music_Voice_One"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                        {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
            <BLANKLINE>
                                \tweak text #tuplet-number::calc-fraction-text
                                \times 6/5 {
            <BLANKLINE>
                                    % [Music_Voice_One measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                    s16
                                    [
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    - \accent                                                        %! baca.accent():IndicatorCommand
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \tweak text #tuplet-number::calc-fraction-text
                                \times 6/5 {
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
                                    - \accent                                                        %! baca.accent():IndicatorCommand
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
                                    - \accent                                                        %! baca.accent():IndicatorCommand
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \tweak text #tuplet-number::calc-fraction-text
                                \times 6/5 {
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''!16
                                    - \accent                                                        %! baca.accent():IndicatorCommand
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16
                                    - \accent                                                        %! baca.accent():IndicatorCommand
            <BLANKLINE>
                                    s16
                                    ]
            <BLANKLINE>
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
            <BLANKLINE>
                            }
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice_One"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice_One measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice_One"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice_One measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context MusicVoiceTwo = "Music_Voice_Two"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                        {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                            {
            <BLANKLINE>
                                \tweak text #tuplet-number::calc-fraction-text
                                \times 6/5 {
            <BLANKLINE>
                                    % [Music_Voice_Two measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16
                                    - \staccato                                                      %! baca.staccato():IndicatorCommand
                                    [
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    - \staccato                                                      %! baca.staccato():IndicatorCommand
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'!16
                                    - \staccato                                                      %! baca.staccato():IndicatorCommand
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''!16
                                    - \staccato                                                      %! baca.staccato():IndicatorCommand
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16
                                    - \staccato                                                      %! baca.staccato():IndicatorCommand
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \tweak text #tuplet-number::calc-fraction-text
                                \times 6/5 {
            <BLANKLINE>
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''!16
                                    - \staccato                                                      %! baca.staccato():IndicatorCommand
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''!16
                                    - \staccato                                                      %! baca.staccato():IndicatorCommand
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
                                    - \staccato                                                      %! baca.staccato():IndicatorCommand
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
                                    - \staccato                                                      %! baca.staccato():IndicatorCommand
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    c'16
                                    - \staccato                                                      %! baca.staccato():IndicatorCommand
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \tweak text #tuplet-number::calc-fraction-text
                                \times 6/5 {
            <BLANKLINE>
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    d'16
                                    - \staccato                                                      %! baca.staccato():IndicatorCommand
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'!16
                                    - \staccato                                                      %! baca.staccato():IndicatorCommand
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''!16
                                    - \staccato                                                      %! baca.staccato():IndicatorCommand
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16
                                    - \staccato                                                      %! baca.staccato():IndicatorCommand
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    ef''!16
                                    - \staccato                                                      %! baca.staccato():IndicatorCommand
                                    ]
            <BLANKLINE>
                                }
            <BLANKLINE>
                            }
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice_Two"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice_Two measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice_Two"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice_Two measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                    >>                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__

    ..  container:: example

        Works with pitch-classes:

        >>> template = baca.TwoVoiceStaffScoreTemplate()
        >>> accumulator = baca.Accumulator(template)

        >>> segment = [
        ...     abjad.NumberedPitchClass(10),
        ...     abjad.NumberedPitchClass(6),
        ...     abjad.NumberedPitchClass(4),
        ...     abjad.NumberedPitchClass(3),
        ... ]
        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> accumulator(
        ...     "Music_Voice_Two",
        ...     collections,
        ...     baca.figure([3], 16),
        ...     rmakers.beam(),
        ...     baca.imbricate(
        ...         "Music_Voice_One",
        ...         segment,
        ...         baca.accent(selector=baca.pheads()),
        ...         rmakers.beam_groups(beam_rests=True),
        ...     ),
        ... )

        >>> maker = baca.SegmentMaker(
        ...     score_template=template,
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=accumulator.time_signatures,
        ... )
        >>> accumulator.populate_segment_maker(maker)
        >>> lilypond_file = maker.run(environment="docs")
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.TwoVoiceStaffScoreTemplate.__call__
            <<                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 27/16                                                                  %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 27/16                                                                   %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                <<                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context MusicStaff = "Music_Staff"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                    <<                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context MusicVoiceOne = "Music_Voice_One"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                        {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    % [Music_Voice_One measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                    s8.
                                    [
            <BLANKLINE>
                                    s8.
            <BLANKLINE>
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    bf'!8.
                                    - \accent                                                        %! baca.accent():IndicatorCommand
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    fs''!8.
                                    - \accent                                                        %! baca.accent():IndicatorCommand
            <BLANKLINE>
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    e''8.
                                    - \accent                                                        %! baca.accent():IndicatorCommand
            <BLANKLINE>
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    ef''!8.
                                    - \accent                                                        %! baca.accent():IndicatorCommand
            <BLANKLINE>
                                    s8.
            <BLANKLINE>
                                    s8.
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    s8.
                                    ]
            <BLANKLINE>
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
            <BLANKLINE>
                            }
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice_One"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice_One measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice_One"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice_One measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context MusicVoiceTwo = "Music_Voice_Two"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                        {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                            {
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    % [Music_Voice_Two measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                    c'8.
                                    [
            <BLANKLINE>
                                    d'8.
            <BLANKLINE>
                                    bf'!8.
                                    ]
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    fs''!8.
                                    [
            <BLANKLINE>
                                    e''8.
            <BLANKLINE>
                                    ef''!8.
            <BLANKLINE>
                                    af''!8.
            <BLANKLINE>
                                    g''8.
                                    ]
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    a'8.
            <BLANKLINE>
                                }
            <BLANKLINE>
                            }
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice_Two"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice_Two measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice_Two"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice_Two measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                    >>                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__

    ..  container:: example

        Works with chords:

        >>> template = baca.TwoVoiceStaffScoreTemplate()
        >>> accumulator = baca.Accumulator(template)

        >>> collections = [
        ...     {0, 2, 10, 18, 16},
        ...     [15, 20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ... ]
        >>> accumulator(
        ...     "Music_Voice_Two",
        ...     collections,
        ...     baca.figure([1], 16),
        ...     rmakers.beam_groups(),
        ...     baca.imbricate(
        ...         "Music_Voice_One",
        ...         [2, 19, 9, 18, 16],
        ...         rmakers.beam_groups(),
        ...     ),
        ... )

        >>> maker = baca.SegmentMaker(
        ...     ignore_repeat_pitch_classes=True,
        ...     score_template=baca.TwoVoiceStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 32)),
        ...     time_signatures=accumulator.time_signatures,
        ... )
        >>> accumulator.populate_segment_maker(maker)
        >>> lilypond_file = maker.run(environment="docs")
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.TwoVoiceStaffScoreTemplate.__call__
            <<                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #32                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 11/16                                                                  %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 11/16                                                                   %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                <<                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context MusicStaff = "Music_Staff"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                    <<                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context MusicVoiceOne = "Music_Voice_One"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                        {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    % [Music_Voice_One measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    g''16
                                    [
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    a'16
                                    ]
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    fs''!16
                                    [
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    e''16
                                    ]
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
            <BLANKLINE>
                            }
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice_One"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice_One measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice_One"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice_One measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context MusicVoiceTwo = "Music_Voice_Two"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                        {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                            {
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    % [Music_Voice_Two measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    <c' d' bf'! e'' fs''!>16
                                    [
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    c'16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    d'16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    ef''!16
                                    ]
            <BLANKLINE>
                                }
            <BLANKLINE>
                            }
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice_Two"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice_Two measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice_Two"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice_Two measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                    >>                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__

    ..  container:: example

        Works with rests:

        >>> template = baca.TwoVoiceStaffScoreTemplate()
        >>> accumulator = baca.Accumulator(template)

        >>> collections = [
        ...     [0, 2, 10, 18, 16],
        ...     [15, 20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ... ]
        >>> accumulator(
        ...     "Music_Voice_Two",
        ...     collections,
        ...     baca.figure([1], 16, affix=baca.rests_around([2], [2])),
        ...     rmakers.beam_groups(),
        ...     baca.imbricate(
        ...         "Music_Voice_One",
        ...         [2, 19, 9, 18, 16],
        ...         rmakers.beam_groups(),
        ...     ),
        ... )

        >>> maker = baca.SegmentMaker(
        ...     ignore_repeat_pitch_classes=True,
        ...     score_template=baca.TwoVoiceStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 32)),
        ...     time_signatures=accumulator.time_signatures,
        ... )
        >>> accumulator.populate_segment_maker(maker)
        >>> lilypond_file = maker.run(environment="docs")
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.TwoVoiceStaffScoreTemplate.__call__
            <<                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #32                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 19/16                                                                  %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 19/16                                                                   %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                <<                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context MusicStaff = "Music_Staff"                                              %! baca.TwoVoiceStaffScoreTemplate.__call__
                    <<                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context MusicVoiceOne = "Music_Voice_One"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                        {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    % [Music_Voice_One measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                    s8
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    g''16
                                    [
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    a'16
                                    ]
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    fs''!16
                                    [
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    e''16
                                    ]
            <BLANKLINE>
                                    s16
            <BLANKLINE>
                                    s8
            <BLANKLINE>
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
            <BLANKLINE>
                            }
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice_One"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice_One measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice_One"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice_One measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context MusicVoiceTwo = "Music_Voice_Two"                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
                        {                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                            {
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    % [Music_Voice_Two measure 1]                                    %! baca.SegmentMaker._comment_measure_numbers()
                                    r8
            <BLANKLINE>
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16
                                    [
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    c'16
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    d'16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    ef''!16
                                    ]
            <BLANKLINE>
                                    r8
            <BLANKLINE>
                                }
            <BLANKLINE>
                            }
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice_Two"                                   %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice_Two measure 2]                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice_Two"                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice_Two measure 2]                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                    >>                                                                               %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.TwoVoiceStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.TwoVoiceStaffScoreTemplate.__call__

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
    left_counts: typing.Sequence[int] = None,
    left_cyclic: bool = None,
    left_length: int = None,
    left_reversed: bool = None,
    middle_counts: typing.Sequence[int] = None,
    middle_cyclic: bool = None,
    middle_reversed: bool = None,
    priority: abjad.HorizontalAlignment = None,
    right_counts: typing.Sequence[int] = None,
    right_cyclic: bool = None,
    right_length: int = None,
    right_reversed: bool = None,
) -> LMR:
    """
    Makes left-middle-right.

    ..  container:: example

        Default LMR:

        >>> lmr = baca.lmr()

        >>> parts = lmr([1])
        >>> for part in parts: part
        Sequence([1])

        >>> parts =lmr([1, 2])
        >>> for part in parts: part
        Sequence([1, 2])

        >>> parts = lmr([1, 2, 3])
        >>> for part in parts: part
        Sequence([1, 2, 3])

        >>> parts = lmr([1, 2, 3, 4])
        >>> for part in parts: part
        Sequence([1, 2, 3, 4])

        >>> parts = lmr([1, 2, 3, 4, 5])
        >>> for part in parts: part
        Sequence([1, 2, 3, 4, 5])

        >>> parts = lmr([1, 2, 3, 4, 5, 6])
        >>> for part in parts: part
        Sequence([1, 2, 3, 4, 5, 6])

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
        >>> for part in parts: part
        Sequence([1, 2, 3, 4, 5, 6, 7])

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
        >>> for part in parts: part
        Sequence([1, 2, 3, 4, 5, 6, 7, 8])

        >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> for part in parts: part
        Sequence([1, 2, 3, 4, 5, 6, 7, 8, 9])

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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 13/8
                    s1 * 13/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 13/11 {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #2                               %! baca.tuplet_bracket_staff_padding():OverrideCommand(1)
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
                        \times 9/10 {
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
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! baca.tuplet_bracket_staff_padding():OverrideCommand(2)
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
    counts: abjad.IntegerSequence,
    denominator: int,
    *,
    acciaccatura: typing.Union[bool, Acciaccatura, LMR] = None,
    affix: RestAffix = None,
    restart_talea: bool = None,
    signature: int = None,
    spelling: rmakers.Spelling = None,
    treatments: typing.Sequence = None,
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 9/8
                    s1 * 9/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/8 {
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding():OverrideCommand(1)
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
                    \times 9/10 {
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
                    \times 2/3 {
                        a'16
                        r8
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():OverrideCommand(2)
                    }
                }
            >>

    """
    return RestAffix(suffix=counts)


def rests_around(
    prefix: typing.List[int], suffix: typing.List[int]
) -> RestAffix:
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 5/4
                    s1 * 5/4
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding():OverrideCommand(1)
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
                    \times 9/10 {
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
                    \times 2/3 {
                        a'16
                        r8
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():OverrideCommand(2)
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> staff = lilypond_file[abjad.Score]
        >>> abjad.override(staff).tuplet_bracket.staff_padding = 4
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            \with
            {
                \override TupletBracket.staff-padding = #4
            }
            <<
                \new GlobalContext
                {
                    \time 13/8
                    s1 * 13/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/8 {
                        r8
                        c'16
                        r16
                        d'16
                        r16
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 11/10 {
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
                    \times 6/5 {
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> staff = lilypond_file[abjad.Score]
        >>> abjad.override(staff).tuplet_bracket.staff_padding = 4
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            \with
            {
                \override TupletBracket.staff-padding = #4
            }
            <<
                \new GlobalContext
                {
                    \time 13/8
                    s1 * 13/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/8 {
                        r8
                        r16
                        c'16
                        r16
                        d'16
                        r16
                        bf'16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 11/10 {
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
                    \times 6/5 {
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 9/16
                    s1 * 9/16
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/4 {
                        r16
                        c'16
                        [
                        d'16
                        bf'16
                        ]
                    }
                    \times 4/5 {
                        fs''16
                        [
                        e''16
                        ef''16
                        af''16
                        g''16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        a'16
                        r16
                    }
                }
            >>

    """
    return RestAffix(prefix=prefix, suffix=suffix)


def rests_before(counts: typing.List[int]) -> RestAffix:
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 19/16
                    s1 * 19/16
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding():OverrideCommand(1)
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
                    \times 9/10 {
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
                    \scaleDurations #'(1 . 1) {
                        a'16
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():OverrideCommand(2)
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
        remote_selector=classes.Expression().select().leaf(-1),
        remote_voice_name=remote_voice_name,
        use_remote_stop_offset=True,
    )


def skips_after(counts: typing.List[int]) -> RestAffix:
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 9/8
                    s1 * 9/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/8 {
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding():OverrideCommand(1)
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
                    \times 9/10 {
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
                    \times 2/3 {
                        a'16
                        s8
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():OverrideCommand(2)
                    }
                }
            >>

    """
    return RestAffix(skips_instead_of_rests=True, suffix=counts)


def skips_around(
    prefix: typing.List[int], suffix: typing.List[int]
) -> RestAffix:
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 5/4
                    s1 * 5/4
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding():OverrideCommand(1)
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
                    \times 9/10 {
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
                    \times 2/3 {
                        a'16
                        s8
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():OverrideCommand(2)
                    }
                }
            >>

    """
    return RestAffix(prefix=prefix, skips_instead_of_rests=True, suffix=suffix)


def skips_before(counts: typing.List[int],) -> RestAffix:
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 19/16
                    s1 * 19/16
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding():OverrideCommand(1)
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
                    \times 9/10 {
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
                    \scaleDurations #'(1 . 1) {
                        a'16
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():OverrideCommand(2)
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
        ...     ]
        >>> selections = stack(collections)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
        >>> staff = lilypond_file[abjad.Score]
        >>> abjad.override(staff).beam.positions = (-6, -6)
        >>> abjad.override(staff).stem.direction = abjad.Down
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            \with
            {
                \override Beam.positions = #'(-6 . -6)
                \override Stem.direction = #down
            }
            <<
                \new GlobalContext
                {
                    \time 15/8
                    s1 * 15/8
                }
                \new Staff
                {
                    \times 4/6 {
                        c'16
                        [
                        d'16
                        bf'8
                        fs''16
                        e''16
                        ]
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        ef''8
                        [
                        af''16
                        g''16
                        a'8
                        c'16
                        ]
                    }
                    \times 4/7 {
                        d'16
                        [
                        bf'8
                        fs''16
                        e''16
                        ef''8
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        af''16
                        [
                        g''16
                        a'8
                        c'16
                        d'16
                        ]
                    }
                    \times 4/7 {
                        bf'8
                        [
                        fs''16
                        e''16
                        ef''8
                        af''16
                        ]
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
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
