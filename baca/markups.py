"""
Markup library.
"""
import abjad
import baca
import typing
from . import library
from .IndicatorCommand import IndicatorCommand
from .Markup import Markup
from .SuiteCommand import SuiteCommand
from .Typing import Number
from .Typing import Selector


def accent_changes_of_direction():
    string = 'accent changes of direction noticeably at each attack'
    return Markup(
        string,
        )

def airtone():
    return Markup(
        'airtone',
        )

def allow_bowing_to_convey_accelerando():
    return Markup(
        'allow bowing to convey accelerando',
        )

def arco():
    return Markup(
        'arco',
        )

def arco_ordinario():
    return Markup(
        'arco ordinario',
        )

def attackless():
    return Markup(
        'attackless',
        )

def bow_on_tailpiece():
    return Markup(
        'bow on tailpiece',
        )

def bow_on_wooden_mute():
    return Markup(
        'bow on wooden mute',
        )

# TODO: selector
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

# TODO: selector
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
    ) -> Markup:
    string = f'x{count}'
    markup = Markup(string)
    markup = markup.sans().bold().fontsize(6)
    markup = markup.box().override(('box-padding', 0.5))
    return markup

def clicks_per_second(
    lower: int,
    upper: int,
    ):
    string = f'{lower}-{upper} clicks/sec.'
    return Markup(
        string,
        )

def col_legno_battuto():
    return Markup(
        'col legno battuto',
        )

def crine():
    return Markup(
        'crine',
        )

def delicatiss():
    return Markup(
        'delicatiss.',
        )

def delicatissimo():
    return Markup(
        'delicatissimo',
        )

def directly_on_bridge_bow_diagonally():
    string = 'directly on bridge:'
    string += ' bow diagonally to produce white noise w/ no pitch'
    return Markup(
        string,
        )

def directly_on_bridge_very_slow_bow():
    string = 'directly on bridge:'
    string += ' very slow bow, imperceptible bow changes'
    return Markup(
        string,
        )

def divisi_1_plus_3():
    return Markup(
        '1 + 3',
        )

