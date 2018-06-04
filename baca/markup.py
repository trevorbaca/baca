"""
Markup library.
"""
import abjad
import baca
import typing
from .IndicatorCommand import IndicatorCommand
from .SuiteCommand import SuiteCommand
from .Typing import Number
from .Typing import Selector


def markup(
    argument: typing.Union[str, abjad.Markup],
    selector: Selector = 'baca.phead(0)',
    direction: abjad.VerticalAlignment = abjad.Up,
    literal: bool = False,
    upright: bool = True,
    whiteout: bool = True,
    ) -> IndicatorCommand:
    r"""
    Makes markup and inserts into indicator command.

    ..  container:: example

        Attaches markup to pitched head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.markup.markup('più mosso'),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_outside_staff_priority(1000),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.outside-staff-priority = #1000                   %! OC1
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            [
                            ^ \markup {                                                              %! IC
                                \whiteout                                                            %! IC
                                    \upright                                                         %! IC
                                        "più mosso"                                                  %! IC
                                }                                                                    %! IC
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.outside-staff-priority                             %! OC2
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches markup to pitched head 0 in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.markup.markup('più mosso', baca.tuplets()[1:2].phead(0)),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_outside_staff_priority(1000),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.outside-staff-priority = #1000                   %! OC1
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            ^ \markup {                                                              %! IC
                                \whiteout                                                            %! IC
                                    \upright                                                         %! IC
                                        "più mosso"                                                  %! IC
                                }                                                                    %! IC
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.outside-staff-priority                             %! OC2
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches markup to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.markup.markup('*', baca.tuplets()[1:2].pheads()),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_outside_staff_priority(1000),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.outside-staff-priority = #1000                   %! OC1
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            ^ \markup {                                                              %! IC
                                \whiteout                                                            %! IC
                                    \upright                                                         %! IC
                                        *                                                            %! IC
                                }                                                                    %! IC
                            e''16
                            ]
                            ^ \markup {                                                              %! IC
                                \whiteout                                                            %! IC
                                    \upright                                                         %! IC
                                        *                                                            %! IC
                                }                                                                    %! IC
                            ef''4
                            ~
                            ^ \markup {                                                              %! IC
                                \whiteout                                                            %! IC
                                    \upright                                                         %! IC
                                        *                                                            %! IC
                                }                                                                    %! IC
                            ef''16
                            r16
                            af''16
                            [
                            ^ \markup {                                                              %! IC
                                \whiteout                                                            %! IC
                                    \upright                                                         %! IC
                                        *                                                            %! IC
                                }                                                                    %! IC
                            g''16
                            ]
                            ^ \markup {                                                              %! IC
                                \whiteout                                                            %! IC
                                    \upright                                                         %! IC
                                        *                                                            %! IC
                                }                                                                    %! IC
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.outside-staff-priority                             %! OC2
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Set the ``literal=True`` to pass predefined markup commands:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.markup.markup(r'\baca_triple_diamond_markup', literal=True),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_outside_staff_priority(1000),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.outside-staff-priority = #1000                   %! OC1
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            [
                            ^ \markup {                                                              %! IC
                                \whiteout                                                            %! IC
                                    \upright                                                         %! IC
                                        \baca_triple_diamond_markup                                     %! IC
                                }                                                                    %! IC
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.outside-staff-priority                             %! OC2
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Raises exception on nonstring, nonmarkup ``argument``:

        >>> baca.markup.markup(['Allegro', 'ma non troppo'])
        Traceback (most recent call last):
            ...
        Exception: MarkupLibary.__call__():
            Value of 'argument' must be str or markup.
            Not ['Allegro', 'ma non troppo'].

    """
    if direction not in (abjad.Down, abjad.Up):
        message = f'direction must be up or down (not {direction!r}).'
        raise Exception(message)
    if isinstance(argument, str):
        if literal:
            markup = abjad.Markup.from_literal(
                argument,
                direction=direction,
                )
        else:
            markup = abjad.Markup(argument, direction=direction)
    elif isinstance(argument, abjad.Markup):
        markup = abjad.new(argument, direction=direction)
    else:
        message = 'MarkupLibary.__call__():\n'
        message += "  Value of 'argument' must be str or markup.\n"
        message += f'  Not {argument!r}.'
        raise Exception(message)
    prototype = (str, abjad.Expression)
    if selector is not None and not isinstance(selector, prototype):
        message = f'selector must be string or expression'
        message += f' (not {selector!r}).'
        raise Exception(message)
    selector = selector or 'baca.phead(0)'
    if upright:
        markup = markup.upright()
    if whiteout:
        markup = markup.whiteout()
    return IndicatorCommand(
        indicators=[markup],
        selector=selector,
        )

