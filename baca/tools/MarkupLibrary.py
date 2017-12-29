import abjad
import baca


class MarkupLibrary(abjad.AbjadObject):
    r'''Markup library.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(1) Library'

    ### SPECIAL METHODS ###

    @staticmethod
    def __call__(
        argument,
        selector='baca.phead(0)',
        direction=abjad.Up,
        is_new=True,
        upright=True,
        whiteout=True,
        ):
        r'''Makes markup and inserts into indicator command.

        ..  container:: example

            Attaches markup to pitched head 0:

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
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                [
                                ^ \markup {                                                              %! IC1
                                    \whiteout                                                            %! IC1
                                        \upright                                                         %! IC1
                                            "più mosso"                                                  %! IC1
                                    }                                                                    %! IC1
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
                                \revert TupletBracket.staff-padding
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
            ...     baca.markup('più mosso', baca.tuplets()[1:2].phead(0)),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
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
                                ^ \markup {                                                              %! IC1
                                    \whiteout                                                            %! IC1
                                        \upright                                                         %! IC1
                                            "più mosso"                                                  %! IC1
                                    }                                                                    %! IC1
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
                                \revert TupletBracket.staff-padding
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
            ...     baca.markup('*', baca.tuplets()[1:2].pheads()),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
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
                                ^ \markup {                                                              %! IC1
                                    \whiteout                                                            %! IC1
                                        \upright                                                         %! IC1
                                            *                                                            %! IC1
                                    }                                                                    %! IC1
                                e''16
                                ]
                                ^ \markup {                                                              %! IC1
                                    \whiteout                                                            %! IC1
                                        \upright                                                         %! IC1
                                            *                                                            %! IC1
                                    }                                                                    %! IC1
                                ef''4
                                ~
                                ^ \markup {                                                              %! IC1
                                    \whiteout                                                            %! IC1
                                        \upright                                                         %! IC1
                                            *                                                            %! IC1
                                    }                                                                    %! IC1
                                ef''16
                                r16
                                af''16
                                [
                                ^ \markup {                                                              %! IC1
                                    \whiteout                                                            %! IC1
                                        \upright                                                         %! IC1
                                            *                                                            %! IC1
                                    }                                                                    %! IC1
                                g''16
                                ]
                                ^ \markup {                                                              %! IC1
                                    \whiteout                                                            %! IC1
                                        \upright                                                         %! IC1
                                            *                                                            %! IC1
                                    }                                                                    %! IC1
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        Returns indicator command.
        '''
        selector = selector or baca.phead(0)
        if isinstance(argument, str):
            if not is_new:
                argument = f'({argument})'
            markup = abjad.Markup(argument, direction=direction)
        elif isinstance(argument, abjad.Markup):
            markup = abjad.new(argument, direction=direction)
        if upright:
            markup = markup.upright()
        if whiteout:
            markup = markup.whiteout()
        return baca.IndicatorCommand(
            indicators=[markup],
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
    def accent_changes_of_direction(selector='baca.pleaf(0)'):
        string = 'accent changes of direction noticeably at each attack'
        return baca.markup(
            string,
            selector=selector,
            )

    @staticmethod
    def airtone(selector='baca.pleaf(0)'):
        return baca.markup(
            'airtone',
            selector=selector,
            )

    @staticmethod
    def allow_bowing_to_convey_accelerando(selector='baca.pleaf(0)'):
        return baca.markup(
            'allow bowing to convey accelerando',
            selector=selector,
            )

    @staticmethod
    def arco(selector='baca.pleaf(0)'):
        return baca.markup(
            'arco',
            selector=selector,
            )

    @staticmethod
    def arco_ordinario(selector='baca.pleaf(0)'):
        return baca.markup(
            'arco ordinario',
            selector=selector,
            )

    @staticmethod
    def attackless(selector='baca.pleaf(0)'):
        return baca.markup(
            'attackless',
            selector=selector,
            )

    @staticmethod
    def bow_on_tailpiece(selector='baca.pleaf(0)'):
        return baca.markup(
            'bow on tailpiece',
            selector=selector,
            )

    @staticmethod
    def bow_on_wooden_mute(selector='baca.pleaf(0)'):
        return baca.markup(
            'bow on wooden mute',
            selector=selector,
            )

    @staticmethod
    def boxed(string, selector='baca.leaf(0)'):
        markup = abjad.Markup(string, direction=abjad.Up)
        markup = markup.box().override(('box-padding', 0.5))
        return baca.markup(
            markup,
            selector=selector,
            )

    @staticmethod
    def boxed_lines(
        strings,
        direction=abjad.Up,
        selector='baca.leaf(0)',
        ):
        assert isinstance(strings, list), repr(strings)
        markup = abjad.MarkupList(strings).column(direction=direction)
        markup = markup.box().override(('box-padding', 0.5))
        return baca.markup(
            markup,
            selector=selector,
            )

    @staticmethod
    def boxed_repeat_count(count, selector='baca.leaf(0)'):
        string = f'x{count}'
        markup = abjad.Markup(string, direction=abjad.Up)
        markup = markup.sans().bold().fontsize(6)
        markup = markup.box().override(('box-padding', 0.5))
        return baca.markup(
            markup,
            selector=selector,
            )

    @staticmethod
    def clicks_per_second(lower, upper, selector='baca.pleaf(0)'):
        string = f'{lower}-{upper} clicks/sec.'
        return baca.markup(
            string,
            selector=selector,
            )

    @staticmethod
    def col_legno_battuto(selector='baca.pleaf(0)'):
        return baca.markup(
            'col legno battuto',
            selector=selector,
            )

    @staticmethod
    def delicatiss(selector='baca.pleaf(0)'):
        return baca.markup(
            'delicatiss.',
            selector=selector,
            )

    @staticmethod
    def delicatissimo(selector='baca.pleaf(0)'):
        return baca.markup(
            'delicatissimo',
            selector=selector,
            )

    @staticmethod
    def directly_on_bridge_bow_diagonally(selector='baca.pleaf(0)'):
        string = 'directly on bridge:'
        string += ' bow diagonally to produce white noise w/ no pitch'
        return baca.markup(
            string,
            selector=selector,
            )

    @staticmethod
    def directly_on_bridge_very_slow_bow(selector='baca.pleaf(0)'):
        string = 'directly on bridge:'
        string += ' very slow bow, imperceptible bow changes'
        return baca.markup(
            string,
            selector=selector,
            )

    @staticmethod
    def estr_sul_pont(selector='baca.pleaf(0)'):
        return baca.markup(
            'estr. sul pont.',
            selector=selector,
            )

    @staticmethod
    def FB(selector='baca.pleaf(0)'):
        return baca.markup(
            'FB',
            selector=selector,
            )

    @staticmethod
    def FB_flaut(selector='baca.pleaf(0)'):
        return baca.markup(
            'FB flaut.',
            selector=selector,
            )

    @staticmethod
    def final_markup(places, dates, selector='baca.leaf(-1)'):
        places = r' \hspace #0.75 – \hspace #0.75 '.join(places)
        places = abjad.Markup(places)
        places = abjad.Markup.line([places])
        dates = r' \hspace #0.75 – \hspace #0.75 '.join(dates)
        dates = abjad.Markup(dates)
        dates = abjad.Markup.line([dates])
        markup = abjad.Markup.right_column([places, dates])
        markup = markup.with_color('black')
        return baca.markup(
            markup,
            direction=abjad.Down,
            selector=selector,
            )

    @staticmethod
    def fluttertongue(selector='baca.pleaf(0)'):
        return baca.markup(
            'fluttertongue',
            selector=selector,
            )

    @staticmethod
    def fractional_OB(numerator, denominator, selector='baca.pleaf(0)'):
        string = f'{numerator}/{denominator}OB'
        return baca.markup(
            string,
            selector=selector,
            )

    @staticmethod
    def fractional_scratch(numerator, denominator, selector='baca.pleaf(0)'):
        string = f'{numerator}/{denominator} scratch'
        return baca.markup(
            string,
            selector=selector,
            )

    @staticmethod
    def full_bow_strokes(selector='baca.pleaf(0)'):
        return baca.markup(
            'full bow strokes',
            selector=selector,
            )

    @staticmethod
    def glissando_lentissimo(selector='baca.pleaf(0)'):
        return baca.markup(
            'glissando lentissimo',
            selector=selector,
            )

    @staticmethod
    def gridato_possibile(selector='baca.pleaf(0)'):
        return baca.markup(
            'gridato possibile',
            selector=selector,
            )

    @staticmethod
    def instrument(string, hcenter_in=16, column=True):
        r'''Makes instrument name markup.

        ..  container:: example

            Makes instrument name markup in column:

            >>> markup = baca.markup.instrument('Eng. horn')

            >>> abjad.show(markup, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(markup, strict=89)
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
            hcenter_in,
            column=column,
            )

    @staticmethod
    def kn_rasg(is_new=True, selector='baca.pleaf(0)'):
        return baca.markup(
            'kn. rasg.',
            is_new=is_new,
            selector=selector,
            )

    @staticmethod
    def knuckle_rasg(is_new=True, selector='baca.pleaf(0)'):
        return baca.markup(
            'knuckle rasg.',
            is_new=is_new,
            selector=selector,
            )

    @staticmethod
    def leggieriss(selector='baca.pleaf(0)'):
        return baca.markup(
            'leggieriss.',
            selector=selector,
            )

    @staticmethod
    def leggierissimo(selector='baca.pleaf(0)'):
        return baca.markup(
            'leggierissimo',
            selector=selector,
            )

    @staticmethod
    def leggierissimo_off_string_bowing_on_staccati(selector='baca.pleaf(0)'):
        return baca.markup(
            'leggierissimo: off-string bowing on staccati',
            selector=selector,
            )

    @staticmethod
    def lines(strings, direction=abjad.Up, selector='baca.leaf(0)'):
        assert isinstance(strings, list), repr(strings)
        markup = abjad.MarkupList(strings).column(direction=direction)
        return baca.markup(
            markup,
            selector=selector,
            )

    @staticmethod
    def lv_possibile(selector='baca.ptail(0)'):
        return baca.markup(
            'l.v. possibile',
            selector=selector,
            )

    @staticmethod
    def molto_flautando(selector='baca.pleaf(0)'):
        return baca.markup(
            'molto flautando',
            selector=selector,
            )

    @staticmethod
    def molto_flautando_e_pont(selector='baca.pleaf(0)'):
        return baca.markup(
            'molto flautando ed estr. sul pont.',
            selector=selector,
            )

    @staticmethod
    def molto_gridato(selector='baca.pleaf(0)'):
        return baca.markup(
            'molto gridato ed estr. sul pont.',
            selector=selector,
            )

    @staticmethod
    def molto_pont_plus_vib_molto(
        first_is_new=True,
        second_is_new=True,
        selector='baca.pleaf(0)',
        ):
        return MarkupLibrary.two_part_transition(
            'molto pont.',
            'vib. molto',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            selector=selector,
            )

    @staticmethod
    def MP_XFB_flaut(selector='baca.pleaf(0)'):
        return baca.markup(
            'MP + XFB flaut.',
            selector=selector,
            )

    @staticmethod
    def nail_rasg(is_new=True, selector='baca.pleaf(0)'):
        return baca.markup(
            'nail rasg.',
            is_new=is_new,
            selector=selector,
            )

    @staticmethod
    def nail_rasgueado(is_new=True, selector='baca.pleaf(0)'):
        return baca.markup(
            'nail rasgueado',
            is_new=is_new,
            selector=selector,
            )

    @staticmethod
    def non_flautando(selector='baca.pleaf(0)'):
        return baca.markup(
            'non flautando',
            selector=selector,
            )

    @staticmethod
    def non_flutt(selector='baca.pleaf(0)'):
        return baca.markup(
            'non flutt.',
            selector=selector,
            )

    @staticmethod
    def non_spazz(selector='baca.pleaf(0)'):
        return baca.markup(
            'non spazz.',
            selector=selector,
            )

    @staticmethod
    def nut(selector='baca.pleaf(0)'):
        return baca.markup(
            'nut',
            selector=selector,
            )

    @staticmethod
    def OB(selector='baca.pleaf(0)'):
        return baca.markup(
            'OB',
            selector=selector,
            )

    @staticmethod
    def OB_full_bow_strokes(selector='baca.pleaf(0)'):
        return baca.markup(
            'OB + full bow strokes',
            selector=selector,
            )

    @staticmethod
    def OB_no_pitch(selector='baca.pleaf(0)'):
        return baca.markup(
            'OB (no pitch)',
            selector=selector,
            )

    @staticmethod
    def OB_terminate_abruptly(selector='baca.pleaf(0)'):
        return baca.markup(
            'OB + terminate abruptly',
            selector=selector,
            )

    @staticmethod
    def OB_terminate_each_note_abruptly(selector='baca.pleaf(0)'):
        return baca.markup(
            'OB + terminate each note abruptly',
            selector=selector,
            )

    @staticmethod
    def off_string_bowing_on_staccati(selector='baca.pleaf(0)'):
        return baca.markup(
            'off-string bowing on staccati',
            selector=selector,
            )

    @staticmethod
    def one_click_every(lower, upper, selector='baca.pleaf(0)'):
        string = f'1 click/{lower}-{upper} sec.'
        return baca.markup(
            string,
            selector=selector,
            )

    @staticmethod
    def ord(selector='baca.pleaf(0)'):
        return baca.markup(
            'ord.',
            selector=selector,
            )

    @staticmethod
    def ord_poco_scratch(selector='baca.pleaf(0)'):
        return baca.markup(
            'ord. + poco scratch',
            selector=selector,
            )

    @staticmethod
    def ord_senza_scratch(selector='baca.pleaf(0)'):
        return baca.markup(
            'ord. (senza scratch)',
            selector=selector,
            )

    @staticmethod
    def ordinario(selector='baca.pleaf(0)'):
        return baca.markup(
            'ordinario',
            selector=selector,
            )

    @staticmethod
    def overblow(selector='baca.pleaf(0)'):
        return baca.markup(
            'overblow',
            selector=selector,
            )

    @staticmethod
    def P_XFB_flaut(selector='baca.pleaf(0)'):
        return baca.markup(
            'P + XFB flaut.',
            selector=selector,
            )

    @staticmethod
    def pizz(selector='baca.pleaf(0)'):
        return baca.markup(
            'pizz.',
            selector=selector,
            )

    @staticmethod
    def PO(selector='baca.pleaf(0)'):
        return baca.markup(
            'PO',
            selector=selector,
            )

    @staticmethod
    def PO_FB_flaut(selector='baca.pleaf(0)'):
        return baca.markup(
            'PO + FB flaut.',
            selector=selector,
            )

    @staticmethod
    def po_meno_scratch(selector='baca.pleaf(0)'):
        return baca.markup(
            "po' meno scratch",
            selector=selector,
            )

    @staticmethod
    def PO_NBS(selector='baca.pleaf(0)'):
        return baca.markup(
            'PO + NBS',
            selector=selector,
            )

    @staticmethod
    def PO_plus_non_vib(
        first_is_new=True,
        second_is_new=True,
        selector='baca.pleaf(0)',
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
        selector='baca.pleaf(0)',
        ):
        return MarkupLibrary.two_part_transition(
            'PO',
            'poco vib.',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            selector=selector,
            )

    @staticmethod
    def PO_scratch(selector='baca.pleaf(0)'):
        return baca.markup(
            'PO + scratch',
            selector=selector,
            )

    @staticmethod
    def PO_slow_bow(selector='baca.pleaf(0)'):
        return baca.markup(
            'PO + slow bow (poco scratch)',
            selector=selector,
            )

    @staticmethod
    def PO_XFB_flaut(selector='baca.pleaf(0)'):
        return baca.markup(
            'PO + XFB flaut.',
            selector=selector,
            )

    @staticmethod
    def pochiss_pont(is_new=True, selector='baca.pleaf(0)'):
        return baca.markup(
            'pochiss. pont.',
            is_new=is_new,
            selector=selector,
            )

    @staticmethod
    def pochiss_scratch(is_new=True, selector='baca.pleaf(0)'):
        return baca.markup(
            'pochiss. scratch',
            is_new=is_new,
            selector=selector,
            )

    @staticmethod
    def pochiss_vib(selector='baca.pleaf(0)'):
        return baca.markup(
            'pochiss. vib.',
            selector=selector,
            )

    @staticmethod
    def poco_pont_plus_non_vib(
        first_is_new=True,
        second_is_new=True,
        selector='baca.pleaf(0)',
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
        selector='baca.pleaf(0)',
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
        selector='baca.pleaf(0)',
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
        selector='baca.pleaf(0)',
        ):
        return MarkupLibrary.two_part_transition(
            'poco pont.',
            'vib. mod.',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            selector=selector,
            )

    @staticmethod
    def poco_scratch(selector='baca.pleaf(0)'):
        return baca.markup(
            'poco scratch',
            selector=selector,
            )

    @staticmethod
    def pont(selector='baca.pleaf(0)'):
        return baca.markup(
            'pont.',
            selector=selector,
            )

    @staticmethod
    def pont_XFB(selector='baca.pleaf(0)'):
        return baca.markup(
            'pont. + XFB',
            selector=selector,
            )

    @staticmethod
    def pont_XFB_flaut(selector='baca.pleaf(0)'):
        return baca.markup(
            'pont. + XFB flaut.',
            selector=selector,
            )

    @staticmethod
    def ponticello(is_new=True, selector='baca.pleaf(0)'):
        return baca.markup(
            'ponticello',
            is_new=is_new,
            selector=selector,
            )

    @staticmethod
    def pos_ord(selector='baca.pleaf(0)'):
        return baca.markup(
            'pos. ord.',
            selector=selector,
            )

    @staticmethod
    def pos_ord_poco_scratch(selector='baca.pleaf(0)'):
        return baca.markup(
            'pos. ord. + poco scratch',
            selector=selector,
            )

    @staticmethod
    def pos_ord_senza_vib(selector='baca.pleaf(0)'):
        return baca.markup(
            'pos. ord. + senza vib',
            selector=selector,
            )

    @staticmethod
    def pos_ord_vib_poco(selector='baca.pleaf(0)'):
        return baca.markup(
            'pos. ord. + vib. poco',
            selector=selector,
            )

    @staticmethod
    def pos_ord_XFB(selector='baca.pleaf(0)'):
        return baca.markup(
            'pos. ord. + XFB',
            selector=selector,
            )

    @staticmethod
    def pos_ord_XFB_flaut(selector='baca.pleaf(0)'):
        return baca.markup(
            'pos. ord. + XFB flaut.',
            selector=selector,
            )

    @staticmethod
    def pP_XFB_flaut(selector='baca.pleaf(0)'):
        return baca.markup(
            'pP + XFB flaut.',
            selector=selector,
            )

    @staticmethod
    def pT_XFB_flaut(selector='baca.pleaf(0)'):
        return baca.markup(
            'pT + XFB flaut.',
            selector=selector,
            )

    @staticmethod
    def put_reed_back_in(selector='baca.leaf(0)'):
        return MarkupLibrary.boxed(
            'put reed back in',
            selector=selector,
            )

    @staticmethod
    def remove_reed(selector='baca.leaf(0)'):
        return MarkupLibrary.boxed(
            'remove reed',
            selector=selector,
            )

    @staticmethod
    def remove_staple(selector='baca.leaf(0)'):
        return MarkupLibrary.boxed(
            'remove staple',
            selector=selector,
            )

    @staticmethod
    def scratch_moltiss(selector='baca.pleaf(0)'):
        return baca.markup(
            'scratch moltiss.',
            selector=selector,
            )

    @staticmethod
    def senza_pedale(selector='baca.pleaf(0)'):
        return baca.markup(
            'senza pedale',
            selector=selector,
            )

    @staticmethod
    def senza_scratch(selector='baca.pleaf(0)'):
        return baca.markup(
            'senza scratch',
            selector=selector,
            )

    @staticmethod
    def senza_vib(selector='baca.pleaf(0)'):
        return baca.markup(
            'senza vib.',
            selector=selector,
            )

    @staticmethod
    def shakers(selector='baca.leaf(0)'):
        return baca.markup(
            'shakers',
            selector=selector,
            )

    @staticmethod
    def short_instrument(string, hcenter_in=10, column=True):
        r'''Makes short instrument name markup.

        ..  container:: example

            Makes short instrument name markup in column:

            >>> markup = baca.markup.short_instrument('Eng. hn.')

            >>> abjad.show(markup, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(markup, strict=89)
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
            hcenter_in,
            column=column,
            )

    @staticmethod
    def sparse_clicks(selector='baca.pleaf(0)'):
        first_line = abjad.Markup(
            'sparse, individual clicks with extremely slow bow')
        first_line = first_line.line()
        second_line = abjad.Markup('(1-2/sec. in irregular rhythm)').line()
        markup = abjad.Markup.column(
            [first_line, second_line], direction=abjad.Up)
        return baca.markup(
            markup,
            selector=selector,
            )

    @staticmethod
    def spazz(selector='baca.pleaf(0)'):
        return baca.markup(
            'spazz.',
            selector=selector,
            )

    @staticmethod
    def spazzolato(selector='baca.pleaf(0)'):
        return baca.markup(
            'spazzolato',
            selector=selector,
            )

    @staticmethod
    def spazzolato_1_2_clt(selector='baca.pleaf(0)'):
        return baca.markup(
            'spazzolato (1/2 clt)',
            selector=selector,
            )

    @staticmethod
    def still(is_new=True, selector='baca.leaf(0)'):
        return baca.markup(
            'still',
            is_new=is_new,
            selector=selector,
            )

    @staticmethod
    def string_number(n, selector='baca.pleaf(0)'):
        to_roman_numeral = {
            1: 'I',
            2: 'II',
            3: 'III',
            4: 'IV',
            }
        string_number = to_roman_numeral[n]
        return baca.markup(
            string_number,
            direction=abjad.Down,
            selector=selector,
            )

    @staticmethod
    def string_numbers(numbers, selector='baca.pleaf(0)'):
        to_roman_numeral = {
            1: 'I',
            2: 'II',
            3: 'III',
            4: 'IV',
            }
        string_numbers = [to_roman_numeral[_] for _ in numbers]
        string_numbers = '+'.join(string_numbers)
        return baca.markup(
            string_numbers,
            direction=abjad.Down,
            selector=selector,
            )

    @staticmethod
    def subito_non_armonichi_e_non_gridato(selector='baca.pleaf(0)'):
        return baca.markup(
            'subito non armonichi e non gridato',
            selector=selector,
            )

    @staticmethod
    def subito_ordinario(selector='baca.pleaf(0)'):
        return baca.markup(
            'subito ordinario',
            selector=selector,
            )

    @staticmethod
    def tamb_tr(is_new=True, selector='baca.pleaf(0)'):
        return baca.markup(
            'tamb. tr.',
            is_new=is_new,
            selector=selector,
            )

    @staticmethod
    def tasto(is_new=True, selector='baca.pleaf(0)'):
        return baca.markup(
            'tasto',
            is_new=is_new,
            selector=selector,
            )

    @staticmethod
    def tasto_FB(selector='baca.pleaf(0)'):
        return baca.markup(
            'tasto + FB',
            selector=selector,
            )

    @staticmethod
    def tasto_FB_flaut(selector='baca.pleaf(0)'):
        return baca.markup(
            'tasto + FB flaut.',
            selector=selector,
            )

    @staticmethod
    def tasto_fractional_scratch(
        numerator,
        denominator,
        selector='baca.pleaf(0)',
        ):
        string = f'tasto + {numerator}/{denominator} scratch'
        return baca.markup(
            string,
            selector=selector,
            )

    @staticmethod
    def tasto_half_scratch(selector='baca.pleaf(0)'):
        return baca.markup(
            'tasto + 1/2 scratch',
            selector=selector,
            )

    @staticmethod
    def tasto_moltiss(selector='baca.pleaf(0)'):
        return baca.markup(
            'tasto moltiss.',
            selector=selector,
            )

    @staticmethod
    def tasto_NBS(selector='baca.pleaf(0)'):
        return baca.markup(
            'tasto + NBS',
            selector=selector,
            )

    @staticmethod
    def tasto_plus_non_vib(
        first_is_new=True,
        second_is_new=True,
        selector='baca.pleaf(0)',
        ):
        return MarkupLibrary.two_part_transition(
            'tasto',
            'non vib.',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            selector=selector,
            )

    @staticmethod
    def tasto_plus_pochiss_scratch(selector='baca.pleaf(0)'):
        return baca.markup(
            'tasto + pochiss. scratch',
            selector=selector,
            )

    @staticmethod
    def tasto_plus_poco_scratch(selector='baca.pleaf(0)'):
        return baca.markup(
            'tasto + poco scratch',
            selector=selector,
            )

    @staticmethod
    def tasto_plus_poco_vib(
        first_is_new=True,
        second_is_new=True,
        selector='baca.pleaf(0)',
        ):
        return MarkupLibrary.two_part_transition(
            'tasto',
            'poco vib.',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            selector=selector,
            )

    @staticmethod
    def tasto_plus_scratch_moltiss(selector='baca.pleaf(0)'):
        return baca.markup(
            'tasto + scratch moltiss.',
            selector=selector,
            )

    @staticmethod
    def tasto_poss(is_new=True, selector='baca.pleaf(0)'):
        return baca.markup(
            'tasto poss.',
            is_new=is_new,
            selector=selector,
            )

    @staticmethod
    def tasto_senza_vib(selector='baca.pleaf(0)'):
        return baca.markup(
            'tasto + senza vib.',
            selector=selector,
            )

    @staticmethod
    def tasto_slow_bow(selector='baca.pleaf(0)'):
        return baca.markup(
            'tasto + slow bow (poco scratch)',
            selector=selector,
            )

    @staticmethod
    def tasto_XFB(selector='baca.pleaf(0)'):
        return baca.markup(
            'tasto + XFB',
            selector=selector,
            )

    @staticmethod
    def tasto_XFB_flaut(selector='baca.pleaf(0)'):
        return baca.markup(
            'tasto + XFB flaut.',
            selector=selector,
            )

    @staticmethod
    def terminate_abruptly(selector='baca.pleaf(0)'):
        return baca.markup(
            'terminate abruptly',
            selector=selector,
            )

    @staticmethod
    def terminate_each_note_abruptly(selector='baca.pleaf(0)'):
        return baca.markup(
            'terminate each note abruptly',
            selector=selector,
            )

    @staticmethod
    def trans(selector='baca.pleaf(0)'):
        return baca.markup(
            'trans.',
            selector=selector,
            )

    @staticmethod
    def trem_flaut_tast(selector='baca.pleaf(0)'):
        return baca.markup(
            'trem. flaut. tast.',
            selector=selector,
            )

    @staticmethod
    def two_part_transition(
        string_1,
        string_2,
        first_is_new=True,
        second_is_new=True,
        selector='baca.pleaf(0)',
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
        return baca.markup(
            composite_string,
            selector=selector,
            )

    @staticmethod
    def vib_moltiss(selector='baca.pleaf(0)'):
        return baca.markup(
            'vib. moltiss.',
            selector=selector,
            )

    @staticmethod
    def vib_pochiss(selector='baca.pleaf(0)'):
        return baca.markup(
            'vib. pochiss.',
            selector=selector,
            )

    @staticmethod
    def vib_poco(selector='baca.pleaf(0)'):
        return baca.markup(
            'vib. poco.',
            selector=selector,
            )

    @staticmethod
    def XFB(selector='baca.pleaf(0)'):
        return baca.markup(
            'XFB',
            selector=selector,
            )

    @staticmethod
    def XFB_flaut(selector='baca.pleaf(0)'):
        return baca.markup(
            'XFB flaut.',
            selector=selector,
            )

    @staticmethod
    def XFB_plus_pochiss_pont(
        first_is_new=True,
        second_is_new=True,
        selector='baca.pleaf(0)',
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
        selector='baca.pleaf(0)',
        ):
        return MarkupLibrary.two_part_transition(
            'XFB',
            'tasto',
            first_is_new=first_is_new,
            second_is_new=second_is_new,
            selector=selector,
            )

    @staticmethod
    def XFB_sempre(selector='baca.pleaf(0)'):
        return baca.markup(
            'XFB sempre',
            selector=selector,
            )

    @staticmethod
    def XP(selector='baca.pleaf(0)'):
        return baca.markup(
            'XP',
            selector=selector,
            )

    @staticmethod
    def XP_FB(selector='baca.pleaf(0)'):
        return baca.markup(
            'XP + FB',
            selector=selector,
            )

    @staticmethod
    def XP_FB_flaut(selector='baca.pleaf(0)'):
        return baca.markup(
            'XP + FB flaut.',
            selector=selector,
            )

    @staticmethod
    def XP_full_bow_strokes(selector='baca.pleaf(0)'):
        return baca.markup(
            'XP + full bow strokes',
            selector=selector,
            )

    @staticmethod
    def XP_XFB(selector='baca.pleaf(0)'):
        return baca.markup(
            'XP + XFB',
            selector=selector,
            )

    @staticmethod
    def XP_XFB_flaut(selector='baca.pleaf(0)'):
        return baca.markup(
            'XP + XFB flaut.',
            selector=selector,
            )

    @staticmethod
    def XT(selector='baca.pleaf(0)'):
        return baca.markup(
            'XT',
            selector=selector,
            )
