"""
Markups library.
"""
import abjad
import baca
import typing
from .Typing import Number
from .Typing import Selector


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

def accent_changes_of_direction(selector='baca.pleaf(0)'):
    string = 'accent changes of direction noticeably at each attack'
    return abjad.Markup(
        string,
        selector=selector,
        )

def airtone(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'airtone',
        selector=selector,
        )

def allow_bowing_to_convey_accelerando(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'allow bowing to convey accelerando',
        selector=selector,
        )

def arco(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'arco',
        selector=selector,
        )

def arco_ordinario(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'arco ordinario',
        selector=selector,
        )

def attackless(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'attackless',
        selector=selector,
        )

def bow_on_tailpiece(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'bow on tailpiece',
        selector=selector,
        )

def bow_on_wooden_mute(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'bow on wooden mute',
        selector=selector,
        )

def boxed(
    string: str,
    selector: Selector = 'baca.leaf(0)',
    direction: abjad.VerticalAlignment = abjad.Up,
    ):
    """
    Makes boxed markup.
    """
    markup = abjad.Markup(string)
    markup = markup.box().override(('box-padding', 0.5))
    return abjad.Markup(
        markup,
        selector=selector,
        direction=direction,
        )

def boxed_lines(
    strings: typing.List[str],
    selector: Selector = 'baca.leaf(0)',
    direction: abjad.VerticalAlignment = abjad.Up,
    ):
    assert isinstance(strings, list), repr(strings)
    markup = abjad.MarkupList(strings).column()
    markup = markup.box().override(('box-padding', 0.5))
    return abjad.Markup(
        markup,
        selector=selector,
        direction=direction,
        )

def boxed_repeat_count(
    count: int,
    selector: Selector = 'baca.leaf(0)',
    direction: abjad.VerticalAlignment = abjad.Up,
    ):
    string = f'x{count}'
    markup = abjad.Markup(string)
    markup = markup.sans().bold().fontsize(6)
    markup = markup.box().override(('box-padding', 0.5))
    return abjad.Markup(
        markup,
        selector=selector,
        direction=direction,
        )

def clicks_per_second(
    lower: int,
    upper: int,
    selector: Selector = 'baca.pleaf(0)',
    ):
    string = f'{lower}-{upper} clicks/sec.'
    return abjad.Markup(
        string,
        selector=selector,
        )

def col_legno_battuto(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'col legno battuto',
        selector=selector,
        )

def crine(selecgtor='baca.pleaf(0))'):
    return abjad.Markup(
        'crine',
        selector=selector,
        )

def delicatiss(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'delicatiss.',
        selector=selector,
        )

def delicatissimo(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'delicatissimo',
        selector=selector,
        )

def directly_on_bridge_bow_diagonally(selector='baca.pleaf(0)'):
    string = 'directly on bridge:'
    string += ' bow diagonally to produce white noise w/ no pitch'
    return abjad.Markup(
        string,
        selector=selector,
        )

def directly_on_bridge_very_slow_bow(selector='baca.pleaf(0)'):
    string = 'directly on bridge:'
    string += ' very slow bow, imperceptible bow changes'
    return abjad.Markup(
        string,
        selector=selector,
        )

def divisi_1_plus_3(selector='baca.pleaf(0)'):
    return abjad.Markup(
        '1 + 3',
        selector=selector,
        )

def divisi_2_plus_4(selector='baca.pleaf(0)'):
    return abjad.Markup(
        '2 + 4',
        selector=selector,
        )

#def edition(
#    not_parts: typing.Union[str, IndicatorCommand],
#    only_parts: typing.Union[str, IndicatorCommand],
#    selector: Selector = 'baca.pleaf(0)',
#    ) -> SuiteCommand:
#    """
#    Makes not-parts / only-parts markup suite.
#    """
#    from .LibraryNS import LibraryNS
#    if isinstance(not_parts, str):
#        not_parts = markup(not_parts)
#    assert isinstance(not_parts, IndicatorCommand)
#    not_parts_ = LibraryNS.not_parts(not_parts)
#    if isinstance(only_parts, str):
#        only_parts = markup(only_parts)
#    assert isinstance(only_parts, IndicatorCommand)
#    only_parts_ = LibraryNS.only_parts(only_parts)
#    return SuiteCommand(
#        not_parts_,
#        only_parts_,
#        selector=selector,
#        )

def estr_sul_pont(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'estr. sul pont.',
        selector=selector,
        )

def ext_pont(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'ext. pont.',
        selector=selector,
        )

def FB(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'FB',
        selector=selector,
        )

def FB_flaut(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'FB flaut.',
        selector=selector,
        )

