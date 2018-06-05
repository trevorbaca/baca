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
        markup = baca.Markup(parts[0]).hcenter_in(space)
    elif column:
        markups = [baca.Markup(_) for _ in parts]
        markup = baca.Markup.center_column(markups, direction=None)
        markup = markup.hcenter_in(space)
    else:
        markups = [baca.Markup(_) for _ in parts]
        markups = baca.MarkupList(markups)
        markup = markups.line()
        markup = markup.hcenter_in(space)
    return markup

def accent_changes_of_direction():
    string = 'accent changes of direction noticeably at each attack'
    return baca.Markup(
        string,
        )

def airtone():
    return baca.Markup(
        'airtone',
        )

def allow_bowing_to_convey_accelerando():
    return baca.Markup(
        'allow bowing to convey accelerando',
        )

def arco():
    return baca.Markup(
        'arco',
        )

def arco_ordinario():
    return baca.Markup(
        'arco ordinario',
        )

def attackless():
    return baca.Markup(
        'attackless',
        )

def bow_on_tailpiece():
    return baca.Markup(
        'bow on tailpiece',
        )

def bow_on_wooden_mute():
    return baca.Markup(
        'bow on wooden mute',
        )

# TODO: selector was baca.leaf(0)
def boxed(
    string: str,
    ):
    """
    Makes boxed markup.
    """
    markup = baca.Markup(string)
    markup = markup.box().override(('box-padding', 0.5))
    return baca.Markup(
        markup,
        )

# TODO: selector was baca.leaf(0)
def boxed_lines(
    strings: typing.List[str],
    ):
    assert isinstance(strings, list), repr(strings)
    markup = baca.MarkupList(strings).column()
    markup = markup.box().override(('box-padding', 0.5))
    return baca.Markup(
        markup,
        )

# TODO: selector was baca.leaf(0)
def boxed_repeat_count(
    count: int,
    ):
    string = f'x{count}'
    markup = baca.Markup(string)
    markup = markup.sans().bold().fontsize(6)
    markup = markup.box().override(('box-padding', 0.5))
    return baca.Markup(
        markup,
        )

def clicks_per_second(
    lower: int,
    upper: int,
    ):
    string = f'{lower}-{upper} clicks/sec.'
    return baca.Markup(
        string,
        )

def col_legno_battuto():
    return baca.Markup(
        'col legno battuto',
        )

def crine():
    return baca.Markup(
        'crine',
        )

def delicatiss():
    return baca.Markup(
        'delicatiss.',
        )

def delicatissimo():
    return baca.Markup(
        'delicatissimo',
        )

def directly_on_bridge_bow_diagonally():
    string = 'directly on bridge:'
    string += ' bow diagonally to produce white noise w/ no pitch'
    return baca.Markup(
        string,
        )

def directly_on_bridge_very_slow_bow():
    string = 'directly on bridge:'
    string += ' very slow bow, imperceptible bow changes'
    return baca.Markup(
        string,
        )

def divisi_1_plus_3():
    return baca.Markup(
        '1 + 3',
        )

