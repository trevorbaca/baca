import abjad
import collections
import typing
from . import classes
from . import const
from . import indicators
from . import pitchcommands
from . import rhythmcommands
from . import scoping
from . import typings


### CLASSES ###


class BCPCommand(scoping.Command):
    """
    Bow contact point command.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_bow_change_tweaks",
        "_bow_contact_points",
        "_final_spanner",
        "_helper",
        "_tweaks",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        bcps: typing.Sequence[abjad.IntegerPair] = None,
        bow_change_tweaks: abjad.IndexedTweakManagers = None,
        final_spanner: bool = None,
        helper: typing.Callable = None,
        map: abjad.SelectorTyping = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        scope: scoping.ScopeTyping = None,
        selector: abjad.SelectorTyping = None,
        tags: typing.List[typing.Union[str, abjad.Tag, None]] = None,
        tweaks: abjad.IndexedTweakManagers = None,
    ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
            tags=tags,
        )
        if bcps is None:
            self._validate_bcps(bcps)
        self._bow_contact_points = bcps
        self._bow_change_tweaks = None
        self._validate_indexed_tweaks(bow_change_tweaks)
        self._bow_change_tweaks = bow_change_tweaks
        if final_spanner is not None:
            final_spanner = bool(final_spanner)
        self._final_spanner = final_spanner
        if helper is not None:
            assert callable(helper), repr(helper)
        self._helper = helper
        self._validate_indexed_tweaks(tweaks)
        self._tweaks = tweaks

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        if argument is None:
            return
        if self.bcps is None:
            return
        if self.selector:
            argument = self.selector(argument)
        leaves = classes.Selection(argument).leaves()
        bcps_ = classes.Sequence(self.bcps)
        if self.helper:
            bcps_ = self.helper(bcps_, argument)
        bcps = abjad.CyclicTuple(bcps_)
        lts = classes.Selection(argument).lts()
        assert isinstance(lts, classes.Selection)
        total = len(lts)
        add_right_text_to_me = None
        if not self.final_spanner:
            rest_count, nonrest_count = 0, 0
            lt: abjad.LogicalTie
            for lt in reversed(lts):
                if self._is_rest(lt.head):
                    rest_count += 1
                else:
                    if 0 < rest_count and nonrest_count == 0:
                        add_right_text_to_me = lt.head
                        break
                    if 0 < nonrest_count and rest_count == 0:
                        add_right_text_to_me = lt.head
                        break
                    nonrest_count += 1
        if (
            self.final_spanner
            and not self._is_rest(lts[-1])
            and len(lts[-1]) == 1
        ):
            next_leaf_after_argument = abjad.inspect(lts[-1][-1]).leaf(1)
            if next_leaf_after_argument is None:
                message = "can not attach final spanner:"
                message += " argument includes end of score."
                raise Exception(message)
        previous_bcp = None
        i = 0
        for lt in lts:
            stop_text_span = abjad.StopTextSpan(command=self.stop_command)
            if (
                not self.final_spanner
                and lt is lts[-1]
                and not self._is_rest(lt.head)
            ):
                abjad.attach(
                    stop_text_span,
                    lt.head,
                    tag=self.tag.append("BCPCommand(1)"),
                )
                break
            previous_leaf = abjad.inspect(lt.head).leaf(-1)
            next_leaf = abjad.inspect(lt.head).leaf(1)
            if self._is_rest(lt.head) and (
                self._is_rest(previous_leaf) or previous_leaf is None
            ):
                continue
            if (
                isinstance(lt.head, abjad.Note)
                and self._is_rest(previous_leaf)
                and previous_bcp is not None
            ):
                numerator, denominator = previous_bcp
            else:
                bcp = bcps[i]
                numerator, denominator = bcp
                i += 1
                next_bcp = bcps[i]
            left_text = r"- \baca-bcp-spanner-left-text"
            left_text += rf" #{numerator} #{denominator}"
            if lt is lts[-1]:
                if self.final_spanner:
                    style = "solid-line-with-arrow"
                else:
                    style = "invisible-line"
            elif not self._is_rest(lt.head):
                style = "solid-line-with-arrow"
            else:
                style = "invisible-line"
            right_text = None
            if lt.head is add_right_text_to_me:
                numerator, denominator = next_bcp
                right_text = r"- \baca-bcp-spanner-right-text"
                right_text += rf" #{numerator} #{denominator}"
            start_text_span = abjad.StartTextSpan(
                command=self.start_command,
                left_text=left_text,
                right_text=right_text,
                style=style,
            )
            if self.tweaks:
                self._apply_tweaks(start_text_span, self.tweaks)
            if self._is_rest(lt.head) and (
                self._is_rest(next_leaf) or next_leaf is None
            ):
                pass
            else:
                abjad.attach(
                    start_text_span,
                    lt.head,
                    tag=self.tag.append("BCPCommand(2)"),
                )
            if 0 < i - 1:
                abjad.attach(
                    stop_text_span,
                    lt.head,
                    tag=self.tag.append("BCPCommand(3)"),
                )
            if lt is lts[-1] and self.final_spanner:
                abjad.attach(
                    stop_text_span,
                    next_leaf_after_argument,
                    tag=self.tag.append("BCPCommand(4)"),
                )
            bcp_fraction = abjad.Fraction(*bcp)
            next_bcp_fraction = abjad.Fraction(*bcps[i])
            if self._is_rest(lt.head):
                pass
            elif self._is_rest(previous_leaf) or previous_bcp is None:
                if bcp_fraction > next_bcp_fraction:
                    articulation = abjad.Articulation("upbow")
                    if self.bow_change_tweaks:
                        self._apply_tweaks(
                            articulation, self.bow_change_tweaks
                        )
                    abjad.attach(
                        # abjad.Articulation('upbow'),
                        articulation,
                        lt.head,
                        tag=self.tag.append("BCPCommand(5)"),
                    )
                elif bcp_fraction < next_bcp_fraction:
                    articulation = abjad.Articulation("downbow")
                    if self.bow_change_tweaks:
                        self._apply_tweaks(
                            articulation, self.bow_change_tweaks
                        )
                    abjad.attach(
                        # abjad.Articulation('downbow'),
                        articulation,
                        lt.head,
                        tag=self.tag.append("BCPCommand(6)"),
                    )
            else:
                previous_bcp_fraction = abjad.Fraction(*previous_bcp)
                if previous_bcp_fraction < bcp_fraction > next_bcp_fraction:
                    articulation = abjad.Articulation("upbow")
                    if self.bow_change_tweaks:
                        self._apply_tweaks(
                            articulation, self.bow_change_tweaks
                        )
                    abjad.attach(
                        # abjad.Articulation('upbow'),
                        articulation,
                        lt.head,
                        tag=self.tag.append("BCPCommand(7)"),
                    )
                elif previous_bcp_fraction > bcp_fraction < next_bcp_fraction:
                    articulation = abjad.Articulation("downbow")
                    if self.bow_change_tweaks:
                        self._apply_tweaks(
                            articulation, self.bow_change_tweaks
                        )
                    abjad.attach(
                        # abjad.Articulation('downbow'),
                        articulation,
                        lt.head,
                        tag=self.tag.append("BCPCommand(8)"),
                    )
            previous_bcp = bcp

    ### PRIVATE METHODS ###

    @staticmethod
    def _is_rest(argument):
        prototype = (abjad.Rest, abjad.MultimeasureRest, abjad.Skip)
        if isinstance(argument, prototype):
            return True
        annotation = abjad.inspect(argument).annotation("is_sounding")
        if annotation is False:
            return True
        return False

    @staticmethod
    def _validate_bcps(bcps):
        if bcps is None:
            return
        for bcp in bcps:
            assert isinstance(bcp, tuple), repr(bcp)
            assert len(bcp) == 2, repr(bcp)

    ### PUBLIC PROPERTIES ###

    @property
    def bcps(self) -> typing.Optional[typing.Sequence[abjad.IntegerPair]]:
        r"""
        Gets bow contact points.

        ..  container:: example

            PATTERN. Define chunkwise spanners like this:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 16)),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.make_even_divisions(),
            ...     baca.new(
            ...         baca.bcps(bcps=[(1, 5), (2, 5)]),
            ...         measures=(1, 2),
            ...         ),
            ...     baca.new(
            ...         baca.bcps(bcps=[(3, 5), (4, 5)]),
            ...         measures=(3, 4),
            ...         ),
            ...     baca.pitches('E4 F4'),
            ...     baca.script_staff_padding(5.5),
            ...     baca.text_spanner_staff_padding(2.5),
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
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
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
                                \override Script.staff-padding = #5.5                                    %! baca.script_staff_padding:OverrideCommand(1)
                                \override TextSpanner.staff-padding = #2.5                               %! baca.text_spanner_staff_padding:OverrideCommand(1)
                                e'8                                                                      %! baca.make_even_divisions
                                - \downbow                                                               %! baca.bcps:BCPCommand(6)
                                [                                                                        %! baca.make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions
                                - \upbow                                                                 %! baca.bcps:BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions
                                - \downbow                                                               %! baca.bcps:BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions
                                - \upbow                                                                 %! baca.bcps:BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                ]                                                                        %! baca.make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                                e'8                                                                      %! baca.make_even_divisions
                                - \downbow                                                               %! baca.bcps:BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                [                                                                        %! baca.make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions
                                - \upbow                                                                 %! baca.bcps:BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-right-text #1 #5                                     %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(1)
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                                f'8                                                                      %! baca.make_even_divisions
                                - \downbow                                                               %! baca.bcps:BCPCommand(6)
                                [                                                                        %! baca.make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #3 #5                                      %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions
                                - \upbow                                                                 %! baca.bcps:BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #4 #5                                      %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions
                                - \downbow                                                               %! baca.bcps:BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #3 #5                                      %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions
                                - \upbow                                                                 %! baca.bcps:BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                ]                                                                        %! baca.make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #4 #5                                      %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                                f'8                                                                      %! baca.make_even_divisions
                                - \downbow                                                               %! baca.bcps:BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                [                                                                        %! baca.make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #3 #5                                      %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions
                                - \upbow                                                                 %! baca.bcps:BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #4 #5                                      %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-right-text #3 #5                                     %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(1)
                                ]                                                                        %! baca.make_even_divisions
                                \revert Script.staff-padding                                             %! baca.script_staff_padding:OverrideCommand(2)
                                \revert TextSpanner.staff-padding                                        %! baca.text_spanner_staff_padding:OverrideCommand(2)
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
        return self._bow_contact_points

    @property
    def bow_change_tweaks(self) -> typing.Optional[abjad.IndexedTweakManagers]:
        """
        Gets bow change tweaks.
        """
        return self._bow_change_tweaks

    @property
    def final_spanner(self) -> typing.Optional[bool]:
        """
        Is true when command outputs dangling final spanner.
        """
        return self._final_spanner

    @property
    def helper(self) -> typing.Optional[typing.Callable]:
        """
        Gets BCP helper.
        """
        return self._helper

    @property
    def start_command(self) -> str:
        r"""
        Gets ``'\bacaStartTextSpanBCP'``.
        """
        return r"\bacaStartTextSpanBCP"

    @property
    def stop_command(self) -> str:
        r"""
        Gets ``'\bacaStopTextSpanBCP'``.
        """
        return r"\bacaStopTextSpanBCP"

    @property
    def tag(self) -> abjad.Tag:
        """
        Gets tag.

        ..  container:: example

            >>> baca.BCPCommand().tag
            Tag()

        """
        return super().tag

    @property
    def tweaks(self) -> typing.Optional[abjad.IndexedTweakManagers]:
        r"""
        Gets tweaks.

        ..  container:: example

            Tweaks LilyPond ``TextSpanner`` grob:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 16)),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.make_even_divisions(),
            ...     baca.bcps(
            ...         [(1, 5), (2, 5)],
            ...         abjad.tweak('red').color,
            ...         abjad.tweak(2.5).staff_padding,
            ...         ),
            ...     baca.pitches('E4 F4'),
            ...     baca.script_staff_padding(5),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Style LilyPond ``Script`` grob with overrides (instead of tweaks).

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
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
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
                                \override Script.staff-padding = #5                                      %! baca.script_staff_padding:OverrideCommand(1)
                                e'8                                                                      %! baca.make_even_divisions
                                - \downbow                                                               %! baca.bcps:BCPCommand(6)
                                [                                                                        %! baca.make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! baca.bcps:BCPCommand(2)
                                - \tweak color #red                                                      %! baca.bcps:BCPCommand(2)
                                - \tweak staff-padding #2.5                                              %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions
                                - \upbow                                                                 %! baca.bcps:BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! baca.bcps:BCPCommand(2)
                                - \tweak color #red                                                      %! baca.bcps:BCPCommand(2)
                                - \tweak staff-padding #2.5                                              %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions
                                - \downbow                                                               %! baca.bcps:BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! baca.bcps:BCPCommand(2)
                                - \tweak color #red                                                      %! baca.bcps:BCPCommand(2)
                                - \tweak staff-padding #2.5                                              %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions
                                - \upbow                                                                 %! baca.bcps:BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                ]                                                                        %! baca.make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! baca.bcps:BCPCommand(2)
                                - \tweak color #red                                                      %! baca.bcps:BCPCommand(2)
                                - \tweak staff-padding #2.5                                              %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                                e'8                                                                      %! baca.make_even_divisions
                                - \downbow                                                               %! baca.bcps:BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                [                                                                        %! baca.make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! baca.bcps:BCPCommand(2)
                                - \tweak color #red                                                      %! baca.bcps:BCPCommand(2)
                                - \tweak staff-padding #2.5                                              %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions
                                - \upbow                                                                 %! baca.bcps:BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! baca.bcps:BCPCommand(2)
                                - \tweak color #red                                                      %! baca.bcps:BCPCommand(2)
                                - \tweak staff-padding #2.5                                              %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions
                                - \downbow                                                               %! baca.bcps:BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                ]                                                                        %! baca.make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! baca.bcps:BCPCommand(2)
                                - \tweak color #red                                                      %! baca.bcps:BCPCommand(2)
                                - \tweak staff-padding #2.5                                              %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                                f'8                                                                      %! baca.make_even_divisions
                                - \upbow                                                                 %! baca.bcps:BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                [                                                                        %! baca.make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! baca.bcps:BCPCommand(2)
                                - \tweak color #red                                                      %! baca.bcps:BCPCommand(2)
                                - \tweak staff-padding #2.5                                              %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions
                                - \downbow                                                               %! baca.bcps:BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! baca.bcps:BCPCommand(2)
                                - \tweak color #red                                                      %! baca.bcps:BCPCommand(2)
                                - \tweak staff-padding #2.5                                              %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions
                                - \upbow                                                                 %! baca.bcps:BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! baca.bcps:BCPCommand(2)
                                - \tweak color #red                                                      %! baca.bcps:BCPCommand(2)
                                - \tweak staff-padding #2.5                                              %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions
                                - \downbow                                                               %! baca.bcps:BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                ]                                                                        %! baca.make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! baca.bcps:BCPCommand(2)
                                - \tweak color #red                                                      %! baca.bcps:BCPCommand(2)
                                - \tweak staff-padding #2.5                                              %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                                f'8                                                                      %! baca.make_even_divisions
                                - \upbow                                                                 %! baca.bcps:BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                [                                                                        %! baca.make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! baca.bcps:BCPCommand(2)
                                - \tweak color #red                                                      %! baca.bcps:BCPCommand(2)
                                - \tweak staff-padding #2.5                                              %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions
                                - \downbow                                                               %! baca.bcps:BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-right-text #2 #5                                     %! baca.bcps:BCPCommand(2)
                                - \tweak color #red                                                      %! baca.bcps:BCPCommand(2)
                                - \tweak staff-padding #2.5                                              %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(1)
                                ]                                                                        %! baca.make_even_divisions
                                \revert Script.staff-padding                                             %! baca.script_staff_padding:OverrideCommand(2)
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

            REGRESSION. Tweaks survive copy:

            >>> command = baca.bcps(
            ...     [(1, 2), (1, 4)],
            ...     abjad.tweak('red').color,
            ...     )
            >>> abjad.f(command)
            baca.BCPCommand(
                bcps=[
                    (1, 2),
                    (1, 4),
                    ],
                selector=baca.leaves(),
                tags=[
                    abjad.Tag('baca.bcps'),
                    ],
                tweaks=(
                    LilyPondTweakManager(('color', 'red')),
                    ),
                )

            >>> new_command = abjad.new(command)
            >>> abjad.f(new_command)
            baca.BCPCommand(
                bcps=[
                    (1, 2),
                    (1, 4),
                    ],
                selector=baca.leaves(),
                tags=[
                    abjad.Tag('baca.bcps'),
                    ],
                tweaks=(
                    LilyPondTweakManager(('color', 'red')),
                    ),
                )

        """
        return self._tweaks


class ColorCommand(scoping.Command):
    """
    Color command.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        map: abjad.SelectorTyping = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        scope: scoping.ScopeTyping = None,
        selector: abjad.SelectorTyping = "baca.leaves()",
    ) -> None:
        assert selector is not None
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
        )

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        assert self.selector is not None
        argument = self.selector(argument)
        self.selector.color(argument)


class ContainerCommand(scoping.Command):
    r"""
    Container command.

    ..  container:: example

        >>> baca.ContainerCommand()
        ContainerCommand(selector=baca.leaves())

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.container('ViolinI', selector=baca.leaves()[:2]),
        ...     baca.container('ViolinII', selector=baca.leaves()[2:]),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')

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
                    \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 1/2                                                                     %! _make_global_skips(1)
        <BLANKLINE>
                    % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                    \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 3/8                                                                     %! _make_global_skips(1)
        <BLANKLINE>
                    % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                    \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 1/2                                                                     %! _make_global_skips(1)
        <BLANKLINE>
                    % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                    \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 3/8                                                                     %! _make_global_skips(1)
                    \baca-bar-line-visible                                                       %! _attach_final_bar_line
                    \bar "|"                                                                     %! _attach_final_bar_line
        <BLANKLINE>
                    % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                        {   %*% ViolinI
        <BLANKLINE>
                            % [Music_Voice measure 1]                                            %! _comment_measure_numbers
                            e'2                                                                  %! baca.make_notes
        <BLANKLINE>
                            % [Music_Voice measure 2]                                            %! _comment_measure_numbers
                            f'4.                                                                 %! baca.make_notes
        <BLANKLINE>
                        }   %*% ViolinI
        <BLANKLINE>
                        {   %*% ViolinII
        <BLANKLINE>
                            % [Music_Voice measure 3]                                            %! _comment_measure_numbers
                            e'2                                                                  %! baca.make_notes
        <BLANKLINE>
                            % [Music_Voice measure 4]                                            %! _comment_measure_numbers
                            f'4.                                                                 %! baca.make_notes
        <BLANKLINE>
                        }   %*% ViolinII
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

    ### CLASS VARIABLES ###

    __slots__ = ("_identifier",)

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        identifier: str = None,
        map: abjad.SelectorTyping = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        scope: scoping.ScopeTyping = None,
        selector: abjad.SelectorTyping = "baca.leaves()",
    ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
        )
        if identifier is not None:
            if not isinstance(identifier, str):
                message = f"identifier must be string (not {identifier!r})."
                raise Exception(message)
        self._identifier = identifier
        self._tags: typing.List[abjad.Tag] = []

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Inserts ``selector`` output in container.
        """
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if not self.identifier:
            identifier = None
        elif self.identifier.startswith("%*%"):
            identifier = self.identifier
        else:
            identifier = f"%*% {self.identifier}"
        container = abjad.Container(identifier=identifier)
        components = classes.Selection(argument).leaves().top()
        abjad.mutate(components).wrap(container)

    ### PRIVATE METHODS ###

    def _mutates_score(self):
        return True

    ### PUBLIC PROPERTIES ###

    @property
    def identifier(self) -> typing.Optional[str]:
        """
        Gets identifier.
        """
        return self._identifier


class DetachCommand(scoping.Command):
    """
    Detach command.

    ..  container:: example

        >>> arguments = [abjad.RepeatTie, abjad.Tie]
        >>> baca.DetachCommand(arguments, baca.leaves())
        DetachCommand([RepeatTie, Tie], baca.leaves())

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_arguments",)

    ### INITIALIZER ###

    def __init__(
        self,
        arguments: typing.Sequence[typing.Any],
        selector: abjad.SelectorTyping,
        map: abjad.SelectorTyping = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        scope: scoping.ScopeTyping = None,
    ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
        )
        self._arguments = arguments

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Applies command to result of selector called on ``argument``.
        """
        if argument is None:
            return
        assert self.selector is not None
        argument = self.selector(argument)
        leaves = classes.Selection(argument).leaves()
        assert isinstance(leaves, abjad.Selection)
        for leaf in leaves:
            for argument in self.arguments:
                abjad.detach(argument, leaf)

    ### PUBLIC PROPERTIES ###

    @property
    def arguments(self) -> typing.Sequence[typing.Any]:
        """
        Gets arguments.
        """
        return self._arguments


class GlissandoCommand(scoping.Command):
    """
    Glissando command.

    ..  container:: example

        >>> baca.GlissandoCommand()
        GlissandoCommand(selector=baca.tleaves(), tags=[])

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_allow_repeats",
        "_allow_ties",
        "_hide_middle_note_heads",
        "_hide_middle_stems",
        "_left_broken",
        "_parenthesize_repeats",
        "_right_broken",
        "_right_broken_show_next",
        "_tweaks",
        "_zero_padding",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        allow_repeats: bool = None,
        allow_ties: bool = None,
        hide_middle_note_heads: bool = None,
        hide_middle_stems: bool = None,
        left_broken: bool = None,
        map: abjad.SelectorTyping = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        parenthesize_repeats: bool = None,
        right_broken: bool = None,
        right_broken_show_next: bool = None,
        scope: scoping.ScopeTyping = None,
        selector: abjad.SelectorTyping = "baca.tleaves()",
        tags: typing.List[typing.Union[str, abjad.Tag, None]] = None,
        tweaks: abjad.IndexedTweakManagers = None,
        zero_padding: bool = None,
    ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
            tags=tags,
        )
        self._allow_repeats = allow_repeats
        self._allow_ties = allow_ties
        self._hide_middle_note_heads = hide_middle_note_heads
        self._hide_middle_stems = hide_middle_stems
        self._left_broken = left_broken
        self._parenthesize_repeats = parenthesize_repeats
        self._right_broken = right_broken
        self._right_broken_show_next = right_broken_show_next
        self._validate_indexed_tweaks(tweaks)
        self._tweaks = tweaks
        self._zero_padding = zero_padding

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Applies command to result of selector called on ``argument``.
        """
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        leaves = classes.Selection(argument).leaves()
        tweaks_: typing.List[abjad.IndexedTweakManager] = []
        prototype = (abjad.LilyPondTweakManager, tuple)
        for tweak in self.tweaks or []:
            assert isinstance(tweak, prototype)
            tweaks_.append(tweak)
        abjad.glissando(
            leaves,
            *tweaks_,
            allow_repeats=self.allow_repeats,
            allow_ties=self.allow_ties,
            hide_middle_note_heads=self.hide_middle_note_heads,
            hide_middle_stems=self.hide_middle_stems,
            left_broken=self.left_broken,
            parenthesize_repeats=self.parenthesize_repeats,
            right_broken=self.right_broken,
            right_broken_show_next=self.right_broken_show_next,
            tag=str(self.tag),
            zero_padding=self.zero_padding,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def allow_repeats(self) -> typing.Optional[bool]:
        """
        Is true when glissando allows repeats.
        """
        return self._allow_repeats

    @property
    def allow_ties(self) -> typing.Optional[bool]:
        """
        Is true when glissando allows ties.
        """
        return self._allow_ties

    @property
    def hide_middle_note_heads(self) -> typing.Optional[bool]:
        """
        Is true when glissando hides middle note heads.
        """
        return self._hide_middle_note_heads

    @property
    def hide_middle_stems(self) -> typing.Optional[bool]:
        """
        Is true when glissando hides middle stems.
        """
        return self._hide_middle_stems

    @property
    def left_broken(self) -> typing.Optional[bool]:
        """
        Is true when glissando is left-broken.
        """
        return self._left_broken

    @property
    def parenthesize_repeats(self) -> typing.Optional[bool]:
        """
        Is true when glissando parenthesizes repeats.
        """
        return self._parenthesize_repeats

    @property
    def right_broken(self) -> typing.Optional[bool]:
        """
        Is true when glissando is right-broken.
        """
        return self._right_broken

    @property
    def right_broken_show_next(self) -> typing.Optional[bool]:
        """
        Is true when right-broken glissando shows next note.
        """
        return self._right_broken_show_next

    @property
    def tweaks(self) -> typing.Optional[abjad.IndexedTweakManagers]:
        """
        Gets tweaks.
        """
        return self._tweaks

    @property
    def zero_padding(self) -> typing.Optional[bool]:
        """
        Is true when glissando formats zero padding.
        """
        return self._zero_padding


class GlobalFermataCommand(scoping.Command):
    """
    Global fermata command.

    ..  container:: example

        >>> baca.GlobalFermataCommand()
        GlobalFermataCommand(selector=baca.leaf(0), tags=[])

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_description",)

    description_to_command = {
        "short": "shortfermata",
        "fermata": "fermata",
        "long": "longfermata",
        "very_long": "verylongfermata",
    }

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        description: str = None,
        map: abjad.SelectorTyping = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        scope: scoping.ScopeTyping = None,
        selector: abjad.SelectorTyping = "baca.leaf(0)",
        tags: typing.List[typing.Union[str, abjad.Tag, None]] = None,
    ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
            tags=tags,
        )
        if description is not None:
            assert description in GlobalFermataCommand.description_to_command
        self._description = description

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Applies command to ``argument`` selector output.
        """
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if isinstance(self.description, str) and self.description != "fermata":
            description = self.description.replace("_", "-")
            command = f"{description}-fermata"
        else:
            command = "fermata"
        if self.description == "short":
            fermata_duration = 1
        elif self.description == "fermata":
            fermata_duration = 2
        elif self.description == "long":
            fermata_duration = 4
        elif self.description == "very_long":
            fermata_duration = 8
        else:
            raise Exception(self.description)
        for leaf in abjad.iterate(argument).leaves():
            assert isinstance(leaf, abjad.MultimeasureRest)
            string = rf"\baca-{command}-markup"
            markup = abjad.Markup(string, literal=True)
            markup = abjad.new(markup, direction=abjad.Up)
            abjad.attach(
                markup, leaf, tag=self.tag.append("GlobalFermataCommand(1)")
            )
            literal = abjad.LilyPondLiteral(r"\baca-fermata-measure")
            abjad.attach(
                literal, leaf, tag=self.tag.append("GlobalFermataCommand(2)")
            )
            tag = abjad.Tag.from_words(
                [
                    abjad.tags.FERMATA_MEASURE,
                    str(self.tag),
                    "GlobalFermataCommand(3)",
                ]
            )
            abjad.attach(
                abjad.tags.FERMATA_MEASURE,
                leaf,
                tag=abjad.tags.FERMATA_MEASURE,
            )
            abjad.annotate(leaf, const.FERMATA_DURATION, fermata_duration)

    ### PUBLIC PROPERTIES ###

    @property
    def description(self) -> typing.Optional[str]:
        """
        Gets description.
        """
        return self._description


class IndicatorCommand(scoping.Command):
    r"""
    Indicator command.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_context",
        "_do_not_test",
        "_indicators",
        "_predicate",
        "_redundant",
        "_tags",
        "_tweaks",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        context: str = None,
        deactivate: bool = None,
        do_not_test: bool = None,
        indicators: typing.List[typing.Any] = None,
        map: abjad.SelectorTyping = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        predicate: typing.Callable = None,
        redundant: bool = None,
        scope: scoping.ScopeTyping = None,
        selector: abjad.SelectorTyping = "baca.pheads()",
        tags: typing.List[typing.Union[str, abjad.Tag, None]] = None,
        tweaks: abjad.IndexedTweakManagers = None,
    ) -> None:
        scoping.Command.__init__(
            self,
            deactivate=deactivate,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
            tags=tags,
        )
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        if do_not_test is not None:
            do_not_test = bool(do_not_test)
        self._do_not_test = do_not_test
        indicators_ = None
        if indicators is not None:
            if isinstance(indicators, collections.abc.Iterable):
                indicators_ = abjad.CyclicTuple(indicators)
            else:
                indicators_ = abjad.CyclicTuple([indicators])
        self._indicators = indicators_
        self._predicate = predicate
        if redundant is not None:
            redundant = bool(redundant)
        self._redundant = redundant
        self._validate_indexed_tweaks(tweaks)
        self._tweaks = tweaks

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        # TODO: externalize late import
        from .segmentmaker import SegmentMaker

        if argument is None:
            return
        if self.indicators is None:
            return
        if self.redundant is True:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        leaves = classes.Selection(argument).leaves()
        for i, leaf in enumerate(leaves):
            if self.predicate and not self.predicate(leaf):
                continue
            indicators = self.indicators[i]
            indicators = self._token_to_indicators(indicators)
            for indicator in indicators:
                self._apply_tweaks(indicator, self.tweaks)
                reapplied = self._remove_reapplied_wrappers(leaf, indicator)
                wrapper = abjad.attach(
                    indicator,
                    leaf,
                    context=self.context,
                    deactivate=self.deactivate,
                    do_not_test=self.do_not_test,
                    tag=self.tag.append("IndicatorCommand"),
                    wrapper=True,
                )
                if scoping.compare_persistent_indicators(indicator, reapplied):
                    status = "redundant"
                    SegmentMaker._treat_persistent_wrapper(
                        self.runtime["manifests"], wrapper, status
                    )

    ### PRIVATE METHODS ###

    @staticmethod
    def _token_to_indicators(token):
        result = []
        if not isinstance(token, (tuple, list)):
            token = [token]
        for item in token:
            if item is None:
                continue
            result.append(item)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> typing.Optional[str]:
        """
        Gets context name.
        """
        return self._context

    @property
    def do_not_test(self) -> typing.Optional[bool]:
        """
        Is true when attach does not test.
        """
        return self._do_not_test

    @property
    def indicators(self) -> typing.Optional[abjad.CyclicTuple]:
        r"""
        Gets indicators.
        """
        return self._indicators

    @property
    def predicate(self) -> typing.Optional[typing.Callable]:
        """
        Gets predicate.
        """
        return self._predicate

    @property
    def redundant(self) -> typing.Optional[bool]:
        """
        Is true when command is redundant.
        """
        return self._redundant

    @property
    def tweaks(self) -> typing.Optional[abjad.IndexedTweakManagers]:
        """
        Gets tweaks.
        """
        return self._tweaks


