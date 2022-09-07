"""
Command.
"""
import dataclasses

from . import typings as _typings


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
