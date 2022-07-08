"""
Command classes.
"""
import collections
import copy
import dataclasses
import pathlib
import typing
from inspect import currentframe as _frame

import abjad

from . import command as _command
from . import indicators as _indicators
from . import overrides as _overrides
from . import parts as _parts
from . import path as _path
from . import pcollections as _pcollections
from . import select as _select
from . import tags as _tags
from . import treat as _treat
from . import tweaks as _tweaks
from . import typings as _typings
from .enums import enums as _enums


def _attach_persistent_indicator(
    argument,
    indicators,
    *,
    context=None,
    do_not_test=False,
    deactivate=False,
    direction=None,
    manifests=None,
    predicate=None,
    tag=None,
):
    assert isinstance(manifests, dict), repr(manifests)
    if isinstance(indicators, collections.abc.Iterable):
        cyclic_indicators = abjad.CyclicTuple(indicators)
    else:
        cyclic_indicators = abjad.CyclicTuple([indicators])
    # TODO: eventually uncomment following two lines:
    # for indicator in cyclic_indicators:
    #     assert getattr(indicator, "persistent", False) is True, repr(indicator)
    leaves = abjad.select.leaves(argument)
    # tag = tag.append(_tags.function_name(_frame()))
    tag = tag.append(abjad.Tag("baca.IndicatorCommand._call()"))
    for i, leaf in enumerate(leaves):
        if predicate and not predicate(leaf):
            continue
        indicators = cyclic_indicators[i]
        indicators = _token_to_indicators(indicators)
        for indicator in indicators:
            reapplied = _treat.remove_reapplied_wrappers(leaf, indicator)
            wrapper = abjad.attach(
                indicator,
                leaf,
                context=context,
                deactivate=deactivate,
                direction=direction,
                do_not_test=do_not_test,
                tag=tag,
                wrapper=True,
            )
            if _treat.compare_persistent_indicators(indicator, reapplied):
                _treat.treat_persistent_wrapper(manifests, wrapper, "redundant")


def _coerce_pitches(pitches):
    if isinstance(pitches, Loop):
        return pitches
    if isinstance(pitches, str):
        pitches = _parse_string(pitches)
    items = []
    for item in pitches:
        if isinstance(item, str) and "<" in item and ">" in item:
            item = item.strip("<")
            item = item.strip(">")
            item = set(abjad.NamedPitch(_) for _ in item.split())
        elif isinstance(item, str):
            item = abjad.NamedPitch(item)
        elif isinstance(item, collections.abc.Iterable):
            item = set(abjad.NamedPitch(_) for _ in item)
        else:
            item = abjad.NamedPitch(item)
        items.append(item)
    pitches = abjad.CyclicTuple(items)
    return pitches


def _do_pitch_command(
    argument,
    cyclic,
    pitches,
    *,
    allow_hidden: bool = False,
    allow_octaves: bool = False,
    allow_out_of_range: bool = False,
    allow_repeats: bool = False,
    allow_repitch: bool = False,
    do_not_transpose: bool = False,
    mock: bool = False,
    previous_pitches_consumed: int = 0,
) -> tuple[int, bool]:
    assert isinstance(previous_pitches_consumed, int)
    pitches = _coerce_pitches(pitches)
    plts = []
    if allow_hidden:
        pleaves = _select.pleaves(argument)
    else:
        pleaves = _select.pleaves(argument, exclude=_enums.HIDDEN)
    for pleaf in pleaves:
        plt = abjad.get.logical_tie(pleaf)
        if plt.head is pleaf:
            plts.append(plt)
    if not cyclic:
        if len(pitches) < len(plts):
            message = f"only {len(pitches)} pitches"
            message += f" for {len(plts)} logical ties:\n\n"
            message += f"{pitches!r} and {plts!r}."
            raise Exception(message)
    if cyclic and not isinstance(pitches, abjad.CyclicTuple | Loop):
        pitches = abjad.CyclicTuple(pitches)
    pitches_consumed = 0
    mutated_score = False
    for i, plt in enumerate(plts):
        pitch = pitches[i + previous_pitches_consumed]
        new_plt = _set_lt_pitch(
            plt,
            pitch,
            allow_hidden=allow_hidden,
            allow_repitch=allow_repitch,
            mock=mock,
        )
        if new_plt is not None:
            mutated_score = True
            plt = new_plt
        if allow_octaves:
            for pleaf in plt:
                abjad.attach(_enums.ALLOW_OCTAVE, pleaf)
        if allow_out_of_range:
            for pleaf in plt:
                abjad.attach(_enums.ALLOW_OUT_OF_RANGE, pleaf)
        if allow_repeats:
            for pleaf in plt:
                abjad.attach(_enums.ALLOW_REPEAT_PITCH, pleaf)
        if do_not_transpose is True:
            for pleaf in plt:
                abjad.attach(_enums.DO_NOT_TRANSPOSE, pleaf)
        pitches_consumed += 1
    return pitches_consumed, mutated_score


def _is_rest(argument):
    prototype = (abjad.Rest, abjad.MultimeasureRest, abjad.Skip)
    if isinstance(argument, prototype):
        return True
    annotation = abjad.get.annotation(argument, "is_sounding")
    if annotation is False:
        return True
    return False


def _parse_string(string):
    items, current_chord = [], []
    for part in string.split():
        if "<" in part:
            assert not current_chord
            current_chord.append(part)
        elif ">" in part:
            assert current_chord
            current_chord.append(part)
            item = " ".join(current_chord)
            items.append(item)
            current_chord = []
        elif current_chord:
            current_chord.append(part)
        else:
            items.append(part)
    assert not current_chord, repr(current_chord)
    return items


def _set_lt_pitch(
    lt,
    pitch,
    *,
    allow_hidden=False,
    allow_repitch=False,
    mock=False,
    set_chord_pitches_equal=False,
):
    new_lt = None
    already_pitched = _enums.ALREADY_PITCHED
    for leaf in lt:
        if not allow_hidden and abjad.get.has_indicator(leaf, _enums.HIDDEN):
            continue
        abjad.detach(_enums.NOT_YET_PITCHED, leaf)
        if mock is True:
            abjad.attach(_enums.MOCK, leaf)
        if allow_repitch:
            continue
        if abjad.get.has_indicator(leaf, already_pitched):
            voice = abjad.get.parentage(leaf).get(abjad.Voice)
            if voice is None:
                name = "no voice"
            else:
                name = voice.name
            raise Exception(f"already pitched {repr(leaf)} in {name}.")
        abjad.attach(already_pitched, leaf)
    if pitch is None:
        if not lt.is_pitched:
            pass
        else:
            for leaf in lt:
                rest = abjad.Rest(leaf.written_duration, multiplier=leaf.multiplier)
                abjad.mutate.replace(leaf, rest, wrappers=True)
            new_lt = abjad.get.logical_tie(rest)
    elif isinstance(pitch, collections.abc.Iterable):
        if isinstance(lt.head, abjad.Chord):
            for chord in lt:
                chord.written_pitches = pitch
        else:
            assert isinstance(lt.head, abjad.Note | abjad.Rest)
            for leaf in lt:
                chord = abjad.Chord(
                    pitch,
                    leaf.written_duration,
                    multiplier=leaf.multiplier,
                )
                abjad.mutate.replace(leaf, chord, wrappers=True)
            new_lt = abjad.get.logical_tie(chord)
    else:
        if isinstance(lt.head, abjad.Note):
            for note in lt:
                note.written_pitch = pitch
        elif set_chord_pitches_equal is True and isinstance(lt.head, abjad.Chord):
            for chord in lt:
                for note_head in chord.note_heads:
                    note_head.written_pitch = pitch
        else:
            assert isinstance(lt.head, abjad.Chord | abjad.Rest)
            for leaf in lt:
                note = abjad.Note(
                    pitch,
                    leaf.written_duration,
                    multiplier=leaf.multiplier,
                )
                abjad.mutate.replace(leaf, note, wrappers=True)
            new_lt = abjad.get.logical_tie(note)
    return new_lt


def _staff_position_function(
    argument,
    numbers,
    *,
    allow_hidden=False,
    allow_out_of_range=False,
    allow_repeats=False,
    allow_repitch=False,
    exact=False,
    mock=False,
    set_chord_pitches_equal=False,
):
    numbers = abjad.CyclicTuple(numbers)
    plt_count = 0
    mutated_score = False
    for i, plt in enumerate(_select.plts(argument)):
        clef = abjad.get.effective(
            plt.head,
            abjad.Clef,
            default=abjad.Clef("treble"),
        )
        number = numbers[i]
        # TODO: remove this first branch (after migration) because never executed?
        if isinstance(number, list):
            raise Exception("ASDF")
            positions = [abjad.StaffPosition(_) for _ in number]
            pitches = [_.to_pitch(clef) for _ in positions]
            new_lt = _set_lt_pitch(
                plt,
                pitches,
                allow_hidden=allow_hidden,
                # allow_repitch=self.allow_repitch,
                # mock=self.mock,
                # set_chord_pitches_equal=self.set_chord_pitches_equal,
                allow_repitch=allow_repitch,
                mock=mock,
                set_chord_pitches_equal=set_chord_pitches_equal,
            )
            if new_lt is not None:
                mutated_score = True
                plt = new_lt
        else:
            position = abjad.StaffPosition(number)
            pitch = clef.to_pitch(position)
            new_lt = _set_lt_pitch(
                plt,
                pitch,
                allow_hidden=allow_hidden,
                # allow_repitch=self.allow_repitch,
                # mock=self.mock,
                # set_chord_pitches_equal=self.set_chord_pitches_equal,
                allow_repitch=allow_repitch,
                mock=mock,
                set_chord_pitches_equal=set_chord_pitches_equal,
            )
            if new_lt is not None:
                mutated_score = True
                plt = new_lt
        plt_count += 1
        for pleaf in plt:
            abjad.attach(_enums.STAFF_POSITION, pleaf)
            if allow_out_of_range:
                abjad.attach(_enums.ALLOW_OUT_OF_RANGE, pleaf)
            if allow_repeats:
                abjad.attach(_enums.ALLOW_REPEAT_PITCH, pleaf)
                abjad.attach(_enums.DO_NOT_TRANSPOSE, pleaf)
    if exact and plt_count != len(numbers):
        message = f"PLT count ({plt_count}) does not match"
        message += f" staff position count ({len(numbers)})."
        raise Exception(message)
    return mutated_score


def _token_to_indicators(token):
    result = []
    if not isinstance(token, tuple | list):
        token = [token]
    for item in token:
        if item is None:
            continue
        result.append(item)
    return result


