"""
Typings library.
"""

import collections
import enum

type Exclude = str | enum.Enum | collections.abc.Sequence[str | enum.Enum]

type Indices = int | tuple[int, int] | list[int] | None

type Slice = int | tuple[int, int] | None
