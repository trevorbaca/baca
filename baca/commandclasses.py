"""
Command classes.
"""
import collections
import typing

import abjad

from . import const, indicators
from . import parts as _parts
from . import scoping
from . import selection as _selection
from . import sequence as _sequence
from . import tags as _tags
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
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        scope: scoping.ScopeTyping = None,
        selector: abjad.Expression = None,
        tags: typing.List[typing.Optional[abjad.Tag]] = None,
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
        bcps_ = _sequence.Sequence(self.bcps)
        if self.helper:
            bcps_ = self.helper(bcps_, argument)
        bcps = abjad.CyclicTuple(bcps_)
        lts = _selection.Selection(argument).lts()
        assert isinstance(lts, _selection.Selection)
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
        if self.final_spanner and not self._is_rest(lts[-1]) and len(lts[-1]) == 1:
            next_leaf_after_argument = abjad.get.leaf(lts[-1][-1], 1)
            if next_leaf_after_argument is None:
                message = "can not attach final spanner:"
                message += " argument includes end of score."
                raise Exception(message)
        previous_bcp = None
        i = 0
        for lt in lts:
            stop_text_span = abjad.StopTextSpan(command=self.stop_command)
            if not self.final_spanner and lt is lts[-1] and not self._is_rest(lt.head):
                abjad.attach(
                    stop_text_span,
                    lt.head,
                    tag=self.tag.append(abjad.Tag("baca.BCPCommand._call(1)")),
                )
                break
            previous_leaf = abjad.get.leaf(lt.head, -1)
            next_leaf = abjad.get.leaf(lt.head, 1)
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
                    tag=self.tag.append(abjad.Tag("baca.BCPCommand._call(2)")),
                )
            if 0 < i - 1:
                abjad.attach(
                    stop_text_span,
                    lt.head,
                    tag=self.tag.append(abjad.Tag("baca.BCPCommand._call(3)")),
                )
            if lt is lts[-1] and self.final_spanner:
                abjad.attach(
                    stop_text_span,
                    next_leaf_after_argument,
                    tag=self.tag.append(abjad.Tag("baca.BCPCommand._call(4)")),
                )
            bcp_fraction = abjad.Fraction(*bcp)
            next_bcp_fraction = abjad.Fraction(*bcps[i])
            if self._is_rest(lt.head):
                pass
            elif self._is_rest(previous_leaf) or previous_bcp is None:
                if bcp_fraction > next_bcp_fraction:
                    articulation = abjad.Articulation("upbow")
                    if self.bow_change_tweaks:
                        self._apply_tweaks(articulation, self.bow_change_tweaks)
                    abjad.attach(
                        articulation,
                        lt.head,
                        tag=self.tag.append(abjad.Tag("baca.BCPCommand._call(5)")),
                    )
                elif bcp_fraction < next_bcp_fraction:
                    articulation = abjad.Articulation("downbow")
                    if self.bow_change_tweaks:
                        self._apply_tweaks(articulation, self.bow_change_tweaks)
                    abjad.attach(
                        articulation,
                        lt.head,
                        tag=self.tag.append(abjad.Tag("baca.BCPCommand._call(6)")),
                    )
            else:
                previous_bcp_fraction = abjad.Fraction(*previous_bcp)
                if previous_bcp_fraction < bcp_fraction > next_bcp_fraction:
                    articulation = abjad.Articulation("upbow")
                    if self.bow_change_tweaks:
                        self._apply_tweaks(articulation, self.bow_change_tweaks)
                    abjad.attach(
                        articulation,
                        lt.head,
                        tag=self.tag.append(abjad.Tag("baca.BCPCommand._call(7)")),
                    )
                elif previous_bcp_fraction > bcp_fraction < next_bcp_fraction:
                    articulation = abjad.Articulation("downbow")
                    if self.bow_change_tweaks:
                        self._apply_tweaks(articulation, self.bow_change_tweaks)
                    abjad.attach(
                        articulation,
                        lt.head,
                        tag=self.tag.append(abjad.Tag("baca.BCPCommand._call(8)")),
                    )
            previous_bcp = bcp

    ### PRIVATE METHODS ###

    @staticmethod
    def _is_rest(argument):
        prototype = (abjad.Rest, abjad.MultimeasureRest, abjad.Skip)
        if isinstance(argument, prototype):
            return True
        annotation = abjad.get.annotation(argument, "is_sounding")
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
            ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 16)),
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
                                - \baca-bcp-spanner-left-text #2 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                e'8
                                - \downbow
                                \bacaStopTextSpanBCP
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #1 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                f'8
                                - \upbow
                                \bacaStopTextSpanBCP
                                ]
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #2 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                % [Music_Voice measure 2]
                                e'8
                                - \downbow
                                \bacaStopTextSpanBCP
                                [
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #1 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                f'8
                                - \upbow
                                \bacaStopTextSpanBCP
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #2 #5
                                - \baca-bcp-spanner-right-text #1 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                e'8
                                \bacaStopTextSpanBCP
                                ]
                <BLANKLINE>
                                % [Music_Voice measure 3]
                                f'8
                                - \downbow
                                [
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #3 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                e'8
                                - \upbow
                                \bacaStopTextSpanBCP
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #4 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                f'8
                                - \downbow
                                \bacaStopTextSpanBCP
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #3 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                e'8
                                - \upbow
                                \bacaStopTextSpanBCP
                                ]
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #4 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                % [Music_Voice measure 4]
                                f'8
                                - \downbow
                                \bacaStopTextSpanBCP
                                [
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #3 #5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                e'8
                                - \upbow
                                \bacaStopTextSpanBCP
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #4 #5
                                - \baca-bcp-spanner-right-text #3 #5
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
            ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 16)),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.make_even_divisions(),
            ...     baca.bcps(
            ...         [(1, 5), (2, 5)],
            ...         abjad.tweak("#red").color,
            ...         abjad.tweak(2.5).staff_padding,
            ...         ),
            ...     baca.pitches('E4 F4'),
            ...     baca.script_staff_padding(5),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            Style LilyPond ``Script`` grob with overrides (instead of tweaks).

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
                                \override Script.staff-padding = 5
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
                                - \tweak color #red
                                - \tweak staff-padding 2.5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                f'8
                                - \upbow
                                \bacaStopTextSpanBCP
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #2 #5
                                - \tweak color #red
                                - \tweak staff-padding 2.5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                e'8
                                - \downbow
                                \bacaStopTextSpanBCP
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #1 #5
                                - \tweak color #red
                                - \tweak staff-padding 2.5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                f'8
                                - \upbow
                                \bacaStopTextSpanBCP
                                ]
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #2 #5
                                - \tweak color #red
                                - \tweak staff-padding 2.5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                % [Music_Voice measure 2]
                                e'8
                                - \downbow
                                \bacaStopTextSpanBCP
                                [
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #1 #5
                                - \tweak color #red
                                - \tweak staff-padding 2.5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                f'8
                                - \upbow
                                \bacaStopTextSpanBCP
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #2 #5
                                - \tweak color #red
                                - \tweak staff-padding 2.5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                e'8
                                - \downbow
                                \bacaStopTextSpanBCP
                                ]
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #1 #5
                                - \tweak color #red
                                - \tweak staff-padding 2.5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                % [Music_Voice measure 3]
                                f'8
                                - \upbow
                                \bacaStopTextSpanBCP
                                [
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #2 #5
                                - \tweak color #red
                                - \tweak staff-padding 2.5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                e'8
                                - \downbow
                                \bacaStopTextSpanBCP
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #1 #5
                                - \tweak color #red
                                - \tweak staff-padding 2.5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                f'8
                                - \upbow
                                \bacaStopTextSpanBCP
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #2 #5
                                - \tweak color #red
                                - \tweak staff-padding 2.5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                e'8
                                - \downbow
                                \bacaStopTextSpanBCP
                                ]
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #1 #5
                                - \tweak color #red
                                - \tweak staff-padding 2.5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                % [Music_Voice measure 4]
                                f'8
                                - \upbow
                                \bacaStopTextSpanBCP
                                [
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #2 #5
                                - \tweak color #red
                                - \tweak staff-padding 2.5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                e'8
                                - \downbow
                                \bacaStopTextSpanBCP
                                - \abjad-solid-line-with-arrow
                                - \baca-bcp-spanner-left-text #1 #5
                                - \baca-bcp-spanner-right-text #2 #5
                                - \tweak color #red
                                - \tweak staff-padding 2.5
                                \bacaStartTextSpanBCP
                <BLANKLINE>
                                f'8
                                \bacaStopTextSpanBCP
                                ]
                                \revert Script.staff-padding
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

            REGRESSION. Tweaks survive copy:

            >>> command = baca.bcps(
            ...     [(1, 2), (1, 4)],
            ...     abjad.tweak("#red").color,
            ...     )
            >>> string = abjad.storage(command)
            >>> print(string)
            baca.BCPCommand(
                bcps=[
                    (1, 2),
                    (1, 4),
                    ],
                selector=...,
                tags=[
                    abjad.Tag('baca.bcps()'),
                    ],
                tweaks=(
                    TweakInterface(('_literal', None), ('color', '#red')),
                    ),
                )

            >>> new_command = abjad.new(command)
            >>> string = abjad.storage(new_command)
            >>> print(string)
            baca.BCPCommand(
                bcps=[
                    (1, 2),
                    (1, 4),
                    ],
                selector=...,
                tags=[
                    abjad.Tag('baca.bcps()'),
                    ],
                tweaks=(
                    TweakInterface(('_literal', None), ('color', '#red')),
                    ),
                )

        """
        return self._tweaks


class ColorCommand(scoping.Command):
    """
    Color command.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("lone",)

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        lone: bool = None,
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        scope: scoping.ScopeTyping = None,
        selector=lambda _: _selection.Selection(_).leaves(),
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
        self.lone = lone

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        assert self.selector is not None
        argument = self.selector(argument)
        abjad.Label(argument).by_selector(self.selector, lone=self.lone)


