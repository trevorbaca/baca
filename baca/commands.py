import abjad
import collections
import typing
from . import classes
from . import indicators
from . import scoping
from . import typings


### CLASSES ###

class BCPCommand(scoping.Command):
    """
    Bow contact point command.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bow_contact_points',
        '_final_spanner',
        '_helper',
        '_tweaks',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *tweaks: abjad.LilyPondTweakManager,
        bcps: typing.Iterable[typings.IntegerPair] = None,
        final_spanner: bool = None,
        helper: typing.Callable = None,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        scope: scoping.scope_typing = None,
        selector: typings.Selector = None,
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
        if bcps is None:
            self._validate_bcps(bcps)
        self._bow_contact_points = bcps
        if final_spanner is not None:
            final_spanner = bool(final_spanner)
        self._final_spanner = final_spanner
        if helper is not None:
            assert callable(helper), repr(helper)
        self._helper = helper
        self._validate_tweaks(tweaks)
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
        total = len(lts)
        add_right_text_to_me = None
        if not self.final_spanner:
            rest_count, nonrest_count = 0, 0
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
        if (self.final_spanner and
            not self._is_rest(lts[-1]) and
            len(lts[-1]) == 1):
            next_leaf_after_argument = abjad.inspect(lts[-1][-1]).leaf(1)
            if next_leaf_after_argument is None:
                raise Exception(
                    'can not attach final spanner:'
                    ' argument includes end of score.'
                    )
        previous_bcp = None
        i = 0
        for lt in lts:
            stop_text_span = abjad.StopTextSpan(
                command=self.stop_command,
                )
            if (not self.final_spanner and
                lt is lts[-1] and
                not self._is_rest(lt.head)):
                abjad.attach(
                    stop_text_span,
                    lt.head,
                    tag=self.tag.append('BCPCommand(1)'),
                    )
                break
            previous_leaf = abjad.inspect(lt.head).leaf(-1)
            if (self._is_rest(lt.head) and
                (self._is_rest(previous_leaf) or previous_leaf is None)):
                continue
            if (isinstance(lt.head, abjad.Note) and
                self._is_rest(previous_leaf) and
                previous_bcp is not None):
                numerator, denominator = previous_bcp
            else:
                bcp = bcps[i]
                numerator, denominator = bcp
                i += 1
                next_bcp = bcps[i]
            left_text = r'- \baca-bcp-spanner-left-text'
            left_text += rf' #{numerator} #{denominator}'
            if lt is lts[-1]:
                if self.final_spanner:
                    style = 'solid-line-with-arrow'
                else:
                    style = 'invisible-line'
            elif not self._is_rest(lt.head):
                style = 'solid-line-with-arrow'
            else:
                style = 'invisible-line'
            right_text = None
            if lt.head is add_right_text_to_me:
                numerator, denominator = next_bcp
                right_text = r'- \baca-bcp-spanner-right-text'
                right_text += rf' #{numerator} #{denominator}'
            start_text_span = abjad.StartTextSpan(
                command=self.start_command,
                left_text=left_text,
                right_text=right_text,
                style=style,
                )
            if self.tweaks:
                self._apply_tweaks(start_text_span, self.tweaks)
            abjad.attach(
                start_text_span,
                lt.head,
                tag=self.tag.append('BCPCommand(2)'),
                )
            if 0 < i:
                abjad.attach(
                    stop_text_span,
                    lt.head,
                    tag=self.tag.append('BCPCommand(3)'),
                    )
            if lt is lts[-1] and self.final_spanner:
                abjad.attach(
                    stop_text_span,
                    next_leaf_after_argument,
                    tag=self.tag.append('BCPCommand(4)'),
                    )
            bcp_fraction = abjad.Fraction(*bcp)
            next_bcp_fraction = abjad.Fraction(*bcps[i])
            if self._is_rest(lt.head):
                pass
            elif self._is_rest(previous_leaf) or previous_bcp is None:
                if bcp_fraction > next_bcp_fraction:
                    abjad.attach(
                        abjad.Articulation('upbow'),
                        lt.head,
                        tag=self.tag.append('BCPCommand(5)'),
                        )
                elif bcp_fraction < next_bcp_fraction:
                    abjad.attach(
                        abjad.Articulation('downbow'),
                        lt.head,
                        tag=self.tag.append('BCPCommand(6)'),
                        )
            else:
                previous_bcp_fraction = abjad.Fraction(*previous_bcp)
                if previous_bcp_fraction < bcp_fraction > next_bcp_fraction:
                    abjad.attach(
                        abjad.Articulation('upbow'),
                        lt.head,
                        tag=self.tag.append('BCPCommand(7)'),
                        )
                elif previous_bcp_fraction > bcp_fraction < next_bcp_fraction:
                    abjad.attach(
                        abjad.Articulation('downbow'),
                        lt.head,
                        tag=self.tag.append('BCPCommand(8)'),
                        )
            previous_bcp = bcp

    ### PRIVATE METHODS ###

    @staticmethod
    def _is_rest(argument):
        prototype = (abjad.Rest, abjad.MultimeasureRest, abjad.Skip)
        if isinstance(argument, prototype):
            return True
        annotation = abjad.inspect(argument).annotation('is_sounding')
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
    def bcps(self) -> typing.Optional[typing.Iterable[typings.IntegerPair]]:
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
            ...     'MusicVoice',
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
                \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
                <<                                                                                       %! SingleStaffScoreTemplate
                <BLANKLINE>
                    \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                    <<                                                                                   %! _make_global_context
                <BLANKLINE>
                        \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                        {                                                                                %! _make_global_context
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
                <BLANKLINE>
                        }                                                                                %! _make_global_context
                <BLANKLINE>
                    >>                                                                                   %! _make_global_context
                <BLANKLINE>
                    \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                    <<                                                                                   %! SingleStaffScoreTemplate
                <BLANKLINE>
                        \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                        {                                                                                %! SingleStaffScoreTemplate
                <BLANKLINE>
                            \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                            {                                                                            %! SingleStaffScoreTemplate
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \override Script.staff-padding = #5.5                                    %! baca_script_staff_padding:OverrideCommand(1)
                                \override TextSpanner.staff-padding = #2.5                               %! baca_text_spanner_staff_padding:OverrideCommand(1)
                                e'8                                                                      %! baca_make_even_divisions
                                - \downbow                                                               %! BCPCommand(6)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                                [                                                                        %! baca_make_even_divisions
                <BLANKLINE>
                                f'8                                                                      %! baca_make_even_divisions
                                - \upbow                                                                 %! BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                <BLANKLINE>
                                e'8                                                                      %! baca_make_even_divisions
                                - \downbow                                                               %! BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                <BLANKLINE>
                                f'8                                                                      %! baca_make_even_divisions
                                - \upbow                                                                 %! BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                ]                                                                        %! baca_make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                e'8                                                                      %! baca_make_even_divisions
                                - \downbow                                                               %! BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                                [                                                                        %! baca_make_even_divisions
                <BLANKLINE>
                                f'8                                                                      %! baca_make_even_divisions
                                - \upbow                                                                 %! BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! BCPCommand(2)
                                - \baca-bcp-spanner-right-text #1 #5                                     %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                <BLANKLINE>
                                e'8                                                                      %! baca_make_even_divisions
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(1)
                                ]                                                                        %! baca_make_even_divisions
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                                f'8                                                                      %! baca_make_even_divisions
                                - \downbow                                                               %! BCPCommand(6)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #3 #5                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                                [                                                                        %! baca_make_even_divisions
                <BLANKLINE>
                                e'8                                                                      %! baca_make_even_divisions
                                - \upbow                                                                 %! BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #4 #5                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                <BLANKLINE>
                                f'8                                                                      %! baca_make_even_divisions
                                - \downbow                                                               %! BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #3 #5                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                <BLANKLINE>
                                e'8                                                                      %! baca_make_even_divisions
                                - \upbow                                                                 %! BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                ]                                                                        %! baca_make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #4 #5                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                                f'8                                                                      %! baca_make_even_divisions
                                - \downbow                                                               %! BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #3 #5                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                                [                                                                        %! baca_make_even_divisions
                <BLANKLINE>
                                e'8                                                                      %! baca_make_even_divisions
                                - \upbow                                                                 %! BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #4 #5                                      %! BCPCommand(2)
                                - \baca-bcp-spanner-right-text #3 #5                                     %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                <BLANKLINE>
                                f'8                                                                      %! baca_make_even_divisions
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(1)
                                ]                                                                        %! baca_make_even_divisions
                                \revert Script.staff-padding                                             %! baca_script_staff_padding:OverrideCommand(2)
                                \revert TextSpanner.staff-padding                                        %! baca_text_spanner_staff_padding:OverrideCommand(2)
                <BLANKLINE>
                            }                                                                            %! SingleStaffScoreTemplate
                <BLANKLINE>
                        }                                                                                %! SingleStaffScoreTemplate
                <BLANKLINE>
                    >>                                                                                   %! SingleStaffScoreTemplate
                <BLANKLINE>
                >>                                                                                       %! SingleStaffScoreTemplate

        """
        return self._bow_contact_points

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
        return r'\bacaStartTextSpanBCP'

    @property
    def stop_command(self) -> str:
        r"""
        Gets ``'\bacaStopTextSpanBCP'``.
        """
        return r'\bacaStopTextSpanBCP'

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
    def tweaks(self) -> typing.Tuple[abjad.LilyPondTweakManager, ...]:
        r"""
        Gets tweaks.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 16)),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_even_divisions(),
            ...     baca.bcps(
            ...         [(1, 5), (2, 5)],
            ...         abjad.tweak('red').color,
            ...         ),
            ...     baca.pitches('E4 F4'),
            ...     baca.script_staff_padding(5.5),
            ...     baca.text_spanner_staff_padding(2.5),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                <BLANKLINE>
                \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
                <<                                                                                       %! SingleStaffScoreTemplate
                <BLANKLINE>
                    \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                    <<                                                                                   %! _make_global_context
                <BLANKLINE>
                        \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                        {                                                                                %! _make_global_context
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
                <BLANKLINE>
                        }                                                                                %! _make_global_context
                <BLANKLINE>
                    >>                                                                                   %! _make_global_context
                <BLANKLINE>
                    \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                    <<                                                                                   %! SingleStaffScoreTemplate
                <BLANKLINE>
                        \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                        {                                                                                %! SingleStaffScoreTemplate
                <BLANKLINE>
                            \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                            {                                                                            %! SingleStaffScoreTemplate
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \override Script.staff-padding = #5.5                                    %! baca_script_staff_padding:OverrideCommand(1)
                                \override TextSpanner.staff-padding = #2.5                               %! baca_text_spanner_staff_padding:OverrideCommand(1)
                                e'8                                                                      %! baca_make_even_divisions
                                - \downbow                                                               %! BCPCommand(6)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! BCPCommand(2)
                                - \tweak color #red                                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                                [                                                                        %! baca_make_even_divisions
                <BLANKLINE>
                                f'8                                                                      %! baca_make_even_divisions
                                - \upbow                                                                 %! BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! BCPCommand(2)
                                - \tweak color #red                                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                <BLANKLINE>
                                e'8                                                                      %! baca_make_even_divisions
                                - \downbow                                                               %! BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! BCPCommand(2)
                                - \tweak color #red                                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                <BLANKLINE>
                                f'8                                                                      %! baca_make_even_divisions
                                - \upbow                                                                 %! BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                ]                                                                        %! baca_make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! BCPCommand(2)
                                - \tweak color #red                                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                e'8                                                                      %! baca_make_even_divisions
                                - \downbow                                                               %! BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! BCPCommand(2)
                                - \tweak color #red                                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                                [                                                                        %! baca_make_even_divisions
                <BLANKLINE>
                                f'8                                                                      %! baca_make_even_divisions
                                - \upbow                                                                 %! BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! BCPCommand(2)
                                - \tweak color #red                                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                <BLANKLINE>
                                e'8                                                                      %! baca_make_even_divisions
                                - \downbow                                                               %! BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                ]                                                                        %! baca_make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! BCPCommand(2)
                                - \tweak color #red                                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                                f'8                                                                      %! baca_make_even_divisions
                                - \upbow                                                                 %! BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! BCPCommand(2)
                                - \tweak color #red                                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                                [                                                                        %! baca_make_even_divisions
                <BLANKLINE>
                                e'8                                                                      %! baca_make_even_divisions
                                - \downbow                                                               %! BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! BCPCommand(2)
                                - \tweak color #red                                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                <BLANKLINE>
                                f'8                                                                      %! baca_make_even_divisions
                                - \upbow                                                                 %! BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! BCPCommand(2)
                                - \tweak color #red                                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                <BLANKLINE>
                                e'8                                                                      %! baca_make_even_divisions
                                - \downbow                                                               %! BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                ]                                                                        %! baca_make_even_divisions
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! BCPCommand(2)
                                - \tweak color #red                                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                                f'8                                                                      %! baca_make_even_divisions
                                - \upbow                                                                 %! BCPCommand(7)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! BCPCommand(2)
                                - \tweak color #red                                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                                [                                                                        %! baca_make_even_divisions
                <BLANKLINE>
                                e'8                                                                      %! baca_make_even_divisions
                                - \downbow                                                               %! BCPCommand(8)
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(3)
                                - \abjad-solid-line-with-arrow                                           %! BCPCommand(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! BCPCommand(2)
                                - \baca-bcp-spanner-right-text #2 #5                                     %! BCPCommand(2)
                                - \tweak color #red                                                      %! BCPCommand(2)
                                \bacaStartTextSpanBCP                                                    %! BCPCommand(2)
                <BLANKLINE>
                                f'8                                                                      %! baca_make_even_divisions
                                \bacaStopTextSpanBCP                                                     %! BCPCommand(1)
                                ]                                                                        %! baca_make_even_divisions
                                \revert Script.staff-padding                                             %! baca_script_staff_padding:OverrideCommand(2)
                                \revert TextSpanner.staff-padding                                        %! baca_text_spanner_staff_padding:OverrideCommand(2)
                <BLANKLINE>
                            }                                                                            %! SingleStaffScoreTemplate
                <BLANKLINE>
                        }                                                                                %! SingleStaffScoreTemplate
                <BLANKLINE>
                    >>                                                                                   %! SingleStaffScoreTemplate
                <BLANKLINE>
                >>                                                                                       %! SingleStaffScoreTemplate

        """
        return self._tweaks

