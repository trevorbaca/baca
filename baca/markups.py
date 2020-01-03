"""
indicators.Markup library.
"""
import abjad
import typing
from . import indicators
from . import typings


### FACTORY FUNCTIONS ###


def accent_changes_of_direction():
    string = "accent changes of direction noticeably at each attack"
    return indicators.Markup(string)


def airtone():
    return indicators.Markup("airtone")


def allow_bowing_to_convey_accelerando():
    return indicators.Markup("allow bowing to convey accelerando")


def arco():
    return indicators.Markup("arco")


def arco_ordinario():
    return indicators.Markup("arco ordinario")


def attackless():
    return indicators.Markup("attackless")


def bass_drum():
    return indicators.Markup("bass drum")


def bow_on_tailpiece():
    return indicators.Markup("bow on tailpiece")


def bow_on_wooden_mute():
    return indicators.Markup("bow on wooden mute")


def bowed_crotales():
    return indicators.Markup("bowed crotales")


def castanets():
    return indicators.Markup("castanets")


def cir(m=None, n=None):
    string = "cir."
    if m is None:
        return indicators.Markup(string)
    assert isinstance(m, int), repr(m)
    if n is None:
        return indicators.Markup(f"{m}” {string}")
    assert isinstance(n, int), repr(n)
    return indicators.Markup(f"{m}-{n}” {string}")


def circles(m=None, n=None, as_string=False):
    string = "circles"
    if m is None:
        pass
    elif n is None:
        assert isinstance(m, int), repr(m)
        string = f"{m}” {string}"
    else:
        assert isinstance(n, int), repr(n)
        string = f"{m}-{n}” {string}"
    if as_string:
        return string
    else:
        return indicators.Markup(string)


def clicks_per_second(lower: int, upper: int):
    string = f"{lower}-{upper} clicks/sec."
    return indicators.Markup(string)


def col_legno_battuto():
    return indicators.Markup("col legno battuto")


def column(*strings):
    markup = abjad.MarkupList(strings).column()
    return indicators.Markup(contents=markup.contents)


def crine():
    return indicators.Markup("crine")


def crotales():
    return indicators.Markup("crotales")


def damp():
    return indicators.Markup("damp")


def delicatiss():
    return indicators.Markup("delicatiss.")


def delicatissimo():
    return indicators.Markup("delicatissimo")


def directly_on_bridge_bow_diagonally():
    string = "directly on bridge:"
    string += " bow diagonally to produce white noise w/ no pitch"
    return indicators.Markup(string)


def directly_on_bridge_very_slow_bow():
    string = "directly on bridge:"
    string += " very slow bow, imperceptible bow changes"
    return indicators.Markup(string)


def divisi_1_plus_3():
    return indicators.Markup("1 + 3")


def divisi_2_plus_4():
    return indicators.Markup("2 + 4")


def estr_sul_pont():
    return indicators.Markup("estr. sul pont.")


def ext_pont():
    return indicators.Markup("ext. pont.")


def fast_whisked_ellipses():
    return indicators.Markup("fast whisked ellipses")


def FB():
    return indicators.Markup("FB")


def FB_flaut():
    return indicators.Markup("FB flaut.")


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


def flaut():
    return indicators.Markup("flaut.")


def flaut_partial_2():
    return indicators.Markup("flaut. (2°)")


def flaut_possibile():
    return indicators.Markup("flaut. possibile")


def fluttertongue():
    return indicators.Markup("fluttertongue")


def fractional_OB(numerator: int, denominator: int):
    string = f"{numerator}/{denominator}OB"
    return indicators.Markup(string)


def fractional_scratch(numerator: int, denominator: int):
    string = f"{numerator}/{denominator} scratch"
    return indicators.Markup(string)


def full_bow_strokes():
    return indicators.Markup("full bow strokes")


def glissando_lentissimo():
    return indicators.Markup("glissando lentissimo")


def golden_tone():
    return indicators.Markup("golden tone")


def grid_possibile():
    return indicators.Markup("grid. possibile")


def gridato_possibile():
    return indicators.Markup("gridato possibile")


def half_clt():
    return indicators.Markup("1/2 clt")


def hair():
    return indicators.Markup("hair")


