"""
Typings library.
"""

import collections
import enum
import typing

Exclude: typing.TypeAlias = typing.Union[
    str | enum.Enum | collections.abc.Sequence[str | enum.Enum]
]

Indices: typing.TypeAlias = typing.Union[int | tuple[int, int] | list[int] | None]

Slice: typing.TypeAlias = typing.Union[int | tuple[int, int] | None]
