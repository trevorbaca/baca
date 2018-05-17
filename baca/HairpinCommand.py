import abjad
import baca
import typing
from .Command import Command
from .Typing import Selector


class HairpinCommand(Command):
    """
    Hairpin command.

    ..  container:: example

        >>> baca.HairpinCommand()
        HairpinCommand(selector=baca.tleaves(), tags=[])

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_leak',
        '_left_broken',
        '_right_broken',
        '_start',
        '_stop',
        '_tags',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        deactivate: bool = None,
        leak: bool = None,
        left_broken: str = None,
        selector: Selector = 'baca.tleaves()',
        right_broken: str = None,
        start: abjad.Dynamic = None,
        stop: abjad.Dynamic = None,
        tags: typing.List[abjad.Tag] = None,
        ) -> None:
        Command.__init__(self, deactivate=deactivate, selector=selector)
        if leak is not None:
            leak = bool(leak)
        self._leak = leak
        if left_broken is not None:
            assert left_broken in ('<', '>', 'niente'), repr(left_broken)
        self._left_broken = left_broken
        if right_broken is not None:
            assert right_broken in ('<', '>', 'niente'), repr(right_broken)
        self._right_broken = right_broken
        if start is not None:
            assert isinstance(start, abjad.Dynamic), repr(start)
        self._start = start
        if stop is not None:
            assert isinstance(stop, abjad.Dynamic), repr(stop)
        self._stop = stop
        tags = tags or []
        assert self._are_valid_tags(tags), repr(tags)
        self._tags = tags

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Applies command to result of selector called on `argument`.
        """
        from .SegmentMaker import SegmentMaker
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if not argument:
            return
        leaves = abjad.select(argument).leaves()
        spanner = abjad.Hairpin(context='Voice', leak=self.leak)
        abjad.attach(
            spanner,
            leaves,
            left_broken=self.left_broken,
            right_broken=self.right_broken,
            tag=self.tag.prepend('HC1'),
            )
        dummy = abjad.Dynamic('f')
        if self.left_broken:
            assert self.start is None, repr(self.start)
            reapplied = self._remove_reapplied_wrappers(spanner[0], dummy)
        if self.right_broken:
            assert self.stop is None, repr(self.stop)
            reapplied = self._remove_reapplied_wrappers(spanner[-1], dummy)
        if self.start:
            reapplied = self._remove_reapplied_wrappers(spanner[0], self.start)
            leaf = spanner[0]
            assert isinstance(leaf, abjad.Leaf)
            wrapper = spanner.attach(
                self.start,
                leaf,
                deactivate=self.deactivate,
                tag=self.tag.prepend('HC2'),
                wrapper=True,
                )
            if self.start == reapplied:
                SegmentMaker._treat_persistent_wrapper(
                    self.manifests,
                    wrapper,
                    'redundant',
                    )
        if self.stop and (1 < len(spanner) or self.left_broken):
            reapplied = self._remove_reapplied_wrappers(spanner[-1], self.stop)
            leaf = spanner[-1]
            assert isinstance(leaf, abjad.Leaf)
            wrapper = spanner.attach(
                self.stop,
                leaf,
                deactivate=self.deactivate,
                tag=self.tag.prepend('HC3'),
                wrapper=True,
                )
            if self.stop == reapplied:
                SegmentMaker._treat_persistent_wrapper(
                    self.manifests,
                    wrapper,
                    'redundant',
                    )

    ### PUBLIC PROPERTIES ###

    @property
    def leak(self) -> typing.Optional[bool]:
        """
        Is true when hairpin leaks one leaf to the right.
        """
        return self._leak

    @property
    def left_broken(self) -> typing.Optional[str]:
        """
        Gets left-broken hairpin string.
        """
        return self._left_broken

    @property
    def right_broken(self) -> typing.Optional[str]:
        """
        Gets right-broken hairpin string.
        """
        return self._right_broken

    @property
    def start(self):
        """
        Gets hairpin start.

        Returns dynamic or none.
        """
        return self._start

    @property
    def stop(self):
        """
        Gets hairpin stop.

        Returns dynamic or none.
        """
        return self._stop
