"""
Spanners.
"""
import dataclasses
import typing
from inspect import currentframe as _frame

import abjad

from . import scoping as _scoping
from . import selectors as _selectors
from . import tags as _tags


@dataclasses.dataclass
class SpannerIndicatorCommand(_scoping.Command):
    """
    Spanner indicator command.
    """

    detach_first: bool = False
    left_broken: bool = False
    right_broken: bool = False
    start_indicator: typing.Any = None
    stop_indicator: typing.Any = None
    tweaks: abjad.IndexedTweakManagers = ()

    def __post_init__(self):
        _scoping.Command.__post_init__(self)
        self.detach_first = bool(self.detach_first)
        self.left_broken = bool(self.left_broken)
        self.right_broken = bool(self.right_broken)
        _scoping.validate_indexed_tweaks(self.tweaks)

    def _call(self, argument=None):
        if argument is None:
            return
        if self.start_indicator is None and self.stop_indicator is None:
            return
        if self.selector:
            argument = self.selector(argument)
        if self.start_indicator is not None:
            start_indicator = self.start_indicator
            if self.detach_first:
                for leaf in abjad.iterate.leaves(argument, grace=False):
                    abjad.detach(type(start_indicator), leaf)
            _scoping.apply_tweaks(start_indicator, self.tweaks)
            first_leaf = abjad.select.leaf(argument, 0)
            if self.left_broken:
                self._attach_indicator(
                    start_indicator,
                    first_leaf,
                    deactivate=self.deactivate,
                    tag=_scoping.site(_frame(), self, n=1)
                    .append(_tags.SPANNER_START)
                    .append(_tags.LEFT_BROKEN),
                )
            else:
                self._attach_indicator(
                    start_indicator,
                    first_leaf,
                    deactivate=self.deactivate,
                    tag=_scoping.site(_frame(), self, n=2).append(_tags.SPANNER_START),
                )
        if self.stop_indicator is not None:
            stop_indicator = self.stop_indicator
            if self.detach_first:
                for leaf in abjad.iterate.leaves(argument, grace=False):
                    abjad.detach(type(stop_indicator), leaf)
            final_leaf = abjad.select.leaf(argument, -1)
            if self.right_broken:
                self._attach_indicator(
                    stop_indicator,
                    final_leaf,
                    deactivate=self.deactivate,
                    tag=_scoping.site(_frame(), self, n=3)
                    .append(_tags.SPANNER_STOP)
                    .append(_tags.RIGHT_BROKEN),
                )
            else:
                self._attach_indicator(
                    stop_indicator,
                    final_leaf,
                    deactivate=self.deactivate,
                    tag=_scoping.site(_frame(), self, n=4).append(_tags.SPANNER_STOP),
                )

    def _attach_indicator(self, indicator, leaf, deactivate=None, tag=None):
        assert isinstance(tag, abjad.Tag), repr(tag)
        reapplied = _scoping.remove_reapplied_wrappers(leaf, indicator)
        tag_ = self.tag.append(tag)
        wrapper = abjad.attach(
            indicator, leaf, deactivate=deactivate, tag=tag_, wrapper=True
        )
        if _scoping.compare_persistent_indicators(indicator, reapplied):
            status = "redundant"
            _scoping.treat_persistent_wrapper(
                self.runtime["manifests"], wrapper, status
            )


def beam(
    *tweaks: abjad.TweakInterface,
    direction: int = None,
    selector=_selectors.tleaves(),
    start_beam: abjad.StartBeam = None,
    stop_beam: abjad.StopBeam = None,
) -> SpannerIndicatorCommand:
    r"""
    Attaches beam.

    ..  container:: example

        Beams everything and sets beam direction down:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.beam(
        ...         direction=abjad.Down,
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitch("C4"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        c'8
                        _ [
                        c'8
                        c'8
                        c'8
                        c'8
                        c'8
                        c'8
                        c'8
                        c'8
                        c'8
                        c'8
                        c'8
                        c'8
                        c'8
                        ]
                    }
                >>
            }

    """
    start_beam = start_beam or abjad.StartBeam(direction=direction)
    stop_beam = stop_beam or abjad.StopBeam()
    return SpannerIndicatorCommand(
        detach_first=True,
        selector=selector,
        start_indicator=start_beam,
        stop_indicator=stop_beam,
        tags=[_scoping.site(_frame())],
        tweaks=tweaks,
    )