class InstrumentChangeCommand(IndicatorCommand):
    """
    Instrument change command.
    """

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Inserts ``selector`` output in container and sets part assignment.
        """
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if self.indicators is None:
            return
        first_leaf = abjad.inspect(argument).leaf(0)
        if first_leaf is not None:
            staff = abjad.inspect(first_leaf).parentage().get(abjad.Staff)
            instrument = self.indicators[0]
            assert isinstance(instrument, abjad.Instrument), repr(instrument)
            if not self.runtime["score_template"].allows_instrument(
                staff.name, instrument
            ):
                message = f"{staff.name} does not allow instrument:\n"
                message += f"  {instrument}"
                raise Exception(message)
        super()._call(argument)


class LabelCommand(scoping.Command):
    r"""
    Label command.
    """

    ### CLASS VARIABLES ##

    __slots__ = ("_expression",)

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        expression=None,
        map: abjad.SelectorTyping = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        scope: scoping.ScopeTyping = None,
        selector="baca.leaves()",
    ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
        )
        if expression is not None:
            assert isinstance(expression, abjad.Expression)
        self._expression = expression

    ### SPECIAL METHODS ###

    def _call(self, argument=None):
        """
        Calls command on ``argument``.

        Returns none.
        """
        if argument is None:
            return
        if self.expression is None:
            return
        if self.selector:
            argument = self.selector(argument)
        self.expression(argument)

    ### PUBLIC PROPERTIES ###

    @property
    def expression(self) -> typing.Optional[abjad.Expression]:
        """
        Gets expression.
        """
        return self._expression


class MetronomeMarkCommand(scoping.Command):
    """
    Metronome mark command.

    ..  container:: example

        >>> baca.MetronomeMarkCommand()
        MetronomeMarkCommand(selector=baca.leaf(0), tags=[])

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_key", "_redundant", "_tags")

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        deactivate: bool = None,
        key: typing.Union[
            str, indicators.Accelerando, indicators.Ritardando
        ] = None,
        map: abjad.SelectorTyping = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        redundant: bool = None,
        scope: scoping.ScopeTyping = None,
        selector: abjad.SelectorTyping = "baca.leaf(0)",
        tags: typing.List[typing.Union[str, abjad.Tag, None]] = None,
    ) -> None:
        scoping.Command.__init__(
            self,
            deactivate=deactivate,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
            tags=tags,
        )
        prototype = (str, indicators.Accelerando, indicators.Ritardando)
        if key is not None:
            assert isinstance(key, prototype), repr(key)
        self._key = key
        if redundant is not None:
            redundant = bool(redundant)
        self._redundant = redundant

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Applies command to result of selector called on ``argument``.
        """
        from .segmentmaker import SegmentMaker

        if argument is None:
            return
        if self.key is None:
            return
        if self.redundant is True:
            return
        if isinstance(self.key, str) and self.runtime["manifests"] is not None:
            metronome_marks = self.runtime["manifests"]["abjad.MetronomeMark"]
            indicator = metronome_marks.get(self.key)
            if indicator is None:
                raise Exception(f"can not find metronome mark {self.key!r}.")
        else:
            indicator = self.key
        if self.selector is not None:
            argument = self.selector(argument)
        if not argument:
            return
        leaf = classes.Selection(argument).leaf(0)
        reapplied = self._remove_reapplied_wrappers(leaf, indicator)
        wrapper = abjad.attach(
            indicator,
            leaf,
            deactivate=self.deactivate,
            tag=self.tag,
            wrapper=True,
        )
        if indicator == reapplied:
            SegmentMaker._treat_persistent_wrapper(
                self.runtime["manifests"], wrapper, "redundant"
            )

    ### PUBLIC PROPERTIES ###

    @property
    def key(
        self
    ) -> typing.Optional[
        typing.Union[str, indicators.Accelerando, indicators.Ritardando]
    ]:
        """
        Gets metronome mark key.
        """
        return self._key

    @property
    def redundant(self) -> typing.Optional[bool]:
        """
        Is true when command is redundant.
        """
        return self._redundant


class PartAssignmentCommand(scoping.Command):
    """
    Part assignment command.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_part_assignment",)

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        map: abjad.SelectorTyping = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        part_assignment: abjad.PartAssignment = None,
        scope: scoping.ScopeTyping = None,
        selector: abjad.SelectorTyping = "baca.leaves()",
    ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
        )
        if part_assignment is not None:
            if not isinstance(part_assignment, abjad.PartAssignment):
                message = "part_assignment must be part assignment"
                message += f" (not {part_assignment!r})."
                raise Exception(message)
        self._part_assignment = part_assignment

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Inserts ``selector`` output in container and sets part assignment.
        """
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        first_leaf = abjad.inspect(argument).leaf(0)
        if first_leaf is None:
            return
        voice = abjad.inspect(first_leaf).parentage().get(abjad.Voice, -1)
        if voice is not None and self.part_assignment is not None:
            if not self.runtime["score_template"].allows_part_assignment(
                voice.name, self.part_assignment
            ):
                message = f"{voice.name} does not allow"
                message += f" {self.part_assignment.section} part assignment:"
                message += f"\n  {self.part_assignment}"
                raise Exception(message)
        identifier = f"%*% {self.part_assignment!s}"
        container = abjad.Container(identifier=identifier)
        components = classes.Selection(argument).leaves().top()
        abjad.mutate(components).wrap(container)

    ### PRIVATE METHODS ###

    def _mutates_score(self):
        # return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def part_assignment(self) -> typing.Optional[abjad.PartAssignment]:
        """
        Gets part assignment.
        """
        return self._part_assignment


class VoltaCommand(scoping.Command):
    """
    Volta command.

    ..  container:: example

        >>> baca.VoltaCommand()
        VoltaCommand(tags=[])

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Applies command to result of selector called on ``argument``.
        """
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        leaves = classes.Selection(argument).leaves()
        container = abjad.Container()
        abjad.mutate(leaves).wrap(container)
        abjad.attach(abjad.Repeat(), container)

    ### PRIVATE METHODS ###

    def _mutates_score(self):
        return True


### FACTORY FUNCTIONS ###


def allow_octaves(
    *, selector: abjad.SelectorTyping = "baca.leaves()"
) -> IndicatorCommand:
    """
    Attaches ALLOW_OCTAVE tag.
    """
    return IndicatorCommand(
        indicators=[abjad.tags.ALLOW_OCTAVE], selector=selector
    )


def bar_extent_persistent(
    pair: abjad.NumberPair = None,
    *,
    after: bool = None,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    tag: typing.Optional[str] = "baca.bar_extent_persistent",
) -> IndicatorCommand:
    r"""
    Makes persistent bar-extent override.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.bar_extent_persistent((0, 0)),
        ...     baca.make_even_divisions(),
        ...     baca.staff_lines(1),
        ...     baca.staff_position(0),
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
                            \override Staff.BarLine.bar-extent = #'(0 . 0)                           %! EXPLICIT_PERSISTENT_OVERRIDE:_set_status_tag:baca.bar_extent_persistent:IndicatorCommand
                            \stopStaff                                                               %! EXPLICIT_STAFF_LINES:_set_status_tag:baca.staff_lines:IndicatorCommand
                            \once \override Staff.StaffSymbol.line-count = 1                         %! EXPLICIT_STAFF_LINES:_set_status_tag:baca.staff_lines:IndicatorCommand
                            \startStaff                                                              %! EXPLICIT_STAFF_LINES:_set_status_tag:baca.staff_lines:IndicatorCommand
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:_attach_color_literal(2)
                            b'8                                                                      %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            b'8                                                                      %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            b'8                                                                      %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            b'8                                                                      %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
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
    override = abjad.PersistentOverride(
        after=after,
        attribute="bar_extent",
        context="Staff",
        grob="bar_line",
        value=pair,
    )
    return IndicatorCommand(
        indicators=[override], selector=selector, tags=[tag]
    )


