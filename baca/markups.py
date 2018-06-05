"""
Markup library.
"""
import abjad
import baca
import typing
from . import library
from .IndicatorCommand import IndicatorCommand
from .SuiteCommand import SuiteCommand
from .Typing import Number
from .Typing import Selector


def accent_changes_of_direction(selector='baca.pleaf(0)'):
    string = 'accent changes of direction noticeably at each attack'
    return library.markup(
        string,
        selector=selector,
        )

def airtone(selector='baca.pleaf(0)'):
    return library.markup(
        'airtone',
        selector=selector,
        )

def allow_bowing_to_convey_accelerando(selector='baca.pleaf(0)'):
    return library.markup(
        'allow bowing to convey accelerando',
        selector=selector,
        )

def arco(selector='baca.pleaf(0)'):
    return library.markup(
        'arco',
        selector=selector,
        )

def arco_ordinario(selector='baca.pleaf(0)'):
    return library.markup(
        'arco ordinario',
        selector=selector,
        )

def attackless(selector='baca.pleaf(0)'):
    return library.markup(
        'attackless',
        selector=selector,
        )

def bow_on_tailpiece(selector='baca.pleaf(0)'):
    return library.markup(
        'bow on tailpiece',
        selector=selector,
        )

def bow_on_wooden_mute(selector='baca.pleaf(0)'):
    return library.markup(
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
    return library.markup(
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
    return library.markup(
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
    return library.markup(
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
    return library.markup(
        string,
        selector=selector,
        )

def col_legno_battuto(selector='baca.pleaf(0)'):
    return library.markup(
        'col legno battuto',
        selector=selector,
        )

def crine(selecgtor='baca.pleaf(0))'):
    return library.markup(
        'crine',
        selector=selector,
        )

def delicatiss(selector='baca.pleaf(0)'):
    return library.markup(
        'delicatiss.',
        selector=selector,
        )

def delicatissimo(selector='baca.pleaf(0)'):
    return library.markup(
        'delicatissimo',
        selector=selector,
        )

def directly_on_bridge_bow_diagonally(selector='baca.pleaf(0)'):
    string = 'directly on bridge:'
    string += ' bow diagonally to produce white noise w/ no pitch'
    return library.markup(
        string,
        selector=selector,
        )

def directly_on_bridge_very_slow_bow(selector='baca.pleaf(0)'):
    string = 'directly on bridge:'
    string += ' very slow bow, imperceptible bow changes'
    return library.markup(
        string,
        selector=selector,
        )

def divisi_1_plus_3(selector='baca.pleaf(0)'):
    return library.markup(
        '1 + 3',
        selector=selector,
        )

def divisi_2_plus_4(selector='baca.pleaf(0)'):
    return library.markup(
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
    if isinstance(not_parts, str):
        not_parts = library.markup(not_parts)
    assert isinstance(not_parts, IndicatorCommand)
    not_parts_ = library.not_parts(not_parts)
    if isinstance(only_parts, str):
        only_parts = library.markup(only_parts)
    assert isinstance(only_parts, IndicatorCommand)
    only_parts_ = library.only_parts(only_parts)
    return SuiteCommand(
        not_parts_,
        only_parts_,
        selector=selector,
        )

def estr_sul_pont(selector='baca.pleaf(0)'):
    return library.markup(
        'estr. sul pont.',
        selector=selector,
        )

def ext_pont(selector='baca.pleaf(0)'):
    return library.markup(
        'ext. pont.',
        selector=selector,
        )

def FB(selector='baca.pleaf(0)'):
    return library.markup(
        'FB',
        selector=selector,
        )

def FB_flaut(selector='baca.pleaf(0)'):
    return library.markup(
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
    return library.markup(
        markup,
        selector=selector,
        direction=abjad.Down,
        )

def flaut(selector='baca.pleaf(0)'):
    return library.markup(
        'flaut.',
        selector=selector,
        )

def flaut_partial_2(selector='baca.pleaf(0)'):
    return library.markup(
        'flaut. (2°)',
        selector=selector,
        )

def fluttertongue(selector='baca.pleaf(0)'):
    return library.markup(
        'fluttertongue',
        selector=selector,
        )

def fractional_OB(
    numerator: int,
    denominator: int,
    selector: Selector = 'baca.pleaf(0)',
    ) -> IndicatorCommand:
    string = f'{numerator}/{denominator}OB'
    return library.markup(
        string,
        selector=selector,
        )

def fractional_scratch(
    numerator: int,
    denominator: int,
    selector: Selector = 'baca.pleaf(0)',
    ) -> IndicatorCommand:
    string = f'{numerator}/{denominator} scratch'
    return library.markup(
        string,
        selector=selector,
        )

def full_bow_strokes(selector='baca.pleaf(0)'):
    return library.markup(
        'full bow strokes',
        selector=selector,
        )

def glissando_lentissimo(selector='baca.pleaf(0)'):
    return library.markup(
        'glissando lentissimo',
        selector=selector,
        )

def gridato_possibile(selector='baca.pleaf(0)'):
    return library.markup(
        'gridato possibile',
        selector=selector,
        )

def half_clt(selector='baca.pleaf(0)'):
    return library.markup(
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

        >>> markup = baca.markups.instrument('Eng. horn')

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
    return make_instrument_name_markup(
        string,
        hcenter_in,
        column=column,
        )

def kn_rasg(selector='baca.pleaf(0)'):
    return library.markup(
        'kn. rasg.',
        selector=selector,
        )

def knuckle_rasg(selector='baca.pleaf(0)'):
    return library.markup(
        'knuckle rasg.',
        selector=selector,
        )

def leggieriss(selector='baca.pleaf(0)'):
    return library.markup(
        'leggieriss.',
        selector=selector,
        )

def leggierissimo(selector='baca.pleaf(0)'):
    return library.markup(
        'leggierissimo',
        selector=selector,
        )

def leggierissimo_off_string_bowing_on_staccati(selector='baca.pleaf(0)'):
    return library.markup(
        'leggierissimo: off-string bowing on staccati',
        selector=selector,
        )

def lh_damp(selector='baca.pleaf(0)'):
    return library.markup(
        'lh damp',
        selector=selector,
        )

def lh_damp_plus_half_clt(selector='baca.pleaf(0)'):
    return library.markup(
        'lh damp + 1/2 clt',
        selector=selector,
        )

def lhd_plus_half_clt(selector='baca.pleaf(0)'):
    return library.markup(
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
    return library.markup(
        markup,
        selector=selector,
        direction=direction,
        whiteout=not(no_whiteout),
        )

def loure(selector='baca.pleaf(0)'):
    return library.markup(
        'louré',
        selector=selector,
        )

def lv_possibile(selector='baca.ptail(0)'):
    return library.markup(
        'l.v. possibile',
        selector=selector,
        )

def make_instrument_name_markup(string, space, column=True):
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

def molto_flautando(selector='baca.pleaf(0)'):
    return library.markup(
        'molto flautando',
        selector=selector,
        )

def molto_flautando_e_pont(selector='baca.pleaf(0)'):
    return library.markup(
        'molto flautando ed estr. sul pont.',
        selector=selector,
        )

def molto_gridato(selector='baca.pleaf(0)'):
    return library.markup(
        'molto gridato ed estr. sul pont.',
        selector=selector,
        )

def molto_overpressure(selector='baca.pleaf(0)'):
    return library.markup(
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
    return library.markup(
        'molto scratch',
        selector=selector,
        )

def MP_XFB_flaut(selector='baca.pleaf(0)'):
    return library.markup(
        'MP + XFB flaut.',
        selector=selector,
        )

def nail_rasg(selector='baca.pleaf(0)'):
    return library.markup(
        'nail rasg.',
        selector=selector,
        )

def nail_rasgueado(selector='baca.pleaf(0)'):
    return library.markup(
        'nail rasgueado',
        selector=selector,
        )

def non_div(selector='baca.leaf(0)'):
    return library.markup(
        'non div.',
        selector=selector,
        )

def non_flaut(selector='baca.pleaf(0)'):
    return library.markup(
        'non flaut.',
        selector=selector,
        )

def non_flautando(selector='baca.pleaf(0)'):
    return library.markup(
        'non flautando',
        selector=selector,
        )

def non_flutt(selector='baca.pleaf(0)'):
    return library.markup(
        'non flutt.',
        selector=selector,
        )

def non_spazz(selector='baca.pleaf(0)'):
    return library.markup(
        'non spazz.',
        selector=selector,
        )

def nut(selector='baca.pleaf(0)'):
    return library.markup(
        'nut',
        selector=selector,
        )

def OB(selector='baca.pleaf(0)'):
    return library.markup(
        'OB',
        selector=selector,
        )

def OB_full_bow_strokes(selector='baca.pleaf(0)'):
    return library.markup(
        'OB + full bow strokes',
        selector=selector,
        )

def OB_no_pitch(selector='baca.pleaf(0)'):
    return library.markup(
        'OB (no pitch)',
        selector=selector,
        )

def OB_terminate_abruptly(selector='baca.pleaf(0)'):
    return library.markup(
        'OB + terminate abruptly',
        selector=selector,
        )

def OB_terminate_each_note_abruptly(selector='baca.pleaf(0)'):
    return library.markup(
        'OB + terminate each note abruptly',
        selector=selector,
        )

def off_string_bowing_on_staccati(selector='baca.pleaf(0)'):
    return library.markup(
        'off-string bowing on staccati',
        selector=selector,
        )

def one_click_every(lower, upper, selector='baca.pleaf(0)'):
    string = f'1 click/{lower}-{upper} sec.'
    return library.markup(
        string,
        selector=selector,
        )

def ord(selector='baca.pleaf(0)'):
    return library.markup(
        'ord.',
        selector=selector,
        )

def ord_poco_scratch(selector='baca.pleaf(0)'):
    return library.markup(
        'ord. + poco scratch',
        selector=selector,
        )

def ord_senza_scratch(selector='baca.pleaf(0)'):
    return library.markup(
        'ord. (senza scratch)',
        selector=selector,
        )

def ordinario(selector='baca.pleaf(0)'):
    return library.markup(
        'ordinario',
        selector=selector,
        )

def overblow(selector='baca.pleaf(0)'):
    return library.markup(
        'overblow',
        selector=selector,
        )

def P_XFB_flaut(selector='baca.pleaf(0)'):
    return library.markup(
        'P + XFB flaut.',
        selector=selector,
        )

def pizz(selector='baca.pleaf(0)'):
    return library.markup(
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
    return library.markup(
        composite_string,
        selector=selector,
        )

def PO(selector='baca.pleaf(0)'):
    return library.markup(
        'PO',
        selector=selector,
        )

def PO_FB_flaut(selector='baca.pleaf(0)'):
    return library.markup(
        'PO + FB flaut.',
        selector=selector,
        )

def po_meno_scratch(selector='baca.pleaf(0)'):
    return library.markup(
        "po' meno scratch",
        selector=selector,
        )

def PO_NBS(selector='baca.pleaf(0)'):
    return library.markup(
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
    return library.markup(
        'PO + scratch',
        selector=selector,
        )

def PO_slow_bow(selector='baca.pleaf(0)'):
    return library.markup(
        'PO + slow bow (poco scratch)',
        selector=selector,
        )

def PO_XFB_flaut(selector='baca.pleaf(0)'):
    return library.markup(
        'PO + XFB flaut.',
        selector=selector,
        )

def pochiss_pont(selector='baca.pleaf(0)'):
    return library.markup(
        'pochiss. pont.',
        selector=selector,
        )

def pochiss_scratch(selector='baca.pleaf(0)'):
    return library.markup(
        'pochiss. scratch',
        selector=selector,
        )

def pochiss_vib(selector='baca.pleaf(0)'):
    return library.markup(
        'pochiss. vib.',
        selector=selector,
        )

def poco_overpressure(selector='baca.pleaf(0)'):
    return library.markup(
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
    return library.markup(
        'poco rasp (2°)',
        selector=selector,
        )

def poco_scratch(selector='baca.pleaf(0)'):
    return library.markup(
        'poco scratch',
        selector=selector,
        )

def pont(selector='baca.pleaf(0)'):
    return library.markup(
        'pont.',
        selector=selector,
        )

def pont_XFB(selector='baca.pleaf(0)'):
    return library.markup(
        'pont. + XFB',
        selector=selector,
        )

def pont_XFB_flaut(selector='baca.pleaf(0)'):
    return library.markup(
        'pont. + XFB flaut.',
        selector=selector,
        )

def ponticello(selector='baca.pleaf(0)'):
    return library.markup(
        'ponticello',
        selector=selector,
        )

def pos_ord(selector='baca.pleaf(0)'):
    return library.markup(
        'pos. ord.',
        selector=selector,
        )

def pos_ord_poco_scratch(selector='baca.pleaf(0)'):
    return library.markup(
        'pos. ord. + poco scratch',
        selector=selector,
        )

def pos_ord_senza_vib(selector='baca.pleaf(0)'):
    return library.markup(
        'pos. ord. + senza vib',
        selector=selector,
        )

def pos_ord_vib_poco(selector='baca.pleaf(0)'):
    return library.markup(
        'pos. ord. + vib. poco',
        selector=selector,
        )

def pos_ord_XFB(selector='baca.pleaf(0)'):
    return library.markup(
        'pos. ord. + XFB',
        selector=selector,
        )

def pos_ord_XFB_flaut(selector='baca.pleaf(0)'):
    return library.markup(
        'pos. ord. + XFB flaut.',
        selector=selector,
        )

def pP_XFB_flaut(selector='baca.pleaf(0)'):
    return library.markup(
        'pP + XFB flaut.',
        selector=selector,
        )

def pres_de_la_table(selector='baca.pleaf(0)'):
    return boxed(
        'près de la table',
        selector=selector,
        )

def pT_XFB_flaut(selector='baca.pleaf(0)'):
    return library.markup(
        'pT + XFB flaut.',
        selector=selector,
        )

def put_reed_back_in(selector='baca.leaf(0)'):
    return boxed(
        'put reed back in',
        selector=selector,
        )

def rasp(selector='baca.pleaf(0)'):
    return library.markup(
        'rasp',
        selector=selector,
        )

def rasp_partial_2(selector='baca.pleaf(0)'):
    return library.markup(
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
    return library.markup(
        'scratch moltiss.',
        selector=selector,
        )

def senza_pedale(selector='baca.pleaf(0)'):
    return library.markup(
        'senza pedale',
        selector=selector,
        )

def senza_scratch(selector='baca.pleaf(0)'):
    return library.markup(
        'senza scratch',
        selector=selector,
        )

def senza_vib(selector='baca.pleaf(0)'):
    return library.markup(
        'senza vib.',
        selector=selector,
        )

def shakers(selector='baca.leaf(0)'):
    return library.markup(
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

        >>> markup = baca.markups.short_instrument('Eng. hn.')

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
    return make_instrument_name_markup(
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
    return library.markup(
        markup,
        selector=selector,
        )

def spazz(selector='baca.pleaf(0)'):
    return library.markup(
        'spazz.',
        selector=selector,
        )

def spazzolato(selector='baca.pleaf(0)'):
    return library.markup(
        'spazzolato',
        selector=selector,
        )

def spazzolato_1_2_clt(selector='baca.pleaf(0)'):
    return library.markup(
        'spazzolato (1/2 clt)',
        selector=selector,
        )

def still(selector='baca.leaf(0)'):
    return library.markup(
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
    return library.markup(
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
    return library.markup(
        string,
        selector=selector,
        direction=abjad.Down,
        )

def subito_non_armonichi_e_non_gridato(selector='baca.pleaf(0)'):
    return library.markup(
        'subito non armonichi e non gridato',
        selector=selector,
        )

def subito_ordinario(selector='baca.pleaf(0)'):
    return library.markup(
        'subito ordinario',
        selector=selector,
        )

def tamb_tr(selector='baca.pleaf(0)'):
    return library.markup(
        'tamb. tr.',
        selector=selector,
        )

def tasto(selector='baca.pleaf(0)'):
    return library.markup(
        'tasto',
        selector=selector,
        )

def tasto_FB(selector='baca.pleaf(0)'):
    return library.markup(
        'tasto + FB',
        selector=selector,
        )

def tasto_FB_flaut(selector='baca.pleaf(0)'):
    return library.markup(
        'tasto + FB flaut.',
        selector=selector,
        )

def tasto_fractional_scratch(
    numerator: int,
    denominator: int,
    selector: Selector = 'baca.pleaf(0)',
    ) -> IndicatorCommand:
    string = f'tasto + {numerator}/{denominator} scratch'
    return library.markup(
        string,
        selector=selector,
        )

def tasto_half_scratch(selector='baca.pleaf(0)'):
    return library.markup(
        'tasto + 1/2 scratch',
        selector=selector,
        )

def tasto_moltiss(selector='baca.pleaf(0)'):
    return library.markup(
        'tasto moltiss.',
        selector=selector,
        )

def tasto_NBS(selector='baca.pleaf(0)'):
    return library.markup(
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
    return library.markup(
        'tasto + pochiss. scratch',
        selector=selector,
        )

def tasto_plus_poco_scratch(selector='baca.pleaf(0)'):
    return library.markup(
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
    return library.markup(
        'tasto + scratch moltiss.',
        selector=selector,
        )

def tasto_poss(selector='baca.pleaf(0)'):
    return library.markup(
        'tasto poss.',
        selector=selector,
        )

def tasto_senza_vib(selector='baca.pleaf(0)'):
    return library.markup(
        'tasto + senza vib.',
        selector=selector,
        )

def tasto_slow_bow(selector='baca.pleaf(0)'):
    return library.markup(
        'tasto + slow bow (poco scratch)',
        selector=selector,
        )

def tasto_XFB(selector='baca.pleaf(0)'):
    return library.markup(
        'tasto + XFB',
        selector=selector,
        )

def tasto_XFB_flaut(selector='baca.pleaf(0)'):
    return library.markup(
        'tasto + XFB flaut.',
        selector=selector,
        )

def terminate_abruptly(selector='baca.pleaf(0)'):
    return library.markup(
        'terminate abruptly',
        selector=selector,
        )

def terminate_each_note_abruptly(selector='baca.pleaf(0)'):
    return library.markup(
        'terminate each note abruptly',
        selector=selector,
        )

def trans(selector='baca.pleaf(0)'):
    return library.markup(
        'trans.',
        selector=selector,
        )

def trem_flaut_tast(selector='baca.pleaf(0)'):
    return library.markup(
        'trem. flaut. tast.',
        selector=selector,
        )

def vib_moltiss(selector='baca.pleaf(0)'):
    return library.markup(
        'vib. moltiss.',
        selector=selector,
        )

def vib_pochiss(selector='baca.pleaf(0)'):
    return library.markup(
        'vib. pochiss.',
        selector=selector,
        )

def vib_poco(selector='baca.pleaf(0)'):
    return library.markup(
        'vib. poco.',
        selector=selector,
        )

def XFB(selector='baca.pleaf(0)'):
    return library.markup(
        'XFB',
        selector=selector,
        )

def XFB_flaut(selector='baca.pleaf(0)'):
    return library.markup(
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
    return library.markup(
        'XFB sempre',
        selector=selector,
        )

def XP(selector='baca.pleaf(0)'):
    return library.markup(
        'XP',
        selector=selector,
        )

def XP_FB(selector='baca.pleaf(0)'):
    return library.markup(
        'XP + FB',
        selector=selector,
        )

def XP_FB_flaut(selector='baca.pleaf(0)'):
    return library.markup(
        'XP + FB flaut.',
        selector=selector,
        )

def XP_full_bow_strokes(selector='baca.pleaf(0)'):
    return library.markup(
        'XP + full bow strokes',
        selector=selector,
        )

def XP_XFB(selector='baca.pleaf(0)'):
    return library.markup(
        'XP + XFB',
        selector=selector,
        )

def XP_XFB_flaut(selector='baca.pleaf(0)'):
    return library.markup(
        'XP + XFB flaut.',
        selector=selector,
        )

def XT(selector='baca.pleaf(0)'):
    return library.markup(
        'XT',
        selector=selector,
        )
