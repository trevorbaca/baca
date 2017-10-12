import abjad
import baca


class MarkupLibrary(object):
    r'''Markup interface.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Libraries'

    ### SPECIAL METHODS ###

    @staticmethod
    def __call__(markup=None, selector=None, direction=None):
        r'''Attaches markup to pitched head 0.

        ..  container:: example

            Attaches markup to pitched head 0:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.markup('più mosso'),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [ - \markup { "più mosso" }
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches markup to pitched head 0 in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.markup(
                ...         'più mosso',
                ...         baca.select_plt_head_in_tuplet(1, 0),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [ - \markup { "più mosso" }
                                e''16 ]
                                ef''4 ~
                                ef''16
                                r16
                                af''16 [
                                g''16 ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches markup to pitched heads in tuplet 1:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
                ...     baca.markup(
                ...         '*',
                ...         baca.select_plt_heads_in_tuplet(1),
                ...         ),
                ...     baca.rests_around([2], [4]),
                ...     baca.tuplet_bracket_staff_padding(5),
                ...     counts=[1, 1, 5, -1],
                ...     time_treatments=[-1],
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16 [
                                d'16 ]
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16 [ - \markup { * }
                                e''16 ] - \markup { * }
                                ef''4 ~ - \markup { * }
                                ef''16
                                r16
                                af''16 [ - \markup { * }
                                g''16 ] - \markup { * }
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if not isinstance(markup, abjad.Markup):
            markup = abjad.Markup(markup, direction=direction)
        selector = selector or baca.select_plt_head(n=0)
        return baca.AttachCommand(
            arguments=[markup],
            selector=selector,
            )

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

    ### PUBLIC METHODS ###

    @staticmethod
    def accent_changes_of_direction(selector=None):
        string = 'accent changes of direction noticeably at each attack'
        return MarkupLibrary.make_markup(
            string,
            selector=selector,
            )

    @staticmethod
    def airtone(selector=None):
        return MarkupLibrary.make_markup(
            'airtone',
            selector=selector,
            )

    @staticmethod
    def allow_bowing_to_convey_accelerando(selector=None):
        return MarkupLibrary.make_markup(
            'allow bowing to convey accelerando',
            selector=selector,
            )

    @staticmethod
    def arco(selector=None):
        return MarkupLibrary.make_markup(
            'arco',
            selector=selector,
            )

    @staticmethod
    def arco_ordinario(selector=None):
        return MarkupLibrary.make_markup(
            'arco ordinario',
            selector=selector,
            )

    @staticmethod
    def attackless(selector=None):
        return MarkupLibrary.make_markup(
            'attackless',
            selector=selector,
            )

    @staticmethod
    def bow_on_tailpiece(selector=None):
        return MarkupLibrary.make_markup(
            'bow on tailpiece',
            selector=selector,
            )

    @staticmethod
    def bow_on_wooden_mute(selector=None):
        return MarkupLibrary.make_markup(
            'bow on wooden mute',
            selector=selector,
            )

    @staticmethod
    def boxed(string, selector=None, whiteout=True):
        markup = abjad.Markup(string, direction=abjad.Up)
        markup = markup.box().override(('box-padding', 0.5))
        if whiteout:
            markup = markup.whiteout()
        return MarkupLibrary()(
            markup=markup,
            selector=selector,
            )

    @staticmethod
    def boxed_lines(strings, direction=abjad.Up, selector=None, whiteout=True):
        assert isinstance(strings, list), repr(strings)
        markup = abjad.MarkupList(strings).column(direction=direction)
        markup = markup.box().override(('box-padding', 0.5))
        if whiteout:
            markup = markup.whiteout()
        return MarkupLibrary()(
            markup=markup,
            selector=selector,
            )

    @staticmethod
    def boxed_repeat_count(count, selector=None):
        string = f'x{count}'
        markup = abjad.Markup(string, direction=abjad.Up)
        markup = markup.sans().bold().fontsize(6).upright()
        markup = markup.box().override(('box-padding', 0.5))
        return MarkupLibrary()(
            markup=markup,
            selector=selector,
            )

    @staticmethod
    def boxed_specifier(string, selector=None, whiteout=True):
        markup = abjad.Markup(string, direction=abjad.Up)
        markup = markup.box().override(('box-padding', 0.5))
        if whiteout:
            markup = markup.whiteout()
        return MarkupLibrary()(
            markup=markup,
            selector=selector,
            )

    @staticmethod
    def clicks_per_second(lower, upper, selector=None):
        string = f'{lower}-{upper} clicks/sec.'
        return MarkupLibrary.make_markup(
            string,
            selector=selector,
            )

    @staticmethod
    def col_legno_battuto(selector=None):
        return MarkupLibrary.make_markup(
            'col legno battuto',
            selector=selector,
            )

    @staticmethod
    def delicatiss(selector=None):
        return MarkupLibrary.make_markup(
            'delicatiss.',
            selector=selector,
            )

    @staticmethod
    def delicatissimo(selector=None):
        return MarkupLibrary.make_markup(
            'delicatissimo',
            selector=selector,
            )

    @staticmethod
    def directly_on_bridge_bow_diagonally(selector=None):
        string = 'directly on bridge:'
        string += ' bow diagonally to produce white noise w/ no pitch'
        return MarkupLibrary.make_markup(
            string,
            selector=selector,
            )

    @staticmethod
    def directly_on_bridge_very_slow_bow(selector=None):
        string = 'directly on bridge:'
        string += ' very slow bow, imperceptible bow changes'
        return MarkupLibrary.make_markup(
            string,
            selector=selector,
            )

    @staticmethod
    def estr_sul_pont(selector=None):
        return MarkupLibrary.make_markup(
            'estr. sul pont.',
            selector=selector,
            )

    @staticmethod
    def FB(selector=None):
        return MarkupLibrary.make_markup(
            'FB',
            selector=selector,
            )

    @staticmethod
    def FB_flaut(selector=None):
        return MarkupLibrary.make_markup(
            'FB flaut.',
            selector=selector,
            )

    @staticmethod
    def final_markup(places, dates, selector=None):
        places = r' \hspace #0.75 – \hspace #0.75 '.join(places)
        places = abjad.Markup(places)
        places = abjad.Markup.line([places])
        dates = r' \hspace #0.75 – \hspace #0.75 '.join(dates)
        dates = abjad.Markup(dates)
        dates = abjad.Markup.line([dates])
        markup = abjad.Markup.right_column([places, dates])
        markup = markup.with_color('black')
        return MarkupLibrary.make_markup(
            markup,
            direction=abjad.Down,
            selector=selector,
            )

    @staticmethod
    def fluttertongue(selector=None):
        return MarkupLibrary.make_markup(
            'fluttertongue',
            selector=selector,
            )

    @staticmethod
    def fractional_OB(numerator, denominator, selector=None):
        string = f'{numerator}/{denominator}OB'
        return MarkupLibrary.make_markup(
            string,
            selector=selector,
            )

    @staticmethod
    def fractional_scratch(numerator, denominator, selector=None):
        string = f'{numerator}/{denominator} scratch'
        return MarkupLibrary.make_markup(
            string,
            selector=selector,
            )

    @staticmethod
    def full_bow_strokes(selector=None):
        return MarkupLibrary.make_markup(
            'full bow strokes',
            selector=selector,
            )

    @staticmethod
    def glissando_lentissimo(selector=None):
        return MarkupLibrary.make_markup(
            'glissando lentissimo',
            selector=selector,
            )

    @staticmethod
    def gridato_possibile(selector=None):
        return MarkupLibrary.make_markup(
            'gridato possibile',
            selector=selector,
            )

    @staticmethod
    def instrument(string, column=True, selector=None):
        r'''Makes instrument name markup.

        ..  container:: example

            Makes instrument name markup in column:

            ::

                >>> markup = baca.markup.instrument('Eng. horn')

            ::

                >>> show(markup) # doctest: +SKIP

            ..  docs::

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

                >>> markup = baca.markup.instrument(
                ...     'Violin 1',
                ...     column=False,
                ...     )

            ::

                >>> show(markup) # doctest: +SKIP

            ..  docs::

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
        return MarkupLibrary._make_instrument_name_markup(
            string,
            16,
            column=column,
            )

    @staticmethod
    def kn_rasg(is_new=True, selector=None):
        return MarkupLibrary.make_markup(
            'kn. rasg.',
            is_new=is_new,
            selector=selector,
            )

    @staticmethod
    def knuckle_rasg(is_new=True, selector=None):
        return MarkupLibrary.make_markup(
            'knuckle rasg.',
            is_new=is_new,
            selector=selector,
            )

    @staticmethod
    def leggieriss(selector=None):
        return MarkupLibrary.make_markup(
            'leggieriss.',
            selector=selector,
            )

    @staticmethod
    def leggierissimo(selector=None):
        return MarkupLibrary.make_markup(
            'leggierissimo',
            selector=selector,
            )

    @staticmethod
    def leggierissimo_off_string_bowing_on_staccati(selector=None):
        return MarkupLibrary.make_markup(
            'leggierissimo: off-string bowing on staccati',
            selector=selector,
            )

    @staticmethod
    def lines(strings, direction=abjad.Up, selector=None):
        assert isinstance(strings, list), repr(strings)
        markup = abjad.MarkupList(strings).column(direction=direction)
        return MarkupLibrary()(
            markup=markup,
            selector=selector,
            )

    @staticmethod
    def lv_possibile(selector=None):
        return MarkupLibrary.make_markup(
            'l.v. possibile',
            selector=selector,
            )

    @staticmethod
    def make_markup(
        string,
        direction=abjad.Up,
        is_new=True,
        selector=None,
        upright=True,
        whiteout=True,
        ):
        if not is_new:
            string = f'({string})'
        markup = abjad.Markup(string, direction=direction)
        if upright:
            markup = markup.upright()
        if whiteout:
            markup = markup.whiteout()
        return MarkupLibrary()(markup=markup, selector=selector)

    @staticmethod
    def molto_flautando(selector=None):
        return MarkupLibrary.make_markup(
            'molto flautando',
            selector=selector,
            )

    @staticmethod
    def molto_flautando_e_pont(selector=None):
        return MarkupLibrary.make_markup(
            'molto flautando ed estr. sul pont.',
            selector=selector,
            )

    @staticmethod
    def molto_gridato(selector=None):
        return MarkupLibrary.make_markup(
            'molto gridato ed estr. sul pont.',
            selector=selector,
            )

    @staticmethod
    def molto_pont_plus_vib_molto(
        first_is_new=True,
        second_is_new=True,
        selector=None,
        ):
        return MarkupLibrary.two_part_transition(
            'molto pont.',
            'vib. molto',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            selector=selector,
            )

    @staticmethod
    def MP_XFB_flaut(selector=None):
        return MarkupLibrary.make_markup(
            'MP + XFB flaut.',
            selector=selector,
            )

    @staticmethod
    def nail_rasg(is_new=True, selector=None):
        return MarkupLibrary.make_markup(
            'nail rasg.',
            is_new=is_new,
            selector=selector,
            )

    @staticmethod
    def nail_rasgueado(is_new=True, selector=None):
        return MarkupLibrary.make_markup(
            'nail rasgueado',
            is_new=is_new,
            selector=selector,
            )

    @staticmethod
    def non_flautando(selector=None):
        return MarkupLibrary.make_markup(
            'non flautando',
            selector=selector,
            )

    @staticmethod
    def non_flutt(selector=None):
        return MarkupLibrary.make_markup(
            'non flutt.',
            selector=selector,
            )

    @staticmethod
    def non_spazz(selector=None):
        return MarkupLibrary.make_markup(
            'non spazz.',
            selector=selector,
            )

    @staticmethod
    def nut(selector=None):
        return MarkupLibrary.make_markup(
            'nut',
            selector=selector,
            )

    @staticmethod
    def OB(selector=None):
        return MarkupLibrary.make_markup(
            'OB',
            selector=selector,
            )

    @staticmethod
    def OB_full_bow_strokes(selector=None):
        return MarkupLibrary.make_markup(
            'OB + full bow strokes',
            selector=selector,
            )

    @staticmethod
    def OB_no_pitch(selector=None):
        return MarkupLibrary.make_markup(
            'OB (no pitch)',
            selector=selector,
            )

    @staticmethod
    def OB_terminate_abruptly(selector=None):
        return MarkupLibrary.make_markup(
            'OB + terminate abruptly',
            selector=selector,
            )

    @staticmethod
    def OB_terminate_each_note_abruptly(selector=None):
        return MarkupLibrary.make_markup(
            'OB + terminate each note abruptly',
            selector=selector,
            )

    @staticmethod
    def off_string_bowing_on_staccati(selector=None):
        return MarkupLibrary.make_markup(
            'off-string bowing on staccati',
            selector=selector,
            )

    @staticmethod
    def one_click_every(lower, upper, selector=None):
        string = f'1 click/{lower}-{upper} sec.'
        return MarkupLibrary.make_markup(
            string,
            selector=selector,
            )

    @staticmethod
    def ord_(selector=None):
        return MarkupLibrary.make_markup(
            'ord.',
            selector=selector,
            )

    @staticmethod
    def ord_poco_scratch(selector=None):
        return MarkupLibrary.make_markup(
            'ord. + poco scratch',
            selector=selector,
            )

    @staticmethod
    def ord_senza_scratch(selector=None):
        return MarkupLibrary.make_markup(
            'ord. (senza scratch)',
            selector=selector,
            )

    @staticmethod
    def ordinario(selector=None):
        return MarkupLibrary.make_markup(
            'ordinario',
            selector=selector,
            )

    @staticmethod
    def overblow(selector=None):
        return MarkupLibrary.make_markup(
            'overblow',
            selector=selector,
            )

    @staticmethod
    def P_XFB_flaut(selector=None):
        return MarkupLibrary.make_markup(
            'P + XFB flaut.',
            selector=selector,
            )

    @staticmethod
    def pizz(selector=None):
        return MarkupLibrary.make_markup(
            'pizz.',
            selector=selector,
            )

    @staticmethod
    def PO(selector=None):
        return MarkupLibrary.make_markup(
            'PO',
            selector=selector,
            )

    @staticmethod
    def PO_FB_flaut(selector=None):
        return MarkupLibrary.make_markup(
            'PO + FB flaut.',
            selector=selector,
            )

    @staticmethod
    def po_meno_scratch(selector=None):
        return MarkupLibrary.make_markup(
            "po' meno scratch",
            selector=selector,
            )

    @staticmethod
    def PO_NBS(selector=None):
        return MarkupLibrary.make_markup(
            'PO + NBS',
            selector=selector,
            )

    @staticmethod
    def PO_plus_non_vib(
        first_is_new=True,
        second_is_new=True,
        selector=None,
        ):
        return MarkupLibrary.two_part_transition(
            'PO',
            'non vib.',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            selector=selector,
            )

    @staticmethod
    def PO_plus_poco_vib(
        first_is_new=True,
        second_is_new=True,
        selector=None,
        ):
        return MarkupLibrary.two_part_transition(
            'PO',
            'poco vib.',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            selector=selector,
            )

    @staticmethod
    def PO_scratch(selector=None):
        return MarkupLibrary.make_markup(
            'PO + scratch',
            selector=selector,
            )

    @staticmethod
    def PO_slow_bow(selector=None):
        return MarkupLibrary.make_markup(
            'PO + slow bow (poco scratch)',
            selector=selector,
            )

    @staticmethod
    def PO_XFB_flaut(selector=None):
        return MarkupLibrary.make_markup(
            'PO + XFB flaut.',
            selector=selector,
            )

    @staticmethod
    def pochiss_pont(is_new=True, selector=None):
        return MarkupLibrary.make_markup(
            'pochiss. pont.',
            is_new=is_new,
            selector=selector,
            )

    @staticmethod
    def pochiss_scratch(is_new=True, selector=None):
        return MarkupLibrary.make_markup(
            'pochiss. scratch',
            is_new=is_new,
            selector=selector,
            )

    @staticmethod
    def pochiss_vib(selector=None):
        return MarkupLibrary.make_markup(
            'pochiss. vib.',
            selector=selector,
            )

    @staticmethod
    def poco_pont_plus_non_vib(
        first_is_new=True,
        second_is_new=True,
        selector=None
        ):
        return MarkupLibrary.two_part_transition(
            'poco pont.',
            'non vib.',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            selector=selector,
            )

    @staticmethod
    def poco_pont_plus_sub_non_vib(
        first_is_new=True,
        second_is_new=True,
        selector=None,
        ):
        return MarkupLibrary.two_part_transition(
            'poco pont.',
            'sub. non vib.',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            selector=selector,
            )

    @staticmethod
    def poco_pont_plus_sub_vib_mod(
        first_is_new=True,
        second_is_new=True,
        selector=None,
        ):
        return MarkupLibrary.two_part_transition(
            'poco pont.',
            'sub. vib. mod.',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            selector=selector,
            )

    @staticmethod
    def poco_pont_plus_vib_mod(
        first_is_new=True,
        second_is_new=True,
        selector=None,
        ):
        return MarkupLibrary.two_part_transition(
            'poco pont.',
            'vib. mod.',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            selector=selector,
            )

    @staticmethod
    def poco_scratch(selector=None):
        return MarkupLibrary.make_markup(
            'poco scratch',
            selector=selector,
            )

    @staticmethod
    def pont(selector=None):
        return MarkupLibrary.make_markup(
            'pont.',
            selector=selector,
            )

    @staticmethod
    def pont_XFB(selector=None):
        return MarkupLibrary.make_markup(
            'pont. + XFB',
            selector=selector,
            )

    @staticmethod
    def pont_XFB_flaut(selector=None):
        return MarkupLibrary.make_markup(
            'pont. + XFB flaut.',
            selector=selector,
            )

    @staticmethod
    def ponticello(is_new=True, selector=None):
        return MarkupLibrary.make_markup(
            'ponticello',
            is_new=is_new,
            selector=selector,
            )

    @staticmethod
    def pos_ord(selector=None):
        return MarkupLibrary.make_markup(
            'pos. ord.',
            selector=selector,
            )

    @staticmethod
    def pos_ord_poco_scratch(selector=None):
        return MarkupLibrary.make_markup(
            'pos. ord. + poco scratch',
            selector=selector,
            )

    @staticmethod
    def pos_ord_senza_vib(selector=None):
        return MarkupLibrary.make_markup(
            'pos. ord. + senza vib',
            selector=selector,
            )

    @staticmethod
    def pos_ord_vib_poco(selector=None):
        return MarkupLibrary.make_markup(
            'pos. ord. + vib. poco',
            selector=selector,
            )

    @staticmethod
    def pos_ord_XFB(selector=None):
        return MarkupLibrary.make_markup(
            'pos. ord. + XFB',
            selector=selector,
            )

    @staticmethod
    def pos_ord_XFB_flaut(selector=None):
        return MarkupLibrary.make_markup(
            'pos. ord. + XFB flaut.',
            selector=selector,
            )

    @staticmethod
    def pP_XFB_flaut(selector=None):
        return MarkupLibrary.make_markup(
            'pP + XFB flaut.',
            selector=selector,
            )

    @staticmethod
    def pT_XFB_flaut(selector=None):
        return MarkupLibrary.make_markup(
            'pT + XFB flaut.',
            selector=selector,
            )

    @staticmethod
    def put_reed_back_in(selector=None):
        return MarkupLibrary.boxed(
            'put reed back in',
            selector=selector,
            )

    @staticmethod
    def remove_reed(selector=None):
        return MarkupLibrary.boxed(
            'remove reed',
            selector=selector,
            )

    @staticmethod
    def remove_staple(selector=None):
        return MarkupLibrary.boxed(
            'remove staple',
            selector=selector,
            )

    @staticmethod
    def scratch_moltiss(selector=None):
        return MarkupLibrary.make_markup(
            'scratch moltiss.',
            selector=selector,
            )

    @staticmethod
    def senza_pedale(selector=None):
        return MarkupLibrary.make_markup(
            'senza pedale',
            selector=selector,
            )

    @staticmethod
    def senza_scratch(selector=None):
        return MarkupLibrary.make_markup(
            'senza scratch',
            selector=selector,
            )

    @staticmethod
    def senza_vib(selector=None):
        return MarkupLibrary.make_markup(
            'senza vib.',
            selector=selector,
            )

    @staticmethod
    def shakers(selector=None):
        return MarkupLibrary.make_markup(
            'shakers',
            selector=selector,
            )

    @staticmethod
    def short_instrument(string, column=True):
        r'''Makes short instrument name markup.

        ..  container:: example

            Makes short instrument name markup in column:

            ::

                >>> markup = baca.markup.short_instrument('Eng. hn.')

            ::

                >>> show(markup) # doctest: +SKIP

            ..  docs::

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

                >>> markup = baca.markup.short_instrument(
                ...     'Vn. 1',
                ...     column=False,
                ...     )

            ::

                >>> show(markup) # doctest: +SKIP

            ..  docs::

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
        return MarkupLibrary._make_instrument_name_markup(
            string,
            10,
            column=column,
            )

    @staticmethod
    def sparse_clicks(selector=None):
        first_line = abjad.Markup(
            'sparse, individual clicks with extremely slow bow')
        first_line = first_line.line()
        second_line = abjad.Markup('(1-2/sec. in irregular rhythm)').line()
        markup = abjad.Markup.column(
            [first_line, second_line], direction=abjad.Up)
        return MarkupLibrary()(
            markup=markup,
            selector=selector,
            )

    @staticmethod
    def spazz(selector=None):
        return MarkupLibrary.make_markup(
            'spazz.',
            selector=selector,
            )

    @staticmethod
    def spazzolato(selector=None):
        return MarkupLibrary.make_markup(
            'spazzolato',
            selector=selector,
            )

    @staticmethod
    def spazzolato_1_2_clt(selector=None):
        return MarkupLibrary.make_markup(
            'spazzolato (1/2 clt)',
            selector=selector,
            )

    @staticmethod
    def specifier(
        string,
        direction=abjad.Up,
        is_new=True,
        selector=None,
        whiteout=True,
        ):
        markup = MarkupLibrary.make_markup(
            string,
            direction=direction,
            is_new=is_new,
            whiteout=whiteout,
            )
        return MarkupLibrary()(markup=markup)

    @staticmethod
    def still(is_new=True):
        return MarkupLibrary.make_markup('still', is_new=is_new)

    @staticmethod
    def string_number(n, selector=None):
        to_roman_numeral = {
            1: 'I',
            2: 'II',
            3: 'III',
            4: 'IV',
            }
        string_number = to_roman_numeral[n]
        return MarkupLibrary.make_markup(
            string_number,
            direction=Down,
            selector=selector,
            )

    @staticmethod
    def string_numbers(numbers, selector=None):
        to_roman_numeral = {
            1: 'I',
            2: 'II',
            3: 'III',
            4: 'IV',
            }
        string_numbers = [to_roman_numeral[_] for _ in numbers]
        string_numbers = '+'.join(string_numbers)
        return MarkupLibrary.make_markup(
            string_numbers,
            direction=Down,
            selector=selector,
            )

    @staticmethod
    def subito_non_armonichi_e_non_gridato(selector=None):
        return MarkupLibrary.make_markup(
            'subito non armonichi e non gridato',
            selector=selector,
            )

    @staticmethod
    def subito_ordinario(selector=None):
        return MarkupLibrary.make_markup(
            'subito ordinario',
            selector=selector,
            )

    @staticmethod
    def tamb_tr(is_new=True, selector=None):
        return MarkupLibrary.make_markup(
            'tamb. tr.',
            is_new=is_new,
            selector=selector,
            )

    @staticmethod
    def tasto(is_new=True, selector=None):
        return MarkupLibrary.make_markup(
            'tasto',
            is_new=is_new,
            selector=selector,
            )

    @staticmethod
    def tasto_FB(selector=None):
        return MarkupLibrary.make_markup(
            'tasto + FB',
            selector=selector,
            )

    @staticmethod
    def tasto_FB_flaut(selector=None):
        return MarkupLibrary.make_markup(
            'tasto + FB flaut.',
            selector=selector,
            )

    @staticmethod
    def tasto_fractional_scratch(numerator, denominator, selector=None):
        string = f'tasto + {numerator}/{denominator} scratch'
        return MarkupLibrary.make_markup(
            string,
            selector=selector,
            )

    @staticmethod
    def tasto_half_scratch(selector=None):
        return MarkupLibrary.make_markup(
            'tasto + 1/2 scratch',
            selector=selector,
            )

    @staticmethod
    def tasto_moltiss(selector=None):
        return MarkupLibrary.make_markup(
            'tasto moltiss.',
            selector=selector,
            )

    @staticmethod
    def tasto_NBS(selector=None):
        return MarkupLibrary.make_markup(
            'tasto + NBS',
            selector=selector,
            )

    @staticmethod
    def tasto_plus_non_vib(
        first_is_new=True,
        second_is_new=True,
        selector=None,
        ):
        return MarkupLibrary.two_part_transition(
            'tasto',
            'non vib.',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            selector=selector,
            )

    @staticmethod
    def tasto_plus_pochiss_scratch(selector=None):
        return MarkupLibrary.make_markup(
            'tasto + pochiss. scratch',
            selector=selector,
            )

    @staticmethod
    def tasto_plus_poco_scratch(selector=None):
        return MarkupLibrary.make_markup(
            'tasto + poco scratch',
            selector=selector,
            )

    @staticmethod
    def tasto_plus_poco_vib(
        first_is_new=True,
        second_is_new=True,
        selector=None,
        ):
        return MarkupLibrary.two_part_transition(
            'tasto',
            'poco vib.',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            selector=selector,
            )

    @staticmethod
    def tasto_plus_scratch_moltiss(selector=None):
        return MarkupLibrary.make_markup(
            'tasto + scratch moltiss.',
            selector=selector,
            )

    @staticmethod
    def tasto_poss(is_new=True, selector=None):
        return MarkupLibrary.make_markup(
            'tasto poss.',
            is_new=is_new,
            selector=selector,
            )

    @staticmethod
    def tasto_senza_vib(selector=None):
        return MarkupLibrary.make_markup(
            'tasto + senza vib.',
            selector=selector,
            )

    @staticmethod
    def tasto_slow_bow(selector=None):
        return MarkupLibrary.make_markup(
            'tasto + slow bow (poco scratch)',
            selector=selector,
            )

    @staticmethod
    def tasto_XFB(selector=None):
        return MarkupLibrary.make_markup(
            'tasto + XFB',
            selector=selector,
            )

    @staticmethod
    def tasto_XFB_flaut(selector=None):
        return MarkupLibrary.make_markup(
            'tasto + XFB flaut.',
            selector=selector,
            )

    @staticmethod
    def terminate_abruptly(selector=None):
        return MarkupLibrary.make_markup(
            'terminate abruptly',
            selector=selector,
            )

    @staticmethod
    def terminate_each_note_abruptly(selector=None):
        return MarkupLibrary.make_markup(
            'terminate each note abruptly',
            selector=selector,
            )

    @staticmethod
    def trans(selector=None):
        return MarkupLibrary.make_markup(
            'trans.',
            selector=selector,
            )

    @staticmethod
    def trem_flaut_tast(selector=None):
        return MarkupLibrary.make_markup(
            'trem. flaut. tast.',
            selector=selector,
            )

    @staticmethod
    def two_part_transition(
        string_1,
        string_2,
        first_is_new=True,
        second_is_new=True,
        selector=None,
        ):
        if first_is_new:
            if second_is_new:
                composite_string = f'{string_1} + {string_2}'
            else:
                composite_string = f'{string_1} (+{string_2})'
        else:
            if second_is_new:
                composite_string = f'({string_1}+) {string_2}'
            else:
                composite_string = f'({string_1} + {string_2})'
        return MarkupLibrary.make_markup(
            composite_string,
            selector=selector,
            )

    @staticmethod
    def vib_moltiss(selector=None):
        return MarkupLibrary.make_markup(
            'vib. moltiss.',
            selector=selector,
            )

    @staticmethod
    def vib_pochiss(selector=None):
        return MarkupLibrary.make_markup(
            'vib. pochiss.',
            selector=selector,
            )

    @staticmethod
    def vib_poco(selector=None):
        return MarkupLibrary.make_markup(
            'vib. poco.',
            selector=selector,
            )

    @staticmethod
    def XFB(selector=None):
        return MarkupLibrary.make_markup(
            'XFB',
            selector=selector,
            )

    @staticmethod
    def XFB_flaut(selector=None):
        return MarkupLibrary.make_markup(
            'XFB flaut.',
            selector=selector,
            )

    @staticmethod
    def XFB_plus_pochiss_pont(
        first_is_new=True,
        second_is_new=True,
        selector=None,
        ):
        return MarkupLibrary.two_part_transition(
            'XFB',
            'pochiss. pont.',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            selector=selector,
            )

    @staticmethod
    def XFB_plus_tasto(
        first_is_new=True,
        second_is_new=True,
        selector=None,
        ):
        return MarkupLibrary.two_part_transition(
            'XFB',
            'tasto',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            selector=selector,
            )

    @staticmethod
    def XFB_sempre(selector=None):
        return MarkupLibrary.make_markup(
            'XFB sempre',
            selector=selector,
            )

    @staticmethod
    def XP(selector=None):
        return MarkupLibrary.make_markup(
            'XP',
            selector=selector,
            )

    @staticmethod
    def XP_FB(selector=None):
        return MarkupLibrary.make_markup(
            'XP + FB',
            selector=selector,
            )

    @staticmethod
    def XP_FB_flaut(selector=None):
        return MarkupLibrary.make_markup(
            'XP + FB flaut.',
            selector=selector,
            )

    @staticmethod
    def XP_full_bow_strokes(selector=None):
        return MarkupLibrary.make_markup(
            'XP + full bow strokes',
            selector=selector,
            )

    @staticmethod
    def XP_XFB(selector=None):
        return MarkupLibrary.make_markup(
            'XP + XFB',
            selector=selector,
            )

    @staticmethod
    def XP_XFB_flaut(selector=None):
        return MarkupLibrary.make_markup(
            'XP + XFB flaut.',
            selector=selector,
            )

    @staticmethod
    def XT(selector=None):
        return MarkupLibrary.make_markup(
            'XT',
            selector=selector,
            )