baca_markup = markup

### PRIVATE FUNCTIONS ###

def _make_instrument_name_markup(string, space, column=True):
    if isinstance(string, str):
        parts = [string]
    elif isinstance(string, list):
        parts = string
    else:
        raise TypeError(string)
    if len(parts) == 1:
        markup = abjad.Markup(parts[0]).hcenter_in(space)
    elif column:
        markups = [abjad.Markup(_) for _ in parts]
        markup = abjad.Markup.center_column(markups, direction=None)
        markup = markup.hcenter_in(space)
    else:
        markups = [abjad.Markup(_) for _ in parts]
        markups = abjad.MarkupList(markups)
        markup = markups.line()
        markup = markup.hcenter_in(space)
    return markup

### PUBLIC METHODS ###

def accent_changes_of_direction(selector='baca.pleaf(0)'):
    string = 'accent changes of direction noticeably at each attack'
    return markup(
        string,
        selector=selector,
        )

def airtone(selector='baca.pleaf(0)'):
    return markup(
        'airtone',
        selector=selector,
        )

def allow_bowing_to_convey_accelerando(selector='baca.pleaf(0)'):
    return markup(
        'allow bowing to convey accelerando',
        selector=selector,
        )

def arco(selector='baca.pleaf(0)'):
    return markup(
        'arco',
        selector=selector,
        )

def arco_ordinario(selector='baca.pleaf(0)'):
    return markup(
        'arco ordinario',
        selector=selector,
        )

def attackless(selector='baca.pleaf(0)'):
    return markup(
        'attackless',
        selector=selector,
        )

def bow_on_tailpiece(selector='baca.pleaf(0)'):
    return markup(
        'bow on tailpiece',
        selector=selector,
        )

def bow_on_wooden_mute(selector='baca.pleaf(0)'):
    return markup(
        'bow on wooden mute',
        selector=selector,
        )

def boxed(
    string: str,
    selector: Selector = 'baca.leaf(0)',
    direction: abjad.VerticalAlignment = abjad.Up,
    ) -> IndicatorCommand:
    """
    Makes boxed markup.
    """
    markup = abjad.Markup(string)
    markup = markup.box().override(('box-padding', 0.5))
    return baca_markup(
        markup,
        selector=selector,
        direction=direction,
        )

def boxed_lines(
    strings: typing.List[str],
    selector: Selector = 'baca.leaf(0)',
    direction: abjad.VerticalAlignment = abjad.Up,
    ) -> IndicatorCommand:
    assert isinstance(strings, list), repr(strings)
    markup = abjad.MarkupList(strings).column()
    markup = markup.box().override(('box-padding', 0.5))
    return markup(
        markup,
        selector=selector,
        direction=direction,
        )

def boxed_repeat_count(
    count: int,
    selector: Selector = 'baca.leaf(0)',
    direction: abjad.VerticalAlignment = abjad.Up,
    ) -> IndicatorCommand:
    string = f'x{count}'
    markup = abjad.Markup(string)
    markup = markup.sans().bold().fontsize(6)
    markup = markup.box().override(('box-padding', 0.5))
    return baca_markup(
        markup,
        selector=selector,
        direction=direction,
        )

def clicks_per_second(
    lower: int,
    upper: int,
    selector: Selector = 'baca.pleaf(0)',
    ) -> IndicatorCommand:
    string = f'{lower}-{upper} clicks/sec.'
    return markup(
        string,
        selector=selector,
        )

def col_legno_battuto(selector='baca.pleaf(0)'):
    return markup(
        'col legno battuto',
        selector=selector,
        )

def crine(selecgtor='baca.pleaf(0))'):
    return markup(
        'crine',
        selector=selector,
        )

def delicatiss(selector='baca.pleaf(0)'):
    return markup(
        'delicatiss.',
        selector=selector,
        )

def delicatissimo(selector='baca.pleaf(0)'):
    return markup(
        'delicatissimo',
        selector=selector,
        )

