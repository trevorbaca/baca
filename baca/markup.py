# -*- coding: utf-8 -*-
from abjad.tools import markuptools


### factory functions ###

def make_markup(string, direction=Up, is_new=True, whiteout=True):
    if not is_new:
        string = '({})'.format(string)
    markup = markuptools.Markup(string, direction=direction)
    markup = markup.upright()
    if whiteout:
        markup = markup.whiteout()
    return markup

def make_markup_lines(strings, direction=Up):
    assert isinstance(strings, list), repr(strings)
    lines = []
    for string in strings:
        line = markuptools.Markup(string).line()
        lines.append(line)
    markup = markuptools.Markup.column(lines, direction=Up)
    return markup

def make_two_part_transition_markup(
    string_1,
    string_2,
    first_is_new=True,
    second_is_new=True,
    ):
    if first_is_new:
        if second_is_new:
            composite_string = '{} + {}'
        else:
            composite_string = '{} (+{})'
    else:
        if second_is_new:
            composite_string = '({}+) {}'
        else:
            composite_string = '({} + {})'
    composite_string = composite_string.format(string_1, string_2)
    return make_markup(composite_string)

### private functions ###

def _make_instrument_name_markup(string, space, column=True):
    parts = string.split()
    if len(parts) == 1:
        markup = markuptools.Markup(parts[0]).hcenter_in(space)
    elif column:
        markups = [markuptools.Markup(_) for _ in parts]
        markup = markuptools.Markup.center_column(markups, direction=None)
        markup = markup.hcenter_in(space)
    else:
        markups = [markuptools.Markup(_) for _ in parts]
        markup = markuptools.Markup.line(*markups)
        markup = markup.hcenter_in(space)
    return markup

def make_instrument_name_markup(string, column=True):
    r'''Makes instrument name markup.

    ::

        >>> import baca

    ..  container:: example

        **Example 1.** Makes instrument name markup in column:

        ::

            >>> markup = baca.markup.make_instrument_name_markup('Eng. horn')

        ::

            >>> show(markup) # doctest: +SKIP

        ..  doctest::

            >>> f(markup)
            \markup {
                \hcenter-in
                    #16
                    \center-column
                        {
                            Eng.
                            horn
                        }
                }

    ..  container:: example

        **Example 2.** Makes instrument name markup in line:

        ::

            >>> markup = baca.markup.make_instrument_name_markup(
            ...     'Violin 1',
            ...     column=False,
            ...     )

        ::

            >>> show(markup) # doctest: +SKIP

        ..  doctest::

            >>> f(markup)
            \markup {
                \hcenter-in
                    #16
                    \line
                        {
                            Violin
                            1
                        }
                }
    
    Centers markup horizontally in 16 spaces.

    Returns markup.
    '''
    return _make_instrument_name_markup(
        string, 
        16,
        column=column,
        )

def make_short_instrument_name_markup(string, column=True):
    r'''Makes short instrument name markup.

    ..  container:: example

        **Example 1.** Makes short instrument name markup in column:

        ::

            >>> markup = baca.markup.make_short_instrument_name_markup(
            ...     'Eng. hn.',
            ...     )

        ::

            >>> show(markup) # doctest: +SKIP

        ..  doctest::

            >>> f(markup)
            \markup {
                \hcenter-in
                    #10
                    \center-column
                        {
                            Eng.
                            hn.
                        }
                }

    ..  container:: example

        **Example 2.** Makes short instrument name markup in line:

        ::

            >>> markup = baca.markup.make_short_instrument_name_markup(
            ...     'Vn. 1',
            ...     column=False,
            ...     )

        ::

            >>> show(markup) # doctest: +SKIP

        ..  doctest::

            >>> f(markup)
            \markup {
                \hcenter-in
                    #10
                    \line
                        {
                            Vn.
                            1
                        }
                }
    
    Centers markup horizontally in 10 spaces.

    Returns markup.
    '''
    return _make_instrument_name_markup(
        string, 
        10,
        column=column,
        )

### library ###

def accent_changes_of_direction():
    string = 'accent changes of direction noticeably at each attack'
    return make_markup(string)

def airtone():
    return make_markup('airtone')

def allow_bowing_to_convey_accelerando():
    return make_markup('allow bowing to convey accelerando')

def arco():
    return make_markup('arco')

def arco_ordinario():
    return make_markup('arco ordinario')

def attackless():
    return make_markup('attackless')

def col_legno_battuto():
    return make_markup('col legno battuto')

def directly_on_bridge_bow_diagonally():
    string = 'directly on bridge:'
    string += ' bow diagonally to produce white noise w/ no pitch',
    return make_markup(string)

def directly_on_bridge_very_slow_bow():
    string = 'directly on bridge:'
    string += ' very slow bow, imperceptible bow changes'
    return make_markup(string)

def estr_sul_pont():
    return make_markup('estr. sul pont.')

def FB():
    return make_markup('FB')

def FB_flaut():
    return make_markup('FB flaut.')

def fluttertongue():
    return make_markup('fluttertongue')

def full_bow_strokes():
    return make_markup('full bow strokes')

def glissando_lentissimo():
    return make_markup('glissando lentissimo')

def gridato_possibile():
    return make_markup('gridato possibile')

def leggieriss():
    return make_markup('leggieriss.')

def leggierissimo():
    return make_markup('leggierissimo')

def leggierissimo_off_string_bowing_on_staccati():
    return make_markup('leggierissimo: off-string bowing on staccati')

def lv_possibile():
    return make_markup('l.v. possibile')

def make_boxed_markup(string, whiteout=True):
    markup = markuptools.Markup(string, direction=Up)
    markup = markup.box().override(('box-padding', 0.5))
    if whiteout:
        markup = markup.whiteout()
    return markup

def make_boxed_markup_lines(strings, direction=Up, whiteout=True):
    assert isinstance(strings, list), repr(strings)
    lines = []
    for string in strings:
        line = markuptools.Markup(string).line()
        lines.append(line)
    markup = markuptools.Markup.column(lines, direction=Up)
    markup = markup.box().override(('box-padding', 0.5))
    if whiteout:
        markup = markup.whiteout()
    return markup

def make_boxed_repeat_count(count):
    string = 'x{}'.format(count)
    markup = markuptools.Markup(string, direction=Up)
    markup = markup.sans().bold().fontsize(6).upright()
    markup = markup.box().override(('box-padding', 0.5))
    return markup

def make_one_click_every(lower, upper):
    string = '1 click/{}-{} sec.'
    string = string.format(lower, upper)
    return make_markup(string)

def make_clicks_per_second(lower, upper):
    string = '{}-{} clicks/sec.'
    string = string.format(lower, upper)
    return make_markup(string)

def make_fractional_OB(numerator, denominator):
    string = '{}/{}OB'
    string = string.format(numerator, denominator)
    return make_markup(string)

def make_fractional_scratch(numerator, denominator):
    string = '{}/{} scratch'
    string = string.format(numerator, denominator)
    return make_markup(string)

def make_pos_ord_fractional_scratch(numerator, denominator):
    string = 'pos. ord. + {}/{} scratch'
    string = string.format(numerator, denominator)
    return make_markup(string)

def make_repeated_markup(markups):
    import baca
    return baca.tools.RepeatedMarkupHandler(
        markups=markups,
        )

def make_string_number(n):
    to_roman_numeral = {
        1: 'I',
        2: 'II',
        3: 'III',
        4: 'IV',
        }
    string_number = to_roman_numeral[n]
    return make_markup(string_number, direction=Down)

def make_string_numbers(numbers):
    to_roman_numeral = {
        1: 'I',
        2: 'II',
        3: 'III',
        4: 'IV',
        }
    string_numbers = [to_roman_numeral[_] for _ in numbers]
    string_numbers = '+'.join(string_numbers)
    return make_markup(string_numbers, direction=Down)

def make_tasto_fractional_scratch(numerator, denominator):
    string = 'tasto + {}/{} scratch'
    string = string.format(numerator, denominator)
    return make_markup(string)

def molto_flautando():
    return make_markup('molto flautando')

def molto_flautando_e_pont():
    return make_markup('molto flautando ed estr. sul pont.')

def molto_gridato():
    return make_markup('molto gridato ed estr. sul pont.')

def molto_pont_plus_vib_molto(
    first_is_new=True,
    second_is_new=True,
    ):
    return make_two_part_transition_markup(
        'molto pont.',
        'vib. molto',
        first_is_new=first_is_new,
        second_is_new=second_is_new,
        )