class ColorCommand(scoping.Command):
    r"""
    Color command.

    >>> from abjadext import rmakers

    ..  container:: example

        With music-maker:

        Colors leaves by default:

        >>> music_maker = baca.MusicMaker(
        ...     baca.color(),
        ...     baca.PitchFirstRhythmCommand(
        ...         rhythm_maker=baca.PitchFirstRhythmMaker(
        ...             talea=rmakers.Talea(
        ...                 counts=[5, 4, 4, 5, 4, 4, 4],
        ...                 denominator=32,
        ...                 ),
        ...             ),
        ...         ),
        ...     )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker('Voice 1', collections)
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'red
                            c'8
                            ~
                            [
                            \abjad-color-music #'blue
                            c'32
                            \abjad-color-music #'red
                            d'8
                            \abjad-color-music #'blue
                            bf'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'red
                            fs''8
                            ~
                            [
                            \abjad-color-music #'blue
                            fs''32
                            \abjad-color-music #'red
                            e''8
                            \abjad-color-music #'blue
                            ef''8
                            \abjad-color-music #'red
                            af''8
                            ~
                            \abjad-color-music #'blue
                            af''32
                            \abjad-color-music #'red
                            g''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'blue
                            a'8
                            ~
                            [
                            \abjad-color-music #'red
                            a'32
                            ]
                        }
                    }
                }
            >>

    ..  container:: example

        With segment-maker:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.color(),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \abjad-color-music #'red
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            \abjad-color-music #'blue
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            \abjad-color-music #'red
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            \abjad-color-music #'blue
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            \abjad-color-music #'red
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            \abjad-color-music #'blue
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            \abjad-color-music #'red
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            \abjad-color-music #'blue
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            \abjad-color-music #'red
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            \abjad-color-music #'blue
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            \abjad-color-music #'red
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            \abjad-color-music #'blue
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            \abjad-color-music #'red
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            \abjad-color-music #'blue
                            d''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        scope: scoping.scope_typing = None,
        selector='baca.leaves()',
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

    def _call(self, argument=None):
        """
        Calls command on ``argument``.

        Returns colored selector result.
        """
        if argument is None:
            return
        argument = self.selector(argument)
        self.selector.color(argument)
        return argument

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
        ...     'MusicVoice',
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.container('ViolinI', selector=baca.leaves()[:2]),
        ...     baca.container('ViolinII', selector=baca.leaves()[2:]),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')

        >>> abjad.f(lilypond_file[abjad.Score], strict=89)
        <BLANKLINE>
        \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
        <<                                                                                       %! SingleStaffScoreTemplate
        <BLANKLINE>
            \context GlobalContext = "GlobalContext"                                             %! _make_global_context
            <<                                                                                   %! _make_global_context
        <BLANKLINE>
                \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                {                                                                                %! _make_global_context
        <BLANKLINE>
                    % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                    \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 1/2                                                                     %! _make_global_skips(1)
        <BLANKLINE>
                    % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                    \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 3/8                                                                     %! _make_global_skips(1)
        <BLANKLINE>
                    % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                    \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 1/2                                                                     %! _make_global_skips(1)
        <BLANKLINE>
                    % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                    \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 3/8                                                                     %! _make_global_skips(1)
                    \baca-bar-line-visible                                                       %! _attach_final_bar_line
                    \bar "|"                                                                     %! _attach_final_bar_line
        <BLANKLINE>
                }                                                                                %! _make_global_context
        <BLANKLINE>
            >>                                                                                   %! _make_global_context
        <BLANKLINE>
            \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
            <<                                                                                   %! SingleStaffScoreTemplate
        <BLANKLINE>
                \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                {                                                                                %! SingleStaffScoreTemplate
        <BLANKLINE>
                    \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                    {                                                                            %! SingleStaffScoreTemplate
        <BLANKLINE>
                        {   %*% ViolinI
        <BLANKLINE>
                            % [MusicVoice measure 1]                                             %! _comment_measure_numbers
                            e'2                                                                  %! baca_make_notes
        <BLANKLINE>
                            % [MusicVoice measure 2]                                             %! _comment_measure_numbers
                            f'4.                                                                 %! baca_make_notes
        <BLANKLINE>
                        }   %*% ViolinI
        <BLANKLINE>
                        {   %*% ViolinII
        <BLANKLINE>
                            % [MusicVoice measure 3]                                             %! _comment_measure_numbers
                            e'2                                                                  %! baca_make_notes
        <BLANKLINE>
                            % [MusicVoice measure 4]                                             %! _comment_measure_numbers
                            f'4.                                                                 %! baca_make_notes
        <BLANKLINE>
                        }   %*% ViolinII
        <BLANKLINE>
                    }                                                                            %! SingleStaffScoreTemplate
        <BLANKLINE>
                }                                                                                %! SingleStaffScoreTemplate
        <BLANKLINE>
            >>                                                                                   %! SingleStaffScoreTemplate
        <BLANKLINE>
        >>                                                                                       %! SingleStaffScoreTemplate

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_identifier',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        identifier: str = None,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        scope: scoping.scope_typing = None,
        selector: typings.Selector = 'baca.leaves()',
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
                message = f'identifier must be string (not {identifier!r}).'
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
        elif self.identifier.startswith('%*%'):
            identifier = self.identifier
        else:
            identifier = f'%*% {self.identifier}'
        container = abjad.Container(identifier=identifier)
        components = classes.Selection(argument).leaves().top()
        abjad.mutate(components).wrap(container)

    ### PUBLIC PROPERTIES ###

    @property
    def identifier(self) -> typing.Optional[str]:
        """
        Gets identifier.
        """
        return self._identifier

class GlobalFermataCommand(scoping.Command):
    """
    Global fermata command.

    ..  container:: example

        >>> baca.GlobalFermataCommand()
        GlobalFermataCommand(selector=baca.leaf(0))

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_description',
        )

    description_to_command = {
        'short': 'shortfermata',
        'fermata': 'fermata',
        'long': 'longfermata',
        'very_long': 'verylongfermata',
        }

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        description: str = None,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        scope: scoping.scope_typing = None,
        selector: typings.Selector = 'baca.leaf(0)',
        ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
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
        if isinstance(self.description, str) and self.description != 'fermata':
            description = self.description.replace('_', '-')
            command = f'{description}-fermata'
        else:
            command = 'fermata'
        for leaf in abjad.iterate(argument).leaves():
            assert isinstance(leaf, abjad.MultimeasureRest)
            string = rf'\baca-{command}-markup'
            markup = abjad.Markup.from_literal(string, literal=True)
            markup = abjad.new(markup, direction=abjad.Up)
            abjad.attach(markup, leaf, tag='GlobalFermataCommand(1)')
            string = r'\once \override Score.TimeSignature.stencil = ##f'
            literal = abjad.LilyPondLiteral(string)
            abjad.attach(literal, leaf, tag='GlobalFermataCommand(2)')
            abjad.attach(
                abjad.tags.FERMATA_MEASURE,
                leaf,
                tag=abjad.tags.FERMATA_MEASURE,
                )

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

    >>> from abjadext import rmakers

    ..  container:: example

        With music-maker:

        >>> music_maker = baca.MusicMaker(
        ...     baca.IndicatorCommand(indicators=[abjad.Fermata()]),
        ...     baca.PitchFirstRhythmCommand(
        ...         rhythm_maker=baca.PitchFirstRhythmMaker(
        ...             talea=rmakers.Talea(
        ...                 counts=[5, 4, 4, 5, 4, 4, 4],
        ...                 denominator=32,
        ...                 ),
        ...             ),
        ...         ),
        ...     )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker('Voice 1', collections)
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            c'8
                            \fermata                                                                 %! IndicatorCommand
                            ~
                            [
                            c'32
                            d'8
                            \fermata                                                                 %! IndicatorCommand
                            bf'8
                            \fermata                                                                 %! IndicatorCommand
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''8
                            \fermata                                                                 %! IndicatorCommand
                            ~
                            [
                            fs''32
                            e''8
                            \fermata                                                                 %! IndicatorCommand
                            ef''8
                            \fermata                                                                 %! IndicatorCommand
                            af''8
                            \fermata                                                                 %! IndicatorCommand
                            ~
                            af''32
                            g''8
                            \fermata                                                                 %! IndicatorCommand
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                            \fermata                                                                 %! IndicatorCommand
                            ~
                            [
                            a'32
                            ]
                        }
                    }
                }
            >>

    ..  container:: example

        With segment-maker:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.IndicatorCommand(indicators=[abjad.Fermata()]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            \fermata                                                                 %! IndicatorCommand
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            \fermata                                                                 %! IndicatorCommand
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            \fermata                                                                 %! IndicatorCommand
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            \fermata                                                                 %! IndicatorCommand
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            \fermata                                                                 %! IndicatorCommand
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
                            \fermata                                                                 %! IndicatorCommand
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            \fermata                                                                 %! IndicatorCommand
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            \fermata                                                                 %! IndicatorCommand
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            \fermata                                                                 %! IndicatorCommand
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            \fermata                                                                 %! IndicatorCommand
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            \fermata                                                                 %! IndicatorCommand
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            \fermata                                                                 %! IndicatorCommand
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            \fermata                                                                 %! IndicatorCommand
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            \fermata                                                                 %! IndicatorCommand
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context',
        '_indicators',
        '_predicate',
        '_redundant',
        '_tags',
        '_tweaks',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *tweaks: abjad.LilyPondTweakManager,
        context: str = None,
        deactivate: bool = None,
        indicators: typing.List[typing.Any] = None,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        predicate: typing.Callable = None,
        redundant: bool = None,
        scope: scoping.scope_typing = None,
        selector: typings.Selector = 'baca.pheads()',
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
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        indicators_ = None
        if indicators is not None:
            if isinstance(indicators, collections.Iterable):
                indicators_ = abjad.CyclicTuple(indicators)
            else:
                indicators_ = abjad.CyclicTuple([indicators])
        self._indicators = indicators_
        self._predicate = predicate
        if redundant is not None:
            redundant = bool(redundant)
        self._redundant = redundant
        self._validate_tweaks(tweaks)
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
        for i, leaf in enumerate(classes.Selection(argument).leaves()):
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
                    tag=self.tag.append('IndicatorCommand'),
                    wrapper=True,
                    )
                if indicator == reapplied:
                    if (isinstance(indicator, abjad.Dynamic) and
                        indicator.sforzando):
                        status = 'explicit'
                    else:
                        status = 'redundant'
                    SegmentMaker._treat_persistent_wrapper(
                        self.runtime['manifests'],
                        wrapper,
                        status,
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
    def indicators(self) -> typing.Optional[abjad.CyclicTuple]:
        r"""
        Gets indicators.

        ..  container:: example

            Attaches fermata to head of every pitched logical tie:

            >>> music_maker = baca.MusicMaker(
            ...     baca.IndicatorCommand(indicators=[abjad.Fermata()]),
            ...     baca.PitchFirstRhythmCommand(
            ...         rhythm_maker=baca.PitchFirstRhythmMaker(
            ...             talea=rmakers.Talea(
            ...                 counts=[5, 4, 4, 5, 4, 4, 4],
            ...                 denominator=32,
            ...                 ),
            ...             ),
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'8
                                \fermata                                                                 %! IndicatorCommand
                                ~
                                [
                                c'32
                                d'8
                                \fermata                                                                 %! IndicatorCommand
                                bf'8
                                \fermata                                                                 %! IndicatorCommand
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs''8
                                \fermata                                                                 %! IndicatorCommand
                                ~
                                [
                                fs''32
                                e''8
                                \fermata                                                                 %! IndicatorCommand
                                ef''8
                                \fermata                                                                 %! IndicatorCommand
                                af''8
                                \fermata                                                                 %! IndicatorCommand
                                ~
                                af''32
                                g''8
                                \fermata                                                                 %! IndicatorCommand
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'8
                                \fermata                                                                 %! IndicatorCommand
                                ~
                                [
                                a'32
                                ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Patterns fermatas:

            >>> music_maker = baca.MusicMaker(
            ...     baca.IndicatorCommand(
            ...         indicators=[
            ...             abjad.Fermata(), None, None,
            ...             abjad.Fermata(), None, None,
            ...             abjad.Fermata(), None,
            ...             ],
            ...         ),
            ...     baca.PitchFirstRhythmCommand(
            ...         rhythm_maker=baca.PitchFirstRhythmMaker(
            ...             talea=rmakers.Talea(
            ...                 counts=[5, 4, 4, 5, 4, 4, 4],
            ...                 denominator=32,
            ...                 ),
            ...             ),
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'8
                                \fermata                                                                 %! IndicatorCommand
                                ~
                                [
                                c'32
                                d'8
                                bf'8
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs''8
                                \fermata                                                                 %! IndicatorCommand
                                ~
                                [
                                fs''32
                                e''8
                                ef''8
                                af''8
                                \fermata                                                                 %! IndicatorCommand
                                ~
                                af''32
                                g''8
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'8
                                \fermata                                                                 %! IndicatorCommand
                                ~
                                [
                                a'32
                                ]
                            }
                        }
                    }
                >>

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
    def tweaks(self) -> typing.Tuple[abjad.LilyPondTweakManager, ...]:
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
            parentage = abjad.inspect(first_leaf).parentage()
            staff = parentage.get_first(abjad.Staff)
            instrument = self.indicators[0]
            assert isinstance(instrument, abjad.Instrument), repr(instrument)
            if not self.runtime['score_template'].allows_instrument(
                staff.name,
                instrument,
                ):
                message = f'{staff.name} does not allow instrument:\n'
                message += f'  {instrument}'
                raise Exception(message)
        super()._call(argument)

class LabelCommand(scoping.Command):
    r"""
    Label command.

    ..  container:: example

        Labels pitch names:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.label(abjad.label().with_pitches(locale='us')),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            ^ \markup { E4 }
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            ^ \markup { D5 }
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            ^ \markup { F4 }
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ^ \markup { E5 }
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            ^ \markup { G4 }
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
                            ^ \markup { F5 }
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ^ \markup { E4 }
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            ^ \markup { D5 }
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            ^ \markup { F4 }
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ^ \markup { E5 }
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ^ \markup { G4 }
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            ^ \markup { F5 }
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ^ \markup { E4 }
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            ^ \markup { D5 }
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        Labels pitch names in tuplet 0:

        >>> music_maker = baca.MusicMaker()

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     collections,
        ...     baca.label(
        ...         abjad.label().with_pitches(locale='us'),
        ...         selector=baca.tuplet(0),
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            c'16
                            ^ \markup { C4 }
                            [
                            d'16
                            ^ \markup { D4 }
                            bf'16
                            ^ \markup { Bb4 }
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''16
                            [
                            e''16
                            ef''16
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'16
                        }
                    }
                }
            >>

    """

    ### CLASS VARIABLES ##

    __slots__ = (
        '_expression',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        expression=None,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        scope: scoping.scope_typing = None,
        selector='baca.leaves()',
        ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector
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
    def expression(self):
        """
        Gets expression.

        Defaults to none.

        Set to label expression or none.

        Returns label expression or none.
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

    __slots__ = (
        '_key',
        '_redundant',
        '_tags',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        deactivate: bool = None,
        key: typing.Union[
            str,
            indicators.Accelerando,
            indicators.Ritardando] = None,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        redundant: bool = None,
        scope: scoping.scope_typing = None,
        selector: typings.Selector = 'baca.leaf(0)',
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
        if isinstance(self.key, str) and self.runtime['manifests'] is not None:
            metronome_marks = self.runtime['manifests']['abjad.MetronomeMark']
            indicator = metronome_marks.get(self.key)
            if indicator is None:
                raise Exception(f'can not find metronome mark {self.key!r}.')
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
                self.runtime['manifests'],
                wrapper,
                'redundant',
                )

    ### PUBLIC PROPERTIES ###

    @property
    def key(self) -> typing.Optional[typing.Union[str,
    indicators.Accelerando, indicators.Ritardando]]:
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

    __slots__ = (
        '_part_assignment',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        part_assignment: abjad.PartAssignment = None,
        scope: scoping.scope_typing = None,
        selector: typings.Selector = 'baca.leaves()',
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
                message = 'part_assignment must be part assignment'
                message += f' (not {part_assignment!r}).'
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
        parentage = abjad.inspect(first_leaf).parentage()
        voice = parentage.get_first(abjad.Voice)
        if voice is not None and self.part_assignment is not None:
            if not self.runtime['score_template'].allows_part_assignment(
                voice.name,
                self.part_assignment,
                ):
                message = f'{voice.name} does not allow'
                message += f' {self.part_assignment.section} part assignment:'
                message += f'\n  {self.part_assignment}'
                raise Exception(message)
        identifier = f'%*% {self.part_assignment!s}'
        container = abjad.Container(identifier=identifier)
        components = classes.Selection(argument).leaves().top()
        abjad.mutate(components).wrap(container)

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

    __slots__ = (
        )

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

### FACTORY FUNCTIONS ###

def allow_octaves(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> IndicatorCommand:
    """
    Attaches ALLOW_OCTAVE tag.
    """
    return IndicatorCommand(
        indicators=[abjad.tags.ALLOW_OCTAVE],
        selector=selector,
        )

def bar_extent_persistent(
    pair: typings.NumberPair = None,
    *,
    selector: typings.Selector = 'baca.leaf(0)',
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
        ...     'MusicVoice',
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
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override Staff.BarLine.bar-extent = #'(0 . 0)                           %! EXPLICIT_PERSISTENT_OVERRIDE:_set_status_tag:IndicatorCommand
                            \stopStaff                                                               %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                            \once \override Staff.StaffSymbol.line-count = 1                         %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                            \startStaff                                                              %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:_attach_color_literal(2)
                            b'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            b'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            b'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            b'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    """
    override = abjad.PersistentOverride(
        after=True,
        attribute='bar_extent',
        context='Staff',
        grob='bar_line',
        value=pair,
        )
    return IndicatorCommand(
        indicators=[override],
        selector=selector,
        )

def bcps(
    bcps: typing.Iterable[typings.IntegerPair],
    *tweaks: abjad.LilyPondTweakManager,
    final_spanner: bool = None,
    helper: typing.Callable = None,
    selector: typings.Selector = 'baca.leaves()',
    ) -> BCPCommand:
    """
    Makes bow contact points.
    """
    if final_spanner is not None:
        final_spanner = bool(final_spanner)
    return BCPCommand(
        *tweaks,
        bcps=bcps,
        final_spanner=final_spanner,
        helper=helper,
        selector=selector,
        )

def color(*, selector: typings.Selector = 'baca.leaves()') -> ColorCommand:
    r"""
    Colors leaves.

    ..  container:: example

        Colors all leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.color(),
        ...     baca.flags(),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
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
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Colors leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.color(selector=baca.tuplets()[1:2].leaves()),
        ...     baca.flags(),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
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
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return ColorCommand(selector=selector)

def container(
    identifier: str = None,
    *,
    selector: typings.Selector = 'baca.leaves()',
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
        ...     'MusicVoice',
        ...     baca.container('ViolinI', selector=baca.leaves()[:2]),
        ...     baca.container('ViolinII', selector=baca.leaves()[2:]),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')

        >>> abjad.f(lilypond_file[abjad.Score], strict=89)
        <BLANKLINE>
        \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
        <<                                                                                       %! SingleStaffScoreTemplate
        <BLANKLINE>
            \context GlobalContext = "GlobalContext"                                             %! _make_global_context
            <<                                                                                   %! _make_global_context
        <BLANKLINE>
                \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                {                                                                                %! _make_global_context
        <BLANKLINE>
                    % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                    \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 1/2                                                                     %! _make_global_skips(1)
        <BLANKLINE>
                    % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                    \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 3/8                                                                     %! _make_global_skips(1)
        <BLANKLINE>
                    % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                    \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 1/2                                                                     %! _make_global_skips(1)
        <BLANKLINE>
                    % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                    \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 3/8                                                                     %! _make_global_skips(1)
                    \baca-bar-line-visible                                                       %! _attach_final_bar_line
                    \bar "|"                                                                     %! _attach_final_bar_line
        <BLANKLINE>
                }                                                                                %! _make_global_context
        <BLANKLINE>
            >>                                                                                   %! _make_global_context
        <BLANKLINE>
            \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
            <<                                                                                   %! SingleStaffScoreTemplate
        <BLANKLINE>
                \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                {                                                                                %! SingleStaffScoreTemplate
        <BLANKLINE>
                    \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                    {                                                                            %! SingleStaffScoreTemplate
        <BLANKLINE>
                        {   %*% ViolinI
        <BLANKLINE>
                            % [MusicVoice measure 1]                                             %! _comment_measure_numbers
                            e'2                                                                  %! baca_make_notes
        <BLANKLINE>
                            % [MusicVoice measure 2]                                             %! _comment_measure_numbers
                            f'4.                                                                 %! baca_make_notes
        <BLANKLINE>
                        }   %*% ViolinI
        <BLANKLINE>
                        {   %*% ViolinII
        <BLANKLINE>
                            % [MusicVoice measure 3]                                             %! _comment_measure_numbers
                            e'2                                                                  %! baca_make_notes
        <BLANKLINE>
                            % [MusicVoice measure 4]                                             %! _comment_measure_numbers
                            f'4.                                                                 %! baca_make_notes
        <BLANKLINE>
                        }   %*% ViolinII
        <BLANKLINE>
                    }                                                                            %! SingleStaffScoreTemplate
        <BLANKLINE>
                }                                                                                %! SingleStaffScoreTemplate
        <BLANKLINE>
            >>                                                                                   %! SingleStaffScoreTemplate
        <BLANKLINE>
        >>                                                                                       %! SingleStaffScoreTemplate

    """
    if identifier is not None:
        if not isinstance(identifier, str):
            message = f'identifier must be string (not {identifier!r}).'
            raise Exception(message)
    return ContainerCommand(
        identifier=identifier,
        selector=selector,
        )

def cross_staff(
    *,
    selector: typings.Selector = 'baca.phead(0)',
    ) -> IndicatorCommand:
    r"""
    Attaches cross-staff command.

    ..  container:: example

        Attaches cross-staff command to pitched head 0:

        >>> score_template = baca.StringTrioScoreTemplate()
        >>> accumulator = baca.MusicAccumulator(score_template=score_template)
        >>> accumulator(
        ...     accumulator.music_maker(
        ...         'ViolinMusicVoice',
        ...         [[9, 11, 12, 14, 16]],
        ...         baca.flags(),
        ...         baca.stem_up(),
        ...         denominator=8,
        ...         figure_name='vn.1',
        ...         talea_denominator=8,
        ...         ),
        ...     )
        >>> accumulator(
        ...     accumulator.music_maker(
        ...         'ViolaMusicVoice',
        ...         [[0, 2, 4, 5, 7]],
        ...         baca.anchor('ViolinMusicVoice'),
        ...         baca.cross_staff(),
        ...         baca.flags(),
        ...         baca.stem_up(),
        ...         figure_name='va.1',
        ...         talea_denominator=8,
        ...         ),
        ...     )
        >>> accumulator(
        ...     accumulator.music_maker(
        ...         'ViolinMusicVoice',
        ...         [[15]],
        ...         baca.flags(),
        ...         figure_name='vn.2',
        ...         talea_denominator=8,
        ...         ),
        ...     )

        >>> maker = baca.SegmentMaker(
        ...     ignore_repeat_pitch_classes=True,
        ...     ignore_unregistered_pitches=True,
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
            \context Score = "Score"                                                                 %! StringTrioScoreTemplate
            <<                                                                                       %! StringTrioScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 5/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 5/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 2/16                                                                   %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! StringTrioScoreTemplate
                <<                                                                                   %! StringTrioScoreTemplate
            <BLANKLINE>
                    \context StringSectionStaffGroup = "String Section Staff Group"                  %! StringTrioScoreTemplate
                    <<                                                                               %! StringTrioScoreTemplate
            <BLANKLINE>
                        \tag Violin                                                                  %! ScoreTemplate(5)
                        \context ViolinMusicStaff = "ViolinMusicStaff"                               %! StringTrioScoreTemplate
                        {                                                                            %! StringTrioScoreTemplate
            <BLANKLINE>
                            \context ViolinMusicVoice = "ViolinMusicVoice"                           %! StringTrioScoreTemplate
                            {                                                                        %! StringTrioScoreTemplate
            <BLANKLINE>
                                {
            <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                        % [ViolinMusicVoice measure 1]                               %! _comment_measure_numbers
                                        \override Stem.direction = #up                               %! baca_stem_up:OverrideCommand(1)
                                        \clef "treble"                                               %! DEFAULT_CLEF:_set_status_tag:attach_defaults
                                        \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                                    %@% \override ViolinMusicStaff.Clef.color = ##f                  %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                        \set ViolinMusicStaff.forceClef = ##t                        %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):attach_defaults
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
                                        \revert Stem.direction                                       %! baca_stem_up:OverrideCommand(2)
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                }
            <BLANKLINE>
                                {
            <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                        % [ViolinMusicVoice measure 2]                               %! _comment_measure_numbers
                                        ef''!8
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                }
            <BLANKLINE>
                            }                                                                        %! StringTrioScoreTemplate
            <BLANKLINE>
                        }                                                                            %! StringTrioScoreTemplate
            <BLANKLINE>
                        \tag Viola                                                                   %! ScoreTemplate(5)
                        \context ViolaMusicStaff = "ViolaMusicStaff"                                 %! StringTrioScoreTemplate
                        {                                                                            %! StringTrioScoreTemplate
            <BLANKLINE>
                            \context ViolaMusicVoice = "ViolaMusicVoice"                             %! StringTrioScoreTemplate
                            {                                                                        %! StringTrioScoreTemplate
            <BLANKLINE>
                                {
            <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                        % [ViolaMusicVoice measure 1]                                %! _comment_measure_numbers
                                        \override Stem.direction = #up                               %! baca_stem_up:OverrideCommand(1)
                                        \clef "alto"                                                 %! DEFAULT_CLEF:_set_status_tag:attach_defaults
                                        \crossStaff                                                  %! IndicatorCommand
                                        \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                                    %@% \override ViolaMusicStaff.Clef.color = ##f                   %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                        \set ViolaMusicStaff.forceClef = ##t                         %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):attach_defaults
                                        c'8
                                        ^ \baca-default-indicator-markup "(Viola)"                   %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                                        \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)  %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                                        d'8
            <BLANKLINE>
                                        e'8
            <BLANKLINE>
                                        f'8
            <BLANKLINE>
                                        g'8
                                        \revert Stem.direction                                       %! baca_stem_up:OverrideCommand(2)
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                }
            <BLANKLINE>
                                % [ViolaMusicVoice measure 2]                                        %! _comment_measure_numbers
                                R1 * 1/8                                                             %! _make_measure_silences
            <BLANKLINE>
                            }                                                                        %! StringTrioScoreTemplate
            <BLANKLINE>
                        }                                                                            %! StringTrioScoreTemplate
            <BLANKLINE>
                        \tag Cello                                                                   %! ScoreTemplate(5)
                        \context CelloMusicStaff = "CelloMusicStaff"                                 %! StringTrioScoreTemplate
                        {                                                                            %! StringTrioScoreTemplate
            <BLANKLINE>
                            \context CelloMusicVoice = "CelloMusicVoice"                             %! StringTrioScoreTemplate
                            {                                                                        %! StringTrioScoreTemplate
            <BLANKLINE>
                                % [CelloMusicVoice measure 1]                                        %! _comment_measure_numbers
                                \clef "bass"                                                         %! DEFAULT_CLEF:_set_status_tag:attach_defaults
                                \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                            %@% \override CelloMusicStaff.Clef.color = ##f                           %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                \set CelloMusicStaff.forceClef = ##t                                 %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):attach_defaults
                                R1 * 5/8                                                             %! _call_rhythm_commands
                                ^ \baca-default-indicator-markup "(Cello)"                           %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                                \override CelloMusicStaff.Clef.color = #(x11-color 'violet)          %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                                % [CelloMusicVoice measure 2]                                        %! _comment_measure_numbers
                                R1 * 1/8                                                             %! _call_rhythm_commands
            <BLANKLINE>
                            }                                                                        %! StringTrioScoreTemplate
            <BLANKLINE>
                        }                                                                            %! StringTrioScoreTemplate
            <BLANKLINE>
                    >>                                                                               %! StringTrioScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! StringTrioScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! StringTrioScoreTemplate

    ..  container:: example

        Attaches cross-staff command to last two pitched leaves:

        >>> score_template = baca.StringTrioScoreTemplate()
        >>> accumulator = baca.MusicAccumulator(score_template=score_template)
        >>> accumulator(
        ...     accumulator.music_maker(
        ...         'ViolinMusicVoice',
        ...         [[9, 11, 12, 14, 16]],
        ...         baca.flags(),
        ...         baca.stem_up(),
        ...         denominator=8,
        ...         figure_name='vn.1',
        ...         talea_denominator=8,
        ...         ),
        ...     )
        >>> accumulator(
        ...     accumulator.music_maker(
        ...         'ViolaMusicVoice',
        ...         [[0, 2, 4, 5, 7]],
        ...         baca.anchor('ViolinMusicVoice'),
        ...         baca.cross_staff(selector=baca.pleaves()[-2:]),
        ...         baca.flags(),
        ...         baca.stem_up(),
        ...         figure_name='va.1',
        ...         talea_denominator=8,
        ...         ),
        ...     )
        >>> accumulator(
        ...     accumulator.music_maker(
        ...         'ViolinMusicVoice',
        ...         [[15]],
        ...         baca.flags(),
        ...         figure_name='vn.2',
        ...         talea_denominator=8,
        ...         ),
        ...     )

        >>> maker = baca.SegmentMaker(
        ...     ignore_repeat_pitch_classes=True,
        ...     ignore_unregistered_pitches=True,
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
            \context Score = "Score"                                                                 %! StringTrioScoreTemplate
            <<                                                                                       %! StringTrioScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 5/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 5/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 2/16                                                                   %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! StringTrioScoreTemplate
                <<                                                                                   %! StringTrioScoreTemplate
            <BLANKLINE>
                    \context StringSectionStaffGroup = "String Section Staff Group"                  %! StringTrioScoreTemplate
                    <<                                                                               %! StringTrioScoreTemplate
            <BLANKLINE>
                        \tag Violin                                                                  %! ScoreTemplate(5)
                        \context ViolinMusicStaff = "ViolinMusicStaff"                               %! StringTrioScoreTemplate
                        {                                                                            %! StringTrioScoreTemplate
            <BLANKLINE>
                            \context ViolinMusicVoice = "ViolinMusicVoice"                           %! StringTrioScoreTemplate
                            {                                                                        %! StringTrioScoreTemplate
            <BLANKLINE>
                                {
            <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                        % [ViolinMusicVoice measure 1]                               %! _comment_measure_numbers
                                        \override Stem.direction = #up                               %! baca_stem_up:OverrideCommand(1)
                                        \clef "treble"                                               %! DEFAULT_CLEF:_set_status_tag:attach_defaults
                                        \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                                    %@% \override ViolinMusicStaff.Clef.color = ##f                  %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                        \set ViolinMusicStaff.forceClef = ##t                        %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):attach_defaults
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
                                        \revert Stem.direction                                       %! baca_stem_up:OverrideCommand(2)
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                }
            <BLANKLINE>
                                {
            <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                        % [ViolinMusicVoice measure 2]                               %! _comment_measure_numbers
                                        ef''!8
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                }
            <BLANKLINE>
                            }                                                                        %! StringTrioScoreTemplate
            <BLANKLINE>
                        }                                                                            %! StringTrioScoreTemplate
            <BLANKLINE>
                        \tag Viola                                                                   %! ScoreTemplate(5)
                        \context ViolaMusicStaff = "ViolaMusicStaff"                                 %! StringTrioScoreTemplate
                        {                                                                            %! StringTrioScoreTemplate
            <BLANKLINE>
                            \context ViolaMusicVoice = "ViolaMusicVoice"                             %! StringTrioScoreTemplate
                            {                                                                        %! StringTrioScoreTemplate
            <BLANKLINE>
                                {
            <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                        % [ViolaMusicVoice measure 1]                                %! _comment_measure_numbers
                                        \override Stem.direction = #up                               %! baca_stem_up:OverrideCommand(1)
                                        \clef "alto"                                                 %! DEFAULT_CLEF:_set_status_tag:attach_defaults
                                        \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                                    %@% \override ViolaMusicStaff.Clef.color = ##f                   %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                        \set ViolaMusicStaff.forceClef = ##t                         %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):attach_defaults
                                        c'8
                                        ^ \baca-default-indicator-markup "(Viola)"                   %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                                        \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)  %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                                        d'8
            <BLANKLINE>
                                        e'8
            <BLANKLINE>
                                        \crossStaff                                                  %! IndicatorCommand
                                        f'8
            <BLANKLINE>
                                        \crossStaff                                                  %! IndicatorCommand
                                        g'8
                                        \revert Stem.direction                                       %! baca_stem_up:OverrideCommand(2)
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                }
            <BLANKLINE>
                                % [ViolaMusicVoice measure 2]                                        %! _comment_measure_numbers
                                R1 * 1/8                                                             %! _make_measure_silences
            <BLANKLINE>
                            }                                                                        %! StringTrioScoreTemplate
            <BLANKLINE>
                        }                                                                            %! StringTrioScoreTemplate
            <BLANKLINE>
                        \tag Cello                                                                   %! ScoreTemplate(5)
                        \context CelloMusicStaff = "CelloMusicStaff"                                 %! StringTrioScoreTemplate
                        {                                                                            %! StringTrioScoreTemplate
            <BLANKLINE>
                            \context CelloMusicVoice = "CelloMusicVoice"                             %! StringTrioScoreTemplate
                            {                                                                        %! StringTrioScoreTemplate
            <BLANKLINE>
                                % [CelloMusicVoice measure 1]                                        %! _comment_measure_numbers
                                \clef "bass"                                                         %! DEFAULT_CLEF:_set_status_tag:attach_defaults
                                \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                            %@% \override CelloMusicStaff.Clef.color = ##f                           %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                \set CelloMusicStaff.forceClef = ##t                                 %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):attach_defaults
                                R1 * 5/8                                                             %! _call_rhythm_commands
                                ^ \baca-default-indicator-markup "(Cello)"                           %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                                \override CelloMusicStaff.Clef.color = #(x11-color 'violet)          %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                                % [CelloMusicVoice measure 2]                                        %! _comment_measure_numbers
                                R1 * 1/8                                                             %! _call_rhythm_commands
            <BLANKLINE>
                            }                                                                        %! StringTrioScoreTemplate
            <BLANKLINE>
                        }                                                                            %! StringTrioScoreTemplate
            <BLANKLINE>
                    >>                                                                               %! StringTrioScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! StringTrioScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! StringTrioScoreTemplate

    """
    return IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r'\crossStaff')],
        selector=selector,
        )

def dynamic_down(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> IndicatorCommand:
    r"""
    Attaches dynamic-down command.

    ..  container:: example

        Attaches dynamic-down command to leaf 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dynamic('p'),
        ...     baca.dynamic('f', selector=baca.tuplets()[1:2].phead(0)),
        ...     baca.dynamic_down(),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            \dynamicDown                                                             %! IndicatorCommand
                            r8
                            c'16
                            \p                                                                       %! IndicatorCommand
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
                            \f                                                                       %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches dynamic-down command to leaf 0 in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dynamic('p'),
        ...     baca.dynamic('f', selector=baca.tuplets()[1:2].phead(0)),
        ...     baca.dynamic_down(selector=baca.tuplets()[1:2].leaf(0)),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            \p                                                                       %! IndicatorCommand
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
                            \dynamicDown                                                             %! IndicatorCommand
                            fs''16
                            \f                                                                       %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r'\dynamicDown')],
        selector=selector,
        )

def dynamic_up(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> IndicatorCommand:
    r"""
    Attaches dynamic-up command.

    ..  container:: example

        Attaches dynamic-up command to leaf 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dynamic('p'),
        ...     baca.dynamic('f', selector=baca.tuplets()[1:2].phead(0)),
        ...     baca.dynamic_up(),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            \dynamicUp                                                               %! IndicatorCommand
                            r8
                            c'16
                            \p                                                                       %! IndicatorCommand
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
                            \f                                                                       %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches dynamic-up command to leaf 0 in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dynamic('p'),
        ...     baca.dynamic('f', selector=baca.tuplets()[1:2].phead(0)),
        ...     baca.dynamic_up(selector=baca.tuplets()[1:2].leaf(0)),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            \p                                                                       %! IndicatorCommand
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
                            \dynamicUp                                                               %! IndicatorCommand
                            fs''16
                            \f                                                                       %! IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r'\dynamicUp')],
        selector=selector,
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
    return scoping.suite(
        not_parts_,
        only_parts_,
        )

def global_fermata(
    description: str = None,
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> GlobalFermataCommand:
    """
    Attaches global fermata.
    """
    return GlobalFermataCommand(
        description=description,
        selector=selector,
        )

def instrument(
    instrument: abjad.Instrument,
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> InstrumentChangeCommand:
    """
    Makes instrument change command.
    """
    if not isinstance(instrument, abjad.Instrument):
        message = f'instrument must be instrument (not {instrument!r}).'
        raise Exception(message)
    return InstrumentChangeCommand(
        indicators=[instrument],
        selector=selector,
        )

def label(
    expression: abjad.Expression,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> LabelCommand:
    r"""
    Labels ``selector`` output with label ``expression``.

    ..  container:: example

        Labels pitch names:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.label(abjad.label().with_pitches(locale='us')),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
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
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Labels pitch names in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.label(
        ...         abjad.label().with_pitches(locale='us'),
        ...         selector=baca.tuplet(1),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
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
                            r4
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return LabelCommand(expression=expression, selector=selector)

def markup(
    argument: typing.Union[str, abjad.Markup],
    *tweaks: abjad.LilyPondTweakManager,
    boxed: bool = None,
    direction: abjad.VerticalAlignment = abjad.Up,
    literal: bool = False,
    selector: typings.Selector = 'baca.pleaf(0)',
    tag: str = 'baca_markup',
    ) -> IndicatorCommand:
    r"""
    Makes markup and inserts into indicator command.

    ..  container:: example

        Attaches markup to pitched head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.markup('più mosso'),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_outside_staff_priority(1000),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.outside-staff-priority = #1000                   %! baca_tuplet_bracket_outside_staff_priority:OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            ^ \markup { "più mosso" }                                                %! baca_markup:IndicatorCommand
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
                            \revert TupletBracket.outside-staff-priority                             %! baca_tuplet_bracket_outside_staff_priority:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
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
        ...     baca.markup(
        ...         'più mosso',
        ...         selector=baca.tuplets()[1:2].phead(0),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_outside_staff_priority(1000),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.outside-staff-priority = #1000                   %! baca_tuplet_bracket_outside_staff_priority:OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
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
                            ^ \markup { "più mosso" }                                                %! baca_markup:IndicatorCommand
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
                            \revert TupletBracket.outside-staff-priority                             %! baca_tuplet_bracket_outside_staff_priority:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
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
        ...     baca.markup(
        ...         '*',
        ...         selector=baca.tuplets()[1:2].pheads(),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_outside_staff_priority(1000),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.outside-staff-priority = #1000                   %! baca_tuplet_bracket_outside_staff_priority:OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
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
                            ^ \markup { * }                                                          %! baca_markup:IndicatorCommand
                            [
                            e''16
                            ^ \markup { * }                                                          %! baca_markup:IndicatorCommand
                            ]
                            ef''4
                            ^ \markup { * }                                                          %! baca_markup:IndicatorCommand
                            ~
                            ef''16
                            r16
                            af''16
                            ^ \markup { * }                                                          %! baca_markup:IndicatorCommand
                            [
                            g''16
                            ^ \markup { * }                                                          %! baca_markup:IndicatorCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.outside-staff-priority                             %! baca_tuplet_bracket_outside_staff_priority:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Set the ``literal=True`` to pass predefined markup commands:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.markup(
        ...         r'\baca-triple-diamond-markup',
        ...         literal=True,
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_outside_staff_priority(1000),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.outside-staff-priority = #1000                   %! baca_tuplet_bracket_outside_staff_priority:OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            ^ \markup { \baca-triple-diamond-markup }                                %! baca_markup:IndicatorCommand
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
                            \revert TupletBracket.outside-staff-priority                             %! baca_tuplet_bracket_outside_staff_priority:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Raises exception on nonstring, nonmarkup ``argument``:

        >>> baca.markup(['Allegro', 'ma non troppo'])
        Traceback (most recent call last):
            ...
        Exception: MarkupLibary.__call__():
            Value of 'argument' must be str or markup.
            Not ['Allegro', 'ma non troppo'].

    """
    if direction not in (abjad.Down, abjad.Up):
        message = f'direction must be up or down (not {direction!r}).'
        raise Exception(message)
    if isinstance(argument, str):
        if literal:
            markup = abjad.Markup.from_literal(
                argument,
                direction=direction,
                )
        else:
            markup = abjad.Markup(argument, direction=direction)
    elif isinstance(argument, abjad.Markup):
        markup = abjad.new(argument, direction=direction)
    else:
        message = 'MarkupLibary.__call__():\n'
        message += "  Value of 'argument' must be str or markup.\n"
        message += f'  Not {argument!r}.'
        raise Exception(message)
    if boxed:
        markup = markup.box().override(('box-padding', 0.5))
    prototype = (str, abjad.Expression)
    if selector is not None and not isinstance(selector, prototype):
        message = f'selector must be string or expression'
        message += f' (not {selector!r}).'
        raise Exception(message)
    selector = selector or 'baca.phead(0)'
    return IndicatorCommand(
        *tweaks,
        indicators=[markup],
        selector=selector,
        tags=[tag],
        )

def metronome_mark(
    key: str,
    *,
    redundant: bool = None,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> typing.Optional[MetronomeMarkCommand]:
    """
    Attaches metronome mark matching ``key`` metronome mark manifest.
    """
    if redundant is True:
        return None
    return MetronomeMarkCommand(
        key=key,
        redundant=redundant,
        selector=selector,
        )

def parts(
    part_assignment: abjad.PartAssignment,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> PartAssignmentCommand:
    r"""
    Inserts ``selector`` output in container and sets part assignment.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.StringTrioScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'ViolinMusicVoice',
        ...     baca.make_notes(),
        ...     baca.parts(abjad.PartAssignment('Violin')),
        ...     baca.pitch('E4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        >>> abjad.f(lilypond_file[abjad.Score], strict=89)
        <BLANKLINE>
        \context Score = "Score"                                                                 %! StringTrioScoreTemplate
        <<                                                                                       %! StringTrioScoreTemplate
        <BLANKLINE>
            \context GlobalContext = "GlobalContext"                                             %! _make_global_context
            <<                                                                                   %! _make_global_context
        <BLANKLINE>
                \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                {                                                                                %! _make_global_context
        <BLANKLINE>
                    % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                    \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 1/2                                                                     %! _make_global_skips(1)
        <BLANKLINE>
                    % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                    \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 3/8                                                                     %! _make_global_skips(1)
        <BLANKLINE>
                    % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                    \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 1/2                                                                     %! _make_global_skips(1)
        <BLANKLINE>
                    % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                    \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                    \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                    s1 * 3/8                                                                     %! _make_global_skips(1)
                    \baca-bar-line-visible                                                       %! _attach_final_bar_line
                    \bar "|"                                                                     %! _attach_final_bar_line
        <BLANKLINE>
                }                                                                                %! _make_global_context
        <BLANKLINE>
            >>                                                                                   %! _make_global_context
        <BLANKLINE>
            \context MusicContext = "MusicContext"                                               %! StringTrioScoreTemplate
            <<                                                                                   %! StringTrioScoreTemplate
        <BLANKLINE>
                \context StringSectionStaffGroup = "String Section Staff Group"                  %! StringTrioScoreTemplate
                <<                                                                               %! StringTrioScoreTemplate
        <BLANKLINE>
                    \tag Violin                                                                  %! ScoreTemplate(5)
                    \context ViolinMusicStaff = "ViolinMusicStaff"                               %! StringTrioScoreTemplate
                    {                                                                            %! StringTrioScoreTemplate
        <BLANKLINE>
                        \context ViolinMusicVoice = "ViolinMusicVoice"                           %! StringTrioScoreTemplate
                        {                                                                        %! StringTrioScoreTemplate
        <BLANKLINE>
                            {   %*% PartAssignment('Violin')
        <BLANKLINE>
                                % [ViolinMusicVoice measure 1]                                   %! _comment_measure_numbers
                                \clef "treble"                                                   %! DEFAULT_CLEF:_set_status_tag:attach_defaults
                                \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                            %@% \override ViolinMusicStaff.Clef.color = ##f                      %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                \set ViolinMusicStaff.forceClef = ##t                            %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):attach_defaults
                                e'2                                                              %! baca_make_notes
                                ^ \baca-default-indicator-markup "(Violin)"                      %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                                \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)     %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
        <BLANKLINE>
                                % [ViolinMusicVoice measure 2]                                   %! _comment_measure_numbers
                                e'4.                                                             %! baca_make_notes
        <BLANKLINE>
                                % [ViolinMusicVoice measure 3]                                   %! _comment_measure_numbers
                                e'2                                                              %! baca_make_notes
        <BLANKLINE>
                                % [ViolinMusicVoice measure 4]                                   %! _comment_measure_numbers
                                e'4.                                                             %! baca_make_notes
        <BLANKLINE>
                            }   %*% PartAssignment('Violin')
        <BLANKLINE>
                        }                                                                        %! StringTrioScoreTemplate
        <BLANKLINE>
                    }                                                                            %! StringTrioScoreTemplate
        <BLANKLINE>
                    \tag Viola                                                                   %! ScoreTemplate(5)
                    \context ViolaMusicStaff = "ViolaMusicStaff"                                 %! StringTrioScoreTemplate
                    {                                                                            %! StringTrioScoreTemplate
        <BLANKLINE>
                        \context ViolaMusicVoice = "ViolaMusicVoice"                             %! StringTrioScoreTemplate
                        {                                                                        %! StringTrioScoreTemplate
        <BLANKLINE>
                            % [ViolaMusicVoice measure 1]                                        %! _comment_measure_numbers
                            \clef "alto"                                                         %! DEFAULT_CLEF:_set_status_tag:attach_defaults
                            \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                        %@% \override ViolaMusicStaff.Clef.color = ##f                           %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                            \set ViolaMusicStaff.forceClef = ##t                                 %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):attach_defaults
                            R1 * 1/2                                                             %! _call_rhythm_commands
                            ^ \baca-default-indicator-markup "(Viola)"                           %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                            \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)          %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
        <BLANKLINE>
                            % [ViolaMusicVoice measure 2]                                        %! _comment_measure_numbers
                            R1 * 3/8                                                             %! _call_rhythm_commands
        <BLANKLINE>
                            % [ViolaMusicVoice measure 3]                                        %! _comment_measure_numbers
                            R1 * 1/2                                                             %! _call_rhythm_commands
        <BLANKLINE>
                            % [ViolaMusicVoice measure 4]                                        %! _comment_measure_numbers
                            R1 * 3/8                                                             %! _call_rhythm_commands
        <BLANKLINE>
                        }                                                                        %! StringTrioScoreTemplate
        <BLANKLINE>
                    }                                                                            %! StringTrioScoreTemplate
        <BLANKLINE>
                    \tag Cello                                                                   %! ScoreTemplate(5)
                    \context CelloMusicStaff = "CelloMusicStaff"                                 %! StringTrioScoreTemplate
                    {                                                                            %! StringTrioScoreTemplate
        <BLANKLINE>
                        \context CelloMusicVoice = "CelloMusicVoice"                             %! StringTrioScoreTemplate
                        {                                                                        %! StringTrioScoreTemplate
        <BLANKLINE>
                            % [CelloMusicVoice measure 1]                                        %! _comment_measure_numbers
                            \clef "bass"                                                         %! DEFAULT_CLEF:_set_status_tag:attach_defaults
                            \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                        %@% \override CelloMusicStaff.Clef.color = ##f                           %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                            \set CelloMusicStaff.forceClef = ##t                                 %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):attach_defaults
                            R1 * 1/2                                                             %! _call_rhythm_commands
                            ^ \baca-default-indicator-markup "(Cello)"                           %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                            \override CelloMusicStaff.Clef.color = #(x11-color 'violet)          %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
        <BLANKLINE>
                            % [CelloMusicVoice measure 2]                                        %! _comment_measure_numbers
                            R1 * 3/8                                                             %! _call_rhythm_commands
        <BLANKLINE>
                            % [CelloMusicVoice measure 3]                                        %! _comment_measure_numbers
                            R1 * 1/2                                                             %! _call_rhythm_commands
        <BLANKLINE>
                            % [CelloMusicVoice measure 4]                                        %! _comment_measure_numbers
                            R1 * 3/8                                                             %! _call_rhythm_commands
        <BLANKLINE>
                        }                                                                        %! StringTrioScoreTemplate
        <BLANKLINE>
                    }                                                                            %! StringTrioScoreTemplate
        <BLANKLINE>
                >>                                                                               %! StringTrioScoreTemplate
        <BLANKLINE>
            >>                                                                                   %! StringTrioScoreTemplate
        <BLANKLINE>
        >>                                                                                       %! StringTrioScoreTemplate

    ..  container:: example

        Raises exception when voice does not allow part assignment:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.StringTrioScoreTemplate(),
        ...     test_container_identifiers=True,
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> part_assignment = abjad.PartAssignment('Flute')

        >>> maker(
        ...     'ViolinMusicVoice',
        ...     baca.make_notes(),
        ...     baca.parts(part_assignment),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        Traceback (most recent call last):
            ...
        Exception: ViolinMusicVoice does not allow Flute part assignment:
            abjad.PartAssignment('Flute')

    """
    if not isinstance(part_assignment, abjad.PartAssignment):
        message = 'part_assignment must be part assignment'
        message += f' (not {part_assignment!r}).'
        raise Exception(message)
    return PartAssignmentCommand(
        part_assignment=part_assignment,
        )

def one_voice(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> IndicatorCommand:
    """
    Makes LilyPond ``\oneVoice`` command.
    """
    literal = abjad.LilyPondLiteral(r'\oneVoice')
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        )

def previous_metadata(path: str) -> typing.Optional[abjad.OrderedDict]:
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
    paths = [_ for _ in paths if not _.name.startswith('.')]
    assert all(_.is_dir() for _ in paths), repr(paths)
    index = paths.index(segment)
    if index == 0:
        return None
    previous_index = index - 1
    previous_segment = paths[previous_index]
    previous_metadata = previous_segment.get_metadata()
    return previous_metadata

def voice_four(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceFour`` command.
    """
    literal = abjad.LilyPondLiteral(r'\voiceFour')
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        )

def voice_one(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceOne`` command.
    """
    literal = abjad.LilyPondLiteral(r'\voiceOne')
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        )

def voice_three(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceThree`` command.
    """
    literal = abjad.LilyPondLiteral(r'\voiceThree')
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        )

def voice_two(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceTwo`` command.
    """
    literal = abjad.LilyPondLiteral(r'\voiceTwo')
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        )

def volta(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> VoltaCommand:
    r"""
    Makes volta container and extends container with ``selector`` output.

    ..  container:: example

        Wraps skips 1 and 2 in volta container:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.RhythmCommand(
        ...         rhythm_maker=rmakers.TaleaRhythmMaker(
        ...             talea=rmakers.Talea(
        ...                 counts=[1, 1, 1, -1],
        ...                 denominator=8,
        ...                 ),
        ...             ),
        ...         ),
        ...     )

        >>> maker(
        ...     'GlobalSkips',
        ...     baca.volta(selector=baca.skips()[1:3]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        \repeat volta 2
                        {
            <BLANKLINE>
                            % [GlobalSkips measure 2]                                                %! _comment_measure_numbers
                            \time 3/8                                                                %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                        %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                 %! _make_global_skips(1)
            <BLANKLINE>
                            % [GlobalSkips measure 3]                                                %! _comment_measure_numbers
                            \time 4/8                                                                %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                        %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                 %! _make_global_skips(1)
            <BLANKLINE>
                        }
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
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
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            e''8
                            [
            <BLANKLINE>
                            g'8
            <BLANKLINE>
                            f''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
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
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            r8
            <BLANKLINE>
                            e''8
                            [
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        Wraps measures 2 and 3 in volta container:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     ('MusicVoice', (1, 3)),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.RhythmCommand(
        ...         rhythm_maker=rmakers.TaleaRhythmMaker(
        ...             talea=rmakers.Talea(
        ...                 counts=[1, 1, 1, -1],
        ...                 denominator=8,
        ...                 ),
        ...             ),
        ...         ),
        ...     )

        >>> maker(
        ...     ('GlobalSkips', (2, 3)),
        ...     baca.volta(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        \repeat volta 2
                        {
            <BLANKLINE>
                            % [GlobalSkips measure 2]                                                %! _comment_measure_numbers
                            \time 3/8                                                                %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                        %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                 %! _make_global_skips(1)
            <BLANKLINE>
                            % [GlobalSkips measure 3]                                                %! _comment_measure_numbers
                            \time 4/8                                                                %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                        %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                 %! _make_global_skips(1)
            <BLANKLINE>
                        }
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
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
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            e''8
                            [
            <BLANKLINE>
                            g'8
            <BLANKLINE>
                            f''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
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
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            R1 * 3/8                                                                 %! _make_measure_silences
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    """
    return VoltaCommand(selector=selector)