def directly_on_bridge_bow_diagonally(selector='baca.pleaf(0)'):
    string = 'directly on bridge:'
    string += ' bow diagonally to produce white noise w/ no pitch'
    return markup(
        string,
        selector=selector,
        )

def directly_on_bridge_very_slow_bow(selector='baca.pleaf(0)'):
    string = 'directly on bridge:'
    string += ' very slow bow, imperceptible bow changes'
    return markup(
        string,
        selector=selector,
        )

def divisi_1_plus_3(selector='baca.pleaf(0)'):
    return markup(
        '1 + 3',
        selector=selector,
        )

def divisi_2_plus_4(selector='baca.pleaf(0)'):
    return markup(
        '2 + 4',
        selector=selector,
        )

def edition(
    not_parts: typing.Union[str, IndicatorCommand],
    only_parts: typing.Union[str, IndicatorCommand],
    selector: Selector = 'baca.pleaf(0)',
    ) -> SuiteCommand:
    """
    Makes not-parts / only-parts markup suite.
    """
    from .LibraryNS import LibraryNS
    if isinstance(not_parts, str):
        not_parts = markup(not_parts)
    assert isinstance(not_parts, IndicatorCommand)
    not_parts_ = LibraryNS.not_parts(not_parts)
    if isinstance(only_parts, str):
        only_parts = markup(only_parts)
    assert isinstance(only_parts, IndicatorCommand)
    only_parts_ = LibraryNS.only_parts(only_parts)
    return SuiteCommand(
        not_parts_,
        only_parts_,
        selector=selector,
        )

def estr_sul_pont(selector='baca.pleaf(0)'):
    return markup(
        'estr. sul pont.',
        selector=selector,
        )

def ext_pont(selector='baca.pleaf(0)'):
    return markup(
        'ext. pont.',
        selector=selector,
        )

def FB(selector='baca.pleaf(0)'):
    return markup(
        'FB',
        selector=selector,
        )

def FB_flaut(selector='baca.pleaf(0)'):
    return markup(
        'FB flaut.',
        selector=selector,
        )

def final_markup(
    places: typing.List[str],
    dates: typing.List[str],
    selector: Selector = 'baca.leaf(-1)',
    ) -> IndicatorCommand:
    string = r' \hspace #0.75 – \hspace #0.75 '.join(places)
    places_ = abjad.Markup(string)
    places_ = abjad.Markup.line([places_])
    string = r' \hspace #0.75 – \hspace #0.75 '.join(dates)
    dates_ = abjad.Markup(string)
    dates_ = abjad.Markup.line([dates_])
    markup = abjad.Markup.right_column([places_, dates_])
    markup = markup.with_color('black')
    markup = markup.override(('font-name', 'Palatino'))
    return baca_markup(
        markup,
        selector=selector,
        direction=abjad.Down,
        )

def flaut(selector='baca.pleaf(0)'):
    return markup(
        'flaut.',
        selector=selector,
        )

def flaut_partial_2(selector='baca.pleaf(0)'):
    return markup(
        'flaut. (2°)',
        selector=selector,
        )

def fluttertongue(selector='baca.pleaf(0)'):
    return markup(
        'fluttertongue',
        selector=selector,
        )

def fractional_OB(
    numerator: int,
    denominator: int,
    selector: Selector = 'baca.pleaf(0)',
    ) -> IndicatorCommand:
    string = f'{numerator}/{denominator}OB'
    return markup(
        string,
        selector=selector,
        )

def fractional_scratch(
    numerator: int,
    denominator: int,
    selector: Selector = 'baca.pleaf(0)',
    ) -> IndicatorCommand:
    string = f'{numerator}/{denominator} scratch'
    return markup(
        string,
        selector=selector,
        )

def full_bow_strokes(selector='baca.pleaf(0)'):
    return markup(
        'full bow strokes',
        selector=selector,
        )

def glissando_lentissimo(selector='baca.pleaf(0)'):
    return markup(
        'glissando lentissimo',
        selector=selector,
        )

def gridato_possibile(selector='baca.pleaf(0)'):
    return markup(
        'gridato possibile',
        selector=selector,
        )

def half_clt(selector='baca.pleaf(0)'):
    return markup(
        '1/2 clt',
        selector=selector,
        )