def bcps(
    bcps,
    *tweaks: abjad.IndexedTweakManager,
    bow_change_tweaks: abjad.IndexedTweakManagers = None,
    final_spanner: bool = None,
    helper: typing.Callable = None,
    selector: abjad.SelectorTyping = "baca.leaves()",
    tag: typing.Optional[str] = "baca.bcps",
) -> BCPCommand:
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
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
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
                                \override Script.staff-padding = #5.5                                    %! baca.script_staff_padding:OverrideCommand(1)
                                \override TextSpanner.staff-padding = #2.5                               %! baca.text_spanner_staff_padding:OverrideCommand(1)
                                e'8                                                                      %! baca.make_even_divisions
                                - \downbow                                                               %! baca.bcps:BCPCommand(6)
                                [                                                                        %! baca.make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions
                                - \upbow                                                                 %! baca.bcps:BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #3 #5                                      %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions
                                - \downbow                                                               %! baca.bcps:BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                ]                                                                        %! baca.make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #4 #5                                      %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                                e'8                                                                      %! baca.make_even_divisions
                                - \upbow                                                                 %! baca.bcps:BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                [                                                                        %! baca.make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #5 #5                                      %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions
                                - \downbow                                                               %! baca.bcps:BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions
                                - \upbow                                                                 %! baca.bcps:BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                ]                                                                        %! baca.make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #3 #5                                      %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                                f'8                                                                      %! baca.make_even_divisions
                                - \downbow                                                               %! baca.bcps:BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                [                                                                        %! baca.make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #4 #5                                      %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions
                                - \upbow                                                                 %! baca.bcps:BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #5 #5                                      %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions
                                - \downbow                                                               %! baca.bcps:BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                ]                                                                        %! baca.make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                                f'8                                                                      %! baca.make_even_divisions
                                - \upbow                                                                 %! baca.bcps:BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                [                                                                        %! baca.make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #3 #5                                      %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions
                                - \downbow                                                               %! baca.bcps:BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! baca.bcps:BCPCommand(2)
                                - \baca-bcp-spanner-right-text #4 #5                                     %! baca.bcps:BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps:BCPCommand(2)
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions
                                \bacaStopTextSpanBCP                                                     %! baca.bcps:BCPCommand(1)
                                ]                                                                        %! baca.make_even_divisions
                                \revert Script.staff-padding                                             %! baca.script_staff_padding:OverrideCommand(2)
                                \revert TextSpanner.staff-padding                                        %! baca.text_spanner_staff_padding:OverrideCommand(2)
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
    if final_spanner is not None:
        final_spanner = bool(final_spanner)
    return BCPCommand(
        bcps=bcps,
        bow_change_tweaks=bow_change_tweaks,
        final_spanner=final_spanner,
        helper=helper,
        selector=selector,
        tags=[tag],
        tweaks=tweaks,
    )


