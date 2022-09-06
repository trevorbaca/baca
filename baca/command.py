"""
Command.
"""
import dataclasses
import typing

import abjad

from . import typings as _typings
from .enums import enums as _enums


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Scope:

    voice_name: str | None
    measures: _typings.Slice = (1, -1)

    def __post_init__(self):
        assert isinstance(self.measures, list | tuple), repr(self.measures)
        assert len(self.measures) == 2, repr(self.measures)
        start, stop = self.measures
        assert isinstance(start, int), repr(start)
        assert start != 0, repr(start)
        assert isinstance(stop, int), repr(stop)
        assert stop != 0, repr(stop)
        assert isinstance(self.voice_name, str), repr(self.voice_name)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Command:
    """
    Command.
    """

    deactivate: bool = False
    scope: Scope | None = None
    selector: typing.Callable = lambda _: abjad.select.leaves(_, exclude=_enums.HIDDEN)
    tag_measure_number: bool = False
    tags: list[abjad.Tag] = dataclasses.field(default_factory=list)
    _state: dict = dataclasses.field(default_factory=dict, repr=False)
    _tags: list[abjad.Tag] = dataclasses.field(default_factory=list, repr=False)

    def __post_init__(self):
        # raise Exception("ASDF")
        if self.selector is not None:
            assert callable(self.selector)
        assert isinstance(self.tags, list), repr(self.tags)
        assert all(isinstance(_, abjad.Tag) for _ in self.tags), repr(self.tags)

    def __call__(self, argument=None, runtime: dict = None) -> bool:
        runtime = runtime or {}
        return self._call(argument=argument, runtime=runtime)

    def __repr__(self):
        return f"{type(self).__name__}(scope={self.scope})"

    def _call(self, *, argument=None, runtime=None) -> bool:
        return False

    # TODO: reimplement as method with leaf argument
    # TODO: supply with all self.get_tag(leaf) functionality
    # TODO: always return tag (never none) for in-place append
    @property
    def tag(self) -> abjad.Tag:
        # TODO: replace self.get_tag() functionality
        words = [_ if isinstance(_, str) else _.string for _ in self.tags]
        string = ":".join(words)
        tag = abjad.Tag(string)
        assert isinstance(tag, abjad.Tag)
        return tag

    # TODO: replace in favor of self.tag(leaf)
    def get_tag(
        self, leaf: abjad.Leaf = None, *, runtime: dict = None
    ) -> abjad.Tag | None:
        tags = self.tags[:]
        if self.tag_measure_number:
            assert runtime, repr(runtime)
            start_offset = abjad.get.timespan(leaf).start_offset
            measure_number = runtime["offset_to_measure_number"].get(start_offset)
            if getattr(self, "after", None) is True:
                measure_number += 1
            if measure_number is not None:
                tag = abjad.Tag(f"MEASURE_{measure_number}")
                tags.append(tag)
        if tags:
            words = [_.string for _ in tags]
            string = ":".join(words)
            tag = abjad.Tag(string)
            return tag
        # TODO: return empty tag (instead of none)
        return None
