import abjad
import typing


class IndicatorBundle(abjad.AbjadObject):
    """
    IndicatorBundle.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bookended_spanner_start',
        '_enchained',
        '_indicator',
        '_spanner_start',
        '_spanner_stop',
        )

    _publish_storage_format=True

    ### INITIALIZER ###

    def __init__(
        self,
        *arguments: typing.Any,
        bookended_spanner_start: typing.Any = None,
        enchained: bool = None,
        ) -> None:
        assert len(arguments) <= 3, repr(arguments)
        self._indicator = None
        self._spanner_start = None
        self._spanner_stop = None
        for argument in arguments:
            if argument is None:
                continue
            elif getattr(argument, 'spanner_start', False) is True:
                self._spanner_start = argument
            elif getattr(argument, 'spanner_stop', False) is True:
                self._spanner_stop = argument
            else:
                self._indicator = argument
        self._bookended_spanner_start = bookended_spanner_start
        if enchained is not None:
            enchained = bool(enchained)
        self._enchained = enchained

    ### SPECIAL METHODS ###

    def __iter__(self) -> typing.Iterator:
        """
        Iterates bundle.
        """
        return iter(self.indicators)

    def __len__(self) -> int:
        """
        Gets length.
        """
        return len(self.indicators)

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        class_ = type(self).__name__
        string = ', '.join([repr(_) for _ in self.indicators])
        return f'{class_}({string})'

    ### PUBLIC PROPERTIES ###

    @property
    def bookended_spanner_start(self) -> typing.Optional[typing.Any]:
        """
        Gets bookended start text span indicator.
        """
        return self._bookended_spanner_start

    @property
    def enchained(self) -> typing.Optional[bool]:
        """
        Is true when bundle contributes to enchained spanner.
        """
        return self._enchained

    @property
    def indicator(self) -> typing.Optional[typing.Any]:
        """
        Gets indicator.
        """
        return self._indicator

    @property
    def indicators(self) -> typing.List:
        """
        Gets indicators.
        """
        result: typing.List = []
        if self.spanner_stop:
            result.append(self.spanner_stop)
        if self.indicator:
            result.append(self.indicator)
        if self.spanner_start:
            result.append(self.spanner_start)
        return result

    @property
    def spanner_start(self) -> typing.Optional[typing.Any]:
        """
        Gets spanner start.
        """
        return self._spanner_start

    @property
    def spanner_stop(self) -> typing.Optional[typing.Any]:
        """
        Gets spanner stop.
        """
        return self._spanner_stop

    ### PUBLIC METHODS ###

    def compound(self) -> bool:
        """
        Is true when bundle has both indicator and spanner_start.
        """
        return bool(self.indicator) and bool(self.spanner_start)

    def indicator_only(self) -> bool:
        """
        Is true when bundle has indicator only.
        """
        if self.indicator and not self.spanner_start:
            return True
        return False

    def simple(self) -> bool:
        """
        Is true when bundle has indicator or spanner start but not both.
        """
        return len(self) == 1

    def spanner_start_only(self) -> bool:
        """
        Is true when bundle has spanner start only.
        """
        if not self.indicator and self.spanner_start:
            return True
        return False

    def with_indicator(self, indicator) -> 'IndicatorBundle':
        """
        Makes new bundle with indicator.

        ..  container:: example

            >>> bundle = baca.IndicatorBundle(
            ...     abjad.Dynamic('p'),
            ...     abjad.DynamicTrend('<'),
            ...     )

            >>> bundle.with_indicator(abjad.Dynamic('f'))
            IndicatorBundle(Dynamic('f'), DynamicTrend(shape='<'))

            >>> bundle.with_indicator(None)
            IndicatorBundle(DynamicTrend(shape='<'))

        """
        if indicator is None:
            return type(self)(self.spanner_start)
        return type(self)(
            self.spanner_stop,
            indicator,
            self.spanner_start,
            bookended_spanner_start=self.bookended_spanner_start,
            enchained=self.enchained,
            )

    def with_spanner_start(self, spanner_start) -> 'IndicatorBundle':
        """
        Makes new bundle with spanner start.

        ..  container:: example

            >>> bundle = baca.IndicatorBundle(
            ...     abjad.Dynamic('p'),
            ...     abjad.DynamicTrend('<'),
            ...     )

            >>> bundle.with_spanner_start(abjad.DynamicTrend('>'))
            IndicatorBundle(Dynamic('p'), DynamicTrend(shape='>'))

            >>> bundle.with_spanner_start(None)
            IndicatorBundle(Dynamic('p'))

        ..  container:: example

            >>> bundle = baca.IndicatorBundle(
            ...     abjad.StopTextSpan(),
            ...     abjad.StartTextSpan(left_text=abjad.Markup('pont.')),
            ...     )

            >>> bundle.with_spanner_start(
            ...     abjad.StartTextSpan(command=r'\startTextSpanOne')
            ...     )
            IndicatorBundle(StopTextSpan(command='\\stopTextSpan'), StartTextSpan(command='\\startTextSpanOne', concat_hspace_left=0.5))

            >>> bundle.with_spanner_start(None)
            IndicatorBundle(StopTextSpan(command='\\stopTextSpan'))

        """
        if (spanner_start is not None and
            getattr(spanner_start, 'spanner_start', False) is not True):
            raise Exception(spanner_start)
        return type(self)(
            self.spanner_stop,
            self.indicator,
            spanner_start,
            bookended_spanner_start=self.bookended_spanner_start,
            enchained=self.enchained,
            )

    def with_spanner_stop(self, spanner_stop) -> 'IndicatorBundle':
        """
        Makes new bundle with spanner stop.

        ..  container:: example

            >>> bundle = baca.IndicatorBundle(
            ...     abjad.StopTextSpan(),
            ...     abjad.StartTextSpan(left_text=abjad.Markup('pont.')),
            ...     )

            >>> string = r'\stopTextSpanOne'
            >>> bundle.with_spanner_stop(abjad.StopTextSpan(command=string))
            IndicatorBundle(StopTextSpan(command='\\stopTextSpanOne'), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5, left_text=Markup(contents=['pont.'])))

            >>> bundle.with_spanner_stop(None)
            IndicatorBundle(StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5, left_text=Markup(contents=['pont.'])))

        """
        if (spanner_stop is not None and
            getattr(spanner_stop, 'spanner_stop', False) is not True):
            raise Exception(spanner_stop)
        return type(self)(
            spanner_stop,
            self.indicator,
            self.spanner_start,
            bookended_spanner_start=self.bookended_spanner_start,
            enchained=self.enchained,
            )