def instrument(
    string: str,
    hcenter_in: typing.Optional[Number] = 16,
    column: bool = True,
    ):
    r"""
    Makes instrument name markup.

    ..  container:: example

        Makes instrument name markup in column:

        >>> markup = baca.markup.instrument('Eng. horn')

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

        >>> markup = baca.markup.instrument(
        ...     'Violin 1',
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

    Returns markup.
    """
    return _make_instrument_name_markup(
        string,
        hcenter_in,
        column=column,
        )

def kn_rasg(selector='baca.pleaf(0)'):
    return markup(
        'kn. rasg.',
        selector=selector,
        )

def knuckle_rasg(selector='baca.pleaf(0)'):
    return markup(
        'knuckle rasg.',
        selector=selector,
        )

def leggieriss(selector='baca.pleaf(0)'):
    return markup(
        'leggieriss.',
        selector=selector,
        )

def leggierissimo(selector='baca.pleaf(0)'):
    return markup(
        'leggierissimo',
        selector=selector,
        )

def leggierissimo_off_string_bowing_on_staccati(selector='baca.pleaf(0)'):
    return markup(
        'leggierissimo: off-string bowing on staccati',
        selector=selector,
        )

def lh_damp(selector='baca.pleaf(0)'):
    return markup(
        'lh damp',
        selector=selector,
        )

def lh_damp_plus_half_clt(selector='baca.pleaf(0)'):
    return markup(
        'lh damp + 1/2 clt',
        selector=selector,
        )

def lhd_plus_half_clt(selector='baca.pleaf(0)'):
    return markup(
        'lhd + 1/2 clt',
        selector=selector,
        )

def lines(
    items: typing.List,
    selector: Selector = 'baca.leaf(0)',
    direction: abjad.VerticalAlignment = abjad.Up,
    no_whiteout: bool = False,
    ) -> IndicatorCommand:
    if not isinstance(items, list):
        message = f'items must be list (not {type(items).__name__}):'
        lines = ['    ' + _ for _ in format(items).split('\n')]
        lines = '\n'.join(lines)
        message += f'\n{lines}'
        raise Exception(message)
    items_ = []
    for item in items:
        if isinstance(item, (str, abjad.Markup)):
            items_.append(item)
        else:
            assert isinstance(item, IndicatorCommand)
            assert item.indicators is not None
            assert len(item.indicators) == 1
            markup = item.indicators[0]
            items_.append(markup)
    markup = abjad.MarkupList(items_).column()
    return baca_markup(
        markup,
        selector=selector,
        direction=direction,
        whiteout=not(no_whiteout),
        )

def loure(selector='baca.pleaf(0)'):
    return markup(
        'louré',
        selector=selector,
        )

def lv_possibile(selector='baca.ptail(0)'):
    return markup(
        'l.v. possibile',
        selector=selector,
        )

def molto_flautando(selector='baca.pleaf(0)'):
    return markup(
        'molto flautando',
        selector=selector,
        )

def molto_flautando_e_pont(selector='baca.pleaf(0)'):
    return markup(
        'molto flautando ed estr. sul pont.',
        selector=selector,
        )

def molto_gridato(selector='baca.pleaf(0)'):
    return markup(
        'molto gridato ed estr. sul pont.',
        selector=selector,
        )

def molto_overpressure(selector='baca.pleaf(0)'):
    return markup(
        'molto overpressure',
        selector=selector,
        )

def molto_pont_plus_vib_molto(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    selector: Selector = 'baca.pleaf(0)',
    ) -> IndicatorCommand:
    return plus_statement(
        'molto pont.',
        'vib. molto',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        selector=selector,
        )

def molto_scratch(selector='baca.pleaf(0)'):
    return markup(
        'molto scratch',
        selector=selector,
        )

def MP_XFB_flaut(selector='baca.pleaf(0)'):
    return markup(
        'MP + XFB flaut.',
        selector=selector,
        )

def nail_rasg(selector='baca.pleaf(0)'):
    return markup(
        'nail rasg.',
        selector=selector,
        )

def nail_rasgueado(selector='baca.pleaf(0)'):
    return markup(
        'nail rasgueado',
        selector=selector,
        )

def non_div(selector='baca.leaf(0)'):
    return markup(
        'non div.',
        selector=selector,
        )

def non_flaut(selector='baca.pleaf(0)'):
    return markup(
        'non flaut.',
        selector=selector,
        )

