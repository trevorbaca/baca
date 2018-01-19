import abjad
import baca
from .Command import Command


class HairpinCommand(Command):
    r'''Hairpin command.

    ..  container:: example

        >>> baca.HairpinCommand()
        HairpinCommand(selector=baca.tleaves(), site='HC', tags=[])

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_site',
        '_start',
        '_stop',
        '_tags',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        deactivate=None,
        selector='baca.tleaves()',
        site='HC',
        start=None,
        stop=None,
        tags=None,
        ):
        Command.__init__(self, deactivate=deactivate, selector=selector)
        if site is not None:
            assert isinstance(site, str), repr(site)
        self._site = site
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
            spanner.attach(
                self.start,
                spanner[0],
                deactivate=self.deactivate,
                site=self.site,
                tag=self.tag,
                )
            if self.start == reapplied:
                wrapper = abjad.inspect(spanner[0]).wrapper(self.start)
                context = wrapper._find_correct_effective_context()
                baca.SegmentMaker._categorize_persistent_indicator(
                    self._manifests,
                    context,
                    spanner[0],
                    wrapper.indicator,
                    'redundant',
                    spanner=spanner,
                    )
        if self.stop and 1 < len(spanner):
            reapplied = baca.IndicatorCommand._remove_reapplied_indicator(
                spanner[-1],
                self.stop,
                )
            spanner.attach(
                self.stop,
                spanner[-1],
                deactivate=self.deactivate,
                site=self.site,
                tag=self.tag,
                )
            if self.stop == reapplied:
                wrapper = abjad.inspect(spanner[-1]).wrapper(self.stop)
                context = wrapper._find_correct_effective_context()
                baca.SegmentMaker._categorize_persistent_indicator(
                    self._manifests,
                    context,
                    spanner[-1],
                    wrapper.indicator,
                    'redundant',
                    spanner=spanner,
                    )

    ### PUBLIC PROPERTIES ###

    @property
    def site(self):
        r'''Gets site.

        Returns string or none.
        '''
        return self._site

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

    @property
    def tag(self):
        r'''Gets colon-delimited tag.

        Returns string or none.
        '''
        if self.tags:
            return ':'.join(self.tags)