def ottava(
    start_ottava: abjad.Ottava = abjad.Ottava(n=1),
    stop_ottava: abjad.Ottava = abjad.Ottava(n=0, format_slot="after"),
    *,
    right_broken: bool = False,
    selector=_selectors.tleaves(),
) -> SpannerIndicatorCommand:
    r"""
    Attaches ottava indicators.

    ..  container:: example

        Attaches ottava indicators to trimmed leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.ottava(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        \ottava 1
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
                    \times 9/10
                    {
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
                    \times 4/5
                    {
                        a'16
                        \ottava 0
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return SpannerIndicatorCommand(
        right_broken=right_broken,
        selector=selector,
        start_indicator=start_ottava,
        stop_indicator=stop_ottava,
        tags=[_scoping.site(_frame())],
    )


def ottava_bassa(
    start_ottava: abjad.Ottava = abjad.Ottava(n=-1),
    stop_ottava: abjad.Ottava = abjad.Ottava(n=0, format_slot="after"),
    *,
    selector=_selectors.tleaves(),
) -> SpannerIndicatorCommand:
    r"""
    Attaches ottava bassa indicators.

    ..  container:: example

        Attaches ottava bassa indicators to trimmed leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.ottava_bassa(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        \ottava -1
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
                    \times 9/10
                    {
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
                    \times 4/5
                    {
                        a'16
                        \ottava 0
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return SpannerIndicatorCommand(
        selector=selector,
        start_indicator=start_ottava,
        stop_indicator=stop_ottava,
        tags=[_scoping.site(_frame())],
    )


def slur(
    *tweaks: abjad.TweakInterface,
    map=None,
    phrasing_slur=False,
    selector=_selectors.tleaves(),
    start_slur: abjad.StartSlur = None,
    stop_slur: abjad.StopSlur = None,
) -> SpannerIndicatorCommand:
    r"""
    Attaches slur.

    ..  container:: example

        Attaches slur to trimmed leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.slur(),
        ...     baca.slur_down(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override Slur.direction = #down
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        (
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
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
                    \times 4/5
                    {
                        a'16
                        )
                        r4
                        \revert Slur.direction
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    if phrasing_slur is True:
        start_slur_ = start_slur or abjad.StartPhrasingSlur()
        stop_slur_ = stop_slur or abjad.StopPhrasingSlur()
    else:
        start_slur_ = start_slur or abjad.StartSlur()
        stop_slur_ = stop_slur or abjad.StopSlur()
    return SpannerIndicatorCommand(
        map=map,
        selector=selector,
        start_indicator=start_slur_,
        stop_indicator=stop_slur_,
        tags=[_scoping.site(_frame())],
        tweaks=tweaks,
    )


def sustain_pedal(
    *,
    selector=_selectors.leaves(),
    start_piano_pedal: abjad.StartPianoPedal = None,
    stop_piano_pedal: abjad.StopPianoPedal = None,
) -> SpannerIndicatorCommand:
    r"""
    Attaches sustain pedal indicators.

    ..  container:: example

        Pedals leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.sustain_pedal(),
        ...     baca.sustain_pedal_staff_padding(4),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override Staff.SustainPedalLineSpanner.staff-padding = 4
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        \sustainOn
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
                    \times 9/10
                    {
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
                    \times 4/5
                    {
                        a'16
                        r4
                        \sustainOff
                        \revert Staff.SustainPedalLineSpanner.staff-padding
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    start_piano_pedal = start_piano_pedal or abjad.StartPianoPedal()
    stop_piano_pedal = stop_piano_pedal or abjad.StopPianoPedal()
    return SpannerIndicatorCommand(
        selector=selector,
        start_indicator=start_piano_pedal,
        stop_indicator=stop_piano_pedal,
        tags=[_scoping.site(_frame())],
    )


def trill_spanner(
    *tweaks: abjad.TweakInterface,
    alteration: str = None,
    harmonic: bool = False,
    left_broken: bool = False,
    map=None,
    right_broken: bool = False,
    selector=_selectors.tleaves(rleak=True),
    start_trill_span: abjad.StartTrillSpan = None,
    stop_trill_span: abjad.StopTrillSpan = None,
) -> SpannerIndicatorCommand:
    r"""
    Attaches trill spanner indicators.

    ..  container:: example

        Attaches trill spanner to trimmed leaves (leaked to the right):

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.trill_spanner(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
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
                    \times 9/10
                    {
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
                    \times 4/5
                    {
                        a'16
                        r4
                        \stopTrillSpan
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Attaches trill to trimmed leaves (leaked to the right) in every
        run:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.trill_spanner(),
        ...         map=baca.selectors.runs(),
        ...     ),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
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
                        \stopTrillSpan
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        \startTrillSpan
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        \stopTrillSpan
                        af''16
                        [
                        \startTrillSpan
                        g''16
                        \stopTrillSpan
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        \startTrillSpan
                        r4
                        \stopTrillSpan
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Tweaks trill spanner:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.trill_spanner(
        ...             abjad.tweak("#red").color,
        ...             alteration='M2',
        ...         ),
        ...     ),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        \pitchedTrill
                        c'16
                        [
                        - \tweak color #red
                        \startTrillSpan d'
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
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
                    \times 4/5
                    {
                        a'16
                        r4
                        \stopTrillSpan
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    if alteration is not None:
        prototype = (abjad.NamedPitch, abjad.NamedInterval, str)
        if not isinstance(alteration, prototype):
            message = "trill spanner 'alteration' must be pitch, interval, str:"
            message += f"\n   {alteration}"
            raise Exception(message)
    interval = pitch = None
    if alteration is not None:
        try:
            pitch = abjad.NamedPitch(alteration)
        except Exception:
            try:
                interval = abjad.NamedInterval(alteration)
            except Exception:
                pass
    start_trill_span = start_trill_span or abjad.StartTrillSpan()
    if pitch is not None or interval is not None:
        start_trill_span = dataclasses.replace(
            start_trill_span, interval=interval, pitch=pitch
        )
    if harmonic is True:
        string = "#(lambda (grob) (grob-interpret-markup grob"
        string += r' #{ \markup \musicglyph #"noteheads.s0harmonic" #}))'
        abjad.tweak(start_trill_span).TrillPitchHead.stencil = string
    stop_trill_span = stop_trill_span or abjad.StopTrillSpan()
    return SpannerIndicatorCommand(
        left_broken=left_broken,
        map=map,
        right_broken=right_broken,
        selector=selector,
        start_indicator=start_trill_span,
        stop_indicator=stop_trill_span,
        tags=[_scoping.site(_frame())],
        tweaks=tweaks,
    )