def color(selector: abjad.SelectorTyping = "baca.leaves()") -> ColorCommand:
    r"""
    Makes color command.

    :param selector: selector.

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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        \abjad-color-music #'red
                        r8
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
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
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
        ...     baca.color(baca.tuplets()[1:2].leaves()),
        ...     rmakers.unbeam(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
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
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return ColorCommand(selector=selector)


def container(
    identifier: str = None, *, selector: abjad.SelectorTyping = "baca.leaves()"
) -> ContainerCommand:
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
                    \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 1/2                                                                     %! _make_global_skips(1)
        <BLANKLINE>
                    % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                    \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 3/8                                                                     %! _make_global_skips(1)
        <BLANKLINE>
                    % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                    \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 1/2                                                                     %! _make_global_skips(1)
        <BLANKLINE>
                    % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                    \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 3/8                                                                     %! _make_global_skips(1)
                    \baca-bar-line-visible                                                       %! _attach_final_bar_line
                    \bar "|"                                                                     %! _attach_final_bar_line
        <BLANKLINE>
                    % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                        {   %*% ViolinI
        <BLANKLINE>
                            % [Music_Voice measure 1]                                            %! _comment_measure_numbers
                            e'2                                                                  %! baca.make_notes
        <BLANKLINE>
                            % [Music_Voice measure 2]                                            %! _comment_measure_numbers
                            f'4.                                                                 %! baca.make_notes
        <BLANKLINE>
                        }   %*% ViolinI
        <BLANKLINE>
                        {   %*% ViolinII
        <BLANKLINE>
                            % [Music_Voice measure 3]                                            %! _comment_measure_numbers
                            e'2                                                                  %! baca.make_notes
        <BLANKLINE>
                            % [Music_Voice measure 4]                                            %! _comment_measure_numbers
                            f'4.                                                                 %! baca.make_notes
        <BLANKLINE>
                        }   %*% ViolinII
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
    if identifier is not None:
        if not isinstance(identifier, str):
            message = f"identifier must be string (not {identifier!r})."
            raise Exception(message)
    return ContainerCommand(identifier=identifier, selector=selector)


def cross_staff(
    *,
    selector: abjad.SelectorTyping = "baca.phead(0)",
    tag: typing.Optional[str] = "baca.cross_staff",
) -> IndicatorCommand:
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
        ...     baca.cross_staff(selector=baca.pleaves()[-2:]),
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
        ...     do_not_color_unregistered_pitches=True,
        ...     score_template=accumulator.score_template,
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=accumulator.time_signatures,
        ...     )
        >>> accumulator.populate_segment_maker(maker)
        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.StringTrioScoreTemplate.__call__
            <<                                                                                       %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 5/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 5/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                \context MusicContext = "Music_Context"                                              %! baca.StringTrioScoreTemplate.__call__
                <<                                                                                   %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                    \context StringSectionStaffGroup = "String_Section_Staff_Group"                  %! baca.StringTrioScoreTemplate.__call__
                    <<                                                                               %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                        \tag Violin                                                                  %! baca.ScoreTemplate._attach_liypond_tag
                        \context ViolinMusicStaff = "Violin_Music_Staff"                             %! baca.StringTrioScoreTemplate.__call__
                        {                                                                            %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                            \context ViolinMusicVoice = "Violin_Music_Voice"                         %! baca.StringTrioScoreTemplate.__call__
                            {                                                                        %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                                {
            <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                        % [Violin_Music_Voice measure 1]                             %! _comment_measure_numbers
                                        \override Stem.direction = #up                               %! baca.stem_up:OverrideCommand(1)
                                        \clef "treble"                                               %! DEFAULT_CLEF:_set_status_tag:abjad.ScoreTemplate.attach_defaults
                                        \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                                    %@% \override ViolinMusicStaff.Clef.color = ##f                  %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                        \set ViolinMusicStaff.forceClef = ##t                        %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):abjad.ScoreTemplate.attach_defaults
                                        a'8
                                        ^ \baca-default-indicator-markup "(Violin)"                  %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                                        \override ViolinMusicStaff.Clef.color = #(x11-color 'violet) %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                                        b'8
            <BLANKLINE>
                                        c''8
            <BLANKLINE>
                                        d''8
            <BLANKLINE>
                                        e''8
                                        \revert Stem.direction                                       %! baca.stem_up:OverrideCommand(2)
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                }
            <BLANKLINE>
                                {
            <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                        % [Violin_Music_Voice measure 2]                             %! _comment_measure_numbers
                                        ef''!8
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                }
            <BLANKLINE>
                                <<                                                                   %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    \context Voice = "Violin_Music_Voice"                            %! PHANTOM:_make_multimeasure_rest_container
                                    {                                                                %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                        % [Violin_Music_Voice measure 3]                             %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                        \baca-invisible-music                                        %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                        c'1 * 1/4                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    }                                                                %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    \context Voice = "Violin_Rest_Voice"                             %! PHANTOM:_make_multimeasure_rest_container
                                    {                                                                %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                        % [Violin_Rest_Voice measure 3]                              %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                        \once \override Score.TimeSignature.X-extent = ##f           %! PHANTOM:_style_phantom_measures(6)
                                        \once \override MultiMeasureRest.transparent = ##t           %! PHANTOM:_style_phantom_measures(7)
                                        \stopStaff                                                   %! PHANTOM:_style_phantom_measures(8)
                                        \once \override Staff.StaffSymbol.transparent = ##t          %! PHANTOM:_style_phantom_measures(8)
                                        \startStaff                                                  %! PHANTOM:_style_phantom_measures(8)
                                        R1 * 1/4                                                     %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    }                                                                %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                >>                                                                   %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                            }                                                                        %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                        }                                                                            %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                        \tag Viola                                                                   %! baca.ScoreTemplate._attach_liypond_tag
                        \context ViolaMusicStaff = "Viola_Music_Staff"                               %! baca.StringTrioScoreTemplate.__call__
                        {                                                                            %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                            \context ViolaMusicVoice = "Viola_Music_Voice"                           %! baca.StringTrioScoreTemplate.__call__
                            {                                                                        %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                                {
            <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                        % [Viola_Music_Voice measure 1]                              %! _comment_measure_numbers
                                        \override Stem.direction = #up                               %! baca.stem_up:OverrideCommand(1)
                                        \clef "alto"                                                 %! DEFAULT_CLEF:_set_status_tag:abjad.ScoreTemplate.attach_defaults
                                        \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                                    %@% \override ViolaMusicStaff.Clef.color = ##f                   %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                        \set ViolaMusicStaff.forceClef = ##t                         %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):abjad.ScoreTemplate.attach_defaults
                                        c'8
                                        ^ \baca-default-indicator-markup "(Viola)"                   %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                                        \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)  %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                                        d'8
            <BLANKLINE>
                                        e'8
            <BLANKLINE>
                                        \crossStaff                                                  %! baca.cross_staff:IndicatorCommand
                                        f'8
            <BLANKLINE>
                                        \crossStaff                                                  %! baca.cross_staff:IndicatorCommand
                                        g'8
                                        \revert Stem.direction                                       %! baca.stem_up:OverrideCommand(2)
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                }
            <BLANKLINE>
                                <<                                                                   %! _make_multimeasure_rest_container
            <BLANKLINE>
                                    \context Voice = "Viola_Music_Voice"                             %! _make_multimeasure_rest_container
                                    {                                                                %! _make_multimeasure_rest_container
            <BLANKLINE>
                                        % [Viola_Music_Voice measure 2]                              %! _comment_measure_numbers
                                        \baca-invisible-music                                        %! _make_multimeasure_rest_container
                                        c'1 * 1/8                                                    %! _make_multimeasure_rest_container
            <BLANKLINE>
                                    }                                                                %! _make_multimeasure_rest_container
            <BLANKLINE>
                                    \context Voice = "Viola_Rest_Voice"                              %! _make_multimeasure_rest_container
                                    {                                                                %! _make_multimeasure_rest_container
            <BLANKLINE>
                                        % [Viola_Rest_Voice measure 2]                               %! _comment_measure_numbers
                                        R1 * 1/8                                                     %! _make_multimeasure_rest_container
            <BLANKLINE>
                                    }                                                                %! _make_multimeasure_rest_container
            <BLANKLINE>
                                >>                                                                   %! _make_multimeasure_rest_container
            <BLANKLINE>
                                <<                                                                   %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    \context Voice = "Viola_Music_Voice"                             %! PHANTOM:_make_multimeasure_rest_container
                                    {                                                                %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                        % [Viola_Music_Voice measure 3]                              %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                        \baca-invisible-music                                        %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                        R1 * 1/4                                                     %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    }                                                                %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    \context Voice = "Viola_Rest_Voice"                              %! PHANTOM:_make_multimeasure_rest_container
                                    {                                                                %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                        % [Viola_Rest_Voice measure 3]                               %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                        \once \override Score.TimeSignature.X-extent = ##f           %! PHANTOM:_style_phantom_measures(6)
                                        \once \override MultiMeasureRest.transparent = ##t           %! PHANTOM:_style_phantom_measures(7)
                                        \stopStaff                                                   %! PHANTOM:_style_phantom_measures(8)
                                        \once \override Staff.StaffSymbol.transparent = ##t          %! PHANTOM:_style_phantom_measures(8)
                                        \startStaff                                                  %! PHANTOM:_style_phantom_measures(8)
                                        R1 * 1/4                                                     %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    }                                                                %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                >>                                                                   %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                            }                                                                        %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                        }                                                                            %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                        \tag Cello                                                                   %! baca.ScoreTemplate._attach_liypond_tag
                        \context CelloMusicStaff = "Cello_Music_Staff"                               %! baca.StringTrioScoreTemplate.__call__
                        {                                                                            %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                            \context CelloMusicVoice = "Cello_Music_Voice"                           %! baca.StringTrioScoreTemplate.__call__
                            {                                                                        %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                                % [Cello_Music_Voice measure 1]                                      %! _comment_measure_numbers
                                \clef "bass"                                                         %! DEFAULT_CLEF:_set_status_tag:abjad.ScoreTemplate.attach_defaults
                                \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                            %@% \override CelloMusicStaff.Clef.color = ##f                           %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                \set CelloMusicStaff.forceClef = ##t                                 %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):abjad.ScoreTemplate.attach_defaults
                                R1 * 5/8                                                             %! _call_rhythm_commands
                                ^ \baca-default-indicator-markup "(Cello)"                           %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                                \override CelloMusicStaff.Clef.color = #(x11-color 'violet)          %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                                % [Cello_Music_Voice measure 2]                                      %! _comment_measure_numbers
                                R1 * 1/8                                                             %! _call_rhythm_commands
            <BLANKLINE>
                                <<                                                                   %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    \context Voice = "Cello_Music_Voice"                             %! PHANTOM:_make_multimeasure_rest_container
                                    {                                                                %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                        % [Cello_Music_Voice measure 3]                              %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                        \baca-invisible-music                                        %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                        R1 * 1/4                                                     %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    }                                                                %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    \context Voice = "Cello_Rest_Voice"                              %! PHANTOM:_make_multimeasure_rest_container
                                    {                                                                %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                        % [Cello_Rest_Voice measure 3]                               %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                        \once \override Score.TimeSignature.X-extent = ##f           %! PHANTOM:_style_phantom_measures(6)
                                        \once \override MultiMeasureRest.transparent = ##t           %! PHANTOM:_style_phantom_measures(7)
                                        \stopStaff                                                   %! PHANTOM:_style_phantom_measures(8)
                                        \once \override Staff.StaffSymbol.transparent = ##t          %! PHANTOM:_style_phantom_measures(8)
                                        \startStaff                                                  %! PHANTOM:_style_phantom_measures(8)
                                        R1 * 1/4                                                     %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    }                                                                %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                >>                                                                   %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                            }                                                                        %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                        }                                                                            %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                    >>                                                                               %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.StringTrioScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.StringTrioScoreTemplate.__call__

    """
    return IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\crossStaff")],
        selector=selector,
        tags=[tag],
    )


