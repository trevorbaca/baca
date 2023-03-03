"""
Classes.
"""
import dataclasses
import typing

import abjad

from . import section as _section


@dataclasses.dataclass(order=True, slots=True, unsafe_hash=True)
class Cursor:
    """
    Cursor.
    """

    source: typing.Sequence = ()
    cyclic: bool = False
    position: int | None = None
    singletons: bool = False
    suppress_exception: bool = False

    def __post_init__(self):
        assert isinstance(self.cyclic, bool), repr(self.cyclic)
        assert isinstance(self.position, int | type(None)), repr(self.position)
        assert isinstance(self.singletons, bool), repr(self.singletons)
        assert isinstance(self.suppress_exception, bool), repr(self.suppress_exception)

    def _source(self):
        if self.cyclic:
            return abjad.CyclicTuple(self.source)
        else:
            return self.source

    def __call__(self, item, *, n=1):
        result = self.get(item, n=n)
        manager = _section.DynamicScope(result)
        return manager

    def __getitem__(self, argument) -> typing.Any:
        """
        Gets item from cursor.
        """
        return self._source().__getitem__(argument)

    def __iter__(self, count=1) -> typing.Generator:
        """
        Iterates cursor.
        """
        return iter(self._source())

    def __len__(self) -> int:
        """
        Gets length of cursor.
        """
        return len(self._source())

    @property
    def exhausted(self) -> bool:
        """
        Is true when cursor is exhausted.
        """
        if self.position is None:
            return False
        try:
            self._source()[self.position]
        except IndexError:
            return True
        return False

    def get(self, item, *, n: int = 1) -> typing.Any:
        """
        Gets next item in cursor and asserts equal to ``item``.
        """
        item_ = self.next(n)
        if item != item_:
            raise Exception(f"{item_} does not equal {item}.")
        return item_

    def next(self, count=1, *, exhausted=False) -> list | None:
        """
        Gets next ``count`` elements from cursor.
        """
        result = []
        if self.position is None:
            self.position = 0
        if 0 < count:
            for i in range(count):
                try:
                    element = self._source()[self.position]
                    result.append(element)
                except IndexError:
                    if not self.suppress_exception:
                        raise Exception(f"cursor only {len(self.source)}.")
                self.position += 1
        elif count < 0:
            for i in range(abs(count)):
                self.position -= 1
                try:
                    element = self._source()[self.position]
                    result.append(element)
                except IndexError:
                    if not self.suppress_exception:
                        raise Exception(f"cursor only {len(self.source)}.")
        if self.singletons:
            if len(result) == 0:
                return None
            elif len(result) == 1:
                result = result[0]
        if exhausted and not self.exhausted:
            raise Exception(f"cusor not exhausted: {self!r}.")
        return result
