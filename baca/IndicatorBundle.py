import abjad
import typing


class IndicatorBundle(abjad.AbjadObject):
    """
    IndicatorBundle.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_indicator',
        '_spanner_start',
        )

    _publish_storage_format=True

    ### INITIALIZER ###

    def __init__(
        self,
        *arguments: typing.Any,
        ) -> None:
        assert len(arguments) <= 2, repr(arguments)
        self._indicator = None
        self._spanner_start = None
        for argument in arguments:
            if getattr(argument, 'spanner_start', False) is True:
                self._spanner_start = argument
            else:
                self._indicator = argument

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
        if self.indicator:
            result.append(self.indicator)
        if self.spanner_start:
            result.append(self.spanner_start)
        return result

    @property
    def spanner_start(self) -> typing.Optional[typing.Any]:
        """
        Gets spanner_start.
        """
        return self._spanner_start

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
        return type(self)(indicator, self.spanner_start)

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

        """
        if spanner_start is None:
            return type(self)(self.indicator)
        if getattr(spanner_start, 'spanner_start', False) is not True:
            raise Exception(spanner_start)
        return type(self)(self.indicator, spanner_start)
