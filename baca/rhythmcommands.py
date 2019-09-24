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
from . import const
from . import overrides
from . import scoping
from . import typings


RhythmMakerTyping = typing.Union[
    rmakers.Assignment, rmakers.RhythmMaker, rmakers.Stack, rmakers.Bind
]


def _site(frame):
    prefix = "baca"
    return scoping.site(frame, prefix)


### CLASSES ###


class RhythmCommand(scoping.Command):
    r"""
    Rhythm command.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(3, 8), (4, 8), (3,8), (4, 8)],
        ...     )

        >>> command = baca.rhythm(
        ...     rmakers.even_division([8]),
        ...     rmakers.beam(),
        ...     rmakers.extract_trivial(),
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
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
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
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'8
                            [
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'8
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'8
                            ]
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'8
                            [
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'8
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'8
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'8
                            ]
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'8
                            [
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'8
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'8
                            ]
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'8
                            [
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'8
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'8
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'8
                            ]
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
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
        "_annotate_not_yet_pitched",
        "_do_not_check_total_duration",
        "_persist",
        "_rhythm_maker",
        "_state",
    )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        rhythm_maker: RhythmMakerTyping,
        *,
        annotate_not_yet_pitched: bool = None,
        do_not_check_total_duration: bool = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        persist: str = None,
        scope: scoping.ScopeTyping = None,
    ) -> None:
        scoping.Command.__init__(
            self, match=match, measures=measures, scope=scope
        )
        if annotate_not_yet_pitched is not None:
            annotate_not_yet_pitched = bool(annotate_not_yet_pitched)
        self._annotate_not_yet_pitched = annotate_not_yet_pitched
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
    def _annotate_not_yet_pitched_(argument):
        rest_prototype = (abjad.MultimeasureRest, abjad.Rest, abjad.Skip)
        for leaf in abjad.iterate(argument).leaves():
            if isinstance(leaf, (abjad.Note, abjad.Chord)):
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
            rmakers.RhythmMaker,
            rmakers.Assignment,
            rmakers.Stack,
            rmakers.Bind,
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
        time_signatures: typing.Sequence[abjad.IntegerPair],
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
            rcommand: rmakers.Stack
            if isinstance(self.rhythm_maker, rmakers.Stack):
                rcommand = self.rhythm_maker
            else:
                rcommand = rmakers.stack(self.rhythm_maker)
            previous_segment_stop_state = self._previous_segment_stop_state(
                runtime
            )
            if isinstance(rcommand, rmakers.Stack):
                selection = rcommand(
                    time_signatures, previous_state=previous_segment_stop_state
                )
                self._state = rcommand.maker.state
            else:
                selection = rcommand(
                    time_signatures,
                    previous_segment_stop_state=previous_segment_stop_state,
                )
                self._state = rcommand.state
        assert isinstance(selection, abjad.Selection), repr(selection)
        if self.annotate_not_yet_pitched or not isinstance(
            self.rhythm_maker, abjad.Selection
        ):
            container = abjad.Container(selection, name="Dummy")
            self._annotate_not_yet_pitched_(container)
            container[:] = []
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
    def annotate_not_yet_pitched(self) -> typing.Optional[bool]:
        """
        Is true when command annotates not-yet-pitched music.
        """
        return self._annotate_not_yet_pitched

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

            >>> baca.RhythmCommand(rmakers.note()).parameter
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

            >>> note_command = rmakers.stack(
            ...     rmakers.note(),
            ...     rmakers.force_rest(baca.lts()),
            ...     rmakers.beam(baca.plts()),
            ... )
            >>> talea_command = rmakers.stack(
            ...     rmakers.talea([3, 4], 16),
            ...     rmakers.beam(),
            ...     rmakers.extract_trivial(),
            ... )
            >>> command = baca.rhythm(
            ...     rmakers.bind(
            ...         rmakers.assign(note_command, abjad.index([2])),
            ...         rmakers.assign(
            ...             talea_command,
            ...             abjad.index([0], 1),
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
                            % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                            \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                            \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
                <BLANKLINE>
                            % [Global_Skips measure 6]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                            \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                            \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                            s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                            \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                            \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
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
                                % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \override TextScript.font-size = #-2                                     %! baca.text_script_font_size():OverrideCommand(1)
                                \override TextScript.staff-padding = #5                                  %! baca.text_script_staff_padding():OverrideCommand(1)
                                \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                                b'8.
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                <BLANKLINE>
                                \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                                b'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                                b'16
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                                ~
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                                b'8
                <BLANKLINE>
                                \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                                b'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                                b'8
                                _ \markup {
                                    \fraction
                                        2
                                        16
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                r2
                                _ \markup {
                                    \fraction
                                        8
                                        16
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                                b'16
                                _ \markup {
                                    \fraction
                                        1
                                        16
                                    }
                <BLANKLINE>
                                \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                                b'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                                b'8.
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 5]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                                b'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                                b'8.
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                                [
                <BLANKLINE>
                                \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                                b'16
                                _ \markup {
                                    \fraction
                                        1
                                        16
                                    }
                                ]
                                \revert TextScript.font-size                                             %! baca.text_script_font_size():OverrideCommand(2)
                                \revert TextScript.staff-padding                                         %! baca.text_script_staff_padding():OverrideCommand(2)
                <BLANKLINE>
                                <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                    \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                        % [Music_Voice measure 6]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                        \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                        c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                    \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                        % [Rest_Voice measure 6]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                        \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                        \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                        \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                        R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                                >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                <BLANKLINE>
                            }                                                                            %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                        }                                                                                %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                    >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

        """
        return self._rhythm_maker

    @property
    def state(self) -> typing.Optional[abjad.OrderedDict]:
        """
        Gets postcall state of rhythm command.

        Populated by segment-maker.
        """
        return self._state