def non_flautando(selector='baca.pleaf(0)'):
    return markup(
        'non flautando',
        selector=selector,
        )

def non_flutt(selector='baca.pleaf(0)'):
    return markup(
        'non flutt.',
        selector=selector,
        )

def non_spazz(selector='baca.pleaf(0)'):
    return markup(
        'non spazz.',
        selector=selector,
        )

def nut(selector='baca.pleaf(0)'):
    return markup(
        'nut',
        selector=selector,
        )

def OB(selector='baca.pleaf(0)'):
    return markup(
        'OB',
        selector=selector,
        )

def OB_full_bow_strokes(selector='baca.pleaf(0)'):
    return markup(
        'OB + full bow strokes',
        selector=selector,
        )

def OB_no_pitch(selector='baca.pleaf(0)'):
    return markup(
        'OB (no pitch)',
        selector=selector,
        )

def OB_terminate_abruptly(selector='baca.pleaf(0)'):
    return markup(
        'OB + terminate abruptly',
        selector=selector,
        )

def OB_terminate_each_note_abruptly(selector='baca.pleaf(0)'):
    return markup(
        'OB + terminate each note abruptly',
        selector=selector,
        )

def off_string_bowing_on_staccati(selector='baca.pleaf(0)'):
    return markup(
        'off-string bowing on staccati',
        selector=selector,
        )

def one_click_every(lower, upper, selector='baca.pleaf(0)'):
    string = f'1 click/{lower}-{upper} sec.'
    return markup(
        string,
        selector=selector,
        )

def ord(selector='baca.pleaf(0)'):
    return markup(
        'ord.',
        selector=selector,
        )

def ord_poco_scratch(selector='baca.pleaf(0)'):
    return markup(
        'ord. + poco scratch',
        selector=selector,
        )

def ord_senza_scratch(selector='baca.pleaf(0)'):
    return markup(
        'ord. (senza scratch)',
        selector=selector,
        )

def ordinario(selector='baca.pleaf(0)'):
    return markup(
        'ordinario',
        selector=selector,
        )

def overblow(selector='baca.pleaf(0)'):
    return markup(
        'overblow',
        selector=selector,
        )

def P_XFB_flaut(selector='baca.pleaf(0)'):
    return markup(
        'P + XFB flaut.',
        selector=selector,
        )

def pizz(selector='baca.pleaf(0)'):
    return markup(
        'pizz.',
        selector=selector,
        )

def plus_statement(
    string_1: str,
    string_2: str,
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    selector: Selector = 'baca.pleaf(0)',
    ):
    if parenthesize_first and parenthesize_last:
        composite_string = f'({string_1} + {string_2})'
    elif parenthesize_first and not parenthesize_last:
        composite_string = f'({string_1}+) {string_2}'
    elif not parenthesize_first and parenthesize_last:
        composite_string = f'{string_1} (+{string_2})'
    else:
        composite_string = f'{string_1} + {string_2}'
    return markup(
        composite_string,
        selector=selector,
        )

def PO(selector='baca.pleaf(0)'):
    return markup(
        'PO',
        selector=selector,
        )

def PO_FB_flaut(selector='baca.pleaf(0)'):
    return markup(
        'PO + FB flaut.',
        selector=selector,
        )

def po_meno_scratch(selector='baca.pleaf(0)'):
    return markup(
        "po' meno scratch",
        selector=selector,
        )

def PO_NBS(selector='baca.pleaf(0)'):
    return markup(
        'PO + NBS',
        selector=selector,
        )

def PO_plus_non_vib(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    selector: Selector = 'baca.pleaf(0)',
    ) -> IndicatorCommand:
    return plus_statement(
        'PO',
        'non vib.',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        selector=selector,
        )

def PO_plus_poco_vib(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    selector: Selector = 'baca.pleaf(0)',
    ) -> IndicatorCommand:
    return plus_statement(
        'PO',
        'poco vib.',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        selector=selector,
        )

def PO_scratch(selector='baca.pleaf(0)'):
    return markup(
        'PO + scratch',
        selector=selector,
        )

def PO_slow_bow(selector='baca.pleaf(0)'):
    return markup(
        'PO + slow bow (poco scratch)',
        selector=selector,
        )

def PO_XFB_flaut(selector='baca.pleaf(0)'):
    return markup(
        'PO + XFB flaut.',
        selector=selector,
        )

