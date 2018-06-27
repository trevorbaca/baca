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
        '_start_selector',
        '_stop_dynamic',
        '_stop_selector',
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
        start_selector: typings.Selector = 'baca.leaf(0)',
        stop_dynamic: abjad.Dynamic = None,
        stop_selector: typings.Selector = 'baca.leaf(-1)',
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
        if start_selector is not None:
            assert isinstance(start_selector, abjad.Expression)
        self._start_selector = start_selector
        if stop_dynamic is not None:
            assert isinstance(stop_dynamic, abjad.Dynamic)
        self._stop_dynamic = stop_dynamic
        if stop_selector is not None:
            assert isinstance(stop_selector, abjad.Expression)
        self._stop_selector = stop_selector
        self._tags = [abjad.Tag('BACA_HAIRPIN')]

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
    def start_selector(self) -> typings.Selector:
        """
        Gets start selector.
        """
        return self._start_selector

    @property
    def stop_dynamic(self) -> typing.Optional[abjad.Dynamic]:
        """
        Gets stop dynamic.
        """
        return self._stop_dynamic

    @property
    def stop_selector(self) -> typing.Optional[typings.Selector]:
        """
        Gets stop selector.
        """
        return self._stop_selector

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
            literal = abjad.LilyPondLiteral(r'\!')
            assert isinstance(self.stop_selector, abjad.Expression)
            command = library.literal(
                r'\!',
                format_slot='after',
                selector=self.stop_selector,
                )
            words = self.tag.words
            words.append(str(abjad.tags.HIDE_TO_JOIN_BROKEN_SPANNERS))
            library.tag(words, command, deactivate=False)
            command.runtime = self.runtime
            command(argument)
        if self.start_dynamic is not None:
            command = _local_dynamic(
                self.start_dynamic,
                selector=self.start_selector,
                )
            library.tag(self.tag.words, command)
            command.runtime = self.runtime
            command(argument)
        if len(leaves) == 1:
            return
        command = _local_dynamic_trend(
            self.dynamic_trend,
            selector=self.start_selector,
            )
        library.tag(self.tag.words, command)
        command.runtime = self.runtime
        command(argument)
        if self.stop_dynamic is not None:
            assert isinstance(self.stop_selector, abjad.Expression)
            command = _local_dynamic(
                self.stop_dynamic,
                selector=self.stop_selector,
                )
            library.tag(self.tag.words, command)
            command.runtime = self.runtime
            command(argument)