def instrument(
    string: typing.Union[str, typing.List[str]],
    hcenter_in: typing.Optional[abjad.Number] = 16,
    column: bool = True,
) -> abjad.Markup:
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
    """
    return make_instrument_name_markup(string, column=column, hcenter_in=hcenter_in)


def keynoise():
    return indicators.Markup("keynoise")


def kn_rasg():
    return indicators.Markup("kn. rasg.")


def knuckle_rasg():
    return indicators.Markup("knuckle rasg.")


def leggieriss():
    return indicators.Markup("leggieriss.")


def leggierissimo():
    return indicators.Markup("leggierissimo")


def leggierissimo_off_string_bowing_on_staccati():
    return indicators.Markup("leggierissimo: off-string bowing on staccati")


def lh_damp():
    return indicators.Markup("lh damp")


def lh_damp_plus_half_clt():
    return indicators.Markup("lh damp + 1/2 clt")


def lhd_plus_half_clt():
    return indicators.Markup("lhd + 1/2 clt")


def lines(items: typing.List, *, boxed: bool = None) -> indicators.Markup:
    if not isinstance(items, list):
        message = f"items must be list (not {type(items).__name__}):"
        lines = ["    " + _ for _ in format(items).split("\n")]
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


def loure():
    return indicators.Markup("louré")


def lv_possibile():
    return indicators.Markup("l.v. possibile")


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


def molto_flautando():
    return indicators.Markup("molto flautando")


def molto_flautando_e_pont():
    return indicators.Markup("molto flautando ed estr. sul pont.")


def molto_gridato():
    return indicators.Markup("molto gridato ed estr. sul pont.")


def molto_overpressure():
    return indicators.Markup("molto overpressure")


def molto_pont_plus_vib_molto(
    parenthesize_first: bool = False, parenthesize_last: bool = False
):
    return plus_statement(
        "molto pont.",
        "vib. molto",
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
    )


def molto_scratch():
    return indicators.Markup("molto scratch")


def MP_XFB_flaut():
    return indicators.Markup("MP + XFB flaut.")


def nail_rasg():
    return indicators.Markup("nail rasg.")


def nail_rasgueado():
    return indicators.Markup("nail rasgueado")


def non_flaut():
    return indicators.Markup("non flaut.")


def non_flautando():
    return indicators.Markup("non flautando")


def non_flutt():
    return indicators.Markup("non flutt.")


def non_spazz():
    return indicators.Markup("non spazz.")


def nut():
    return indicators.Markup("nut")


def OB():
    return indicators.Markup("OB")


def OB_full_bow_strokes():
    return indicators.Markup("OB + full bow strokes")


def OB_no_pitch():
    return indicators.Markup("OB (no pitch)")


def OB_terminate_abruptly():
    return indicators.Markup("OB + terminate abruptly")


def OB_terminate_each_note_abruptly():
    return indicators.Markup("OB + terminate each note abruptly")


def off_string_bowing_on_staccati():
    return indicators.Markup("off-string bowing on staccati")


def one_click_every(lower, upper):
    string = f"1 click/{lower}-{upper} sec."
    return indicators.Markup(string)


def ord():
    return indicators.Markup("ord.")


def ord_poco_scratch():
    return indicators.Markup("ord. + poco scratch")


def ord_senza_scratch():
    return indicators.Markup("ord. (senza scratch)")


def ordinario():
    return indicators.Markup("ordinario")


def overblow():
    return indicators.Markup("overblow")


def P_XFB_flaut():
    return indicators.Markup("P + XFB flaut.")


def pizz():
    return indicators.Markup("pizz.")


def plus_statement(
    string_1: str,
    string_2: str,
    parenthesize_first: bool = False,
    parenthesize_last: bool = False,
):
    if parenthesize_first and parenthesize_last:
        composite_string = f"({string_1} + {string_2})"
    elif parenthesize_first and not parenthesize_last:
        composite_string = f"({string_1}+) {string_2}"
    elif not parenthesize_first and parenthesize_last:
        composite_string = f"{string_1} (+{string_2})"
    else:
        composite_string = f"{string_1} + {string_2}"
    return indicators.Markup(composite_string)


def PO():
    return indicators.Markup("PO")


def PO_FB_flaut():
    return indicators.Markup("PO + FB flaut.")


def po_meno_scratch():
    return indicators.Markup("po' meno scratch")


def PO_NBS():
    return indicators.Markup("PO + NBS")


def PO_plus_non_vib(parenthesize_first: bool = False, parenthesize_last: bool = False):
    return plus_statement(
        "PO",
        "non vib.",
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
    )


def PO_plus_poco_vib(parenthesize_first: bool = False, parenthesize_last: bool = False):
    return plus_statement(
        "PO",
        "poco vib.",
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
    )


def PO_scratch():
    return indicators.Markup("PO + scratch")


def PO_slow_bow():
    return indicators.Markup("PO + slow bow (poco scratch)")


def PO_XFB_flaut():
    return indicators.Markup("PO + XFB flaut.")


def pochiss_pont():
    return indicators.Markup("pochiss. pont.")


def pochiss_scratch():
    return indicators.Markup("pochiss. scratch")


def pochiss_vib():
    return indicators.Markup("pochiss. vib.")


def poco_overpressure():
    return indicators.Markup("poco overpressure")


def poco_pont_plus_non_vib(
    parenthesize_first: bool = False, parenthesize_last: bool = False
):
    return plus_statement(
        "poco pont.",
        "non vib.",
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
    )


def poco_pont_plus_sub_non_vib(
    parenthesize_first: bool = False, parenthesize_last: bool = False
):
    return plus_statement(
        "poco pont.",
        "sub. non vib.",
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
    )


def poco_pont_plus_sub_vib_mod(
    parenthesize_first: bool = False, parenthesize_last: bool = False
):
    return plus_statement(
        "poco pont.",
        "sub. vib. mod.",
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
    )


def poco_pont_plus_vib_mod(
    parenthesize_first: bool = False, parenthesize_last: bool = False
):
    return plus_statement(
        "poco pont.",
        "vib. mod.",
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
    )


def poco_rasp_partial_2():
    return indicators.Markup("poco rasp (2°)")


def poco_scratch():
    return indicators.Markup("poco scratch")


def pont():
    return indicators.Markup("pont.")


def pont_XFB():
    return indicators.Markup("pont. + XFB")


def pont_XFB_flaut():
    return indicators.Markup("pont. + XFB flaut.")


def ponticello():
    return indicators.Markup("ponticello")


def pos_ord():
    return indicators.Markup("pos. ord.")


def pos_ord_poco_scratch():
    return indicators.Markup("pos. ord. + poco scratch")


def pos_ord_senza_vib():
    return indicators.Markup("pos. ord. + senza vib")


def pos_ord_vib_poco():
    return indicators.Markup("pos. ord. + vib. poco")


def pos_ord_XFB():
    return indicators.Markup("pos. ord. + XFB")


def pos_ord_XFB_flaut():
    return indicators.Markup("pos. ord. + XFB flaut.")


def pP_XFB_flaut():
    return indicators.Markup("pP + XFB flaut.")


def pres_de_la_table():
    return boxed("près de la table")


def pT_XFB_flaut():
    return indicators.Markup("pT + XFB flaut.")


def put_reed_back_in():
    return indicators.Markup("put reed back in")


def rasp():
    return indicators.Markup("rasp")


def rasp_partial_2():
    return indicators.Markup("rasp (2°)")


def ratchet():
    return indicators.Markup("ratchet")


def remove_staple():
    return indicators.Markup("remove staple")


def repeat_count(count: int,) -> indicators.Markup:
    string = f"x{count}"
    markup = indicators.Markup(string)
    markup = markup.sans().bold().fontsize(6)
    return markup


def scraped_slate():
    return indicators.Markup("scraped slate")


def scratch_moltiss():
    return indicators.Markup("scratch moltiss.")


def senza_pedale():
    return indicators.Markup("senza pedale")


def senza_scratch():
    return indicators.Markup("senza scratch")


def senza_vib():
    return indicators.Markup("senza vib.")


def short_instrument(
    string: str, hcenter_in: abjad.Number = 10, column: bool = True
) -> abjad.Markup:
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
    """
    return make_instrument_name_markup(string, column=column, hcenter_in=hcenter_in)


def snare_drum():
    return indicators.Markup("snare drum")


def sparse_clicks():
    first_line = indicators.Markup("sparse, individual clicks with extremely slow bow")
    first_line = first_line.line()
    second_line = indicators.Markup("(1-2/sec. in irregular rhythm)").line()
    markup = indicators.Markup.column([first_line, second_line])
    return indicators.Markup(markup)


def spazz():
    return indicators.Markup("spazz.")


def spazzolato():
    return indicators.Markup("spazzolato")


def spazzolato_1_2_clt():
    return indicators.Markup("spazzolato (1/2 clt)")


def sponges():
    return indicators.Markup("sponges")


def still():
    return indicators.Markup("still")


def string_number(n: int):
    to_roman_numeral = {1: "I", 2: "II", 3: "III", 4: "IV"}
    string_number = to_roman_numeral[n]
    return indicators.Markup(string_number, direction=abjad.Down)


def string_numbers(numbers: typing.List[int],):
    to_roman_numeral = {1: "I", 2: "II", 3: "III", 4: "IV"}
    string_numbers = [to_roman_numeral[_] for _ in numbers]
    string = "+".join(string_numbers)
    return indicators.Markup(string, direction=abjad.Down)


def subito_non_armonichi_e_non_gridato():
    return indicators.Markup("subito non armonichi e non gridato")