def dynamic_down(
    *,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    tag: typing.Optional[str] = "baca.dynamic_down",
) -> IndicatorCommand:
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
        ...     baca.dynamic('f', selector=baca.tuplets()[1:2].phead(0)),
        ...     baca.dynamic_down(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        \dynamicDown                                                                 %! baca.dynamic_down:IndicatorCommand
                        r8
                        c'16
                        \p                                                                           %! baca.dynamic:IndicatorCommand
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
                        \f                                                                           %! baca.dynamic:IndicatorCommand
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
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\dynamicDown")],
        selector=selector,
        tags=[tag],
    )


def dynamic_up(
    *,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    tag: typing.Optional[str] = "baca.dynamic_down",
) -> IndicatorCommand:
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
        ...     baca.dynamic('f', selector=baca.tuplets()[1:2].phead(0)),
        ...     baca.dynamic_up(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        \dynamicUp                                                                   %! baca.dynamic_down:IndicatorCommand
                        r8
                        c'16
                        \p                                                                           %! baca.dynamic:IndicatorCommand
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
                        \f                                                                           %! baca.dynamic:IndicatorCommand
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
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\dynamicUp")],
        selector=selector,
        tags=[tag],
    )


def edition(
    not_parts: typing.Union[str, abjad.Markup, IndicatorCommand],
    only_parts: typing.Union[str, abjad.Markup, IndicatorCommand],
) -> scoping.Suite:
    """
    Makes not-parts / only-parts markup suite.
    """
    if isinstance(not_parts, (str, abjad.Markup)):
        not_parts = markup(not_parts)
    assert isinstance(not_parts, IndicatorCommand)
    not_parts_ = scoping.not_parts(not_parts)
    if isinstance(only_parts, (str, abjad.Markup)):
        only_parts = markup(only_parts)
    assert isinstance(only_parts, IndicatorCommand)
    only_parts_ = scoping.only_parts(only_parts)
    return scoping.suite(not_parts_, only_parts_)


