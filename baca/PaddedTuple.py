import abjad
import typing


class PaddedTuple(abjad.AbjadObject):
    """
    Padded tuple.

    ..  container:: example

        >>> tuple_ = baca.PaddedTuple('abcd', pad=2)

        >>> tuple_
        PaddedTuple(['a', 'b', 'c', 'd'], pad=2)

        >>> for i in range(8):
        ...     print(i, tuple_[i])
        ...
        0 a
        1 b
        2 c
        3 d
        4 c
        5 d
        6 c
        7 d

    Padded tuples overload the item-getting method of built-in tuples.

    Padded tuples return a value for any integer index.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_items',
        '_pad',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        items: typing.Sequence = None,
        pad: int = 1,
        ) -> None:
        items = items or ()
        items = tuple(items)
        self._items: typing.Tuple = items
        assert isinstance(pad, int), repr(pad)
        assert 1 <= pad, repr(pad)
        self._pad = pad

    ### SPECIAL METHODS ###

    def __contains__(self, item) -> bool:
        """
        Is true when padded tuple contains ``item``.
        """
        return self._items.__contains__(item)

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a tuple with ``items`` and ``pad`` equal
        to those of this padded tuple.
        """
        if isinstance(argument, tuple):
            return self._items == argument
        elif isinstance(argument, type(self)):
            return self._items == argument._items
        return False

    def __getitem__(self, argument) -> typing.Any:
        """
        Gets item or slice identified by ``argument``.

        ..  container:: example

            Gets slice open at right:

            >>> baca.PaddedTuple('abcd', pad=3)[2:]
            ('c', 'd')

            Gets slice closed at right:

            >>> slice_ = baca.PaddedTuple('abcd', pad=3)[:15]
            >>> slice_
            ('a', 'b', 'c', 'd', 'b', 'c', 'd', 'b', 'c', 'd', 'b', 'c', 'd', 'b', 'c')

            >>> len(slice_)
            15

        Raises index error when ``argument`` can not be found in padded tuple.
        """
        if isinstance(argument, slice):
            if argument.start is None:
                if argument.stop is None:
                    start, stop, stride = 0, len(self), 1
                elif 0 < argument.stop:
                    start, stop, stride = 0, argument.stop, 1
                elif argument.stop < 0:
                    start, stop, stride = -1, stop, -1
            elif argument.stop is None:
                if argument.start is None:
                    start, stop, stride = 0, len(self), 1
                elif 0 < argument.start:
                    start, stop, stride = argument.start, len(self), 1
                elif argument.start < 0:
                    start, stop, stride = argument.start, -len(self), -1
            elif 0 < argument.start and 0 < argument.stop:
                start, stop, stride = argument.start, argument.stop, 1
            elif argument.start < 0 and argument.stop < 0:
                start, stop, stride = argument.start, argument.stop, -1
            else:
                raise ValueError(argument)
            items = []
            for i in range(start, stop, stride):
                item = self[i]
                items.append(item)
            return tuple(items)
        if not self:
            raise IndexError(f'padded tuple is empty: {self!r}.')
        length = len(self)
        if 0 <= argument < len(self):
            pass
        elif length <= argument:
            right = self.pad
            left = length - right
            overage = argument - length
            argument = left + (overage % right)
        elif -length <= argument < 0:
            pass
        else:
            assert argument < -length
            left = self.pad
            right = length - left
            assert left + right == length
            overage = abs(argument) - length
            overage = overage % left
            if overage == 0:
                overage = left
            positive_argument = right + overage
            argument = -positive_argument
        return self._items.__getitem__(argument)

    def __hash__(self) -> int:
        """
        Hashes padded tuple.

        Redefined in tandem with __eq__.
        """
        return super(PaddedTuple, self).__hash__()

    def __iter__(self) -> typing.Iterator:
        """
        Iterates padded tuple.

        Iterates items only once.

        Does not iterate infinitely.
        """
        return self._items.__iter__()

    def __len__(self) -> int:
        """
        Gets length of padded tuple.

        ..  container:: example

            >>> len(baca.PaddedTuple('abcd', pad=3))
            4

        """
        assert isinstance(self._items, tuple)
        return self._items.__len__()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_args_values=[list(self._items)],
            )

    def _get_slice(self, start_index, stop_index):
        if 0 < stop_index and start_index is None:
            start_index = 0
        elif stop_index < 0 and start_index is None:
            start_index = -1
        items = []
        if 0 <= start_index and 0 <= stop_index:
            for i in range(start_index, stop_index):
                item = self[i]
                items.append(item)
        elif start_index < 0 and stop_index < 0:
            for i in range(start_index, stop_index, -1):
                item = self[i]
                items.append(item)
        else:
            raise Exception('slice index signs must be equal.')
        return tuple(items)

    ### PUBLIC PROPERTIES ###

    @property
    def items(self) -> typing.Tuple:
        """
        Gets items.

        ..  container:: example

            >>> baca.PaddedTuple('abcd', pad=1).items
            ('a', 'b', 'c', 'd')

            >>> baca.PaddedTuple([1, 2, 3, 4], pad=1).items
            (1, 2, 3, 4)

        """
        return self._items

    @property
    def pad(self) -> typing.Optional[int]:
        """
        Gets pad.

        ..  container:: example

            With nonnegative indices:

            >>> tuple_ = baca.PaddedTuple('abcd', pad=1)
            >>> for i in range(8):
            ...     print(i, tuple_[i])
            ...
            0 a
            1 b
            2 c
            3 d
            4 d
            5 d
            6 d
            7 d

            >>> tuple_ = baca.PaddedTuple('abcd', pad=2)
            >>> for i in range(8):
            ...     print(i, tuple_[i])
            ...
            0 a
            1 b
            2 c
            3 d
            4 c
            5 d
            6 c
            7 d

            >>> tuple_ = baca.PaddedTuple('abcd', pad=3)
            >>> for i in range(8):
            ...     print(i, tuple_[i])
            ...
            0 a
            1 b
            2 c
            3 d
            4 b
            5 c
            6 d
            7 b

            >>> tuple_ = baca.PaddedTuple('abcd', pad=4)
            >>> for i in range(8):
            ...     print(i, tuple_[i])
            ...
            0 a
            1 b
            2 c
            3 d
            4 a
            5 b
            6 c
            7 d

        ..  container:: example

            With nonpositive indices:

            >>> tuple_ = baca.PaddedTuple('abcd', pad=1)
            >>> for i in range(-1, -9, -1):
            ...     print(i, tuple_[i])
            ...
            -1 d
            -2 c
            -3 b
            -4 a
            -5 a
            -6 a
            -7 a
            -8 a

            >>> tuple_ = baca.PaddedTuple('abcd', pad=2)
            >>> for i in range(-1, -9, -1):
            ...     print(i, tuple_[i])
            ...
            -1 d
            -2 c
            -3 b
            -4 a
            -5 b
            -6 a
            -7 b
            -8 a

            >>> tuple_ = baca.PaddedTuple('abcd', pad=3)
            >>> for i in range(-1, -9, -1):
            ...     print(i, tuple_[i])
            ...
            -1 d
            -2 c
            -3 b
            -4 a
            -5 c
            -6 b
            -7 a
            -8 c

            >>> tuple_ = baca.PaddedTuple('abcd', pad=4)
            >>> for i in range(-1, -9, -1):
            ...     print(i, tuple_[i])
            ...
            -1 d
            -2 c
            -3 b
            -4 a
            -5 d
            -6 c
            -7 b
            -8 a

        """
        return self._pad