def subito_ordinario():
    return indicators.Markup("subito ordinario")


def suspended_cymbal():
    return indicators.Markup("suspended cymbal")


def tailpiece():
    return indicators.Markup("tailpiece")


def tam_tam():
    return indicators.Markup("tam-tam")


def tamb_tr():
    return indicators.Markup("tamb. tr.")


def tasto():
    return indicators.Markup("tasto")


def tasto_FB():
    return indicators.Markup("tasto + FB")


def tasto_FB_flaut():
    return indicators.Markup("tasto + FB flaut.")


def tasto_fractional_scratch(numerator: int, denominator: int):
    string = f"tasto + {numerator}/{denominator} scratch"
    return indicators.Markup(string)


def tasto_half_scratch():
    return indicators.Markup("tasto + 1/2 scratch")


def tasto_moltiss():
    return indicators.Markup("tasto moltiss.")


def tasto_NBS():
    return indicators.Markup("tasto + NBS")


def tasto_plus_non_vib(
    parenthesize_first: bool = False, parenthesize_last: bool = False
):
    return plus_statement(
        "tasto",
        "non vib.",
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
    )


def tasto_plus_pochiss_scratch():
    return indicators.Markup("tasto + pochiss. scratch")


def tasto_plus_poco_scratch():
    return indicators.Markup("tasto + poco scratch")


def tasto_plus_poco_vib(
    parenthesize_first: bool = False, parenthesize_last: bool = False
):
    return plus_statement(
        "tasto",
        "poco vib.",
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
    )


def tasto_plus_scratch_moltiss():
    return indicators.Markup("tasto + scratch moltiss.")


def tasto_poss():
    return indicators.Markup("tasto poss.")


def tasto_senza_vib():
    return indicators.Markup("tasto + senza vib.")


def tasto_slow_bow():
    return indicators.Markup("tasto + slow bow (poco scratch)")


def tasto_XFB():
    return indicators.Markup("tasto + XFB")


def tasto_XFB_flaut():
    return indicators.Markup("tasto + XFB flaut.")


def terminate_abruptly():
    return indicators.Markup("terminate abruptly")


def terminate_each_note_abruptly():
    return indicators.Markup("terminate each note abruptly")


def trans():
    return indicators.Markup("trans.")


def trem_flaut_tast():
    return indicators.Markup("trem. flaut. tast.")


def vib_moltiss():
    return indicators.Markup("vib. moltiss.")


def vib_pochiss():
    return indicators.Markup("vib. pochiss.")


def vib_poco():
    return indicators.Markup("vib. poco.")


def vibraphone():
    return indicators.Markup("vibraphone")


def XFB():
    return indicators.Markup("XFB")


def XFB_flaut():
    return indicators.Markup("XFB flaut.")


def XFB_plus_pochiss_pont(
    parenthesize_first: bool = False, parenthesize_last: bool = False
):
    return plus_statement(
        "XFB",
        "pochiss. pont.",
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
    )


def XFB_plus_tasto(parenthesize_first: bool = False, parenthesize_last: bool = False):
    return plus_statement(
        "XFB",
        "tasto",
        parenthesize_first=parenthesize_first,
        parenthesize_last=parenthesize_last,
    )


def XFB_sempre():
    return indicators.Markup("XFB sempre")


def XP():
    return indicators.Markup("XP")


def XP_FB():
    return indicators.Markup("XP + FB")


def XP_FB_flaut():
    return indicators.Markup("XP + FB flaut.")


def XP_full_bow_strokes():
    return indicators.Markup("XP + full bow strokes")


def XP_XFB():
    return indicators.Markup("XP + XFB")


def XP_XFB_flaut():
    return indicators.Markup("XP + XFB flaut.")


def XT():
    return indicators.Markup("XT")


def xylophone():
    return indicators.Markup("xylophone")