def finger_pressure_transition(
    *,
    selector: abjad.SelectorTyping = "baca.tleaves()",
    right_broken: bool = None,
    tag: typing.Optional[str] = "baca.finger_pressure_transition",
) -> GlissandoCommand:
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
        ...     baca.finger_pressure_transition(selector=baca.notes()[:2]),
        ...     baca.finger_pressure_transition(selector=baca.notes()[2:]),
        ...     baca.make_notes(),
        ...     baca.note_head_style_harmonic(selector=baca.note(0)),
        ...     baca.note_head_style_harmonic(selector=baca.note(2)),
        ...     baca.pitch('C5'),
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
                            \once \override NoteHead.style = #'harmonic                              %! baca.note_head_style_harmonic:OverrideCommand(1)
                            c''2                                                                     %! baca.make_notes
                            - \tweak arrow-length #2                                                 %! baca.finger_pressure_transition
                            - \tweak arrow-width #0.5                                                %! baca.finger_pressure_transition
                            - \tweak bound-details.right.arrow ##t                                   %! baca.finger_pressure_transition
                            - \tweak thickness #3                                                    %! baca.finger_pressure_transition
                            \glissando                                                               %! baca.finger_pressure_transition
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            c''4.                                                                    %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            \once \override NoteHead.style = #'harmonic                              %! baca.note_head_style_harmonic:OverrideCommand(1)
                            c''2                                                                     %! baca.make_notes
                            - \tweak arrow-length #2                                                 %! baca.finger_pressure_transition
                            - \tweak arrow-width #0.5                                                %! baca.finger_pressure_transition
                            - \tweak bound-details.right.arrow ##t                                   %! baca.finger_pressure_transition
                            - \tweak thickness #3                                                    %! baca.finger_pressure_transition
                            \glissando                                                               %! baca.finger_pressure_transition
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            c''4.                                                                    %! baca.make_notes
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
    return GlissandoCommand(
        allow_repeats=True,
        right_broken=right_broken,
        selector=selector,
        tags=[tag],
        tweaks=(
            abjad.tweak(2).arrow_length,
            abjad.tweak(0.5).arrow_width,
            abjad.tweak(True).bound_details__right__arrow,
            abjad.tweak(3).thickness,
        ),
    )


def flat_glissando(
    pitch,
    *tweaks,
    hide_middle_stems=None,
    left_broken=None,
    right_broken=None,
    right_broken_show_next=None,
    rleak=None,
    selector="baca.pleaves()",
    stop_pitch=None,
):
    """
    Makes flat glissando.
    """
    # for selector evaluation
    import baca

    if isinstance(selector, str):
        selector = eval(selector)
    if stop_pitch is not None:
        assert pitch is not None
    if rleak:
        selector = selector.rleak()
    commands = []
    command = glissando(
        *tweaks,
        allow_repeats=True,
        allow_ties=True,
        hide_middle_note_heads=True,
        hide_middle_stems=hide_middle_stems,
        left_broken=left_broken,
        right_broken=right_broken,
        right_broken_show_next=right_broken_show_next,
        selector=selector,
    )
    commands.append(command)
    command = untie(selector.leaves())
    commands.append(command)
    if pitch is not None and stop_pitch is None:
        command = pitchcommands.pitch(pitch, selector=selector)
        commands.append(command)
    elif pitch is not None and stop_pitch is not None:
        command = pitchcommands.interpolate_staff_positions(
            pitch, stop_pitch, selector=selector
        )
        commands.append(command)
    return scoping.suite(*commands)


def glissando(
    *tweaks: abjad.IndexedTweakManager,
    allow_repeats: bool = None,
    allow_ties: bool = None,
    hide_middle_note_heads: bool = None,
    hide_middle_stems: bool = None,
    left_broken: bool = None,
    map: abjad.SelectorTyping = None,
    right_broken: bool = None,
    right_broken_show_next: bool = None,
    selector: abjad.SelectorTyping = "baca.tleaves()",
    style: str = None,
    tag: typing.Optional[str] = "baca.glissando",
    zero_padding: bool = None,
) -> GlissandoCommand:
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
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                            e'8                                                                      %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            d''8                                                                     %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            g'8                                                                      %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            f''8                                                                     %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            d''8                                                                     %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            g'8                                                                      %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            f''8                                                                     %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            d''8                                                                     %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
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
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                            e'8                                                                      %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            d''8                                                                     %! baca.make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            g'8                                                                      %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca.make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            d''8                                                                     %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            f''8                                                                     %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            d''8                                                                     %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
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
        ...         abjad.tweak('red').color,
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
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                            e'8                                                                      %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
                            - \tweak color #red                                                      %! baca.glissando
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            d''8                                                                     %! baca.make_even_divisions
                            - \tweak color #red                                                      %! baca.glissando
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions
                            - \tweak color #red                                                      %! baca.glissando
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
                            - \tweak color #red                                                      %! baca.glissando
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            g'8                                                                      %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
                            - \tweak color #red                                                      %! baca.glissando
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            f''8                                                                     %! baca.make_even_divisions
                            - \tweak color #red                                                      %! baca.glissando
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
                            - \tweak color #red                                                      %! baca.glissando
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            d''8                                                                     %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
                            - \tweak color #red                                                      %! baca.glissando
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions
                            - \tweak color #red                                                      %! baca.glissando
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions
                            - \tweak color #red                                                      %! baca.glissando
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            g'8                                                                      %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
                            - \tweak color #red                                                      %! baca.glissando
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            f''8                                                                     %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
                            - \tweak color #red                                                      %! baca.glissando
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions
                            - \tweak color #red                                                      %! baca.glissando
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            d''8                                                                     %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
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
        ...         (abjad.tweak('red').color, 0),
        ...         (abjad.tweak('red').color, -1),
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
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                            e'8                                                                      %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
                            - \tweak color #red                                                      %! baca.glissando
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            d''8                                                                     %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            g'8                                                                      %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            f''8                                                                     %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            d''8                                                                     %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            g'8                                                                      %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            f''8                                                                     %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions
                            - \tweak color #red                                                      %! baca.glissando
                            \glissando                                                               %! baca.glissando
            <BLANKLINE>
                            d''8                                                                     %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
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
    return GlissandoCommand(
        allow_repeats=allow_repeats,
        allow_ties=allow_ties,
        hide_middle_note_heads=hide_middle_note_heads,
        hide_middle_stems=hide_middle_stems,
        left_broken=left_broken,
        map=map,
        right_broken=right_broken,
        right_broken_show_next=right_broken_show_next,
        selector=selector,
        tags=[tag],
        tweaks=tweaks,
        zero_padding=zero_padding,
    )


