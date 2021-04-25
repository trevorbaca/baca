import inspect
import typing

import ide

import abjad

from . import (
    classes,
    commandclasses,
    const,
    indicatorcommands,
    indicators,
    overrides,
    pitchcommands,
    scoping,
    typings,
)


def _site(frame, n=None):
    prefix = "baca"
    return scoping.site(frame, prefix, n=n)


### FACTORY FUNCTIONS ###


def allow_octaves(
    *, selector=lambda _: classes.Selection(_).leaves()
) -> commandclasses.IndicatorCommand:
    """
    Attaches ALLOW_OCTAVE constant.
    """
    return commandclasses.IndicatorCommand(
        indicators=[const.ALLOW_OCTAVE], selector=selector
    )


def bcps(
    bcps,
    *tweaks: abjad.IndexedTweakManager,
    bow_change_tweaks: abjad.IndexedTweakManagers = None,
    final_spanner: bool = None,
    helper: typing.Callable = None,
    selector=lambda _: classes.Selection(_).leaves(),
) -> commandclasses.BCPCommand:
    r"""
    Makes bow contact point command.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 16)),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.make_even_divisions(),
            ...     baca.bcps(
            ...         [(1, 5), (3, 5), (2, 5), (4, 5), (5, 5)],
            ...         ),
            ...     baca.pitches('E4 F4'),
            ...     baca.script_staff_padding(5.5),
            ...     baca.text_spanner_staff_padding(2.5),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
                <BLANKLINE>
                \context Score = "Score"
                <<
                <BLANKLINE>
                    \context GlobalContext = "Global_Context"
                    <<
                <BLANKLINE>
                        \context GlobalSkips = "Global_Skips"
                        {
                <BLANKLINE>
                            % [Global_Skips measure 1]
                            \baca-new-spacing-section #1 #16
                            \time 4/8
                            \baca-time-signature-color #'blue
                            s1 * 1/2
                <BLANKLINE>
                            % [Global_Skips measure 2]
                            \baca-new-spacing-section #1 #16
                            \time 3/8
                            \baca-time-signature-color #'blue
                            s1 * 3/8
                <BLANKLINE>
                            % [Global_Skips measure 3]
                            \baca-new-spacing-section #1 #16
                            \time 4/8
                            \baca-time-signature-color #'blue
                            s1 * 1/2
                <BLANKLINE>
                            % [Global_Skips measure 4]
                            \baca-new-spacing-section #1 #16
                            \time 3/8
                            \baca-time-signature-color #'blue
                            s1 * 3/8
                <BLANKLINE>
                            % [Global_Skips measure 5]
                            \baca-new-spacing-section #1 #4
                            \time 1/4
                            \baca-time-signature-transparent
                            s1 * 1/4
                            \once \override Score.BarLine.transparent = ##t
                            \once \override Score.SpanBar.transparent = ##t
                <BLANKLINE>
                        }
                <BLANKLINE>
                    >>
                <BLANKLINE>
                    \context MusicContext = "Music_Context"
                    <<
                <BLANKLINE>
                        \context Staff = "Music_Staff"
                        {
                <BLANKLINE>
                            \context Voice = "Music_Voice"
                            {
                <BLANKLINE>
                                % [Music_Voice measure 1]
                                \override Script.staff-padding = 5.5
                                \override TextSpanner.staff-padding = 2.5
                                e'8
                                - \downbow
                                [
                                - \abjad-dashed-line-with-hook
                                - \baca-text-spanner-left-text "make_even_divisions()"
                                - \tweak bound-details.right.padding 2.75
                                - \tweak color #darkcyan
                                - \tweak staff-padding 8
                                \bacaStartTextSpanRhythmAnnotation
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #1 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                f'8
                                - \upbow
                                \bacaStopTextSpanBCP
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #3 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                e'8
                                - \downbow
                                \bacaStopTextSpanBCP
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #2 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                f'8
                                \bacaStopTextSpanBCP
                                ]
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #4 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                % [Music_Voice measure 2]
                                e'8
                                - \upbow
                                \bacaStopTextSpanBCP
                                [
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #5 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                f'8
                                - \downbow
                                \bacaStopTextSpanBCP
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #1 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                e'8
                                - \upbow
                                \bacaStopTextSpanBCP
                                ]
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #3 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                % [Music_Voice measure 3]
                                f'8
                                - \downbow
                                \bacaStopTextSpanBCP
                                [
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #2 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                e'8
                                \bacaStopTextSpanBCP
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #4 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                f'8
                                - \upbow
                                \bacaStopTextSpanBCP
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #5 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                e'8
                                - \downbow
                                \bacaStopTextSpanBCP
                                ]
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #1 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                % [Music_Voice measure 4]
                                f'8
                                - \upbow
                                \bacaStopTextSpanBCP
                                [
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #3 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                e'8
                                - \downbow
                                \bacaStopTextSpanBCP
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #2 #5
                                - \baca-bcp-spanner-right-text #4 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                f'8
                                \bacaStopTextSpanBCP
                                ]
                                \revert Script.staff-padding
                                \revert TextSpanner.staff-padding
                                <> \bacaStopTextSpanRhythmAnnotation
                <BLANKLINE>
                                <<
                <BLANKLINE>
                                    \context Voice = "Music_Voice"
                                    {
                <BLANKLINE>
                                        % [Music_Voice measure 5]
                                        \abjad-invisible-music-coloring
                                        %@% \abjad-invisible-music
                                        \baca-not-yet-pitched-coloring
                                        b'1 * 1/4
                                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                <BLANKLINE>
                                    }
                <BLANKLINE>
                                    \context Voice = "Rest_Voice"
                                    {
                <BLANKLINE>
                                        % [Rest_Voice measure 5]
                                        \once \override Score.TimeSignature.X-extent = ##f
                                        \once \override MultiMeasureRest.transparent = ##t
                                        \stopStaff
                                        \once \override Staff.StaffSymbol.transparent = ##t
                                        \startStaff
                                        R1 * 1/4
                                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                <BLANKLINE>
                                    }
                <BLANKLINE>
                                >>
                <BLANKLINE>
                            }
                <BLANKLINE>
                        }
                <BLANKLINE>
                    >>
                <BLANKLINE>
                >>

    """
    if final_spanner is not None:
        final_spanner = bool(final_spanner)
    return commandclasses.BCPCommand(
        bcps=bcps,
        bow_change_tweaks=bow_change_tweaks,
        final_spanner=final_spanner,
        helper=helper,
        selector=selector,
        tags=[_site(inspect.currentframe())],
        tweaks=tweaks,
    )


