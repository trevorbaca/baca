import abjad
import typing


class IndicatorBundle(abjad.AbjadObject):
    """
    IndicatorBundle.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_dynamic',
        '_dynamic_trend',
        )

    _publish_storage_format=True

    ### INITIALIZER ###

    def __init__(
        self,
        dynamic: typing.Union[abjad.Dynamic, abjad.LilyPondLiteral] = None,
        dynamic_trend: abjad.DynamicTrend = None,
        ) -> None:
        if dynamic is not None:
            prototype = (abjad.Dynamic, abjad.LilyPondLiteral)
            assert isinstance(dynamic, prototype), repr(dynamic)
        self._dynamic = dynamic
        if dynamic_trend is not None:
            assert isinstance(dynamic_trend, abjad.DynamicTrend)
        self._dynamic_trend = dynamic_trend

    ### SPECIAL METHODS ###

    def __len__(self) -> int:
        """
        Gets length.
        """
        length = 0
        if self.dynamic:
            length += 1
        if self.dynamic_trend:
            length += 1
        return length

    ### PUBLIC PROPERTIES ###

    @property
    def dynamic(self) -> typing.Optional[
        typing.Union[abjad.Dynamic, abjad.LilyPondLiteral]
        ]:
        """
        Gets dynamic.
        """
        return self._dynamic

    @property
    def dynamic_trend(self) -> typing.Optional[abjad.DynamicTrend]:
        """
        Gets dynamic trend.
        """
        return self._dynamic_trend

    @property
    def has_dynamic_only(self) -> bool:
        """
        Is true when bundle has dynamic only.
        """
        if self.dynamic and not self.dynamic_trend:
            return True
        return False

    ### PUBLIC METHODS ###

    def both(self) -> bool:
        """
        Is true when bundle has both indicator and trend.
        """
        return bool(self.dynamic) and bool(self.dynamic_trend)

    def dynamic_only(self) -> 'IndicatorBundle':
        """
        Makes new bundle with dynamic only.
        """
        return type(self)(dynamic=self.dynamic)

    @classmethod
    def from_indicator(class_, indicator) -> 'IndicatorBundle':
        """
        Makes dynamic bundle from indicator.
        """
        if isinstance(indicator, (abjad.Dynamic, abjad.LilyPondLiteral)):
            return class_(dynamic=indicator)
        elif isinstance(indicator, abjad.DynamicTrend):
            return class_(dynamic_trend=indicator)
        else:
            raise TypeError(indicator)

    @property
    def indicators(self) -> typing.List:
        """
        Gets indicators.
        """
        result: typing.List = []
        if self.dynamic:
            result.append(self.dynamic)
        if self.dynamic_trend:
            result.append(self.dynamic_trend)
        return result
