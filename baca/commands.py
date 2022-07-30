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
from . import indicatorclasses as _indicatorclasses
from . import overrides as _overrides
from . import parts as _parts
from . import path as _path
from . import pitchfunctions as _pitchfunctions
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
    tag_ = _tags.function_name(_frame())
    if tag is not None:
        tag_ = tag_.append(tag)
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
                tag=tag_,
                wrapper=True,
            )
            if _treat.compare_persistent_indicators(indicator, reapplied):
                _treat.treat_persistent_wrapper(manifests, wrapper, "redundant")


def _do_bcp_command(
    argument,
    bcps,
    *,
    bow_change_tweaks=None,
    helper: typing.Callable = lambda x, y: x,
    final_spanner=None,
    tag=None,
    tweaks=None,
):
    if tag is None:
        tag = abjad.Tag()
    bcps_ = list(bcps)
    bcps_ = helper(bcps_, argument)
    bcps = abjad.CyclicTuple(bcps_)
    lts = _select.lts(argument)
    add_right_text_to_me = None
    if not final_spanner:
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
    if final_spanner and not _is_rest(lts[-1]) and len(lts[-1]) == 1:
        next_leaf_after_argument = abjad.get.leaf(lts[-1][-1], 1)
        if next_leaf_after_argument is None:
            message = "can not attach final spanner:"
            message += " argument includes end of score."
            raise Exception(message)
    previous_bcp = None
    i = 0
    for lt in lts:
        stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanBCP")
        if not final_spanner and lt is lts[-1] and not _is_rest(lt.head):
            abjad.attach(
                stop_text_span,
                lt.head,
                # tag=self.tag.append(_tags.function_name(_frame(), self, n=1)),
                tag=tag.append(abjad.Tag("baca.bcps(1)")),
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
            if final_spanner:
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
            command=r"\bacaStartTextSpanBCP",
            left_text=left_text,
            right_text=right_text,
            style=style,
        )
        if tweaks:
            start_text_span = _tweaks.bundle_tweaks(start_text_span, tweaks)
        if _is_rest(lt.head) and (_is_rest(next_leaf) or next_leaf is None):
            pass
        else:
            abjad.attach(
                start_text_span,
                lt.head,
                # tag=self.tag.append(_tags.function_name(_frame(), self, n=2)),
                tag=tag.append(abjad.Tag("baca.bcps(2)")),
            )
        if 0 < i - 1:
            abjad.attach(
                stop_text_span,
                lt.head,
                # tag=self.tag.append(_tags.function_name(_frame(), self, n=3)),
                tag=tag.append(abjad.Tag("baca.bcps(3)")),
            )
        if lt is lts[-1] and final_spanner:
            abjad.attach(
                stop_text_span,
                next_leaf_after_argument,
                # tag=self.tag.append(_tags.function_name(_frame(), self, n=4)),
                tag=tag.append(abjad.Tag("baca.bcps(4)")),
            )
        bcp_fraction = abjad.Fraction(*bcp)
        next_bcp_fraction = abjad.Fraction(*bcps[i])
        if _is_rest(lt.head):
            pass
        elif _is_rest(previous_leaf) or previous_bcp is None:
            if bcp_fraction > next_bcp_fraction:
                articulation = abjad.Articulation("upbow")
                if bow_change_tweaks:
                    articulation = _tweaks.bundle_tweaks(
                        articulation,
                        bow_change_tweaks,
                    )
                abjad.attach(
                    articulation,
                    lt.head,
                    # tag=self.tag.append(_tags.function_name(_frame(), self, n=5)),
                    tag=tag.append(abjad.Tag("baca.bcps(5)")),
                )
            elif bcp_fraction < next_bcp_fraction:
                articulation = abjad.Articulation("downbow")
                if bow_change_tweaks:
                    articulation = _tweaks.bundle_tweaks(
                        articulation,
                        bow_change_tweaks,
                    )
                abjad.attach(
                    articulation,
                    lt.head,
                    # tag=self.tag.append(_tags.function_name(_frame(), self, n=6)),
                    tag=tag.append(abjad.Tag("baca.bcps(6)")),
                )
        else:
            previous_bcp_fraction = abjad.Fraction(*previous_bcp)
            if previous_bcp_fraction < bcp_fraction > next_bcp_fraction:
                articulation = abjad.Articulation("upbow")
                if bow_change_tweaks:
                    articulation = _tweaks.bundle_tweaks(
                        articulation,
                        bow_change_tweaks,
                    )
                abjad.attach(
                    articulation,
                    lt.head,
                    # tag=self.tag.append(_tags.function_name(_frame(), self, n=7)),
                    tag=tag.append(abjad.Tag("baca.bcps(7)")),
                )
            elif previous_bcp_fraction > bcp_fraction < next_bcp_fraction:
                articulation = abjad.Articulation("downbow")
                if bow_change_tweaks:
                    articulation = _tweaks.bundle_tweaks(
                        articulation,
                        bow_change_tweaks,
                    )
                abjad.attach(
                    articulation,
                    lt.head,
                    # tag=self.tag.append(_tags.function_name(_frame(), self, n=8)),
                    tag=tag.append(abjad.Tag("baca.bcps(8)")),
                )
        previous_bcp = bcp


