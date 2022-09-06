"""
Command.
"""
import dataclasses
import typing

import abjad

from . import tags as _tags
from . import typings as _typings
from .enums import enums as _enums


# TODO: frozen=True
@dataclasses.dataclass(order=True, slots=True, unsafe_hash=True)
class Scope:

    # TODO: reverse order of parameters; make voice_name mandatory

    measures: _typings.Slice = (1, -1)
    voice_name: str | None = None

    def __post_init__(self):
        if isinstance(self.measures, int):
            self.measures = (self.measures, self.measures)
        assert isinstance(self.measures, list | tuple), repr(self.measures)
        assert len(self.measures) == 2, repr(self.measures)
        start, stop = self.measures
        assert isinstance(start, int), repr(start)
        assert start != 0, repr(start)
        assert isinstance(stop, int), repr(stop)
        assert stop != 0, repr(stop)
        assert isinstance(self.voice_name, str), repr(self.voice_name)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Command:
    """
    Command.
    """

    deactivate: bool = False
    scope: Scope | None = None
    selector: typing.Callable = lambda _: abjad.select.leaves(_, exclude=_enums.HIDDEN)
    tag_measure_number: bool = False
    tags: list[abjad.Tag] = dataclasses.field(default_factory=list)
    _state: dict = dataclasses.field(default_factory=dict, repr=False)
    _tags: list[abjad.Tag] = dataclasses.field(default_factory=list, repr=False)

    def __post_init__(self):
        # raise Exception("ASDF")
        if self.selector is not None:
            assert callable(self.selector)
        assert isinstance(self.tags, list), repr(self.tags)
        assert all(isinstance(_, abjad.Tag) for _ in self.tags), repr(self.tags)

    def __call__(self, argument=None, runtime: dict = None) -> bool:
        runtime = runtime or {}
        return self._call(argument=argument, runtime=runtime)

    def __repr__(self):
        return f"{type(self).__name__}(scope={self.scope})"

    def _call(self, *, argument=None, runtime=None) -> bool:
        return False

    # TODO: reimplement as method with leaf argument
    # TODO: supply with all self.get_tag(leaf) functionality
    # TODO: always return tag (never none) for in-place append
    @property
    def tag(self) -> abjad.Tag:
        # TODO: replace self.get_tag() functionality
        words = [_ if isinstance(_, str) else _.string for _ in self.tags]
        string = ":".join(words)
        tag = abjad.Tag(string)
        assert isinstance(tag, abjad.Tag)
        return tag

    # TODO: replace in favor of self.tag(leaf)
    def get_tag(
        self, leaf: abjad.Leaf = None, *, runtime: dict = None
    ) -> abjad.Tag | None:
        tags = self.tags[:]
        if self.tag_measure_number:
            assert runtime, repr(runtime)
            start_offset = abjad.get.timespan(leaf).start_offset
            measure_number = runtime["offset_to_measure_number"].get(start_offset)
            if getattr(self, "after", None) is True:
                measure_number += 1
            if measure_number is not None:
                tag = abjad.Tag(f"MEASURE_{measure_number}")
                tags.append(tag)
        if tags:
            words = [_.string for _ in tags]
            string = ":".join(words)
            tag = abjad.Tag(string)
            return tag
        # TODO: return empty tag (instead of none)
        return None


def not_mol(command: Command) -> Command:
    """
    Tags ``command`` with ``NOT_MOL`` (not middle-of-line).
    """
    return tag(_tags.NOT_MOL, command, tag_measure_number=True)


def not_parts(command: Command) -> Command:
    """
    Tags ``command`` with ``-PARTS``.
    """
    return tag(_tags.NOT_PARTS, command)


def not_score(command: Command) -> Command:
    """
    Tags ``command`` with ``-SCORE``.
    """
    return tag(_tags.NOT_SCORE, command)


def not_section(command: Command) -> Command:
    """
    Tags ``command`` with ``-SECTION``.
    """
    return tag(_tags.NOT_SECTION, command)


def only_mol(command: Command) -> Command:
    """
    Tags ``command`` with ``ONLY_MOL`` (only middle-of-line).
    """
    return tag(_tags.ONLY_MOL, command, tag_measure_number=True)


def only_parts(command: Command) -> Command:
    r"""
    Tags ``command`` with ``+PARTS``.

    ..  container:: example

        REGRESSION. Dynamic status color tweaks copy dynamic edition tags:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> first_measure_number = baca.interpret.set_up_score(
        ...     score,
        ...     accumulator.time_signatures,
        ...     accumulator,
        ...     docs=True,
        ... )
        >>> baca.SpacingSpecifier((1, 12))(score)
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> voice = score["Music"]
        >>> wrappers = baca.hairpin_function(voice, "p < f")
        >>> baca.tags.wrappers(wrappers, baca.tags.ONLY_PARTS)

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     {},
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
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
                        \baca-repeat-pitch-class-coloring
                        c'2
                        - \tweak color #(x11-color 'blue)
                        \p
                        \<
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        \baca-repeat-pitch-class-coloring
                        c'2
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        \f
                    }
                >>
            }

    """
    return tag(_tags.ONLY_PARTS, command)


def only_score(command: Command) -> Command:
    """
    Tags ``command`` with ``+SCORE``.
    """
    return tag(_tags.ONLY_SCORE, command)


def only_section(command: Command) -> Command:
    """
    Tags ``command`` with ``+SECTION``.
    """
    return tag(_tags.ONLY_SECTION, command)


def tag(
    tags: abjad.Tag | list[abjad.Tag],
    command: Command,
    *,
    deactivate: bool = False,
    tag_measure_number: bool = False,
) -> Command:
    """
    Appends each tag in ``tags`` to ``command``.

    Sorts ``command`` tags.
    """
    if isinstance(tags, abjad.Tag):
        tags = [tags]
    if not isinstance(tags, list):
        raise Exception("tags must be tag or list of tags (not {tags!r}).")
    assert all(isinstance(_, abjad.Tag) for _ in tags), repr(tags)
    assert isinstance(tags, list), repr(tags)
    assert all(isinstance(_, abjad.Tag) for _ in tags), repr(tags)
    if not isinstance(command, Command):
        raise Exception("can only tag command or suite.")
    assert isinstance(command, Command), repr(command)
    assert command._tags is not None
    try:
        tags.sort()
    except TypeError:
        pass
    assert all(isinstance(_, abjad.Tag) for _ in tags), repr(tags)
    command.tags.extend(tags)
    command = dataclasses.replace(
        command,
        deactivate=deactivate,
        tag_measure_number=tag_measure_number,
    )
    return command
