import typing
import abjad
import baca
from . import library
from . import typings
from .Command import Command


class HairpinCommand(Command):
    """
    Hairpin command.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_dynamic_trend',
        '_lone_dynamic',
        '_right_broken',
        '_start_dynamic',
        '_stop_dynamic',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        dynamic_trend: abjad.DynamicTrend,
        *,
        lone_dynamic: bool = True,
        right_broken: bool = None,
        selector: typings.Selector = 'baca.teaves()',
        start_dynamic: abjad.Dynamic = None,
        stop_dynamic: abjad.Dynamic = None,
        ) -> None:
        Command.__init__(self, selector=selector)
        assert isinstance(dynamic_trend, abjad.DynamicTrend)
        self._dynamic_trend = dynamic_trend
        if lone_dynamic is not None:
            lone_dynamic = bool(lone_dynamic)
        self._lone_dynamic = lone_dynamic
        if right_broken is not None:
            right_broken = bool(right_broken)
        self._right_broken = right_broken
        if start_dynamic is not None:
            assert isinstance(start_dynamic, abjad.Dynamic)
        self._start_dynamic = start_dynamic
        if stop_dynamic is not None:
            assert isinstance(stop_dynamic, abjad.Dynamic)
        self._stop_dynamic = stop_dynamic
        self._tags = [abjad.Tag('BACA_HAIRPIN')]

    ### SPECIAL METHODS ###

    def __call__(self, argument: abjad.Selection = None) -> None:
        """
        Calls command.
        """
        from .dynamics import dynamic as _local_dynamic
        from .dynamics import dynamic_trend as _local_dynamic_trend
        if self.selector:
            argument = self.selector(argument)
        leaves = baca.select(argument).leaves()
        if len(leaves) == 1 and self.lone_dynamic is False:
            return None
        if self.right_broken is True:
            command = library.literal(
                r'\!',
                format_slot='after',
                selector=baca.select().leaf(-1),
                )
            words = self.tag.words
            words.append(str(abjad.tags.HIDE_TO_JOIN_BROKEN_SPANNERS))
            library.tag(words, command, deactivate=False)
            command.runtime = self.runtime
            command(argument)
        if self.start_dynamic is not None:
            command = _local_dynamic(
                self.start_dynamic,
                selector=baca.select().leaf(0),
                )
            library.tag(self.tag.words, command)
            command.runtime = self.runtime
            command(argument)
        if len(leaves) == 1:
            return
        command = _local_dynamic_trend(
            self.dynamic_trend,
            selector=baca.select().leaf(0),
            )
        library.tag(self.tag.words, command)
        command.runtime = self.runtime
        command(argument)
        if self.stop_dynamic is not None:
            command = _local_dynamic(
                self.stop_dynamic,
                selector=baca.select().leaf(-1),
                )
            library.tag(self.tag.words, command)
            command.runtime = self.runtime
            command(argument)

    ### PUBLIC PROPERTIES ###

    @property
    def dynamic_trend(self) -> abjad.DynamicTrend:
        """
        Gets dynamic trend.
        """
        return self._dynamic_trend

    @property
    def lone_dynamic(self) -> typing.Optional[bool]:
        """
        Is true when command attaches start dynamic to lone leaf.
        """
        return self._lone_dynamic

    @property
    def right_broken(self) -> typing.Optional[bool]:
        """
        Is true when command formats tagged ``\!`` to stop leaf.
        """
        return self._right_broken

    @property
    def start_dynamic(self) -> typing.Optional[abjad.Dynamic]:
        """
        Gets start dynamic.
        """
        return self._start_dynamic

    @property
    def stop_dynamic(self) -> typing.Optional[abjad.Dynamic]:
        """
        Gets stop dynamic.
        """
        return self._stop_dynamic
