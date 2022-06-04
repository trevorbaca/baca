"""
Command.
"""
import dataclasses
import typing

import abjad

from . import scope as _scope
from . import tags as _tags
from . import typings


@dataclasses.dataclass(slots=True)
class Command:
    """
    Command.
    """

    deactivate: bool = False
    map: typing.Any = None
    match: typings.Indices = None
    measures: typings.Slice = None
    scope: _scope.Scope | _scope.TimelineScope | None = None
    selector: typing.Callable | None = None
    tag_measure_number: bool = False
    tags: list[abjad.Tag | None] = dataclasses.field(default_factory=list)
    _mutated_score: bool = dataclasses.field(default=False, init=False, repr=False)
    _runtime: dict = dataclasses.field(default_factory=dict, init=False, repr=False)
    _state: dict = dataclasses.field(default_factory=dict, init=False, repr=False)
    _tags: list[abjad.Tag] = dataclasses.field(init=False, repr=False)

    def __post_init__(self):
        if self.selector is not None:
            assert callable(self.selector)
        self.tags = list(self.tags or [])
        assert isinstance(self.tags, list), repr(self.tags)
        assert all(isinstance(_, abjad.Tag) for _ in self.tags), repr(self.tags)
        self._initialize_tags(self.tags)

    def __call__(self, argument=None, runtime: dict = None) -> None:
        self._runtime = runtime or {}
        if self.map is not None:
            assert callable(self.map)
            argument = self.map(argument)
            for subargument in argument:
                self._call(argument=subargument)
        else:
            return self._call(argument=argument)

    def __repr__(self):
        return f"{type(self).__name__}(scope={self.scope})"

    def _call(self, argument=None):
        pass

    def _initialize_tags(self, tags):
        tags_ = []
        for tag in tags or []:
            if tag in (None, ""):
                continue
            elif isinstance(tag, str):
                for word in tag.split(":"):
                    tag_ = abjad.Tag(word)
                    tags_.append(tag_)
            elif isinstance(tag, abjad.Tag):
                tags_.append(tag)
            else:
                raise TypeError(tag)
        assert all(isinstance(_, abjad.Tag) for _ in tags_)
        self._tags = tags_

    def _matches_scope_index(self, scope_count, i):
        if isinstance(self.match, int):
            if 0 <= self.match and self.match != i:
                return False
            if self.match < 0 and -(scope_count - i) != self.match:
                return False
        elif isinstance(self.match, tuple):
            assert len(self.match) == 2
            triple = slice(*self.match).indices(scope_count)
            if i not in range(*triple):
                return False
        elif isinstance(self.match, list):
            assert all(isinstance(_, int) for _ in self.match)
            if i not in self.match:
                return False
        return True

    @property
    def runtime(self) -> dict:
        return self._runtime

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
    def get_tag(self, leaf: abjad.Leaf = None) -> abjad.Tag | None:
        tags = self.tags[:]
        if self.tag_measure_number:
            start_offset = abjad.get.timespan(leaf).start_offset
            measure_number = self.runtime["offset_to_measure_number"].get(start_offset)
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


@dataclasses.dataclass(slots=True)
class Suite:
    """
    Suite.

    ..  container:: example

        >>> suite = baca.suite(
        ...     baca.accent(),
        ...     baca.tenuto(),
        ...     measures=(1, 2),
        ...     selector=lambda _: baca.select.pleaves(_),
        ... )

    ..  container:: example

        REGRESSION. Templating works like this:

        >>> suite = baca.suite(
        ...     baca.accent(),
        ...     baca.tenuto(),
        ...     measures=(1, 2),
        ... )
        >>> suite.commands[0].measures
        (1, 2)

        >>> new_suite = baca.suite(suite.commands, measures=(3, 4))
        >>> new_suite.commands[0].measures
        (3, 4)

    """

    commands: typing.Sequence["Command | Suite"] = ()
    keywords: dict | None = None

    def __post_init__(self):
        self.commands = self.commands or []
        assert all(isinstance(_, Command | Suite) for _ in self.commands)
        keywords = self.keywords or {}
        commands_ = []
        for item in self.commands:
            if isinstance(item, Command):
                item_ = dataclasses.replace(item, **keywords)
            else:
                item_ = Suite([new(_, **keywords) for _ in item.commands])
            commands_.append(item_)
        self.commands = tuple(commands_)

    def __call__(self, argument=None, runtime=None) -> None:
        """
        Applies each command in ``commands`` to ``argument``.
        """
        if argument is None:
            return
        if not self.commands:
            return
        for command in self.commands:
            command(argument, runtime=runtime)

    def __iter__(self):
        """
        Iterates commands.
        """
        return iter(self.commands)

    def __repr__(self):
        """
        Gets repr.
        """
        return f"{type(self).__name__}(commands={self.commands})"


def chunk(*commands: Command | Suite, **keywords) -> Suite:
    """
    Chunks commands.
    """
    return suite(*commands, **keywords)


