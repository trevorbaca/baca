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
        indicator: typing.Any = None,
        spanner_start: typing.Any = None,
        ) -> None:
        self._indicator = indicator
        if (spanner_start is not None
            and getattr(spanner_start, 'spanner_start', False) is not True):
            raise Exception(f'must be spanner start (not {spanner_start}).')
        self._spanner_start = spanner_start

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

    @classmethod
    def from_indicator(class_, indicator) -> 'IndicatorBundle':
        """
        Makes indicator bundle from indicator.
        """
        if getattr(indicator, 'spanner_start', False) is True:
            return class_(spanner_start=indicator)
        else:
            return class_(indicator=indicator)

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
        """
        return type(self)(
            indicator=indicator,
            spanner_start=self.spanner_start,
            )

    def with_spanner_start(self, spanner_start) -> 'IndicatorBundle':
        """
        Makes new bundle with spanner start.
        """
        return type(self)(
            indicator=self.indicator,
            spanner_start=spanner_start,
            )