def final_markup(
    places: typing.List[str],
    dates: typing.List[str],
    selector: Selector = 'baca.leaf(-1)',
    ):
    string = r' \hspace #0.75 – \hspace #0.75 '.join(places)
    places_ = abjad.Markup(string)
    places_ = abjad.Markup.line([places_])
    string = r' \hspace #0.75 – \hspace #0.75 '.join(dates)
    dates_ = abjad.Markup(string)
    dates_ = abjad.Markup.line([dates_])
    markup = abjad.Markup.right_column([places_, dates_])
    markup = markup.with_color('black')
    markup = markup.override(('font-name', 'Palatino'))
    return abjad.Markup(
        markup,
        selector=selector,
        direction=abjad.Down,
        )

def flaut(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'flaut.',
        selector=selector,
        )

def flaut_partial_2(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'flaut. (2°)',
        selector=selector,
        )

def fluttertongue(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'fluttertongue',
        selector=selector,
        )

def fractional_OB(
    numerator: int,
    denominator: int,
    selector: Selector = 'baca.pleaf(0)',
    ):
    string = f'{numerator}/{denominator}OB'
    return abjad.Markup(
        string,
        selector=selector,
        )

def fractional_scratch(
    numerator: int,
    denominator: int,
    selector: Selector = 'baca.pleaf(0)',
    ) :
    string = f'{numerator}/{denominator} scratch'
    return abjad.Markup(
        string,
        selector=selector,
        )

def full_bow_strokes(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'full bow strokes',
        selector=selector,
        )

def glissando_lentissimo(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'glissando lentissimo',
        selector=selector,
        )

def gridato_possibile(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'gridato possibile',
        selector=selector,
        )

def half_clt(selector='baca.pleaf(0)'):
    return abjad.Markup(
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
    return abjad.Markup(
        'kn. rasg.',
        selector=selector,
        )

def knuckle_rasg(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'knuckle rasg.',
        selector=selector,
        )

def leggieriss(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'leggieriss.',
        selector=selector,
        )

def leggierissimo(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'leggierissimo',
        selector=selector,
        )

def leggierissimo_off_string_bowing_on_staccati(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'leggierissimo: off-string bowing on staccati',
        selector=selector,
        )

def lh_damp(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'lh damp',
        selector=selector,
        )

def lh_damp_plus_half_clt(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'lh damp + 1/2 clt',
        selector=selector,
        )

def lhd_plus_half_clt(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'lhd + 1/2 clt',
        selector=selector,
        )

def lines(
    items: typing.List,
    selector: Selector = 'baca.leaf(0)',
    direction: abjad.VerticalAlignment = abjad.Up,
    no_whiteout: bool = False,
    ):
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
            raise TypeError
            #assert isinstance(item, IndicatorCommand)
            assert item.indicators is not None
            assert len(item.indicators) == 1
            markup = item.indicators[0]
            items_.append(markup)
    markup = abjad.MarkupList(items_).column()
    return abjad.Markup(
        markup,
        selector=selector,
        direction=direction,
        whiteout=not(no_whiteout),
        )

def loure(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'louré',
        selector=selector,
        )

def lv_possibile(selector='baca.ptail(0)'):
    return abjad.Markup(
        'l.v. possibile',
        selector=selector,
        )

def molto_flautando(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'molto flautando',
        selector=selector,
        )

def molto_flautando_e_pont(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'molto flautando ed estr. sul pont.',
        selector=selector,
        )

def molto_gridato(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'molto gridato ed estr. sul pont.',
        selector=selector,
        )

def molto_overpressure(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'molto overpressure',
        selector=selector,
        )

def molto_pont_plus_vib_molto(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    selector: Selector = 'baca.pleaf(0)',
    ):
    return plus_statement(
        'molto pont.',
        'vib. molto',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        selector=selector,
        )

def molto_scratch(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'molto scratch',
        selector=selector,
        )

def MP_XFB_flaut(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'MP + XFB flaut.',
        selector=selector,
        )

def nail_rasg(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'nail rasg.',
        selector=selector,
        )

def nail_rasgueado(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'nail rasgueado',
        selector=selector,
        )

def non_div(selector='baca.leaf(0)'):
    return abjad.Markup(
        'non div.',
        selector=selector,
        )

def non_flaut(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'non flaut.',
        selector=selector,
        )

def non_flautando(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'non flautando',
        selector=selector,
        )

def non_flutt(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'non flutt.',
        selector=selector,
        )

def non_spazz(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'non spazz.',
        selector=selector,
        )

def nut(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'nut',
        selector=selector,
        )

def OB(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'OB',
        selector=selector,
        )

def OB_full_bow_strokes(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'OB + full bow strokes',
        selector=selector,
        )

def OB_no_pitch(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'OB (no pitch)',
        selector=selector,
        )

def OB_terminate_abruptly(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'OB + terminate abruptly',
        selector=selector,
        )

def OB_terminate_each_note_abruptly(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'OB + terminate each note abruptly',
        selector=selector,
        )

def off_string_bowing_on_staccati(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'off-string bowing on staccati',
        selector=selector,
        )

def one_click_every(lower, upper, selector='baca.pleaf(0)'):
    string = f'1 click/{lower}-{upper} sec.'
    return abjad.Markup(
        string,
        selector=selector,
        )

def ord(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'ord.',
        selector=selector,
        )

def ord_poco_scratch(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'ord. + poco scratch',
        selector=selector,
        )

def ord_senza_scratch(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'ord. (senza scratch)',
        selector=selector,
        )

def ordinario(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'ordinario',
        selector=selector,
        )

def overblow(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'overblow',
        selector=selector,
        )

def P_XFB_flaut(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'P + XFB flaut.',
        selector=selector,
        )

def pizz(selector='baca.pleaf(0)'):
    return abjad.Markup(
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
    return abjad.Markup(
        composite_string,
        selector=selector,
        )

def PO(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'PO',
        selector=selector,
        )

def PO_FB_flaut(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'PO + FB flaut.',
        selector=selector,
        )

def po_meno_scratch(selector='baca.pleaf(0)'):
    return abjad.Markup(
        "po' meno scratch",
        selector=selector,
        )

def PO_NBS(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'PO + NBS',
        selector=selector,
        )

def PO_plus_non_vib(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    selector: Selector = 'baca.pleaf(0)',
    ):
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
    ):
    return plus_statement(
        'PO',
        'poco vib.',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        selector=selector,
        )

def PO_scratch(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'PO + scratch',
        selector=selector,
        )

def PO_slow_bow(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'PO + slow bow (poco scratch)',
        selector=selector,
        )

def PO_XFB_flaut(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'PO + XFB flaut.',
        selector=selector,
        )

def pochiss_pont(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'pochiss. pont.',
        selector=selector,
        )

def pochiss_scratch(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'pochiss. scratch',
        selector=selector,
        )

def pochiss_vib(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'pochiss. vib.',
        selector=selector,
        )

def poco_overpressure(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'poco overpressure',
        selector=selector,
        )

def poco_pont_plus_non_vib(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    selector: Selector = 'baca.pleaf(0)',
    ):
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
    ):
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
    ):
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
    ):
    return plus_statement(
        'poco pont.',
        'vib. mod.',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        selector=selector,
        )