def _do_detach_command(argument, indicators):
    leaves = abjad.select.leaves(argument)
    assert isinstance(leaves, list)
    for leaf in leaves:
        for indicator in indicators:
            abjad.detach(indicator, leaf)
    return False


def _do_part_assignment_command(argument, part_assignment):
    first_leaf = abjad.get.leaf(argument, 0)
    if first_leaf is None:
        return False
    voice = abjad.get.parentage(first_leaf).get(abjad.Voice, -1)
    if voice is not None and part_assignment is not None:
        assert isinstance(voice, abjad.Voice)
        section = part_assignment.name or "ZZZ"
        assert voice.name is not None
        if not voice.name.startswith(section):
            message = f"{voice.name} does not allow"
            message += f" {part_assignment.name} part assignment:"
            message += f"\n  {part_assignment}"
            raise Exception(message)
    assert part_assignment is not None
    name, token = part_assignment.name, part_assignment.token
    if token is None:
        identifier = f"%*% PartAssignment({name!r})"
    else:
        identifier = f"%*% PartAssignment({name!r}, {token!r})"
    container = abjad.Container(identifier=identifier)
    leaves = abjad.select.leaves(argument)
    components = abjad.select.top(leaves)
    abjad.mutate.wrap(components, container)


def _is_rest(argument):
    prototype = (abjad.Rest, abjad.MultimeasureRest, abjad.Skip)
    if isinstance(argument, prototype):
        return True
    annotation = abjad.get.annotation(argument, "is_sounding")
    if annotation is False:
        return True
    return False


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
class AccidentalAdjustmentCommand(_command.Command):

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
class BCPCommand(_command.Command):

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
        _do_bcp_command(
            argument,
            self.bcps,
            bow_change_tweaks=self.bow_change_tweaks,
            helper=self.helper,
            final_spanner=self.final_spanner,
            tag=self.tag,
            tweaks=self.tweaks,
        )
        return False


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
        _do_detach_command(argument, self.arguments)
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
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN)
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
        _do_part_assignment_command(argument, self.part_assignment)
        return False


