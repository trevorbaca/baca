"""
Rhythm library.
"""
import abjad
import collections
import inspect
import math
import typing
from abjadext import rmakers
from . import classes
from . import divisionclasses
from . import const
from . import overrides
from . import scoping
from . import typings


RhythmMakerTyping = typing.Union[
    rmakers.RhythmCommand,
    rmakers.RhythmMaker,
    rmakers.MakerAssignment,
    rmakers.MakerAssignments,
]

### CLASSES ###


class DurationMultiplierCommand(scoping.Command):
    """
    Duration multiplier command.

    ..  container:: example

        >>> baca.DurationMultiplierCommand()
        DurationMultiplierCommand(selector=baca.leaf(0))

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_written_duration",)

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        map: abjad.SelectorTyping = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        scope: scoping.ScopeTyping = None,
        selector: abjad.SelectorTyping = "baca.leaf(0)",
        written_duration: abjad.DurationTyping = None,
    ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
        )
        written_duration_ = None
        if written_duration is not None:
            written_duration_ = abjad.Duration(written_duration)
        self._written_duration = written_duration_

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Applies ``DurationMultiplierCommand`` to result of selector called on
        ``argument``.
        """
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        leaves = classes.Selection(argument).leaves()
        assert isinstance(leaves, classes.Selection)
        for leaf in leaves:
            self._set_multiplied_duration(leaf, self.written_duration)

    ### PRIVATE METHODS ###

    @staticmethod
    def _set_multiplied_duration(leaf, written_duration):
        if written_duration is None:
            return
        old_duration = abjad.inspect(leaf).duration()
        if written_duration == old_duration:
            return
        leaf.written_duration = written_duration
        multiplier = old_duration / written_duration
        leaf.multiplier = multiplier

    ### PUBLIC PROPERTIES ###

    @property
    def written_duration(self) -> typing.Optional[abjad.Duration]:
        """
        Gets written duration.
        """
        return self._written_duration