def poco_rasp_partial_2(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'poco rasp (2°)',
        selector=selector,
        )

def poco_scratch(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'poco scratch',
        selector=selector,
        )

def pont(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'pont.',
        selector=selector,
        )

def pont_XFB(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'pont. + XFB',
        selector=selector,
        )

def pont_XFB_flaut(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'pont. + XFB flaut.',
        selector=selector,
        )

def ponticello(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'ponticello',
        selector=selector,
        )

def pos_ord(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'pos. ord.',
        selector=selector,
        )

def pos_ord_poco_scratch(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'pos. ord. + poco scratch',
        selector=selector,
        )

def pos_ord_senza_vib(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'pos. ord. + senza vib',
        selector=selector,
        )

def pos_ord_vib_poco(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'pos. ord. + vib. poco',
        selector=selector,
        )

def pos_ord_XFB(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'pos. ord. + XFB',
        selector=selector,
        )

def pos_ord_XFB_flaut(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'pos. ord. + XFB flaut.',
        selector=selector,
        )

def pP_XFB_flaut(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'pP + XFB flaut.',
        selector=selector,
        )

def pres_de_la_table(selector='baca.pleaf(0)'):
    return boxed(
        'près de la table',
        selector=selector,
        )

def pT_XFB_flaut(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'pT + XFB flaut.',
        selector=selector,
        )

def put_reed_back_in(selector='baca.leaf(0)'):
    return boxed(
        'put reed back in',
        selector=selector,
        )

def rasp(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'rasp',
        selector=selector,
        )