def MP_XFB_flaut():
    return make_markup('MP + XFB flaut.')

def non_flautando():
    return make_markup('non flautando')

def non_flutt():
    return make_markup('non flutt.')

def non_spazz():
    return make_markup('non spazz.')

def nut():
    return make_markup('nut')

def OB():
    return make_markup('OB')

def OB_no_pitch():
    return make_markup('OB (no pitch)')

def OB_terminate_abruptly():
    return make_markup('OB + terminate abruptly')

def OB_terminate_each_note_abruptly():
    return make_markup('OB + terminate each note abruptly')

def off_string_bowing_on_staccati():
    return make_markup('off-string bowing on staccati')

def ord_():
    return make_markup('ord.')

def ord_poco_scratch():
    return make_markup('ord. + poco scratch')

def ord_senza_scratch():
    return make_markup('ord. (senza scratch)')

def ordinario():
    return make_markup('ordinario')

def P_XFB_flaut():
    return make_markup('P + XFB flaut.')

def piu_meno_scratch():
    return make_markup('più meno scratch')

def pizz():
    return make_markup('pizz.')

def PO():
    return make_markup('PO')

def PO_FB_flaut():
    return make_markup('PO + FB flaut.')

def PO_NBS():
    return make_markup('PO + NBS')

def PO_plus_non_vib(
    first_is_new=True,
    second_is_new=True,
    ):
    return make_two_part_transition_markup(
        'PO',
        'non vib.',
        first_is_new=first_is_new,
        second_is_new=second_is_new,
        )

def PO_plus_poco_vib(
    first_is_new=True,
    second_is_new=True,
    ):
    return make_two_part_transition_markup(
        'PO',
        'poco vib.',
        first_is_new=first_is_new,
        second_is_new=second_is_new,
        )

def PO_scratch():
    return make_markup('PO + scratch')

def PO_slow_bow():
    return make_markup('PO + slow bow (poco scratch)')

def PO_XFB_flaut():
    return make_markup('PO + XFB flaut.')

def pochiss_pont(is_new=True):
    return make_markup('pochiss. pont.', is_new=is_new)

def pochiss_scratch(is_new=True):
    return make_markup('pochiss. scratch', is_new=is_new)

def pochiss_vib():
    return make_markup('pochiss. vib.')

def poco_pont_plus_non_vib(
    first_is_new=True,
    second_is_new=True,
    ):
    return make_two_part_transition_markup(
        'poco pont.',
        'non vib.',
        first_is_new=first_is_new,
        second_is_new=second_is_new,
        )

def poco_pont_plus_sub_non_vib(
    first_is_new=True,
    second_is_new=True,
    ):
    return make_two_part_transition_markup(
        'poco pont.',
        'sub. non vib.',
        first_is_new=first_is_new,
        second_is_new=second_is_new,
        )

def poco_pont_plus_vib_mod(
    first_is_new=True,
    second_is_new=True,
    ):
    return make_two_part_transition_markup(
        'poco pont.',
        'vib. mod.',
        first_is_new=first_is_new,
        second_is_new=second_is_new,
        )

def poco_pont_plus_sub_vib_mod(
    first_is_new=True,
    second_is_new=True,
    ):
    return make_two_part_transition_markup(
        'poco pont.',
        'sub. vib. mod.',
        first_is_new=first_is_new,
        second_is_new=second_is_new,
        )

def poco_scratch():
    return make_markup('poco scratch')

def pont():
    return make_markup('pont.')

def pont_XFB():
    return make_markup('pont. + XFB')

def pont_XFB_flaut():
    return make_markup('pont. + XFB flaut.')

def pos_ord():
    return make_markup('pos. ord.')

def pos_ord_poco_scratch():
    return make_markup('pos. ord. + poco scratch')

def pos_ord_senza_vib():
    return make_markup('pos. ord. + senza vib')

def pos_ord_vib_poco():
    return make_markup('pos. ord. + vib. poco')

def pos_ord_XFB():
    return make_markup('pos. ord. + XFB')

def pos_ord_XFB_flaut():
    return make_markup('pos. ord. + XFB flaut.')

def pP_XFB_flaut():
    return make_markup('pP + XFB flaut.')