class RhythmCommand(scoping.Command):
    r"""
    Rhythm command.

    >>> from abjadext import rmakers

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(3, 8), (4, 8), (3,8), (4, 8)],
        ...     )

        >>> command = baca.RhythmCommand(
        ...     rhythm_maker=rmakers.even_division(
        ...         rmakers.beam(),
        ...         rmakers.extract_trivial(),
        ...     ),
        ... )

        >>> maker(
        ...     'Music_Voice',
        ...     command,
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:_style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:_style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:_style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:_make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
                            [
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
                            ]
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
                            [
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
                            ]
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
                            [
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
                            ]
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
                            [
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'8
                            ]
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \baca-invisible-music                                            %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                    c'1 * 1/4                                                        %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:_style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:_style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:_style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:_style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:_style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        "_annotate_unpitched_music",
        "_do_not_check_total_duration",
        "_persist",
        "_rhythm_maker",
        "_state",
    )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        rhythm_maker: RhythmMakerTyping = rmakers.note(),
        *,
        annotate_unpitched_music: bool = None,
        do_not_check_total_duration: bool = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        persist: str = None,
        scope: scoping.ScopeTyping = None,
    ) -> None:
        scoping.Command.__init__(
            self, match=match, measures=measures, scope=scope
        )
        if annotate_unpitched_music is not None:
            annotate_unpitched_music = bool(annotate_unpitched_music)
        self._annotate_unpitched_music = annotate_unpitched_music
        if do_not_check_total_duration is not None:
            do_not_check_total_duration = bool(do_not_check_total_duration)
        self._do_not_check_total_duration = do_not_check_total_duration
        if persist is not None:
            assert isinstance(persist, str), repr(persist)
        self._persist = persist
        self._check_rhythm_maker_input(rhythm_maker)
        self._rhythm_maker = rhythm_maker
        self._state: typing.Optional[abjad.OrderedDict] = None

    ### PRIVATE METHODS ###

    @staticmethod
    def _annotate_unpitched_music_(argument):
        rest_prototype = (abjad.MultimeasureRest, abjad.Rest, abjad.Skip)
        for leaf in abjad.iterate(argument).leaves():
            if isinstance(leaf, abjad.Chord):
                message = f"rhythm-makers make only notes and rests: {leaf!r}."
                raise Exception(message)
            elif isinstance(leaf, abjad.Note):
                abjad.attach(abjad.tags.NOT_YET_PITCHED, leaf, tag=None)
            elif isinstance(leaf, rest_prototype):
                pass
            else:
                raise TypeError(leaf)

    def _check_rhythm_maker_input(self, rhythm_maker):
        if rhythm_maker is None:
            return
        prototype = (
            abjad.Selection,
            rmakers.RhythmCommand,
            rmakers.RhythmMaker,
            rmakers.MakerAssignment,
            rmakers.MakerAssignments,
        )
        if isinstance(rhythm_maker, prototype):
            return
        message = '\n  Input parameter "rhythm_maker" accepts:'
        message += "\n    rhythm-maker"
        message += "\n    selection"
        message += "\n    sequence of division assignment objects"
        message += "\n    none"
        message += '\n  Input parameter "rhythm_maker" received:'
        message += f"\n    {format(rhythm_maker)}"
        raise Exception(message)

    def _make_selection(
        self,
        time_signatures: typing.Iterable[abjad.TimeSignature],
        runtime: abjad.OrderedDict = None,
    ) -> abjad.Selection:
        """
        Calls ``RhythmCommand`` on ``time_signatures``.
        """
        rhythm_maker = self.rhythm_maker
        if isinstance(rhythm_maker, abjad.Selection):
            selection = rhythm_maker
            total_duration = sum([_.duration for _ in time_signatures])
            selection_duration = abjad.inspect(selection).duration()
            if (
                not self.do_not_check_total_duration
                and selection_duration != total_duration
            ):
                message = f"selection duration ({selection_duration}) does not"
                message += f" equal total duration ({total_duration})."
                raise Exception(message)
        else:
            if isinstance(self.rhythm_maker, rmakers.RhythmCommand):
                rcommand = self.rhythm_maker
            else:
                rcommand = rmakers.RhythmCommand(self.rhythm_maker)
            previous_segment_stop_state = self._previous_segment_stop_state(
                runtime
            )
            selection = rcommand(
                time_signatures,
                previous_segment_stop_state=previous_segment_stop_state,
            )
            self._state = rcommand.state
        assert isinstance(selection, abjad.Selection), repr(selection)
        if self.annotate_unpitched_music or not isinstance(
            self.rhythm_maker, abjad.Selection
        ):
            self._annotate_unpitched_music_(selection)
        return selection

    def _previous_segment_stop_state(self, runtime):
        previous_segment_stop_state = None
        dictionary = runtime.get("previous_segment_voice_metadata")
        if dictionary:
            previous_segment_stop_state = dictionary.get(const.RHYTHM)
            if (
                previous_segment_stop_state is not None
                and previous_segment_stop_state.get("name") != self.persist
            ):
                previous_segment_stop_state = None
        return previous_segment_stop_state

    ### PUBLIC PROPERTIES ###

    @property
    def annotate_unpitched_music(self) -> typing.Optional[bool]:
        """
        Is true when command annotates unpitched music.
        """
        return self._annotate_unpitched_music

    @property
    def do_not_check_total_duration(self) -> typing.Optional[bool]:
        """
        Is true when command does not check total duration.
        """
        return self._do_not_check_total_duration

    @property
    def parameter(self) -> str:
        """
        Gets persistence parameter.

        ..  container:: example

            >>> baca.RhythmCommand().parameter
            'RHYTHM'

        """
        return const.RHYTHM

    @property
    def persist(self) -> typing.Optional[str]:
        """
        Gets persist name.
        """
        return self._persist

    @property
    def rhythm_maker(self) -> RhythmMakerTyping:
        r"""
        Gets selection, rhythm-maker or division assignment.

        ..  container:: example

            Talea rhythm-maker remembers previous state across gaps:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=5 * [(4, 8)],
            ...     )

            >>> note_rhythm_maker = rmakers.note(
            ...     rmakers.force_rest(baca.lts()),
            ...     rmakers.beam(baca.plts()),
            ... )
            >>> talea_rhythm_maker = rmakers.talea(
            ...     [3, 4],
            ...     16,
            ...     rmakers.beam(),
            ...     rmakers.extract_trivial(),
            ... )
            >>> command = baca.RhythmCommand(
            ...     rhythm_maker=rmakers.MakerAssignments(
            ...         rmakers.MakerAssignment(
            ...             abjad.index([2]), note_rhythm_maker,
            ...         ),
            ...         rmakers.MakerAssignment(
            ...             abjad.index([0], 1),
            ...             talea_rhythm_maker,
            ...             remember_state_across_gaps=True,
            ...         ),
            ...     ),
            ... )

            >>> label = abjad.label().with_durations(
            ...     direction=abjad.Down,
            ...     denominator=16,
            ...     )
            >>> maker(
            ...     'Music_Voice',
            ...     baca.label(label),
            ...     baca.text_script_font_size(-2),
            ...     baca.text_script_staff_padding(5),
            ...     command,
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                <BLANKLINE>
                \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                    \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                    <<                                                                                   %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                        \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                        {                                                                                %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                            % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
                <BLANKLINE>
                            % [Global_Skips measure 6]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
                            \baca-new-spacing-section #1 #4                                              %! PHANTOM:_style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 1/4                                                                    %! PHANTOM:_style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(3)
                            \baca-time-signature-transparent                                             %! PHANTOM:_style_phantom_measures(2)
                            s1 * 1/4                                                                     %! PHANTOM:_make_global_skips(3)
                            \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
                            \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
                <BLANKLINE>
                        }                                                                                %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                    >>                                                                                   %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                    \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                    <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                        \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                                %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                            \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                            {                                                                            %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                                % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                                \override TextScript.font-size = #-2                                     %! baca.text_script_font_size:OverrideCommand(1)
                                \override TextScript.staff-padding = #5                                  %! baca.text_script_staff_padding:OverrideCommand(1)
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8.
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'16
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                                ~
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8
                                _ \markup {
                                    \fraction
                                        2
                                        16
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                                r2
                                _ \markup {
                                    \fraction
                                        8
                                        16
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'16
                                _ \markup {
                                    \fraction
                                        1
                                        16
                                    }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8.
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 5]                                                %! _comment_measure_numbers
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8.
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                                [
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'16
                                _ \markup {
                                    \fraction
                                        1
                                        16
                                    }
                                ]
                                \revert TextScript.font-size                                             %! baca.text_script_font_size:OverrideCommand(2)
                                \revert TextScript.staff-padding                                         %! baca.text_script_staff_padding:OverrideCommand(2)
                <BLANKLINE>
                                <<                                                                       %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                    \context Voice = "Music_Voice"                                       %! PHANTOM:_make_multimeasure_rest_container
                                    {                                                                    %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        % [Music_Voice measure 6]                                        %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                        \baca-invisible-music                                            %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                        c'1 * 1/4                                                        %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                    \context Voice = "Rest_Voice"                                        %! PHANTOM:_make_multimeasure_rest_container
                                    {                                                                    %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        % [Rest_Voice measure 6]                                         %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                        \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:_style_phantom_measures(6)
                                        \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:_style_phantom_measures(7)
                                        \stopStaff                                                       %! PHANTOM:_style_phantom_measures(8)
                                        \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:_style_phantom_measures(8)
                                        \startStaff                                                      %! PHANTOM:_style_phantom_measures(8)
                                        R1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                >>                                                                       %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                            }                                                                            %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                        }                                                                                %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                    >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

        ..  container:: example exception

            Raises exception on invalid input:

            >>> command = baca.RhythmCommand(
            ...     rhythm_maker='text',
            ...     )
            Traceback (most recent call last):
                ...
            Exception:
              Input parameter "rhythm_maker" accepts:
                rhythm-maker
                selection
                sequence of division assignment objects
                none
              Input parameter "rhythm_maker" received:
                text

        """
        return self._rhythm_maker

    @property
    def state(self) -> typing.Optional[abjad.OrderedDict]:
        """
        Gets postcall state of rhythm command.

        Populated by segment-maker.
        """
        return self._state


class SkipRhythmMaker(rmakers.RhythmMaker):
    r"""
    Skip rhythm-maker.

    ..  container:: example

        Makes skips.

        >>> rhythm_maker = baca.SkipRhythmMaker()

        >>> divisions = [(1, 4), (3, 16), (5, 8), (1, 3)]
        >>> selections = rhythm_maker(divisions)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     selections,
        ...     divisions,
        ...     )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \new Score
            <<
                \new GlobalContext
                {
                    \time 1/4
                    s1 * 1/4
                    \time 3/16
                    s1 * 3/16
                    \time 5/8
                    s1 * 5/8
                    #(ly:expect-warning "strange time signature found")
                    \time 1/3
                    s1 * 1/3
                }
                \new RhythmicStaff
                {
                    s1 * 1/4
                    s1 * 3/16
                    s1 * 5/8
                    s1 * 1/3
                }
            >>

    ..  container:: example

        Makes multimeasure rests.

        >>> rhythm_maker = baca.SkipRhythmMaker(use_multimeasure_rests=True)

        >>> divisions = [(1, 4), (3, 16), (5, 8), (1, 3)]
        >>> selections = rhythm_maker(divisions)
        >>> lilypond_file = abjad.LilyPondFile.rhythm(
        ...     selections,
        ...     divisions,
        ...     )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \new Score
            <<
                \new GlobalContext
                {
                    \time 1/4
                    s1 * 1/4
                    \time 3/16
                    s1 * 3/16
                    \time 5/8
                    s1 * 5/8
                    #(ly:expect-warning "strange time signature found")
                    \time 1/3
                    s1 * 1/3
                }
                \new RhythmicStaff
                {
                    R1 * 1/4
                    R1 * 3/16
                    R1 * 5/8
                    R1 * 1/3
                }
            >>

    Usage follows the two-step configure-once / call-repeatedly pattern shown
    here.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_use_multimeasure_rests",)

    ### INITIALIZER ###

    def __init__(
        self,
        *specifiers: rmakers.Command,
        tag: str = None,
        use_multimeasure_rests: bool = None,
    ) -> None:
        rmakers.RhythmMaker.__init__(
            self,
            *specifiers,
            tag=tag,
        )
        if use_multimeasure_rests is not None:
            use_multimeasure_rests = bool(use_multimeasure_rests)
        self._use_multimeasure_rests = use_multimeasure_rests

    ### SPECIAL METHODS ###

    def __call__(
        self,
        divisions: typing.Sequence[abjad.IntegerPair],
        previous_state: abjad.OrderedDict = None,
    ) -> abjad.Selection:
        """
        Calls skip rhythm-maker on ``divisions``.
        """
        return rmakers.RhythmMaker.__call__(
            self, divisions, previous_state=previous_state
        )

    def __format__(self, format_specification="") -> str:
        """
        Formats skip rhythm-maker.

        Set ``format_specification`` to ``''`` or ``'storage'``.

        ..  container:: example

            >>> rhythm_maker = baca.SkipRhythmMaker()
            >>> abjad.f(rhythm_maker)
            baca.SkipRhythmMaker()

        """
        return super().__format__(format_specification=format_specification)

    ### PRIVATE METHODS ###

    def _make_music(self, divisions) -> typing.List[abjad.Selection]:
        component: typing.Union[abjad.MultimeasureRest, abjad.Skip]
        components = []
        for division in divisions:
            assert isinstance(division, abjad.NonreducedFraction)
            if self.use_multimeasure_rests is True:
                component = abjad.MultimeasureRest(
                    1, multiplier=division, tag=self.tag
                )
            else:
                component = abjad.Skip(1, multiplier=division, tag=self.tag)
            components.append(component)
        selection = abjad.select(components)
        return [selection]

    ### PUBLIC PROPERTIES ###

    @property
    def use_multimeasure_rests(self) -> typing.Optional[bool]:
        r"""
        Is true when rhythm-maker makes multimeasure rests instead of skips.
        """
        return self._use_multimeasure_rests


### FACTORY FUNCTIONS ###


def make_even_divisions(
    *,
    measures: typings.SliceTyping = None,
    tag: str = "baca.make_even_divisions",
) -> RhythmCommand:
    """
    Makes even divisions.
    """
    return RhythmCommand(
        measures=measures,
        rhythm_maker=rmakers.even_division(
            rmakers.beam(), rmakers.extract_trivial(), tag=tag
        ),
    )


def make_fused_tuplet_monads(
    *,
    measures: typings.SliceTyping = None,
    tag: str = "baca.make_fused_tuplet_monads",
    tuplet_ratio: typing.Tuple[int] = None,
) -> RhythmCommand:
    """
    Makes fused tuplet monads.
    """
    tuplet_ratios = []
    if tuplet_ratio is None:
        tuplet_ratios.append((1,))
    else:
        tuplet_ratios.append(tuplet_ratio)
    return RhythmCommand(
        measures=measures,
        rhythm_maker=rmakers.RhythmCommand(
            rmakers.TupletRhythmMaker(tag=tag, tuplet_ratios=tuplet_ratios),
            rmakers.beam(),
            rmakers.rewrite_rest_filled(),
            rmakers.trivialize(),
            rmakers.extract_trivial(),
            rmakers.force_repeat_tie(),
            preprocessor=abjad.sequence().sum().sequence(),
            tag=tag,
        ),
    )


def make_monads(fractions: str,) -> RhythmCommand:
    r"""
    Makes monads.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 4)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_monads('2/5 2/5 1/5'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/4                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1                                                                       %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:_style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:_style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:_style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:_make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            \tweak edge-height #'(0.7 . 0)
                            \times 4/5 {
            <BLANKLINE>
                                % [Music_Voice measure 1]                                            %! _comment_measure_numbers
                                \baca-unpitched-music-warning                                        %! _color_unpitched_notes
                                c'2
            <BLANKLINE>
                            }
            <BLANKLINE>
                            \tweak edge-height #'(0.7 . 0)
                            \times 4/5 {
            <BLANKLINE>
                                \baca-unpitched-music-warning                                        %! _color_unpitched_notes
                                c'2
            <BLANKLINE>
                            }
            <BLANKLINE>
                            \tweak edge-height #'(0.7 . 0)
                            \times 4/5 {
            <BLANKLINE>
                                \baca-unpitched-music-warning                                        %! _color_unpitched_notes
                                c'4
            <BLANKLINE>
                            }
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Music_Voice measure 2]                                        %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \baca-invisible-music                                            %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                    c'1 * 1/4                                                        %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Rest_Voice measure 2]                                         %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:_style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:_style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:_style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:_style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:_style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """
    components: typing.List[abjad.Component] = []
    maker = abjad.LeafMaker()
    pitch = 0
    for fraction in fractions.split():
        leaves = maker([pitch], [fraction])
        components.extend(leaves)
    rhythm_maker = abjad.select(components)
    return RhythmCommand(
        annotate_unpitched_music=True, rhythm_maker=rhythm_maker
    )


def make_multimeasure_rests(
    *,
    measures: typings.SliceTyping = None,
    tag: str = "baca.make_multimeasure_rests",
) -> RhythmCommand:
    """
    Makes multimeasure rests.
    """
    return RhythmCommand(
        measures=measures,
        rhythm_maker=SkipRhythmMaker(tag=tag, use_multimeasure_rests=True),
    )


def make_notes(
    *specifiers,
    measures: typings.SliceTyping = None,
    repeat_ties: bool = False,
    tag: str = "baca.make_notes",
) -> RhythmCommand:
    """
    Makes notes; rewrites meter.
    """
    if repeat_ties:
        repeat_tie_specifier = [rmakers.force_repeat_tie()]
    else:
        repeat_tie_specifier = []
    return RhythmCommand(
        measures=measures,
        rhythm_maker=rmakers.note(
            *specifiers,
            # TODO: can this beam specifier be removed?
            rmakers.beam(classes._select().plts()),
            rmakers.rewrite_meter(),
            *repeat_tie_specifier,
            tag=tag,
        ),
    )


def make_repeat_tied_notes(
    *specifiers: rmakers.Command,
    do_not_rewrite_meter: bool = None,
    measures: typings.SliceTyping = None,
    tag: str = "baca.make_repeat_tied_notes",
) -> RhythmCommand:
    r"""
    Makes repeat-tied notes; rewrites meter.

    ..  container:: example

        REGRESSION. All notes below are tagged unpitched (and colored
        gold), even tied notes resulting from meter rewriting:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(10, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_repeat_tied_notes(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 10/8                                                                   %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 5/4                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:_style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:_style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:_style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:_make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'4.
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'4
                            \repeatTie
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'4.
                            \repeatTie
            <BLANKLINE>
                            \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                            c'4                                                                      %! baca.make_repeat_tied_notes
                            \repeatTie
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Music_Voice measure 2]                                        %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \baca-invisible-music                                            %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                    c'1 * 1/4                                                        %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Rest_Voice measure 2]                                         %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:_style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:_style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:_style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:_style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:_style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """
    specifier: rmakers.Command
    specifiers_ = list(specifiers)
    specifier = rmakers.beam(classes._select().plts())
    specifiers_.append(specifier)
    specifier = rmakers.repeat_tie(classes._select().pheads()[1:])
    specifiers_.append(specifier)
    if not do_not_rewrite_meter:
        command = rmakers.rewrite_meter()
        specifiers_.append(command)
    specifier = rmakers.force_repeat_tie()
    specifiers_.append(specifier)
    return RhythmCommand(
        measures=measures, rhythm_maker=rmakers.note(*specifiers_, tag=tag)
    )


def make_repeated_duration_notes(
    durations: typing.Sequence[abjad.DurationTyping],
    *specifiers: rmakers.Command,
    do_not_rewrite_meter: bool = None,
    measures: typings.SliceTyping = None,
    tag: str = "baca.make_repeated_duration_notes",
) -> RhythmCommand:
    """
    Makes repeated-duration notes; rewrites meter.
    """
    if isinstance(durations, abjad.Duration):
        durations = [durations]
    elif isinstance(durations, tuple):
        assert len(durations) == 2
        durations = [abjad.Duration(durations)]
    divisions = divisionclasses._divisions().fuse()
    divisions = divisions.split(durations, cyclic=True)
    rewrite_specifiers: typing.List[rmakers.Command] = []
    if not do_not_rewrite_meter:
        rewrite_specifiers.append(rmakers.rewrite_meter())
    return RhythmCommand(
        rmakers.rhythm(
            rmakers.note(),
            *specifiers,
            *rewrite_specifiers,
            rmakers.force_repeat_tie(),
            preprocessor=divisions,
            tag=tag,
        ),
        measures=measures,
    )


def make_rests(
    *, measures: typings.SliceTyping = None, tag: str = "baca.make_rests"
) -> RhythmCommand:
    """
    Makes rests.
    """
    return RhythmCommand(
        measures=measures,
        rhythm_maker=rmakers.note(
            rmakers.force_rest(classes._select().lts()), tag=tag
        ),
    )


def make_single_attack(
    duration,
    *,
    measures: typings.SliceTyping = None,
    tag: str = "baca.make_single_attack",
) -> RhythmCommand:
    """
    Makes single attacks with ``duration``.
    """
    duration = abjad.Duration(duration)
    numerator, denominator = duration.pair
    rhythm_maker = rmakers.IncisedRhythmMaker(
        rmakers.beam(),
        rmakers.extract_trivial(),
        incise=rmakers.Incise(
            fill_with_rests=True,
            outer_divisions_only=True,
            prefix_talea=[numerator],
            prefix_counts=[1],
            talea_denominator=denominator,
        ),
        tag=tag,
    )
    return RhythmCommand(measures=measures, rhythm_maker=rhythm_maker)


def make_skips(
    *, measures: typings.SliceTyping = None, tag: str = "baca.make_skips"
) -> RhythmCommand:
    """
    Makes skips.
    """
    return RhythmCommand(measures=measures, rhythm_maker=SkipRhythmMaker())


def make_tied_notes(
    *, measures: typings.SliceTyping = None, tag: str = "baca.make_tied_notes"
) -> RhythmCommand:
    """
    Makes tied notes; rewrites meter.
    """
    return RhythmCommand(
        measures=measures,
        rhythm_maker=rmakers.note(
            rmakers.beam(classes._select().plts()),
            rmakers.tie(classes._select().ptails()[:-1]),
            rmakers.rewrite_meter(),
            tag=tag,
        ),
    )


def make_tied_repeated_durations(
    durations: typing.Sequence[abjad.DurationTyping],
    *,
    measures: typings.SliceTyping = None,
    tag: str = "baca.make_tied_repeated_durations",
) -> RhythmCommand:
    """
    Makes tied repeated durations; does not rewrite meter.
    """
    specifiers: typing.List[rmakers.Command] = []
    if isinstance(durations, abjad.Duration):
        durations = [durations]
    elif isinstance(durations, tuple):
        assert len(durations) == 2
        durations = [abjad.Duration(durations)]
    tie_specifier: rmakers.Command
    tie_specifier = rmakers.repeat_tie(classes._select().pheads()[1:])
    specifiers.append(tie_specifier)
    tie_specifier = rmakers.force_repeat_tie()
    specifiers.append(tie_specifier)
    divisions = divisionclasses._divisions().fuse()
    divisions = divisions.split(durations, cyclic=True)
    return RhythmCommand(
        measures=measures,
        rhythm_maker=rmakers.RhythmCommand(
            rmakers.note(tag=tag), *specifiers, preprocessor=divisions, tag=tag
        ),
    )


def music(
    argument: typing.Union[str, abjad.Selection],
    *,
    do_not_check_total_duration: bool = None,
    tag: typing.Optional[str] = "baca.music",
) -> RhythmCommand:
    """
    Makes rhythm command from string or selection ``argument``.
    """
    if isinstance(argument, str):
        string = f"{{ {argument} }}"
        container = abjad.parse(string)
        selection = abjad.mutate(container).eject_contents()
    elif isinstance(argument, abjad.Selection):
        selection = argument
    else:
        message = "baca.music() accepts string or selection,"
        message += " not {repr(argument)}."
        raise TypeError(message)
    if tag is not None:
        tag_selection(selection, tag)
    return RhythmCommand(
        selection, do_not_check_total_duration=do_not_check_total_duration
    )


def rhythm(
    argument: RhythmMakerTyping,
    *,
    measures: typings.SliceTyping = None,
    persist: str = None,
    tag: str = None,
) -> RhythmCommand:
    """
    Makes rhythm command from ``argument``.
    """
    prototype = (
        rmakers.MakerAssignment,
        rmakers.MakerAssignments,
        rmakers.RhythmCommand,
        rmakers.RhythmMaker,
    )
    if not isinstance(argument, prototype):
        message = "baca.rhythm() accepts rhythm-maker and division"
        message += " assignment(s):\n"
        message += f" {repr(argument)}."
        raise TypeError(message)
    if tag is not None:
        if isinstance(argument, rmakers.MakerAssignment):
            argument = abjad.new(argument, rhythm_maker__tag=tag)
        elif isinstance(argument, rmakers.MakerAssignments):
            assignments_ = []
            for assignment in argument.assignments:
                assignment_ = abjad.new(assignment, rhythm_maker__tag=tag)
                assignments_.append(assignment_)
            argument = abjad.new(argument, assignments=assignments_)
        elif isinstance(argument, rmakers.RhythmCommand):
            argument = abjad.new(argument, tag=tag)
        elif isinstance(argument, rmakers.RhythmMaker):
            argument = abjad.new(argument, tag=tag)
        else:
            raise TypeError(argument)
    return RhythmCommand(
        argument,
        annotate_unpitched_music=True,
        measures=measures,
        persist=persist,
    )


def skeleton(
    argument: typing.Union[str, abjad.Selection],
    *,
    do_not_check_total_duration: bool = None,
    tag: typing.Optional[str] = "baca.skeleton",
) -> RhythmCommand:
    """
    Makes rhythm command from ``string`` and annotates music as unpitched.
    """
    if isinstance(argument, str):
        string = f"{{ {argument} }}"
        container = abjad.parse(string)
        selection = abjad.mutate(container).eject_contents()
    elif isinstance(argument, abjad.Selection):
        selection = argument
    else:
        message = "baca.skeleton() accepts string or selection,"
        message += " not {repr(argument)}."
        raise TypeError(message)
    if tag is not None:
        tag_selection(selection, tag)
    return RhythmCommand(
        selection,
        annotate_unpitched_music=True,
        do_not_check_total_duration=do_not_check_total_duration,
    )


def set_duration_multiplier(
    *,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    written_duration: abjad.DurationTyping = None,
) -> DurationMultiplierCommand:
    r"""
    Sets duration multiplier.

    ..  container:: example

        Does nothing when ``written_duration`` is none:

        >>> maker = baca.SegmentMaker(
        ...     do_not_color_unpitched_music=True,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_repeated_duration_notes([(1, 8)]),
        ...     baca.set_duration_multiplier(
        ...         selector=baca.leaves(),
        ...         written_duration=None,
        ...         ),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:_style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:_style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:_style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:_make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            c'8                                                                      %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'8                                                                      %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'8                                                                      %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'8                                                                      %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            c'8                                                                      %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'8                                                                      %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'8                                                                      %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            c'8                                                                      %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'8                                                                      %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'8                                                                      %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'8                                                                      %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            c'8                                                                      %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'8                                                                      %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'8                                                                      %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \baca-invisible-music                                            %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                    c'1 * 1/4                                                        %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:_style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:_style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:_style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:_style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:_style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    ..  container:: example

        Sets duration multiplier to achieve ``written_duration`` equal to 3/32:

        >>> maker = baca.SegmentMaker(
        ...     do_not_color_unpitched_music=True,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_repeated_duration_notes([(1, 8)]),
        ...     baca.set_duration_multiplier(
        ...         selector=baca.leaves(),
        ...         written_duration=(3, 32),
        ...         ),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:_style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:_style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:_style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:_make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            c'16. * 4/3                                                              %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'16. * 4/3                                                              %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'16. * 4/3                                                              %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'16. * 4/3                                                              %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            c'16. * 4/3                                                              %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'16. * 4/3                                                              %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'16. * 4/3                                                              %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            c'16. * 4/3                                                              %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'16. * 4/3                                                              %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'16. * 4/3                                                              %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'16. * 4/3                                                              %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            c'16. * 4/3                                                              %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'16. * 4/3                                                              %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'16. * 4/3                                                              %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \baca-invisible-music                                            %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                    c'1 * 1/4                                                        %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:_style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:_style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:_style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:_style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:_style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    ..  container:: example

        Sets duration multiplier automatically to achieve ``written_duration``
        equal to 1:

        >>> maker = baca.SegmentMaker(
        ...     do_not_color_unpitched_music=True,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_repeated_duration_notes([(1, 8)]),
        ...     baca.set_duration_multiplier(
        ...         selector=baca.leaves(),
        ...         written_duration=(1,),
        ...         ),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:_style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:_style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:_style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:_make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            c'1 * 1/8                                                                %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'1 * 1/8                                                                %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'1 * 1/8                                                                %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'1 * 1/8                                                                %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            c'1 * 1/8                                                                %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'1 * 1/8                                                                %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'1 * 1/8                                                                %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            c'1 * 1/8                                                                %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'1 * 1/8                                                                %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'1 * 1/8                                                                %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'1 * 1/8                                                                %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            c'1 * 1/8                                                                %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'1 * 1/8                                                                %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            c'1 * 1/8                                                                %! baca.make_repeated_duration_notes
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \baca-invisible-music                                            %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                    c'1 * 1/4                                                        %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:_style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:_style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:_style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:_style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:_style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """
    return DurationMultiplierCommand(
        selector=selector, written_duration=written_duration
    )


def tacet(
    color: str = "green",
    *,
    measures: typings.SliceTyping = None,
    selector: abjad.SelectorTyping = "baca.mmrests()",
) -> overrides.OverrideCommand:
    """
    Colors multimeasure rests.
    """
    command = overrides.mmrest_color(
        color, selector=selector, tag=f"{const.TACET}:baca_tacet"
    )
    command_ = scoping.new(command, measures=measures)
    assert isinstance(command_, overrides.OverrideCommand)
    return command_


def tag_selection(selection: abjad.Selection, tag: str) -> None:
    """
    Tags selection.
    """
    assert isinstance(tag, str), repr(tag)
    # TODO: tag attachments
    for component in abjad.iterate(selection).components():
        component._tag = tag