def _validate_bcps(bcps):
    if bcps is None:
        return
    for bcp in bcps:
        assert isinstance(bcp, tuple), repr(bcp)
        assert len(bcp) == 2, repr(bcp)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class BCPCommand(_command.Command):
    r"""
    Bow contact point command.

    ..  container:: example

        Tweaks LilyPond ``TextSpanner`` grob:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 16)),
        ... )
        >>> music = baca.make_even_divisions(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.bcps(
        ...         [(1, 5), (2, 5)],
        ...         abjad.Tweak(r"- \tweak color #red"),
        ...         abjad.Tweak(r"- \tweak staff-padding 2.5"),
        ...     ),
        ...     baca.pitches("E4 F4"),
        ...     baca.script_staff_padding(5),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        Style LilyPond ``Script`` grob with overrides (instead of tweaks).

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #16
                        \time 4/8
                        s1 * 4/8
                        \baca-new-spacing-section #1 #16
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #16
                        \time 4/8
                        s1 * 4/8
                        \baca-new-spacing-section #1 #16
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \override Script.staff-padding = 5
                        e'8
                        - \downbow
                        [
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        ]
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        [
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        ]
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        [
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        ]
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        [
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        - \tweak color #red
                        - \tweak staff-padding 2.5
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        - \baca-bcp-spanner-right-text #2 #5
                        \bacaStartTextSpanBCP
                        f'8
                        \bacaStopTextSpanBCP
                        ]
                        \revert Script.staff-padding
                    }
                >>
            }

    ..  container:: example

        REGRESSION. Tweaks survive copy:

        >>> command = baca.bcps(
        ...     [(1, 2), (1, 4)],
        ...     abjad.Tweak(r"- \tweak color #red"),
        ... )

        >>> import copy
        >>> new_command = copy.copy(command)
        >>> new_command.tweaks
        (Tweak(string='- \\tweak color #red', tag=None),)

    ..  container:: example

        PATTERN. Define chunkwise spanners like this:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 16)),
        ... )

        >>> music = baca.make_even_divisions(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.new(
        ...         baca.bcps(bcps=[(1, 5), (2, 5)]),
        ...         measures=(1, 2),
        ...     ),
        ...     baca.new(
        ...         baca.bcps(bcps=[(3, 5), (4, 5)]),
        ...         measures=(3, 4),
        ...     ),
        ...     baca.pitches("E4 F4"),
        ...     baca.script_staff_padding(5.5),
        ...     baca.text_spanner_staff_padding(2.5),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #16
                        \time 4/8
                        s1 * 4/8
                        \baca-new-spacing-section #1 #16
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #16
                        \time 4/8
                        s1 * 4/8
                        \baca-new-spacing-section #1 #16
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \override Script.staff-padding = 5.5
                        \override TextSpanner.staff-padding = 2.5
                        e'8
                        - \downbow
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        ]
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        - \baca-bcp-spanner-right-text #1 #5
                        \bacaStartTextSpanBCP
                        e'8
                        \bacaStopTextSpanBCP
                        ]
                        f'8
                        - \downbow
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #3 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #4 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #3 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        ]
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #4 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #3 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #4 #5
                        - \baca-bcp-spanner-right-text #3 #5
                        \bacaStartTextSpanBCP
                        f'8
                        \bacaStopTextSpanBCP
                        ]
                        \revert Script.staff-padding
                        \revert TextSpanner.staff-padding
                    }
                >>
            }

    """

    bcps: typing.Sequence[tuple[int, int]] = ()
    bow_change_tweaks: tuple[_typings.IndexedTweak, ...] = ()
    final_spanner: bool = False
    helper: typing.Callable = lambda x, y: x
    tweaks: tuple[_typings.IndexedTweak, ...] = ()

    def __post_init__(self):
        _command.Command.__post_init__(self)
        _validate_bcps(self.bcps)
        _tweaks.validate_indexed_tweaks(self.bow_change_tweaks)
        assert isinstance(self.final_spanner, bool), repr(self.final_spanner)
        assert callable(self.helper), repr(self.helper)
        _tweaks.validate_indexed_tweaks(self.tweaks)

    __repr__ = _command.Command.__repr__

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if self.bcps is None:
            return False
        if self.selector:
            argument = self.selector(argument)
        bcps_ = list(self.bcps)
        bcps_ = self.helper(bcps_, argument)
        bcps = abjad.CyclicTuple(bcps_)
        lts = _select.lts(argument)
        add_right_text_to_me = None
        if not self.final_spanner:
            rest_count, nonrest_count = 0, 0
            for lt in reversed(lts):
                if _is_rest(lt.head):
                    rest_count += 1
                else:
                    if 0 < rest_count and nonrest_count == 0:
                        add_right_text_to_me = lt.head
                        break
                    if 0 < nonrest_count and rest_count == 0:
                        add_right_text_to_me = lt.head
                        break
                    nonrest_count += 1
        if self.final_spanner and not _is_rest(lts[-1]) and len(lts[-1]) == 1:
            next_leaf_after_argument = abjad.get.leaf(lts[-1][-1], 1)
            if next_leaf_after_argument is None:
                message = "can not attach final spanner:"
                message += " argument includes end of score."
                raise Exception(message)
        previous_bcp = None
        i = 0
        for lt in lts:
            stop_text_span = abjad.StopTextSpan(command=self.stop_command)
            if not self.final_spanner and lt is lts[-1] and not _is_rest(lt.head):
                abjad.attach(
                    stop_text_span,
                    lt.head,
                    tag=self.tag.append(_tags.function_name(_frame(), self, n=1)),
                )
                break
            previous_leaf = abjad.get.leaf(lt.head, -1)
            next_leaf = abjad.get.leaf(lt.head, 1)
            if _is_rest(lt.head) and (_is_rest(previous_leaf) or previous_leaf is None):
                continue
            if (
                isinstance(lt.head, abjad.Note)
                and _is_rest(previous_leaf)
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
            elif not _is_rest(lt.head):
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
                start_text_span = _tweaks.bundle_tweaks(start_text_span, self.tweaks)
            if _is_rest(lt.head) and (_is_rest(next_leaf) or next_leaf is None):
                pass
            else:
                abjad.attach(
                    start_text_span,
                    lt.head,
                    tag=self.tag.append(_tags.function_name(_frame(), self, n=2)),
                )
            if 0 < i - 1:
                abjad.attach(
                    stop_text_span,
                    lt.head,
                    tag=self.tag.append(_tags.function_name(_frame(), self, n=3)),
                )
            if lt is lts[-1] and self.final_spanner:
                abjad.attach(
                    stop_text_span,
                    next_leaf_after_argument,
                    tag=self.tag.append(_tags.function_name(_frame(), self, n=4)),
                )
            bcp_fraction = abjad.Fraction(*bcp)
            next_bcp_fraction = abjad.Fraction(*bcps[i])
            if _is_rest(lt.head):
                pass
            elif _is_rest(previous_leaf) or previous_bcp is None:
                if bcp_fraction > next_bcp_fraction:
                    articulation = abjad.Articulation("upbow")
                    if self.bow_change_tweaks:
                        articulation = _tweaks.bundle_tweaks(
                            articulation, self.bow_change_tweaks
                        )
                    abjad.attach(
                        articulation,
                        lt.head,
                        tag=self.tag.append(_tags.function_name(_frame(), self, n=5)),
                    )
                elif bcp_fraction < next_bcp_fraction:
                    articulation = abjad.Articulation("downbow")
                    if self.bow_change_tweaks:
                        articulation = _tweaks.bundle_tweaks(
                            articulation, self.bow_change_tweaks
                        )
                    abjad.attach(
                        articulation,
                        lt.head,
                        tag=self.tag.append(_tags.function_name(_frame(), self, n=6)),
                    )
            else:
                previous_bcp_fraction = abjad.Fraction(*previous_bcp)
                if previous_bcp_fraction < bcp_fraction > next_bcp_fraction:
                    articulation = abjad.Articulation("upbow")
                    if self.bow_change_tweaks:
                        articulation = _tweaks.bundle_tweaks(
                            articulation, self.bow_change_tweaks
                        )
                    abjad.attach(
                        articulation,
                        lt.head,
                        tag=self.tag.append(_tags.function_name(_frame(), self, n=7)),
                    )
                elif previous_bcp_fraction > bcp_fraction < next_bcp_fraction:
                    articulation = abjad.Articulation("downbow")
                    if self.bow_change_tweaks:
                        articulation = _tweaks.bundle_tweaks(
                            articulation, self.bow_change_tweaks
                        )
                    abjad.attach(
                        articulation,
                        lt.head,
                        tag=self.tag.append(_tags.function_name(_frame(), self, n=8)),
                    )
            previous_bcp = bcp
        return False

    @property
    def start_command(self) -> str:
        r"""
        Gets ``"\bacaStartTextSpanBCP"``.
        """
        return r"\bacaStartTextSpanBCP"

    @property
    def stop_command(self) -> str:
        r"""
        Gets ``"\bacaStopTextSpanBCP"``.
        """
        return r"\bacaStopTextSpanBCP"


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class ColorCommand(_command.Command):

    lone: bool = False

    def __post_init__(self):
        assert self.selector is not None
        _command.Command.__post_init__(self)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        assert self.selector is not None
        argument = self.selector(argument)
        abjad.label.by_selector(argument, self.selector, lone=self.lone)
        return False


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class ContainerCommand(_command.Command):
    r"""
    Container command.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_notes(commands.get(), repeat_ties=True)
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.container(
        ...         "ViolinI",
        ...         selector=lambda _: baca.select.leaves(_)[:2],
        ...     ),
        ...     baca.container(
        ...         "ViolinII",
        ...         selector=lambda _: baca.select.leaves(_)[2:],
        ...         ),
        ...     baca.pitches("E4 F4"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            <<
                \context Voice = "Skips"
                {
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    {   %*% ViolinI
                        e'2
                        f'4.
                    }   %*% ViolinI
                    {   %*% ViolinII
                        e'2
                        f'4.
                    }   %*% ViolinII
                }
            >>
        }

    """

    identifier: str | None = None

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert isinstance(self.identifier, str), repr(self.identifier)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if self.selector is not None:
            argument = self.selector(argument)
        if not self.identifier:
            identifier = None
        elif self.identifier.startswith("%*%"):
            identifier = self.identifier
        else:
            identifier = f"%*% {self.identifier}"
        container = abjad.Container(identifier=identifier)
        leaves = abjad.select.leaves(argument)
        components = abjad.select.top(leaves)
        abjad.mutate.wrap(components, container)
        return True


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class DetachCommand(_command.Command):

    arguments: typing.Sequence[typing.Any] = ()

    def __post_init__(self):
        _command.Command.__post_init__(self)

    __repr__ = _command.Command.__repr__

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        assert self.selector is not None
        argument = self.selector(argument)
        leaves = abjad.select.leaves(argument)
        assert isinstance(leaves, list)
        for leaf in leaves:
            for argument in self.arguments:
                abjad.detach(argument, leaf)
        return False


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class GenericCommand(_command.Command):

    function: typing.Callable = lambda _: _
    name: str = ""

    def __post_init__(self):
        assert callable(self.function), repr(self.function)
        _command.Command.__post_init__(self)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if self.selector is not None:
            argument = self.selector(argument)
        self.function(argument, runtime=runtime)
        return False


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class GlissandoCommand(_command.Command):

    allow_repeats: bool = False
    allow_ties: bool = False
    hide_middle_note_heads: bool = False
    hide_middle_stems: bool = False
    hide_stem_selector: typing.Callable | None = None
    left_broken: bool = False
    parenthesize_repeats: bool = False
    right_broken: bool = False
    right_broken_show_next: bool = False
    selector: typing.Callable = lambda _: _select.tleaves(_)
    tweaks: typing.Sequence[abjad.Tweak] = ()
    zero_padding: bool = False

    def __post_init__(self):
        _command.Command.__post_init__(self)
        _tweaks.validate_indexed_tweaks(self.tweaks)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if self.selector is not None:
            argument = self.selector(argument)
        leaves = abjad.select.leaves(argument)
        tweaks_ = []
        prototype = (abjad.Tweak, tuple)
        for tweak in self.tweaks or []:
            assert isinstance(tweak, prototype), repr(tweak)
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
        return False


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class IndicatorCommand(_command.Command):

    indicators: typing.Sequence = ()
    context: str | None = None
    direction: abjad.Vertical | None = None
    do_not_test: bool = False
    predicate: typing.Callable | None = None
    redundant: bool = False

    def __post_init__(self):
        _command.Command.__post_init__(self)
        if self.context is not None:
            assert isinstance(self.context, str), repr(self.context)
        assert isinstance(self.do_not_test, bool), repr(self.do_not_test)
        assert isinstance(self.redundant, bool), repr(self.redundant)

    def __copy__(self, *arguments):
        result = dataclasses.replace(self)
        result.indicators = copy.deepcopy(self._indicators_coerced())
        return result

    __repr__ = _command.Command.__repr__

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if self._indicators_coerced() is None:
            return False
        if self.redundant is True:
            return False
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return False
        _attach_persistent_indicator(
            argument,
            self._indicators_coerced(),
            context=self.context,
            do_not_test=self.do_not_test,
            deactivate=self.deactivate,
            direction=self.direction,
            manifests=runtime.get("manifests", {}),
            predicate=self.predicate,
            tag=self.tag,
        )
        return False

    def _indicators_coerced(self):
        indicators_ = None
        if self.indicators is not None:
            if isinstance(self.indicators, collections.abc.Iterable):
                indicators_ = abjad.CyclicTuple(self.indicators)
            else:
                indicators_ = abjad.CyclicTuple([self.indicators])
        return indicators_


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class InstrumentChangeCommand(IndicatorCommand):
    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if self.selector is not None:
            argument = self.selector(argument)
        if self._indicators_coerced() is None:
            return False
        return IndicatorCommand._call(self, argument=argument, runtime=runtime)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class LabelCommand(_command.Command):

    callable_: typing.Any = None

    def __post_init__(self):
        _command.Command.__post_init__(self)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if self.callable_ is None:
            return False
        if self.selector:
            argument = self.selector(argument)
        self.callable_(argument)
        return False


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class PartAssignmentCommand(_command.Command):

    part_assignment: _parts.PartAssignment | None = None

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert isinstance(self.part_assignment, _parts.PartAssignment)

    __repr__ = _command.Command.__repr__

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if self.selector is not None:
            argument = self.selector(argument)
        first_leaf = abjad.get.leaf(argument, 0)
        if first_leaf is None:
            return False
        voice = abjad.get.parentage(first_leaf).get(abjad.Voice, -1)
        if voice is not None and self.part_assignment is not None:
            assert isinstance(voice, abjad.Voice)
            section = self.part_assignment.name or "ZZZ"
            assert voice.name is not None
            if not voice.name.startswith(section):
                message = f"{voice.name} does not allow"
                message += f" {self.part_assignment.name} part assignment:"
                message += f"\n  {self.part_assignment}"
                raise Exception(message)
        assert self.part_assignment is not None
        name, token = self.part_assignment.name, self.part_assignment.token
        if token is None:
            identifier = f"%*% PartAssignment({name!r})"
        else:
            identifier = f"%*% PartAssignment({name!r}, {token!r})"
        container = abjad.Container(identifier=identifier)
        leaves = abjad.select.leaves(argument)
        components = abjad.select.top(leaves)
        abjad.mutate.wrap(components, container)
        return False


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class AccidentalAdjustmentCommand(_command.Command):
    r"""
    Accidental adjustment command.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )


        >>> music = baca.make_notes(commands.get(), repeat_ties=True)
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.pitches("E4 F4"),
        ...     baca.force_accidental(
        ...         selector=lambda _: baca.select.pleaves(_)[:2],
        ...     ),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        e'!2
                        f'!4.
                        e'2
                        f'4.
                    }
                >>
            }

    """

    cautionary: bool = False
    forced: bool = False
    parenthesized: bool = False

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert isinstance(self.cautionary, bool), repr(self.cautionary)
        assert isinstance(self.forced, bool), repr(self.forced)
        assert isinstance(self.parenthesized, bool), repr(self.parenthesized)

    __repr__ = _command.Command.__repr__

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if self.selector is not None:
            argument = self.selector(argument)
        if self.tag.string:
            if not self.tag.only_edition() and not self.tag.not_editions():
                raise Exception(f"tag must have edition: {self.tag!r}.")
            tag = _tags.function_name(_frame(), self)
            alternative_tag = self.tag.append(tag)
            primary_tag = alternative_tag.invert_edition_tags()
        pleaves = _select.pleaves(argument)
        assert isinstance(pleaves, list)
        for pleaf in pleaves:
            if isinstance(pleaf, abjad.Note):
                note_heads = [pleaf.note_head]
            else:
                assert isinstance(pleaf, abjad.Chord)
                note_heads = list(pleaf.note_heads)
            for note_head in note_heads:
                assert note_head is not None
                if not self.tag.string:
                    if self.cautionary:
                        note_head.is_cautionary = True
                    if self.forced:
                        note_head.is_forced = True
                    if self.parenthesized:
                        note_head.is_parenthesized = True
                else:
                    alternative = copy.copy(note_head)
                    if self.cautionary:
                        alternative.is_cautionary = True
                    if self.forced:
                        alternative.is_forced = True
                    if self.parenthesized:
                        alternative.is_parenthesized = True
                    note_head.alternative = (
                        alternative,
                        alternative_tag,
                        primary_tag,
                    )
        return False


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class ClusterCommand(_command.Command):
    r"""
    Cluster command.

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.replace_with_clusters([3, 4]),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selection = stack(collections)

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
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        \time 9/16
                        <c' e' g'>16
                        ^ \markup \center-align \concat { \natural \flat }
                        [
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <d' f' a' c''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <bf' d'' f''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <fs'' a'' c''' e'''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        [
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e'' g'' b''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <ef'' g'' b'' d'''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <af'' c''' e'''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <g'' b'' d''' f'''>16
                        ^ \markup \center-align \concat { \natural \flat }
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <a' c'' e''>16
                        ^ \markup \center-align \concat { \natural \flat }
                    }
                }
            >>

    ..  container:: example

        Hides flat markup:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )


        >>> music = baca.make_notes(commands.get(), repeat_ties=True)
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.pitch("E4"),
        ...     baca.natural_clusters(widths=[3]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>2
                        ^ \markup \center-align \natural
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>4.
                        ^ \markup \center-align \natural
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>2
                        ^ \markup \center-align \natural
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>4.
                        ^ \markup \center-align \natural
                    }
                >>
            }

    ..  container:: example

        Takes start pitch from input notes:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )


        >>> music = baca.make_notes(commands.get(), repeat_ties=True)
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.pitches("C4 D4 E4 F4"),
        ...     baca.replace_with_clusters([3]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <c' e' g'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <d' f' a'>4.
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <f' a' c''>4.
                        ^ \markup \center-align \concat { \natural \flat }
                    }
                >>
            }

    ..  container:: example

        Sets start pitch explicitly:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_notes(commands.get(), repeat_ties=True)
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.replace_with_clusters([3], start_pitch="G4"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <g' b' d''>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <g' b' d''>4.
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <g' b' d''>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <g' b' d''>4.
                        ^ \markup \center-align \concat { \natural \flat }
                    }
                >>
            }

    ..  container:: example

        Increasing widths:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_notes(commands.get(), repeat_ties=True)
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.replace_with_clusters([1, 2, 3, 4], start_pitch="E4"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g'>4.
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b' d''>4.
                        ^ \markup \center-align \concat { \natural \flat }
                    }
                >>
            }

    ..  container:: example

        Patterned widths:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_notes(commands.get(), repeat_ties=True)
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.replace_with_clusters([1, 3], start_pitch="E4"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>4.
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e'>2
                        ^ \markup \center-align \concat { \natural \flat }
                        \once \override Accidental.stencil = ##f
                        \once \override AccidentalCautionary.stencil = ##f
                        \once \override Arpeggio.X-offset = #-2
                        \once \override NoteHead.stencil = #ly:text-interface::print
                        \once \override NoteHead.text =
                        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                        <e' g' b'>4.
                        ^ \markup \center-align \concat { \natural \flat }
                    }
                >>
            }

    ..  container:: example

        Leaves notes and chords unchanged:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_notes(commands.get(), repeat_ties=True)
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.pitch("E4"),
        ...     baca.replace_with_clusters([]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        e'2
                        e'4.
                        e'2
                        e'4.
                    }
                >>
            }

        Inteprets positive integers as widths in thirds.

        Interprets zero to mean input note or chord is left unchanged.

    """

    direction: abjad.Vertical | None = abjad.UP
    hide_flat_markup: bool = False
    selector: typing.Callable = lambda _: _select.plts(_)
    start_pitch: abjad.NamedPitch | None = None
    widths: typing.Sequence[int] | None = None

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert isinstance(self.hide_flat_markup, bool), repr(self.hide_flat_markup)
        if self.start_pitch is not None:
            assert isinstance(self.start_pitch, abjad.NamedPitch), repr(
                self.start_pitch
            )
        assert abjad.math.all_are_nonnegative_integers(self.widths)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if not self.widths:
            return False
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return False
        leaf = abjad.select.leaf(argument, 0)
        root = abjad.get.parentage(leaf).root
        widths = abjad.CyclicTuple(self.widths)
        with abjad.ForbidUpdate(component=root):
            for i, plt in enumerate(_select.plts(argument)):
                width = widths[i]
                self._make_cluster(plt, width)
        return True

    def _make_cluster(self, plt, width):
        assert plt.is_pitched, repr(plt)
        if not width:
            return False
        if self.start_pitch is not None:
            start_pitch = self.start_pitch
        else:
            start_pitch = plt.head.written_pitch
        pitches = self._make_pitches(start_pitch, width)
        key_cluster = abjad.KeyCluster(include_flat_markup=not self.hide_flat_markup)
        for pleaf in plt:
            chord = abjad.Chord(pitches, pleaf.written_duration)
            wrappers = abjad.get.wrappers(pleaf)
            abjad.detach(object, pleaf)
            for wrapper in wrappers:
                abjad.attach(wrapper, chord, direction=wrapper.direction)
            abjad.mutate.replace(pleaf, chord)
            abjad.attach(key_cluster, chord, direction=self.direction)
            abjad.attach(_enums.ALLOW_REPEAT_PITCH, chord)
            abjad.detach(_enums.NOT_YET_PITCHED, chord)

    def _make_pitches(self, start_pitch, width):
        pitches = [start_pitch]
        for i in range(width - 1):
            pitch = pitches[-1] + abjad.NamedInterval("M3")
            pitch = abjad.NamedPitch(pitch, accidental="natural")
            assert pitch.accidental == abjad.Accidental("natural")
            pitches.append(pitch)
        return pitches


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class ColorFingeringCommand(_command.Command):
    r"""
    Color fingering command.

    ..  container:: example

        With section-commands:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_notes(commands.get(), repeat_ties=True)
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.pitch("E4"),
        ...     baca.ColorFingeringCommand(numbers=[0, 1, 2, 1]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        e'2
                        e'4.
                        ^ \markup { \override #'(circle-padding . 0.25) \circle \finger 1 }
                        e'2
                        ^ \markup { \override #'(circle-padding . 0.25) \circle \finger 2 }
                        e'4.
                        ^ \markup { \override #'(circle-padding . 0.25) \circle \finger 1 }
                    }
                >>
            }

    """

    direction: abjad.Vertical | None = abjad.UP
    numbers: typing.Sequence[int] = ()
    tweaks: tuple[_typings.IndexedTweak, ...] = ()

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert abjad.math.all_are_nonnegative_integers(self.numbers)
        _tweaks.validate_indexed_tweaks(self.tweaks)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if not self.numbers:
            return False
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return False
        pheads = _select.pheads(argument)
        total = len(pheads)
        numbers = abjad.CyclicTuple(self.numbers)
        for i, phead in enumerate(pheads):
            number = numbers[i]
            if number != 0:
                fingering = abjad.ColorFingering(number)
                fingering = _tweaks.bundle_tweaks(
                    fingering, self.tweaks, i=i, total=total
                )
                abjad.attach(fingering, phead, direction=self.direction)
        return False


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class DiatonicClusterCommand(_command.Command):
    r"""
    Diatonic cluster command.

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' f'")
        >>> command = baca.diatonic_clusters([4, 6])
        >>> command(staff)
        True

        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                <c' d' e' f'>4
                <d' e' f' g' a' b'>4
                <e' f' g' a'>4
                <f' g' a' b' c'' d''>4
            }

    """

    widths: typing.Sequence[int] = ()
    selector: typing.Callable = lambda _: _select.plts(_)

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert abjad.math.all_are_nonnegative_integers(self.widths)
        assert all(isinstance(_, int) for _ in self.widths), repr(self.widths)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if not self.widths:
            return False
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return False
        widths = abjad.CyclicTuple(self.widths)
        for i, plt in enumerate(_select.plts(argument)):
            width = widths[i]
            start = self._get_lowest_diatonic_pitch_number(plt)
            numbers = range(start, start + width)
            change = abjad.pitch._diatonic_pc_number_to_pitch_class_number
            numbers_ = [(12 * (_ // 7)) + change[_ % 7] for _ in numbers]
            pitches = [abjad.NamedPitch(_) for _ in numbers_]
            for pleaf in plt:
                chord = abjad.Chord(pleaf)
                chord.note_heads[:] = pitches
                abjad.mutate.replace(pleaf, chord)
        return True

    def _get_lowest_diatonic_pitch_number(self, plt):
        if isinstance(plt.head, abjad.Note):
            pitch = plt.head.written_pitch
        elif isinstance(plt.head, abjad.Chord):
            pitch = plt.head.written_pitches[0]
        else:
            raise TypeError(plt)
        return pitch._get_diatonic_pitch_number()


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Loop:
    """
    Loop.

    ..  container:: example

        >>> loop = baca.Loop([0, 2, 4], [1])
        >>> loop
        Loop(pitches=[0, 2, 4], intervals=[1])

        >>> for i in range(12):
        ...     loop[i]
        NamedPitch("c'")
        NamedPitch("d'")
        NamedPitch("e'")
        NamedPitch("cs'")
        NamedPitch("ef'")
        NamedPitch("f'")
        NamedPitch("d'")
        NamedPitch("e'")
        NamedPitch("fs'")
        NamedPitch("ef'")
        NamedPitch("f'")
        NamedPitch("g'")

    """

    pitches: typing.Sequence[int]
    intervals: typing.Sequence[int]

    def __post_init__(self):
        assert all(isinstance(_, int) for _ in self.pitches), self.pitches
        assert all(isinstance(_, int) for _ in self.intervals), self.intervals

    def __getitem__(self, i: int) -> abjad.NamedPitch:
        assert isinstance(i, int), repr(i)
        intervals = abjad.CyclicTuple(self.intervals)
        pitches = abjad.CyclicTuple(self.pitches)
        iteration = i // len(pitches)
        if not pitches:
            transposition = 0
        else:
            transposition = sum(intervals[:iteration])
        number = pitches[i]
        pitch = abjad.NamedPitch(number + transposition)
        return pitch

    def __iter__(self):
        return self.pitches.__iter__()


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class MicrotoneDeviationCommand(_command.Command):
    r"""
    Microtone deviation command.

    ..  container:: example

        With alternating up- and down-quatertones:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.pitches("E4"),
        ...     baca.deviation([0, 0.5, 0, -0.5]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        e'8
                        [
                        eqs'8
                        e'8
                        eqf'8
                        ]
                        e'8
                        [
                        eqs'8
                        e'8
                        ]
                        eqf'8
                        [
                        e'8
                        eqs'8
                        e'8
                        ]
                        eqf'8
                        [
                        e'8
                        eqs'8
                        ]
                    }
                >>
            }

    """

    deviations: typing.Sequence[int | float] = ()

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert all(isinstance(_, int | float) for _ in self.deviations)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if not self.deviations:
            return False
        if self.selector:
            argument = self.selector(argument)
        deviations = abjad.CyclicTuple(self.deviations)
        for i, plt in enumerate(_select.plts(argument)):
            deviation = deviations[i]
            self._adjust_pitch(plt, deviation)
        return False

    def _adjust_pitch(self, plt, deviation):
        assert deviation in (0.5, 0, -0.5)
        if deviation == 0:
            return
        for pleaf in plt:
            pitch = pleaf.written_pitch
            accidental = pitch.accidental.semitones + deviation
            pitch = abjad.NamedPitch(pitch, accidental=accidental)
            pleaf.written_pitch = pitch
            annotation = {"color microtone": True}
            abjad.attach(annotation, pleaf)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class OctaveDisplacementCommand(_command.Command):
    r"""
    Octave displacement command.

    ..  container:: example

        Displaces octaves:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.suite(
        ...         baca.pitch("G4"),
        ...         baca.displacement([0, 0, 1, 1, 0, 0, -1, -1, 2, 2]),
        ...     ),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        g'8
                        [
                        g'8
                        g''8
                        g''8
                        ]
                        g'8
                        [
                        g'8
                        g8
                        ]
                        g8
                        [
                        g'''8
                        g'''8
                        g'8
                        ]
                        g'8
                        [
                        g''8
                        g''8
                        ]
                    }
                >>
            }

    """

    displacements: typing.Sequence[int] = ()

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert self._is_octave_displacement_vector(self.displacements)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if self.displacements is None:
            return False
        if self.selector:
            argument = self.selector(argument)
        displacements = abjad.CyclicTuple(self.displacements)
        for i, plt in enumerate(_select.plts(argument)):
            displacement = displacements[i]
            interval = abjad.NumberedInterval(12 * displacement)
            for pleaf in plt:
                if isinstance(pleaf, abjad.Note):
                    pitch = pleaf.written_pitch
                    assert isinstance(pitch, abjad.NamedPitch)
                    pitch += interval
                    pleaf.written_pitch = pitch
                elif isinstance(pleaf, abjad.Chord):
                    pitches = [_ + interval for _ in pleaf.written_pitches]
                    pleaf.written_pitches = tuple(pitches)
                else:
                    raise TypeError(pleaf)
        return False

    def _is_octave_displacement_vector(self, argument):
        if isinstance(argument, tuple | list):
            if all(isinstance(_, int) for _ in argument):
                return True
        return False


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class PitchCommand(_command.Command):
    r"""
    Pitch command.

    ..  container:: example

        With pitch numbers:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.pitches([19, 13, 15, 16, 17, 23]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        g''8
                        [
                        cs''8
                        ef''8
                        e''8
                        ]
                        f''8
                        [
                        b''8
                        g''8
                        ]
                        cs''8
                        [
                        ef''8
                        e''8
                        f''8
                        ]
                        b''8
                        [
                        g''8
                        cs''8
                        ]
                    }
                >>
            }

    ..  container:: example

        With pitch numbers:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.pitches("C4 F4 F#4 <B4 C#5> D5"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        c'8
                        [
                        f'8
                        fs'8
                        <b' cs''>8
                        ]
                        d''8
                        [
                        c'8
                        f'8
                        ]
                        fs'8
                        [
                        <b' cs''>8
                        d''8
                        c'8
                        ]
                        f'8
                        [
                        fs'8
                        <b' cs''>8
                        ]
                    }
                >>
            }

    ..  container:: example

        Large chord:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.pitches("<C4 D4 E4 F4 G4 A4 B4 C4>", allow_repeats=True)
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        <c' d' e' f' g' a' b'>8
                        [
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        ]
                        <c' d' e' f' g' a' b'>8
                        [
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        ]
                        <c' d' e' f' g' a' b'>8
                        [
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        ]
                        <c' d' e' f' g' a' b'>8
                        [
                        <c' d' e' f' g' a' b'>8
                        <c' d' e' f' g' a' b'>8
                        ]
                    }
                >>
            }

    ..  container:: example

        Works with Abjad container:

        >>> command = baca.PitchCommand(
        ...     cyclic=True,
        ...     pitches=[19, 13, 15, 16, 17, 23],
        ... )

        >>> staff = abjad.Staff("c'8 c' c' c' c' c' c' c'")
        >>> command(staff)
        False

        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                g''8
                cs''8
                ef''8
                e''8
                f''8
                b''8
                g''8
                cs''8
            }


    """

    allow_hidden: bool = False
    allow_octaves: bool = False
    allow_out_of_range: bool = False
    allow_repeats: bool = False
    allow_repitch: bool = False
    mock: bool = False
    cyclic: bool = False
    do_not_transpose: bool = False
    ignore_incomplete: bool = False
    persist: str = ""
    pitches: typing.Sequence | Loop = ()

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert isinstance(self.allow_hidden, bool), repr(self.allow_hidden)
        assert isinstance(self.allow_octaves, bool), repr(self.allow_octaves)
        assert isinstance(self.allow_out_of_range, bool), repr(self.allow_out_of_range)
        assert isinstance(self.allow_repeats, bool), repr(self.allow_repeats)
        assert isinstance(self.allow_repitch, bool), repr(self.allow_repitch)
        assert isinstance(self.mock, bool), repr(self.mock)
        assert isinstance(self.cyclic, bool), repr(self.cyclic)
        assert isinstance(self.do_not_transpose, bool), repr(self.do_not_transpose)
        assert isinstance(self.ignore_incomplete, bool), repr(self.ignore_incomplete)
        assert isinstance(self.persist, str), repr(self.persist)

    __repr__ = _command.Command.__repr__

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if not self.pitches:
            return False
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return False
        previous_pitches_consumed = self._previous_pitches_consumed(runtime)
        pitches = _coerce_pitches(self.pitches)
        pitches_consumed, mutated_score = _do_pitch_command(
            argument,
            self.cyclic,
            pitches,
            allow_hidden=self.allow_hidden,
            allow_octaves=self.allow_octaves,
            allow_out_of_range=self.allow_out_of_range,
            allow_repeats=self.allow_repeats,
            allow_repitch=self.allow_repitch,
            do_not_transpose=self.do_not_transpose,
            mock=self.mock,
            previous_pitches_consumed=previous_pitches_consumed,
        )
        pitches_consumed += previous_pitches_consumed
        self.state["pitches_consumed"] = pitches_consumed
        return mutated_score

    def _previous_pitches_consumed(self, runtime):
        assert isinstance(runtime, dict), repr(runtime)
        dictionary = runtime.get("previous_section_voice_metadata", None)
        if not dictionary:
            return 0
        dictionary = dictionary.get(_enums.PITCH.name, None)
        if not dictionary:
            return 0
        if dictionary.get("name") != self.persist:
            return 0
        pitches_consumed = dictionary.get("pitches_consumed", None)
        if not pitches_consumed:
            return 0
        assert 1 <= pitches_consumed
        if self.ignore_incomplete:
            return pitches_consumed
        dictionary = runtime["previous_section_voice_metadata"]
        dictionary = dictionary.get(_enums.RHYTHM.name, None)
        if dictionary:
            if dictionary.get("incomplete_final_note", False):
                pitches_consumed -= 1
        return pitches_consumed

    @property
    def parameter(self) -> str:
        """
        Gets persistence parameter.

        ..  container:: example

            >>> baca.PitchCommand().parameter
            'PITCH'

        """
        return _enums.PITCH.name

    @property
    def state(self):
        """
        Gets state dictionary.
        """
        return self._state


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class RegisterCommand(_command.Command):
    r"""
    Register command.

    ..  container:: example

        With music-commands:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration(
        ...             [("[A0, C8]", 15)],
        ...         ),
        ...     ),
        ... )
        >>> selection = stack([[10, 12, 14], [10, 12, 14], [10, 12, 14]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 9/16
                        bf''16
                        [
                        c'''16
                        d'''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        bf''16
                        [
                        c'''16
                        d'''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        bf''16
                        [
                        c'''16
                        d'''16
                        ]
                    }
                }
            >>

    ..  container:: example

        With section-commands:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.pitches("G4 G+4 G#4 G#+4 A~4 Ab4 Ab~4"),
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration([("[A0, C8]", 15)]),
        ...     ),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        g''8
                        [
                        gqs''8
                        gs''8
                        gtqs''8
                        ]
                        aqf''8
                        [
                        af''8
                        atqf''8
                        ]
                        g''8
                        [
                        gqs''8
                        gs''8
                        gtqs''8
                        ]
                        aqf''8
                        [
                        af''8
                        atqf''8
                        ]
                    }
                >>
            }

    ..  container:: example

        Works with chords:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration([("[A0, C8]", -6)]),
        ...     ),
        ... )
        >>> selection = stack([{10, 12, 14}])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 1/16
                        <bf c' d'>16
                    }
                }
            >>

    """

    registration: _pcollections.Registration | None = None

    def __post_init__(self):
        _command.Command.__post_init__(self)
        prototype = _pcollections.Registration
        assert isinstance(self.registration, prototype), repr(self.registration)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if self.registration is None:
            return False
        if self.selector:
            argument = self.selector(argument)
        plts = _select.plts(argument)
        assert isinstance(plts, list)
        for plt in plts:
            for pleaf in plt:
                if isinstance(pleaf, abjad.Note):
                    pitch = pleaf.written_pitch
                    pitches = self.registration([pitch])
                    pleaf.written_pitch = pitches[0]
                elif isinstance(pleaf, abjad.Chord):
                    pitches = pleaf.written_pitches
                    pitches = self.registration(pitches)
                    pleaf.written_pitches = pitches
                else:
                    raise TypeError(pleaf)
                abjad.detach(_enums.NOT_YET_REGISTERED, pleaf)
        return False


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class RegisterInterpolationCommand(_command.Command):
    r"""
    Register interpolation command.

    ..  container:: example

        With music-commands:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.register(0, 24),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/2
                        fs'16
                        [
                        e'16
                        ef'16
                        f'16
                        a'16
                        bf'16
                        c''16
                        b'16
                        af'16
                        g''16
                        cs''16
                        d''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        fs''16
                        [
                        e''16
                        ef''16
                        f''16
                        a''16
                        bf''16
                        c'''16
                        b''16
                        af''16
                        g'''16
                        cs'''16
                        d'''16
                        ]
                    }
                }
            >>

    ..  container:: example

        With chords:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.register(0, 24),
        ... )

        >>> collections = [
        ...     [6, 4], [3, 5], [9, 10], [0, 11], [8, 7], [1, 2],
        ... ]
        >>> collections = [set(_) for _ in collections]
        >>> selection = stack(collections)

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/8
                        <e' fs'>16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <f' ef''>16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <a' bf'>16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c'' b''>16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <g'' af''>16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <cs''' d'''>16
                    }
                }
            >>

    ..  container:: example

        Holds register constant:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = 4 * [(4, 8), (3, 8)]
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=time_signatures,
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> music = baca.make_even_divisions(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.pitches(pitches),
        ...     baca.register(12, 12),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        fs''8
                        [
                        e''8
                        ef''8
                        f''8
                        ]
                        a''8
                        [
                        bf''8
                        c''8
                        ]
                        b''8
                        [
                        af''8
                        g''8
                        cs''8
                        ]
                        d''8
                        [
                        fs''8
                        e''8
                        ]
                        ef''8
                        [
                        f''8
                        a''8
                        bf''8
                        ]
                        c''8
                        [
                        b''8
                        af''8
                        ]
                        g''8
                        [
                        cs''8
                        d''8
                        fs''8
                        ]
                        e''8
                        [
                        ef''8
                        f''8
                        ]
                    }
                >>
            }

    ..  container:: example

        Octave-transposes to a target interpolated from 12 down to 0:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = 4 * [(4, 8), (3, 8)]
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=time_signatures,
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(commands.get())
        >>> score["Music"].extend(music)
        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> commands(
        ...     "Music",
        ...     baca.pitches(pitches),
        ...     baca.register(12, 0),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        fs''8
                        [
                        e''8
                        ef''8
                        f''8
                        ]
                        a''8
                        [
                        bf'8
                        c''8
                        ]
                        b'8
                        [
                        af'8
                        g''8
                        cs''8
                        ]
                        d''8
                        [
                        fs'8
                        e''8
                        ]
                        ef''8
                        [
                        f'8
                        a'8
                        bf'8
                        ]
                        c''8
                        [
                        b'8
                        af'8
                        ]
                        g'8
                        [
                        cs''8
                        d'8
                        fs'8
                        ]
                        e'8
                        [
                        ef'8
                        f'8
                        ]
                    }
                >>
            }

    ..  container:: example

        Octave-transposes to a target interpolated from 0 up to 12:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = 4 * [(4, 8), (3, 8)]
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=time_signatures,
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(commands.get())
        >>> score["Music"].extend(music)
        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> commands(
        ...     "Music",
        ...     baca.pitches(pitches),
        ...     baca.register(0, 12),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        fs'8
                        [
                        e'8
                        ef'8
                        f'8
                        ]
                        a'8
                        [
                        bf'8
                        c''8
                        ]
                        b'8
                        [
                        af'8
                        g'8
                        cs''8
                        ]
                        d''8
                        [
                        fs'8
                        e''8
                        ]
                        ef''8
                        [
                        f''8
                        a'8
                        bf'8
                        ]
                        c''8
                        [
                        b'8
                        af'8
                        ]
                        g''8
                        [
                        cs''8
                        d''8
                        fs''8
                        ]
                        e''8
                        [
                        ef''8
                        f''8
                        ]
                    }
                >>
            }

    ..  container:: example

        Octave-transposes to a target interpolated from 12 down to -12:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = 4 * [(4, 8), (3, 8)]
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=time_signatures,
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(commands.get())
        >>> score["Music"].extend(music)
        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> commands(
        ...     "Music",
        ...     baca.pitches(pitches),
        ...     baca.register(12, -12),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        fs''8
                        [
                        e''8
                        ef''8
                        f''8
                        ]
                        a'8
                        [
                        bf'8
                        c''8
                        ]
                        b'8
                        [
                        af'8
                        g'8
                        cs''8
                        ]
                        d'8
                        [
                        fs'8
                        e'8
                        ]
                        ef'8
                        [
                        f'8
                        a'8
                        bf8
                        ]
                        c'8
                        [
                        b8
                        af8
                        ]
                        g8
                        [
                        cs'8
                        d'8
                        fs8
                        ]
                        e8
                        [
                        ef8
                        f8
                        ]
                    }
                >>
            }

    ..  container:: example

        Octave-transposes to a target interpolated from -12 up to 12:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = 4 * [(4, 8), (3, 8)]
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=time_signatures,
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(commands.get())
        >>> score["Music"].extend(music)
        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> commands(
        ...     "Music",
        ...     baca.pitches(pitches),
        ...     baca.register(-12, 12),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        fs8
                        [
                        e8
                        ef8
                        f8
                        ]
                        a8
                        [
                        bf8
                        c'8
                        ]
                        b8
                        [
                        af8
                        g'8
                        cs'8
                        ]
                        d'8
                        [
                        fs'8
                        e'8
                        ]
                        ef'8
                        [
                        f'8
                        a'8
                        bf'8
                        ]
                        c''8
                        [
                        b'8
                        af'8
                        ]
                        g'8
                        [
                        cs''8
                        d''8
                        fs''8
                        ]
                        e''8
                        [
                        ef''8
                        f''8
                        ]
                    }
                >>
            }

    ..  container:: example

        Selects tuplet 0:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.color(
        ...         lambda _: baca.select.tuplet(_, 0),
        ...         lone=True,
        ...     ),
        ...     baca.register(
        ...         0, 24,
        ...         selector=lambda _: baca.select.tuplet(_, 0),
        ...     ),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

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
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        \time 3/2
                        fs'16
                        [
                        \abjad-color-music #'green
                        e'16
                        \abjad-color-music #'green
                        ef''16
                        \abjad-color-music #'green
                        f''16
                        \abjad-color-music #'green
                        a'16
                        \abjad-color-music #'green
                        bf'16
                        \abjad-color-music #'green
                        c''16
                        \abjad-color-music #'green
                        b''16
                        \abjad-color-music #'green
                        af''16
                        \abjad-color-music #'green
                        g''16
                        \abjad-color-music #'green
                        cs'''16
                        \abjad-color-music #'green
                        d'''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        fs'16
                        [
                        e'16
                        ef'16
                        f'16
                        a'16
                        bf'16
                        c'16
                        b'16
                        af'16
                        g'16
                        cs'16
                        d'16
                        ]
                    }
                }
            >>

    ..  container:: example

        Selects tuplet -1:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.color(
        ...         lambda _: baca.select.tuplet(_, -1),
        ...         lone=True,
        ...     ),
        ...     baca.register(
        ...         0, 24,
        ...         selector=lambda _: baca.select.tuplet(_, -1),
        ...     ),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/2
                        fs'16
                        [
                        e'16
                        ef'16
                        f'16
                        a'16
                        bf'16
                        c'16
                        b'16
                        af'16
                        g'16
                        cs'16
                        d'16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        fs'16
                        [
                        \abjad-color-music #'green
                        e'16
                        \abjad-color-music #'green
                        ef''16
                        \abjad-color-music #'green
                        f''16
                        \abjad-color-music #'green
                        a'16
                        \abjad-color-music #'green
                        bf'16
                        \abjad-color-music #'green
                        c''16
                        \abjad-color-music #'green
                        b''16
                        \abjad-color-music #'green
                        af''16
                        \abjad-color-music #'green
                        g''16
                        \abjad-color-music #'green
                        cs'''16
                        \abjad-color-music #'green
                        d'''16
                        ]
                    }
                }
            >>

    ..  container:: example

        Maps to tuplets:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.color(
        ...         lambda _: abjad.select.tuplets(_)
        ...     ),
        ...     baca.new(
        ...         baca.register(0, 24),
        ...         map=lambda _: abjad.select.tuplets(_),
        ...     ),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

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
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        \time 3/2
                        fs'16
                        [
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        ef''16
                        \abjad-color-music #'red
                        f''16
                        \abjad-color-music #'red
                        a'16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'red
                        c''16
                        \abjad-color-music #'red
                        b''16
                        \abjad-color-music #'red
                        af''16
                        \abjad-color-music #'red
                        g''16
                        \abjad-color-music #'red
                        cs'''16
                        \abjad-color-music #'red
                        d'''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        fs'16
                        [
                        \abjad-color-music #'blue
                        e'16
                        \abjad-color-music #'blue
                        ef''16
                        \abjad-color-music #'blue
                        f''16
                        \abjad-color-music #'blue
                        a'16
                        \abjad-color-music #'blue
                        bf'16
                        \abjad-color-music #'blue
                        c''16
                        \abjad-color-music #'blue
                        b''16
                        \abjad-color-music #'blue
                        af''16
                        \abjad-color-music #'blue
                        g''16
                        \abjad-color-music #'blue
                        cs'''16
                        \abjad-color-music #'blue
                        d'''16
                        ]
                    }
                }
            >>

    """

    start_pitch: abjad.NumberedPitch = abjad.NumberedPitch(0)
    stop_pitch: abjad.NumberedPitch = abjad.NumberedPitch(0)

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert isinstance(self.start_pitch, abjad.NumberedPitch), repr(self.start_pitch)
        assert isinstance(self.stop_pitch, abjad.NumberedPitch), repr(self.stop_pitch)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if self.selector:
            argument = self.selector(argument)
        plts = _select.plts(argument)
        length = len(plts)
        for i, plt in enumerate(plts):
            registration = self._get_registration(i, length)
            for pleaf in plt:
                if isinstance(pleaf, abjad.Note):
                    written_pitches = registration([pleaf.written_pitch])
                    pleaf.written_pitch = written_pitches[0]
                elif isinstance(pleaf, abjad.Chord):
                    written_pitches = registration(pleaf.written_pitches)
                    pleaf.written_pitches = written_pitches
                else:
                    raise TypeError(pleaf)
                abjad.detach(_enums.NOT_YET_REGISTERED, pleaf)
        return False

    def _get_registration(self, i, length):
        start_pitch = self.start_pitch.number
        stop_pitch = self.stop_pitch.number
        compass = stop_pitch - start_pitch
        fraction = abjad.Fraction(i, length)
        addendum = fraction * compass
        current_pitch = start_pitch + addendum
        current_pitch = int(current_pitch)
        return _pcollections.Registration([("[A0, C8]", current_pitch)])


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class RegisterToOctaveCommand(_command.Command):
    r"""
    Register-to-octave command.

    ..  container:: example

        Chords:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.DOWN,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([{0, 14, 28}])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 1/16
                        <c' d'' e'''>16
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.CENTER,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([{0, 14, 28}])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 1/16
                        <c d' e''>16
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.UP,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([{0, 14, 28}])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 1/16
                        <c, d e'>16
                    }
                }
            >>

    ..  container:: example

        Disjunct notes:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.DOWN,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[0, 14, 28]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        c'16
                        [
                        d''16
                        e'''16
                        ]
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.CENTER,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[0, 14, 28]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        c16
                        [
                        d'16
                        e''16
                        ]
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.UP,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[0, 14, 28]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        c,16
                        [
                        d16
                        e'16
                        ]
                    }
                }
            >>

    ..  container:: example

        Conjunct notes:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.DOWN,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[10, 12, 14]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        bf'16
                        [
                        c''16
                        d''16
                        ]
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.CENTER,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[10, 12, 14]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        bf16
                        [
                        c'16
                        d'16
                        ]
                    }
                }
            >>

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.UP,
        ...         octave_number=4,
        ...     ),
        ... )

        >>> selection = stack([[10, 12, 14]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 3/16
                        bf16
                        [
                        c'16
                        d'16
                        ]
                    }
                }
            >>

    ..  container:: example

        Bass anchored at octave 5:

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(
        ...     anchor=abjad.DOWN,
        ...     octave_number=5,
        ... )
        >>> command(chord)
        False

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c'' d''' e''''>1

    ..  container:: example

        Center anchored at octave 5:

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(
        ...     anchor=abjad.CENTER,
        ...     octave_number=5,
        ... )
        >>> command(chord)
        False

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c' d'' e'''>1

    ..  container:: example

        Soprano anchored at octave 5:

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(
        ...     anchor=abjad.UP,
        ...     octave_number=5,
        ... )
        >>> command(chord)
        False

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c d' e''>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> staff = abjad.Staff([chord])
        >>> abjad.attach(abjad.Clef("bass"), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            \clef "bass"
            <c, d e'>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(octave_number=1)
        >>> command(chord)
        False

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c,, d, e>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(octave_number=2)
        >>> command(chord)
        False

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c, d e'>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(octave_number=3)
        >>> command(chord)
        False

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c d' e''>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(octave_number=4)
        >>> command(chord)
        False

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c' d'' e'''>1

    ..  container:: example

        >>> chord = abjad.Chord("<c, d e'>1")
        >>> command = baca.RegisterToOctaveCommand(octave_number=5)
        >>> command(chord)
        False

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c'' d''' e''''>1

    """

    anchor: abjad.Vertical = abjad.DOWN
    octave_number: int | None = None

    def __post_init__(self):
        _command.Command.__post_init__(self)
        prototype = (abjad.CENTER, abjad.DOWN, abjad.UP)
        assert self.anchor in prototype, repr(self.anchor)
        assert isinstance(self.octave_number, int), repr(self.octave_number)

    __repr__ = _command.Command.__repr__

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if self.octave_number is None:
            return False
        if self.selector:
            argument = self.selector(argument)
        pitches = abjad.iterate.pitches(argument)
        octave_adjustment = _pcollections.pitches_to_octave_adjustment(
            pitches, anchor=self.anchor, octave_number=self.octave_number
        )
        pleaves = _select.pleaves(argument)
        for pleaf in pleaves:
            self._set_pitch(pleaf, lambda _: _.transpose(n=12 * octave_adjustment))
        return False

    def _set_pitch(self, leaf, transposition):
        if isinstance(leaf, abjad.Note):
            pitch = transposition(leaf.written_pitch)
            leaf.written_pitch = pitch
        elif isinstance(leaf, abjad.Chord):
            pitches = [transposition(_) for _ in leaf.written_pitches]
            leaf.written_pitches = pitches
        abjad.detach(_enums.NOT_YET_REGISTERED, leaf)


class SchemeManifest:
    """
    Scheme manifest.

    New functions defined in ``~/baca/lilypond/baca.ily`` must currently be added here by
    hand.

    TODO: eliminate duplication. Define custom Scheme functions here (``SchemeManifest``)
    and teach ``SchemeManifest`` to write ``~/baca/lilypond/baca.ily`` automatically.
    """

    _dynamics = (
        ("baca-appena-udibile", "appena udibile"),
        ("baca-f-but-accents-sffz", "f"),
        ("baca-f-sub-but-accents-continue-sffz", "f"),
        ("baca-ffp", "p"),
        ("baca-fffp", "p"),
        ("niente", "niente"),
        ("baca-p-sub-but-accents-continue-sffz", "p"),
        #
        ("baca-pppf", "f"),
        ("baca-pppff", "ff"),
        ("baca-pppfff", "fff"),
        #
        ("baca-ppf", "f"),
        ("baca-ppff", "ff"),
        ("baca-ppfff", "fff"),
        #
        ("baca-pf", "f"),
        ("baca-pff", "ff"),
        ("baca-pfff", "fff"),
        #
        ("baca-ppp-ppp", "ppp"),
        ("baca-ppp-pp", "pp"),
        ("baca-ppp-p", "p"),
        ("baca-ppp-mp", "mp"),
        ("baca-ppp-mf", "mf"),
        ("baca-ppp-f", "f"),
        ("baca-ppp-ff", "ff"),
        ("baca-ppp-fff", "fff"),
        #
        ("baca-pp-ppp", "ppp"),
        ("baca-pp-pp", "pp"),
        ("baca-pp-p", "p"),
        ("baca-pp-mp", "mp"),
        ("baca-pp-mf", "mf"),
        ("baca-pp-f", "f"),
        ("baca-pp-ff", "ff"),
        ("baca-pp-fff", "fff"),
        #
        ("baca-p-ppp", "ppp"),
        ("baca-p-pp", "pp"),
        ("baca-p-p", "p"),
        ("baca-p-mp", "mp"),
        ("baca-p-mf", "mf"),
        ("baca-p-f", "f"),
        ("baca-p-ff", "ff"),
        ("baca-p-fff", "fff"),
        #
        ("baca-mp-ppp", "ppp"),
        ("baca-mp-pp", "pp"),
        ("baca-mp-p", "p"),
        ("baca-mp-mp", "mp"),
        ("baca-mp-mf", "mf"),
        ("baca-mp-f", "f"),
        ("baca-mp-ff", "ff"),
        ("baca-mp-fff", "fff"),
        #
        ("baca-mf-ppp", "ppp"),
        ("baca-mf-pp", "pp"),
        ("baca-mf-p", "p"),
        ("baca-mf-mp", "mp"),
        ("baca-mf-mf", "mf"),
        ("baca-mf-f", "f"),
        ("baca-mf-ff", "ff"),
        ("baca-mf-fff", "fff"),
        #
        ("baca-f-ppp", "ppp"),
        ("baca-f-pp", "pp"),
        ("baca-f-p", "p"),
        ("baca-f-mp", "mp"),
        ("baca-f-mf", "mf"),
        ("baca-f-f", "f"),
        ("baca-f-ff", "ff"),
        ("baca-f-fff", "fff"),
        #
        ("baca-ff-ppp", "ppp"),
        ("baca-ff-pp", "pp"),
        ("baca-ff-p", "p"),
        ("baca-ff-mp", "mp"),
        ("baca-ff-mf", "mf"),
        ("baca-ff-f", "f"),
        ("baca-ff-ff", "ff"),
        ("baca-ff-fff", "fff"),
        #
        ("baca-fff-ppp", "ppp"),
        ("baca-fff-pp", "pp"),
        ("baca-fff-p", "p"),
        ("baca-fff-mp", "mp"),
        ("baca-fff-mf", "mf"),
        ("baca-fff-f", "f"),
        ("baca-fff-ff", "ff"),
        ("baca-fff-fff", "fff"),
        #
        ("baca-sff", "ff"),
        ("baca-sffp", "p"),
        ("baca-sffpp", "pp"),
        ("baca-sfffz", "fff"),
        ("baca-sffz", "ff"),
        ("baca-sfpp", "pp"),
        ("baca-sfz-f", "f"),
        ("baca-sfz-p", "p"),
    )

    ### PUBLIC PROPERTIES ###

    @property
    def dynamics(self) -> list[str]:
        """
        Gets dynamics.

        ..  container:: example

            >>> scheme_manifest = baca.SchemeManifest()
            >>> for dynamic in scheme_manifest.dynamics:
            ...     dynamic
            ...
            'baca-appena-udibile'
            'baca-f-but-accents-sffz'
            'baca-f-sub-but-accents-continue-sffz'
            'baca-ffp'
            'baca-fffp'
            'niente'
            'baca-p-sub-but-accents-continue-sffz'
            'baca-pppf'
            'baca-pppff'
            'baca-pppfff'
            'baca-ppf'
            'baca-ppff'
            'baca-ppfff'
            'baca-pf'
            'baca-pff'
            'baca-pfff'
            'baca-ppp-ppp'
            'baca-ppp-pp'
            'baca-ppp-p'
            'baca-ppp-mp'
            'baca-ppp-mf'
            'baca-ppp-f'
            'baca-ppp-ff'
            'baca-ppp-fff'
            'baca-pp-ppp'
            'baca-pp-pp'
            'baca-pp-p'
            'baca-pp-mp'
            'baca-pp-mf'
            'baca-pp-f'
            'baca-pp-ff'
            'baca-pp-fff'
            'baca-p-ppp'
            'baca-p-pp'
            'baca-p-p'
            'baca-p-mp'
            'baca-p-mf'
            'baca-p-f'
            'baca-p-ff'
            'baca-p-fff'
            'baca-mp-ppp'
            'baca-mp-pp'
            'baca-mp-p'
            'baca-mp-mp'
            'baca-mp-mf'
            'baca-mp-f'
            'baca-mp-ff'
            'baca-mp-fff'
            'baca-mf-ppp'
            'baca-mf-pp'
            'baca-mf-p'
            'baca-mf-mp'
            'baca-mf-mf'
            'baca-mf-f'
            'baca-mf-ff'
            'baca-mf-fff'
            'baca-f-ppp'
            'baca-f-pp'
            'baca-f-p'
            'baca-f-mp'
            'baca-f-mf'
            'baca-f-f'
            'baca-f-ff'
            'baca-f-fff'
            'baca-ff-ppp'
            'baca-ff-pp'
            'baca-ff-p'
            'baca-ff-mp'
            'baca-ff-mf'
            'baca-ff-f'
            'baca-ff-ff'
            'baca-ff-fff'
            'baca-fff-ppp'
            'baca-fff-pp'
            'baca-fff-p'
            'baca-fff-mp'
            'baca-fff-mf'
            'baca-fff-f'
            'baca-fff-ff'
            'baca-fff-fff'
            'baca-sff'
            'baca-sffp'
            'baca-sffpp'
            'baca-sfffz'
            'baca-sffz'
            'baca-sfpp'
            'baca-sfz-f'
            'baca-sfz-p'

        """
        return [_[0] for _ in self._dynamics]

    ### PUBLIC METHODS ###

    def dynamic_to_steady_state(self, dynamic):
        """
        Changes ``dynamic`` to steady state.

        ..  container:: example

            >>> scheme_manifest = baca.SchemeManifest()
            >>> scheme_manifest.dynamic_to_steady_state("sfz-p")
            'p'

        Returns string.
        """
        for dynamic_, steady_state in self._dynamics:
            if dynamic_ == dynamic:
                return steady_state
            if dynamic_ == "baca-" + dynamic:
                return steady_state
        raise KeyError(dynamic)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class StaffPositionCommand(_command.Command):
    r"""
    Staff position command.

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' f'")
        >>> abjad.attach(abjad.Clef("treble"), staff[0])
        >>> command = baca.staff_positions([0, 2])
        >>> command(staff)
        False

        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "treble"
                b'4
                d''4
                b'4
                d''4
            }

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' f'")
        >>> abjad.attach(abjad.Clef("percussion"), staff[0])
        >>> command = baca.staff_positions([0, 2])
        >>> command(staff)
        False

        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "percussion"
                c'4
                e'4
                c'4
                e'4
            }

    """

    numbers: typing.Sequence[int | list | abjad.StaffPosition] = ()
    allow_hidden: bool = False
    allow_out_of_range: bool = False
    allow_repeats: bool = False
    allow_repitch: bool = False
    exact: bool = False
    mock: bool = False
    selector: typing.Callable = lambda _: _select.plts(_)
    set_chord_pitches_equal: bool = False

    def __post_init__(self):
        _command.Command.__post_init__(self)
        prototype = (int, list, abjad.StaffPosition)
        assert all(isinstance(_, prototype) for _ in self.numbers), repr(self.numbers)
        assert isinstance(self.allow_hidden, bool), repr(self.allow_hidden)
        assert isinstance(self.allow_out_of_range, bool), repr(self.allow_out_of_range)
        assert isinstance(self.allow_repeats, bool), repr(self.allow_repeats)
        assert isinstance(self.allow_repitch, bool), repr(self.allow_repitch)
        assert isinstance(self.mock, bool), repr(self.mock)
        assert isinstance(self.exact, bool), repr(self.exact)
        assert isinstance(self.set_chord_pitches_equal, bool), repr(
            self.set_chord_pitches_equal
        )

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if not self.numbers:
            return False
        if self.selector:
            argument = self.selector(argument)
        numbers = abjad.CyclicTuple(self.numbers)
        mutated_score = _staff_position_function(
            argument,
            numbers,
            allow_hidden=self.allow_hidden,
            allow_out_of_range=self.allow_out_of_range,
            allow_repeats=self.allow_repeats,
            allow_repitch=self.allow_repitch,
            exact=self.exact,
            set_chord_pitches_equal=self.set_chord_pitches_equal,
        )
        return mutated_score


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class StaffPositionInterpolationCommand(_command.Command):

    start: int | str | abjad.NamedPitch | abjad.StaffPosition | None = None
    stop: int | str | abjad.NamedPitch | abjad.StaffPosition | None = None
    allow_hidden: bool = False
    mock: bool = False
    pitches_instead_of_staff_positions: bool = False
    selector: typing.Callable = lambda _: _select.plts(_)

    def __post_init__(self):
        _command.Command.__post_init__(self)
        prototype = (abjad.NamedPitch, abjad.StaffPosition)
        if isinstance(self.start, str):
            self.start = abjad.NamedPitch(self.start)
        elif isinstance(self.start, int):
            self.start = abjad.StaffPosition(self.start)
        assert isinstance(self.start, prototype), repr(self.start)
        if isinstance(self.stop, str):
            self.stop = abjad.NamedPitch(self.stop)
        elif isinstance(self.stop, int):
            self.stop = abjad.StaffPosition(self.stop)
        assert isinstance(self.stop, prototype), repr(self.stop)
        assert isinstance(self.allow_hidden, bool), repr(self.allow_hidden)
        assert isinstance(self.mock, bool), repr(self.mock)
        assert isinstance(self.pitches_instead_of_staff_positions, bool)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if self.selector:
            argument = self.selector(argument)
        plts = _select.plts(argument)
        if not plts:
            return False
        count = len(plts)
        if isinstance(self.start, abjad.StaffPosition):
            start_staff_position = self.start
        else:
            start_phead = plts[0].head
            clef = abjad.get.effective(start_phead, abjad.Clef)
            start_staff_position = clef.to_staff_position(self.start)
        if isinstance(self.stop, abjad.StaffPosition):
            stop_staff_position = self.stop
        else:
            stop_phead = plts[-1].head
            clef = abjad.get.effective(
                stop_phead,
                abjad.Clef,
                default=abjad.Clef("treble"),
            )
            stop_staff_position = clef.to_staff_position(self.stop)
        unit_distance = abjad.Fraction(
            stop_staff_position.number - start_staff_position.number, count - 1
        )
        for i, plt in enumerate(plts):
            staff_position = unit_distance * i + start_staff_position.number
            staff_position = round(staff_position)
            staff_position = abjad.StaffPosition(staff_position)
            clef = abjad.get.effective(
                plt.head,
                abjad.Clef,
                default=abjad.Clef("treble"),
            )
            pitch = clef.to_pitch(staff_position)
            new_lt = _set_lt_pitch(
                plt,
                pitch,
                allow_hidden=self.allow_hidden,
                allow_repitch=True,
                mock=self.mock,
            )
            assert new_lt is None, repr(new_lt)
            for leaf in plt:
                abjad.attach(_enums.ALLOW_REPEAT_PITCH, leaf)
                if not self.pitches_instead_of_staff_positions:
                    abjad.attach(_enums.STAFF_POSITION, leaf)
        if isinstance(self.start, abjad.NamedPitch):
            start_pitch = self.start
        else:
            assert isinstance(self.start, abjad.StaffPosition)
            clef = abjad.get.effective(
                plts[0],
                abjad.Clef,
                default=abjad.Clef("treble"),
            )
            start_pitch = clef.to_pitch(self.start)
        new_lt = _set_lt_pitch(
            plts[0],
            start_pitch,
            allow_hidden=self.allow_hidden,
            allow_repitch=True,
            mock=self.mock,
        )
        assert new_lt is None, repr(new_lt)
        if isinstance(self.stop, abjad.NamedPitch):
            stop_pitch = self.stop
        else:
            assert isinstance(self.stop, abjad.StaffPosition)
            clef = abjad.get.effective(
                plts[0],
                abjad.Clef,
                default=abjad.Clef("treble"),
            )
            stop_pitch = clef.to_pitch(self.stop)
        new_lt = _set_lt_pitch(
            plts[-1],
            stop_pitch,
            allow_hidden=self.allow_hidden,
            allow_repitch=True,
            mock=self.mock,
        )
        assert new_lt is None, repr(new_lt)
        return False


def bass_to_octave(
    n: int,
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> RegisterToOctaveCommand:
    r"""
    Octave-transposes music.

    ..  container:: example

        Octave-transposes music such that the lowest note in the entire selection appears
        in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.bass_to_octave(3),
        ...     baca.color(
        ...         lambda _: baca.select.plts(_),
        ...         lone=True,
        ...     ),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        \time 5/4
                        <c d bf>8
                        [
                        ~
                        \abjad-color-music #'green
                        <c d bf>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        f'8
                        [
                        ~
                        \abjad-color-music #'green
                        f'32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <ef' e' fs''>8
                        [
                        ~
                        \abjad-color-music #'green
                        <ef' e' fs''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <g af'>8
                        [
                        ~
                        \abjad-color-music #'green
                        <g af'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        a8
                        [
                        ~
                        \abjad-color-music #'green
                        a32
                        ]
                        r16.
                    }
                }
            >>

    ..  container:: example

        Octave-transposes music such that the lowest pitch in each pitched logical tie
        appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.bass_to_octave(3),
        ...         map=lambda _: baca.select.plts(_),
        ...     ),
        ...     baca.color(lambda _: baca.select.plts(_)),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        \time 5/4
                        <c d bf>8
                        [
                        ~
                        \abjad-color-music #'red
                        <c d bf>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        f8
                        [
                        ~
                        \abjad-color-music #'blue
                        f32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        <ef e fs'>8
                        [
                        ~
                        \abjad-color-music #'red
                        <ef e fs'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        <g af'>8
                        [
                        ~
                        \abjad-color-music #'blue
                        <g af'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        a8
                        [
                        ~
                        \abjad-color-music #'red
                        a32
                        ]
                        r16.
                    }
                }
            >>

    """
    return RegisterToOctaveCommand(
        anchor=abjad.DOWN, octave_number=n, selector=selector
    )


def center_to_octave(
    n: int,
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> RegisterToOctaveCommand:
    r"""
    Octave-transposes music.

    ..  container:: example

        Octave-transposes music such that the centroid of all PLTs appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.center_to_octave(3),
        ...     baca.color(
        ...         lambda _: baca.select.plts(_),
        ...         lone=True,
        ...     ),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        \time 5/4
                        <c, d, bf,>8
                        [
                        ~
                        \abjad-color-music #'green
                        <c, d, bf,>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        f8
                        [
                        ~
                        \abjad-color-music #'green
                        f32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <ef e fs'>8
                        [
                        ~
                        \abjad-color-music #'green
                        <ef e fs'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <g, af>8
                        [
                        ~
                        \abjad-color-music #'green
                        <g, af>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        a,8
                        [
                        ~
                        \abjad-color-music #'green
                        a,32
                        ]
                        r16.
                    }
                }
            >>

    ..  container:: example

        Octave-transposes music such that the centroid of each pitched logical tie
        appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.center_to_octave(3),
        ...         map=lambda _: baca.select.plts(_),
        ...     ),
        ...     baca.color(lambda _: baca.select.plts(_)),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        \time 5/4
                        <c d bf>8
                        [
                        ~
                        \abjad-color-music #'red
                        <c d bf>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        f8
                        [
                        ~
                        \abjad-color-music #'blue
                        f32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        <ef e fs'>8
                        [
                        ~
                        \abjad-color-music #'red
                        <ef e fs'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        <g, af>8
                        [
                        ~
                        \abjad-color-music #'blue
                        <g, af>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        a8
                        [
                        ~
                        \abjad-color-music #'red
                        a32
                        ]
                        r16.
                    }
                }
            >>

    """
    return RegisterToOctaveCommand(
        anchor=abjad.CENTER, octave_number=n, selector=selector
    )


def color_fingerings(
    numbers: list[int],
    *tweaks: _typings.IndexedTweak,
    selector=lambda _: _select.pheads(_, exclude=_enums.HIDDEN),
) -> ColorFingeringCommand:
    return ColorFingeringCommand(numbers=numbers, selector=selector, tweaks=tweaks)


def deviation(
    deviations: list[int | float],
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> MicrotoneDeviationCommand:
    return MicrotoneDeviationCommand(deviations=deviations, selector=selector)


def diatonic_clusters(
    widths: list[int],
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> DiatonicClusterCommand:
    return DiatonicClusterCommand(selector=selector, widths=widths)


def displacement(
    displacements: list[int],
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> OctaveDisplacementCommand:
    r"""
    Octave-displaces ``selector`` output.

    ..  container:: example

        Octave-displaces PLTs:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.displacement([0, 0, -1, -1, 1, 1]),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack(3 * [[0, 2, 3]])

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
                        \time 27/16
                        r8
                        c'16
                        [
                        d'16
                        ]
                        ef4
                        ~
                        ef16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/8
                    {
                        c16
                        [
                        d''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 11/12
                    {
                        c'16
                        [
                        d'16
                        ]
                        ef4
                        ~
                        ef16
                        r16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Octave-displaces chords:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [4],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...     ),
        ...     rmakers.beam(),
        ...     baca.displacement([0, 0, -1, -1, 1, 1]),
        ... )
        >>> selection = stack(6 * [{0, 2, 3}])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 15/8
                        r8
                        <c' d' ef'>4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c' d' ef'>4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c d ef>4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c d ef>4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c'' d'' ef''>4
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <c'' d'' ef''>4
                        r4
                    }
                }
            >>

    """
    return OctaveDisplacementCommand(displacements=displacements, selector=selector)


def dynamic(
    dynamic: str | abjad.Dynamic,
    *tweaks: abjad.Tweak,
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    selector=lambda _: _select.phead(_, 0),
    redundant: bool = False,
) -> IndicatorCommand:
    r"""
    Attaches dynamic.

    ..  container:: example

        Attaches dynamic to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.dynamic("f"),
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
                        \f
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Works with effort dynamics:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.dynamic('"f"'),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(
        ...     selection, includes=["baca.ily"]
        ... )
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
                        \baca-effort-f
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Works with hairpins:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 13)),
        ... )

        >>> music = baca.make_even_divisions(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.pitches("E4 D5 F4 C5 G4 F5"),
        ...     baca.dynamic("p"),
        ...     baca.dynamic("<"),
        ...     baca.dynamic(
        ...         "!",
        ...         selector=lambda _: baca.select.pleaf(_, -1),
        ...     ),
        ...     baca.dls_staff_padding(5),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #13
                        \time 4/8
                        s1 * 4/8
                        \baca-new-spacing-section #1 #13
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #13
                        \time 4/8
                        s1 * 4/8
                        \baca-new-spacing-section #1 #13
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \override DynamicLineSpanner.staff-padding = 5
                        e'8
                        - \tweak color #(x11-color 'blue)
                        \p
                        [
                        \<
                        d''8
                        f'8
                        c''8
                        ]
                        g'8
                        [
                        f''8
                        e'8
                        ]
                        d''8
                        [
                        f'8
                        c''8
                        g'8
                        ]
                        f''8
                        [
                        e'8
                        d''8
                        \!
                        ]
                        \revert DynamicLineSpanner.staff-padding
                    }
                >>
            }

    ..  container:: example

        Works with tweaks:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )

        >>> music = baca.make_even_divisions(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.pitches("E4 D5 F4 C5 G4 F5"),
        ...     baca.dynamic(
        ...         "p",
        ...         abjad.Tweak(r"- \tweak extra-offset #'(-4 . 0)"),
        ...     ),
        ...     baca.dls_staff_padding(5),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 4/8
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 4/8
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \override DynamicLineSpanner.staff-padding = 5
                        e'8
                        - \tweak extra-offset #'(-4 . 0)
                        \p
                        [
                        d''8
                        f'8
                        c''8
                        ]
                        g'8
                        [
                        f''8
                        e'8
                        ]
                        d''8
                        [
                        f'8
                        c''8
                        g'8
                        ]
                        f''8
                        [
                        e'8
                        d''8
                        ]
                        \revert DynamicLineSpanner.staff-padding
                    }
                >>
            }

    """
    if isinstance(dynamic, str):
        indicator = make_dynamic(dynamic)
    else:
        indicator = dynamic
    prototype = (abjad.Dynamic, abjad.StartHairpin, abjad.StopHairpin)
    assert isinstance(indicator, prototype), repr(indicator)
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return IndicatorCommand(
        context="Voice",
        indicators=[indicator],
        map=map,
        match=match,
        measures=measures,
        redundant=redundant,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dynamic_function(
    leaf: abjad.Leaf,
    dynamic: str | abjad.Dynamic,
    *tweaks: abjad.Tweak,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(dynamic, str):
        indicator = make_dynamic(dynamic)
    else:
        indicator = dynamic
    prototype = (abjad.Dynamic, abjad.StartHairpin, abjad.StopHairpin)
    assert isinstance(indicator, prototype), repr(indicator)
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    # tag = _tags.function_name(_frame())
    tag = abjad.Tag("baca.dynamic()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    _attach_persistent_indicator(
        leaf,
        [indicator],
        manifests={},
        tag=tag,
    )


def force_accidental(
    selector=lambda _: _select.pleaf(_, 0, exclude=_enums.HIDDEN),
) -> AccidentalAdjustmentCommand:
    r"""
    Forces accidental.

    ..  container:: example

        Inverts edition-specific tags:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_notes(commands.get(), repeat_ties=True)
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.pitches("E4 F4"),
        ...     baca.not_parts(
        ...         baca.force_accidental(
        ...             selector=lambda _: baca.select.pleaves(_)[:2],
        ...         ),
        ...     ),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        e'2
                        %@% e'!2
                        f'4.
                        %@% f'!4.
                        e'2
                        f'4.
                    }
                >>
            }

    """
    return AccidentalAdjustmentCommand(forced=True, selector=selector)


def interpolate_pitches(
    start: int | str | abjad.NamedPitch,
    stop: int | str | abjad.NamedPitch,
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    allow_hidden: bool = False,
    mock: bool = False,
) -> StaffPositionInterpolationCommand:
    r"""
    Interpolates from staff position of ``start`` pitch to staff position of ``stop``
    pitch.

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.clef("treble"),
        ...     baca.interpolate_pitches("Eb4", "F#5"),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

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
                    \scaleDurations #'(1 . 1)
                    {
                        \clef "treble"
                        \time 3/2
                        ef'16
                        [
                        e'16
                        f'16
                        f'16
                        f'16
                        g'16
                        g'16
                        g'16
                        a'16
                        a'16
                        a'16
                        b'16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        b'16
                        [
                        c''16
                        c''16
                        c''16
                        d''16
                        d''16
                        d''16
                        e''16
                        e''16
                        e''16
                        f''16
                        fs''16
                        ]
                    }
                }
            >>

    ..  container:: example

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.clef("treble"),
        ...     baca.interpolate_pitches("Eb4", "F#5"),
        ...     baca.glissando(
        ...         allow_repeats=True,
        ...         hide_middle_note_heads=True,
        ...     ),
        ...     baca.glissando_thickness(3),
        ... )

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> selection = stack(collections)

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
                    \scaleDurations #'(1 . 1)
                    {
                        \override Glissando.thickness = 3
                        \clef "treble"
                        \time 3/2
                        ef'16
                        [
                        \glissando
                        \hide NoteHead
                        \override Accidental.stencil = ##f
                        \override NoteColumn.glissando-skip = ##t
                        \override NoteHead.no-ledgers = ##t
                        e'16
                        f'16
                        f'16
                        f'16
                        g'16
                        g'16
                        g'16
                        a'16
                        a'16
                        a'16
                        b'16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        b'16
                        [
                        c''16
                        c''16
                        c''16
                        d''16
                        d''16
                        d''16
                        e''16
                        e''16
                        e''16
                        f''16
                        \revert Accidental.stencil
                        \revert NoteColumn.glissando-skip
                        \revert NoteHead.no-ledgers
                        \undo \hide NoteHead
                        fs''16
                        ]
                        \revert Glissando.thickness
                    }
                }
            >>

    """
    start_ = abjad.NamedPitch(start)
    stop_ = abjad.NamedPitch(stop)
    return StaffPositionInterpolationCommand(
        start=start_,
        stop=stop_,
        allow_hidden=allow_hidden,
        mock=mock,
        pitches_instead_of_staff_positions=True,
        selector=selector,
    )


_interpolate_pitches_function = interpolate_pitches


def interpolate_staff_positions(
    start: int | abjad.StaffPosition,
    stop: int | abjad.StaffPosition,
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    allow_hidden: bool = False,
    mock: bool = False,
) -> StaffPositionInterpolationCommand:
    """
    Interpolates from ``start`` staff position to ``stop`` staff position.
    """
    if isinstance(start, abjad.StaffPosition):
        start_ = start
    else:
        start_ = abjad.StaffPosition(start)
    if isinstance(stop, abjad.StaffPosition):
        stop_ = stop
    else:
        stop_ = abjad.StaffPosition(stop)
    return StaffPositionInterpolationCommand(
        start=start_,
        stop=stop_,
        allow_hidden=allow_hidden,
        mock=mock,
        selector=selector,
    )


_interpolate_staff_positions_function = interpolate_staff_positions


def levine_multiphonic(n: int) -> abjad.Markup:
    assert isinstance(n, int), repr(n)
    return abjad.Markup(rf'\baca-boxed-markup "L.{n}"')


def loop(
    pitches: list[int],
    intervals: list[int],
    *,
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> PitchCommand:
    """
    Loops ``pitches`` at ``intervals``.
    """
    loop = Loop(pitches, intervals)
    return _pitches_command_factory(loop, selector=selector)


def make_dynamic(
    string: str, *, forbid_al_niente_to_bar_line: bool = False
) -> abjad.Dynamic | abjad.StartHairpin | abjad.StopHairpin | abjad.Bundle:
    r"""
    Makes dynamic.

    ..  container:: example

        >>> baca.make_dynamic("p")
        Dynamic(name='p', command=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic("sffz")
        Dynamic(name='ff', command='\\baca-sffz', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=3)

        >>> baca.make_dynamic("niente")
        Dynamic(name='niente', command='\\!', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=NegativeInfinity())

        >>> baca.make_dynamic("<")
        StartHairpin(shape='<')

        >>> baca.make_dynamic("o<|")
        StartHairpin(shape='o<|')

        >>> baca.make_dynamic("appena-udibile")
        Dynamic(name='appena udibile', command='\\baca-appena-udibile', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=None)

    ..  container:: example

        Stop hairpin:

        >>> baca.make_dynamic("!")
        StopHairpin(leak=False)

    ..  container:: example

        Ancora dynamics:

        >>> baca.make_dynamic("p-ancora")
        Dynamic(name='p', command='\\baca-p-ancora', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic("f-ancora")
        Dynamic(name='f', command='\\baca-f-ancora', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Composite dynamics:

        >>> baca.make_dynamic("pf")
        Dynamic(name='f', command='\\baca-pf', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=2)

        >>> baca.make_dynamic("pff")
        Dynamic(name='ff', command='\\baca-pff', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=3)

    ..  container:: example

        Effort dynamics:

        >>> baca.make_dynamic('"p"')
        Dynamic(name='"p"', command='\\baca-effort-p', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic('"f"')
        Dynamic(name='"f"', command='\\baca-effort-f', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Effort dynamics (parenthesized):

        >>> baca.make_dynamic('("p")')
        Dynamic(name='p', command='\\baca-effort-p-parenthesized', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic('("f")')
        Dynamic(name='f', command='\\baca-effort-f-parenthesized', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Effort dynamics (ancora):

        >>> baca.make_dynamic('"p"-ancora')
        Dynamic(name='p', command='\\baca-effort-ancora-p', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic('"f"-ancora')
        Dynamic(name='f', command='\\baca-effort-ancora-f', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Effort dynamics (sempre):

        >>> baca.make_dynamic('"p"-sempre')
        Dynamic(name='p', command='\\baca-effort-p-sempre', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic('"f"-sempre')
        Dynamic(name='f', command='\\baca-effort-f-sempre', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Sub. effort dynamics:

        >>> baca.make_dynamic("p-effort-sub")
        Dynamic(name='p', command='\\baca-p-effort-sub', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic("f-effort-sub")
        Dynamic(name='f', command='\\baca-f-effort-sub', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Mezzo:

        >>> baca.make_dynamic("m")
        Dynamic(name='m', command='\\baca-m', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=None)

    ..  container:: example

        Parenthesized dynamics:

        >>> baca.make_dynamic("(p)")
        Dynamic(name='p', command='\\baca-p-parenthesized', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic("(f)")
        Dynamic(name='f', command='\\baca-f-parenthesized', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Poco scratch dynamics:

        >>> baca.make_dynamic("p-poco-scratch")
        Dynamic(name='p', command='\\baca-p-poco-scratch', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic("f-poco-scratch")
        Dynamic(name='f', command='\\baca-f-poco-scratch', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Possibile dynamics:

        >>> baca.make_dynamic("p-poss")
        Dynamic(name='p', command='\\baca-p-poss', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic("f-poss")
        Dynamic(name='f', command='\\baca-f-poss', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Scratch dynamics:

        >>> baca.make_dynamic("p-scratch")
        Dynamic(name='p', command='\\baca-p-scratch', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic("f-scratch")
        Dynamic(name='f', command='\\baca-f-scratch', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Sempre dynamics:

        >>> baca.make_dynamic("p-sempre")
        Dynamic(name='p', command='\\baca-p-sempre', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic("f-sempre")
        Dynamic(name='f', command='\\baca-f-sempre', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Subito dynamics:

        >>> baca.make_dynamic("p-sub")
        Dynamic(name='p', command='\\baca-p-sub', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic("f-sub")
        Dynamic(name='f', command='\\baca-f-sub', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Whiteout dynamics:

        >>> baca.make_dynamic("p-whiteout")
        Dynamic(name='p', command='\\baca-p-whiteout', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2)

        >>> baca.make_dynamic("f-whiteout")
        Dynamic(name='f', command='\\baca-f-whiteout', format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2)

    ..  container:: example

        Al niente hairpins are special-cased to carry to-barline tweaks:

        >>> baca.make_dynamic(">o")
        Bundle(indicator=StartHairpin(shape='>o'), tweaks=(Tweak(string='- \\tweak to-barline ##t', tag=None),))

        >>> baca.make_dynamic("|>o")
        Bundle(indicator=StartHairpin(shape='|>o'), tweaks=(Tweak(string='- \\tweak to-barline ##t', tag=None),))

    ..  container:: example exception

        Errors on nondynamic input:

        >>> baca.make_dynamic("text")
        Traceback (most recent call last):
            ...
        Exception: the string 'text' initializes no known dynamic.

    """
    assert isinstance(string, str), repr(string)
    scheme_manifest = SchemeManifest()
    known_shapes = abjad.StartHairpin("<").known_shapes
    indicator: abjad.Dynamic | abjad.StartHairpin | abjad.StopHairpin | abjad.Bundle
    if "_" in string:
        raise Exception(f"use hyphens instead of underscores ({string!r}).")
    if string == "niente":
        indicator = abjad.Dynamic("niente", command=r"\!")
    elif string.endswith("-ancora") and '"' not in string:
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-ancora"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-ancora") and '"' in string:
        dynamic = string.split("-")[0]
        dynamic = dynamic.strip('"')
        command = rf"\baca-effort-ancora-{dynamic}"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-effort-sub"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-effort-sub"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.startswith('("') and string.endswith('")'):
        dynamic = string.strip('(")')
        command = rf"\baca-effort-{dynamic}-parenthesized"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.startswith("(") and string.endswith(")"):
        dynamic = string.strip("()")
        command = rf"\baca-{dynamic}-parenthesized"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-poco-scratch"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-poco-scratch"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-poss"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-poss"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-scratch"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-scratch"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-sempre") and not string.startswith('"'):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-sempre"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-sempre") and string.startswith('"'):
        dynamic = string.split("-")[0].strip('"')
        command = rf"\baca-effort-{dynamic}-sempre"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-sub"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-sub"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-whiteout"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-whiteout"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif "baca-" + string in scheme_manifest.dynamics:
        name = scheme_manifest.dynamic_to_steady_state(string)
        command = "\\baca-" + string
        pieces = string.split("-")
        if pieces[0] in ("sfz", "sffz", "sfffz"):
            sforzando = True
        else:
            sforzando = False
        name_is_textual = not (sforzando)
        indicator = abjad.Dynamic(
            name,
            command=command,
            name_is_textual=name_is_textual,
        )
    elif string.startswith('"'):
        assert string.endswith('"')
        stripped_string = string.strip('"')
        command = rf"\baca-effort-{stripped_string}"
        indicator = abjad.Dynamic(f"{string}", command=command)
    elif string in known_shapes:
        indicator = abjad.StartHairpin(string)
        if string.endswith(">o") and not forbid_al_niente_to_bar_line:
            indicator = abjad.bundle(indicator, r"- \tweak to-barline ##t")
    elif string == "!":
        indicator = abjad.StopHairpin()
    elif string == "m":
        indicator = abjad.Dynamic("m", command=r"\baca-m")
    else:
        failed = False
        try:
            indicator = abjad.Dynamic(string)
        except Exception:
            failed = True
        if failed:
            raise Exception(f"the string {string!r} initializes no known dynamic.")
    prototype = (abjad.Dynamic, abjad.StartHairpin, abjad.StopHairpin, abjad.Bundle)
    assert isinstance(indicator, prototype), repr(indicator)
    return indicator


def metronome_mark(skip, indicator, manifests, *, deactivate=False, tag=None):
    prototype = (
        abjad.MetricModulation,
        abjad.MetronomeMark,
        _indicators.Accelerando,
        _indicators.Ritardando,
    )
    assert isinstance(indicator, prototype), repr(indicator)
    reapplied = _treat.remove_reapplied_wrappers(skip, indicator)
    wrapper = abjad.attach(
        indicator,
        skip,
        deactivate=deactivate,
        tag=tag,
        wrapper=True,
    )
    if indicator == reapplied:
        _treat.treat_persistent_wrapper(manifests, wrapper, "redundant")


def natural_clusters(
    widths: typing.Sequence[int],
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    start_pitch: int | str | abjad.NamedPitch | None = None,
) -> ClusterCommand:
    if start_pitch is not None:
        start_pitch = abjad.NamedPitch(start_pitch)
    return ClusterCommand(
        hide_flat_markup=True,
        selector=selector,
        start_pitch=start_pitch,
        widths=widths,
    )


def pitch(
    pitch,
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    allow_hidden: bool = False,
    allow_out_of_range: bool = False,
    allow_repitch: bool = False,
    mock: bool = False,
    do_not_transpose: bool = False,
    persist: str = "",
) -> PitchCommand:
    r"""
    Makes pitch command.

    ..  container:: example

        REGRESSION. Preserves duration multipliers when leaves cast from one type to
        another (note to chord in this example):

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> stack = rmakers.stack(
        ...     rmakers.note(),
        ...     rmakers.written_duration(1),
        ... )
        >>> music = stack(commands.get())
        >>> score["Music"].extend(music)

        >>> commands(
        ...     "Music",
        ...     baca.pitch("<C4 D4 E4>"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        <c' d' e'>1 * 1/2
                        %@% ^ \baca-duration-multiplier-markup #"1" #"2"
                        <c' d' e'>1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        <c' d' e'>1 * 1/2
                        %@% ^ \baca-duration-multiplier-markup #"1" #"2"
                        <c' d' e'>1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    }
                >>
            }

    """
    if isinstance(pitch, list | tuple) and len(pitch) == 1:
        raise Exception(f"one-note chord {pitch!r}?")
    if allow_out_of_range not in (None, True, False):
        raise Exception(
            f"allow_out_of_range must be boolean (not {allow_out_of_range!r})."
        )
    if do_not_transpose not in (None, True, False):
        raise Exception(f"do_not_transpose must be boolean (not {do_not_transpose!r}).")
    if persist is not None and not isinstance(persist, str):
        raise Exception(f"persist name must be string (not {persist!r}).")
    return PitchCommand(
        allow_hidden=allow_hidden,
        allow_out_of_range=allow_out_of_range,
        allow_repeats=True,
        allow_repitch=allow_repitch,
        cyclic=True,
        do_not_transpose=do_not_transpose,
        mock=mock,
        persist=persist,
        pitches=[pitch],
        selector=selector,
    )


def pitch_function(
    argument,
    pitch,
    *,
    allow_hidden: bool = False,
    allow_out_of_range: bool = False,
    allow_repitch: bool = False,
    mock: bool = False,
    do_not_transpose: bool = False,
    persist: str = None,
) -> bool:
    assert isinstance(pitch, str | list | tuple | abjad.Pitch), repr(pitch)
    if isinstance(pitch, list | tuple) and len(pitch) == 1:
        raise Exception(f"one-note chord {pitch!r}?")
    assert isinstance(allow_out_of_range, bool), repr(allow_out_of_range)
    assert isinstance(do_not_transpose, bool), repr(do_not_transpose)
    if persist is not None:
        assert isinstance(persist, str), repr(persist)
    cyclic = True
    result = _do_pitch_command(
        argument,
        cyclic,
        [pitch],
        allow_hidden=allow_hidden,
        allow_repeats=True,
        allow_repitch=allow_repitch,
        do_not_transpose=do_not_transpose,
        mock=mock,
    )
    pitches_consumed, mutated_score = result
    return mutated_score


_pitch_command_factory = pitch


def pitches(
    pitches,
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    allow_hidden: bool = False,
    allow_octaves: bool = False,
    allow_repeats: bool = False,
    allow_repitch: bool = False,
    mock: bool = False,
    do_not_transpose: bool = False,
    exact: bool = False,
    ignore_incomplete: bool = False,
    persist: str = "",
) -> PitchCommand:
    if do_not_transpose not in (None, True, False):
        raise Exception(f"do_not_transpose must be boolean (not {do_not_transpose!r}).")
    if bool(exact):
        cyclic = False
    else:
        cyclic = True
    if ignore_incomplete not in (None, True, False):
        raise Exception(
            f"ignore_incomplete must be boolean (not {ignore_incomplete!r})."
        )
    if ignore_incomplete is True and not persist:
        raise Exception("ignore_incomplete is ignored when persist is not set.")
    if persist is not None and not isinstance(persist, str):
        raise Exception(f"persist name must be string (not {persist!r}).")
    return PitchCommand(
        allow_hidden=allow_hidden,
        allow_octaves=allow_octaves,
        allow_repeats=allow_repeats,
        allow_repitch=allow_repitch,
        cyclic=cyclic,
        do_not_transpose=do_not_transpose,
        ignore_incomplete=ignore_incomplete,
        mock=mock,
        persist=persist,
        pitches=pitches,
        selector=selector,
    )


_pitches_command_factory = pitches


def pitches_function(
    argument,
    pitches,
    *,
    allow_hidden: bool = False,
    allow_octaves: bool = False,
    allow_repeats: bool = False,
    allow_repitch: bool = False,
    mock: bool = False,
    do_not_transpose: bool = False,
    exact: bool = False,
    ignore_incomplete: bool = False,
    persist: str = None,
) -> bool:
    if do_not_transpose not in (None, True, False):
        raise Exception(f"do_not_transpose must be boolean (not {do_not_transpose!r}).")
    if bool(exact):
        cyclic = False
    else:
        cyclic = True
    if ignore_incomplete not in (None, True, False):
        raise Exception(
            f"ignore_incomplete must be boolean (not {ignore_incomplete!r})."
        )
    if ignore_incomplete is True and not persist:
        raise Exception("ignore_incomplete is ignored when persist is not set.")
    if persist is not None and not isinstance(persist, str):
        raise Exception(f"persist name must be string (not {persist!r}).")
    result = _do_pitch_command(
        argument,
        cyclic,
        pitches,
        allow_hidden=allow_hidden,
        allow_octaves=allow_octaves,
        allow_repeats=allow_repeats,
        allow_repitch=allow_repitch,
        do_not_transpose=do_not_transpose,
        mock=mock,
    )
    pitches_consumed, mutated_score = result
    return mutated_score


def register(
    start: int,
    stop: int = None,
    *,
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> RegisterCommand | RegisterInterpolationCommand:
    r"""
    Octave-transposes ``selector`` output.

    ..  container:: example

        Octave-transposes all PLTs to the octave rooted at -6:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.register(-6),
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
                        d'16
                        ]
                        bf4
                        ~
                        bf16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs16
                        [
                        e'16
                        ]
                        ef'4
                        ~
                        ef'16
                        r16
                        af16
                        [
                        g16
                        ]
                    }
                    \times 4/5
                    {
                        a16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

        Octave-transposes PLTs in tuplet 1 to the octave rooted at -6:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.color(
        ...         lambda _: baca.select.tuplet(_, 1),
        ...         lone=True,
        ...     ),
        ...     baca.register(
        ...         -6,
        ...         selector=lambda _: baca.select.tuplet(_, 1),
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
                        \abjad-color-music #'green
                        fs16
                        [
                        \abjad-color-music #'green
                        e'16
                        ]
                        \abjad-color-music #'green
                        ef'4
                        ~
                        \abjad-color-music #'green
                        ef'16
                        \abjad-color-music #'green
                        r16
                        \abjad-color-music #'green
                        af16
                        [
                        \abjad-color-music #'green
                        g16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Octave-transposes all PLTs to an octave interpolated from -6 to 18:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.register(-6, 18),
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
                        fs'16
                        [
                        e'16
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
                        a''16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

        Octave-transposes PLTs in tuplet 1 to an octave interpolated from -6 to 18:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.color(
        ...         lambda _: baca.select.tuplet(_, 1),
        ...         lone=True,
        ...     ),
        ...     baca.register(
        ...         -6, 18,
        ...         selector=lambda _: baca.select.tuplet(_, 1),
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
                        \abjad-color-music #'green
                        fs16
                        [
                        \abjad-color-music #'green
                        e'16
                        ]
                        \abjad-color-music #'green
                        ef'4
                        ~
                        \abjad-color-music #'green
                        ef'16
                        \abjad-color-music #'green
                        r16
                        \abjad-color-music #'green
                        af'16
                        [
                        \abjad-color-music #'green
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    if stop is None:
        start_pitch = abjad.NumberedPitch(start)
        return RegisterCommand(
            registration=_pcollections.Registration([("[A0, C8]", start_pitch)]),
            selector=selector,
        )
    if start is not None:
        start_pitch = abjad.NumberedPitch(start)
    if stop is not None:
        stop_pitch = abjad.NumberedPitch(stop)
    return RegisterInterpolationCommand(
        selector=selector, start_pitch=start_pitch, stop_pitch=stop_pitch
    )


def soprano_to_octave(
    n: int,
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
) -> RegisterToOctaveCommand:
    r"""
    Octave-transposes music.

    ..  container:: example

        Octave-transposes music such that the highest note in the collection of all PLTs
        appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.color(
        ...         lambda _: baca.select.plts(_),
        ...         lone=True,
        ...     ),
        ...     baca.soprano_to_octave(3),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        \time 5/4
                        <c,, d,, bf,,>8
                        [
                        ~
                        \abjad-color-music #'green
                        <c,, d,, bf,,>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        f,8
                        [
                        ~
                        \abjad-color-music #'green
                        f,32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <ef, e, fs>8
                        [
                        ~
                        \abjad-color-music #'green
                        <ef, e, fs>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        <g,, af,>8
                        [
                        ~
                        \abjad-color-music #'green
                        <g,, af,>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'green
                        a,,8
                        [
                        ~
                        \abjad-color-music #'green
                        a,,32
                        ]
                        r16.
                    }
                }
            >>

    ..  container:: example

        Octave-transposes music that such that the highest note in each pitched logical
        tie appears in octave 3:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.soprano_to_octave(3),
        ...         map=lambda _: baca.select.plts(_),
        ...     ),
        ...     baca.color(lambda _: baca.select.plts(_)),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        \time 5/4
                        <c d bf>8
                        [
                        ~
                        \abjad-color-music #'red
                        <c d bf>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        f8
                        [
                        ~
                        \abjad-color-music #'blue
                        f32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        <ef, e, fs>8
                        [
                        ~
                        \abjad-color-music #'red
                        <ef, e, fs>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'blue
                        <g, af>8
                        [
                        ~
                        \abjad-color-music #'blue
                        <g, af>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \abjad-color-music #'red
                        a8
                        [
                        ~
                        \abjad-color-music #'red
                        a32
                        ]
                        r16.
                    }
                }
            >>

    """
    return RegisterToOctaveCommand(anchor=abjad.UP, octave_number=n, selector=selector)


def staff_position(
    argument: int | list | abjad.StaffPosition,
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    allow_hidden: bool = False,
    allow_out_of_range: bool = False,
    allow_repitch: bool = False,
    mock: bool = False,
    set_chord_pitches_equal: bool = False,
) -> StaffPositionCommand:
    assert isinstance(argument, int | list | abjad.StaffPosition), repr(argument)
    if isinstance(argument, list):
        assert all(isinstance(_, int | abjad.StaffPosition) for _ in argument)
    return StaffPositionCommand(
        numbers=[argument],
        allow_hidden=allow_hidden,
        allow_out_of_range=allow_out_of_range,
        allow_repeats=True,
        allow_repitch=allow_repitch,
        mock=mock,
        selector=selector,
        set_chord_pitches_equal=set_chord_pitches_equal,
    )


def staff_position_function(
    argument,
    numbers: int | list | abjad.StaffPosition,
    *,
    allow_hidden: bool = False,
    allow_out_of_range: bool = False,
    allow_repitch: bool = False,
    mock: bool = False,
    set_chord_pitches_equal: bool = False,
) -> bool:
    assert isinstance(numbers, int | list | abjad.StaffPosition), repr(numbers)
    if isinstance(numbers, list):
        assert all(isinstance(_, int | abjad.StaffPosition) for _ in numbers)
    mutated_score = _staff_position_function(
        argument,
        [numbers],
        allow_hidden=allow_hidden,
        allow_out_of_range=allow_out_of_range,
        allow_repeats=True,
        allow_repitch=allow_repitch,
        mock=mock,
        set_chord_pitches_equal=set_chord_pitches_equal,
    )
    return mutated_score


_staff_position_command = staff_position


def staff_positions(
    numbers,
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    allow_hidden: bool = False,
    allow_out_of_range: bool = False,
    allow_repeats: bool = False,
    mock: bool = False,
    exact: bool = False,
) -> StaffPositionCommand:
    if allow_repeats is None and len(numbers) == 1:
        allow_repeats = True
    return StaffPositionCommand(
        numbers=numbers,
        allow_hidden=allow_hidden,
        allow_out_of_range=allow_out_of_range,
        allow_repeats=allow_repeats,
        exact=exact,
        mock=mock,
        selector=selector,
    )


def accent(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
):
    r"""
    Attaches accent.

    ..  container:: example

        Attaches accent to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.accent(),
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
                        - \accent
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation(">")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def _alternate_bow_strokes_preparation(*tweaks, downbow_first, full):
    indicators: list[abjad.Articulation | abjad.Bundle]
    if downbow_first:
        if full:
            strings = ["baca-full-downbow", "baca-full-upbow"]
        else:
            strings = ["downbow", "upbow"]
    else:
        if full:
            strings = ["baca-full-upbow", "baca-full-downbow"]
        else:
            strings = ["upbow", "downbow"]
    indicators = [abjad.Articulation(_) for _ in strings]
    indicators = [_tweaks.bundle_tweaks(_, tweaks) for _ in indicators]
    return indicators


def alternate_bow_strokes(
    selector=lambda _: _select.pheads(_, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
    downbow_first: bool = True,
    full: bool = False,
) -> IndicatorCommand:
    r"""
    Attaches alternate bow strokes.

    ..  container:: example

        Attaches alternate bow strokes to pitched heads (down-bow first):

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.alternate_bow_strokes(downbow_first=True),
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
                        - \downbow
                        [
                        d'16
                        - \upbow
                        ]
                        bf'4
                        - \downbow
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        - \upbow
                        [
                        e''16
                        - \downbow
                        ]
                        ef''4
                        - \upbow
                        ~
                        ef''16
                        r16
                        af''16
                        - \downbow
                        [
                        g''16
                        - \upbow
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        - \downbow
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Attaches alternate bow strokes to pitched heads (up-bow first):

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.alternate_bow_strokes(downbow_first=False),
        ...     baca.tuplet_bracket_staff_padding(6),
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
                        \override TupletBracket.staff-padding = 6
                        \time 11/8
                        r8
                        c'16
                        - \upbow
                        [
                        d'16
                        - \downbow
                        ]
                        bf'4
                        - \upbow
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        - \downbow
                        [
                        e''16
                        - \upbow
                        ]
                        ef''4
                        - \downbow
                        ~
                        ef''16
                        r16
                        af''16
                        - \upbow
                        [
                        g''16
                        - \downbow
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        - \upbow
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Attaches alternate full bow strokes to pitched heads:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.alternate_bow_strokes(full=True),
        ...     baca.tuplet_bracket_staff_padding(6),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(
        ...     selection, includes=["baca.ily"]
        ... )
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
                        \override TupletBracket.staff-padding = 6
                        \time 11/8
                        r8
                        c'16
                        - \baca-full-downbow
                        [
                        d'16
                        - \baca-full-upbow
                        ]
                        bf'4
                        - \baca-full-downbow
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        - \baca-full-upbow
                        [
                        e''16
                        - \baca-full-downbow
                        ]
                        ef''4
                        - \baca-full-upbow
                        ~
                        ef''16
                        r16
                        af''16
                        - \baca-full-downbow
                        [
                        g''16
                        - \baca-full-upbow
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        - \baca-full-downbow
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    indicators = _alternate_bow_strokes_preparation(
        *tweaks, downbow_first=downbow_first, full=full
    )
    return IndicatorCommand(
        indicators=indicators,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def alternate_bow_strokes_function(
    argument,
    *tweaks: abjad.Tweak,
    downbow_first: bool = True,
    full: bool = False,
    tags: list[abjad.Tag] = None,
) -> None:
    pass
    # tag = _tags.function_name(_frame())
    tag = abjad.Tag("baca.alternate_bow_strokes()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    indicators = _alternate_bow_strokes_preparation(
        *tweaks, downbow_first=downbow_first, full=full
    )
    indicators = abjad.CyclicTuple(indicators)
    leaves = abjad.select.leaves(argument)
    for i, leaf in enumerate(leaves):
        indicator = indicators[i]
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def arpeggio(
    selector=lambda _: _select.chead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches arpeggio.

    ..  container:: example

        Attaches arpeggio to chord head 0:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.arpeggio(),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \time 5/4
                        <c' d' bf'>8
                        - \arpeggio
                        [
                        ~
                        <c' d' bf'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        f''8
                        [
                        ~
                        f''32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <ef'' e'' fs'''>8
                        [
                        ~
                        <ef'' e'' fs'''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <g' af''>8
                        [
                        ~
                        <g' af''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'8
                        [
                        ~
                        a'32
                        ]
                        r16.
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("arpeggio")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def articulation(
    articulation: str,
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    articulation_ = abjad.Articulation(articulation)
    return IndicatorCommand(
        indicators=[articulation_],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def articulations(
    articulations: list,
    selector=lambda _: _select.pheads(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=articulations,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def bar_line_command(
    abbreviation: str = "|",
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    site: str = "after",
) -> IndicatorCommand:
    indicator = abjad.BarLine(abbreviation, site=site)
    return IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def bar_line(
    skip,
    abbreviation: str = "|",
    *,
    deactivate: bool = False,
    site: str = "after",
):
    assert isinstance(abbreviation, str), repr(abbreviation)
    indicator = abjad.BarLine(abbreviation, site=site)
    abjad.attach(
        indicator,
        skip,
        deactivate=deactivate,
        tag=_tags.function_name(_frame()),
    )


def breathe(
    selector=lambda _: _select.pleaf(_, -1, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
) -> IndicatorCommand:
    indicator: abjad.LilyPondLiteral | abjad.Bundle
    # TODO: change to abjad.Articulation("breathe", site="after")?
    indicator = abjad.LilyPondLiteral(r"\breathe", site="after")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def breathe_function(
    leaf,
    *tweaks: abjad.Tweak,
    tags: list[abjad.Tag] = None,
) -> None:
    indicator: abjad.LilyPondLiteral | abjad.Bundle
    # TODO: change to abjad.Articulation("breathe", site="after")?
    indicator = abjad.LilyPondLiteral(r"\breathe", site="after")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    # tag = _tags.function_name(_frame())
    tag = abjad.Tag("baca.breathe()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    abjad.attach(
        indicator,
        leaf,
        tag=tag,
    )


def clef(
    clef: str = "treble",
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    redundant: bool = False,
) -> IndicatorCommand:
    r"""
    Attaches clef.

    ..  container:: example

        Attaches clef to leaf 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.clef("alto"),
        ...     baca.tuplet_bracket_staff_padding(7),
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
                        \override TupletBracket.staff-padding = 7
                        \clef "alto"
                        \time 11/8
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    indicator = abjad.Clef(clef)
    return IndicatorCommand(
        indicators=[indicator],
        redundant=redundant,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def clef_function(
    leaf: abjad.Leaf,
    clef: str,
) -> None:
    assert isinstance(leaf, abjad.Leaf), repr(leaf)
    assert isinstance(clef, str), repr(clef)
    indicator = abjad.Clef(clef)
    _attach_persistent_indicator(
        leaf,
        [indicator],
        manifests={},
        tag=abjad.Tag("baca.clef()"),
    )


def damp(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
) -> IndicatorCommand:
    indicator: abjad.Articulation | abjad.Bundle
    indicator = abjad.Articulation("baca-damp")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def double_flageolet(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.Articulation("baca-double-flageolet")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def double_staccato(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches double-staccato.

    ..  container:: example

        Attaches double-staccato to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.double_staccato(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(
        ...     selection, includes=["baca.ily"]
        ... )
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
                        - \baca-staccati #2
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("baca-staccati #2")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def down_arpeggio(
    selector=lambda _: _select.chead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches down-arpeggio.

    ..  container:: example

        Attaches down-arpeggio to chord head 0:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.down_arpeggio(),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \arpeggioArrowDown
                        \time 5/4
                        <c' d' bf'>8
                        \arpeggio
                        [
                        ~
                        <c' d' bf'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        f''8
                        [
                        ~
                        f''32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <ef'' e'' fs'''>8
                        [
                        ~
                        <ef'' e'' fs'''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <g' af''>8
                        [
                        ~
                        <g' af''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'8
                        [
                        ~
                        a'32
                        ]
                        r16.
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Arpeggio(direction=abjad.DOWN)],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def down_bow(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
    full: bool = False,
) -> IndicatorCommand:
    r"""
    Attaches down-bow.

    ..  container:: example

        Attaches down-bow to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.down_bow(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(
        ...     selection, includes=["baca.ily"]
        ... )
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
                        - \downbow
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Attaches full down-bow to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.down_bow(full=True),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(
        ...     selection, includes=["baca.ily"]
        ... )
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
                        - \baca-full-downbow
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    indicator: abjad.Articulation | abjad.Bundle
    if full:
        indicator = abjad.Articulation("baca-full-downbow")
    else:
        indicator = abjad.Articulation("downbow")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def down_bow_function(
    leaf: abjad.Leaf,
    *tweaks: abjad.Tweak,
    full: bool = False,
    tags: list[abjad.Tag] = None,
) -> None:
    assert isinstance(leaf, abjad.Leaf), repr(leaf)
    indicator: abjad.Articulation | abjad.Bundle
    if full:
        indicator = abjad.Articulation("baca-full-downbow")
    else:
        indicator = abjad.Articulation("downbow")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    # tag = _tags.function_name(_frame())
    tag = abjad.Tag("baca.down_bow()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    abjad.attach(
        indicator,
        leaf,
        tag=tag,
    )


def espressivo(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
) -> IndicatorCommand:
    r"""
    Attaches espressivo.

    ..  container:: example

        Attaches espressivo to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.espressivo(),
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
                        - \espressivo
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    indicator: abjad.Articulation | abjad.Bundle
    indicator = abjad.Articulation("espressivo")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def espressivo_function(
    leaf,
    *tweaks: abjad.Tweak,
    tags: list[abjad.Tag] = None,
) -> None:
    indicator: abjad.Articulation | abjad.Bundle
    indicator = abjad.Articulation("espressivo")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    # tag = _tags.function_name(_frame())
    tag = abjad.Tag("baca.espressivo()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    abjad.attach(
        indicator,
        leaf,
        tag=tag,
    )


def fermata(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> IndicatorCommand:
    r"""
    Attaches fermata.

    ..  container:: example

        Attaches fermata to first leaf:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.fermata(),
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
                        - \fermata
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("fermata")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def flageolet(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches flageolet.

    ..  container:: example

        Attaches flageolet to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.flageolet(),
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
                        - \flageolet
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("flageolet")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def hide_black_note_heads(
    selector=lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches note-head stencil false to black note-heads.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_notes(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.hide_black_note_heads(),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'2
                        \baca-repeat-pitch-class-coloring
                        \once \override NoteHead.transparent = ##t
                        c'4.
                        \baca-repeat-pitch-class-coloring
                        c'2
                        \baca-repeat-pitch-class-coloring
                        \once \override NoteHead.transparent = ##t
                        c'4.
                    }
                >>
            }

    """
    string = r"\once \override NoteHead.transparent = ##t"
    literal = abjad.LilyPondLiteral(string)
    return IndicatorCommand(
        indicators=[literal],
        predicate=lambda _: _.written_duration < abjad.Duration(1, 2),
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def instrument_name(
    argument: str,
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    context: str = "Staff",
) -> IndicatorCommand:
    assert isinstance(argument, str), repr(argument)
    assert argument.startswith("\\"), repr(argument)
    instrument_name = abjad.InstrumentName(argument, context=context)
    command = IndicatorCommand(
        indicators=[instrument_name],
        selector=selector,
        tags=[_tags.function_name(_frame()), _tags.NOT_PARTS],
    )
    return command


def instrument_name_function(
    leaf: abjad.Leaf,
    argument: str,
    *,
    context: str = "Staff",
) -> None:
    assert isinstance(argument, str), repr(argument)
    assert argument.startswith("\\"), repr(argument)
    indicator = abjad.InstrumentName(argument, context=context)
    # tag = _tags.function_name(_frame())
    tag = abjad.Tag("baca.instrument_name()")
    tag = tag.append(_tags.NOT_PARTS)
    abjad.attach(
        indicator,
        leaf,
        tag=tag,
    )


def laissez_vibrer(
    selector=lambda _: _select.ptail(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches laissez vibrer.

    ..  container:: example

        Attaches laissez vibrer to PLT tail 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.laissez_vibrer(),
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
                        \laissezVibrer
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.LaissezVibrer()],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def literal(
    string: str | list[str],
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    site: str = "before",
) -> IndicatorCommand:
    literal = abjad.LilyPondLiteral(string, site=site)
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def literal_function(
    leaf: abjad.Leaf,
    string: str | list[str],
    *,
    site: str = "before",
    tags: list[abjad.Tag] = None,
) -> None:
    assert isinstance(leaf, abjad.Leaf), repr(leaf)
    indicator = abjad.LilyPondLiteral(string, site=site)
    # tag = _tags.function_name(_frame())
    tag = abjad.Tag("baca.literal()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    abjad.attach(
        indicator,
        leaf,
        tag=tag,
    )


def long_fermata(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> IndicatorCommand:
    r"""
    Attaches long fermata.

    ..  container:: example

        Attaches long fermata to first leaf:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.long_fermata(),
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
                        - \longfermata
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("longfermata")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def marcato(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches marcato.

    ..  container:: example

        Attaches marcato to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.marcato(),
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
                        - \marcato
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("marcato")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def short_instrument_name(
    argument: str,
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    alert: IndicatorCommand = None,
    context: str = "Staff",
) -> IndicatorCommand | _command.Suite:
    r"""
    Attaches short instrument name.

    ..  container:: example

        >>> short_instrument_names = {}
        >>> markup = abjad.Markup(r"\markup Fl.")
        >>> short_instrument_names["Fl."] = abjad.ShortInstrumentName(markup)
        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     short_instrument_names=short_instrument_names,
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_notes(commands.get(), repeat_ties=True)
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.short_instrument_name(r"\markup Fl."),
        ...     baca.pitches("E4 F4"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     first_section=True,
        ...     short_instrument_names=commands.short_instrument_names,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \set Staff.shortInstrumentName = \markup Fl.
                        e'2
                        f'4.
                        e'2
                        f'4.
                    }
                >>
            }

    """
    if isinstance(argument, str):
        markup = abjad.Markup(argument)
        short_instrument_name = abjad.ShortInstrumentName(markup, context=context)
    elif isinstance(argument, abjad.Markup):
        markup = abjad.Markup(argument)
        short_instrument_name = abjad.ShortInstrumentName(markup, context=context)
    elif isinstance(argument, abjad.ShortInstrumentName):
        short_instrument_name = dataclasses.replace(argument, context=context)
    else:
        raise TypeError(argument)
    assert isinstance(short_instrument_name, abjad.ShortInstrumentName)
    command = IndicatorCommand(
        indicators=[short_instrument_name],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )
    if bool(alert):
        assert isinstance(alert, IndicatorCommand), repr(alert)
        return _command.suite(command, alert)
    else:
        return command


def short_instrument_name_function(
    leaf,
    short_instrument_name: abjad.ShortInstrumentName,
    *,
    context: str = "Staff",
) -> None:
    assert isinstance(short_instrument_name, abjad.ShortInstrumentName), repr(
        short_instrument_name
    )
    # tag = _tags.function_name(_frame())
    tag = abjad.Tag("baca.short_instrument_name()")
    tag = tag.append(_tags.NOT_PARTS)
    abjad.attach(
        short_instrument_name,
        leaf,
        tag=tag,
    )


def mark(
    argument: str,
    selector=lambda _: abjad.select.leaf(_, 0),
    *tweaks: abjad.Tweak,
) -> IndicatorCommand:
    assert isinstance(argument, abjad.Markup | str), repr(argument)
    rehearsal_mark = abjad.RehearsalMark(markup=argument)
    rehearsal_mark = _tweaks.bundle_tweaks(rehearsal_mark, tweaks)
    return IndicatorCommand(
        indicators=[rehearsal_mark],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def parenthesize(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches LilyPond ``\parenthesize`` command.

    ..  container:: example

        Attaches parenthesize command to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.parenthesize(),
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
                        \parenthesize
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\parenthesize")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def quadruple_staccato(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.Articulation("baca-staccati #4")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def rehearsal_mark(
    argument: int | str,
    selector=lambda _: abjad.select.leaf(_, 0),
    *tweaks: abjad.Tweak,
    font_size: int = 10,
) -> IndicatorCommand:
    assert isinstance(argument, str), repr(argument)
    assert isinstance(font_size, int | float), repr(font_size)
    string = rf'\baca-rehearsal-mark-markup "{argument}" #{font_size}'
    indicator: abjad.Markup | abjad.Bundle
    indicator = abjad.Markup(string)
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return IndicatorCommand(
        direction=abjad.CENTER,
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def rehearsal_mark_function(
    leaf: abjad.Leaf,
    argument: int | str,
    *tweaks: abjad.Tweak,
    font_size: int = 10,
    tags: list[abjad.Tag] = None,
) -> None:
    assert isinstance(leaf, abjad.Leaf), repr(leaf)
    assert isinstance(argument, str), repr(argument)
    assert isinstance(font_size, int | float), repr(font_size)
    string = rf'\baca-rehearsal-mark-markup "{argument}" #{font_size}'
    indicator: abjad.Markup | abjad.Bundle
    indicator = abjad.Markup(string)
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    tag = _tags.function_name(_frame())
    for tag_ in tags or []:
        tag = tag.append(tag_)
    abjad.attach(
        indicator,
        leaf,
        direction=abjad.CENTER,
        tag=tag,
    )


def repeat_tie(selector, *, allow_rest: bool = False) -> IndicatorCommand:
    r"""
    Attaches repeat-tie.

    ..  container:: example

        Attaches repeat-tie to pitched head 1:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.chunk(
        ...         baca.pitch(
        ...             0,
        ...             selector=lambda _: baca.select.plt(_, 1),
        ...         ),
        ...         baca.repeat_tie(
        ...             lambda _: baca.select.phead(_, 1),
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
                        c'16
                        [
                        c'16
                        ]
                        \repeatTie
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    if allow_rest is not None:
        allow_rest = bool(allow_rest)
    return IndicatorCommand(
        do_not_test=allow_rest,
        indicators=[abjad.RepeatTie()],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def repeat_tie_function(leaf: abjad.Leaf) -> None:
    assert isinstance(leaf, abjad.Leaf), repr(leaf)
    indicator = abjad.RepeatTie()
    abjad.attach(
        indicator,
        leaf,
        # tag=_tags.function_name(_frame())
        tag=abjad.Tag("baca.repeat_tie()"),
    )


def short_fermata(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> IndicatorCommand:
    r"""
    Attaches short fermata.

    ..  container:: example

        Attaches short fermata to first leaf:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.short_fermata(),
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
                        - \shortfermata
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("shortfermata")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def snap_pizzicato(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.Articulation("snappizzicato")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def staccatissimo(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches staccatissimo.

    ..  container:: example

        Attaches staccatissimo to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.staccatissimo(),
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
                        - \staccatissimo
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("staccatissimo")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def staccato(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches staccato.

    ..  container:: example

        Attaches staccato to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.staccato(),
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
                        - \staccato
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("staccato")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def staccato_function(
    argument,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    # tag = _tags.function_name(_frame())
    tag = abjad.Tag("baca.staccato()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("staccato")
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def staff_lines(n: int, selector=lambda _: abjad.select.leaf(_, 0)) -> _command.Suite:
    r"""
    Makes staff line command.

    ..  container:: example

        Single-line staff with percussion clef:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )

        >>> music = baca.make_notes(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.clef("percussion"),
        ...     baca.staff_lines(1),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \override Staff.BarLine.bar-extent = #'(0 . 0)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 1
                        \startStaff
                        \clef "percussion"
                        a4.
                        b4.
                        c'4.
                        d'4.
                        e'4.
                    }
                >>
            }


        Single-line staff with bass clef:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )

        >>> music = baca.make_notes(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.clef("bass"),
        ...     baca.staff_lines(1),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \override Staff.BarLine.bar-extent = #'(0 . 0)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 1
                        \startStaff
                        \clef "bass"
                        b,4.
                        c4.
                        d4.
                        e4.
                        f4.
                    }
                >>
            }

    ..  container:: example

        Two-line staff with percussion clef:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )

        >>> music = baca.make_notes(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.clef("percussion"),
        ...     baca.staff_lines(2),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \override Staff.BarLine.bar-extent = #'(-0.5 . 0.5)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 2
                        \startStaff
                        \clef "percussion"
                        a4.
                        b4.
                        c'4.
                        d'4.
                        e'4.
                    }
                >>
            }

        Two-line staff with bass clef; clef set before staff positions:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )

        >>> music = baca.make_notes(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.clef("bass"),
        ...     baca.staff_lines(2),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \override Staff.BarLine.bar-extent = #'(-0.5 . 0.5)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 2
                        \startStaff
                        \clef "bass"
                        b,4.
                        c4.
                        d4.
                        e4.
                        f4.
                    }
                >>
            }

        Two-line staff with bass clef; staff positions set before clef:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )

        >>> music = baca.make_notes(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.staff_lines(2),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ...     baca.clef("bass"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \override Staff.BarLine.bar-extent = #'(-0.5 . 0.5)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 2
                        \startStaff
                        \clef "bass"
                        g'4.
                        a'4.
                        b'4.
                        c''4.
                        d''4.
                    }
                >>
            }

    """
    command_1 = IndicatorCommand(
        indicators=[_indicators.BarExtent(n)],
        selector=selector,
        tags=[_tags.function_name(_frame(), n=1), _tags.NOT_PARTS],
    )
    command_2 = IndicatorCommand(
        indicators=[_indicators.StaffLines(n)],
        selector=selector,
        tags=[_tags.function_name(_frame(), n=2)],
    )
    return _command.suite(command_1, command_2)


def staff_lines_function(argument, n: int) -> None:
    assert isinstance(n, int), repr(n)
    bar_extent = _indicators.BarExtent(n)
    _attach_persistent_indicator(
        argument,
        [bar_extent],
        manifests={},
        tag=abjad.Tag("baca.staff_lines(1)").append(_tags.NOT_PARTS),
    )
    staff_lines = _indicators.StaffLines(n)
    _attach_persistent_indicator(
        argument,
        [staff_lines],
        manifests={},
        tag=abjad.Tag("baca.staff_lines(2)"),
    )


def stem_tremolo(
    selector=lambda _: _select.pleaf(_, 0, exclude=_enums.HIDDEN),
    *,
    tremolo_flags: int = 32,
) -> IndicatorCommand:
    r"""
    Attaches stem tremolo.

    ..  container:: example

        Attaches stem tremolo to pitched leaf 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.stem_tremolo(),
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
                        :32
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.StemTremolo(tremolo_flags=tremolo_flags)],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def stem_tremolo_function(
    leaf: abjad.Leaf,
    *,
    tremolo_flags: int = 32,
    tags: list[abjad.Tag] = None,
) -> None:
    indicator = abjad.StemTremolo(tremolo_flags=tremolo_flags)
    # tag = _tags.function_name(_frame())
    tag = abjad.Tag("baca.stem_tremolo()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    abjad.attach(
        indicator,
        leaf,
        tag=tag,
    )


def stop_on_string(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
    *,
    map=None,
) -> IndicatorCommand:
    r"""
    Attaches stop-on-string.

    ..  container:: example

        Attaches stop-on-string to pitched head -1:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.stop_on_string(
        ...         selector=lambda _: baca.select.pleaf(_, -1),
        ...     ),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(
        ...     selection, includes=["baca.ily"]
        ... )
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
                        - \baca-stop-on-string
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    articulation = abjad.Articulation("baca-stop-on-string")
    return IndicatorCommand(
        indicators=[articulation],
        map=map,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def stop_trill(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> IndicatorCommand:
    r"""
    Attaches stop trill to closing-slot.

    The closing format slot is important because LilyPond fails to compile when
    ``\stopTrillSpan`` appears after ``\set instrumentName`` commands (and probably other
    ``\set`` commands). Setting format slot to closing here positions ``\stopTrillSpan``
    after the leaf in question (which is required) and also draws ``\stopTrillSpan``
    closer to the leaf in question, prior to ``\set instrumentName`` and other commands
    positioned in the after slot.

    Eventually it will probably be necessary to model ``\stopTrillSpan`` with a dedicated
    format slot.
    """
    return literal(r"\stopTrillSpan", site="closing", selector=selector)


def stopped(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches stopped +-sign.

    ..  container:: example

        Attaches stopped +-sign to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.stopped(),
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
                        - \stopped
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("stopped")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def tie(selector) -> IndicatorCommand:
    r"""
    Attaches tie.

    ..  container:: example

        Attaches tie to pitched tail 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.chunk(
        ...         baca.pitch(
        ...             2,
        ...             selector=lambda _: baca.select.plt(_, 0),
        ...         ),
        ...         baca.tie(lambda _: baca.select.ptail(_, 0)),
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
                        d'16
                        [
                        ~
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Tie()],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def tie_function(leaf: abjad.Leaf) -> None:
    assert isinstance(leaf, abjad.Leaf), repr(leaf)
    indicator = abjad.Tie()
    abjad.attach(
        indicator,
        leaf,
        # tag=_tags.function_name(_frame())
        tag=abjad.Tag("baca.tie()"),
    )


def tenuto(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches tenuto.

    ..  container:: example

        Attaches tenuto to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tenuto(),
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
                        - \tenuto
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("tenuto")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def triple_staccato(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.Articulation("baca-staccati #3")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def up_arpeggio(
    selector=lambda _: _select.chead(_, 0, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches up-arpeggio.

    ..  container:: example

        Attaches up-arpeggios to chord head 0:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.up_arpeggio(),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

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
                    \scaleDurations #'(1 . 1)
                    {
                        \arpeggioArrowUp
                        \time 5/4
                        <c' d' bf'>8
                        \arpeggio
                        [
                        ~
                        <c' d' bf'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        f''8
                        [
                        ~
                        f''32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <ef'' e'' fs'''>8
                        [
                        ~
                        <ef'' e'' fs'''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <g' af''>8
                        [
                        ~
                        <g' af''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'8
                        [
                        ~
                        a'32
                        ]
                        r16.
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Arpeggio(direction=abjad.UP)],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def up_bow(
    selector=lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
    full: bool = False,
) -> IndicatorCommand:
    r"""
    Attaches up-bow.

    ..  container:: example

        Attaches up-bow to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ...     baca.up_bow(),
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
                        - \upbow
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    indicator: abjad.Articulation | abjad.Bundle
    if full:
        indicator = abjad.Articulation("baca-full-upbow")
    else:
        indicator = abjad.Articulation("upbow")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def very_long_fermata(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> IndicatorCommand:
    r"""
    Attaches very long fermata.

    ..  container:: example

        Attaches very long fermata to first leaf:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.very_long_fermata(),
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
                        - \verylongfermata
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
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation("verylongfermata")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def allow_octaves(*, selector=lambda _: _select.leaves(_)) -> IndicatorCommand:
    """
    Attaches ALLOW_OCTAVE constant.
    """
    return IndicatorCommand(indicators=[_enums.ALLOW_OCTAVE], selector=selector)


def assign_part(
    part_assignment: _parts.PartAssignment,
    *,
    selector=lambda _: _select.leaves(_),
) -> PartAssignmentCommand:
    r"""
    Inserts ``selector`` output in container and sets part assignment.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_notes(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.assign_part(baca.parts.PartAssignment("Music")),
        ...     baca.pitch("E4"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(score)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            <<
                \context Voice = "Skips"
                {
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    {   %*% PartAssignment('Music')
                        e'2
                        e'4.
                        e'2
                        e'4.
                    }   %*% PartAssignment('Music')
                }
            >>
        }

    ..  container:: example exception

        Raises exception when voice does not allow part assignment:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> part_assignment = baca.parts.PartAssignment("Flute")

        >>> music = baca.make_notes(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.assign_part(baca.parts.PartAssignment("Flute.Music")),
        ...     baca.pitches("E4 F4"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        Traceback (most recent call last):
            ...
        Exception: Music does not allow Flute.Music part assignment:
          PartAssignment(name='Flute.Music', token=None)

    """
    assert isinstance(part_assignment, _parts.PartAssignment), repr(part_assignment)
    return PartAssignmentCommand(part_assignment=part_assignment, selector=selector)


def bcps(
    bcps,
    *tweaks: _typings.IndexedTweak,
    bow_change_tweaks: typing.Sequence[_typings.IndexedTweak] = (),
    final_spanner: bool = False,
    helper: typing.Callable = lambda x, y: x,
    selector=lambda _: _select.leaves(_),
) -> BCPCommand:
    r"""
    Makes bow contact point command.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 16)),
        ... )

        >>> music = baca.make_even_divisions(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.bcps(
        ...         [(1, 5), (3, 5), (2, 5), (4, 5), (5, 5)],
        ...     ),
        ...     baca.pitches("E4 F4"),
        ...     baca.script_staff_padding(5.5),
        ...     baca.text_spanner_staff_padding(2.5),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #16
                        \time 4/8
                        s1 * 4/8
                        \baca-new-spacing-section #1 #16
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #16
                        \time 4/8
                        s1 * 4/8
                        \baca-new-spacing-section #1 #16
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \override Script.staff-padding = 5.5
                        \override TextSpanner.staff-padding = 2.5
                        e'8
                        - \downbow
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #3 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        \bacaStartTextSpanBCP
                        f'8
                        \bacaStopTextSpanBCP
                        ]
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #4 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #5 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        ]
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #3 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        \bacaStartTextSpanBCP
                        e'8
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #4 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #5 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        ]
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #1 #5
                        \bacaStartTextSpanBCP
                        f'8
                        - \upbow
                        \bacaStopTextSpanBCP
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #3 #5
                        \bacaStartTextSpanBCP
                        e'8
                        - \downbow
                        \bacaStopTextSpanBCP
                        - \abjad-solid-line-with-arrow
                        - \baca-bcp-spanner-left-text #2 #5
                        - \baca-bcp-spanner-right-text #4 #5
                        \bacaStartTextSpanBCP
                        f'8
                        \bacaStopTextSpanBCP
                        ]
                        \revert Script.staff-padding
                        \revert TextSpanner.staff-padding
                    }
                >>
            }

    """
    if final_spanner is not None:
        final_spanner = bool(final_spanner)
    return BCPCommand(
        bcps=bcps,
        bow_change_tweaks=tuple(bow_change_tweaks),
        final_spanner=final_spanner,
        helper=helper,
        selector=selector,
        tags=[_tags.function_name(_frame())],
        tweaks=tweaks,
    )


def close_volta(skip, first_measure_number, site: str = "before"):
    assert isinstance(first_measure_number, int), repr(first_measure_number)
    assert isinstance(site, str), repr(site)
    after = site == "after"
    bar_line(skip, ":|.", site=site)
    tag = _tags.function_name(_frame())
    measure_number = abjad.get.measure_number(skip)
    measure_number += first_measure_number - 1
    if after is True:
        measure_number += 1
    measure_number_tag = abjad.Tag(f"MEASURE_{measure_number}")
    # ONLY_MOL instead of NOT_MOL
    _overrides.bar_line_x_extent(
        [skip],
        (0, 1.5),
        after=after,
        tags=[tag, measure_number_tag, _tags.ONLY_MOL],
    )


def color(
    selector=lambda _: _select.leaves(_),
    lone=False,
) -> ColorCommand:
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
                        \abjad-color-music #'red
                        \time 11/8
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
                    \times 9/10
                    {
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
                    \times 4/5
                    {
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

        >>> def color_selector(argument):
        ...     result = abjad.select.tuplet(argument, 1)
        ...     result = abjad.select.leaves(result)
        ...     return result
        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.color(color_selector),
        ...     rmakers.unbeam(),
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
                        d'16
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
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
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return ColorCommand(selector=selector, lone=lone)


def container(
    identifier: str = None,
    *,
    selector=lambda _: _select.leaves(_),
) -> ContainerCommand:
    r"""
    Makes container with ``identifier`` and extends container with ``selector`` output.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_notes(commands.get(), repeat_ties=True)
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.container(
        ...         "ViolinI",
        ...         selector=lambda _: baca.select.leaves(_)[:2],
        ...     ),
        ...     baca.container(
        ...         "ViolinII",
        ...         selector=lambda _: baca.select.leaves(_)[2:],
        ...     ),
        ...     baca.pitches("E4 F4"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            <<
                \context Voice = "Skips"
                {
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    {   %*% ViolinI
                        e'2
                        f'4.
                    }   %*% ViolinI
                    {   %*% ViolinII
                        e'2
                        f'4.
                    }   %*% ViolinII
                }
            >>
        }

    """
    if identifier is not None:
        if not isinstance(identifier, str):
            raise Exception(f"identifier must be string (not {identifier!r}).")
    return ContainerCommand(identifier=identifier, selector=selector)


def cross_staff(*, selector=lambda _: _select.phead(_, 0)) -> IndicatorCommand:
    r"""
    Attaches cross-staff command.

    ..  container:: example

        Attaches cross-staff command to last two pitched leaves:

        >>> score = baca.docs.make_empty_score(1, 1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 4)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = abjad.Container("e'4 f' g' a'")[:]
        >>> score["Music.1"].extend(music)

        >>> music = abjad.Container("c'4 d' e' f'")[:]
        >>> score["Music.2"].extend(music)

        >>> commands(
        ...     ("Music.2", 1),
        ...     baca.cross_staff(
        ...         selector=lambda _: baca.select.pleaves(_)[-2:],
        ...     ),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context StaffGroup = "StaffGroup"
                <<
                    \context Staff = "Staff.1"
                    <<
                        \context Voice = "Skips"
                        {
                            \time 4/4
                            s1 * 4/4
                        }
                        \context Voice = "Music.1"
                        {
                            e'4
                            f'4
                            g'4
                            a'4
                        }
                    >>
                    \context Staff = "Staff.2"
                    {
                        \context Voice = "Music.2"
                        {
                            c'4
                            d'4
                            \crossStaff
                            e'4
                            \crossStaff
                            f'4
                        }
                    }
                >>
            }

    """
    return IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\crossStaff")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def double_volta(skip, first_measure_number):
    assert isinstance(first_measure_number, int), repr(first_measure_number)
    bar_line(skip, ":.|.:", site="before")
    tag = _tags.function_name(_frame())
    measure_number = abjad.get.measure_number(skip)
    measure_number += first_measure_number - 1
    measure_number_tag = abjad.Tag(f"MEASURE_{measure_number}")
    _overrides.bar_line_x_extent(
        [skip],
        (0, 3),
        tags=[tag, _tags.NOT_MOL, measure_number_tag],
    )
    _overrides.bar_line_x_extent(
        [skip],
        (0, 4),
        tags=[tag, _tags.ONLY_MOL, measure_number_tag],
    )


def dynamic_down(*, selector=lambda _: abjad.select.leaf(_, 0)) -> IndicatorCommand:
    r"""
    Attaches dynamic-down command.

    ..  container:: example

        Attaches dynamic-down command to leaf 0:

        >>> def forte_selector(argument):
        ...     result = abjad.select.tuplet(argument, 1)
        ...     result = baca.select.phead(result, 0)
        ...     return result
        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.dynamic("p"),
        ...     baca.dynamic("f", selector=forte_selector),
        ...     baca.dynamic_down(),
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
                        \dynamicDown
                        \time 11/8
                        r8
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
                    \times 9/10
                    {
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
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\dynamicDown")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dynamic_up(*, selector=lambda _: abjad.select.leaf(_, 0)) -> IndicatorCommand:
    r"""
    Attaches dynamic-up command.

    ..  container:: example

        Attaches dynamic-up command to leaf 0:

        >>> def forte_selector(argument):
        ...     result = abjad.select.tuplet(argument, 1)
        ...     result = baca.select.phead(result, 0)
        ...     return result
        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.dynamic("p"),
        ...     baca.dynamic("f", selector=forte_selector),
        ...     baca.dynamic_up(),
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
                        \dynamicUp
                        \time 11/8
                        r8
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
                    \times 9/10
                    {
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
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\dynamicUp")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def edition(
    not_parts: str | abjad.Markup | IndicatorCommand,
    only_parts: str | abjad.Markup | IndicatorCommand,
) -> _command.Suite:
    """
    Makes not-parts / only-parts markup suite.
    """
    if isinstance(not_parts, str):
        not_parts = markup(rf"\markup {{ {not_parts} }}")
    elif isinstance(not_parts, abjad.Markup):
        not_parts = markup(not_parts)
    assert isinstance(not_parts, IndicatorCommand)
    not_parts_ = _command.not_parts(not_parts)
    if isinstance(only_parts, str):
        only_parts = markup(rf"\markup {{ {only_parts} }}")
    elif isinstance(only_parts, abjad.Markup):
        only_parts = markup(only_parts)
    assert isinstance(only_parts, IndicatorCommand)
    only_parts_ = _command.only_parts(only_parts)
    return _command.suite(not_parts_, only_parts_)


def finger_pressure_transition(
    *,
    selector=lambda _: _select.tleaves(_),
    right_broken: bool = False,
) -> GlissandoCommand:
    r"""
    Makes finger pressure transition glissando.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )

        >>> music = baca.make_notes(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.pitch("C5"),
        ...     baca.note_head_style_harmonic(selector=lambda _: abjad.select.note(_, 0)),
        ...     baca.note_head_style_harmonic(selector=lambda _: abjad.select.note(_, 2)),
        ...     baca.finger_pressure_transition(
        ...         selector=lambda _: abjad.select.notes(_)[:2],
        ...     ),
        ...     baca.finger_pressure_transition(
        ...         selector=lambda _: abjad.select.notes(_)[2:],
        ...     ),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 4/8
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 4/8
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \once \override NoteHead.style = #'harmonic
                        c''2
                        - \tweak arrow-length 2
                        - \tweak arrow-width 0.5
                        - \tweak bound-details.right.arrow ##t
                        - \tweak thickness 3
                        \glissando
                        c''4.
                        \once \override NoteHead.style = #'harmonic
                        c''2
                        - \tweak arrow-length 2
                        - \tweak arrow-width 0.5
                        - \tweak bound-details.right.arrow ##t
                        - \tweak thickness 3
                        \glissando
                        c''4.
                    }
                >>
            }

    """
    return GlissandoCommand(
        allow_repeats=True,
        right_broken=right_broken,
        selector=selector,
        tags=[_tags.function_name(_frame())],
        tweaks=(
            abjad.Tweak(r"- \tweak arrow-length 2"),
            abjad.Tweak(r"- \tweak arrow-width 0.5"),
            abjad.Tweak(r"- \tweak bound-details.right.arrow ##t"),
            abjad.Tweak(r"- \tweak thickness 3"),
        ),
    )


def flat_glissando(
    pitch: str
    | abjad.NamedPitch
    | abjad.StaffPosition
    | list[abjad.StaffPosition]
    | None = None,
    *tweaks,
    allow_hidden: bool = False,
    allow_repitch: bool = False,
    do_not_hide_middle_note_heads: bool = False,
    mock: bool = False,
    hide_middle_stems: bool = False,
    hide_stem_selector: typing.Callable = None,
    left_broken: bool = False,
    right_broken: bool = False,
    right_broken_show_next: bool = False,
    rleak: bool = False,
    selector=lambda _: _select.pleaves(_),
    stop_pitch: str | abjad.NamedPitch | abjad.StaffPosition | None = None,
) -> _command.Suite:
    prototype = (list, str, abjad.NamedPitch, abjad.StaffPosition)
    if pitch is not None:
        assert isinstance(pitch, prototype), repr(pitch)
    if stop_pitch is not None:
        assert type(pitch) is type(stop_pitch), repr((pitch, stop_pitch))
    if rleak is True:

        def _selector_rleak(argument):
            result = selector(argument)
            result = _select.rleak(result)
            return result

        new_selector = _selector_rleak
    else:
        new_selector = selector
    commands: list[_command.Command] = []
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
        return abjad.select.leaves(new_selector(argument))

    untie_command = untie(_leaves_of_selector)
    commands.append(untie_command)
    if pitch is not None and stop_pitch is None:
        # TODO: remove list test from or-clause?
        if isinstance(pitch, abjad.StaffPosition) or (
            isinstance(pitch, list) and isinstance(pitch[0], abjad.StaffPosition)
        ):
            staff_position_command_object = _staff_position_command(
                pitch,
                allow_hidden=allow_hidden,
                allow_repitch=allow_repitch,
                mock=mock,
                selector=new_selector,
            )
            commands.append(staff_position_command_object)
        else:
            pitch_command_object = _pitch_command_factory(
                pitch,
                allow_hidden=allow_hidden,
                allow_repitch=allow_repitch,
                mock=mock,
                selector=new_selector,
            )
            commands.append(pitch_command_object)
    elif pitch is not None and stop_pitch is not None:
        if isinstance(pitch, abjad.StaffPosition):
            assert isinstance(stop_pitch, abjad.StaffPosition)
            interpolation_command = _interpolate_staff_positions_function(
                pitch,
                stop_pitch,
                allow_hidden=allow_hidden,
                mock=mock,
                selector=new_selector,
            )
        else:
            assert isinstance(pitch, str | abjad.NamedPitch)
            assert isinstance(stop_pitch, str | abjad.NamedPitch)
            interpolation_command = _interpolate_pitches_function(
                pitch,
                stop_pitch,
                allow_hidden=allow_hidden,
                mock=mock,
                selector=new_selector,
            )
        commands.append(interpolation_command)
    return _command.suite(*commands)


def fractions(items):
    result = []
    for item in items:
        item_ = abjad.NonreducedFraction(item)
        result.append(item_)
    return result


def glissando(
    *tweaks: abjad.Tweak,
    allow_repeats: bool = False,
    allow_ties: bool = False,
    hide_middle_note_heads: bool = False,
    hide_middle_stems: bool = False,
    hide_stem_selector: typing.Callable = None,
    left_broken: bool = False,
    map=None,
    right_broken: bool = False,
    right_broken_show_next: bool = False,
    selector=lambda _: _select.tleaves(_),
    style: str = None,
    zero_padding: bool = False,
) -> GlissandoCommand:
    r"""
    Attaches glissando.

    ..  container:: example

        With section-commands:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ...     baca.glissando()
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(score)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        e'8
                        [
                        \glissando
                        d''8
                        \glissando
                        f'8
                        \glissando
                        e''8
                        ]
                        \glissando
                        g'8
                        [
                        \glissando
                        f''8
                        \glissando
                        e'8
                        ]
                        \glissando
                        d''8
                        [
                        \glissando
                        f'8
                        \glissando
                        e''8
                        \glissando
                        g'8
                        ]
                        \glissando
                        f''8
                        [
                        \glissando
                        e'8
                        \glissando
                        d''8
                        ]
                    }
                >>
            }

    ..  container:: example

        First and last PLTs:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ...     baca.glissando(selector=lambda _: baca.select.plts(_)[:2]),
        ...     baca.glissando(selector=lambda _: baca.select.plts(_)[-2:]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(score)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        e'8
                        [
                        \glissando
                        d''8
                        f'8
                        e''8
                        ]
                        g'8
                        [
                        f''8
                        e'8
                        ]
                        d''8
                        [
                        f'8
                        e''8
                        g'8
                        ]
                        f''8
                        [
                        e'8
                        \glissando
                        d''8
                        ]
                    }
                >>
            }

    ..  container:: example

        Works with tweaks:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ...     baca.glissando(
        ...         abjad.Tweak(r"- \tweak color #red"),
        ...     ),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(score)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        e'8
                        [
                        - \tweak color #red
                        \glissando
                        d''8
                        - \tweak color #red
                        \glissando
                        f'8
                        - \tweak color #red
                        \glissando
                        e''8
                        ]
                        - \tweak color #red
                        \glissando
                        g'8
                        [
                        - \tweak color #red
                        \glissando
                        f''8
                        - \tweak color #red
                        \glissando
                        e'8
                        ]
                        - \tweak color #red
                        \glissando
                        d''8
                        [
                        - \tweak color #red
                        \glissando
                        f'8
                        - \tweak color #red
                        \glissando
                        e''8
                        - \tweak color #red
                        \glissando
                        g'8
                        ]
                        - \tweak color #red
                        \glissando
                        f''8
                        [
                        - \tweak color #red
                        \glissando
                        e'8
                        - \tweak color #red
                        \glissando
                        d''8
                        ]
                    }
                >>
            }

    ..  container:: example

        Works with indexed tweaks:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_even_divisions(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ...     baca.glissando(
        ...         (abjad.Tweak(r"- \tweak color #red"), 0),
        ...         (abjad.Tweak(r"- \tweak color #red"), -1),
        ...     ),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(score)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        e'8
                        [
                        - \tweak color #red
                        \glissando
                        d''8
                        \glissando
                        f'8
                        \glissando
                        e''8
                        ]
                        \glissando
                        g'8
                        [
                        \glissando
                        f''8
                        \glissando
                        e'8
                        ]
                        \glissando
                        d''8
                        [
                        \glissando
                        f'8
                        \glissando
                        e''8
                        \glissando
                        g'8
                        ]
                        \glissando
                        f''8
                        [
                        \glissando
                        e'8
                        - \tweak color #red
                        \glissando
                        d''8
                        ]
                    }
                >>
            }

    """
    return GlissandoCommand(
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
        tags=[_tags.function_name(_frame())],
        tweaks=tweaks,
        zero_padding=zero_padding,
    )


def glissando_function(
    argument,
    *tweaks: abjad.Tweak,
    allow_repeats: bool = False,
    allow_ties: bool = False,
    hide_middle_note_heads: bool = False,
    hide_middle_stems: bool = False,
    hide_stem_selector: typing.Callable = None,
    left_broken: bool = False,
    # map=None,
    parenthesize_repeats: bool = False,
    right_broken: bool = False,
    right_broken_show_next: bool = False,
    # selector=lambda _: _select.tleaves(_),
    style: str = None,
    tags: list[abjad.Tag] = None,
    zero_padding: bool = False,
) -> None:
    leaves = abjad.select.leaves(argument)
    tweaks_ = []
    prototype = (abjad.Tweak, tuple)
    for tweak in tweaks or []:
        assert isinstance(tweak, prototype), repr(tweak)
        tweaks_.append(tweak)
    tag = abjad.Tag("baca.glissando()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    abjad.glissando(
        leaves,
        *tweaks_,
        allow_repeats=allow_repeats,
        allow_ties=allow_ties,
        hide_middle_note_heads=hide_middle_note_heads,
        hide_middle_stems=hide_middle_stems,
        hide_stem_selector=hide_stem_selector,
        left_broken=left_broken,
        parenthesize_repeats=parenthesize_repeats,
        right_broken=right_broken,
        right_broken_show_next=right_broken_show_next,
        tag=tag,
        zero_padding=zero_padding,
    )


def global_fermata(
    mmrest: abjad.MultimeasureRest,
    description: str = "fermata",
) -> None:
    description_to_command = {
        "short": "shortfermata",
        "fermata": "fermata",
        "long": "longfermata",
        "very_long": "verylongfermata",
    }
    fermatas = description_to_command.keys()
    if description not in fermatas:
        message = f"must be in {repr(', '.join(fermatas))}:\n"
        message += f"   {repr(description)}"
        raise Exception(message)
    if isinstance(description, str) and description != "fermata":
        command = description.replace("_", "-")
        command = f"{command}-fermata"
    else:
        command = "fermata"
    if description == "short":
        fermata_duration = 1
    elif description == "fermata":
        fermata_duration = 2
    elif description == "long":
        fermata_duration = 4
    elif description == "very_long":
        fermata_duration = 8
    else:
        raise Exception(description)
    assert isinstance(mmrest, abjad.MultimeasureRest), repr(mmrest)
    assert isinstance(command, str), repr(command)
    assert isinstance(fermata_duration, int), repr(fermata_duration)
    markup = abjad.Markup(rf"\baca-{command}-markup")
    abjad.attach(
        markup,
        mmrest,
        direction=abjad.UP,
        # tag=self.tag.append(_tags.function_name(_frame(), self, n=1)),
        tag=_tags.function_name(_frame(), n=1),
    )
    literal = abjad.LilyPondLiteral(r"\baca-fermata-measure")
    abjad.attach(
        literal,
        mmrest,
        # tag=self.tag.append(_tags.function_name(_frame(), self, n=2)),
        tag=_tags.function_name(_frame(), n=2),
    )
    # tag = abjad.Tag(_enums.FERMATA_MEASURE.name)
    # tag = tag.append(self.tag)
    # tag = tag.append(_tags.function_name(_frame(), n=3))
    abjad.attach(
        _enums.FERMATA_MEASURE,
        mmrest,
        # TODO: remove enum tag?
        tag=_tags.FERMATA_MEASURE,
    )
    abjad.annotate(mmrest, _enums.FERMATA_DURATION, fermata_duration)


def instrument(
    instrument: abjad.Instrument,
    selector=lambda _: abjad.select.leaf(_, 0),
) -> InstrumentChangeCommand:
    assert isinstance(instrument, abjad.Instrument), repr(instrument)
    return InstrumentChangeCommand(
        indicators=[instrument],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def instrument_function(
    leaf: abjad.Leaf,
    instrument: abjad.Instrument,
    tags: list[abjad.Tag] = None,
) -> None:
    assert isinstance(instrument, abjad.Instrument), repr(instrument)
    # tag = _tags.function_name(_frame())
    tag = abjad.Tag("baca.instrument()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    abjad.attach(
        instrument,
        leaf,
        tag=tag,
    )


def invisible_music(
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    map=None,
) -> _command.Suite:
    r"""
    Attaches ``\baca-invisible-music`` literal.

    ..  container:: example

        Attaches ``\baca-invisible-music`` literal to middle leaves:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     commands,
        ...     commands.manifests(),
        ...     commands.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ... )

        >>> music = baca.make_notes(commands.get())
        >>> score["Music"].extend(music)
        >>> commands(
        ...     "Music",
        ...     baca.pitch("C5"),
        ...     baca.invisible_music(
        ...         selector=lambda _: baca.select.leaves(_)[1:-1],
        ...     ),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 4/8
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 4/8
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        c''2
                        %@% \abjad-invisible-music
                        \abjad-invisible-music-coloring
                        c''4.
                        %@% \abjad-invisible-music
                        \abjad-invisible-music-coloring
                        c''2
                        c''4.
                    }
                >>
            }

    """
    tag = _tags.function_name(_frame(), n=1)
    tag = tag.append(_tags.INVISIBLE_MUSIC_COMMAND)
    command_1 = IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\abjad-invisible-music")],
        deactivate=True,
        map=map,
        selector=selector,
        tags=[tag],
    )
    tag = _tags.function_name(_frame(), n=2)
    tag = tag.append(_tags.INVISIBLE_MUSIC_COLORING)
    command_2 = IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\abjad-invisible-music-coloring")],
        map=map,
        selector=selector,
        tags=[tag],
    )
    return _command.suite(command_1, command_2)


def label(
    callable_,
    selector=lambda _: _select.leaves(_),
) -> LabelCommand:
    r"""
    Applies label ``callable_`` to ``selector`` output.

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
        ...     baca.label(lambda _: abjad.label.with_pitches(_, locale="us")),
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
                    \times 9/10
                    {
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
                    \times 4/5
                    {
                        a'16
                        ^ \markup { A4 }
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return LabelCommand(callable_=callable_, selector=selector)


def markup(
    argument: str | abjad.Markup,
    *tweaks: abjad.Tweak,
    direction=abjad.UP,
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    selector=lambda _: _select.pleaf(_, 0),
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
        ...     baca.markup(r'\markup "più mosso"'),
        ...     baca.tuplet_bracket_outside_staff_priority(1000),
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
                        \override TupletBracket.outside-staff-priority = 1000
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        ^ \markup "più mosso"
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
                        \revert TupletBracket.outside-staff-priority
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Pass predefined markup commands like this:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.markup(r"\markup { \baca-triple-diamond-markup }"),
        ...     baca.tuplet_bracket_outside_staff_priority(1000),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(
        ...     selection, includes=["baca.ily"]
        ... )
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
                        \override TupletBracket.outside-staff-priority = 1000
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
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
    if direction not in (abjad.DOWN, abjad.UP):
        message = f"direction must be up or down (not {direction!r})."
        raise Exception(message)
    indicator: abjad.Markup | abjad.Bundle
    if isinstance(argument, str):
        indicator = abjad.Markup(argument)
    elif isinstance(argument, abjad.Markup):
        indicator = dataclasses.replace(argument)
    else:
        message = "MarkupLibary.__call__():\n"
        message += "  Value of 'argument' must be str or markup.\n"
        message += f"  Not {argument!r}."
        raise Exception(message)
    if tweaks:
        indicator = abjad.bundle(indicator, *tweaks)
    if (
        selector is not None
        and not isinstance(selector, str)
        and not callable(selector)
    ):
        message = "selector must be string or callable"
        message += f" (not {selector!r})."
        raise Exception(message)

    def select_phead_0(argument):
        return _select.phead(argument, 0)

    selector = selector or select_phead_0
    return IndicatorCommand(
        direction=direction,
        indicators=[indicator],
        map=map,
        match=match,
        measures=measures,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def markup_function(
    leaf,
    argument: str | abjad.Markup,
    *tweaks: abjad.Tweak,
    direction=abjad.UP,
    tags: list[abjad.Tag] = None,
) -> None:
    assert isinstance(leaf, abjad.Leaf), repr(leaf)
    if direction not in (abjad.DOWN, abjad.UP):
        message = f"direction must be up or down (not {direction!r})."
        raise Exception(message)
    indicator: abjad.Markup | abjad.Bundle
    if isinstance(argument, str):
        indicator = abjad.Markup(argument)
    elif isinstance(argument, abjad.Markup):
        indicator = dataclasses.replace(argument)
    else:
        message = "MarkupLibary.__call__():\n"
        message += "  Value of 'argument' must be str or markup.\n"
        message += f"  Not {argument!r}."
        raise Exception(message)
    if tweaks:
        indicator = abjad.bundle(indicator, *tweaks)
    # tag = _tags.function_name(_frame())
    tag = abjad.Tag("baca.markup()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    abjad.attach(
        indicator,
        leaf,
        direction=direction,
        tag=tag,
    )


def one_voice(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> IndicatorCommand:
    literal = abjad.LilyPondLiteral(r"\oneVoice")
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def open_volta(skip, first_measure_number):
    assert isinstance(first_measure_number, int), repr(first_measure_number)
    bar_line(skip, ".|:", site="before")
    tag = _tags.function_name(_frame())
    measure_number = abjad.get.measure_number(skip)
    measure_number += first_measure_number - 1
    measure_number_tag = abjad.Tag(f"MEASURE_{measure_number}")
    _overrides.bar_line_x_extent(
        [skip],
        (0, 2),
        tags=[tag, _tags.NOT_MOL, measure_number_tag],
    )
    _overrides.bar_line_x_extent(
        [skip],
        (0, 3),
        tags=[tag, _tags.ONLY_MOL, measure_number_tag],
    )


def previous_metadata(path: str, file_name: str = "__metadata__"):
    # reproduces baca.path.Path.get_previous_path()
    # because Travis isn't configured for scores-directory calculations
    music_py = pathlib.Path(path)
    section = pathlib.Path(music_py).parent
    assert section.parent.name == "sections", repr(section)
    sections = section.parent
    assert sections.name == "sections", repr(sections)
    paths = list(sorted(sections.glob("*")))
    paths = [_ for _ in paths if not _.name.startswith(".")]
    paths = [_ for _ in paths if _.is_dir()]
    index = paths.index(section)
    if index == 0:
        return {}
    previous_index = index - 1
    previous_section = paths[previous_index]
    previous_metadata = _path.get_metadata(previous_section, file_name=file_name)
    return previous_metadata


def replace_with_clusters(
    widths: list[int],
    selector=lambda _: _select.plts(_, exclude=_enums.HIDDEN),
    *,
    start_pitch: int | str | abjad.NamedPitch | None = None,
) -> ClusterCommand:
    if start_pitch is not None:
        start_pitch = abjad.NamedPitch(start_pitch)
    return ClusterCommand(selector=selector, start_pitch=start_pitch, widths=widths)


def untie(selector) -> DetachCommand:
    return DetachCommand(arguments=[abjad.Tie, abjad.RepeatTie], selector=selector)


def voice_four(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> IndicatorCommand:
    literal = abjad.LilyPondLiteral(r"\voiceFour")
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def voice_one(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> IndicatorCommand:
    literal = abjad.LilyPondLiteral(r"\voiceOne")
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def voice_three(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> IndicatorCommand:
    literal = abjad.LilyPondLiteral(r"\voiceThree")
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def voice_two(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> IndicatorCommand:
    literal = abjad.LilyPondLiteral(r"\voiceTwo")
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )
