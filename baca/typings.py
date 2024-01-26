"""
Typings library.
"""

import typing

import abjad

IndexedTweak: typing.TypeAlias = typing.Union[abjad.Tweak, tuple[abjad.Tweak, int]]

Indices: typing.TypeAlias = typing.Union[int | tuple[int, int] | list[int] | None]

Slice: typing.TypeAlias = typing.Union[int | tuple[int, int] | None]