def global_fermata(
    description: str = None,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    tag: typing.Optional[str] = "baca.global_fermata",
) -> GlobalFermataCommand:
    """
    Attaches global fermata.
    """
    return GlobalFermataCommand(
        description=description, selector=selector, tags=[tag]
    )


def instrument(
    instrument: abjad.Instrument,
    *,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    tag: typing.Optional[str] = "baca.instrument",
) -> InstrumentChangeCommand:
    """
    Makes instrument change command.
    """
    if not isinstance(instrument, abjad.Instrument):
        message = f"instrument must be instrument (not {instrument!r})."
        raise Exception(message)
    return InstrumentChangeCommand(
        indicators=[instrument], selector=selector, tags=[tag]
    )


def invisible_music(
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    tag: typing.Optional[str] = "baca.invisible_music",
) -> IndicatorCommand:
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
                            c''2                                                                     %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            \baca-invisible-music                                                    %! baca.invisible_music:IndicatorCommand
                            c''4.                                                                    %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            \baca-invisible-music                                                    %! baca.invisible_music:IndicatorCommand
                            c''2                                                                     %! baca.make_notes
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            c''4.                                                                    %! baca.make_notes
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
    return IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\baca-invisible-music")],
        selector=selector,
        tags=[tag],
    )


def label(
    expression: abjad.Expression,
    *,
    selector: abjad.SelectorTyping = "baca.leaves()",
) -> LabelCommand:
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
        ...     baca.label(abjad.label().with_pitches(locale='us')),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
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
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return LabelCommand(expression=expression, selector=selector)


def markup(
    argument: typing.Union[str, abjad.Markup],
    *tweaks: abjad.LilyPondTweakManager,
    boxed: bool = None,
    # typehinting is weird for some reason
    direction=abjad.Up,
    literal: bool = False,
    map: abjad.SelectorTyping = None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    selector: abjad.SelectorTyping = "baca.pleaf(0)",
    tag: typing.Optional[str] = "baca.markup",
) -> IndicatorCommand:
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TupletBracket.outside-staff-priority = #1000                       %! baca.tuplet_bracket_outside_staff_priority:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        c'16
                        ^ \markup { "più mosso" }                                                    %! baca.markup:IndicatorCommand
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
                        \revert TupletBracket.outside-staff-priority                                 %! baca.tuplet_bracket_outside_staff_priority:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TupletBracket.outside-staff-priority = #1000                       %! baca.tuplet_bracket_outside_staff_priority:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        c'16
                        ^ \markup { \baca-triple-diamond-markup }                                    %! baca.markup:IndicatorCommand
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
                        \revert TupletBracket.outside-staff-priority                                 %! baca.tuplet_bracket_outside_staff_priority:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
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
    if boxed:
        markup = markup.box().override(("box-padding", 0.5))
    prototype = (str, abjad.Expression)
    if selector is not None and not isinstance(selector, prototype):
        message = f"selector must be string or expression"
        message += f" (not {selector!r})."
        raise Exception(message)
    selector = selector or "baca.phead(0)"
    return IndicatorCommand(
        indicators=[markup],
        map=map,
        match=match,
        measures=measures,
        selector=selector,
        tags=[tag],
        tweaks=tweaks,
    )


def metronome_mark(
    key: typing.Union[str, indicators.Accelerando, indicators.Ritardando],
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    redundant: bool = None,
) -> typing.Optional[MetronomeMarkCommand]:
    """
    Attaches metronome mark matching ``key`` metronome mark manifest.
    """
    if redundant is True:
        return None
    return MetronomeMarkCommand(
        key=key, redundant=redundant, selector=selector
    )