def divisi_2_plus_4():
    return Markup(
        '2 + 4',
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

def estr_sul_pont():
    return Markup(
        'estr. sul pont.',
        )

def ext_pont():
    return Markup(
        'ext. pont.',
        )

def FB():
    return Markup(
        'FB',
        )

def FB_flaut():
    return Markup(
        'FB flaut.',
        )

def final_markup(
    places: typing.List[str],
    dates: typing.List[str],
    ) -> Markup:
    string = r' \hspace #0.75 – \hspace #0.75 '.join(places)
    places_ = abjad.Markup(string)
    places_ = abjad.Markup.line([places_])
    string = r' \hspace #0.75 – \hspace #0.75 '.join(dates)
    dates_ = abjad.Markup(string)
    dates_ = abjad.Markup.line([dates_])
    markup = abjad.Markup.right_column([places_, dates_])
    markup = markup.with_color('black')
    markup = markup.override(('font-name', 'Palatino'))
    markup = Markup(contents=markup.contents)
    return markup

def flaut():
    return Markup(
        'flaut.',
        )

def flaut_partial_2():
    return Markup(
        'flaut. (2°)',
        )

def fluttertongue():
    return Markup(
        'fluttertongue',
        )

def fractional_OB(
    numerator: int,
    denominator: int,
    ):
    string = f'{numerator}/{denominator}OB'
    return Markup(
        string,
        )

def fractional_scratch(
    numerator: int,
    denominator: int,
    ) :
    string = f'{numerator}/{denominator} scratch'
    return Markup(
        string,
        )

def full_bow_strokes():
    return Markup(
        'full bow strokes',
        )

def glissando_lentissimo():
    return Markup(
        'glissando lentissimo',
        )

def gridato_possibile():
    return Markup(
        'gridato possibile',
        )

def half_clt():
    return Markup(
        '1/2 clt',
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

def kn_rasg():
    return Markup(
        'kn. rasg.',
        )

def knuckle_rasg():
    return Markup(
        'knuckle rasg.',
        )

def leggieriss():
    return Markup(
        'leggieriss.',
        )

def leggierissimo():
    return Markup(
        'leggierissimo',
        )

def leggierissimo_off_string_bowing_on_staccati():
    return Markup(
        'leggierissimo: off-string bowing on staccati',
        )

def lh_damp():
    return Markup(
        'lh damp',
        )

def lh_damp_plus_half_clt():
    return Markup(
        'lh damp + 1/2 clt',
        )

def lhd_plus_half_clt():
    return Markup(
        'lhd + 1/2 clt',
        )

# TODO: selector was baca.leaf(0)
# TODO: old no_whiteout=False parameter
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

def loure():
    return Markup(
        'louré',
        )

def lv_possibile():
    return Markup(
        'l.v. possibile',
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

def molto_flautando():
    return Markup(
        'molto flautando',
        )

def molto_flautando_e_pont():
    return Markup(
        'molto flautando ed estr. sul pont.',
        )

def molto_gridato():
    return Markup(
        'molto gridato ed estr. sul pont.',
        )

def molto_overpressure():
    return Markup(
        'molto overpressure',
        )

def molto_pont_plus_vib_molto(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    ):
    return plus_statement(
        'molto pont.',
        'vib. molto',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        )

def molto_scratch():
    return Markup(
        'molto scratch',
        )

def MP_XFB_flaut():
    return Markup(
        'MP + XFB flaut.',
        )

def nail_rasg():
    return Markup(
        'nail rasg.',
        )

def nail_rasgueado():
    return Markup(
        'nail rasgueado',
        )

def non_flaut():
    return Markup(
        'non flaut.',
        )

def non_flautando():
    return Markup(
        'non flautando',
        )

def non_flutt():
    return Markup(
        'non flutt.',
        )

def non_spazz():
    return Markup(
        'non spazz.',
        )

def nut():
    return Markup(
        'nut',
        )

def OB():
    return Markup(
        'OB',
        )

def OB_full_bow_strokes():
    return Markup(
        'OB + full bow strokes',
        )

def OB_no_pitch():
    return Markup(
        'OB (no pitch)',
        )

def OB_terminate_abruptly():
    return Markup(
        'OB + terminate abruptly',
        )

def OB_terminate_each_note_abruptly():
    return Markup(
        'OB + terminate each note abruptly',
        )

def off_string_bowing_on_staccati():
    return Markup(
        'off-string bowing on staccati',
        )

def one_click_every(lower, upper):
    string = f'1 click/{lower}-{upper} sec.'
    return Markup(
        string,
        )

def ord():
    return Markup(
        'ord.',
        )

def ord_poco_scratch():
    return Markup(
        'ord. + poco scratch',
        )

def ord_senza_scratch():
    return Markup(
        'ord. (senza scratch)',
        )

def ordinario():
    return Markup(
        'ordinario',
        )

def overblow():
    return Markup(
        'overblow',
        )

def P_XFB_flaut():
    return Markup(
        'P + XFB flaut.',
        )

def pizz():
    return Markup(
        'pizz.',
        )

def plus_statement(
    string_1: str,
    string_2: str,
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    ):
    if parenthesize_first and parenthesize_last:
        composite_string = f'({string_1} + {string_2})'
    elif parenthesize_first and not parenthesize_last:
        composite_string = f'({string_1}+) {string_2}'
    elif not parenthesize_first and parenthesize_last:
        composite_string = f'{string_1} (+{string_2})'
    else:
        composite_string = f'{string_1} + {string_2}'
    return Markup(
        composite_string,
        )

def PO():
    return Markup(
        'PO',
        )

def PO_FB_flaut():
    return Markup(
        'PO + FB flaut.',
        )

def po_meno_scratch():
    return Markup(
        "po' meno scratch",
        )

def PO_NBS():
    return Markup(
        'PO + NBS',
        )

def PO_plus_non_vib(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    ):
    return plus_statement(
        'PO',
        'non vib.',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        )

def PO_plus_poco_vib(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    ):
    return plus_statement(
        'PO',
        'poco vib.',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        )

def PO_scratch():
    return Markup(
        'PO + scratch',
        )

def PO_slow_bow():
    return Markup(
        'PO + slow bow (poco scratch)',
        )

def PO_XFB_flaut():
    return Markup(
        'PO + XFB flaut.',
        )

def pochiss_pont():
    return Markup(
        'pochiss. pont.',
        )

def pochiss_scratch():
    return Markup(
        'pochiss. scratch',
        )

def pochiss_vib():
    return Markup(
        'pochiss. vib.',
        )

def poco_overpressure():
    return Markup(
        'poco overpressure',
        )

def poco_pont_plus_non_vib(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    ):
    return plus_statement(
        'poco pont.',
        'non vib.',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        )

def poco_pont_plus_sub_non_vib(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    ):
    return plus_statement(
        'poco pont.',
        'sub. non vib.',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        )

def poco_pont_plus_sub_vib_mod(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    ):
    return plus_statement(
        'poco pont.',
        'sub. vib. mod.',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        )

def poco_pont_plus_vib_mod(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    ):
    return plus_statement(
        'poco pont.',
        'vib. mod.',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        )

def poco_rasp_partial_2():
    return Markup(
        'poco rasp (2°)',
        )

def poco_scratch():
    return Markup(
        'poco scratch',
        )

def pont():
    return Markup(
        'pont.',
        )

def pont_XFB():
    return Markup(
        'pont. + XFB',
        )

def pont_XFB_flaut():
    return Markup(
        'pont. + XFB flaut.',
        )

def ponticello():
    return Markup(
        'ponticello',
        )

def pos_ord():
    return Markup(
        'pos. ord.',
        )

def pos_ord_poco_scratch():
    return Markup(
        'pos. ord. + poco scratch',
        )

def pos_ord_senza_vib():
    return Markup(
        'pos. ord. + senza vib',
        )

def pos_ord_vib_poco():
    return Markup(
        'pos. ord. + vib. poco',
        )

def pos_ord_XFB():
    return Markup(
        'pos. ord. + XFB',
        )

def pos_ord_XFB_flaut():
    return Markup(
        'pos. ord. + XFB flaut.',
        )

def pP_XFB_flaut():
    return Markup(
        'pP + XFB flaut.',
        )

def pres_de_la_table():
    return boxed(
        'près de la table',
        )

def pT_XFB_flaut():
    return Markup(
        'pT + XFB flaut.',
        )

def put_reed_back_in():
    return Markup(
        'put reed back in',
        )

def rasp():
    return Markup(
        'rasp',
        )

def rasp_partial_2():
    return Markup(
        'rasp (2°)',
        )

def remove_staple():
    return Markup(
        'remove staple',
        )

def scratch_moltiss():
    return Markup(
        'scratch moltiss.',
        )

def senza_pedale():
    return Markup(
        'senza pedale',
        )

def senza_scratch():
    return Markup(
        'senza scratch',
        )

def senza_vib():
    return Markup(
        'senza vib.',
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

def sparse_clicks():
    first_line = Markup(
        'sparse, individual clicks with extremely slow bow')
    first_line = first_line.line()
    second_line = Markup('(1-2/sec. in irregular rhythm)').line()
    markup = Markup.column([first_line, second_line])
    return Markup(
        markup,
        )

def spazz():
    return Markup(
        'spazz.',
        )

def spazzolato():
    return Markup(
        'spazzolato',
        )

def spazzolato_1_2_clt():
    return Markup(
        'spazzolato (1/2 clt)',
        )

def still():
    return Markup(
        'still',
        )

def string_number(n: int):
    to_roman_numeral = {
        1: 'I',
        2: 'II',
        3: 'III',
        4: 'IV',
        }
    string_number = to_roman_numeral[n]
    return Markup(
        string_number,
        direction=abjad.Down,
        )

def string_numbers(
    numbers: typing.List[int],
    ):
    to_roman_numeral = {
        1: 'I',
        2: 'II',
        3: 'III',
        4: 'IV',
        }
    string_numbers = [to_roman_numeral[_] for _ in numbers]
    string = '+'.join(string_numbers)
    return Markup(
        string,
        direction=abjad.Down,
        )

def subito_non_armonichi_e_non_gridato():
    return Markup(
        'subito non armonichi e non gridato',
        )

def subito_ordinario():
    return Markup(
        'subito ordinario',
        )

def tamb_tr():
    return Markup(
        'tamb. tr.',
        )

def tasto():
    return Markup(
        'tasto',
        )

def tasto_FB():
    return Markup(
        'tasto + FB',
        )

def tasto_FB_flaut():
    return Markup(
        'tasto + FB flaut.',
        )

def tasto_fractional_scratch(
    numerator: int,
    denominator: int,
    ):
    string = f'tasto + {numerator}/{denominator} scratch'
    return Markup(
        string,
        )

def tasto_half_scratch():
    return Markup(
        'tasto + 1/2 scratch',
        )

def tasto_moltiss():
    return Markup(
        'tasto moltiss.',
        )

def tasto_NBS():
    return Markup(
        'tasto + NBS',
        )

def tasto_plus_non_vib(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    ):
    return plus_statement(
        'tasto',
        'non vib.',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        )

def tasto_plus_pochiss_scratch():
    return Markup(
        'tasto + pochiss. scratch',
        )

def tasto_plus_poco_scratch():
    return Markup(
        'tasto + poco scratch',
        )

def tasto_plus_poco_vib(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    ):
    return plus_statement(
        'tasto',
        'poco vib.',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        )

def tasto_plus_scratch_moltiss():
    return Markup(
        'tasto + scratch moltiss.',
        )

def tasto_poss():
    return Markup(
        'tasto poss.',
        )

def tasto_senza_vib():
    return Markup(
        'tasto + senza vib.',
        )

def tasto_slow_bow():
    return Markup(
        'tasto + slow bow (poco scratch)',
        )

def tasto_XFB():
    return Markup(
        'tasto + XFB',
        )

def tasto_XFB_flaut():
    return Markup(
        'tasto + XFB flaut.',
        )

def terminate_abruptly():
    return Markup(
        'terminate abruptly',
        )

def terminate_each_note_abruptly():
    return Markup(
        'terminate each note abruptly',
        )

def trans():
    return Markup(
        'trans.',
        )

def trem_flaut_tast():
    return Markup(
        'trem. flaut. tast.',
        )

def vib_moltiss():
    return Markup(
        'vib. moltiss.',
        )

def vib_pochiss():
    return Markup(
        'vib. pochiss.',
        )

def vib_poco():
    return Markup(
        'vib. poco.',
        )

def XFB():
    return Markup(
        'XFB',
        )

def XFB_flaut():
    return Markup(
        'XFB flaut.',
        )

def XFB_plus_pochiss_pont(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    ):
    return plus_statement(
        'XFB',
        'pochiss. pont.',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        )

def XFB_plus_tasto(
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
    ):
    return plus_statement(
        'XFB',
        'tasto',
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
        )

def XFB_sempre():
    return Markup(
        'XFB sempre',
        )

def XP():
    return Markup(
        'XP',
        )

def XP_FB():
    return Markup(
        'XP + FB',
        )

def XP_FB_flaut():
    return Markup(
        'XP + FB flaut.',
        )

def XP_full_bow_strokes():
    return Markup(
        'XP + full bow strokes',
        )

def XP_XFB():
    return Markup(
        'XP + XFB',
        )

def XP_XFB_flaut():
    return Markup(
        'XP + XFB flaut.',
        )

def XT():
    return Markup(
        'XT',
        )