### FACTORY FUNCTIONS ###


def make_even_divisions(
    *, measures: typings.SliceTyping = None
) -> RhythmCommand:
    """
    Makes even divisions.
    """
    return RhythmCommand(
        rmakers.stack(
            rmakers.even_division([8]),
            rmakers.beam(),
            rmakers.extract_trivial(),
            tag=_site(inspect.currentframe()),
        ),
        measures=measures,
    )


def make_fused_tuplet_monads(
    *,
    measures: typings.SliceTyping = None,
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
        rmakers.stack(
            rmakers.tuplet(tuplet_ratios),
            rmakers.beam(),
            rmakers.rewrite_rest_filled(),
            rmakers.trivialize(),
            rmakers.extract_trivial(),
            rmakers.force_repeat_tie(),
            preprocessor=abjad.sequence().sum().sequence(),
            tag=_site(inspect.currentframe()),
        ),
        measures=measures,
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
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/4                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 1                                                                       %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
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
                                % [Music_Voice measure 1]                                            %! baca.SegmentMaker._comment_measure_numbers()
                                \baca-not-yet-pitched-coloring                                       %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                                b'2
            <BLANKLINE>
                            }
            <BLANKLINE>
                            \tweak edge-height #'(0.7 . 0)
                            \times 4/5 {
            <BLANKLINE>
                                \baca-not-yet-pitched-coloring                                       %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                                b'2
            <BLANKLINE>
                            }
            <BLANKLINE>
                            \tweak edge-height #'(0.7 . 0)
                            \times 4/5 {
            <BLANKLINE>
                                \baca-not-yet-pitched-coloring                                       %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                                b'4
            <BLANKLINE>
                            }
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 2]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 2]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
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
    return RhythmCommand(rhythm_maker, annotate_not_yet_pitched=True)


def make_multimeasure_rests(
    *, measures: typings.SliceTyping = None
) -> RhythmCommand:
    """
    Makes multiplied-duration multimeasure rests.
    """
    return RhythmCommand(
        rmakers.multiplied_duration(
            abjad.MultimeasureRest, tag=_site(inspect.currentframe())
        ),
        measures=measures,
    )


def make_notes(
    *specifiers,
    measures: typings.SliceTyping = None,
    repeat_ties: bool = False,
) -> RhythmCommand:
    """
    Makes notes; rewrites meter.
    """
    if repeat_ties:
        repeat_tie_specifier = [rmakers.force_repeat_tie()]
    else:
        repeat_tie_specifier = []
    return RhythmCommand(
        rmakers.stack(
            rmakers.note(),
            *specifiers,
            # TODO: can this beam specifier be removed?
            ###rmakers.beam(classes.Expression().select().plts()),
            rmakers.rewrite_meter(),
            *repeat_tie_specifier,
            tag=_site(inspect.currentframe()),
        ),
        measures=measures,
    )