def pochiss_pont(selector='baca.pleaf(0)'):
    return markup(
        'pochiss. pont.',
        selector=selector,
        )

def pochiss_scratch(selector='baca.pleaf(0)'):
    return markup(
        'pochiss. scratch',
        selector=selector,
        )

def pochiss_vib(selector='baca.pleaf(0)'):
    return markup(
        'pochiss. vib.',
        selector=selector,
        )

def poco_overpressure(selector='baca.pleaf(0)'):
    return markup(
        'poco overpressure',
        selector=selector,
        )

def poco_pont_plus_non_vib(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    selector: Selector = 'baca.pleaf(0)',
    ) -> IndicatorCommand:
    return plus_statement(
        'poco pont.',
        'non vib.',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        selector=selector,
        )

def poco_pont_plus_sub_non_vib(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    selector: Selector = 'baca.pleaf(0)',
    ) -> IndicatorCommand:
    return plus_statement(
        'poco pont.',
        'sub. non vib.',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        selector=selector,
        )

def poco_pont_plus_sub_vib_mod(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    selector: Selector = 'baca.pleaf(0)',
    ) -> IndicatorCommand:
    return plus_statement(
        'poco pont.',
        'sub. vib. mod.',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        selector=selector,
        )

def poco_pont_plus_vib_mod(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    selector: Selector = 'baca.pleaf(0)',
    ) -> IndicatorCommand:
    return plus_statement(
        'poco pont.',
        'vib. mod.',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        selector=selector,
        )

def poco_rasp_partial_2(selector='baca.pleaf(0)'):
    return markup(
        'poco rasp (2°)',
        selector=selector,
        )

def poco_scratch(selector='baca.pleaf(0)'):
    return markup(
        'poco scratch',
        selector=selector,
        )

def pont(selector='baca.pleaf(0)'):
    return markup(
        'pont.',
        selector=selector,
        )

def pont_XFB(selector='baca.pleaf(0)'):
    return markup(
        'pont. + XFB',
        selector=selector,
        )

def pont_XFB_flaut(selector='baca.pleaf(0)'):
    return markup(
        'pont. + XFB flaut.',
        selector=selector,
        )

def ponticello(selector='baca.pleaf(0)'):
    return markup(
        'ponticello',
        selector=selector,
        )

def pos_ord(selector='baca.pleaf(0)'):
    return markup(
        'pos. ord.',
        selector=selector,
        )

def pos_ord_poco_scratch(selector='baca.pleaf(0)'):
    return markup(
        'pos. ord. + poco scratch',
        selector=selector,
        )

def pos_ord_senza_vib(selector='baca.pleaf(0)'):
    return markup(
        'pos. ord. + senza vib',
        selector=selector,
        )

def pos_ord_vib_poco(selector='baca.pleaf(0)'):
    return markup(
        'pos. ord. + vib. poco',
        selector=selector,
        )

def pos_ord_XFB(selector='baca.pleaf(0)'):
    return markup(
        'pos. ord. + XFB',
        selector=selector,
        )

def pos_ord_XFB_flaut(selector='baca.pleaf(0)'):
    return markup(
        'pos. ord. + XFB flaut.',
        selector=selector,
        )

def pP_XFB_flaut(selector='baca.pleaf(0)'):
    return markup(
        'pP + XFB flaut.',
        selector=selector,
        )

def pres_de_la_table(selector='baca.pleaf(0)'):
    return boxed(
        'près de la table',
        selector=selector,
        )

def pT_XFB_flaut(selector='baca.pleaf(0)'):
    return markup(
        'pT + XFB flaut.',
        selector=selector,
        )

def put_reed_back_in(selector='baca.leaf(0)'):
    return boxed(
        'put reed back in',
        selector=selector,
        )

def rasp(selector='baca.pleaf(0)'):
    return markup(
        'rasp',
        selector=selector,
        )

def rasp_partial_2(selector='baca.pleaf(0)'):
    return markup(
        'rasp (2°)',
        selector=selector,
        )

def remove_reed(selector='baca.leaf(0)'):
    return boxed(
        'remove reed',
        selector=selector,
        )

def remove_staple(selector='baca.leaf(0)'):
    return boxed(
        'remove staple',
        selector=selector,
        )

