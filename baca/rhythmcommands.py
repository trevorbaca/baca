"""
Rhythm commands.
"""
import inspect
import typing

import abjad
from abjadext import rmakers

from . import classes, const, overrides, scoping
from . import sequence as _sequence
from . import tags as _tags
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
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
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
                            \baca-not-yet-pitched-coloring
                            b'8
                            [
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring
                            b'8
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring
                            b'8
                            ]
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            \baca-not-yet-pitched-coloring
                            b'8
                            [
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring
                            b'8
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring
                            b'8
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring
                            b'8
                            ]
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            \baca-not-yet-pitched-coloring
                            b'8
                            [
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring
                            b'8
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring
                            b'8
                            ]
            <BLANKLINE>
                            % [Music_Voice measure 4]
                            \baca-not-yet-pitched-coloring
                            b'8
                            [
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring
                            b'8
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring
                            b'8
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring
                            b'8
                            ]
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

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        "_annotation_spanner_color",
        "_annotation_spanner_text",
        "_attach_not_yet_pitched",
        "_do_not_check_total_duration",
        "_frame",
        "_persist",
        "_rhythm_maker",
        "_state",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        rhythm_maker: RhythmMakerTyping,
        *,
        annotation_spanner_color: str = None,
        annotation_spanner_text: str = None,
        attach_not_yet_pitched: bool = None,
        do_not_check_total_duration: bool = None,
        frame=None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        persist: str = None,
        scope: scoping.ScopeTyping = None,
    ) -> None:
        scoping.Command.__init__(self, match=match, measures=measures, scope=scope)
        if annotation_spanner_color is not None:
            assert isinstance(annotation_spanner_color, str)
        self._annotation_spanner_color = annotation_spanner_color
        if annotation_spanner_text is not None:
            assert isinstance(annotation_spanner_text, str)
        self._annotation_spanner_text = annotation_spanner_text
        if attach_not_yet_pitched is not None:
            attach_not_yet_pitched = bool(attach_not_yet_pitched)
        self._attach_not_yet_pitched = attach_not_yet_pitched
        if do_not_check_total_duration is not None:
            do_not_check_total_duration = bool(do_not_check_total_duration)
        self._do_not_check_total_duration = do_not_check_total_duration
        if persist is not None:
            assert isinstance(persist, str), repr(persist)
        self._persist = persist
        self._check_rhythm_maker_input(rhythm_maker)
        self._frame = frame
        self._rhythm_maker = rhythm_maker
        self._state: typing.Optional[abjad.OrderedDict] = None

    ### PRIVATE METHODS ###

    @staticmethod
    def _attach_not_yet_pitched_(argument):
        rest_prototype = (abjad.MultimeasureRest, abjad.Rest, abjad.Skip)
        for leaf in abjad.iterate(argument).leaves():
            if isinstance(leaf, (abjad.Note, abjad.Chord)):
                abjad.attach(const.NOT_YET_PITCHED, leaf, tag=None)
            elif isinstance(leaf, rest_prototype):
                pass
            else:
                raise TypeError(leaf)

    def _attach_rhythm_annotation_spanner(self, selection):
        from . import piecewise

        if not self.annotation_spanner_text and not self.frame:
            return
        leaves = []
        for leaf in abjad.iterate(selection).leaves():
            if abjad.get.parentage(leaf).get(abjad.OnBeatGraceContainer):
                continue
            leaves.append(leaf)
        container = abjad.get.before_grace_container(leaves[0])
        if container is not None:
            leaves_ = abjad.select(container).leaves()
            leaves[0:0] = leaves_
        container = abjad.get.after_grace_container(leaves[-1])
        if container is not None:
            leaves_ = abjad.select(container).leaves()
            leaves.extend(leaves_)
        string = self.annotation_spanner_text
        if string is None:
            string = self._make_rhythm_annotation_string()
        color = self.annotation_spanner_color or "#darkyellow"
        command = piecewise.rhythm_annotation_spanner(
            string,
            abjad.tweak(color).color,
            abjad.tweak(8).staff_padding,
            leak_spanner_stop=True,
            selector=lambda _: classes.Selection(_).leaves(),
        )
        command(leaves)

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
        message += f"\n    {abjad.storage(rhythm_maker)}"
        raise Exception(message)

    def _make_rhythm_annotation_string(self):
        if not self.frame:
            return
        frame_info = inspect.getframeinfo(self.frame)
        function_name = frame_info.function
        wrapped_arguments = abjad.Expression._wrap_arguments(self.frame)
        string = f"{function_name}({wrapped_arguments}) =|"
        return string

    def _make_selection(
        self,
        time_signatures: typing.Sequence[abjad.IntegerPair],
        runtime: abjad.OrderedDict = None,
    ) -> abjad.Selection:
        """
        Calls ``RhythmCommand`` on ``time_signatures``.
        """
        rhythm_maker = self.rhythm_maker
        selection: abjad.Selection
        if isinstance(rhythm_maker, abjad.Selection):
            selection = rhythm_maker
            total_duration = sum([_.duration for _ in time_signatures])
            selection_duration = abjad.get.duration(selection)
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
            previous_segment_stop_state = self._previous_segment_stop_state(runtime)
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
        if self.attach_not_yet_pitched or not isinstance(
            self.rhythm_maker, abjad.Selection
        ):
            container = abjad.Container(selection, name="Dummy")
            self._attach_not_yet_pitched_(container)
            container[:] = []
        self._attach_rhythm_annotation_spanner(selection)
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
    def annotation_spanner_color(self) -> typing.Optional[str]:
        """
        Gets annotation spanner color.
        """
        return self._annotation_spanner_color

    @property
    def annotation_spanner_text(self) -> typing.Optional[str]:
        """
        Gets annotation spanner text.
        """
        return self._annotation_spanner_text

    @property
    def attach_not_yet_pitched(self) -> typing.Optional[bool]:
        """
        Is true when command attaches NOT_YET_PITCHED indicator.
        """
        return self._attach_not_yet_pitched

    @property
    def do_not_check_total_duration(self) -> typing.Optional[bool]:
        """
        Is true when command does not check total duration.
        """
        return self._do_not_check_total_duration

    @property
    def frame(self):
        """
        Gets frame in which rhythm command was called.
        """
        return self._frame

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
            ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 16)),
            ...     time_signatures=5 * [(4, 8)],
            ...     )

            >>> note_command = rmakers.stack(
            ...     rmakers.note(),
            ...     rmakers.force_rest(
            ...         baca.selectors.lts(),
            ...     ),
            ...     rmakers.beam(baca.selectors.plts()),
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

            >>> def label_with_durations(music):
            ...     return abjad.Label(music).with_durations(
            ...         direction=abjad.Down,
            ...         denominator=16,
            ...     )
            >>> maker(
            ...     'Music_Voice',
            ...     baca.label(label_with_durations),
            ...     baca.text_script_font_size(-2),
            ...     baca.text_script_staff_padding(5),
            ...     command,
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
                            s1 * 1/2
                <BLANKLINE>
                            % [Global_Skips measure 3]
                            \baca-new-spacing-section #1 #16
                            s1 * 1/2
                <BLANKLINE>
                            % [Global_Skips measure 4]
                            \baca-new-spacing-section #1 #16
                            s1 * 1/2
                <BLANKLINE>
                            % [Global_Skips measure 5]
                            \baca-new-spacing-section #1 #16
                            s1 * 1/2
                <BLANKLINE>
                            % [Global_Skips measure 6]
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
                                \override TextScript.font-size = -2
                                \override TextScript.staff-padding = 5
                                \baca-not-yet-pitched-coloring
                                b'8.
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                <BLANKLINE>
                                \baca-not-yet-pitched-coloring
                                b'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca-not-yet-pitched-coloring
                                b'16
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                                ~
                <BLANKLINE>
                                % [Music_Voice measure 2]
                                \baca-not-yet-pitched-coloring
                                b'8
                <BLANKLINE>
                                \baca-not-yet-pitched-coloring
                                b'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca-not-yet-pitched-coloring
                                b'8
                                _ \markup {
                                    \fraction
                                        2
                                        16
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 3]
                                r2
                                _ \markup {
                                    \fraction
                                        8
                                        16
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 4]
                                \baca-not-yet-pitched-coloring
                                b'16
                                _ \markup {
                                    \fraction
                                        1
                                        16
                                    }
                <BLANKLINE>
                                \baca-not-yet-pitched-coloring
                                b'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca-not-yet-pitched-coloring
                                b'8.
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 5]
                                \baca-not-yet-pitched-coloring
                                b'4
                                _ \markup {
                                    \fraction
                                        4
                                        16
                                    }
                <BLANKLINE>
                                \baca-not-yet-pitched-coloring
                                b'8.
                                _ \markup {
                                    \fraction
                                        3
                                        16
                                    }
                                [
                <BLANKLINE>
                                \baca-not-yet-pitched-coloring
                                b'16
                                _ \markup {
                                    \fraction
                                        1
                                        16
                                    }
                                ]
                                \revert TextScript.font-size
                                \revert TextScript.staff-padding
                <BLANKLINE>
                                <<
                <BLANKLINE>
                                    \context Voice = "Music_Voice"
                                    {
                <BLANKLINE>
                                        % [Music_Voice measure 6]
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
                                        % [Rest_Voice measure 6]
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
        return self._rhythm_maker

    @property
    def state(self) -> typing.Optional[abjad.OrderedDict]:
        """
        Gets postcall state of rhythm command.

        Populated by segment-maker.
        """
        return self._state


class TimeSignatureMaker:
    """
    Time-signature-maker.

    ..  container:: example

        >>> time_signatures = [
        ...     [(1, 16), (2, 16), (3, 16)],
        ...     [(1, 8), (2, 8), (3, 8)],
        ...     ]
        >>> maker = baca.TimeSignatureMaker(
        ...     time_signatures=time_signatures,
        ...     count=5,
        ...     fermata_measures=[5],
        ...     )
        >>> maker.run()
        [(1, 16), (2, 16), (3, 16), (1, 8), TimeSignature((1, 4))]

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_count",
        "_fermata_measures",
        "_rotation",
        "_time_signatures",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        time_signatures,
        *,
        count: int = None,
        fermata_measures: abjad.IntegerSequence = None,
        rotation: int = None,
    ) -> None:
        self._time_signatures = time_signatures
        if count is not None:
            assert isinstance(count, int), repr(count)
        self._count = count
        if fermata_measures is not None:
            assert all(isinstance(_, int) for _ in fermata_measures)
            fermata_measures = list(fermata_measures)
        self._fermata_measures = fermata_measures
        self._rotation = rotation

    ### PRIVATE METHODS ###

    def _normalize_fermata_measures(self):
        fermata_measures = []
        if self.fermata_measures is None:
            return fermata_measures
        for n in self.fermata_measures:
            if 0 < n:
                fermata_measures.append(n)
            elif n == 0:
                raise ValueError(n)
            else:
                fermata_measures.append(self.count - abs(n) + 1)
        fermata_measures.sort()
        return fermata_measures

    ### PUBLIC PROPERTIES ###

    @property
    def count(self) -> typing.Optional[int]:
        """
        Gets count.
        """
        return self._count

    @property
    def fermata_measures(self) -> typing.Optional[typing.List[int]]:
        """
        Gets fermata measures.
        """
        return self._fermata_measures

    @property
    def rotation(self) -> typing.Optional[int]:
        """
        Gets rotation.
        """
        return self._rotation

    @property
    def time_signatures(self) -> typing.List[abjad.TimeSignature]:
        """
        Gets time signatures.
        """
        return self._time_signatures

    ### PUBLIC METHODS ###

    def run(self) -> typing.List[abjad.TimeSignature]:
        """
        Makes time signatures (without stages).

        Accounts for fermata measures.

        Does not account for stages.
        """
        if not self.count:
            raise Exception("must specify count with run().")
        result = []
        time_signatures = abjad.Sequence(self.time_signatures)
        time_signatures = time_signatures.rotate(self.rotation)
        time_signatures = time_signatures.flatten(depth=1)
        time_signatures_ = abjad.CyclicTuple(time_signatures)
        i = 0
        fermata_measures = self._normalize_fermata_measures()
        for j in range(self.count):
            measure_number = j + 1
            if measure_number in fermata_measures:
                result.append(abjad.TimeSignature((1, 4)))
            else:
                time_signature = time_signatures_[i]
                result.append(time_signature)
                i += 1
        return result


### FACTORY FUNCTIONS ###


def make_even_divisions(*, measures: typings.SliceTyping = None) -> RhythmCommand:
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
        annotation_spanner_color="#darkcyan",
        frame=inspect.currentframe(),
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
            preprocessor=lambda _: _sequence.Sequence([_sequence.Sequence(_).sum()]),
            tag=_site(inspect.currentframe()),
        ),
        annotation_spanner_color="#darkcyan",
        frame=inspect.currentframe(),
        measures=measures,
    )


def make_monads(
    fractions: str,
) -> RhythmCommand:
    r"""
    Makes monads.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ...     time_signatures=[(4, 4)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_monads('2/5 2/5 1/5'),
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
                        \time 4/4
                        \baca-time-signature-color #'blue
                        s1 * 1
            <BLANKLINE>
                        % [Global_Skips measure 2]
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
                            \tweak edge-height #'(0.7 . 0)
                            \times 4/5 {
            <BLANKLINE>
                                % [Music_Voice measure 1]
                                \baca-not-yet-pitched-coloring
                                b'2
                                - \abjad-dashed-line-with-hook
                                - \baca-text-spanner-left-text "make_monads('2/5 2/5 1/5')"
                                - \tweak bound-details.right.padding 2.75
                                - \tweak color #darkcyan
                                - \tweak staff-padding 8
                                \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            }
            <BLANKLINE>
                            \tweak edge-height #'(0.7 . 0)
                            \times 4/5 {
            <BLANKLINE>
                                \baca-not-yet-pitched-coloring
                                b'2
            <BLANKLINE>
                            }
            <BLANKLINE>
                            \tweak edge-height #'(0.7 . 0)
                            \times 4/5 {
            <BLANKLINE>
                                \baca-not-yet-pitched-coloring
                                b'4
                                <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            }
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 2]
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
                                    % [Rest_Voice measure 2]
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
    components: typing.List[abjad.Component] = []
    maker = abjad.LeafMaker()
    pitch = 0
    for fraction in fractions.split():
        leaves = maker([pitch], [fraction])
        components.extend(leaves)
    for tuplet in abjad.select(components).tuplets():
        tuplet.multiplier = abjad.Multiplier(tuplet.multiplier)
    rhythm_maker = abjad.select(components)
    return RhythmCommand(
        rhythm_maker,
        annotation_spanner_color="#darkcyan",
        attach_not_yet_pitched=True,
        frame=inspect.currentframe(),
    )


# TODO: REMOVE?
def make_multimeasure_rests(*, measures: typings.SliceTyping = None) -> RhythmCommand:
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
            rmakers.rewrite_meter(),
            *repeat_tie_specifier,
            tag=_site(inspect.currentframe()),
        ),
        annotation_spanner_color="#darkcyan",
        frame=inspect.currentframe(),
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

        REGRESSION. All notes below are tagged NOT_YET_PITCHED_COLORING (and
        colored gold), even tied notes resulting from meter rewriting:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ...     time_signatures=[(10, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_repeat_tied_notes(),
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
                        \time 10/8
                        \baca-time-signature-color #'blue
                        s1 * 5/4
            <BLANKLINE>
                        % [Global_Skips measure 2]
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
                            \baca-not-yet-pitched-coloring
                            b'4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_repeat_tied_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            - \tweak stencil ##f
                            ~
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring
                            b'4
                            \repeatTie
                            - \tweak stencil ##f
                            ~
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring
                            b'4.
                            \repeatTie
                            - \tweak stencil ##f
                            ~
            <BLANKLINE>
                            \baca-not-yet-pitched-coloring
                            b'4
                            \repeatTie
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 2]
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
                                    % [Rest_Voice measure 2]
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
    specifier: rmakers.Command
    specifiers_ = list(specifiers)
    specifier = rmakers.beam(lambda _: classes.Selection(_).plts())
    specifiers_.append(specifier)
    specifier = rmakers.repeat_tie(lambda _: classes.Selection(_).pheads()[1:])
    specifiers_.append(specifier)
    if not do_not_rewrite_meter:
        command = rmakers.rewrite_meter()
        specifiers_.append(command)
    specifier = rmakers.force_repeat_tie()
    specifiers_.append(specifier)
    return RhythmCommand(
        rmakers.stack(rmakers.note(), *specifiers_, tag=_site(inspect.currentframe())),
        annotation_spanner_color="#darkcyan",
        frame=inspect.currentframe(),
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

    def preprocessor(divisions):
        divisions = _sequence.Sequence(divisions)
        divisions = divisions.fuse()
        divisions = divisions.split_divisions(durations, cyclic=True)
        return divisions

    rewrite_specifiers: typing.List[rmakers.Command] = []
    if not do_not_rewrite_meter:
        rewrite_specifiers.append(rmakers.rewrite_meter())
    return RhythmCommand(
        rmakers.stack(
            rmakers.note(),
            *specifiers,
            *rewrite_specifiers,
            rmakers.force_repeat_tie(),
            preprocessor=preprocessor,
            tag=_site(inspect.currentframe()),
        ),
        annotation_spanner_color="#darkcyan",
        frame=inspect.currentframe(),
        measures=measures,
    )


def make_rests(*, measures: typings.SliceTyping = None) -> RhythmCommand:
    """
    Makes rests.
    """
    return RhythmCommand(
        rmakers.stack(
            rmakers.note(),
            rmakers.force_rest(lambda _: classes.Selection(_).lts()),
            tag=_site(inspect.currentframe()),
        ),
        annotation_spanner_color="#darkcyan",
        frame=inspect.currentframe(),
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
        annotation_spanner_color="#darkcyan",
        frame=inspect.currentframe(),
        measures=measures,
    )


# TODO: REMOVE?
def make_skips(*, measures: typings.SliceTyping = None) -> RhythmCommand:
    """
    Makes multiplied-duration skips.
    """
    return RhythmCommand(
        rmakers.multiplied_duration(abjad.Skip, tag=_site(inspect.currentframe())),
        measures=measures,
    )


def make_tied_notes(*, measures: typings.SliceTyping = None) -> RhythmCommand:
    """
    Makes tied notes; rewrites meter.
    """
    return RhythmCommand(
        rmakers.stack(
            rmakers.note(),
            rmakers.beam(lambda _: classes.Selection(_).plts()),
            rmakers.tie(lambda _: classes.Selection(_).ptails()[:-1]),
            rmakers.rewrite_meter(),
            tag=_site(inspect.currentframe()),
        ),
        annotation_spanner_color="#darkcyan",
        frame=inspect.currentframe(),
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
    tie_specifier = rmakers.repeat_tie(lambda _: classes.Selection(_).pheads()[1:])
    specifiers.append(tie_specifier)
    tie_specifier = rmakers.force_repeat_tie()
    specifiers.append(tie_specifier)

    def preprocessor(divisions):
        divisions = _sequence.Sequence(divisions)
        divisions = divisions.fuse()
        divisions = divisions.split_divisions(durations, cyclic=True)
        return divisions

    return RhythmCommand(
        rmakers.stack(
            rmakers.note(),
            *specifiers,
            preprocessor=preprocessor,
            tag=_site(inspect.currentframe()),
        ),
        annotation_spanner_color="#darkcyan",
        frame=inspect.currentframe(),
        measures=measures,
    )


def music(
    argument: typing.Union[str, abjad.Selection],
    *,
    do_not_check_total_duration: bool = None,
    tag: typing.Optional[abjad.Tag] = abjad.Tag("baca.music()"),
) -> RhythmCommand:
    """
    Makes rhythm command from string or selection ``argument``.
    """
    if isinstance(argument, str):
        string = f"{{ {argument} }}"
        container = abjad.parse(string)
        selection = abjad.mutate.eject_contents(container)
    elif isinstance(argument, abjad.Selection):
        selection = argument
    else:
        message = "baca.music() accepts string or selection,"
        message += f" not {repr(argument)}."
        raise TypeError(message)
    if tag is not None:
        tag_selection(selection, tag)
    return RhythmCommand(
        selection,
        annotation_spanner_color="#darkcyan",
        annotation_spanner_text="baca.music() =|",
        do_not_check_total_duration=do_not_check_total_duration,
    )


def rhythm(
    *arguments,
    frame=None,
    preprocessor: abjad.Expression = None,
    measures: typings.SliceTyping = None,
    persist: str = None,
    tag: abjad.Tag = None,
) -> RhythmCommand:
    """
    Makes rhythm command from ``argument``.
    """
    if tag is not None:
        assert isinstance(tag, abjad.Tag), repr(tag)
    argument = rmakers.stack(*arguments, preprocessor=preprocessor, tag=tag)
    return RhythmCommand(
        argument,
        attach_not_yet_pitched=True,
        frame=frame,
        measures=measures,
        persist=persist,
    )


def skeleton(
    argument: typing.Union[str, abjad.Selection],
    *,
    do_not_check_total_duration: bool = None,
    tag: typing.Optional[abjad.Tag] = abjad.Tag("baca.skeleton()"),
) -> RhythmCommand:
    """
    Makes rhythm command from ``string`` and attaches NOT_YET_PITCHED
    indicators to music.
    """
    if isinstance(argument, str):
        string = f"{{ {argument} }}"
        container = abjad.parse(string)
        selection = abjad.mutate.eject_contents(container)
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
        annotation_spanner_color="#darkcyan",
        annotation_spanner_text="baca.skeleton() =|",
        attach_not_yet_pitched=True,
        do_not_check_total_duration=do_not_check_total_duration,
    )


def tacet(
    color: str = "#green",
    *,
    measures: typings.SliceTyping = None,
    selector=lambda _: classes.Selection(_).mmrests(),
) -> overrides.OverrideCommand:
    """
    Colors multimeasure rests.
    """
    command = overrides.mmrest_color(color, selector=selector)
    scoping.tag(_tags.TACET_COLORING, command)
    scoping.tag(_site(inspect.currentframe()), command)
    command_ = scoping.new(command, measures=measures)
    assert isinstance(command_, overrides.OverrideCommand)
    return command_


def tag_selection(selection: abjad.Selection, tag: abjad.Tag) -> None:
    """
    Tags selection.
    """
    assert isinstance(tag, abjad.Tag), repr(tag)
    # TODO: tag attachments
    for component in abjad.iterate(selection).components():
        component._tag = tag