def make_repeat_tied_notes(
    *specifiers: rmakers.Command,
    do_not_rewrite_meter: bool = None,
    measures: typings.SliceTyping = None,
) -> RhythmCommand:
    r"""
    Makes repeat-tied notes; rewrites meter.

    ..  container:: example

        REGRESSION. All notes below are tagged NOT_YET_PITCHED (and colored
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
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 10/8                                                                   %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 5/4                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
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
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4
                            \repeatTie
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.
                            \repeatTie
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4                                                                      %! baca.make_repeat_tied_notes()
                            \repeatTie
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 2]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 2]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_mutlipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
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
    specifier = rmakers.beam(classes.Expression().select().plts())
    specifiers_.append(specifier)
    specifier = rmakers.repeat_tie(classes.Expression().select().pheads()[1:])
    specifiers_.append(specifier)
    if not do_not_rewrite_meter:
        command = rmakers.rewrite_meter()
        specifiers_.append(command)
    specifier = rmakers.force_repeat_tie()
    specifiers_.append(specifier)
    return RhythmCommand(
        rmakers.stack(
            rmakers.note(), *specifiers_, tag=_site(inspect.currentframe())
        )
    )


def make_repeated_duration_notes(
    durations: typing.Sequence[abjad.DurationTyping],
    *specifiers: rmakers.Command,
    do_not_rewrite_meter: bool = None,
    measures: typings.SliceTyping = None,
) -> RhythmCommand:
    """
    Makes repeated-duration notes; rewrites meter.
    """
    if isinstance(durations, abjad.Duration):
        durations = [durations]
    elif isinstance(durations, tuple):
        assert len(durations) == 2
        durations = [abjad.Duration(durations)]
    divisions = classes.Expression().sequence().fuse()
    divisions = divisions.split_divisions(durations, cyclic=True)
    rewrite_specifiers: typing.List[rmakers.Command] = []
    if not do_not_rewrite_meter:
        rewrite_specifiers.append(rmakers.rewrite_meter())
    return RhythmCommand(
        rmakers.stack(
            rmakers.note(),
            *specifiers,
            *rewrite_specifiers,
            rmakers.force_repeat_tie(),
            preprocessor=divisions,
            tag=_site(inspect.currentframe()),
        ),
        measures=measures,
    )


def make_rests(*, measures: typings.SliceTyping = None) -> RhythmCommand:
    """
    Makes rests.
    """
    return RhythmCommand(
        rmakers.stack(
            rmakers.note(),
            rmakers.force_rest(classes.Expression().select().lts()),
            tag=_site(inspect.currentframe()),
        ),
        measures=measures,
    )


def make_single_attack(
    duration, *, measures: typings.SliceTyping = None
) -> RhythmCommand:
    """
    Makes single attacks with ``duration``.
    """
    duration = abjad.Duration(duration)
    numerator, denominator = duration.pair
    return RhythmCommand(
        rmakers.stack(
            rmakers.incised(
                fill_with_rests=True,
                outer_divisions_only=True,
                prefix_talea=[numerator],
                prefix_counts=[1],
                talea_denominator=denominator,
            ),
            rmakers.beam(),
            rmakers.extract_trivial(),
            tag=_site(inspect.currentframe()),
        ),
        measures=measures,
    )


def make_skips(*, measures: typings.SliceTyping = None) -> RhythmCommand:
    """
    Makes multiplied-duration skips.
    """
    return RhythmCommand(
        rmakers.multiplied_duration(
            abjad.Skip, tag=_site(inspect.currentframe())
        ),
        measures=measures,
    )


def make_tied_notes(*, measures: typings.SliceTyping = None) -> RhythmCommand:
    """
    Makes tied notes; rewrites meter.
    """
    return RhythmCommand(
        rmakers.stack(
            rmakers.note(),
            rmakers.beam(classes.Expression().select().plts()),
            rmakers.tie(classes.Expression().select().ptails()[:-1]),
            rmakers.rewrite_meter(),
            tag=_site(inspect.currentframe()),
        ),
        measures=measures,
    )


def make_tied_repeated_durations(
    durations: typing.Sequence[abjad.DurationTyping],
    *,
    measures: typings.SliceTyping = None,
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
    tie_specifier = rmakers.repeat_tie(
        classes.Expression().select().pheads()[1:]
    )
    specifiers.append(tie_specifier)
    tie_specifier = rmakers.force_repeat_tie()
    specifiers.append(tie_specifier)
    divisions = classes.Expression().sequence().fuse()
    divisions = divisions.split_divisions(durations, cyclic=True)
    return RhythmCommand(
        rmakers.stack(
            rmakers.note(),
            *specifiers,
            preprocessor=divisions,
            tag=_site(inspect.currentframe()),
        ),
        measures=measures,
    )


def music(
    argument: typing.Union[str, abjad.Selection],
    *,
    do_not_check_total_duration: bool = None,
    tag: typing.Optional[str] = "baca.music()",
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
        message += f" not {repr(argument)}."
        raise TypeError(message)
    if tag is not None:
        tag_selection(selection, tag)
    return RhythmCommand(
        selection, do_not_check_total_duration=do_not_check_total_duration
    )


def rhythm(
    *arguments,
    preprocessor: abjad.Expression = None,
    measures: typings.SliceTyping = None,
    persist: str = None,
    tag: str = None,
) -> RhythmCommand:
    """
    Makes rhythm command from ``argument``.
    """
    argument = rmakers.stack(*arguments, preprocessor=preprocessor, tag=tag)
    return RhythmCommand(
        argument,
        annotate_not_yet_pitched=True,
        measures=measures,
        persist=persist,
    )


def skeleton(
    argument: typing.Union[str, abjad.Selection],
    *,
    do_not_check_total_duration: bool = None,
    tag: typing.Optional[str] = "baca.skeleton()",
) -> RhythmCommand:
    """
    Makes rhythm command from ``string`` and annotates music as NOT_YET_PITCHED.
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
        annotate_not_yet_pitched=True,
        do_not_check_total_duration=do_not_check_total_duration,
    )


def tacet(
    color: str = "green",
    *,
    measures: typings.SliceTyping = None,
    selector: abjad.SelectorTyping = classes.Expression().select().mmrests(),
) -> overrides.OverrideCommand:
    """
    Colors multimeasure rests.
    """
    command = overrides.mmrest_color(color, selector=selector)
    scoping.tag(const.TACET, command)
    scoping.tag(_site(inspect.currentframe()), command)
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
