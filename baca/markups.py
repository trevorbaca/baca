"""
Markup library.
"""
import typing

import abjad

from . import indicators


def final_markup(
    places: typing.List[str], dates: typing.List[str]
) -> indicators.Markup:
    string = r" \hspace #0.75 – \hspace #0.75 ".join(places)
    places_ = abjad.Markup(string)
    places_ = abjad.Markup.line([places_])
    string = r" \hspace #0.75 – \hspace #0.75 ".join(dates)
    dates_ = abjad.Markup(string)
    dates_ = abjad.Markup.line([dates_])
    markup = abjad.Markup.right_column([places_, dates_])
    markup = markup.with_color("black")
    markup = markup.override(("font-name", "Palatino"))
    markup = indicators.Markup(contents=markup.contents)
    return markup


def instrument(
    string: typing.Union[str, typing.List[str]],
    hcenter_in: typing.Optional[abjad.Number] = 16,
    column: bool = True,
) -> abjad.Markup:
    r"""
    Makes instrument name markup.

    ..  container:: example

        Makes instrument name markup in column:

        >>> markup = baca.markups.instrument("Eng. horn")

        >>> abjad.show(markup, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(markup, strict=89)
            \markup {
                \hcenter-in
                    #16
                    "Eng. horn"
                }

    ..  container:: example

        Makes instrument name markup in line:

        >>> markup = baca.markups.instrument(
        ...     "Violin 1",
        ...     column=False,
        ...     )

        >>> abjad.show(markup, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(markup, strict=89)
            \markup {
                \hcenter-in
                    #16
                    "Violin 1"
                }

    Centers markup horizontally in 16 spaces.
    """
    return make_instrument_name_markup(string, column=column, hcenter_in=hcenter_in)


def lines(items: typing.List, *, boxed: bool = None) -> indicators.Markup:
    if not isinstance(items, list):
        message = f"items must be list (not {type(items).__name__}):"
        lines = ["    " + _ for _ in abjad.lilypond(items).split("\n")]
        lines = "\n".join(lines)
        message += f"\n{lines}"
        raise Exception(message)
    items_ = []
    for item in items:
        if isinstance(item, (str, abjad.Markup)):
            items_.append(item)
        else:
            assert item.indicators is not None
            assert len(item.indicators) == 1
            markup = item.indicators[0]
            items_.append(markup)
    markup = abjad.MarkupList(items_).column()
    markup = indicators.Markup(contents=markup.contents)
    if boxed:
        markup = markup.boxed()
    return markup


def make_instrument_name_markup(string, *, column=True, hcenter_in=None):
    if hcenter_in is not None:
        assert isinstance(hcenter_in, (int, float)), repr(hcenter_in)
    if isinstance(string, str):
        parts = [string]
    elif isinstance(string, list):
        parts = string
    else:
        raise TypeError(string)
    if len(parts) == 1:
        markup = abjad.Markup(parts[0])
    elif column:
        markups = [abjad.Markup(_) for _ in parts]
        markup = abjad.Markup.center_column(markups, direction=None)
    else:
        markups = [abjad.Markup(_) for _ in parts]
        markups = abjad.MarkupList(markups)
        markup = markups.line()
    if hcenter_in is not None:
        markup = markup.hcenter_in(hcenter_in)
    return markup


def markup(string):
    return indicators.Markup(string)


def short_instrument(
    string: str, hcenter_in: abjad.Number = 10, column: bool = True
) -> abjad.Markup:
    r"""
    Makes short instrument name markup.

    ..  container:: example

        Makes short instrument name markup in column:

        >>> markup = baca.markups.short_instrument("Eng. hn.")

        >>> abjad.show(markup, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(markup, strict=89)
            \markup {
                \hcenter-in
                    #10
                    "Eng. hn."
                }

    ..  container:: example

        Makes short instrument name markup in line:

        >>> markup = baca.markups.short_instrument(
        ...     "Vn. 1",
        ...     column=False,
        ...     )

        >>> abjad.show(markup, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(markup, strict=89)
            \markup {
                \hcenter-in
                    #10
                    "Vn. 1"
                }

    Centers markup horizontally in 10 spaces.
    """
    return make_instrument_name_markup(string, column=column, hcenter_in=hcenter_in)


def string_number(n: int):
    to_roman_numeral = {1: "I", 2: "II", 3: "III", 4: "IV"}
    string_number = to_roman_numeral[n]
    return indicators.Markup(string_number, direction=abjad.Down)


def string_numbers(numbers: typing.List[int],):
    to_roman_numeral = {1: "I", 2: "II", 3: "III", 4: "IV"}
    string_numbers = [to_roman_numeral[_] for _ in numbers]
    string = "+".join(string_numbers)
    return indicators.Markup(string, direction=abjad.Down)
