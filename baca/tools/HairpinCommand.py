import abjad
import baca
from .Command import Command
from .Typing import List
from .Typing import Optional
from .Typing import Selector


class HairpinCommand(Command):
    r'''Hairpin command.

    ..  container:: example

        >>> baca.HairpinCommand()
        HairpinCommand(selector=baca.tleaves(), tags=[])

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
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
        left_broken: str = None,
        selector: Selector = 'baca.tleaves()',
        right_broken: str = None,
        start: abjad.Dynamic = None,
        stop: abjad.Dynamic = None,
        tags: List[abjad.Tag] = None,
        ) -> None:
        Command.__init__(self, deactivate=deactivate, selector=selector)
        if left_broken is not None:
            assert left_broken in ('<', '>', 'niente'), repr(left_broken)
        self._left_broken: str = left_broken
        if right_broken is not None:
            assert right_broken in ('<', '>', 'niente'), repr(right_broken)
        self._right_broken: str = right_broken
        if start is not None:
            assert isinstance(start, abjad.Dynamic), repr(start)
        self._start: abjad.Dynamic = start
        if stop is not None:
            assert isinstance(stop, abjad.Dynamic), repr(stop)
        self._stop: abjad.Dynamic = stop
        tags = tags or []
        assert self._are_valid_tags(tags), repr(tags)
        self._tags: List[abjad.Tag] = tags

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        r'''Applies command to result of selector called on `argument`.
        '''
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if not argument:
            return
        leaves = abjad.select(argument).leaves()
        spanner = abjad.Hairpin(context='Voice')
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
            wrapper = spanner.attach(
                self.start,
                spanner[0],
                deactivate=self.deactivate,
                tag=self.tag.prepend('HC2'),
                wrapper=True,
                )
            if self.start == reapplied:
                baca.SegmentMaker._treat_persistent_wrapper(
                    self.manifests,
                    wrapper,
                    'redundant',
                    )
        if self.stop and (1 < len(spanner) or self.left_broken):
            reapplied = self._remove_reapplied_wrappers(spanner[-1], self.stop)
            wrapper = spanner.attach(
                self.stop,
                spanner[-1],
                deactivate=self.deactivate,
                tag=self.tag.prepend('HC3'),
                wrapper=True,
                )
            if self.stop == reapplied:
                baca.SegmentMaker._treat_persistent_wrapper(
                    self.manifests,
                    wrapper,
                    'redundant',
                    )

    ### PUBLIC PROPERTIES ###

    @property
    def left_broken(self) -> Optional[str]:
        r'''Gets left-broken hairpin string.
        '''
        return self._left_broken

    @property
    def right_broken(self) -> Optional[str]:
        r'''Gets right-broken hairpin string.
        '''
        return self._right_broken

    @property
    def start(self):
        r'''Gets hairpin start.

        Returns dynamic or none.
        '''
        return self._start

    @property
    def stop(self):
        r'''Gets hairpin stop.

        Returns dynamic or none.
        '''
        return self._stop
