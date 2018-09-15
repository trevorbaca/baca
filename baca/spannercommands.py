import abjad
import typing
from . import classes
from . import commands
from . import scoping
from . import typings


### CLASSES ###

class SpannerCommand(scoping.Command):
    r"""
    Spanner command.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_detach_first',
        '_left_broken',
        '_right_broken',
        '_spanner',
        '_tags',
        '_tweaks',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        deactivate: bool = None,
        detach_first: bool = None,
        left_broken: bool = None,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        right_broken: bool = None,
        scope: scoping.ScopeTyping = None,
        selector: typings.Selector = 'baca.leaves()',
        spanner: abjad.Spanner = None,
        tags: typing.List[typing.Union[str, abjad.Tag, None]] = None,
        tweaks: typing.Tuple[typings.TweaksTyping, ...] = None,
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
        if detach_first is not None:
            detach_first = bool(detach_first)
        self._detach_first = detach_first
        if left_broken is not None:
            left_broken = bool(left_broken)
        self._left_broken = left_broken
        if right_broken is not None:
            right_broken = bool(right_broken)
        self._right_broken = right_broken
        self._spanner = spanner
        self._validate_tweaks(tweaks)
        self._tweaks = tweaks

    ### SPECIAL METHODS ###

    def _call(self, argument=None):
        """
        Calls command on ``argument``.

        Returns spanner (for handoff to piecewise command).
        """
        if argument is None:
            return
        if self.spanner is None:
            return
        if self.selector:
            argument = self.selector(argument)
        leaves = abjad.select(argument).leaves()
        spanner = abjad.new(self.spanner)
        if self.left_broken:
            spanner = abjad.new(spanner, left_broken=self.left_broken)
        if self.right_broken:
            spanner = abjad.new(spanner, right_broken=self.right_broken)
        self._apply_tweaks(spanner, self.tweaks)
        if self.detach_first:
            abjad.detach(
                type(spanner),
                leaves,
                )
        abjad.attach(
            spanner,
            leaves,
            deactivate=self.deactivate,
            tag=self.tag.append('SpannerCommand'),
            )
        return spanner

    ### PUBLIC PROPERTIES ###

    @property
    def detach_first(self) -> typing.Optional[bool]:
        """
        Is true when command detaches existing spanners before attaching new
        ones.
        """
        return self._detach_first

    @property
    def left_broken(self) -> typing.Optional[bool]:
        """
        Is true when spanner is left-broken.
        """
        return self._left_broken

    @property
    def right_broken(self) -> typing.Optional[bool]:
        """
        Is true when spanner is right-broken.
        """
        return self._right_broken

    @property
    def selector(self) -> typing.Optional[abjad.Expression]:
        r"""
        Gets selector.
        """
        return self._selector

    @property
    def spanner(self) -> typing.Optional[abjad.Spanner]:
        r"""
        Gets spanner.

        ..  container:: example

            Ties are smart enough to remove existing ties prior to attach:

            >>> music_maker = baca.MusicMaker()

            >>> contribution = music_maker(
            ...     'Voice_1',
            ...     [[14, 14, 14]],
            ...     counts=[5],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                d''4
                                ~
                                d''16
                                d''4
                                ~
                                d''16
                                d''4
                                ~
                                d''16
                            }
                        }
                    }
                >>

            >>> contribution = music_maker(
            ...     'Voice_1',
            ...     [[14, 14, 14]],
            ...     baca.SpannerCommand(spanner=abjad.Tie()),
            ...     counts=[5],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                d''4
                                ~                                                                        %! SpannerCommand
                                d''16
                                ~                                                                        %! SpannerCommand
                                d''4
                                ~                                                                        %! SpannerCommand
                                d''16
                                ~                                                                        %! SpannerCommand
                                d''4
                                ~                                                                        %! SpannerCommand
                                d''16
                            }
                        }
                    }
                >>

        """
        return self._spanner

    @property
    def tweaks(self) -> typing.Optional[
        typing.Tuple[typings.TweaksTyping, ...]]:
        """
        Gets tweaks.
        """
        return self._tweaks

class SpannerIndicatorCommand(scoping.Command):
    r"""
    Spanner indicator command.

    ..  container:: example

        With music-maker:

        >>> music_maker = baca.MusicMaker(
        ...     baca.slur(
        ...         selector=baca.tuplet(1),
        ...         ),
        ...     )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker('Voice_1', collections)
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            d'16
                            bf'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''16
                            [
                            (                                                                        %! baca_slur:SpannerIndicatorCommand(1)
                            e''16
                            ef''16
                            af''16
                            g''16
                            )                                                                        %! baca_slur:SpannerIndicatorCommand(2)
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'16
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
        ...     'Music_Voice',
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.slur(
        ...         selector=baca.leaves()[4:7],
        ...         ),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                    {                                                                                %! _make_global_context
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
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
                            (                                                                        %! baca_slur:SpannerIndicatorCommand(1)
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            )                                                                        %! baca_slur:SpannerIndicatorCommand(2)
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
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

    ..  container:: example

        >>> baca.SpannerCommand()
        SpannerCommand(selector=baca.leaves(), tags=[])

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_detach_first',
        '_left_broken',
        '_right_broken',
        '_start_indicator',
        '_stop_indicator',
        '_tags',
        '_tweaks',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        deactivate: bool = None,
        detach_first: bool = None,
        left_broken: bool = None,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        right_broken: bool = None,
        scope: scoping.ScopeTyping = None,
        selector: typings.Selector = 'baca.leaves()',
        start_indicator: typing.Any = None,
        stop_indicator: typing.Any = None,
        tags: typing.List[typing.Union[str, abjad.Tag, None]] = None,
        tweaks: typing.Tuple[typings.TweaksTyping, ...] = None,
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
        if detach_first is not None:
            detach_first = bool(detach_first)
        self._detach_first = detach_first
        if left_broken is not None:
            left_broken = bool(left_broken)
        self._left_broken = left_broken
        if right_broken is not None:
            right_broken = bool(right_broken)
        self._right_broken = right_broken
        self._start_indicator = start_indicator
        self._stop_indicator = stop_indicator
        self._validate_tweaks(tweaks)
        self._tweaks = tweaks

    ### SPECIAL METHODS ###

    def _call(self, argument=None):
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if self.start_indicator is None and self.stop_indicator is None:
            return
        if self.selector:
            argument = self.selector(argument)
        if self.start_indicator is not None:
            start_indicator = self.start_indicator
            if self.detach_first:
                for leaf in abjad.iterate(argument).leaves(grace_notes=False):
                    abjad.detach(type(start_indicator), leaf)
            if self.left_broken:
                start_indicator = abjad.new(
                    start_indicator,
                    left_broken=self.left_broken,
                    )
            self._apply_tweaks(start_indicator, self.tweaks)
            first_leaf = abjad.select(argument).leaf(0)
            self._attach_indicator(
                start_indicator,
                first_leaf,
                deactivate=self.deactivate,
                tag='SpannerIndicatorCommand(1)',
                )
        if self.stop_indicator is not None:
            stop_indicator = self.stop_indicator
            if self.detach_first:
                for leaf in abjad.iterate(argument).leaves(grace_notes=False):
                    abjad.detach(type(stop_indicator), leaf)
            if self.right_broken:
                stop_indicator = abjad.new(
                    stop_indicator,
                    right_broken=self.right_broken,
                    )
            last_leaf = abjad.select(argument).leaf(-1)
            self._attach_indicator(
                stop_indicator,
                last_leaf,
                deactivate=self.deactivate,
                tag='SpannerIndicatorCommand(2)',
                )

    ### PRIVATE METHODS ###

    def _attach_indicator(
        self,
        indicator,
        leaf,
        deactivate=None,
        tag=None,
        ):
        # TODO: factor out late import
        from .segmentmaker import SegmentMaker
        assert isinstance(tag, str), repr(tag)
        reapplied = scoping.Command._remove_reapplied_wrappers(
            leaf,
            indicator,
            )
        wrapper = abjad.attach(
            indicator,
            leaf,
            deactivate=deactivate,
            tag=self.tag.append(tag),
            wrapper=True,
            )
        if scoping.compare_persistent_indicators(
            indicator,
            reapplied,
            ):
            status = 'redundant'
            SegmentMaker._treat_persistent_wrapper(
                self.runtime['manifests'],
                wrapper,
                status,
                )

    ### PUBLIC PROPERTIES ###

    @property
    def detach_first(self) -> typing.Optional[bool]:
        """
        Is true when command detaches existing indicator first.
        """
        return self._detach_first

    @property
    def left_broken(self) -> typing.Optional[bool]:
        """
        Is true when spanner is left-broken.
        """
        return self._left_broken

    @property
    def right_broken(self) -> typing.Optional[bool]:
        """
        Is true when spanner is right-broken.
        """
        return self._right_broken

    @property
    def selector(self) -> typing.Optional[abjad.Expression]:
        r"""
        Gets selector.
        """
        return self._selector

    @property
    def start_indicator(self) -> typing.Optional[typing.Any]:
        """
        Gets start indicator.
        """
        return self._start_indicator

    @property
    def stop_indicator(self) -> typing.Optional[typing.Any]:
        """
        Gets stop indicator.
        """
        return self._stop_indicator

    @property
    def tweaks(self) -> typing.Optional[
        typing.Tuple[typings.TweaksTyping, ...]]:
        """
        Gets tweaks.
        """
        return self._tweaks

### FACTORY FUNCTIONS ###

def beam(
    *tweaks: abjad.LilyPondTweakManager,
    selector: typings.Selector = 'baca.tleaves()',
    start_beam: abjad.StartBeam = None,
    stop_beam: abjad.StopBeam = None,
    tag: typing.Optional[str] = 'baca_beam',
    ) -> SpannerIndicatorCommand:
    r"""
    Attaches beam.

    ..  container:: example

        Beams everything:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.beam(),
        ...     baca.make_even_divisions(),
        ...     baca.pitch('C4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
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
                \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            c'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_beam:SpannerIndicatorCommand(1)
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_beam:SpannerIndicatorCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    """
    start_beam = start_beam or abjad.StartBeam()
    stop_beam = stop_beam or abjad.StopBeam()
    return SpannerIndicatorCommand(
        detach_first=True,
        selector=selector,
        start_indicator=start_beam,
        stop_indicator=stop_beam,
        tags=[tag],
        tweaks=tweaks,
        )

def ottava(
    start_ottava: abjad.Ottava = abjad.Ottava(n=1),
    stop_ottava: abjad.Ottava = abjad.Ottava(n=0, format_slot='after'),
    *,
    selector: typings.Selector = 'baca.tleaves()',
    tag: typing.Optional[str] = 'baca_ottava',
    ) -> SpannerCommand:
    r"""
    Attaches ottava indicators.

    ..  container:: example

        Attaches ottava indicators to trimmed leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.ottava(),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            \ottava 1                                                                %! baca_ottava:SpannerIndicatorCommand(1)
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
                            \ottava 0                                                                %! baca_ottava:SpannerIndicatorCommand(2)
                            r4
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return SpannerIndicatorCommand(
        selector=selector,
        start_indicator=start_ottava,
        stop_indicator=stop_ottava,
        tags=[tag],
        )

def ottava_bassa(
    start_ottava: abjad.Ottava = abjad.Ottava(n=-1),
    stop_ottava: abjad.Ottava = abjad.Ottava(n=0, format_slot='after'),
    *,
    selector: typings.Selector = 'baca.tleaves()',
    tag: typing.Optional[str] = 'baca_ottava_bassa',
    ) -> SpannerCommand:
    r"""
    Attaches ottava bassa indicators.

    ..  container:: example

        Attaches ottava bassa indicators to trimmed leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.ottava_bassa(),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            \ottava -1                                                               %! baca_ottava_bassa:SpannerIndicatorCommand(1)
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
                            \ottava 0                                                                %! baca_ottava_bassa:SpannerIndicatorCommand(2)
                            r4
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return SpannerIndicatorCommand(
        selector=selector,
        start_indicator=start_ottava,
        stop_indicator=stop_ottava,
        tags=[tag],
        )

def repeat_tie(
    *,
    selector: typings.Selector = 'baca.qrun(0)',
    tag: typing.Optional[str] = 'baca_repeat_tie',
    ) -> SpannerCommand:
    r"""
    Attaches repeat tie.

    ..  container:: example

        Attaches repeat tie to each equipitch run:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
        ...     baca.new(
        ...         baca.repeat_tie(),
        ...         map=baca.qruns(),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            [
                            c'16
                            \repeatTie                                                               %! baca_repeat_tie:SpannerCommand
                            ]
                            bf'4
                            bf'16
                            \repeatTie                                                               %! baca_repeat_tie:SpannerCommand
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            bf'16
                            [
                            e''16
                            ]
                            e''4
                            \repeatTie                                                               %! baca_repeat_tie:SpannerCommand
                            e''16
                            \repeatTie                                                               %! baca_repeat_tie:SpannerCommand
                            r16
                            fs''16
                            [
                            af''16
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
    return SpannerCommand(
        selector=selector,
        spanner=abjad.Tie(repeat=True),
        tags=[tag],
        )

def repeat_tie_repeat_pitches(
    *,
    tag: typing.Optional[str] = 'baca_repeat_tie_repeat_pitches',
    ) -> SpannerCommand:
    """
    Repeat-ties repeat pitches.
    """
    return SpannerCommand(
        map=classes.selector().ltqruns().nontrivial(),
        selector='baca.qrun(0)',
        spanner=abjad.Tie(repeat=True),
        tags=[tag],
        )

def slur(
    *tweaks: abjad.LilyPondTweakManager,
    selector: typings.Selector = 'baca.tleaves()',
    start_slur: abjad.StartSlur = None,
    stop_slur: abjad.StopSlur = None,
    tag: typing.Optional[str] = 'baca_slur',
    ) -> SpannerIndicatorCommand:
    r"""
    Attaches slur.

    ..  container:: example

        Attaches slur to trimmed leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.slur(),
        ...     baca.slur_down(),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Slur.direction = #down                                         %! baca_slur_down:OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            [
                            (                                                                        %! baca_slur:SpannerIndicatorCommand(1)
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
                            )                                                                        %! baca_slur:SpannerIndicatorCommand(2)
                            r4
                            \revert Slur.direction                                                   %! baca_slur_down:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches slur to trimmed leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.new(
        ...         baca.slur(),
        ...         map=baca.tuplet(1),
        ...         ),
        ...     baca.slur_down(),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Slur.direction = #down                                         %! baca_slur_down:OverrideCommand(1)
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
                            [
                            (                                                                        %! baca_slur:SpannerIndicatorCommand(1)
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            )                                                                        %! baca_slur:SpannerIndicatorCommand(2)
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert Slur.direction                                                   %! baca_slur_down:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    start_slur = start_slur or abjad.StartSlur()
    stop_slur = stop_slur or abjad.StopSlur()
    return SpannerIndicatorCommand(
        selector=selector,
        start_indicator=start_slur,
        stop_indicator=stop_slur,
        tags=[tag],
        tweaks=tweaks,
        )

def sustain_pedal(
    *,
    selector: typings.Selector = 'baca.leaves()',
    tag: typing.Optional[str] = 'baca_sustain_pedal',
    ) -> SpannerCommand:
    r"""
    Attaches sustain pedal.

    ..  container:: example

        Pedals leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.sustain_pedal(),
        ...     baca.sustain_pedal_staff_padding(4),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! baca_sustain_pedal_staff_padding:OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            r8
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
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
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            \revert Staff.SustainPedalLineSpanner.staff-padding                      %! baca_sustain_pedal_staff_padding:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Pedals leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.new(
        ...         baca.sustain_pedal(),
        ...         map=baca.tuplet(1),
        ...         ),
        ...     baca.sustain_pedal_staff_padding(4),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! baca_sustain_pedal_staff_padding:OverrideCommand(1)
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
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            fs''16
                            [
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert Staff.SustainPedalLineSpanner.staff-padding                      %! baca_sustain_pedal_staff_padding:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Pedals leaves in tuplet 1 (leaked to the left):

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.new(
        ...         baca.sustain_pedal(selector=baca.lleaves()),
        ...         map=baca.tuplet(1),
        ...         ),
        ...     baca.sustain_pedal_staff_padding(4),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! baca_sustain_pedal_staff_padding:OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            r16
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
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
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert Staff.SustainPedalLineSpanner.staff-padding                      %! baca_sustain_pedal_staff_padding:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Pedals leaves in tuplet 1 (leaked to the right):

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.new(
        ...         baca.sustain_pedal(selector=baca.rleaves()),
        ...         map=baca.tuplet(1),
        ...         ),
        ...     baca.sustain_pedal_staff_padding(4),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! baca_sustain_pedal_staff_padding:OverrideCommand(1)
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
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            fs''16
                            [
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
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
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            r4
                            \revert Staff.SustainPedalLineSpanner.staff-padding                      %! baca_sustain_pedal_staff_padding:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Pedals leaves in tuplet 1 (leaked wide):

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.new(
        ...         baca.sustain_pedal(selector=baca.wleaves()),
        ...         map=baca.tuplet(1),
        ...         ),
        ...     baca.sustain_pedal_staff_padding(4),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! baca_sustain_pedal_staff_padding:OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            r16
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
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
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            r4
                            \revert Staff.SustainPedalLineSpanner.staff-padding                      %! baca_sustain_pedal_staff_padding:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Pedals leaves in tuplets:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.new(
        ...         baca.sustain_pedal(),
        ...         map=baca.tuplets(),
        ...         ),
        ...     baca.sustain_pedal_staff_padding(4),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! baca_sustain_pedal_staff_padding:OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            r8
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            fs''16
                            [
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            ]
                        }
                        \times 4/5 {
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            a'16
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
                            r4
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            \revert Staff.SustainPedalLineSpanner.staff-padding                      %! baca_sustain_pedal_staff_padding:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Pedals leaves in tuplets (leaked to the left):

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.new(
        ...         baca.sustain_pedal(selector=baca.lleaves()),
        ...         map=baca.tuplets(),
        ...         ),
        ...     baca.sustain_pedal_staff_padding(4),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! baca_sustain_pedal_staff_padding:OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            r8
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            r16
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
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
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            g''16
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            ]
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            \revert Staff.SustainPedalLineSpanner.staff-padding                      %! baca_sustain_pedal_staff_padding:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Pedals leaves in tuplets (leaked to the right):

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.new(
        ...         baca.sustain_pedal(selector=baca.rleaves()),
        ...         map=baca.tuplets(),
        ...         ),
        ...     baca.sustain_pedal_staff_padding(4),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! baca_sustain_pedal_staff_padding:OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            r8
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
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
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            fs''16
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            [
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
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
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            a'16
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
                            r4
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            \revert Staff.SustainPedalLineSpanner.staff-padding                      %! baca_sustain_pedal_staff_padding:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return SpannerCommand(
        selector=selector,
        spanner=abjad.PianoPedalSpanner(style='bracket'),
        tags=[tag],
        )

def tie(
    *,
    map: typings.Selector = None,
    repeat: typing.Union[
        bool,
        typings.IntegerPair,
        abjad.DurationInequality,
        ] = None,
    selector: typings.Selector = 'baca.qrun(0)',
    tag: typing.Optional[str] = 'baca_tie',
    ) -> SpannerCommand:
    r"""
    Attaches tie.

    ..  container:: example

        Attaches ties to equipitch runs:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
        ...     baca.new(
        ...         baca.tie(),
        ...         map=baca.qruns(),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            ~                                                                        %! baca_tie:SpannerCommand
                            [
                            c'16
                            ]
                            bf'4
                            ~                                                                        %! baca_tie:SpannerCommand
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            bf'16
                            [
                            e''16
                            ~                                                                        %! baca_tie:SpannerCommand
                            ]
                            e''4
                            ~                                                                        %! baca_tie:SpannerCommand
                            e''16
                            r16
                            fs''16
                            [
                            af''16
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

        Attaches repeat-threshold ties to equipitch runs:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
        ...     baca.new(
        ...         baca.tie(repeat=(1, 8)),
        ...         map=baca.qruns(),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            ~                                                                        %! baca_tie:SpannerCommand
                            [
                            c'16
                            ]
                            bf'4
                            bf'16
                            \repeatTie                                                               %! baca_tie:SpannerCommand
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            bf'16
                            [
                            e''16
                            ~                                                                        %! baca_tie:SpannerCommand
                            ]
                            e''4
                            e''16
                            \repeatTie                                                               %! baca_tie:SpannerCommand
                            r16
                            fs''16
                            [
                            af''16
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
    tie = abjad.Tie(
        repeat=repeat,
        )
    return SpannerCommand(
        map=map,
        selector=selector,
        spanner=tie,
        tags=[tag],
        )

def tie_repeat_pitches(
    *,
    tag: typing.Optional[str] = 'baca_tie_repeat_pitches',
    ) -> SpannerCommand:
    """
    Ties repeat pitches.
    """
    map = classes.selector().ltqruns().nontrivial()
    command = tie(
        map=map,
        tag=tag,
        )
    return command

def trill_spanner(
    string: str = None,
    *,
    harmonic: bool = None,
    left_broken: bool = None,
    right_broken: bool = None,
    selector: typings.Selector = 'baca.tleaves().with_next_leaf()',
    tag: typing.Optional[str] = 'baca_trill_spanner',
    ) -> SpannerCommand:
    r"""
    Attaches trill spanner.

    ..  container:: example

        Attaches trill spanner to trimmed leaves (leaked to the right):

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.trill_spanner(),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            [
                            \startTrillSpan
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
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches trill spanner to trimmed leaves (leaked to the right) in
        every equipitch run:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.new(
        ...         baca.trill_spanner(),
        ...         map=baca.qruns(),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            [
                            \startTrillSpan
                            d'16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            ]
                            \startTrillSpan
                            bf'4
                            ~
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan
                            bf'16
                            r16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            \startTrillSpan
                            e''16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            ]
                            \startTrillSpan
                            ef''4
                            ~
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan
                            ef''16
                            r16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            af''16
                            [
                            \startTrillSpan
                            g''16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            ]
                            \startTrillSpan
                        }
                        \times 4/5 {
                            a'16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan
                            r4
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches trill to trimmed leaves (leaked to the right) in every
        run:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.new(
        ...         baca.trill_spanner(),
        ...         map=baca.runs(),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            [
                            \startTrillSpan
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            \startTrillSpan
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            af''16
                            [
                            \startTrillSpan
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches pitched trill to trimmed leaves (leaked to the right) in
        equipitch run 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.new(
        ...         baca.trill_spanner(string='Eb4'),
        ...         map=baca.qrun(0),
        ...         ),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            c'16
                            [
                            \startTrillSpan ef'
                            d'16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
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
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches pitched trill to trimmed leaves (leaked to the right) in
        every equipitch run:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.new(
        ...         baca.trill_spanner(string='Eb4'),
        ...         map=baca.qruns(),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            c'16
                            [
                            \startTrillSpan ef'
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            d'16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            ]
                            \startTrillSpan ef'
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            bf'4
                            ~
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan ef'
                            bf'16
                            r16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            fs''16
                            [
                            \startTrillSpan ef'
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            e''16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            ]
                            \startTrillSpan ef'
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            ef''4
                            ~
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan ef'
                            ef''16
                            r16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            af''16
                            [
                            \startTrillSpan ef'
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            g''16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            ]
                            \startTrillSpan ef'
                        }
                        \times 4/5 {
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            a'16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan ef'
                            r4
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches pitched trill (specified by interval) to trimmed leaves
        (leaked to the right) in every equipitch run:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.new(
        ...         baca.trill_spanner(string='M2'),
        ...         map=baca.qruns(),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            c'16
                            [
                            \startTrillSpan d'
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            d'16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            ]
                            \startTrillSpan e'
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            bf'4
                            ~
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan c''
                            bf'16
                            r16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            fs''16
                            [
                            \startTrillSpan gs''
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            e''16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            ]
                            \startTrillSpan fs''
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            ef''4
                            ~
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan f''
                            ef''16
                            r16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            af''16
                            [
                            \startTrillSpan bf''
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            g''16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            ]
                            \startTrillSpan a''
                        }
                        \times 4/5 {
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            a'16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan b'
                            r4
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    if string is None:
        interval = None
        pitch = None
    else:
        try:
            interval = None
            pitch = abjad.NamedPitch(string)
        except ValueError:
            interval = abjad.NamedInterval(string)
            pitch = None
    return SpannerCommand(
        left_broken=left_broken,
        right_broken=right_broken,
        spanner=abjad.TrillSpanner(
            interval=interval,
            is_harmonic=harmonic,
            pitch=pitch,
            ),
        selector=selector,
        tags=[tag],
        )