def pT_XFB_flaut():
    return make_markup('pT + XFB flaut.')

def remove_staple():
    return make_boxed_markup('remove staple')

def scratch_moltiss():
    return make_markup('scratch moltiss.')

def senza_scratch():
    return make_markup('senza scratch')

def senza_vib():
    return make_markup('senza vib.')

def sparse_clicks():
    first_line = markuptools.Markup(
        'sparse, individual clicks with extremely slow bow')
    first_line = first_line.line()
    second_line = markuptools.Markup('(1-2/sec. in irregular rhythm)').line()
    markup = markuptools.Markup.column([first_line, second_line], direction=Up)
    return markup

def spazz():
    return make_markup('spazz.')

def spazzolato():
    return make_markup('spazzolato')

def spazzolato_1_2_clt():
    return make_markup('spazzolato (1/2 clt)')

def subito_non_armonichi_e_non_gridato():
    return make_markup('subito non armonichi e non gridato')

def subito_ordinario():
    return make_markup('subito ordinario')

def tasto(is_new=True):
    return make_markup('tasto', is_new=is_new)

def tasto_FB():
    return make_markup('tasto + FB')

def tasto_FB_flaut():
    return make_markup('tasto + FB flaut.')

def tasto_half_scratch():
    return make_markup('tasto + 1/2 scratch')

def tasto_moltiss():
    return make_markup('tasto moltiss.')

def tasto_NBS():
    return make_markup('tasto + NBS')

def tasto_plus_non_vib(
    first_is_new=True,
    second_is_new=True,
    ):
    return make_two_part_transition_markup(
        'tasto',
        'non vib.',
        first_is_new=first_is_new,
        second_is_new=second_is_new,
        )

def tasto_plus_pochiss_scratch():
    return make_markup('tasto + pochiss. scratch')

def tasto_plus_poco_scratch():
    return make_markup('tasto + poco scratch')

def tasto_plus_scratch_moltiss():
    return make_markup('tasto + scratch moltiss.')

def tasto_plus_poco_vib(
    first_is_new=True,
    second_is_new=True,
    ):
    return make_two_part_transition_markup(
        'tasto',
        'poco vib.',
        first_is_new=first_is_new,
        second_is_new=second_is_new,
        )

def tasto_poss(is_new=True):
    return make_markup('tasto poss.', is_new=is_new)

def tasto_senza_vib():
    return make_markup('tasto + senza vib.')

def tasto_slow_bow():
    return make_markup('tasto + slow bow (poco scratch)')

def tasto_XFB():
    return make_markup('tasto + XFB')

def tasto_XFB_flaut():
    return make_markup('tasto + XFB flaut.')

def terminate_abruptly():
    return make_markup('terminate abruptly')

def terminate_each_note_abruptly():
    return make_markup('terminate each note abruptly')

def trans():
    return make_markup('trans.')

def trem_flaut_tast():
    return make_markup('trem. flaut. tast.')

def vib_moltiss():
    return make_markup('vib. moltiss.')

def vib_pochiss():
    return make_markup('vib. pochiss.')

def vib_poco():
    return make_markup('vib. poco.')

def XFB():
    return make_markup('XFB')

def XFB_flaut():
    return make_markup('XFB flaut.')

def XFB_plus_pochiss_pont(
    first_is_new=True,
    second_is_new=True,
    ):
    return make_two_part_transition_markup(
        'XFB',
        'pochiss. pont.',
        first_is_new=first_is_new,
        second_is_new=second_is_new,
        )

def XFB_plus_tasto(
    first_is_new=True,
    second_is_new=True,
    ):
    return make_two_part_transition_markup(
        'XFB',
        'tasto',
        first_is_new=first_is_new,
        second_is_new=second_is_new,
        )

def XFB_sempre():
    return make_markup('XFB sempre')

def XP():
    return make_markup('XP')

def XP_FB():
    return make_markup('XP + FB')

def XP_FB_flaut():
    return make_markup('XP + FB flaut.')

def XP_full_bow_strokes():
    return make_markup('XP + full bow strokes')

def XP_XFB():
    return make_markup('XP + XFB')

def XP_XFB_flaut():
    return make_markup('XP + XFB flaut.')

def XT():
    return make_markup('XT')