def close_volta(
    selector=lambda _: classes.Selection(_).leaf(0),
    *,
    format_slot: str = "before",
) -> scoping.Suite:
    """
    Attaches bar line and overrides bar line X-extent.
    """
    assert format_slot in ("after", "before"), repr(format_slot)
    after = format_slot == "after"
    # does not require not_mol() tagging, just only_mol() tagging:
    return scoping.suite(
        indicatorcommands.bar_line(":|.", selector, format_slot=format_slot),
        scoping.only_mol(overrides.bar_line_x_extent((0, 1.5), selector, after=after)),
    )


def color(
    selector=lambda _: classes.Selection(_).leaves(),
    lone=False,
) -> commandclasses.ColorCommand:
    r"""
    Makes color command.

    ..  container:: example

        Colors leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.color(),
        ...     rmakers.unbeam(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.illustrators.attach_markup_struts(lilypond_file)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = 2
                        \abjad-color-music #'red
                        r8
                        - \tweak staff-padding 11
                        - \tweak transparent ##t
                        ^ \markup I
                        \abjad-color-music #'blue
                        c'16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'blue
                        bf'4
                        ~
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \abjad-color-music #'red
                        fs''16
                        \abjad-color-music #'blue
                        e''16
                        \abjad-color-music #'red
                        ef''4
                        ~
                        \abjad-color-music #'blue
                        ef''16
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'blue
                        af''16
                        \abjad-color-music #'red
                        g''16
                    }
                    \times 4/5 {
                        \abjad-color-music #'blue
                        a'16
                        \abjad-color-music #'red
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Colors leaves in tuplet 1:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.color(lambda _: baca.Selection(_).tuplets()[1:2].leaves()),
        ...     rmakers.unbeam(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.illustrators.attach_markup_struts(lilypond_file)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = 2
                        r8
                        - \tweak staff-padding 11
                        - \tweak transparent ##t
                        ^ \markup I
                        c'16
                        d'16
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \abjad-color-music #'red
                        fs''16
                        \abjad-color-music #'blue
                        e''16
                        \abjad-color-music #'red
                        ef''4
                        ~
                        \abjad-color-music #'blue
                        ef''16
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'blue
                        af''16
                        \abjad-color-music #'red
                        g''16
                    }
                    \times 4/5 {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return commandclasses.ColorCommand(selector=selector, lone=lone)


def container(
    identifier: str = None,
    *,
    selector=lambda _: classes.Selection(_).leaves(),
) -> commandclasses.ContainerCommand:
    r"""
    Makes container with ``identifier`` and extends container with
    ``selector`` output.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.container('ViolinI', selector=baca.leaves()[:2]),
        ...     baca.container('ViolinII', selector=baca.leaves()[2:]),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')

        >>> string = abjad.lilypond(lilypond_file[abjad.Score])
        >>> print(string)
        <BLANKLINE>
        \context Score = "Score"
        <<
        <BLANKLINE>
            \context GlobalContext = "Global_Context"
            <<
        <BLANKLINE>
                \context GlobalSkips = "Global_Skips"
                {
        <BLANKLINE>
                    % [Global_Skips measure 1]
                    \time 4/8
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 2]
                    \time 3/8
                    \baca-time-signature-color #'blue
                    s1 * 3/8
        <BLANKLINE>
                    % [Global_Skips measure 3]
                    \time 4/8
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 4]
                    \time 3/8
                    \baca-time-signature-color #'blue
                    s1 * 3/8
        <BLANKLINE>
                    % [Global_Skips measure 5]
                    \time 1/4
                    \baca-time-signature-transparent
                    s1 * 1/4
                    \once \override Score.BarLine.transparent = ##t
                    \once \override Score.SpanBar.transparent = ##t
        <BLANKLINE>
                }
        <BLANKLINE>
            >>
        <BLANKLINE>
            \context MusicContext = "Music_Context"
            <<
        <BLANKLINE>
                \context Staff = "Music_Staff"
                {
        <BLANKLINE>
                    \context Voice = "Music_Voice"
                    {
        <BLANKLINE>
                        {   %*% ViolinI
        <BLANKLINE>
                            % [Music_Voice measure 1]
                            e'2
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes(repeat_ties=True)"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
        <BLANKLINE>
                            % [Music_Voice measure 2]
                            f'4.
        <BLANKLINE>
                        }   %*% ViolinI
        <BLANKLINE>
                        {   %*% ViolinII
        <BLANKLINE>
                            % [Music_Voice measure 3]
                            e'2
        <BLANKLINE>
                            % [Music_Voice measure 4]
                            f'4.
                            <> \bacaStopTextSpanRhythmAnnotation
        <BLANKLINE>
                        }   %*% ViolinII
        <BLANKLINE>
                        <<
        <BLANKLINE>
                            \context Voice = "Music_Voice"
                            {
        <BLANKLINE>
                                % [Music_Voice measure 5]
                                \abjad-invisible-music-coloring
                                %@% \abjad-invisible-music
                                \baca-not-yet-pitched-coloring
                                b'1 * 1/4
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                            }
        <BLANKLINE>
                            \context Voice = "Rest_Voice"
                            {
        <BLANKLINE>
                                % [Rest_Voice measure 5]
                                \once \override Score.TimeSignature.X-extent = ##f
                                \once \override MultiMeasureRest.transparent = ##t
                                \stopStaff
                                \once \override Staff.StaffSymbol.transparent = ##t
                                \startStaff
                                R1 * 1/4
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                            }
        <BLANKLINE>
                        >>
        <BLANKLINE>
                    }
        <BLANKLINE>
                }
        <BLANKLINE>
            >>
        <BLANKLINE>
        >>

    """
    if identifier is not None:
        if not isinstance(identifier, str):
            message = f"identifier must be string (not {identifier!r})."
            raise Exception(message)
    return commandclasses.ContainerCommand(identifier=identifier, selector=selector)


def cross_staff(
    *, selector=lambda _: classes.Selection(_).phead(0)
) -> commandclasses.IndicatorCommand:
    r"""
    Attaches cross-staff command.

    ..  container:: example

        Attaches cross-staff command to last two pitched leaves:

        >>> score_template = baca.StringTrioScoreTemplate()
        >>> accumulator = baca.Accumulator(score_template=score_template)
        >>> commands = [
        ...     baca.figure([1], 8, signature=8),
        ...     rmakers.beam(),
        ... ]
        >>> accumulator(
        ...     'Violin_Music_Voice',
        ...     [[9, 11, 12, 14, 16]],
        ...     *commands,
        ...     rmakers.unbeam(),
        ...     baca.stem_up(),
        ...     figure_name='vn.1',
        ... )
        >>> accumulator(
        ...     'Viola_Music_Voice',
        ...     [[0, 2, 4, 5, 7]],
        ...     *commands,
        ...     baca.cross_staff(
        ...         selector=baca.selectors.pleaves((-2, None)),
        ...     ),
        ...     rmakers.unbeam(),
        ...     baca.stem_up(),
        ...     anchor=baca.anchor('Violin_Music_Voice'),
        ...     figure_name='va.1',
        ... )
        >>> accumulator(
        ...     'Violin_Music_Voice',
        ...     [[15]],
        ...     *commands,
        ...     rmakers.unbeam(),
        ...     figure_name='vn.2',
        ... )

        >>> maker = baca.SegmentMaker(
        ...     ignore_repeat_pitch_classes=True,
        ...     score_template=accumulator.score_template,
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=accumulator.time_signatures,
        ...     )
        >>> accumulator.populate_segment_maker(maker)
        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            <BLANKLINE>
            \context Score = "Score"
            <<
            <BLANKLINE>
                \context GlobalContext = "Global_Context"
                <<
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"
                    {
            <BLANKLINE>
                        % [Global_Skips measure 1]
                        \baca-new-spacing-section #1 #12
                        \time 5/8
                        \baca-time-signature-color #'blue
                        s1 * 5/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #12
                        \time 1/8
                        \baca-time-signature-color #'blue
                        s1 * 1/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
                \context MusicContext = "Music_Context"
                <<
            <BLANKLINE>
                    \context StringSectionStaffGroup = "String_Section_Staff_Group"
                    <<
            <BLANKLINE>
                        \tag Violin
                        \context ViolinMusicStaff = "Violin_Music_Staff"
                        {
            <BLANKLINE>
                            \context ViolinMusicVoice = "Violin_Music_Voice"
                            {
            <BLANKLINE>
                                {
            <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                        % [Violin_Music_Voice measure 1]
                                        \override Stem.direction = #up
                                        \clef "treble"
                                        \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet)
                                        %@% \override ViolinMusicStaff.Clef.color = ##f
                                        \set ViolinMusicStaff.forceClef = ##t
                                        a'8
                                        ^ \baca-default-indicator-markup "(Violin)"
                                        - \abjad-dashed-line-with-hook
                                        - \baca-text-spanner-left-text "baca.music()"
                                        - \tweak bound-details.right.padding 2.75
                                        - \tweak color #darkcyan
                                        - \tweak staff-padding 8
                                        \bacaStartTextSpanRhythmAnnotation
                                        \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)
            <BLANKLINE>
                                        b'8
            <BLANKLINE>
                                        c''8
            <BLANKLINE>
                                        d''8
            <BLANKLINE>
                                        e''8
                                        \revert Stem.direction
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                }
            <BLANKLINE>
                                {
            <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                        % [Violin_Music_Voice measure 2]
                                        ef''!8
                                        <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                }
            <BLANKLINE>
                                <<
            <BLANKLINE>
                                    \context Voice = "Violin_Music_Voice"
                                    {
            <BLANKLINE>
                                        % [Violin_Music_Voice measure 3]
                                        \abjad-invisible-music-coloring
                                        %@% \abjad-invisible-music
                                        \baca-not-yet-pitched-coloring
                                        b'1 * 1/4
                                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                    \context Voice = "Violin_Rest_Voice"
                                    {
            <BLANKLINE>
                                        % [Violin_Rest_Voice measure 3]
                                        \once \override Score.TimeSignature.X-extent = ##f
                                        \once \override MultiMeasureRest.transparent = ##t
                                        \stopStaff
                                        \once \override Staff.StaffSymbol.transparent = ##t
                                        \startStaff
                                        R1 * 1/4
                                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                >>
            <BLANKLINE>
                            }
            <BLANKLINE>
                        }
            <BLANKLINE>
                        \tag Viola
                        \context ViolaMusicStaff = "Viola_Music_Staff"
                        {
            <BLANKLINE>
                            \context ViolaMusicVoice = "Viola_Music_Voice"
                            {
            <BLANKLINE>
                                {
            <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                        % [Viola_Music_Voice measure 1]
                                        \override Stem.direction = #up
                                        \clef "alto"
                                        \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet)
                                        %@% \override ViolaMusicStaff.Clef.color = ##f
                                        \set ViolaMusicStaff.forceClef = ##t
                                        c'8
                                        ^ \baca-default-indicator-markup "(Viola)"
                                        - \abjad-dashed-line-with-hook
                                        - \baca-text-spanner-left-text "baca.music()"
                                        - \tweak bound-details.right.padding 2.75
                                        - \tweak color #darkcyan
                                        - \tweak staff-padding 8
                                        \bacaStartTextSpanRhythmAnnotation
                                        \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)
            <BLANKLINE>
                                        d'8
            <BLANKLINE>
                                        e'8
            <BLANKLINE>
                                        \crossStaff
                                        f'8
            <BLANKLINE>
                                        \crossStaff
                                        g'8
                                        \revert Stem.direction
                                        <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                }
            <BLANKLINE>
                                <<
            <BLANKLINE>
                                    \context Voice = "Viola_Music_Voice"
                                    {
            <BLANKLINE>
                                        % [Viola_Music_Voice measure 2]
                                        \abjad-invisible-music-coloring
                                        %@% \abjad-invisible-music
                                        \baca-not-yet-pitched-coloring
                                        c'1 * 1/8
                                        %@% ^ \baca-duration-multiplier-markup #"1" #"8"
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                    \context Voice = "Viola_Rest_Voice"
                                    {
            <BLANKLINE>
                                        % [Viola_Rest_Voice measure 2]
                                        R1 * 1/8
                                        %@% ^ \baca-duration-multiplier-markup #"1" #"8"
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                >>
            <BLANKLINE>
                                <<
            <BLANKLINE>
                                    \context Voice = "Viola_Music_Voice"
                                    {
            <BLANKLINE>
                                        % [Viola_Music_Voice measure 3]
                                        \abjad-invisible-music-coloring
                                        %@% \abjad-invisible-music
                                        R1 * 1/4
                                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                    \context Voice = "Viola_Rest_Voice"
                                    {
            <BLANKLINE>
                                        % [Viola_Rest_Voice measure 3]
                                        \once \override Score.TimeSignature.X-extent = ##f
                                        \once \override MultiMeasureRest.transparent = ##t
                                        \stopStaff
                                        \once \override Staff.StaffSymbol.transparent = ##t
                                        \startStaff
                                        R1 * 1/4
                                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                >>
            <BLANKLINE>
                            }
            <BLANKLINE>
                        }
            <BLANKLINE>
                        \tag Cello
                        \context CelloMusicStaff = "Cello_Music_Staff"
                        {
            <BLANKLINE>
                            \context CelloMusicVoice = "Cello_Music_Voice"
                            {
            <BLANKLINE>
                                % [Cello_Music_Voice measure 1]
                                \clef "bass"
                                \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet)
                                %@% \override CelloMusicStaff.Clef.color = ##f
                                \set CelloMusicStaff.forceClef = ##t
                                R1 * 5/8
                                ^ \baca-default-indicator-markup "(Cello)"
                                %@% ^ \baca-duration-multiplier-markup #"5" #"8"
                                \override CelloMusicStaff.Clef.color = #(x11-color 'violet)
            <BLANKLINE>
                                % [Cello_Music_Voice measure 2]
                                R1 * 1/8
                                %@% ^ \baca-duration-multiplier-markup #"1" #"8"
            <BLANKLINE>
                                <<
            <BLANKLINE>
                                    \context Voice = "Cello_Music_Voice"
                                    {
            <BLANKLINE>
                                        % [Cello_Music_Voice measure 3]
                                        \abjad-invisible-music-coloring
                                        %@% \abjad-invisible-music
                                        R1 * 1/4
                                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                    \context Voice = "Cello_Rest_Voice"
                                    {
            <BLANKLINE>
                                        % [Cello_Rest_Voice measure 3]
                                        \once \override Score.TimeSignature.X-extent = ##f
                                        \once \override MultiMeasureRest.transparent = ##t
                                        \stopStaff
                                        \once \override Staff.StaffSymbol.transparent = ##t
                                        \startStaff
                                        R1 * 1/4
                                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                >>
            <BLANKLINE>
                            }
            <BLANKLINE>
                        }
            <BLANKLINE>
                    >>
            <BLANKLINE>
                >>
            <BLANKLINE>
            >>

    """
    return commandclasses.IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\crossStaff")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def double_volta(
    selector=lambda _: classes.Selection(_).leaf(0),
) -> scoping.Suite:
    """
    Attaches bar line and overrides bar line X-extent.
    """
    return scoping.suite(
        indicatorcommands.bar_line(":.|.:", selector, format_slot="before"),
        scoping.not_mol(overrides.bar_line_x_extent((0, 3), selector)),
        scoping.only_mol(overrides.bar_line_x_extent((0, 4), selector)),
    )


def dynamic_down(
    *, selector=lambda _: classes.Selection(_).leaf(0)
) -> commandclasses.IndicatorCommand:
    r"""
    Attaches dynamic-down command.

    ..  container:: example

        Attaches dynamic-down command to leaf 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.dynamic('p'),
        ...     baca.dynamic('f', selector=lambda _: baca.Selection(_).tuplets()[1:2].phead(0)),
        ...     baca.dynamic_down(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.illustrators.attach_markup_struts(lilypond_file)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = 2
                        \dynamicDown
                        r8
                        - \tweak staff-padding 11
                        - \tweak transparent ##t
                        ^ \markup I
                        c'16
                        \p
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
                        \f
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
            >>

    """
    return commandclasses.IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\dynamicDown")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def dynamic_up(
    *, selector=lambda _: classes.Selection(_).leaf(0)
) -> commandclasses.IndicatorCommand:
    r"""
    Attaches dynamic-up command.

    ..  container:: example

        Attaches dynamic-up command to leaf 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.dynamic('p'),
        ...     baca.dynamic('f', selector=lambda _: baca.Selection(_).tuplets()[1:2].phead(0)),
        ...     baca.dynamic_up(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.illustrators.attach_markup_struts(lilypond_file)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = 2
                        \dynamicUp
                        r8
                        - \tweak staff-padding 11
                        - \tweak transparent ##t
                        ^ \markup I
                        c'16
                        \p
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
                        \f
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
            >>

    """
    return commandclasses.IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\dynamicUp")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def edition(
    not_parts: typing.Union[str, abjad.Markup, commandclasses.IndicatorCommand],
    only_parts: typing.Union[str, abjad.Markup, commandclasses.IndicatorCommand],
) -> scoping.Suite:
    """
    Makes not-parts / only-parts markup suite.
    """
    if isinstance(not_parts, (str, abjad.Markup)):
        not_parts = markup(not_parts)
    assert isinstance(not_parts, commandclasses.IndicatorCommand)
    not_parts_ = scoping.not_parts(not_parts)
    if isinstance(only_parts, (str, abjad.Markup)):
        only_parts = markup(only_parts)
    assert isinstance(only_parts, commandclasses.IndicatorCommand)
    only_parts_ = scoping.only_parts(only_parts)
    return scoping.suite(not_parts_, only_parts_)


def finger_pressure_transition(
    *,
    selector=lambda _: classes.Selection(_).tleaves(),
    right_broken: bool = None,
) -> commandclasses.GlissandoCommand:
    r"""
    Makes finger pressure transition glissando.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.finger_pressure_transition(selector=baca.selectors.notes((None, 2))),
        ...     baca.finger_pressure_transition(selector=baca.selectors.notes((2, None))),
        ...     baca.make_notes(),
        ...     baca.note_head_style_harmonic(selector=baca.selectors.note(0)),
        ...     baca.note_head_style_harmonic(selector=baca.selectors.note(2)),
        ...     baca.pitch('C5'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            <BLANKLINE>
            \context Score = "Score"
            <<
            <BLANKLINE>
                \context GlobalContext = "Global_Context"
                <<
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"
                    {
            <BLANKLINE>
                        % [Global_Skips measure 1]
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 5]
                        \baca-new-spacing-section #1 #4
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
                \context MusicContext = "Music_Context"
                <<
            <BLANKLINE>
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \once \override NoteHead.style = #'harmonic
                            c''2
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            - \tweak arrow-length 2
                            - \tweak arrow-width 0.5
                            - \tweak bound-details.right.arrow ##t
                            - \tweak thickness 3
                            \glissando
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            c''4.
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            \once \override NoteHead.style = #'harmonic
                            c''2
                            - \tweak arrow-length 2
                            - \tweak arrow-width 0.5
                            - \tweak bound-details.right.arrow ##t
                            - \tweak thickness 3
                            \glissando
            <BLANKLINE>
                            % [Music_Voice measure 4]
                            c''4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 5]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    \baca-not-yet-pitched-coloring
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 5]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                            >>
            <BLANKLINE>
                        }
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
            >>

    """
    return commandclasses.GlissandoCommand(
        allow_repeats=True,
        right_broken=right_broken,
        selector=selector,
        tags=[_site(inspect.currentframe())],
        tweaks=(
            abjad.tweak(2).arrow_length,
            abjad.tweak(0.5).arrow_width,
            abjad.tweak(True).bound_details__right__arrow,
            abjad.tweak(3).thickness,
        ),
    )


def flat_glissando(
    pitch: typing.Union[
        str,
        abjad.NamedPitch,
        abjad.StaffPosition,
        typing.List[abjad.StaffPosition],
    ] = None,
    *tweaks,
    allow_repitch: bool = None,
    do_not_hide_middle_note_heads: bool = None,
    mock: bool = None,
    hide_middle_stems: bool = None,
    hide_stem_selector: abjad.Expression = None,
    left_broken: bool = None,
    right_broken: bool = None,
    right_broken_show_next: bool = None,
    rleak: bool = None,
    selector=lambda _: classes.Selection(_).pleaves(),
    stop_pitch: typing.Union[str, abjad.NamedPitch, abjad.StaffPosition] = None,
) -> scoping.Suite:
    """
    Makes flat glissando.
    """
    prototype = (list, str, abjad.NamedPitch, abjad.StaffPosition)
    if pitch is not None:
        assert isinstance(pitch, prototype), repr(pitch)
    if stop_pitch is not None:
        assert type(pitch) is type(stop_pitch), repr((pitch, stop_pitch))
    if rleak is True:

        def _selector_rleak(argument):
            return selector(argument).rleak()

        new_selector = _selector_rleak
    else:
        new_selector = selector
    commands: typing.List[scoping.Command] = []
    command = glissando(
        *tweaks,
        allow_repeats=True,
        allow_ties=True,
        hide_middle_note_heads=not do_not_hide_middle_note_heads,
        hide_middle_stems=hide_middle_stems,
        hide_stem_selector=hide_stem_selector,
        left_broken=left_broken,
        right_broken=right_broken,
        right_broken_show_next=right_broken_show_next,
        selector=new_selector,
    )
    commands.append(command)

    def _leaves_of_selector(argument):
        return new_selector(argument).leaves()

    untie_command = untie(_leaves_of_selector)
    commands.append(untie_command)
    if pitch is not None and stop_pitch is None:
        if isinstance(pitch, abjad.StaffPosition) or (
            isinstance(pitch, list) and isinstance(pitch[0], abjad.StaffPosition)
        ):
            staff_position_command = pitchcommands.staff_position(
                pitch,
                allow_repitch=allow_repitch,
                mock=mock,
                selector=new_selector,
            )
            commands.append(staff_position_command)
        else:
            pitch_command = pitchcommands.pitch(
                pitch,
                allow_repitch=allow_repitch,
                mock=mock,
                selector=new_selector,
            )
            commands.append(pitch_command)
    elif pitch is not None and stop_pitch is not None:
        if isinstance(pitch, abjad.StaffPosition):
            assert isinstance(stop_pitch, abjad.StaffPosition)
            interpolation_command = pitchcommands.interpolate_staff_positions(
                pitch, stop_pitch, mock=mock, selector=new_selector
            )
        else:
            assert isinstance(pitch, (str, abjad.NamedPitch))
            assert isinstance(stop_pitch, (str, abjad.NamedPitch))
            interpolation_command = pitchcommands.interpolate_pitches(
                pitch, stop_pitch, mock=mock, selector=new_selector
            )
        commands.append(interpolation_command)
    return scoping.suite(*commands)


def fractions(items):
    """
    Makes fractions.
    """
    result = []
    for item in items:
        item_ = abjad.NonreducedFraction(item)
        result.append(item_)
    return result


def glissando(
    *tweaks: abjad.IndexedTweakManager,
    allow_repeats: bool = None,
    allow_ties: bool = None,
    hide_middle_note_heads: bool = None,
    hide_middle_stems: bool = None,
    hide_stem_selector: abjad.Expression = None,
    left_broken: bool = None,
    map: abjad.Expression = None,
    right_broken: bool = None,
    right_broken_show_next: bool = None,
    selector=lambda _: classes.Selection(_).tleaves(),
    style: str = None,
    zero_padding: bool = None,
) -> commandclasses.GlissandoCommand:
    r"""
    Attaches glissando.

    ..  container:: example

        With segment-maker:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.glissando()
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            <BLANKLINE>
            \context Score = "Score"
            <<
            <BLANKLINE>
                \context GlobalContext = "Global_Context"
                <<
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"
                    {
            <BLANKLINE>
                        % [Global_Skips measure 1]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 5]
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
                \context MusicContext = "Music_Context"
                <<
            <BLANKLINE>
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            e'8
                            [
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_even_divisions()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \glissando
            <BLANKLINE>
                            d''8
                            \glissando
            <BLANKLINE>
                            f'8
                            \glissando
            <BLANKLINE>
                            e''8
                            ]
                            \glissando
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            g'8
                            [
                            \glissando
            <BLANKLINE>
                            f''8
                            \glissando
            <BLANKLINE>
                            e'8
                            ]
                            \glissando
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            d''8
                            [
                            \glissando
            <BLANKLINE>
                            f'8
                            \glissando
            <BLANKLINE>
                            e''8
                            \glissando
            <BLANKLINE>
                            g'8
                            ]
                            \glissando
            <BLANKLINE>
                            % [Music_Voice measure 4]
                            f''8
                            [
                            \glissando
            <BLANKLINE>
                            e'8
                            \glissando
            <BLANKLINE>
                            d''8
                            ]
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 5]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    \baca-not-yet-pitched-coloring
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 5]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                            >>
            <BLANKLINE>
                        }
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
            >>

    ..  container:: example

        First and last PLTs:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.make_even_divisions(),
        ...     baca.glissando(selector=baca.plts()[:2]),
        ...     baca.glissando(selector=baca.plts()[-2:]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            <BLANKLINE>
            \context Score = "Score"
            <<
            <BLANKLINE>
                \context GlobalContext = "Global_Context"
                <<
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"
                    {
            <BLANKLINE>
                        % [Global_Skips measure 1]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 5]
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
                \context MusicContext = "Music_Context"
                <<
            <BLANKLINE>
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            e'8
                            [
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_even_divisions()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \glissando
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [Music_Voice measure 4]
                            f''8
                            [
            <BLANKLINE>
                            e'8
                            \glissando
            <BLANKLINE>
                            d''8
                            ]
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 5]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    \baca-not-yet-pitched-coloring
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 5]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                            >>
            <BLANKLINE>
                        }
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
            >>

    ..  container:: example

        Works with tweaks:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.glissando(
        ...         abjad.tweak("#red").color,
        ...         ),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            <BLANKLINE>
            \context Score = "Score"
            <<
            <BLANKLINE>
                \context GlobalContext = "Global_Context"
                <<
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"
                    {
            <BLANKLINE>
                        % [Global_Skips measure 1]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 5]
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
                \context MusicContext = "Music_Context"
                <<
            <BLANKLINE>
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            e'8
                            [
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_even_divisions()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            - \tweak color #red
                            \glissando
            <BLANKLINE>
                            d''8
                            - \tweak color #red
                            \glissando
            <BLANKLINE>
                            f'8
                            - \tweak color #red
                            \glissando
            <BLANKLINE>
                            e''8
                            ]
                            - \tweak color #red
                            \glissando
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            g'8
                            [
                            - \tweak color #red
                            \glissando
            <BLANKLINE>
                            f''8
                            - \tweak color #red
                            \glissando
            <BLANKLINE>
                            e'8
                            ]
                            - \tweak color #red
                            \glissando
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            d''8
                            [
                            - \tweak color #red
                            \glissando
            <BLANKLINE>
                            f'8
                            - \tweak color #red
                            \glissando
            <BLANKLINE>
                            e''8
                            - \tweak color #red
                            \glissando
            <BLANKLINE>
                            g'8
                            ]
                            - \tweak color #red
                            \glissando
            <BLANKLINE>
                            % [Music_Voice measure 4]
                            f''8
                            [
                            - \tweak color #red
                            \glissando
            <BLANKLINE>
                            e'8
                            - \tweak color #red
                            \glissando
            <BLANKLINE>
                            d''8
                            ]
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 5]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    \baca-not-yet-pitched-coloring
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 5]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                            >>
            <BLANKLINE>
                        }
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
            >>

    ..  container:: example

        Works with indexed tweaks:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.glissando(
        ...         (abjad.tweak("#red").color, 0),
        ...         (abjad.tweak("#red").color, -1),
        ...         ),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            <BLANKLINE>
            \context Score = "Score"
            <<
            <BLANKLINE>
                \context GlobalContext = "Global_Context"
                <<
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"
                    {
            <BLANKLINE>
                        % [Global_Skips measure 1]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 5]
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
                \context MusicContext = "Music_Context"
                <<
            <BLANKLINE>
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            e'8
                            [
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_even_divisions()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            - \tweak color #red
                            \glissando
            <BLANKLINE>
                            d''8
                            \glissando
            <BLANKLINE>
                            f'8
                            \glissando
            <BLANKLINE>
                            e''8
                            ]
                            \glissando
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            g'8
                            [
                            \glissando
            <BLANKLINE>
                            f''8
                            \glissando
            <BLANKLINE>
                            e'8
                            ]
                            \glissando
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            d''8
                            [
                            \glissando
            <BLANKLINE>
                            f'8
                            \glissando
            <BLANKLINE>
                            e''8
                            \glissando
            <BLANKLINE>
                            g'8
                            ]
                            \glissando
            <BLANKLINE>
                            % [Music_Voice measure 4]
                            f''8
                            [
                            \glissando
            <BLANKLINE>
                            e'8
                            - \tweak color #red
                            \glissando
            <BLANKLINE>
                            d''8
                            ]
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 5]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    \baca-not-yet-pitched-coloring
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 5]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                            >>
            <BLANKLINE>
                        }
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
            >>

    """
    return commandclasses.GlissandoCommand(
        allow_repeats=allow_repeats,
        allow_ties=allow_ties,
        hide_middle_note_heads=hide_middle_note_heads,
        hide_middle_stems=hide_middle_stems,
        hide_stem_selector=hide_stem_selector,
        left_broken=left_broken,
        map=map,
        right_broken=right_broken,
        right_broken_show_next=right_broken_show_next,
        selector=selector,
        tags=[_site(inspect.currentframe())],
        tweaks=tweaks,
        zero_padding=zero_padding,
    )


def global_fermata(
    description: str = "fermata",
    selector=lambda _: classes.Selection(_).leaf(0),
) -> commandclasses.GlobalFermataCommand:
    """
    Attaches global fermata.
    """
    fermatas = commandclasses.GlobalFermataCommand.description_to_command.keys()
    if description not in fermatas:
        message = f"must be in {repr(', '.join(fermatas))}:\n"
        message += f"   {repr(description)}"
        raise Exception(message)
    return commandclasses.GlobalFermataCommand(
        description=description,
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def instrument(
    instrument: abjad.Instrument,
    selector=lambda _: classes.Selection(_).leaf(0),
) -> commandclasses.InstrumentChangeCommand:
    """
    Makes instrument change command.
    """
    if not isinstance(instrument, abjad.Instrument):
        message = f"instrument must be instrument (not {instrument!r})."
        raise Exception(message)
    return commandclasses.InstrumentChangeCommand(
        indicators=[instrument],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def invisible_music(
    selector=lambda _: classes.Selection(_).leaf(0),
    *,
    map: abjad.Expression = None,
) -> scoping.Suite:
    r"""
    Attaches ``\baca-invisible-music`` literal.

    ..  container:: example

        Attaches ``\baca-invisible-music`` literal to middle leaves:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.invisible_music(
        ...         selector=baca.leaves()[1:-1],
        ...         ),
        ...     baca.make_notes(),
        ...     baca.pitch('C5'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            <BLANKLINE>
            \context Score = "Score"
            <<
            <BLANKLINE>
                \context GlobalContext = "Global_Context"
                <<
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"
                    {
            <BLANKLINE>
                        % [Global_Skips measure 1]
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 5]
                        \baca-new-spacing-section #1 #4
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
                \context MusicContext = "Music_Context"
                <<
            <BLANKLINE>
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            c''2
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \abjad-invisible-music
                            \abjad-invisible-music-coloring
                            c''4.
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            %@% \abjad-invisible-music
                            \abjad-invisible-music-coloring
                            c''2
            <BLANKLINE>
                            % [Music_Voice measure 4]
                            c''4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 5]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    \baca-not-yet-pitched-coloring
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 5]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                            >>
            <BLANKLINE>
                        }
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
            >>

    """
    tag = _site(inspect.currentframe(), 1)
    tag = tag.append(ide.tags.INVISIBLE_MUSIC_COMMAND)
    command_1 = commandclasses.IndicatorCommand(
        [abjad.LilyPondLiteral(r"\abjad-invisible-music")],
        deactivate=True,
        map=map,
        selector=selector,
        tags=[tag],
    )
    tag = _site(inspect.currentframe(), 2)
    tag = tag.append(ide.tags.INVISIBLE_MUSIC_COLORING)
    command_2 = commandclasses.IndicatorCommand(
        [abjad.LilyPondLiteral(r"\abjad-invisible-music-coloring")],
        map=map,
        selector=selector,
        tags=[tag],
    )
    return scoping.suite(command_1, command_2)


def label(
    expression: abjad.Expression,
    selector=lambda _: classes.Selection(_).leaves(),
) -> commandclasses.LabelCommand:
    r"""
    Labels ``selector`` output with label ``expression``.

    ..  container:: example

        Labels pitch names:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.label(lambda _: abjad.Label(_).with_pitches(locale="us")),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.illustrators.attach_markup_struts(lilypond_file)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = 2
                        r8
                        - \tweak staff-padding 11
                        - \tweak transparent ##t
                        ^ \markup I
                        c'16
                        ^ \markup { C4 }
                        [
                        d'16
                        ^ \markup { D4 }
                        ]
                        bf'4
                        ^ \markup { Bb4 }
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs''16
                        ^ \markup { "F#5" }
                        [
                        e''16
                        ^ \markup { E5 }
                        ]
                        ef''4
                        ^ \markup { Eb5 }
                        ~
                        ef''16
                        r16
                        af''16
                        ^ \markup { Ab5 }
                        [
                        g''16
                        ^ \markup { G5 }
                        ]
                    }
                    \times 4/5 {
                        a'16
                        ^ \markup { A4 }
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return commandclasses.LabelCommand(expression=expression, selector=selector)


def markup(
    argument: typing.Union[str, abjad.Markup],
    *tweaks: abjad.TweakInterface,
    # typehinting is weird for some reason
    direction=abjad.Up,
    literal: bool = False,
    map: abjad.Expression = None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    selector=lambda _: classes.Selection(_).pleaf(0),
) -> commandclasses.IndicatorCommand:
    r"""
    Makes markup and inserts into indicator command.

    ..  container:: example

        Attaches markup to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.markup('più mosso'),
        ...     baca.tuplet_bracket_outside_staff_priority(1000),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.illustrators.attach_markup_struts(lilypond_file)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.outside-staff-priority = 1000
                        \override TupletBracket.staff-padding = 2
                        r8
                        - \tweak staff-padding 11
                        - \tweak transparent ##t
                        ^ \markup I
                        c'16
                        ^ \markup { più mosso }
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
                        \revert TupletBracket.outside-staff-priority
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Set ``literal=True`` to pass predefined markup commands:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.markup(
        ...         r'\markup { \baca-triple-diamond-markup }',
        ...         literal=True,
        ...         ),
        ...     baca.tuplet_bracket_outside_staff_priority(1000),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.illustrators.attach_markup_struts(lilypond_file)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.outside-staff-priority = 1000
                        \override TupletBracket.staff-padding = 2
                        r8
                        - \tweak staff-padding 11
                        - \tweak transparent ##t
                        ^ \markup I
                        c'16
                        ^ \markup { \baca-triple-diamond-markup }
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
                        \revert TupletBracket.outside-staff-priority
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example exception

        Raises exception on nonstring, nonmarkup ``argument``:

        >>> baca.markup(['Allegro', 'ma non troppo'])
        Traceback (most recent call last):
            ...
        Exception: MarkupLibary.__call__():
            Value of 'argument' must be str or markup.
            Not ['Allegro', 'ma non troppo'].

    """
    if direction not in (abjad.Down, abjad.Up):
        message = f"direction must be up or down (not {direction!r})."
        raise Exception(message)
    if isinstance(argument, str):
        if literal:
            markup = abjad.Markup(argument, direction=direction, literal=True)
        else:
            markup = abjad.Markup(argument, direction=direction)
    elif isinstance(argument, abjad.Markup):
        markup = abjad.new(argument, direction=direction)
    else:
        message = "MarkupLibary.__call__():\n"
        message += "  Value of 'argument' must be str or markup.\n"
        message += f"  Not {argument!r}."
        raise Exception(message)
    if (
        selector is not None
        and not isinstance(selector, str)
        and not callable(selector)
    ):
        message = "selector must be string or callable"
        message += f" (not {selector!r})."
        raise Exception(message)

    def select_phead_0(argument):
        return classes.Selection(argument).phead(0)

    selector = selector or select_phead_0
    return commandclasses.IndicatorCommand(
        indicators=[markup],
        map=map,
        match=match,
        measures=measures,
        selector=selector,
        tags=[_site(inspect.currentframe())],
        tweaks=tweaks,
    )


def metronome_mark(
    key: typing.Union[str, indicators.Accelerando, indicators.Ritardando],
    selector=lambda _: classes.Selection(_).leaf(0),
    *,
    redundant: bool = None,
) -> typing.Optional[commandclasses.MetronomeMarkCommand]:
    """
    Attaches metronome mark matching ``key`` metronome mark manifest.
    """
    if redundant is True:
        return None
    return commandclasses.MetronomeMarkCommand(
        key=key, redundant=redundant, selector=selector
    )


def parts(
    part_assignment: ide.PartAssignment,
    *,
    selector=lambda _: classes.Selection(_).leaves(),
) -> commandclasses.PartAssignmentCommand:
    r"""
    Inserts ``selector`` output in container and sets part assignment.

    ..  container:: example

        >>> import ide
        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.StringTrioScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Violin_Music_Voice',
        ...     baca.make_notes(),
        ...     baca.parts(ide.PartAssignment('Violin')),
        ...     baca.pitch('E4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> string = abjad.lilypond(lilypond_file[abjad.Score])
        >>> print(string)
        <BLANKLINE>
        \context Score = "Score"
        <<
        <BLANKLINE>
            \context GlobalContext = "Global_Context"
            <<
        <BLANKLINE>
                \context GlobalSkips = "Global_Skips"
                {
        <BLANKLINE>
                    % [Global_Skips measure 1]
                    \time 4/8
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 2]
                    \time 3/8
                    \baca-time-signature-color #'blue
                    s1 * 3/8
        <BLANKLINE>
                    % [Global_Skips measure 3]
                    \time 4/8
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 4]
                    \time 3/8
                    \baca-time-signature-color #'blue
                    s1 * 3/8
        <BLANKLINE>
                    % [Global_Skips measure 5]
                    \time 1/4
                    \baca-time-signature-transparent
                    s1 * 1/4
                    \once \override Score.BarLine.transparent = ##t
                    \once \override Score.SpanBar.transparent = ##t
        <BLANKLINE>
                }
        <BLANKLINE>
            >>
        <BLANKLINE>
            \context MusicContext = "Music_Context"
            <<
        <BLANKLINE>
                \context StringSectionStaffGroup = "String_Section_Staff_Group"
                <<
        <BLANKLINE>
                    \tag Violin
                    \context ViolinMusicStaff = "Violin_Music_Staff"
                    {
        <BLANKLINE>
                        \context ViolinMusicVoice = "Violin_Music_Voice"
                        {
        <BLANKLINE>
                            {   %*% PartAssignment('Violin')
        <BLANKLINE>
                                % [Violin_Music_Voice measure 1]
                                \clef "treble"
                                \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet)
                                %@% \override ViolinMusicStaff.Clef.color = ##f
                                \set ViolinMusicStaff.forceClef = ##t
                                e'2
                                ^ \baca-default-indicator-markup "(Violin)"
                                - \abjad-dashed-line-with-hook
                                - \baca-text-spanner-left-text "make_notes()"
                                - \tweak bound-details.right.padding 2.75
                                - \tweak color #darkcyan
                                - \tweak staff-padding 8
                                \bacaStartTextSpanRhythmAnnotation
                                \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)
        <BLANKLINE>
                                % [Violin_Music_Voice measure 2]
                                e'4.
        <BLANKLINE>
                                % [Violin_Music_Voice measure 3]
                                e'2
        <BLANKLINE>
                                % [Violin_Music_Voice measure 4]
                                e'4.
                                <> \bacaStopTextSpanRhythmAnnotation
        <BLANKLINE>
                            }   %*% PartAssignment('Violin')
        <BLANKLINE>
                            <<
        <BLANKLINE>
                                \context Voice = "Violin_Music_Voice"
                                {
        <BLANKLINE>
                                    % [Violin_Music_Voice measure 5]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    \baca-not-yet-pitched-coloring
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                                }
        <BLANKLINE>
                                \context Voice = "Violin_Rest_Voice"
                                {
        <BLANKLINE>
                                    % [Violin_Rest_Voice measure 5]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                                }
        <BLANKLINE>
                            >>
        <BLANKLINE>
                        }
        <BLANKLINE>
                    }
        <BLANKLINE>
                    \tag Viola
                    \context ViolaMusicStaff = "Viola_Music_Staff"
                    {
        <BLANKLINE>
                        \context ViolaMusicVoice = "Viola_Music_Voice"
                        {
        <BLANKLINE>
                            % [Viola_Music_Voice measure 1]
                            \clef "alto"
                            \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet)
                            %@% \override ViolaMusicStaff.Clef.color = ##f
                            \set ViolaMusicStaff.forceClef = ##t
                            R1 * 4/8
                            ^ \baca-default-indicator-markup "(Viola)"
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                            \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)
        <BLANKLINE>
                            % [Viola_Music_Voice measure 2]
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
        <BLANKLINE>
                            % [Viola_Music_Voice measure 3]
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
        <BLANKLINE>
                            % [Viola_Music_Voice measure 4]
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
        <BLANKLINE>
                            <<
        <BLANKLINE>
                                \context Voice = "Viola_Music_Voice"
                                {
        <BLANKLINE>
                                    % [Viola_Music_Voice measure 5]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                                }
        <BLANKLINE>
                                \context Voice = "Viola_Rest_Voice"
                                {
        <BLANKLINE>
                                    % [Viola_Rest_Voice measure 5]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                                }
        <BLANKLINE>
                            >>
        <BLANKLINE>
                        }
        <BLANKLINE>
                    }
        <BLANKLINE>
                    \tag Cello
                    \context CelloMusicStaff = "Cello_Music_Staff"
                    {
        <BLANKLINE>
                        \context CelloMusicVoice = "Cello_Music_Voice"
                        {
        <BLANKLINE>
                            % [Cello_Music_Voice measure 1]
                            \clef "bass"
                            \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet)
                            %@% \override CelloMusicStaff.Clef.color = ##f
                            \set CelloMusicStaff.forceClef = ##t
                            R1 * 4/8
                            ^ \baca-default-indicator-markup "(Cello)"
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                            \override CelloMusicStaff.Clef.color = #(x11-color 'violet)
        <BLANKLINE>
                            % [Cello_Music_Voice measure 2]
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
        <BLANKLINE>
                            % [Cello_Music_Voice measure 3]
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
        <BLANKLINE>
                            % [Cello_Music_Voice measure 4]
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
        <BLANKLINE>
                            <<
        <BLANKLINE>
                                \context Voice = "Cello_Music_Voice"
                                {
        <BLANKLINE>
                                    % [Cello_Music_Voice measure 5]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                                }
        <BLANKLINE>
                                \context Voice = "Cello_Rest_Voice"
                                {
        <BLANKLINE>
                                    % [Cello_Rest_Voice measure 5]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                                }
        <BLANKLINE>
                            >>
        <BLANKLINE>
                        }
        <BLANKLINE>
                    }
        <BLANKLINE>
                >>
        <BLANKLINE>
            >>
        <BLANKLINE>
        >>

    ..  container:: example exception

        Raises exception when voice does not allow part assignment:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.StringTrioScoreTemplate(),
        ...     test_container_identifiers=True,
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> part_assignment = ide.PartAssignment('Flute')

        >>> maker(
        ...     'Violin_Music_Voice',
        ...     baca.make_notes(),
        ...     baca.parts(part_assignment),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        Traceback (most recent call last):
            ...
        Exception: Violin_Music_Voice does not allow Flute part assignment:
            PartAssignment('Flute')

    """
    if not isinstance(part_assignment, ide.PartAssignment):
        message = "part_assignment must be part assignment"
        message += f" (not {part_assignment!r})."
        raise Exception(message)
    return commandclasses.PartAssignmentCommand(
        part_assignment=part_assignment, selector=selector
    )


def one_voice(
    selector=lambda _: classes.Selection(_).leaf(0),
) -> commandclasses.IndicatorCommand:
    r"""
    Makes LilyPond ``\oneVoice`` command.
    """
    literal = abjad.LilyPondLiteral(r"\oneVoice")
    return commandclasses.IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def open_volta(
    selector=lambda _: classes.Selection(_).leaf(0),
) -> scoping.Suite:
    """
    Attaches bar line and overrides bar line X-extent.
    """
    return scoping.suite(
        indicatorcommands.bar_line(".|:", selector, format_slot="before"),
        scoping.not_mol(overrides.bar_line_x_extent((0, 2), selector)),
        scoping.only_mol(overrides.bar_line_x_extent((0, 3), selector)),
    )


def previous_metadata(path: str) -> abjad.OrderedDict:
    """
    Gets previous segment metadata before ``path``.
    """
    # reproduces ide.Path.get_previous_path()
    # because Travis isn't configured for scores-directory calculations
    definition_py = ide.Path(path)
    segment = ide.Path(definition_py).parent
    assert segment.is_segment(), repr(segment)
    segments = segment.parent
    assert segments.is_segments(), repr(segments)
    paths = segments.list_paths()
    paths = [_ for _ in paths if not _.name.startswith(".")]
    assert all(_.is_dir() for _ in paths), repr(paths)
    index = paths.index(segment)
    if index == 0:
        return abjad.OrderedDict()
    previous_index = index - 1
    previous_segment = paths[previous_index]
    previous_metadata = previous_segment.get_metadata()
    return previous_metadata


def untie(selector: abjad.Expression) -> commandclasses.DetachCommand:
    """
    Makes (repeat-)tie detach command.
    """
    return commandclasses.DetachCommand([abjad.Tie, abjad.RepeatTie], selector=selector)


def voice_four(
    selector=lambda _: classes.Selection(_).leaf(0),
) -> commandclasses.IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceFour`` command.
    """
    literal = abjad.LilyPondLiteral(r"\voiceFour")
    return commandclasses.IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def voice_one(
    selector=lambda _: classes.Selection(_).leaf(0),
) -> commandclasses.IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceOne`` command.
    """
    literal = abjad.LilyPondLiteral(r"\voiceOne")
    return commandclasses.IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def voice_three(
    selector=lambda _: classes.Selection(_).leaf(0),
) -> commandclasses.IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceThree`` command.
    """
    literal = abjad.LilyPondLiteral(r"\voiceThree")
    return commandclasses.IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def voice_two(
    selector=lambda _: classes.Selection(_).leaf(0),
) -> commandclasses.IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceTwo`` command.
    """
    literal = abjad.LilyPondLiteral(r"\voiceTwo")
    return commandclasses.IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )
