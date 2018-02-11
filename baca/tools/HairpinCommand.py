import abjad
import baca
from .Command import Command


class HairpinCommand(Command):
    r'''Hairpin command.

    ..  container:: example

        >>> baca.HairpinCommand()
        HairpinCommand(selector=baca.tleaves(), tags=[])

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_start',
        '_stop',
        '_tags',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        deactivate=None,
        selector='baca.tleaves()',
        start=None,
        stop=None,
        tags=None,
        ):
        Command.__init__(self, deactivate=deactivate, selector=selector)
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

    def __call__(self, argument=None):
        r'''Applies command to result of selector called on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if not argument:
            return
        leaves = abjad.select(argument).leaves()
        spanner = abjad.Hairpin(context='Voice')
        abjad.attach(spanner, leaves)
        if self.start:
            reapplied = baca.IndicatorCommand._remove_reapplied_indicator(
                spanner[0],
                self.start,
                )
            if self.tag:
                tag = self.tag.append('HC')
            else:
                tag = abjad.Tag('HC')
            wrapper = spanner.attach(
                self.start,
                spanner[0],
                deactivate=self.deactivate,
                tag=str(tag),
                wrapper=True,
                )
            if self.start == reapplied:
                context = wrapper._find_correct_effective_context()
                baca.SegmentMaker._categorize_persistent_indicator(
                    self._manifests,
                    wrapper,
                    context,
                    'redundant',
                    )
        if self.stop and 1 < len(spanner):
            reapplied = baca.IndicatorCommand._remove_reapplied_indicator(
                spanner[-1],
                self.stop,
                )
            if self.tag:
                tag = self.tag.append('HC')
            else:
                tag = abjad.Tag('HC')
            wrapper = spanner.attach(
                self.stop,
                spanner[-1],
                deactivate=self.deactivate,
                tag=str(tag),
                wrapper=True,
                )
            if self.stop == reapplied:
                context = wrapper._find_correct_effective_context()
                baca.SegmentMaker._categorize_persistent_indicator(
                    self._manifests,
                    wrapper,
                    context,
                    'redundant',
                    )

    ### PUBLIC PROPERTIES ###

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