def parts(
    part_assignment: abjad.PartAssignment,
    *,
    selector: abjad.SelectorTyping = "baca.leaves()",
) -> PartAssignmentCommand:
    r"""
    Inserts ``selector`` output in container and sets part assignment.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.StringTrioScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Violin_Music_Voice',
        ...     baca.make_notes(),
        ...     baca.parts(abjad.PartAssignment('Violin')),
        ...     baca.pitch('E4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        >>> abjad.f(lilypond_file[abjad.Score], strict=89)
        <BLANKLINE>
        \context Score = "Score"                                                                 %! baca.StringTrioScoreTemplate.__call__
        <<                                                                                       %! baca.StringTrioScoreTemplate.__call__
        <BLANKLINE>
            \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
            <<                                                                                   %! abjad.ScoreTemplate._make_global_context
        <BLANKLINE>
                \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                {                                                                                %! abjad.ScoreTemplate._make_global_context
        <BLANKLINE>
                    % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                    \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 1/2                                                                     %! _make_global_skips(1)
        <BLANKLINE>
                    % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                    \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 3/8                                                                     %! _make_global_skips(1)
        <BLANKLINE>
                    % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                    \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 1/2                                                                     %! _make_global_skips(1)
        <BLANKLINE>
                    % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                    \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 3/8                                                                     %! _make_global_skips(1)
                    \baca-bar-line-visible                                                       %! _attach_final_bar_line
                    \bar "|"                                                                     %! _attach_final_bar_line
        <BLANKLINE>
                    % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
            \context MusicContext = "Music_Context"                                              %! baca.StringTrioScoreTemplate.__call__
            <<                                                                                   %! baca.StringTrioScoreTemplate.__call__
        <BLANKLINE>
                \context StringSectionStaffGroup = "String_Section_Staff_Group"                  %! baca.StringTrioScoreTemplate.__call__
                <<                                                                               %! baca.StringTrioScoreTemplate.__call__
        <BLANKLINE>
                    \tag Violin                                                                  %! baca.ScoreTemplate._attach_liypond_tag
                    \context ViolinMusicStaff = "Violin_Music_Staff"                             %! baca.StringTrioScoreTemplate.__call__
                    {                                                                            %! baca.StringTrioScoreTemplate.__call__
        <BLANKLINE>
                        \context ViolinMusicVoice = "Violin_Music_Voice"                         %! baca.StringTrioScoreTemplate.__call__
                        {                                                                        %! baca.StringTrioScoreTemplate.__call__
        <BLANKLINE>
                            {   %*% PartAssignment('Violin')
        <BLANKLINE>
                                % [Violin_Music_Voice measure 1]                                 %! _comment_measure_numbers
                                \clef "treble"                                                   %! DEFAULT_CLEF:_set_status_tag:abjad.ScoreTemplate.attach_defaults
                                \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                            %@% \override ViolinMusicStaff.Clef.color = ##f                      %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                \set ViolinMusicStaff.forceClef = ##t                            %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):abjad.ScoreTemplate.attach_defaults
                                e'2                                                              %! baca.make_notes
                                ^ \baca-default-indicator-markup "(Violin)"                      %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                                \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)     %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
        <BLANKLINE>
                                % [Violin_Music_Voice measure 2]                                 %! _comment_measure_numbers
                                e'4.                                                             %! baca.make_notes
        <BLANKLINE>
                                % [Violin_Music_Voice measure 3]                                 %! _comment_measure_numbers
                                e'2                                                              %! baca.make_notes
        <BLANKLINE>
                                % [Violin_Music_Voice measure 4]                                 %! _comment_measure_numbers
                                e'4.                                                             %! baca.make_notes
        <BLANKLINE>
                            }   %*% PartAssignment('Violin')
        <BLANKLINE>
                            <<                                                                   %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                                \context Voice = "Violin_Music_Voice"                            %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                                    % [Violin_Music_Voice measure 5]                             %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \baca-invisible-music                                        %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                    c'1 * 1/4                                                    %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                                }                                                                %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                                \context Voice = "Violin_Rest_Voice"                             %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                                    % [Violin_Rest_Voice measure 5]                              %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \once \override Score.TimeSignature.X-extent = ##f           %! PHANTOM:_style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t           %! PHANTOM:_style_phantom_measures(7)
                                    \stopStaff                                                   %! PHANTOM:_style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t          %! PHANTOM:_style_phantom_measures(8)
                                    \startStaff                                                  %! PHANTOM:_style_phantom_measures(8)
                                    R1 * 1/4                                                     %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                                }                                                                %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                            >>                                                                   %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                        }                                                                        %! baca.StringTrioScoreTemplate.__call__
        <BLANKLINE>
                    }                                                                            %! baca.StringTrioScoreTemplate.__call__
        <BLANKLINE>
                    \tag Viola                                                                   %! baca.ScoreTemplate._attach_liypond_tag
                    \context ViolaMusicStaff = "Viola_Music_Staff"                               %! baca.StringTrioScoreTemplate.__call__
                    {                                                                            %! baca.StringTrioScoreTemplate.__call__
        <BLANKLINE>
                        \context ViolaMusicVoice = "Viola_Music_Voice"                           %! baca.StringTrioScoreTemplate.__call__
                        {                                                                        %! baca.StringTrioScoreTemplate.__call__
        <BLANKLINE>
                            % [Viola_Music_Voice measure 1]                                      %! _comment_measure_numbers
                            \clef "alto"                                                         %! DEFAULT_CLEF:_set_status_tag:abjad.ScoreTemplate.attach_defaults
                            \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                        %@% \override ViolaMusicStaff.Clef.color = ##f                           %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                            \set ViolaMusicStaff.forceClef = ##t                                 %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):abjad.ScoreTemplate.attach_defaults
                            R1 * 4/8                                                             %! _call_rhythm_commands
                            ^ \baca-default-indicator-markup "(Viola)"                           %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                            \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)          %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
        <BLANKLINE>
                            % [Viola_Music_Voice measure 2]                                      %! _comment_measure_numbers
                            R1 * 3/8                                                             %! _call_rhythm_commands
        <BLANKLINE>
                            % [Viola_Music_Voice measure 3]                                      %! _comment_measure_numbers
                            R1 * 4/8                                                             %! _call_rhythm_commands
        <BLANKLINE>
                            % [Viola_Music_Voice measure 4]                                      %! _comment_measure_numbers
                            R1 * 3/8                                                             %! _call_rhythm_commands
        <BLANKLINE>
                            <<                                                                   %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                                \context Voice = "Viola_Music_Voice"                             %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                                    % [Viola_Music_Voice measure 5]                              %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \baca-invisible-music                                        %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                    R1 * 1/4                                                     %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                                }                                                                %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                                \context Voice = "Viola_Rest_Voice"                              %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                                    % [Viola_Rest_Voice measure 5]                               %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \once \override Score.TimeSignature.X-extent = ##f           %! PHANTOM:_style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t           %! PHANTOM:_style_phantom_measures(7)
                                    \stopStaff                                                   %! PHANTOM:_style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t          %! PHANTOM:_style_phantom_measures(8)
                                    \startStaff                                                  %! PHANTOM:_style_phantom_measures(8)
                                    R1 * 1/4                                                     %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                                }                                                                %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                            >>                                                                   %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                        }                                                                        %! baca.StringTrioScoreTemplate.__call__
        <BLANKLINE>
                    }                                                                            %! baca.StringTrioScoreTemplate.__call__
        <BLANKLINE>
                    \tag Cello                                                                   %! baca.ScoreTemplate._attach_liypond_tag
                    \context CelloMusicStaff = "Cello_Music_Staff"                               %! baca.StringTrioScoreTemplate.__call__
                    {                                                                            %! baca.StringTrioScoreTemplate.__call__
        <BLANKLINE>
                        \context CelloMusicVoice = "Cello_Music_Voice"                           %! baca.StringTrioScoreTemplate.__call__
                        {                                                                        %! baca.StringTrioScoreTemplate.__call__
        <BLANKLINE>
                            % [Cello_Music_Voice measure 1]                                      %! _comment_measure_numbers
                            \clef "bass"                                                         %! DEFAULT_CLEF:_set_status_tag:abjad.ScoreTemplate.attach_defaults
                            \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                        %@% \override CelloMusicStaff.Clef.color = ##f                           %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                            \set CelloMusicStaff.forceClef = ##t                                 %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):abjad.ScoreTemplate.attach_defaults
                            R1 * 4/8                                                             %! _call_rhythm_commands
                            ^ \baca-default-indicator-markup "(Cello)"                           %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                            \override CelloMusicStaff.Clef.color = #(x11-color 'violet)          %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
        <BLANKLINE>
                            % [Cello_Music_Voice measure 2]                                      %! _comment_measure_numbers
                            R1 * 3/8                                                             %! _call_rhythm_commands
        <BLANKLINE>
                            % [Cello_Music_Voice measure 3]                                      %! _comment_measure_numbers
                            R1 * 4/8                                                             %! _call_rhythm_commands
        <BLANKLINE>
                            % [Cello_Music_Voice measure 4]                                      %! _comment_measure_numbers
                            R1 * 3/8                                                             %! _call_rhythm_commands
        <BLANKLINE>
                            <<                                                                   %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                                \context Voice = "Cello_Music_Voice"                             %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                                    % [Cello_Music_Voice measure 5]                              %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \baca-invisible-music                                        %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                    R1 * 1/4                                                     %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                                }                                                                %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                                \context Voice = "Cello_Rest_Voice"                              %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                                    % [Cello_Rest_Voice measure 5]                               %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \once \override Score.TimeSignature.X-extent = ##f           %! PHANTOM:_style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t           %! PHANTOM:_style_phantom_measures(7)
                                    \stopStaff                                                   %! PHANTOM:_style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t          %! PHANTOM:_style_phantom_measures(8)
                                    \startStaff                                                  %! PHANTOM:_style_phantom_measures(8)
                                    R1 * 1/4                                                     %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                                }                                                                %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                            >>                                                                   %! PHANTOM:_make_multimeasure_rest_container
        <BLANKLINE>
                        }                                                                        %! baca.StringTrioScoreTemplate.__call__
        <BLANKLINE>
                    }                                                                            %! baca.StringTrioScoreTemplate.__call__
        <BLANKLINE>
                >>                                                                               %! baca.StringTrioScoreTemplate.__call__
        <BLANKLINE>
            >>                                                                                   %! baca.StringTrioScoreTemplate.__call__
        <BLANKLINE>
        >>                                                                                       %! baca.StringTrioScoreTemplate.__call__

    ..  container:: example exception

        Raises exception when voice does not allow part assignment:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.StringTrioScoreTemplate(),
        ...     test_container_identifiers=True,
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> part_assignment = abjad.PartAssignment('Flute')

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
            abjad.PartAssignment('Flute')

    """
    if not isinstance(part_assignment, abjad.PartAssignment):
        message = "part_assignment must be part assignment"
        message += f" (not {part_assignment!r})."
        raise Exception(message)
    return PartAssignmentCommand(
        part_assignment=part_assignment, selector=selector
    )


def one_voice(
    *,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    tag: typing.Optional[str] = "baca.one_voice",
) -> IndicatorCommand:
    r"""
    Makes LilyPond ``\oneVoice`` command.
    """
    literal = abjad.LilyPondLiteral(r"\oneVoice")
    return IndicatorCommand(
        indicators=[literal], selector=selector, tags=[tag]
    )


def previous_metadata(path: str) -> abjad.OrderedDict:
    """
    Gets previous segment metadata before ``path``.
    """
    # reproduces abjad.Path.get_previous_path()
    # because Travis isn't configured for scores-directory calculations
    definition_py = abjad.Path(path)
    segment = abjad.Path(definition_py).parent
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


def untie(selector: abjad.SelectorTyping) -> DetachCommand:
    r"""
    Makes (repeat-)tie detach command.
    """
    return DetachCommand([abjad.Tie, abjad.RepeatTie], selector=selector)


def voice_four(
    *,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    tag: typing.Optional[str] = "baca.voice_four",
) -> IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceFour`` command.
    """
    literal = abjad.LilyPondLiteral(r"\voiceFour")
    return IndicatorCommand(
        indicators=[literal], selector=selector, tags=[tag]
    )


def voice_one(
    *,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    tag: typing.Optional[str] = "baca.voice_one",
) -> IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceOne`` command.
    """
    literal = abjad.LilyPondLiteral(r"\voiceOne")
    return IndicatorCommand(
        indicators=[literal], selector=selector, tags=[tag]
    )


def voice_three(
    *,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    tag: typing.Optional[str] = "baca.voice_three",
) -> IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceThree`` command.
    """
    literal = abjad.LilyPondLiteral(r"\voiceThree")
    return IndicatorCommand(
        indicators=[literal], selector=selector, tags=[tag]
    )


def voice_two(
    *,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    tag: typing.Optional[str] = "baca.voice_two",
) -> IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceTwo`` command.
    """
    literal = abjad.LilyPondLiteral(r"\voiceTwo")
    return IndicatorCommand(
        indicators=[literal], selector=selector, tags=[tag]
    )


def volta(*, selector: abjad.SelectorTyping = "baca.leaves()") -> VoltaCommand:
    r"""
    Makes volta container and extends container with ``selector`` output.

    ..  container:: example

        Wraps measures 2 and 3 in volta container:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     ('Music_Voice', (1, 3)),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.rhythm(
        ...         rmakers.talea([1, 1, 1, -1], 8),
        ...         rmakers.beam(),
        ...         rmakers.extract_trivial(),
        ...     ),
        ... )

        >>> maker(
        ...     ('Global_Skips', (2, 3)),
        ...     baca.volta(),
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
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        \repeat volta 2
                        {
            <BLANKLINE>
                            % [Global_Skips measure 2]                                               %! _comment_measure_numbers
                            \time 3/8                                                                %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                        %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                 %! _make_global_skips(1)
            <BLANKLINE>
                            % [Global_Skips measure 3]                                               %! _comment_measure_numbers
                            \time 4/8                                                                %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                        %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                 %! _make_global_skips(1)
            <BLANKLINE>
                        }
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
                            ]
            <BLANKLINE>
                            r8
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            e''8
                            [
            <BLANKLINE>
                            g'8
            <BLANKLINE>
                            f''8
                            ]
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            r8
            <BLANKLINE>
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
                            ]
            <BLANKLINE>
                            <<                                                                       %! _make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! _make_multimeasure_rest_container
                                {                                                                    %! _make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Music_Voice measure 4]                                        %! _comment_measure_numbers
                                    \baca-invisible-music                                            %! _make_multimeasure_rest_container
                                    c'1 * 3/8                                                        %! _make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! _make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! _make_multimeasure_rest_container
                                {                                                                    %! _make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Rest_Voice measure 4]                                         %! _comment_measure_numbers
                                    R1 * 3/8                                                         %! _make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! _make_multimeasure_rest_container
            <BLANKLINE>
                            >>                                                                       %! _make_multimeasure_rest_container
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \baca-invisible-music                                            %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                    R1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
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
    return VoltaCommand(selector=selector)
