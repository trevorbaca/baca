# -*- coding: utf-8 -*-
import abjad
import baca


class MarkupLibrary(object):
    r'''Markup interface.

    ::

        >>> import abjad
        >>> import baca

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Library'

    ### PUBLIC METHODS ###

    ### factory functions ###

    @staticmethod
    def make_markup(string, direction=Up, is_new=True, whiteout=True):
        if not is_new:
            string = '({})'.format(string)
        markup = abjad.Markup(string, direction=direction)
        markup = markup.upright()
        if whiteout:
            markup = markup.whiteout()
        return markup

    @staticmethod
    def make_markup_lines(strings, direction=Up):
        assert isinstance(strings, list), repr(strings)
        lines = []
        for string in strings:
            line = abjad.Markup(string).line()
            lines.append(line)
        markup = abjad.Markup.column(lines, direction=Up)
        return markup

    @classmethod
    def make_markup_lines_specifier(
        class_,
        strings,
        direction=Up,
        selector=None,
        ):
        markup = class_.make_markup_lines(strings, direction=direction)
        return baca.tools.MarkupSpecifier(
            markup=markup,
            selector=selector,
            )

    @classmethod
    def make_markup_specifier(
        class_,
        string,
        direction=Up,
        is_new=True,
        selector=None,
        whiteout=True,
        ):
        markup = class_.make_markup(
            string,
            direction=direction,
            is_new=is_new,
            whiteout=whiteout,
            )
        return baca.tools.MarkupSpecifier(
            markup=markup,
            selector=selector,
            )

    @staticmethod
    def make_repeated_markup(markups):
        return baca.tools.MarkupSpecifier(
            markup=markups,
            selector=abjad.select().
                by_logical_tie(pitched=True).
                get_item(0, apply_to_each=True),
            )

    @classmethod
    def make_two_part_transition_markup(
        class_,
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
        return class_.make_markup(composite_string)

    ### PRIVATE FUNCTIONS ###

    @staticmethod
    def _make_instrument_name_markup(string, space, column=True):
        parts = string.split()
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

    @classmethod
    def make_instrument_name_markup(class_, string, column=True):
        r'''Makes instrument name markup.

        ::

            >>> import abjad
            >>> import baca

        ..  container:: example

            Makes instrument name markup in column:

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

            Makes instrument name markup in line:

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
        return class_._make_instrument_name_markup(
            string, 
            16,
            column=column,
            )

    @classmethod
    def make_short_instrument_name_markup(class_, string, column=True):
        r'''Makes short instrument name markup.

        ..  container:: example

            Makes short instrument name markup in column:

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

            Makes short instrument name markup in line:

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
        return class_._make_instrument_name_markup(
            string, 
            10,
            column=column,
            )

    ### library ###

    @classmethod
    def accent_changes_of_direction(class_):
        string = 'accent changes of direction noticeably at each attack'
        return class_.make_markup(string)

    @classmethod
    def airtone(class_):
        return class_.make_markup('airtone')

    @classmethod
    def allow_bowing_to_convey_accelerando(class_):
        return class_.make_markup('allow bowing to convey accelerando')

    @classmethod
    def arco(class_):
        return class_.make_markup('arco')

    @classmethod
    def arco_ordinario(class_):
        return class_.make_markup('arco ordinario')

    @classmethod
    def attackless(class_):
        return class_.make_markup('attackless')

    @classmethod
    def col_legno_battuto(class_):
        return class_.make_markup('col legno battuto')

    @classmethod
    def delicatiss(class_):
        return class_.make_markup('delicatiss.')

    @classmethod
    def delicatissimo(class_):
        return class_.make_markup('delicatissimo')

    @classmethod
    def directly_on_bridge_bow_diagonally(class_):
        string = 'directly on bridge:'
        string += ' bow diagonally to produce white noise w/ no pitch',
        return class_.make_markup(string)

    @classmethod
    def directly_on_bridge_very_slow_bow(class_):
        string = 'directly on bridge:'
        string += ' very slow bow, imperceptible bow changes'
        return class_.make_markup(string)

    @classmethod
    def estr_sul_pont(class_):
        return class_.make_markup('estr. sul pont.')

    @classmethod
    def FB(class_):
        return class_.make_markup('FB')

    @classmethod
    def FB_flaut(class_):
        return class_.make_markup('FB flaut.')

    @classmethod
    def fluttertongue(class_):
        return class_.make_markup('fluttertongue')

    @classmethod
    def full_bow_strokes(class_):
        return class_.make_markup('full bow strokes')

    @classmethod
    def glissando_lentissimo(class_):
        return class_.make_markup('glissando lentissimo')

    @classmethod
    def gridato_possibile(class_):
        return class_.make_markup('gridato possibile')

    @classmethod
    def kn_rasg(class_, is_new=True):
        return class_.make_markup('kn. rasg.', is_new=is_new)

    @classmethod
    def knuckle_rasg(class_, is_new=True):
        return class_.make_markup('knuckle rasg.', is_new=is_new)

    @classmethod
    def leggieriss(class_):
        return class_.make_markup('leggieriss.')

    @classmethod
    def leggierissimo(class_):
        return class_.make_markup('leggierissimo')

    @classmethod
    def leggierissimo_off_string_bowing_on_staccati(class_):
        return class_.make_markup('leggierissimo: off-string bowing on staccati')

    @classmethod
    def lv_possibile(class_):
        return class_.make_markup('l.v. possibile')

    @classmethod
    def make_boxed_markup(class_, string, whiteout=True):
        markup = abjad.Markup(string, direction=Up)
        markup = markup.box().override(('box-padding', 0.5))
        if whiteout:
            markup = markup.whiteout()
        return markup

    @staticmethod
    def make_boxed_markup_lines(strings, direction=Up, whiteout=True):
        assert isinstance(strings, list), repr(strings)
        lines = []
        for string in strings:
            line = abjad.Markup(string).line()
            lines.append(line)
        markup = abjad.MarkupList(lines, direction=direction).column()
        markup = markup.box().override(('box-padding', 0.5))
        if whiteout:
            markup = markup.whiteout()
        return markup

    @staticmethod
    def make_boxed_markup_specifier(string, whiteout=True):
        markup = abjad.Markup(string, direction=Up)
        markup = markup.box().override(('box-padding', 0.5))
        if whiteout:
            markup = markup.whiteout()
        return baca.tools.MarkupSpecifier(markup=markup)

    @staticmethod
    def make_boxed_repeat_count(count):
        string = 'x{}'.format(count)
        markup = abjad.Markup(string, direction=Up)
        markup = markup.sans().bold().fontsize(6).upright()
        markup = markup.box().override(('box-padding', 0.5))
        return markup

    @staticmethod
    def make_clicks_per_second(lower, upper):
        string = '{}-{} clicks/sec.'
        string = string.format(lower, upper)
        return MarkupLibrary.make_markup(string)

    @staticmethod
    def make_fractional_OB(numerator, denominator):
        string = '{}/{}OB'
        string = string.format(numerator, denominator)
        return MarkupLibrary.make_markup(string)

    @classmethod
    def make_fractional_scratch(numerator, denominator):
        string = '{}/{} scratch'
        string = string.format(numerator, denominator)
        return class_.make_markup(string)

    @staticmethod
    def make_one_click_every(lower, upper):
        string = '1 click/{}-{} sec.'
        string = string.format(lower, upper)
        return MarkupLibrary.make_markup(string)

    @classmethod
    def make_pos_ord_fractional_scratch(numerator, denominator):
        string = 'pos. ord. + {}/{} scratch'
        string = string.format(numerator, denominator)
        return class_.make_markup(string)

    @classmethod
    def make_string_number(n):
        to_roman_numeral = {
            1: 'I',
            2: 'II',
            3: 'III',
            4: 'IV',
            }
        string_number = to_roman_numeral[n]
        return class_.make_markup(string_number, direction=Down)

    @classmethod
    def make_string_numbers(numbers):
        to_roman_numeral = {
            1: 'I',
            2: 'II',
            3: 'III',
            4: 'IV',
            }
        string_numbers = [to_roman_numeral[_] for _ in numbers]
        string_numbers = '+'.join(string_numbers)
        return class_.make_markup(string_numbers, direction=Down)

    @classmethod
    def make_tasto_fractional_scratch(numerator, denominator):
        string = 'tasto + {}/{} scratch'
        string = string.format(numerator, denominator)
        return class_.make_markup(string)

    @classmethod
    def molto_flautando(class_):
        return class_.make_markup('molto flautando')

    @classmethod
    def molto_flautando_e_pont(class_):
        return class_.make_markup('molto flautando ed estr. sul pont.')

    @classmethod
    def molto_gridato(class_):
        return class_.make_markup('molto gridato ed estr. sul pont.')

    @classmethod
    def molto_pont_plus_vib_molto(
        class_,
        first_is_new=True,
        second_is_new=True,
        ):
        return class_.make_two_part_transition_markup(
            'molto pont.',
            'vib. molto',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            )

    @classmethod
    def MP_XFB_flaut(class_):
        return class_.make_markup('MP + XFB flaut.')

    @classmethod
    def nail_rasg(class_, is_new=True):
        return class_.make_markup('nail rasg.', is_new=is_new)

    @classmethod
    def nail_rasgueado(class_, is_new=True):
        return class_.make_markup('nail rasgueado', is_new=is_new)

    @classmethod
    def non_flautando(class_):
        return class_.make_markup('non flautando')

    @classmethod
    def non_flutt(class_):
        return class_.make_markup('non flutt.')

    @classmethod
    def non_spazz(class_):
        return class_.make_markup('non spazz.')

    @classmethod
    def nut(class_):
        return class_.make_markup('nut')

    @classmethod
    def OB(class_):
        return class_.make_markup('OB')

    @classmethod
    def OB_no_pitch(class_):
        return class_.make_markup('OB (no pitch)')

    @classmethod
    def OB_terminate_abruptly(class_):
        return class_.make_markup('OB + terminate abruptly')

    @classmethod
    def OB_terminate_each_note_abruptly(class_):
        return class_.make_markup('OB + terminate each note abruptly')

    @classmethod
    def off_string_bowing_on_staccati(class_):
        return class_.make_markup('off-string bowing on staccati')

    @classmethod
    def ord_(class_):
        return class_.make_markup('ord.')

    @classmethod
    def ord_poco_scratch(class_):
        return class_.make_markup('ord. + poco scratch')

    @classmethod
    def ord_senza_scratch(class_):
        return class_.make_markup('ord. (senza scratch)')

    @classmethod
    def ordinario(class_):
        return class_.make_markup('ordinario')

    @classmethod
    def P_XFB_flaut(class_):
        return class_.make_markup('P + XFB flaut.')

    @classmethod
    def piu_meno_scratch(class_):
        return class_.make_markup('più meno scratch')

    @classmethod
    def pizz(class_):
        return class_.make_markup('pizz.')

    @classmethod
    def PO(class_):
        return class_.make_markup('PO')

    @classmethod
    def PO_FB_flaut(class_):
        return class_.make_markup('PO + FB flaut.')

    @classmethod
    def PO_NBS(class_):
        return class_.make_markup('PO + NBS')

    @classmethod
    def PO_plus_non_vib(
        class_,
        first_is_new=True,
        second_is_new=True,
        ):
        return class_.make_two_part_transition_markup(
            'PO',
            'non vib.',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            )

    @classmethod
    def PO_plus_poco_vib(
        class_,
        first_is_new=True,
        second_is_new=True,
        ):
        return class_.make_two_part_transition_markup(
            'PO',
            'poco vib.',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            )

    @classmethod
    def PO_scratch(class_):
        return class_.make_markup('PO + scratch')

    @classmethod
    def PO_slow_bow(class_):
        return class_.make_markup('PO + slow bow (poco scratch)')

    @classmethod
    def PO_XFB_flaut(class_):
        return class_.make_markup('PO + XFB flaut.')

    @classmethod
    def pochiss_pont(class_, is_new=True):
        return class_.make_markup('pochiss. pont.', is_new=is_new)

    @classmethod
    def pochiss_scratch(class_, is_new=True):
        return class_.make_markup('pochiss. scratch', is_new=is_new)

    @classmethod
    def pochiss_vib(class_):
        return class_.make_markup('pochiss. vib.')

    @classmethod
    def poco_pont_plus_non_vib(
        class_,
        first_is_new=True,
        second_is_new=True,
        ):
        return class_.make_two_part_transition_markup(
            'poco pont.',
            'non vib.',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            )

    @classmethod
    def poco_pont_plus_sub_non_vib(
        class_,
        first_is_new=True,
        second_is_new=True,
        ):
        return class_.make_two_part_transition_markup(
            'poco pont.',
            'sub. non vib.',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            )

    @classmethod
    def poco_pont_plus_sub_vib_mod(
        class_,
        first_is_new=True,
        second_is_new=True,
        ):
        return class_.make_two_part_transition_markup(
            'poco pont.',
            'sub. vib. mod.',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            )

    @classmethod
    def poco_pont_plus_vib_mod(
        class_,
        first_is_new=True,
        second_is_new=True,
        ):
        return class_.make_two_part_transition_markup(
            'poco pont.',
            'vib. mod.',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            )

    @classmethod
    def poco_scratch(class_):
        return class_.make_markup('poco scratch')

    @classmethod
    def pont(class_):
        return class_.make_markup('pont.')

    @classmethod
    def pont_XFB(class_):
        return class_.make_markup('pont. + XFB')

    @classmethod
    def pont_XFB_flaut(class_):
        return class_.make_markup('pont. + XFB flaut.')

    @classmethod
    def ponticello(class_, is_new=True):
        return class_.make_markup('ponticello', is_new=is_new)

    @classmethod
    def pos_ord(class_):
        return class_.make_markup('pos. ord.')

    @classmethod
    def pos_ord_poco_scratch(class_):
        return class_.make_markup('pos. ord. + poco scratch')

    @classmethod
    def pos_ord_senza_vib(class_):
        return class_.make_markup('pos. ord. + senza vib')

    @classmethod
    def pos_ord_vib_poco(class_):
        return class_.make_markup('pos. ord. + vib. poco')

    @classmethod
    def pos_ord_XFB(class_):
        return class_.make_markup('pos. ord. + XFB')

    @classmethod
    def pos_ord_XFB_flaut(class_):
        return class_.make_markup('pos. ord. + XFB flaut.')

    @classmethod
    def pP_XFB_flaut(class_):
        return class_.make_markup('pP + XFB flaut.')

    @classmethod
    def pT_XFB_flaut(class_):
        return class_.make_markup('pT + XFB flaut.')

    @classmethod
    def remove_staple(class_):
        return make_boxed_markup('remove staple')

    @classmethod
    def scratch_moltiss(class_):
        return class_.make_markup('scratch moltiss.')

    @classmethod
    def senza_scratch(class_):
        return class_.make_markup('senza scratch')

    @classmethod
    def senza_vib(class_):
        return class_.make_markup('senza vib.')

    @classmethod
    def sparse_clicks(class_):
        first_line = abjad.Markup(
            'sparse, individual clicks with extremely slow bow')
        first_line = first_line.line(class_)
        second_line = abjad.Markup('(1-2/sec. in irregular rhythm)').line(class_)
        markup = abjad.Markup.column([first_line, second_line], direction=Up)
        return markup

    @classmethod
    def spazz(class_):
        return class_.make_markup('spazz.')

    @classmethod
    def spazzolato(class_):
        return class_.make_markup('spazzolato')

    @classmethod
    def spazzolato_1_2_clt(class_):
        return class_.make_markup('spazzolato (1/2 clt)')

    @classmethod
    def still(class_, is_new=True):
        return class_.make_markup('still', is_new=is_new)

    @classmethod
    def subito_non_armonichi_e_non_gridato(class_):
        return class_.make_markup('subito non armonichi e non gridato')

    @classmethod
    def subito_ordinario(class_):
        return class_.make_markup('subito ordinario')

    @classmethod
    def tamb_tr(class_, is_new=True):
        return class_.make_markup('tamb. tr.', is_new=is_new)

    @classmethod
    def tasto(class_, is_new=True):
        return class_.make_markup('tasto', is_new=is_new)

    @classmethod
    def tasto_FB(class_):
        return class_.make_markup('tasto + FB')

    @classmethod
    def tasto_FB_flaut(class_):
        return class_.make_markup('tasto + FB flaut.')

    @classmethod
    def tasto_half_scratch(class_):
        return class_.make_markup('tasto + 1/2 scratch')

    @classmethod
    def tasto_moltiss(class_):
        return class_.make_markup('tasto moltiss.')

    @classmethod
    def tasto_NBS(class_):
        return class_.make_markup('tasto + NBS')

    @classmethod
    def tasto_plus_non_vib(
        class_,
        first_is_new=True,
        second_is_new=True,
        ):
        return class_.make_two_part_transition_markup(
            'tasto',
            'non vib.',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            )

    @classmethod
    def tasto_plus_pochiss_scratch(class_):
        return class_.make_markup('tasto + pochiss. scratch')

    @classmethod
    def tasto_plus_poco_scratch(class_):
        return class_.make_markup('tasto + poco scratch')

    @classmethod
    def tasto_plus_poco_vib(
        class_,
        first_is_new=True,
        second_is_new=True,
        ):
        return class_.make_two_part_transition_markup(
            'tasto',
            'poco vib.',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            )

    @classmethod
    def tasto_plus_scratch_moltiss(class_):
        return class_.make_markup('tasto + scratch moltiss.')

    @classmethod
    def tasto_poss(class_, is_new=True):
        return class_.make_markup('tasto poss.', is_new=is_new)

    @classmethod
    def tasto_senza_vib(class_):
        return class_.make_markup('tasto + senza vib.')

    @classmethod
    def tasto_slow_bow(class_):
        return class_.make_markup('tasto + slow bow (poco scratch)')

    @classmethod
    def tasto_XFB(class_):
        return class_.make_markup('tasto + XFB')

    @classmethod
    def tasto_XFB_flaut(class_):
        return class_.make_markup('tasto + XFB flaut.')

    @classmethod
    def terminate_abruptly(class_):
        return class_.make_markup('terminate abruptly')

    @classmethod
    def terminate_each_note_abruptly(class_):
        return class_.make_markup('terminate each note abruptly')

    @classmethod
    def trans(class_):
        return class_.make_markup('trans.')

    @classmethod
    def trem_flaut_tast(class_):
        return class_.make_markup('trem. flaut. tast.')

    @classmethod
    def vib_moltiss(class_):
        return class_.make_markup('vib. moltiss.')

    @classmethod
    def vib_pochiss(class_):
        return class_.make_markup('vib. pochiss.')

    @classmethod
    def vib_poco(class_):
        return class_.make_markup('vib. poco.')

    @classmethod
    def XFB(class_):
        return class_.make_markup('XFB')

    @classmethod
    def XFB_flaut(class_):
        return class_.make_markup('XFB flaut.')

    @classmethod
    def XFB_plus_pochiss_pont(
        class_,
        first_is_new=True,
        second_is_new=True,
        ):
        return class_.make_two_part_transition_markup(
            'XFB',
            'pochiss. pont.',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            )

    @classmethod
    def XFB_plus_tasto(
        class_,
        first_is_new=True,
        second_is_new=True,
        ):
        return class_.make_two_part_transition_markup(
            'XFB',
            'tasto',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            )

    @classmethod
    def XFB_sempre(class_):
        return class_.make_markup('XFB sempre')

    @classmethod
    def XP(class_):
        return class_.make_markup('XP')

    @classmethod
    def XP_FB(class_):
        return class_.make_markup('XP + FB')

    @classmethod
    def XP_FB_flaut(class_):
        return class_.make_markup('XP + FB flaut.')

    @classmethod
    def XP_full_bow_strokes(class_):
        return class_.make_markup('XP + full bow strokes')

    @classmethod
    def XP_XFB(class_):
        return class_.make_markup('XP + XFB')

    @classmethod
    def XP_XFB_flaut(class_):
        return class_.make_markup('XP + XFB flaut.')

    @classmethod
    def XT(class_):
        return class_.make_markup('XT')