class SchemeManifest:
    """
    Scheme manifest.

    New functions defined in ``~/baca/lilypond/baca.ily`` must be added here.
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

    def dynamic_to_steady_state(self, dynamic) -> str:
        """
        Changes ``dynamic`` to steady state.

        ..  container:: example

            >>> scheme_manifest = baca.SchemeManifest()
            >>> scheme_manifest.dynamic_to_steady_state("sfz-p")
            'p'

        """
        for dynamic_, steady_state in self._dynamics:
            if dynamic_ == dynamic:
                return steady_state
            if dynamic_ == "baca-" + dynamic:
                return steady_state
        raise KeyError(dynamic)


def dynamic(
    dynamic: str | abjad.Dynamic,
    *tweaks: abjad.Tweak,
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
    redundant: bool = False,
) -> IndicatorCommand:
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
    argument,
    dynamic: str | abjad.Dynamic,
    *tweaks: abjad.Tweak,
    tags: list[abjad.Tag] = None,
) -> None:
    tag = _tags.function_name(_frame())
    for tag_ in tags or []:
        tag = tag.append(tag_)
    for leaf in abjad.select.leaves(argument):
        if isinstance(dynamic, str):
            indicator = make_dynamic(dynamic)
        else:
            indicator = dynamic
        prototype = (abjad.Dynamic, abjad.StartHairpin, abjad.StopHairpin)
        assert isinstance(indicator, prototype), repr(indicator)
        indicator = _tweaks.bundle_tweaks(indicator, tweaks)
        _attach_persistent_indicator(
            leaf,
            [indicator],
            manifests={},
            tag=tag,
        )


def force_accidental(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> AccidentalAdjustmentCommand:
    return AccidentalAdjustmentCommand(forced=True, selector=selector)


def levine_multiphonic(n: int) -> abjad.Markup:
    assert isinstance(n, int), repr(n)
    return abjad.Markup(rf'\baca-boxed-markup "L.{n}"')


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


def metronome_mark_function(
    argument,
    indicator,
    manifests,
    *,
    deactivate=False,
    tags: list[abjad.Tag] = None,
):
    prototype = (
        abjad.MetricModulation,
        abjad.MetronomeMark,
        _indicatorclasses.Accelerando,
        _indicatorclasses.Ritardando,
    )
    assert isinstance(indicator, prototype), repr(indicator)
    tag = _tags.function_name(_frame())
    for tag_ in tags or []:
        tag = tag.append(tag_)
    for leaf in abjad.select.leaves(argument):
        _attach_persistent_indicator(
            leaf,
            [indicator],
            deactivate=deactivate,
            manifests=manifests,
            tag=tag,
        )


def bar_line_function(
    argument,
    abbreviation: str = "|",
    *,
    site: str = "after",
):
    assert isinstance(abbreviation, str), repr(abbreviation)
    tag = _tags.function_name(_frame())
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.BarLine(abbreviation, site=site)
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def clef(
    clef: str = "treble",
    *,
    redundant: bool = False,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    indicator = abjad.Clef(clef)
    return IndicatorCommand(
        indicators=[indicator],
        redundant=redundant,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def clef_function(
    argument,
    clef: str,
) -> None:
    assert isinstance(clef, str), repr(clef)
    tag = _tags.function_name(_frame())
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.Clef(clef)
        _attach_persistent_indicator(
            leaf,
            [indicator],
            manifests={},
            tag=tag,
        )


def instrument_name(
    string: str,
    *,
    context: str = "Staff",
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    assert isinstance(string, str), repr(string)
    assert string.startswith("\\"), repr(string)
    indicator = abjad.InstrumentName(string, context=context)
    command = IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame()), _tags.NOT_PARTS],
    )
    return command


def instrument_name_function(
    argument,
    string: str,
    *,
    context: str = "Staff",
) -> None:
    assert isinstance(string, str), repr(string)
    assert string.startswith("\\"), repr(string)
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.NOT_PARTS)
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.InstrumentName(string, context=context)
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def literal(
    string: str | list[str],
    *,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
    site: str = "before",
) -> IndicatorCommand:
    literal = abjad.LilyPondLiteral(string, site=site)
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def literal_function(
    argument,
    string: str | list[str],
    *,
    site: str = "before",
    tags: list[abjad.Tag] = None,
) -> None:
    tag = _tags.function_name(_frame())
    for tag_ in tags or []:
        tag = tag.append(tag_)
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.LilyPondLiteral(string, site=site)
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def short_instrument_name(
    argument: str,
    *,
    alert: IndicatorCommand = None,
    context: str = "Staff",
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand | _command.Suite:
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
    argument,
    short_instrument_name: abjad.ShortInstrumentName,
    manifests: dict = None,
    *,
    context: str = "Staff",
) -> None:
    assert isinstance(short_instrument_name, abjad.ShortInstrumentName), repr(
        short_instrument_name
    )
    manifests = manifests or {}
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.NOT_PARTS)
    for leaf in abjad.select.leaves(argument):
        _attach_persistent_indicator(
            leaf,
            [short_instrument_name],
            manifests=manifests,
            tag=tag,
        )


def mark(
    argument: str,
    *tweaks: abjad.Tweak,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    assert isinstance(argument, abjad.Markup | str), repr(argument)
    rehearsal_mark = abjad.RehearsalMark(markup=argument)
    rehearsal_mark = _tweaks.bundle_tweaks(rehearsal_mark, tweaks)
    return IndicatorCommand(
        indicators=[rehearsal_mark],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def mark_function(
    argument,
    string: str,
    *tweaks: abjad.Tweak,
) -> None:
    assert isinstance(string, abjad.Markup | str), repr(string)
    tag = _tags.function_name(_frame())
    for leaf in abjad.select.leaves(argument):
        rehearsal_mark = abjad.RehearsalMark(markup=string)
        rehearsal_mark = _tweaks.bundle_tweaks(rehearsal_mark, tweaks)
        abjad.attach(
            rehearsal_mark,
            leaf,
            tag=tag,
        )


def parenthesize_function(argument) -> None:
    tag = _tags.function_name(_frame())
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.LilyPondLiteral(r"\parenthesize")
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def rehearsal_mark_function(
    argument,
    string: str,
    *tweaks: abjad.Tweak,
    font_size: int = 10,
    tags: list[abjad.Tag] = None,
) -> None:
    assert isinstance(string, str), repr(string)
    assert isinstance(font_size, int | float), repr(font_size)
    string = rf'\baca-rehearsal-mark-markup "{string}" #{font_size}'
    for leaf in abjad.select.leaves(argument):
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
    if allow_rest is not None:
        allow_rest = bool(allow_rest)
    return IndicatorCommand(
        do_not_test=allow_rest,
        indicators=[abjad.RepeatTie()],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def repeat_tie_function(argument) -> None:
    tag = _tags.function_name(_frame())
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.RepeatTie()
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def staff_lines(
    n: int,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _command.Suite:
    command_1 = IndicatorCommand(
        indicators=[_indicatorclasses.BarExtent(n)],
        selector=selector,
        tags=[_tags.function_name(_frame(), n=1), _tags.NOT_PARTS],
    )
    command_2 = IndicatorCommand(
        indicators=[_indicatorclasses.StaffLines(n)],
        selector=selector,
        tags=[_tags.function_name(_frame(), n=2)],
    )
    return _command.suite(command_1, command_2)


def staff_lines_function(argument, n: int) -> None:
    assert isinstance(n, int), repr(n)
    for leaf in abjad.select.leaves(argument):
        bar_extent = _indicatorclasses.BarExtent(n)
        _attach_persistent_indicator(
            leaf,
            [bar_extent],
            manifests={},
            tag=abjad.Tag("baca.staff_lines_function(1)").append(_tags.NOT_PARTS),
        )
        staff_lines = _indicatorclasses.StaffLines(n)
        _attach_persistent_indicator(
            leaf,
            [staff_lines],
            manifests={},
            tag=abjad.Tag("baca.staff_lines_function(2)"),
        )


def stop_trill(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    r"""
    Attaches stop trill to closing-slot.

    The closing format slot is important because LilyPond fails to compile when
    ``\stopTrillSpan`` appears after ``\set instrumentName`` accumulator (and
    probably other ``\set`` accumulator). Setting format slot to closing here
    positions ``\stopTrillSpan`` after the leaf in question (which is required)
    and also draws ``\stopTrillSpan`` closer to the leaf in question, prior to
    ``\set instrumentName`` and other accumulator positioned in the after slot.

    Eventually it will probably be necessary to model ``\stopTrillSpan`` with a
    dedicated format slot.
    """
    return literal(r"\stopTrillSpan", site="closing", selector=selector)


def tie(
    *, selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN)
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.Tie()],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def tie_function(argument) -> None:
    tag = _tags.function_name(_frame())
    for leaf in abjad.select.leaves(argument):
        indicator = abjad.Tie()
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def allow_octaves(
    *, selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN)
) -> IndicatorCommand:
    return IndicatorCommand(indicators=[_enums.ALLOW_OCTAVE], selector=selector)


def assign_part(
    part_assignment: _parts.PartAssignment,
    *,
    # IMPORTANT: must include hidden leaves:
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> PartAssignmentCommand:
    assert isinstance(part_assignment, _parts.PartAssignment), repr(part_assignment)
    return PartAssignmentCommand(part_assignment=part_assignment, selector=selector)


def assign_part_function(
    argument,
    part_assignment: _parts.PartAssignment,
) -> None:
    assert isinstance(part_assignment, _parts.PartAssignment), repr(part_assignment)
    _do_part_assignment_command(argument, part_assignment)


def bcps(
    bcps,
    *tweaks: _typings.IndexedTweak,
    bow_change_tweaks: typing.Sequence[_typings.IndexedTweak] = (),
    final_spanner: bool = False,
    helper: typing.Callable = lambda x, y: x,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> BCPCommand:
    if final_spanner is not None:
        assert isinstance(final_spanner, bool), repr(final_spanner)
    return BCPCommand(
        bcps=bcps,
        bow_change_tweaks=tuple(bow_change_tweaks),
        final_spanner=final_spanner,
        helper=helper,
        selector=selector,
        tags=[_tags.function_name(_frame())],
        tweaks=tweaks,
    )


def bcps_function(
    argument,
    bcps,
    *tweaks: _typings.IndexedTweak,
    bow_change_tweaks: typing.Sequence[_typings.IndexedTweak] = (),
    final_spanner: bool = False,
    helper: typing.Callable = lambda x, y: x,
    tag=abjad.Tag("baca.bcps_function()"),
) -> None:
    _do_bcp_command(
        argument,
        bcps,
        bow_change_tweaks=bow_change_tweaks,
        helper=helper,
        final_spanner=final_spanner,
        tag=tag,
        tweaks=tweaks,
    )


def close_volta_function(skip, first_measure_number, site: str = "before"):
    assert isinstance(first_measure_number, int), repr(first_measure_number)
    assert isinstance(site, str), repr(site)
    after = site == "after"
    bar_line_function(skip, ":|.", site=site)
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
    *,
    lone: bool = False,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> ColorCommand:
    return ColorCommand(selector=selector, lone=lone)


def container(
    identifier: str = None,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> ContainerCommand:
    if identifier is not None:
        if not isinstance(identifier, str):
            raise Exception(f"identifier must be string (not {identifier!r}).")
    return ContainerCommand(identifier=identifier, selector=selector)


def cross_staff(
    *, selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN)
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\crossStaff")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def double_volta_function(skip, first_measure_number):
    assert isinstance(first_measure_number, int), repr(first_measure_number)
    bar_line_function(skip, ":.|.:", site="before")
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


def dynamic_down(
    *, selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN)
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\dynamicDown")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dynamic_up(
    *, selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN)
) -> IndicatorCommand:
    return IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\dynamicUp")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def edition(
    not_parts: str | abjad.Markup | IndicatorCommand,
    only_parts: str | abjad.Markup | IndicatorCommand,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _command.Suite:
    """
    Makes not-parts / only-parts markup suite.
    """
    if isinstance(not_parts, str):
        not_parts = markup(rf"\markup {{ {not_parts} }}", selector=selector)
    elif isinstance(not_parts, abjad.Markup):
        not_parts = markup(not_parts, selector=selector)
    assert isinstance(not_parts, IndicatorCommand)
    not_parts_ = _command.not_parts(not_parts)
    if isinstance(only_parts, str):
        only_parts = markup(rf"\markup {{ {only_parts} }}", selector=selector)
    elif isinstance(only_parts, abjad.Markup):
        only_parts = markup(only_parts, selector=selector)
    assert isinstance(only_parts, IndicatorCommand)
    only_parts_ = _command.only_parts(only_parts)
    return _command.suite(not_parts_, only_parts_)


def finger_pressure_transition(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
    right_broken: bool = False,
) -> GlissandoCommand:
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
    # TODO: maybe remove rleak
    rleak: bool = False,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
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
    accumulator: list[_command.Command] = []
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
    accumulator.append(command)

    def _leaves_of_selector(argument):
        return abjad.select.leaves(new_selector(argument))

    untie_command = untie(_leaves_of_selector)
    accumulator.append(untie_command)
    if pitch is not None and stop_pitch is None:
        # TODO: remove list test from or-clause?
        if isinstance(pitch, abjad.StaffPosition) or (
            isinstance(pitch, list) and isinstance(pitch[0], abjad.StaffPosition)
        ):
            staff_position_command_object = _pitchfunctions._staff_position_command(
                pitch,
                allow_hidden=allow_hidden,
                allow_repitch=allow_repitch,
                mock=mock,
                selector=new_selector,
            )
            accumulator.append(staff_position_command_object)
        else:
            pitch_command_object = _pitchfunctions._pitch_command_factory(
                pitch,
                allow_hidden=allow_hidden,
                allow_repitch=allow_repitch,
                mock=mock,
                selector=new_selector,
            )
            accumulator.append(pitch_command_object)
    elif pitch is not None and stop_pitch is not None:
        if isinstance(pitch, abjad.StaffPosition):
            assert isinstance(stop_pitch, abjad.StaffPosition)
            interpolation_command = (
                _pitchfunctions._interpolate_staff_positions_function(
                    pitch,
                    stop_pitch,
                    allow_hidden=allow_hidden,
                    mock=mock,
                    selector=new_selector,
                )
            )
        else:
            assert isinstance(pitch, str | abjad.NamedPitch)
            assert isinstance(stop_pitch, str | abjad.NamedPitch)
            interpolation_command = _pitchfunctions._interpolate_pitches_function(
                pitch,
                stop_pitch,
                allow_hidden=allow_hidden,
                mock=mock,
                selector=new_selector,
            )
        accumulator.append(interpolation_command)
    return _command.suite(*accumulator)


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
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
    style: str = None,
    zero_padding: bool = False,
) -> GlissandoCommand:
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
    parenthesize_repeats: bool = False,
    right_broken: bool = False,
    right_broken_show_next: bool = False,
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
    tag = _tags.function_name(_frame())
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


def global_fermata_function(
    argument,
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
    assert isinstance(command, str), repr(command)
    assert isinstance(fermata_duration, int), repr(fermata_duration)
    for leaf in abjad.select.leaves(argument):
        markup = abjad.Markup(rf"\baca-{command}-markup")
        abjad.attach(
            markup,
            leaf,
            direction=abjad.UP,
            tag=abjad.Tag("baca.global_fermata_function(1)"),
        )
        literal = abjad.LilyPondLiteral(r"\baca-fermata-measure")
        abjad.attach(
            literal,
            leaf,
            tag=abjad.Tag("baca.global_fermata_function(2)"),
        )
        abjad.attach(
            _enums.FERMATA_MEASURE,
            leaf,
            # TODO: remove enum tag?
            tag=_tags.FERMATA_MEASURE,
        )
        abjad.annotate(leaf, _enums.FERMATA_DURATION, fermata_duration)


def instrument(
    instrument: abjad.Instrument,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> InstrumentChangeCommand:
    assert isinstance(instrument, abjad.Instrument), repr(instrument)
    return InstrumentChangeCommand(
        indicators=[instrument],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def instrument_function(
    argument,
    instrument: abjad.Instrument,
    manifests: dict = None,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    assert isinstance(instrument, abjad.Instrument), repr(instrument)
    manifests = manifests or {}
    tag = _tags.function_name(_frame())
    for tag_ in tags or []:
        tag = tag.append(tag_)
    for leaf in abjad.select.leaves(argument):
        _attach_persistent_indicator(
            leaf,
            [instrument],
            manifests=manifests,
            tag=tag,
        )


def invisible_music(
    *,
    map=None,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> _command.Suite:
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
    *,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> LabelCommand:
    return LabelCommand(callable_=callable_, selector=selector)


def markup(
    argument: str | abjad.Markup,
    *tweaks: abjad.Tweak,
    direction=abjad.UP,
    map=None,
    match: _typings.Indices = None,
    measures: _typings.Slice = None,
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
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
    argument,
    markup: str | abjad.Markup,
    *tweaks: abjad.Tweak,
    direction: abjad.Vertical = abjad.UP,
    tags: list[abjad.Tag] = None,
) -> list[abjad.Wrapper]:
    assert direction in (abjad.DOWN, abjad.UP), repr(direction)
    tag = _tags.function_name(_frame())
    for tag_ in tags or []:
        tag = tag.append(tag_)
    wrappers = []
    for leaf in abjad.select.leaves(argument):
        indicator: abjad.Markup | abjad.Bundle
        if isinstance(markup, str):
            indicator = abjad.Markup(markup)
        else:
            assert isinstance(markup, abjad.Markup), repr(markup)
            indicator = dataclasses.replace(markup)
        if tweaks:
            indicator = abjad.bundle(indicator, *tweaks)
        wrapper = abjad.attach(
            indicator,
            leaf,
            direction=direction,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def one_voice(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    literal = abjad.LilyPondLiteral(r"\oneVoice")
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def open_volta_function(skip, first_measure_number):
    assert isinstance(first_measure_number, int), repr(first_measure_number)
    bar_line_function(skip, ".|:", site="before")
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


def untie(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN)
) -> DetachCommand:
    return DetachCommand(arguments=[abjad.Tie, abjad.RepeatTie], selector=selector)


def untie_function(argument) -> None:
    _do_detach_command(argument, indicators=[abjad.Tie, abjad.RepeatTie])


def voice_four(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    literal = abjad.LilyPondLiteral(r"\voiceFour")
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def voice_one(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    literal = abjad.LilyPondLiteral(r"\voiceOne")
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def voice_three(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    literal = abjad.LilyPondLiteral(r"\voiceThree")
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def voice_two(
    selector: typing.Callable = lambda _: _select.leaves(_, exclude=_enums.HIDDEN),
) -> IndicatorCommand:
    literal = abjad.LilyPondLiteral(r"\voiceTwo")
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )
