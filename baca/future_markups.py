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

def accent_changes_of_direction():
    string = 'accent changes of direction noticeably at each attack'
    return abjad.Markup(
        string,
        )

def airtone():
    return abjad.Markup(
        'airtone',
        )

def allow_bowing_to_convey_accelerando():
    return abjad.Markup(
        'allow bowing to convey accelerando',
        )

def arco():
    return abjad.Markup(
        'arco',
        )

def arco_ordinario():
    return abjad.Markup(
        'arco ordinario',
        )

def attackless():
    return abjad.Markup(
        'attackless',
        )

def bow_on_tailpiece():
    return abjad.Markup(
        'bow on tailpiece',
        )

def bow_on_wooden_mute():
    return abjad.Markup(
        'bow on wooden mute',
        )

# TODO: selector was baca.leaf(0)
def boxed(
    string: str,
    ):
    """
    Makes boxed markup.
    """
    markup = abjad.Markup(string)
    markup = markup.box().override(('box-padding', 0.5))
    return abjad.Markup(
        markup,
        )

# TODO: selector was baca.leaf(0)
def boxed_lines(
    strings: typing.List[str],
    ):
    assert isinstance(strings, list), repr(strings)
    markup = abjad.MarkupList(strings).column()
    markup = markup.box().override(('box-padding', 0.5))
    return abjad.Markup(
        markup,
        )

# TODO: selector was baca.leaf(0)
def boxed_repeat_count(
    count: int,
    ):
    string = f'x{count}'
    markup = abjad.Markup(string)
    markup = markup.sans().bold().fontsize(6)
    markup = markup.box().override(('box-padding', 0.5))
    return abjad.Markup(
        markup,
        )

def clicks_per_second(
    lower: int,
    upper: int,
    ):
    string = f'{lower}-{upper} clicks/sec.'
    return abjad.Markup(
        string,
        )

def col_legno_battuto():
    return abjad.Markup(
        'col legno battuto',
        )

def crine():
    return abjad.Markup(
        'crine',
        )

def delicatiss():
    return abjad.Markup(
        'delicatiss.',
        )

def delicatissimo():
    return abjad.Markup(
        'delicatissimo',
        )

def directly_on_bridge_bow_diagonally():
    string = 'directly on bridge:'
    string += ' bow diagonally to produce white noise w/ no pitch'
    return abjad.Markup(
        string,
        )

def directly_on_bridge_very_slow_bow():
    string = 'directly on bridge:'
    string += ' very slow bow, imperceptible bow changes'
    return abjad.Markup(
        string,
        )

def divisi_1_plus_3():
    return abjad.Markup(
        '1 + 3',
        )

def divisi_2_plus_4():
    return abjad.Markup(
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
    return abjad.Markup(
        'estr. sul pont.',
        )

def ext_pont():
    return abjad.Markup(
        'ext. pont.',
        )

def FB():
    return abjad.Markup(
        'FB',
        )

def FB_flaut():
    return abjad.Markup(
        'FB flaut.',
        )

# TODO: selector was baca.leaf(-1)
def final_markup(
    places: typing.List[str],
    dates: typing.List[str],
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
        )

def flaut():
    return abjad.Markup(
        'flaut.',
        )

def flaut_partial_2():
    return abjad.Markup(
        'flaut. (2°)',
        )

def fluttertongue():
    return abjad.Markup(
        'fluttertongue',
        )

def fractional_OB(
    numerator: int,
    denominator: int,
    ):
    string = f'{numerator}/{denominator}OB'
    return abjad.Markup(
        string,
        )

def fractional_scratch(
    numerator: int,
    denominator: int,
    ) :
    string = f'{numerator}/{denominator} scratch'
    return abjad.Markup(
        string,
        )

def full_bow_strokes():
    return abjad.Markup(
        'full bow strokes',
        )

def glissando_lentissimo():
    return abjad.Markup(
        'glissando lentissimo',
        )

def gridato_possibile():
    return abjad.Markup(
        'gridato possibile',
        )

def half_clt():
    return abjad.Markup(
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

def kn_rasg():
    return abjad.Markup(
        'kn. rasg.',
        )

def knuckle_rasg():
    return abjad.Markup(
        'knuckle rasg.',
        )

def leggieriss():
    return abjad.Markup(
        'leggieriss.',
        )

def leggierissimo():
    return abjad.Markup(
        'leggierissimo',
        )

def leggierissimo_off_string_bowing_on_staccati():
    return abjad.Markup(
        'leggierissimo: off-string bowing on staccati',
        )

def lh_damp():
    return abjad.Markup(
        'lh damp',
        )

def lh_damp_plus_half_clt():
    return abjad.Markup(
        'lh damp + 1/2 clt',
        )

def lhd_plus_half_clt():
    return abjad.Markup(
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
        )

def loure():
    return abjad.Markup(
        'louré',
        )

# TODO: selector was baca.pltail(0)
def lv_possibile():
    return abjad.Markup(
        'l.v. possibile',
        )

def molto_flautando():
    return abjad.Markup(
        'molto flautando',
        )

def molto_flautando_e_pont():
    return abjad.Markup(
        'molto flautando ed estr. sul pont.',
        )

def molto_gridato():
    return abjad.Markup(
        'molto gridato ed estr. sul pont.',
        )

def molto_overpressure():
    return abjad.Markup(
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
    return abjad.Markup(
        'molto scratch',
        )

def MP_XFB_flaut():
    return abjad.Markup(
        'MP + XFB flaut.',
        )

def nail_rasg():
    return abjad.Markup(
        'nail rasg.',
        )

def nail_rasgueado():
    return abjad.Markup(
        'nail rasgueado',
        )

# TODO: selector was baca.leaf(0)
def non_div():
    return abjad.Markup(
        'non div.',
        )

def non_flaut():
    return abjad.Markup(
        'non flaut.',
        )

def non_flautando():
    return abjad.Markup(
        'non flautando',
        )

def non_flutt():
    return abjad.Markup(
        'non flutt.',
        )

def non_spazz():
    return abjad.Markup(
        'non spazz.',
        )

def nut():
    return abjad.Markup(
        'nut',
        )

def OB():
    return abjad.Markup(
        'OB',
        )

def OB_full_bow_strokes():
    return abjad.Markup(
        'OB + full bow strokes',
        )

def OB_no_pitch():
    return abjad.Markup(
        'OB (no pitch)',
        )

def OB_terminate_abruptly():
    return abjad.Markup(
        'OB + terminate abruptly',
        )

def OB_terminate_each_note_abruptly():
    return abjad.Markup(
        'OB + terminate each note abruptly',
        )

def off_string_bowing_on_staccati():
    return abjad.Markup(
        'off-string bowing on staccati',
        )

def one_click_every(lower, upper):
    string = f'1 click/{lower}-{upper} sec.'
    return abjad.Markup(
        string,
        )

def ord():
    return abjad.Markup(
        'ord.',
        )

def ord_poco_scratch():
    return abjad.Markup(
        'ord. + poco scratch',
        )

def ord_senza_scratch():
    return abjad.Markup(
        'ord. (senza scratch)',
        )

def ordinario():
    return abjad.Markup(
        'ordinario',
        )

def overblow():
    return abjad.Markup(
        'overblow',
        )

def P_XFB_flaut():
    return abjad.Markup(
        'P + XFB flaut.',
        )

def pizz():
    return abjad.Markup(
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
    return abjad.Markup(
        composite_string,
        )

def PO():
    return abjad.Markup(
        'PO',
        )

def PO_FB_flaut():
    return abjad.Markup(
        'PO + FB flaut.',
        )

def po_meno_scratch():
    return abjad.Markup(
        "po' meno scratch",
        )

def PO_NBS():
    return abjad.Markup(
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
    return abjad.Markup(
        'PO + scratch',
        )

def PO_slow_bow():
    return abjad.Markup(
        'PO + slow bow (poco scratch)',
        )

def PO_XFB_flaut():
    return abjad.Markup(
        'PO + XFB flaut.',
        )

def pochiss_pont():
    return abjad.Markup(
        'pochiss. pont.',
        )

def pochiss_scratch():
    return abjad.Markup(
        'pochiss. scratch',
        )

def pochiss_vib():
    return abjad.Markup(
        'pochiss. vib.',
        )

def poco_overpressure():
    return abjad.Markup(
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
    return abjad.Markup(
        'poco rasp (2°)',
        )

def poco_scratch():
    return abjad.Markup(
        'poco scratch',
        )

def pont():
    return abjad.Markup(
        'pont.',
        )

def pont_XFB():
    return abjad.Markup(
        'pont. + XFB',
        )

def pont_XFB_flaut():
    return abjad.Markup(
        'pont. + XFB flaut.',
        )

def ponticello():
    return abjad.Markup(
        'ponticello',
        )

def pos_ord():
    return abjad.Markup(
        'pos. ord.',
        )

def pos_ord_poco_scratch():
    return abjad.Markup(
        'pos. ord. + poco scratch',
        )

def pos_ord_senza_vib():
    return abjad.Markup(
        'pos. ord. + senza vib',
        )

def pos_ord_vib_poco():
    return abjad.Markup(
        'pos. ord. + vib. poco',
        )

def pos_ord_XFB():
    return abjad.Markup(
        'pos. ord. + XFB',
        )

def pos_ord_XFB_flaut():
    return abjad.Markup(
        'pos. ord. + XFB flaut.',
        )

def pP_XFB_flaut():
    return abjad.Markup(
        'pP + XFB flaut.',
        )

def pres_de_la_table():
    return boxed(
        'près de la table',
        )

def pT_XFB_flaut():
    return abjad.Markup(
        'pT + XFB flaut.',
        )

# TODO: selector was baca.leaf(0)
def put_reed_back_in():
    return boxed(
        'put reed back in',
        )

def rasp():
    return abjad.Markup(
        'rasp',
        )

def rasp_partial_2():
    return abjad.Markup(
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
    return abjad.Markup(
        'scratch moltiss.',
        )

def senza_pedale():
    return abjad.Markup(
        'senza pedale',
        )

def senza_scratch():
    return abjad.Markup(
        'senza scratch',
        )

def senza_vib():
    return abjad.Markup(
        'senza vib.',
        )

# TODO: selector was baca.leaf(0)
def shakers():
    return abjad.Markup(
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

def sparse_clicks():
    first_line = abjad.Markup(
        'sparse, individual clicks with extremely slow bow')
    first_line = first_line.line()
    second_line = abjad.Markup('(1-2/sec. in irregular rhythm)').line()
    markup = abjad.Markup.column([first_line, second_line])
    return abjad.Markup(
        markup,
        )

def spazz():
    return abjad.Markup(
        'spazz.',
        )

def spazzolato():
    return abjad.Markup(
        'spazzolato',
        )

def spazzolato_1_2_clt():
    return abjad.Markup(
        'spazzolato (1/2 clt)',
        )

# TODO: selector was baca.leaf(0)
def still():
    return abjad.Markup(
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
    return abjad.Markup(
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
    return abjad.Markup(
        string,
        direction=abjad.Down,
        )

def subito_non_armonichi_e_non_gridato():
    return abjad.Markup(
        'subito non armonichi e non gridato',
        )

def subito_ordinario():
    return abjad.Markup(
        'subito ordinario',
        )

def tamb_tr():
    return abjad.Markup(
        'tamb. tr.',
        )

def tasto():
    return abjad.Markup(
        'tasto',
        )

def tasto_FB():
    return abjad.Markup(
        'tasto + FB',
        )

def tasto_FB_flaut():
    return abjad.Markup(
        'tasto + FB flaut.',
        )

def tasto_fractional_scratch(
    numerator: int,
    denominator: int,
    ):
    string = f'tasto + {numerator}/{denominator} scratch'
    return abjad.Markup(
        string,
        )

def tasto_half_scratch():
    return abjad.Markup(
        'tasto + 1/2 scratch',
        )

def tasto_moltiss():
    return abjad.Markup(
        'tasto moltiss.',
        )

def tasto_NBS():
    return abjad.Markup(
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
    return abjad.Markup(
        'tasto + pochiss. scratch',
        )

def tasto_plus_poco_scratch():
    return abjad.Markup(
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
    return abjad.Markup(
        'tasto + scratch moltiss.',
        )

def tasto_poss():
    return abjad.Markup(
        'tasto poss.',
        )

def tasto_senza_vib():
    return abjad.Markup(
        'tasto + senza vib.',
        )

def tasto_slow_bow():
    return abjad.Markup(
        'tasto + slow bow (poco scratch)',
        )

def tasto_XFB():
    return abjad.Markup(
        'tasto + XFB',
        )

def tasto_XFB_flaut():
    return abjad.Markup(
        'tasto + XFB flaut.',
        )

def terminate_abruptly():
    return abjad.Markup(
        'terminate abruptly',
        )

def terminate_each_note_abruptly():
    return abjad.Markup(
        'terminate each note abruptly',
        )

def trans():
    return abjad.Markup(
        'trans.',
        )

def trem_flaut_tast():
    return abjad.Markup(
        'trem. flaut. tast.',
        )

def vib_moltiss():
    return abjad.Markup(
        'vib. moltiss.',
        )

def vib_pochiss():
    return abjad.Markup(
        'vib. pochiss.',
        )

def vib_poco():
    return abjad.Markup(
        'vib. poco.',
        )

def XFB():
    return abjad.Markup(
        'XFB',
        )

def XFB_flaut():
    return abjad.Markup(
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
    return abjad.Markup(
        'XFB sempre',
        )

def XP():
    return abjad.Markup(
        'XP',
        )

def XP_FB():
    return abjad.Markup(
        'XP + FB',
        )

def XP_FB_flaut():
    return abjad.Markup(
        'XP + FB flaut.',
        )

def XP_full_bow_strokes():
    return abjad.Markup(
        'XP + full bow strokes',
        )

def XP_XFB():
    return abjad.Markup(
        'XP + XFB',
        )

def XP_XFB_flaut():
    return abjad.Markup(
        'XP + XFB flaut.',
        )

def XT():
    return abjad.Markup(
        'XT',
        )