def new(*commands: Command | Suite, **keywords) -> Command | Suite:
    r"""
    Makes new ``commands`` with ``keywords``.

    ..  container:: example

        Applies leaf selector to commands:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "MusicVoice",
        ...     baca.make_even_divisions(),
        ...     baca.new(
        ...         baca.marcato(),
        ...         baca.slur(),
        ...         baca.staccato(),
        ...         selector=lambda _: baca.select.leaves(_)[4:-3],
        ...     ),
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
                    \context Voice = "MusicVoice"
                    {
                        b'8
                        [
                        b'8
                        b'8
                        b'8
                        ]
                        b'8
                        - \marcato
                        - \staccato
                        [
                        (
                        b'8
                        - \marcato
                        - \staccato
                        b'8
                        - \marcato
                        - \staccato
                        ]
                        b'8
                        - \marcato
                        - \staccato
                        [
                        b'8
                        - \marcato
                        - \staccato
                        b'8
                        - \marcato
                        - \staccato
                        b'8
                        - \marcato
                        - \staccato
                        )
                        ]
                        b'8
                        [
                        b'8
                        b'8
                        ]
                    }
                >>
            }

    ..  container:: example

        Applies measure selector to commands:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "MusicVoice",
        ...     baca.make_even_divisions(),
        ...     baca.new(
        ...         baca.marcato(),
        ...         baca.slur(),
        ...         baca.staccato(),
        ...         selector=lambda _: baca.select.cmgroups(_)[1:-1],
        ...     ),
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
                    \context Voice = "MusicVoice"
                    {
                        b'8
                        [
                        b'8
                        b'8
                        b'8
                        ]
                        b'8
                        - \marcato
                        - \staccato
                        [
                        (
                        b'8
                        - \marcato
                        - \staccato
                        b'8
                        - \marcato
                        - \staccato
                        ]
                        b'8
                        - \marcato
                        - \staccato
                        [
                        b'8
                        - \marcato
                        - \staccato
                        b'8
                        - \marcato
                        - \staccato
                        b'8
                        - \marcato
                        - \staccato
                        )
                        ]
                        b'8
                        [
                        b'8
                        b'8
                        ]
                    }
                >>
            }

    """
    result = []
    assert all(isinstance(_, Command | Suite) for _ in commands), repr(commands)
    for item in commands:
        item_: Command | Suite
        if isinstance(item, Command):
            item_ = dataclasses.replace(item, **keywords)
        else:
            item_ = Suite([new(_, **keywords) for _ in item.commands])
        result.append(item_)
    if len(result) == 1:
        return result[0]
    else:
        return suite(*result)


def not_mol(command: Command | Suite) -> Command | Suite:
    """
    Tags ``command`` with ``NOT_MOL`` (not middle-of-line).
    """
    return tag(_tags.NOT_MOL, command, tag_measure_number=True)


def not_parts(command: Command | Suite) -> Command | Suite:
    """
    Tags ``command`` with ``-PARTS``.
    """
    return tag(_tags.NOT_PARTS, command)


def not_score(command: Command | Suite) -> Command | Suite:
    """
    Tags ``command`` with ``-SCORE``.
    """
    return tag(_tags.NOT_SCORE, command)


def not_section(command: Command | Suite) -> Command | Suite:
    """
    Tags ``command`` with ``-SEGMENT``.
    """
    return tag(_tags.NOT_SEGMENT, command)


def only_mol(command: Command | Suite) -> Command | Suite:
    """
    Tags ``command`` with ``ONLY_MOL`` (only middle-of-line).
    """
    return tag(_tags.ONLY_MOL, command, tag_measure_number=True)


def only_parts(command: Command | Suite) -> Command | Suite:
    r"""
    Tags ``command`` with ``+PARTS``.

    ..  container:: example

        REGRESSION. Dynamic status color tweaks copy dynamic edition tags:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "MusicVoice",
        ...     baca.make_notes(),
        ...     baca.only_parts(
        ...         baca.hairpin("p < f"),
        ...     ),
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
                    \context Voice = "MusicVoice"
                    {
                        b'2
                        - \tweak color #(x11-color 'blue)
                        \p
                        \<
                        b'4.
                        b'2
                        b'4.
                        \f
                    }
                >>
            }

    """
    return tag(_tags.ONLY_PARTS, command)


def only_score(command: Command | Suite) -> Command | Suite:
    """
    Tags ``command`` with ``+SCORE``.
    """
    return tag(_tags.ONLY_SCORE, command)


def only_section(command: Command | Suite) -> Command | Suite:
    """
    Tags ``command`` with ``+SEGMENT``.
    """
    return tag(_tags.ONLY_SEGMENT, command)


def suite(*commands: Command | Suite, **keywords) -> Suite:
    """
    Makes suite.

    ..  container:: example exception

        Raises exception on noncommand:

        >>> baca.suite("Allegro")
        Traceback (most recent call last):
            ...
        Exception:
            Must contain only commands and suites.
            Not str:
            'Allegro'

    """
    commands_: list[Command | Suite] = []
    for item in commands:
        if isinstance(item, list | tuple):
            commands_.extend(item)
        else:
            commands_.append(item)
    for command in commands_:
        if isinstance(command, Command | Suite):
            continue
        message = "\n  Must contain only commands and suites."
        message += f"\n  Not {type(command).__name__}:"
        message += f"\n  {repr(command)}"
        raise Exception(message)
    return Suite(commands_, keywords)


def tag(
    tags: abjad.Tag | list[abjad.Tag],
    command: Command | Suite,
    *,
    deactivate: bool = False,
    tag_measure_number: bool = False,
) -> Command | Suite:
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
    if not isinstance(command, Command | Suite):
        raise Exception("can only tag command or suite.")
    if isinstance(command, Suite):
        for command_ in command.commands:
            tag(
                tags,
                command_,
                deactivate=deactivate,
                tag_measure_number=tag_measure_number,
            )
    else:
        assert isinstance(command, Command), repr(command)
        assert command._tags is not None
        try:
            tags.sort()
        except TypeError:
            pass
        assert all(isinstance(_, abjad.Tag) for _ in tags), repr(tags)
        command.tags.extend(tags)
        command.deactivate = deactivate
        command.tag_measure_number = tag_measure_number
    return command