def scratch_moltiss(selector='baca.pleaf(0)'):
    return markup(
        'scratch moltiss.',
        selector=selector,
        )

def senza_pedale(selector='baca.pleaf(0)'):
    return markup(
        'senza pedale',
        selector=selector,
        )

def senza_scratch(selector='baca.pleaf(0)'):
    return markup(
        'senza scratch',
        selector=selector,
        )

def senza_vib(selector='baca.pleaf(0)'):
    return markup(
        'senza vib.',
        selector=selector,
        )

def shakers(selector='baca.leaf(0)'):
    return markup(
        'shakers',
        selector=selector,
        )

def short_instrument(
    string: str,
    hcenter_in: Number = 10,
    column: bool = True,
    ) -> IndicatorCommand:
    r"""
    Makes short instrument name markup.

    ..  container:: example

        Makes short instrument name markup in column:

        >>> markup = baca.markup.short_instrument('Eng. hn.')

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

        >>> markup = baca.markup.short_instrument(
        ...     'Vn. 1',
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

    Returns markup.
    """
    return _make_instrument_name_markup(
        string,
        hcenter_in,
        column=column,
        )

def sparse_clicks(selector='baca.pleaf(0)'):
    first_line = abjad.Markup(
        'sparse, individual clicks with extremely slow bow')
    first_line = first_line.line()
    second_line = abjad.Markup('(1-2/sec. in irregular rhythm)').line()
    markup = abjad.Markup.column([first_line, second_line])
    return baca_markup(
        markup,
        selector=selector,
        )

def spazz(selector='baca.pleaf(0)'):
    return markup(
        'spazz.',
        selector=selector,
        )

def spazzolato(selector='baca.pleaf(0)'):
    return markup(
        'spazzolato',
        selector=selector,
        )

def spazzolato_1_2_clt(selector='baca.pleaf(0)'):
    return markup(
        'spazzolato (1/2 clt)',
        selector=selector,
        )

def still(selector='baca.leaf(0)'):
    return markup(
        'still',
        selector=selector,
        )

def string_number(
    n: int,
    selector: Selector = 'baca.pleaf(0)',
    ) -> IndicatorCommand:
    to_roman_numeral = {
        1: 'I',
        2: 'II',
        3: 'III',
        4: 'IV',
        }
    string_number = to_roman_numeral[n]
    return markup(
        string_number,
        selector=selector,
        direction=abjad.Down,
        )

def string_numbers(
    numbers: typing.List[int],
    selector: Selector = 'baca.pleaf(0)',
    ) -> IndicatorCommand:
    to_roman_numeral = {
        1: 'I',
        2: 'II',
        3: 'III',
        4: 'IV',
        }
    string_numbers = [to_roman_numeral[_] for _ in numbers]
    string = '+'.join(string_numbers)
    return markup(
        string,
        selector=selector,
        direction=abjad.Down,
        )

def subito_non_armonichi_e_non_gridato(selector='baca.pleaf(0)'):
    return markup(
        'subito non armonichi e non gridato',
        selector=selector,
        )

def subito_ordinario(selector='baca.pleaf(0)'):
    return markup(
        'subito ordinario',
        selector=selector,
        )

def tamb_tr(selector='baca.pleaf(0)'):
    return markup(
        'tamb. tr.',
        selector=selector,
        )

def tasto(selector='baca.pleaf(0)'):
    return markup(
        'tasto',
        selector=selector,
        )

def tasto_FB(selector='baca.pleaf(0)'):
    return markup(
        'tasto + FB',
        selector=selector,
        )

def tasto_FB_flaut(selector='baca.pleaf(0)'):
    return markup(
        'tasto + FB flaut.',
        selector=selector,
        )

def tasto_fractional_scratch(
    numerator: int,
    denominator: int,
    selector: Selector = 'baca.pleaf(0)',
    ) -> IndicatorCommand:
    string = f'tasto + {numerator}/{denominator} scratch'
    return markup(
        string,
        selector=selector,
        )

def tasto_half_scratch(selector='baca.pleaf(0)'):
    return markup(
        'tasto + 1/2 scratch',
        selector=selector,
        )

def tasto_moltiss(selector='baca.pleaf(0)'):
    return markup(
        'tasto moltiss.',
        selector=selector,
        )

def tasto_NBS(selector='baca.pleaf(0)'):
    return markup(
        'tasto + NBS',
        selector=selector,
        )