def rasp_partial_2(selector='baca.pleaf(0)'):
    return abjad.Markup(
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
    return abjad.Markup(
        'scratch moltiss.',
        selector=selector,
        )

def senza_pedale(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'senza pedale',
        selector=selector,
        )

def senza_scratch(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'senza scratch',
        selector=selector,
        )

def senza_vib(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'senza vib.',
        selector=selector,
        )

def shakers(selector='baca.leaf(0)'):
    return abjad.Markup(
        'shakers',
        selector=selector,
        )

def short_instrument(
    string: str,
    hcenter_in: Number = 10,
    column: bool = True,
    ):
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
    return abjad.Markup(
        markup,
        selector=selector,
        )

def spazz(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'spazz.',
        selector=selector,
        )

def spazzolato(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'spazzolato',
        selector=selector,
        )

def spazzolato_1_2_clt(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'spazzolato (1/2 clt)',
        selector=selector,
        )

def still(selector='baca.leaf(0)'):
    return abjad.Markup(
        'still',
        selector=selector,
        )

def string_number(
    n: int,
    selector: Selector = 'baca.pleaf(0)',
    ):
    to_roman_numeral = {
        1: 'I',
        2: 'II',
        3: 'III',
        4: 'IV',
        }
    string_number = to_roman_numeral[n]
    return abjad.Markup(
        string_number,
        selector=selector,
        direction=abjad.Down,
        )

def string_numbers(
    numbers: typing.List[int],
    selector: Selector = 'baca.pleaf(0)',
    ):
    to_roman_numeral = {
        1: 'I',
        2: 'II',
        3: 'III',
        4: 'IV',
        }
    string_numbers = [to_roman_numeral[_] for _ in numbers]
    string = '+'.join(string_numbers)
    return abjad.Markup(
        string,
        selector=selector,
        direction=abjad.Down,
        )

def subito_non_armonichi_e_non_gridato(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'subito non armonichi e non gridato',
        selector=selector,
        )

def subito_ordinario(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'subito ordinario',
        selector=selector,
        )

def tamb_tr(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'tamb. tr.',
        selector=selector,
        )

def tasto(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'tasto',
        selector=selector,
        )

def tasto_FB(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'tasto + FB',
        selector=selector,
        )

def tasto_FB_flaut(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'tasto + FB flaut.',
        selector=selector,
        )

def tasto_fractional_scratch(
    numerator: int,
    denominator: int,
    selector: Selector = 'baca.pleaf(0)',
    ):
    string = f'tasto + {numerator}/{denominator} scratch'
    return abjad.Markup(
        string,
        selector=selector,
        )

def tasto_half_scratch(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'tasto + 1/2 scratch',
        selector=selector,
        )

def tasto_moltiss(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'tasto moltiss.',
        selector=selector,
        )

def tasto_NBS(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'tasto + NBS',
        selector=selector,
        )

def tasto_plus_non_vib(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    selector: Selector = 'baca.pleaf(0)',
    ):
    return plus_statement(
        'tasto',
        'non vib.',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        selector=selector,
        )

def tasto_plus_pochiss_scratch(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'tasto + pochiss. scratch',
        selector=selector,
        )

def tasto_plus_poco_scratch(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'tasto + poco scratch',
        selector=selector,
        )

def tasto_plus_poco_vib(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    selector: Selector = 'baca.pleaf(0)',
    ):
    return plus_statement(
        'tasto',
        'poco vib.',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        selector=selector,
        )

def tasto_plus_scratch_moltiss(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'tasto + scratch moltiss.',
        selector=selector,
        )

def tasto_poss(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'tasto poss.',
        selector=selector,
        )

def tasto_senza_vib(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'tasto + senza vib.',
        selector=selector,
        )

def tasto_slow_bow(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'tasto + slow bow (poco scratch)',
        selector=selector,
        )

def tasto_XFB(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'tasto + XFB',
        selector=selector,
        )

def tasto_XFB_flaut(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'tasto + XFB flaut.',
        selector=selector,
        )

def terminate_abruptly(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'terminate abruptly',
        selector=selector,
        )

def terminate_each_note_abruptly(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'terminate each note abruptly',
        selector=selector,
        )

def trans(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'trans.',
        selector=selector,
        )

def trem_flaut_tast(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'trem. flaut. tast.',
        selector=selector,
        )

def vib_moltiss(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'vib. moltiss.',
        selector=selector,
        )

def vib_pochiss(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'vib. pochiss.',
        selector=selector,
        )

def vib_poco(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'vib. poco.',
        selector=selector,
        )

def XFB(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'XFB',
        selector=selector,
        )

def XFB_flaut(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'XFB flaut.',
        selector=selector,
        )

def XFB_plus_pochiss_pont(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    selector: Selector = 'baca.pleaf(0)',
    ):
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
    ):
    return plus_statement(
        'XFB',
        'tasto',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        selector=selector,
        )

def XFB_sempre(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'XFB sempre',
        selector=selector,
        )

def XP(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'XP',
        selector=selector,
        )

def XP_FB(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'XP + FB',
        selector=selector,
        )

def XP_FB_flaut(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'XP + FB flaut.',
        selector=selector,
        )

def XP_full_bow_strokes(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'XP + full bow strokes',
        selector=selector,
        )

def XP_XFB(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'XP + XFB',
        selector=selector,
        )

def XP_XFB_flaut(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'XP + XFB flaut.',
        selector=selector,
        )

def XT(selector='baca.pleaf(0)'):
    return abjad.Markup(
        'XT',
        selector=selector,
        )
