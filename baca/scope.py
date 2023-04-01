import abjad

from . import select as _select
from .enums import enums as _enums


class DynamicScope:
    def __init__(self, argument):
        self.argument = argument

    def __enter__(self):
        return self

    def __eq__(self, argument):
        return self.argument == argument

    def __exit__(self, exc_type, exc_value, traceback):
        del self.argument

    def __getitem__(self, i):
        return self.argument.__getitem__(i)

    def __iter__(self):
        try:
            return iter(self.argument)
        except TypeError:
            return iter([self.argument])

    def __len__(self):
        try:
            return len(self.argument)
        except TypeError:
            return 1

    def leaf(self, n, *, grace=None):
        return abjad.select.leaf(self.argument, n, exclude=_enums.HIDDEN, grace=grace)

    def leaves(self, *, grace=None):
        return abjad.select.leaves(self.argument, exclude=_enums.HIDDEN, grace=grace)

    def lleaf(self, n):
        return _select.lleaf(self.argument, n, exclude=_enums.HIDDEN)

    def lleaves(self, *, count=None):
        return _select.lleaves(self.argument, count=count, exclude=_enums.HIDDEN)

    def ltleaves(self):
        return _select.ltleaves(self.argument, exclude=_enums.HIDDEN)

    def mmrest(self, n):
        return _select.mmrest(self.argument, n, exclude=_enums.HIDDEN)

    def mmrests(self):
        return _select.mmrests(self.argument, exclude=_enums.HIDDEN)

    def phead(self, n):
        return _select.phead(self.argument, n, exclude=_enums.HIDDEN)

    def pheads(self, *, grace=None):
        return _select.pheads(self.argument, exclude=_enums.HIDDEN, grace=grace)

    def pleaf(self, n, *, grace=None):
        return _select.pleaf(self.argument, n, exclude=_enums.HIDDEN, grace=grace)

    def pleaves(self, *, grace=None):
        return _select.pleaves(self.argument, exclude=_enums.HIDDEN, grace=grace)

    def plt(self, n):
        return _select.plt(self.argument, n, exclude=_enums.HIDDEN)

    def plts(self, *, grace=None):
        return _select.plts(self.argument, exclude=_enums.HIDDEN, grace=grace)

    def ptail(self, n):
        return _select.ptail(self.argument, n, exclude=_enums.HIDDEN)

    def ptails(self):
        return _select.ptails(self.argument, exclude=_enums.HIDDEN)

    def rest(self, n):
        return abjad.select.rest(self.argument, n, exclude=_enums.HIDDEN)

    def rests(self):
        return abjad.select.rests(self.argument)

    def rleaf(self, n):
        return _select.rleaf(self.argument, n)

    def rleak(self):
        return _select.rleak(self.argument)

    def rleaves(self, *, count=1):
        return _select.rleaves(self.argument, count=count, exclude=_enums.HIDDEN)

    def run(self, n):
        return abjad.select.run(self.argument, n, exclude=_enums.HIDDEN)

    def runs(self):
        return _select.runs(self.argument, exclude=_enums.HIDDEN)

    def tleaves(self, *, grace=None):
        return _select.tleaves(self.argument, grace=grace)


def scope(cache):
    return DynamicScope(cache)