def tasto_plus_non_vib(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    selector: Selector = 'baca.pleaf(0)',
    ) -> IndicatorCommand:
    return plus_statement(
        'tasto',
        'non vib.',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        selector=selector,
        )

def tasto_plus_pochiss_scratch(selector='baca.pleaf(0)'):
    return markup(
        'tasto + pochiss. scratch',
        selector=selector,
        )

def tasto_plus_poco_scratch(selector='baca.pleaf(0)'):
    return markup(
        'tasto + poco scratch',
        selector=selector,
        )

def tasto_plus_poco_vib(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    selector: Selector = 'baca.pleaf(0)',
    ) -> IndicatorCommand:
    return plus_statement(
        'tasto',
        'poco vib.',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        selector=selector,
        )

def tasto_plus_scratch_moltiss(selector='baca.pleaf(0)'):
    return markup(
        'tasto + scratch moltiss.',
        selector=selector,
        )

def tasto_poss(selector='baca.pleaf(0)'):
    return markup(
        'tasto poss.',
        selector=selector,
        )

def tasto_senza_vib(selector='baca.pleaf(0)'):
    return markup(
        'tasto + senza vib.',
        selector=selector,
        )

def tasto_slow_bow(selector='baca.pleaf(0)'):
    return markup(
        'tasto + slow bow (poco scratch)',
        selector=selector,
        )

def tasto_XFB(selector='baca.pleaf(0)'):
    return markup(
        'tasto + XFB',
        selector=selector,
        )

def tasto_XFB_flaut(selector='baca.pleaf(0)'):
    return markup(
        'tasto + XFB flaut.',
        selector=selector,
        )

def terminate_abruptly(selector='baca.pleaf(0)'):
    return markup(
        'terminate abruptly',
        selector=selector,
        )

def terminate_each_note_abruptly(selector='baca.pleaf(0)'):
    return markup(
        'terminate each note abruptly',
        selector=selector,
        )

def trans(selector='baca.pleaf(0)'):
    return markup(
        'trans.',
        selector=selector,
        )

def trem_flaut_tast(selector='baca.pleaf(0)'):
    return markup(
        'trem. flaut. tast.',
        selector=selector,
        )

def vib_moltiss(selector='baca.pleaf(0)'):
    return markup(
        'vib. moltiss.',
        selector=selector,
        )

def vib_pochiss(selector='baca.pleaf(0)'):
    return markup(
        'vib. pochiss.',
        selector=selector,
        )

def vib_poco(selector='baca.pleaf(0)'):
    return markup(
        'vib. poco.',
        selector=selector,
        )

def XFB(selector='baca.pleaf(0)'):
    return markup(
        'XFB',
        selector=selector,
        )

def XFB_flaut(selector='baca.pleaf(0)'):
    return markup(
        'XFB flaut.',
        selector=selector,
        )

def XFB_plus_pochiss_pont(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    selector: Selector = 'baca.pleaf(0)',
    ) -> IndicatorCommand:
    return plus_statement(
        'XFB',
        'pochiss. pont.',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        selector=selector,
        )

def XFB_plus_tasto(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    selector: Selector = 'baca.pleaf(0)',
    ) -> IndicatorCommand:
    return plus_statement(
        'XFB',
        'tasto',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        selector=selector,
        )

def XFB_sempre(selector='baca.pleaf(0)'):
    return markup(
        'XFB sempre',
        selector=selector,
        )

def XP(selector='baca.pleaf(0)'):
    return markup(
        'XP',
        selector=selector,
        )

def XP_FB(selector='baca.pleaf(0)'):
    return markup(
        'XP + FB',
        selector=selector,
        )

def XP_FB_flaut(selector='baca.pleaf(0)'):
    return markup(
        'XP + FB flaut.',
        selector=selector,
        )

def XP_full_bow_strokes(selector='baca.pleaf(0)'):
    return markup(
        'XP + full bow strokes',
        selector=selector,
        )

def XP_XFB(selector='baca.pleaf(0)'):
    return markup(
        'XP + XFB',
        selector=selector,
        )

def XP_XFB_flaut(selector='baca.pleaf(0)'):
    return markup(
        'XP + XFB flaut.',
        selector=selector,
        )

def XT(selector='baca.pleaf(0)'):
    return markup(
        'XT',
        selector=selector,
        )