class ContainerCommand(scoping.Command):
    r"""
    Container command.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.container('ViolinI', selector=baca.selectors.leaves((None, 2))),
        ...     baca.container('ViolinII', selector=baca.selectors.leaves((2, None))),
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

    ### CLASS VARIABLES ###

    __slots__ = ("_identifier",)

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        identifier: str = None,
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        scope: scoping.ScopeTyping = None,
        selector=lambda _: _selection.Selection(_).leaves(),
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
        components = _selection.Selection(argument).leaves().top()
        abjad.mutate.wrap(components, container)

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
        >>> baca.DetachCommand(arguments, baca.selectors.leaves())
        DetachCommand([RepeatTie, Tie], ...)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_arguments",)

    ### INITIALIZER ###

    def __init__(
        self,
        arguments: typing.Sequence[typing.Any],
        selector: abjad.Expression,
        map: abjad.Expression = None,
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
        leaves = _selection.Selection(argument).leaves()
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
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_allow_repeats",
        "_allow_ties",
        "_hide_middle_note_heads",
        "_hide_middle_stems",
        "_hide_stem_selector",
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
        hide_stem_selector: typing.Callable = None,
        left_broken: bool = None,
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        parenthesize_repeats: bool = None,
        right_broken: bool = None,
        right_broken_show_next: bool = None,
        scope: scoping.ScopeTyping = None,
        selector=lambda _: _selection.Selection(_).tleaves(),
        tags: typing.List[typing.Optional[abjad.Tag]] = None,
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
        self._hide_stem_selector = hide_stem_selector
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
        leaves = _selection.Selection(argument).leaves()
        tweaks_: typing.List[abjad.IndexedTweakManager] = []
        prototype = (abjad.TweakInterface, tuple)
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
            hide_stem_selector=self.hide_stem_selector,
            left_broken=self.left_broken,
            parenthesize_repeats=self.parenthesize_repeats,
            right_broken=self.right_broken,
            right_broken_show_next=self.right_broken_show_next,
            tag=self.tag,
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
    def hide_stem_selector(self) -> typing.Optional[typing.Callable]:
        """
        Gets hide-stem selector.
        """
        return self._hide_stem_selector

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
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        scope: scoping.ScopeTyping = None,
        selector=lambda _: _selection.Selection(_).leaf(0),
        tags: typing.List[typing.Optional[abjad.Tag]] = None,
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
                markup,
                leaf,
                tag=self.tag.append(abjad.Tag("baca.GlobalFermataCommand._call(1)")),
            )
            literal = abjad.LilyPondLiteral(r"\baca-fermata-measure")
            abjad.attach(
                literal,
                leaf,
                tag=self.tag.append(abjad.Tag("baca.GlobalFermataCommand._call(2)")),
            )
            tag = abjad.Tag(const.FERMATA_MEASURE)
            tag = tag.append(self.tag)
            tag = tag.append(abjad.Tag("baca.GlobalFermataCommand._call(3)"))
            abjad.attach(
                const.FERMATA_MEASURE,
                leaf,
                tag=_tags.FERMATA_MEASURE,
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
        indicators: typing.List[typing.Any],
        *,
        context: str = None,
        deactivate: bool = None,
        do_not_test: bool = None,
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        predicate: typing.Callable = None,
        redundant: bool = None,
        scope: scoping.ScopeTyping = None,
        selector=lambda _: _selection.Selection(_).pheads(),
        tags: typing.List[typing.Optional[abjad.Tag]] = None,
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
        leaves = _selection.Selection(argument).leaves()
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
                    tag=self.tag.append(abjad.Tag("baca.IndicatorCommand._call()")),
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
        first_leaf = abjad.get.leaf(argument, 0)
        if first_leaf is not None:
            staff = abjad.get.parentage(first_leaf).get(abjad.Staff)
            assert isinstance(staff, abjad.Staff)
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

    __slots__ = ("_callable",)

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        callable_=None,
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        scope: scoping.ScopeTyping = None,
        selector=lambda _: _selection.Selection(_).leaves(),
    ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
        )
        self._callable = callable_

    ### SPECIAL METHODS ###

    def _call(self, argument=None):
        """
        Calls command on ``argument``.

        Returns none.
        """
        if argument is None:
            return
        if self.callable_ is None:
            return
        if self.selector:
            argument = self.selector(argument)
        self.callable_(argument)

    ### PUBLIC PROPERTIES ###

    @property
    def callable_(self):
        """
        Gets callable.
        """
        return self._callable


class MetronomeMarkCommand(scoping.Command):
    """
    Metronome mark command.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_key", "_redundant", "_tags")

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        deactivate: bool = None,
        key: typing.Union[str, indicators.Accelerando, indicators.Ritardando] = None,
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        redundant: bool = None,
        scope: scoping.ScopeTyping = None,
        selector=lambda _: _selection.Selection(_).leaf(0),
        tags: typing.List[typing.Optional[abjad.Tag]] = None,
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
        leaf = _selection.Selection(argument).leaf(0)
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
        self,
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
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        part_assignment: _parts.PartAssignment = None,
        scope: scoping.ScopeTyping = None,
        selector=lambda _: _selection.Selection(_).leaves(),
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
            if not isinstance(part_assignment, _parts.PartAssignment):
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
        first_leaf = abjad.get.leaf(argument, 0)
        if first_leaf is None:
            return
        voice = abjad.get.parentage(first_leaf).get(abjad.Voice, -1)
        if voice is not None and self.part_assignment is not None:
            assert isinstance(voice, abjad.Voice)
            if not self.runtime["score_template"].allows_part_assignment(
                voice.name, self.part_assignment
            ):
                message = f"{voice.name} does not allow"
                message += f" {self.part_assignment.section} part assignment:"
                message += f"\n  {self.part_assignment}"
                raise Exception(message)
        identifier = f"%*% {self.part_assignment!s}"
        container = abjad.Container(identifier=identifier)
        components = _selection.Selection(argument).leaves().top()
        abjad.mutate.wrap(components, container)

    ### PRIVATE METHODS ###

    def _mutates_score(self):
        # return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def part_assignment(self) -> typing.Optional[_parts.PartAssignment]:
        """
        Gets part assignment.
        """
        return self._part_assignment
