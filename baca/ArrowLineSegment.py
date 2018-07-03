import typing
from abjad import enums
from abjad import typings
from abjad.markups import Markup
from .LineSegment import LineSegment


class ArrowLineSegment(LineSegment):
    r"""
    Arrow line segment.

    Arrow line segment is a preconfigured line segment.

    Follow the piecewise definition protocol shown here.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        arrow_width: typings.Number = 0.25,
        dash_fraction: typings.Number = 1,
        dash_period: typings.Number = None,
        left_broken_padding: typings.Number = None,
        left_broken_text: typing.Union[bool, str, Markup] = None,
        left_hspace: typings.Number = 0.25,
        left_padding: typings.Number = None,
        left_stencil_align_direction_y: typing.Union[
            typings.Number, enums.VerticalAlignment, None
            ] = enums.Center,
        right_arrow: bool = True,
        right_broken_arrow: bool = None,
        right_broken_padding: typings.Number = 0,
        right_broken_text: typing.Union[bool, str, Markup] = False,
        right_padding: typings.Number = 0.5,
        right_stencil_align_direction_y: typing.Union[
            typings.Number, enums.VerticalAlignment, None
            ] = enums.Center,
        style: str = None,
        ) -> None:
        super().__init__(
            arrow_width=arrow_width,
            dash_fraction=dash_fraction,
            dash_period=dash_period,
            left_broken_padding=left_broken_padding,
            left_broken_text=left_broken_text,
            left_hspace=left_hspace,
            left_padding=left_padding,
            left_stencil_align_direction_y=left_stencil_align_direction_y,
            right_arrow=right_arrow,
            right_broken_arrow=right_broken_arrow,
            right_broken_padding=right_broken_padding,
            right_broken_text=right_broken_text,
            right_padding=right_padding,
            right_stencil_align_direction_y=right_stencil_align_direction_y,
            style=style,
            )

    ### PRIVATE METHODS ###

    """No _get_lilypond_format(), _get_lilypond_format_bundle()
    because class is used only by piecewise spanner.
    """

    ### PUBLIC PROPERTIES ###

    @property
    def arrow_width(self) -> typing.Optional[typings.Number]:
        r"""
        Gets arrow width of arrow.
        """
        return super().arrow_width

    @property
    def dash_fraction(self) -> typing.Optional[typings.Number]:
        r"""
        Gets dash fraction of arrow.
        """
        return super().dash_fraction

    @property
    def dash_period(self) -> typing.Optional[typings.Number]:
        r"""
        Gets dash period of arrow.
        """
        return super().dash_period

    @property
    def left_broken_text(self) -> typing.Union[bool, str, Markup, None]:
        r"""
        Gets left broken text of arrow.
        """
        return self._left_broken_text

    @property
    def right_broken_arrow(self) -> typing.Optional[bool]:
        r"""
        Is true when arrow should appear immediately before line break.
        """
        return self._right_broken_arrow

    @property
    def style(self) -> typing.Optional[str]:
        r"""
        Gets style of arrow.
        """
        return super().style

    @property
    def tweaks(self) -> None:
        """
        Are not implemented on arrow line segment.
        """
        pass
