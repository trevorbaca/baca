import abjad
import collections
import copy
import typing
from . import scoping
from . import typings
from .IndicatorBundle import IndicatorBundle
from .IndicatorCommand import IndicatorCommand
from .Selection import Selection


class PiecewiseIndicatorCommand(scoping.Command):
    """
    Piecewise indicator command.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bookend',
        '_bundles',
        '_final_piece_spanner',
        '_leak',
        '_piece_selector',
        '_remove_length_1_spanner_start',
        '_right_broken',
        '_selector',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        bookend: typing.Union[bool, int] = None,
        bundles: typing.List[IndicatorBundle] = None,
        final_piece_spanner: typing.Any = None,
        leak: bool = None,
        piece_selector: typings.Selector = 'baca.leaves()',
        remove_length_1_spanner_start: bool = None,
        right_broken: typing.Any = None,
        selector: typings.Selector = 'baca.leaves()',
        ) -> None:
        # for selector evaluation
        import baca
        scoping.Command.__init__(self, selector=selector)
        if bookend is not None:
            assert isinstance(bookend, (int, bool)), repr(bookend)
        self._bookend = bookend
        bundles_ = None
        if bundles is not None:
            bundles_ = abjad.CyclicTuple(bundles)
        self._bundles = bundles_
        if final_piece_spanner not in (None, False):
            assert getattr(final_piece_spanner, 'spanner_start', False)
        self._final_piece_spanner = final_piece_spanner
        if leak is not None:
            leak = bool(leak)
        self._leak = leak
        if isinstance(piece_selector, str):
            piece_selector = eval(piece_selector)
        if piece_selector is not None:
            assert isinstance(piece_selector, abjad.Expression), repr(
                piece_selector)
        self._piece_selector = piece_selector
        if remove_length_1_spanner_start is not None:
            remove_length_1_spanner_start = bool(remove_length_1_spanner_start)
        self._remove_length_1_spanner_start = remove_length_1_spanner_start
        self._right_broken = right_broken
        self._tags = []

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if not self.bundles:
            return
        if self.selector is not None:
            assert not isinstance(self.selector, str)
            argument = self.selector(argument)
        if self.piece_selector is not None:
            assert not isinstance(self.piece_selector, str)
            pieces = self.piece_selector(argument)
        else:
            pieces = argument
        assert pieces is not None
        piece_count = len(pieces)
        assert 0 < piece_count, repr(piece_count)
        if self.bookend in (False, None):
            bookend_pattern = abjad.Pattern()
        elif self.bookend is True:
            bookend_pattern = abjad.index([0], 1)
        else:
            assert isinstance(self.bookend, int), repr(self.bookend)
            bookend_pattern = abjad.index([self.bookend], period=piece_count)
        for i, piece in enumerate(pieces):
            start_leaf = Selection(piece).leaf(0)
            stop_leaf = Selection(piece).leaf(-1)
            if i == 0:
                is_first_piece = True
            else:
                is_first_piece = False
            if i == piece_count - 1:
                is_final_piece = True
            else:
                is_final_piece = False
            if is_final_piece and self.right_broken:
                bundle = IndicatorBundle(self.right_broken)
                self._attach_indicators(
                    bundle,
                    stop_leaf,
                    tag=str(abjad.tags.HIDE_TO_JOIN_BROKEN_SPANNERS),
                    )
            if (bookend_pattern.matches_index(i, piece_count) and
                1 < len(piece)):
                should_bookend = True
            else:
                should_bookend = False
            if is_final_piece and self.right_broken:
                should_bookend = False
            bundle = self.bundles[i]
            if should_bookend and bundle.bookended_spanner_start:
                bundle = bundle.with_spanner_start(
                    bundle.bookended_spanner_start
                    )
            if (len(piece) == 1 and
                bundle.compound() and
                self.remove_length_1_spanner_start):
                bundle = bundle.with_spanner_start(None)
            if is_final_piece and bundle.compound():
                if self.final_piece_spanner:
                    bundle = bundle.with_spanner_start(
                        self.final_piece_spanner)
                elif self.final_piece_spanner is False:
                    bundle = bundle.with_spanner_start(None)
            if is_first_piece:
                bundle = bundle.with_spanner_stop(None)
            self._attach_indicators(
                bundle,
                start_leaf,
                tag='PIC',
                )
            next_bundle = self.bundles[i + 1]
            if should_bookend:
                if bundle.bookended_spanner_start is not None:
                    next_bundle = next_bundle.with_spanner_start(None)
                if next_bundle.compound():
                    next_bundle = next_bundle.with_spanner_start(None)
                self._attach_indicators(
                    next_bundle,
                    stop_leaf,
                    tag='PIC',
                    )
            elif is_final_piece and next_bundle.spanner_stop:
                spanner_stop = next_bundle.spanner_stop
                if self.leak:
                    spanner_stop = abjad.new(spanner_stop, leak=True)
                bundle = IndicatorBundle(spanner_stop)
                self._attach_indicators(
                    bundle,
                    stop_leaf,
                    tag='PIC',
                    )

    ### PRIVATE METHODS ###

    def _attach_indicators(
        self,
        bundle,
        leaf,
        tag=None,
        ):
        # TODO: factor out late import
        from .SegmentMaker import SegmentMaker
        assert isinstance(tag, str), repr(tag)
        for indicator in bundle:
            reapplied = scoping.Command._remove_reapplied_wrappers(
                leaf,
                indicator,
                )
            wrapper = abjad.attach(
                indicator,
                leaf,
                tag=self.tag.prepend(tag),
                wrapper=True,
                )
            if indicator == reapplied:
                if (isinstance(indicator, abjad.Dynamic) and
                    indicator.sforzando):
                    status = 'explicit'
                else:
                    status = 'redundant'
                SegmentMaker._treat_persistent_wrapper(
                    self.runtime['manifests'],
                    wrapper,
                    status,
                    )

    ### PUBLIC PROPERTIES ###

    @property
    def bookend(self) -> typing.Optional[typing.Union[bool, int]]:
        """
        Gets bookend token.

        Command attaches indicator to first leaf in each group of
        selector output when ``bookend`` is false.

        Command attaches indicator to both first leaf and last
        leaf in each group of selector output when ``bookend`` is true.

        When ``bookend`` equals integer ``n``, command attaches indicator to
        first leaf and last leaf in group ``n`` of selector output and attaches
        indicator to only first leaf in other groups of selector output.
        """
        return self._bookend

    @property
    def bundles(self) -> typing.Optional[abjad.CyclicTuple]:
        """
        Gets bundles.
        """
        return self._bundles

    @property
    def final_piece_spanner(self) -> typing.Optional[typing.Any]:
        """
        Gets last piece spanner start.
        """
        return self._final_piece_spanner

    @property
    def leak(self) -> typing.Optional[bool]:
        """
        Is true when command leaks final spanner stop.
        """
        return self._leak

    @property
    def piece_selector(self) -> typing.Optional[abjad.Expression]:
        """
        Gets piece selector.
        """
        return self._piece_selector

    @property
    def remove_length_1_spanner_start(self) -> typing.Optional[bool]:
        """
        Is true when command removes spanner start from length-1 pieces.
        """
        return self._remove_length_1_spanner_start

    @property
    def right_broken(self) -> typing.Optional[typing.Any]:
        """
        Gets right-broken indicator.
        """
        return self._right_broken

    @property
    def selector(self) -> typing.Optional[abjad.Expression]:
        """
        Gets (first-order) selector.
        """
        return self._selector