def divisi_2_plus_4():
    return baca.Markup(
        '2 + 4',
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

def estr_sul_pont():
    return baca.Markup(
        'estr. sul pont.',
        )

def ext_pont():
    return baca.Markup(
        'ext. pont.',
        )

def FB():
    return baca.Markup(
        'FB',
        )

def FB_flaut():
    return baca.Markup(
        'FB flaut.',
        )

# TODO: selector was baca.leaf(-1)
def final_markup(
    places: typing.List[str],
    dates: typing.List[str],
    ):
    string = r' \hspace #0.75 – \hspace #0.75 '.join(places)
    places_ = baca.Markup(string)
    places_ = baca.Markup.line([places_])
    string = r' \hspace #0.75 – \hspace #0.75 '.join(dates)
    dates_ = baca.Markup(string)
    dates_ = baca.Markup.line([dates_])
    markup = baca.Markup.right_column([places_, dates_])
    markup = markup.with_color('black')
    markup = markup.override(('font-name', 'Palatino'))
    return baca.Markup(
        markup,
        )

def flaut():
    return baca.Markup(
        'flaut.',
        )

def flaut_partial_2():
    return baca.Markup(
        'flaut. (2°)',
        )

def fluttertongue():
    return baca.Markup(
        'fluttertongue',
        )

def fractional_OB(
    numerator: int,
    denominator: int,
    ):
    string = f'{numerator}/{denominator}OB'
    return baca.Markup(
        string,
        )

def fractional_scratch(
    numerator: int,
    denominator: int,
    ) :
    string = f'{numerator}/{denominator} scratch'
    return baca.Markup(
        string,
        )

def full_bow_strokes():
    return baca.Markup(
        'full bow strokes',
        )

def glissando_lentissimo():
    return baca.Markup(
        'glissando lentissimo',
        )

def gridato_possibile():
    return baca.Markup(
        'gridato possibile',
        )

def half_clt():
    return baca.Markup(
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
    return _make_instrument_name_markup(
        string,
        hcenter_in,
        column=column,
        )

def kn_rasg():
    return baca.Markup(
        'kn. rasg.',
        )

def knuckle_rasg():
    return baca.Markup(
        'knuckle rasg.',
        )

def leggieriss():
    return baca.Markup(
        'leggieriss.',
        )

def leggierissimo():
    return baca.Markup(
        'leggierissimo',
        )

def leggierissimo_off_string_bowing_on_staccati():
    return baca.Markup(
        'leggierissimo: off-string bowing on staccati',
        )

def lh_damp():
    return baca.Markup(
        'lh damp',
        )

def lh_damp_plus_half_clt():
    return baca.Markup(
        'lh damp + 1/2 clt',
        )

def lhd_plus_half_clt():
    return baca.Markup(
        'lhd + 1/2 clt',
        )

# TODO: selector was baca.leaf(0)
# TODO: old no_whiteout=False parameter
def lines(
    items: typing.List,
    ):
    if not isinstance(items, list):
        message = f'items must be list (not {type(items).__name__}):'
        lines = ['    ' + _ for _ in format(items).split('\n')]
        lines = '\n'.join(lines)
        message += f'\n{lines}'
        raise Exception(message)
    items_ = []
    for item in items:
        if isinstance(item, (str, baca.Markup)):
            items_.append(item)
        else:
            raise TypeError
            #assert isinstance(item, IndicatorCommand)
            assert item.indicators is not None
            assert len(item.indicators) == 1
            markup = item.indicators[0]
            items_.append(markup)
    markup = baca.MarkupList(items_).column()
    return baca.Markup(
        markup,
        )

def loure():
    return baca.Markup(
        'louré',
        )

# TODO: selector was baca.ptail(0)
def lv_possibile():
    return baca.Markup(
        'l.v. possibile',
        )

def molto_flautando():
    return baca.Markup(
        'molto flautando',
        )

def molto_flautando_e_pont():
    return baca.Markup(
        'molto flautando ed estr. sul pont.',
        )

def molto_gridato():
    return baca.Markup(
        'molto gridato ed estr. sul pont.',
        )

def molto_overpressure():
    return baca.Markup(
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
    return baca.Markup(
        'molto scratch',
        )

def MP_XFB_flaut():
    return baca.Markup(
        'MP + XFB flaut.',
        )

def nail_rasg():
    return baca.Markup(
        'nail rasg.',
        )

def nail_rasgueado():
    return baca.Markup(
        'nail rasgueado',
        )

# TODO: selector was baca.leaf(0)
def non_div():
    return baca.Markup(
        'non div.',
        )

def non_flaut():
    return baca.Markup(
        'non flaut.',
        )

def non_flautando():
    return baca.Markup(
        'non flautando',
        )

def non_flutt():
    return baca.Markup(
        'non flutt.',
        )

def non_spazz():
    return baca.Markup(
        'non spazz.',
        )

def nut():
    return baca.Markup(
        'nut',
        )

def OB():
    return baca.Markup(
        'OB',
        )

def OB_full_bow_strokes():
    return baca.Markup(
        'OB + full bow strokes',
        )

def OB_no_pitch():
    return baca.Markup(
        'OB (no pitch)',
        )

def OB_terminate_abruptly():
    return baca.Markup(
        'OB + terminate abruptly',
        )

def OB_terminate_each_note_abruptly():
    return baca.Markup(
        'OB + terminate each note abruptly',
        )

def off_string_bowing_on_staccati():
    return baca.Markup(
        'off-string bowing on staccati',
        )

def one_click_every(lower, upper):
    string = f'1 click/{lower}-{upper} sec.'
    return baca.Markup(
        string,
        )

def ord():
    return baca.Markup(
        'ord.',
        )

def ord_poco_scratch():
    return baca.Markup(
        'ord. + poco scratch',
        )

def ord_senza_scratch():
    return baca.Markup(
        'ord. (senza scratch)',
        )

def ordinario():
    return baca.Markup(
        'ordinario',
        )

def overblow():
    return baca.Markup(
        'overblow',
        )

def P_XFB_flaut():
    return baca.Markup(
        'P + XFB flaut.',
        )

def pizz():
    return baca.Markup(
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
    return baca.Markup(
        composite_string,
        )

def PO():
    return baca.Markup(
        'PO',
        )

def PO_FB_flaut():
    return baca.Markup(
        'PO + FB flaut.',
        )

def po_meno_scratch():
    return baca.Markup(
        "po' meno scratch",
        )

def PO_NBS():
    return baca.Markup(
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
    return baca.Markup(
        'PO + scratch',
        )

def PO_slow_bow():
    return baca.Markup(
        'PO + slow bow (poco scratch)',
        )

def PO_XFB_flaut():
    return baca.Markup(
        'PO + XFB flaut.',
        )

def pochiss_pont():
    return baca.Markup(
        'pochiss. pont.',
        )

def pochiss_scratch():
    return baca.Markup(
        'pochiss. scratch',
        )

def pochiss_vib():
    return baca.Markup(
        'pochiss. vib.',
        )

def poco_overpressure():
    return baca.Markup(
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
    return baca.Markup(
        'poco rasp (2°)',
        )

def poco_scratch():
    return baca.Markup(
        'poco scratch',
        )

def pont():
    return baca.Markup(
        'pont.',
        )

def pont_XFB():
    return baca.Markup(
        'pont. + XFB',
        )

def pont_XFB_flaut():
    return baca.Markup(
        'pont. + XFB flaut.',
        )

def ponticello():
    return baca.Markup(
        'ponticello',
        )

def pos_ord():
    return baca.Markup(
        'pos. ord.',
        )

def pos_ord_poco_scratch():
    return baca.Markup(
        'pos. ord. + poco scratch',
        )

def pos_ord_senza_vib():
    return baca.Markup(
        'pos. ord. + senza vib',
        )

def pos_ord_vib_poco():
    return baca.Markup(
        'pos. ord. + vib. poco',
        )

def pos_ord_XFB():
    return baca.Markup(
        'pos. ord. + XFB',
        )

def pos_ord_XFB_flaut():
    return baca.Markup(
        'pos. ord. + XFB flaut.',
        )

def pP_XFB_flaut():
    return baca.Markup(
        'pP + XFB flaut.',
        )

def pres_de_la_table():
    return boxed(
        'près de la table',
        )

def pT_XFB_flaut():
    return baca.Markup(
        'pT + XFB flaut.',
        )

# TODO: selector was baca.leaf(0)
def put_reed_back_in():
    return boxed(
        'put reed back in',
        )

def rasp():
    return baca.Markup(
        'rasp',
        )

def rasp_partial_2():
    return baca.Markup(
        'rasp (2°)',
        )

# TODO: selector was baca.leaf(0)
def remove_reed():
    return boxed(
        'remove reed',
        )

# TODO: selector was baca.leaf(0)
def remove_staple():
    return boxed(
        'remove staple',
        )

def scratch_moltiss():
    return baca.Markup(
        'scratch moltiss.',
        )

def senza_pedale():
    return baca.Markup(
        'senza pedale',
        )

def senza_scratch():
    return baca.Markup(
        'senza scratch',
        )

def senza_vib():
    return baca.Markup(
        'senza vib.',
        )

# TODO: selector was baca.leaf(0)
def shakers():
    return baca.Markup(
        'shakers',
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
    return _make_instrument_name_markup(
        string,
        hcenter_in,
        column=column,
        )

def sparse_clicks():
    first_line = baca.Markup(
        'sparse, individual clicks with extremely slow bow')
    first_line = first_line.line()
    second_line = baca.Markup('(1-2/sec. in irregular rhythm)').line()
    markup = baca.Markup.column([first_line, second_line])
    return baca.Markup(
        markup,
        )

def spazz():
    return baca.Markup(
        'spazz.',
        )

def spazzolato():
    return baca.Markup(
        'spazzolato',
        )

def spazzolato_1_2_clt():
    return baca.Markup(
        'spazzolato (1/2 clt)',
        )

# TODO: selector was baca.leaf(0)
def still():
    return baca.Markup(
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
    return baca.Markup(
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
    return baca.Markup(
        string,
        direction=abjad.Down,
        )

def subito_non_armonichi_e_non_gridato():
    return baca.Markup(
        'subito non armonichi e non gridato',
        )

def subito_ordinario():
    return baca.Markup(
        'subito ordinario',
        )

def tamb_tr():
    return baca.Markup(
        'tamb. tr.',
        )

def tasto():
    return baca.Markup(
        'tasto',
        )

def tasto_FB():
    return baca.Markup(
        'tasto + FB',
        )

def tasto_FB_flaut():
    return baca.Markup(
        'tasto + FB flaut.',
        )

def tasto_fractional_scratch(
    numerator: int,
    denominator: int,
    ):
    string = f'tasto + {numerator}/{denominator} scratch'
    return baca.Markup(
        string,
        )

def tasto_half_scratch():
    return baca.Markup(
        'tasto + 1/2 scratch',
        )

def tasto_moltiss():
    return baca.Markup(
        'tasto moltiss.',
        )

def tasto_NBS():
    return baca.Markup(
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
    return baca.Markup(
        'tasto + pochiss. scratch',
        )

def tasto_plus_poco_scratch():
    return baca.Markup(
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
    return baca.Markup(
        'tasto + scratch moltiss.',
        )

def tasto_poss():
    return baca.Markup(
        'tasto poss.',
        )

def tasto_senza_vib():
    return baca.Markup(
        'tasto + senza vib.',
        )

def tasto_slow_bow():
    return baca.Markup(
        'tasto + slow bow (poco scratch)',
        )

def tasto_XFB():
    return baca.Markup(
        'tasto + XFB',
        )

def tasto_XFB_flaut():
    return baca.Markup(
        'tasto + XFB flaut.',
        )

def terminate_abruptly():
    return baca.Markup(
        'terminate abruptly',
        )

def terminate_each_note_abruptly():
    return baca.Markup(
        'terminate each note abruptly',
        )

def trans():
    return baca.Markup(
        'trans.',
        )

def trem_flaut_tast():
    return baca.Markup(
        'trem. flaut. tast.',
        )

def vib_moltiss():
    return baca.Markup(
        'vib. moltiss.',
        )

def vib_pochiss():
    return baca.Markup(
        'vib. pochiss.',
        )

def vib_poco():
    return baca.Markup(
        'vib. poco.',
        )

def XFB():
    return baca.Markup(
        'XFB',
        )

def XFB_flaut():
    return baca.Markup(
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
    return baca.Markup(
        'XFB sempre',
        )

def XP():
    return baca.Markup(
        'XP',
        )

def XP_FB():
    return baca.Markup(
        'XP + FB',
        )

def XP_FB_flaut():
    return baca.Markup(
        'XP + FB flaut.',
        )

def XP_full_bow_strokes():
    return baca.Markup(
        'XP + full bow strokes',
        )

def XP_XFB():
    return baca.Markup(
        'XP + XFB',
        )

def XP_XFB_flaut():
    return baca.Markup(
        'XP + XFB flaut.',
        )

def XT():
    return baca.Markup(
        'XT',
        )
