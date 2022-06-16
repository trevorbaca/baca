"""
Parts.
"""
import dataclasses
import importlib
import typing

import abjad

from . import path as _path


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Part:
    """
    Part.

    ..  container:: example

        >>> baca.Part("FirstViolin", 18)
        Part(name='FirstViolin', number=18)

    """

    name: str
    number: int | None = None

    def __post_init__(self):
        assert isinstance(self.name, str), repr(self.name)
        if self.number is not None:
            assert isinstance(self.number, int), repr(self.number)

    def identifier(self):
        """
        Gets identifier.

        ..  container:: example

            >>> baca.Part("FirstViolin", 18).identifier()
            'FirstViolin-18'

        """
        if self.number is None:
            return self.name
        else:
            return f"{self.name}-{self.number}"


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class PartAssignment:
    """
    Part assignment.

    ..  container:: example

        >>> baca.PartAssignment("Horn")
        baca.PartAssignment('Horn')

        >>> baca.PartAssignment("Horn", 1)
        baca.PartAssignment('Horn', 1)

        >>> baca.PartAssignment("Horn", 2)
        baca.PartAssignment('Horn', 2)

        >>> baca.PartAssignment("Horn", (3, 4))
        baca.PartAssignment('Horn', (3, 4))

        >>> baca.PartAssignment("Horn", [1, 3])
        baca.PartAssignment('Horn', [1, 3])

    """

    section: typing.Any = None
    token: typing.Any = None

    def __post_init__(self):
        assert isinstance(self.section, str), repr(self.section)
        assert _is_part_assignment_token(self.token), repr(self.token)

    def __contains__(self, part: Part):
        """
        Is true when part assignment contains ``part``.

        ..  container:: example

            >>> parts = [
            ...     baca.Part(name="Horn", number=1),
            ...     baca.Part(name="Horn", number=2),
            ...     baca.Part(name="Horn", number=3),
            ...     baca.Part(name="Horn", number=4),
            ... ]

            >>> part_assignment = baca.PartAssignment("Horn")
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(name='Horn', number=1), True)
            (Part(name='Horn', number=2), True)
            (Part(name='Horn', number=3), True)
            (Part(name='Horn', number=4), True)

            >>> part_assignment = baca.PartAssignment("Horn", 1)
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(name='Horn', number=1), True)
            (Part(name='Horn', number=2), False)
            (Part(name='Horn', number=3), False)
            (Part(name='Horn', number=4), False)

            >>> part_assignment = baca.PartAssignment("Horn", 2)
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(name='Horn', number=1), False)
            (Part(name='Horn', number=2), True)
            (Part(name='Horn', number=3), False)
            (Part(name='Horn', number=4), False)

            >>> part_assignment = baca.PartAssignment("Horn", (3, 4))
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(name='Horn', number=1), False)
            (Part(name='Horn', number=2), False)
            (Part(name='Horn', number=3), True)
            (Part(name='Horn', number=4), True)

            >>> part_assignment = baca.PartAssignment("Horn", [1, 3])
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(name='Horn', number=1), True)
            (Part(name='Horn', number=2), False)
            (Part(name='Horn', number=3), True)
            (Part(name='Horn', number=4), False)

        """
        assert isinstance(part, Part), repr(part)
        members = self.members()
        if part.name == self.section:
            if (
                part.number is None
                or members is None
                or part.number in members
                or members == []
            ):
                return True
            return False
        return False

    # TODO: add keyword section=, token= to repr
    def __repr__(self):
        """
        Custom repr for "baca.PartAssignment" in __persist__ files.
        """
        if self.token is not None:
            return f"baca.{type(self).__name__}({self.section!r}, {self.token!r})"
        else:
            return f"baca.{type(self).__name__}({self.section!r})"

    def members(self):
        members = []
        if self.token is None:
            return members
        if isinstance(self.token, int):
            members.append(self.token)
        elif isinstance(self.token, tuple):
            assert len(self.token) == 2, repr(self.token)
            for member in range(self.token[0], self.token[1] + 1):
                members.append(member)
        else:
            assert isinstance(self.token, list), repr(self.token)
            members.extend(self.token)
        return members

    def parts(self):
        parts = []
        members = self.members()
        if members is None:
            part = Part(name=self.section)
            parts.append(part)
        else:
            for member in members:
                part = Part(name=self.section, number=member)
                parts.append(part)
        return parts


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Section:
    """
    Section.

    ..  container:: example

        >>> baca.Section(
        ...     abbreviation="VN-1",
        ...     count=18,
        ...     name="FirstViolin",
        ... )
        Section(abbreviation='VN-1', count=18, name='FirstViolin')

        >>> baca.Section(
        ...     abbreviation="VN-2",
        ...     count=18,
        ...     name="SecondViolin",
        ... )
        Section(abbreviation='VN-2', count=18, name='SecondViolin')

        >>> baca.Section(
        ...     abbreviation="VA",
        ...     count=18,
        ...     name="Viola",
        ... )
        Section(abbreviation='VA', count=18, name='Viola')

        >>> baca.Section(
        ...     abbreviation="VC",
        ...     count=14,
        ...     name="Cello",
        ... )
        Section(abbreviation='VC', count=14, name='Cello')

        >>> baca.Section(
        ...     abbreviation="CB",
        ...     count=6,
        ...     name="Contrabass",
        ... )
        Section(abbreviation='CB', count=6, name='Contrabass')

    """

    abbreviation: str = ""
    count: int = 1
    name: str = ""

    def __post_init__(self):
        assert isinstance(self.abbreviation, str), repr(self.abbreviation)
        assert isinstance(self.count, int), repr(self.count)
        assert 1 <= self.count, repr(self.count)
        assert isinstance(self.name, str), repr(self.name)

    def parts(self):
        r"""
        Gets parts.

        ..  container:: example

            >>> section = baca.Section(
            ...     abbreviation="VN-1",
            ...     count=18,
            ...     name="FirstViolin",
            ... )

            >>> for part in section.parts(): part
            Part(name='FirstViolin', number=1)
            Part(name='FirstViolin', number=2)
            Part(name='FirstViolin', number=3)
            Part(name='FirstViolin', number=4)
            Part(name='FirstViolin', number=5)
            Part(name='FirstViolin', number=6)
            Part(name='FirstViolin', number=7)
            Part(name='FirstViolin', number=8)
            Part(name='FirstViolin', number=9)
            Part(name='FirstViolin', number=10)
            Part(name='FirstViolin', number=11)
            Part(name='FirstViolin', number=12)
            Part(name='FirstViolin', number=13)
            Part(name='FirstViolin', number=14)
            Part(name='FirstViolin', number=15)
            Part(name='FirstViolin', number=16)
            Part(name='FirstViolin', number=17)
            Part(name='FirstViolin', number=18)

        """
        parts = []
        if self.count is None:
            part = Part(self.name)
            parts.append(part)
        else:
            for member in range(1, self.count + 1):
                part = Part(name=self.name, number=member)
                parts.append(part)
        return parts


class PartManifest:
    """
    Part manifest.

    ..  container:: example

        Initializes from parts:

        >>> part_manifest = baca.PartManifest(
        ...     baca.Part(name="BassClarinet"),
        ...     baca.Part(name="Violin"),
        ...     baca.Part(name="Viola"),
        ...     baca.Part(name="Cello"),
        ... )
        >>> len(part_manifest.parts)
        4

    ..  container:: example

        Initializes from orchestra sections:

        >>> part_manifest = baca.PartManifest(
        ...     baca.Section(
        ...         abbreviation="FL",
        ...         count=4,
        ...         name="Flute",
        ...     ),
        ...     baca.Section(
        ...         abbreviation="OB",
        ...         count=3,
        ...         name="Oboe",
        ...     ),
        ...     baca.Part("EnglishHorn"),
        ...     baca.Section(
        ...         abbreviation="VN-1",
        ...         count=18,
        ...         name="FirstViolin",
        ...     ),
        ...     baca.Section(
        ...         abbreviation="VN-2",
        ...         count=18,
        ...         name="SecondViolin",
        ...         ),
        ... )
        >>> len(part_manifest.parts)
        44

    ..  container:: example

        Makes parts on initialization:

        >>> part_manifest = baca.PartManifest(
        ...     baca.Part("BassClarinet"),
        ...     baca.Part("Violin"),
        ...     baca.Part("Viola"),
        ...     baca.Part("Cello"),
        ... )
        >>> for part in part_manifest.parts: part
        Part(name='BassClarinet', number=None)
        Part(name='Violin', number=None)
        Part(name='Viola', number=None)
        Part(name='Cello', number=None)

    ..  container:: example

        >>> part_manifest = baca.PartManifest(
        ...     baca.Section(
        ...         abbreviation="FL",
        ...         count=4,
        ...         name="Flute",
        ...     ),
        ...     baca.Section(
        ...         abbreviation="OB",
        ...         count=3,
        ...         name="Oboe",
        ...     ),
        ...     baca.Part("EnglishHorn"),
        ...     baca.Section(
        ...         abbreviation="VN-1",
        ...         count=18,
        ...         name="FirstViolin",
        ...     ),
        ...     baca.Section(
        ...         abbreviation="VN-2",
        ...         count=18,
        ...         name="SecondViolin",
        ...     ),
        ... )

        >>> for part in part_manifest.parts: part
        Part(name='Flute', number=1)
        Part(name='Flute', number=2)
        Part(name='Flute', number=3)
        Part(name='Flute', number=4)
        Part(name='Oboe', number=1)
        Part(name='Oboe', number=2)
        Part(name='Oboe', number=3)
        Part(name='EnglishHorn', number=None)
        Part(name='FirstViolin', number=1)
        Part(name='FirstViolin', number=2)
        Part(name='FirstViolin', number=3)
        Part(name='FirstViolin', number=4)
        Part(name='FirstViolin', number=5)
        Part(name='FirstViolin', number=6)
        Part(name='FirstViolin', number=7)
        Part(name='FirstViolin', number=8)
        Part(name='FirstViolin', number=9)
        Part(name='FirstViolin', number=10)
        Part(name='FirstViolin', number=11)
        Part(name='FirstViolin', number=12)
        Part(name='FirstViolin', number=13)
        Part(name='FirstViolin', number=14)
        Part(name='FirstViolin', number=15)
        Part(name='FirstViolin', number=16)
        Part(name='FirstViolin', number=17)
        Part(name='FirstViolin', number=18)
        Part(name='SecondViolin', number=1)
        Part(name='SecondViolin', number=2)
        Part(name='SecondViolin', number=3)
        Part(name='SecondViolin', number=4)
        Part(name='SecondViolin', number=5)
        Part(name='SecondViolin', number=6)
        Part(name='SecondViolin', number=7)
        Part(name='SecondViolin', number=8)
        Part(name='SecondViolin', number=9)
        Part(name='SecondViolin', number=10)
        Part(name='SecondViolin', number=11)
        Part(name='SecondViolin', number=12)
        Part(name='SecondViolin', number=13)
        Part(name='SecondViolin', number=14)
        Part(name='SecondViolin', number=15)
        Part(name='SecondViolin', number=16)
        Part(name='SecondViolin', number=17)
        Part(name='SecondViolin', number=18)

    ..  container:: example

        >>> baca.Part("FirstViolin",18) in part_manifest.parts
        True

        >>> baca.Part("FirstViolin", 19) in part_manifest.parts
        False

    ..  container:: example

        Makes sections at initialization:

        >>> part_manifest = baca.PartManifest(
        ...     baca.Part("BassClarinet"),
        ...     baca.Part("Violin"),
        ...     baca.Part("Viola"),
        ...     baca.Part("Cello"),
        ... )
        >>> part_manifest.sections
        []

        >>> part_manifest = baca.PartManifest(
        ...     baca.Section(
        ...         abbreviation="FL",
        ...         count=4,
        ...         name="Flute",
        ...     ),
        ...     baca.Section(
        ...         abbreviation="OB",
        ...         count=3,
        ...         name="Oboe",
        ...     ),
        ...     baca.Part("EnglishHorn"),
        ...     baca.Section(
        ...         abbreviation="VN-1",
        ...         count=18,
        ...         name="FirstViolin",
        ...     ),
        ...     baca.Section(
        ...         abbreviation="VN-2",
        ...         count=18,
        ...         name="SecondViolin",
        ...     ),
        ... )

        >>> for section in part_manifest.sections:
        ...     section
        ...
        Section(abbreviation='FL', count=4, name='Flute')
        Section(abbreviation='OB', count=3, name='Oboe')
        Section(abbreviation='VN-1', count=18, name='FirstViolin')
        Section(abbreviation='VN-2', count=18, name='SecondViolin')

        >>> section = baca.Section(
        ...     abbreviation="VN-1",
        ...     count=18,
        ...     name="FirstViolin",
        ... )
        >>> section in part_manifest.sections
        True

        >>> section = baca.Section(
        ...     abbreviation="VN-1",
        ...     count=36,
        ...     name="FirstViolin",
        ... )
        >>> section in part_manifest.sections
        False

    """

    __slots__ = ("parts", "sections")

    def __init__(self, *arguments):
        parts, sections = [], []
        for argument in arguments:
            if isinstance(argument, Part):
                parts.append(argument)
            elif isinstance(argument, Section):
                sections.append(argument)
                parts.extend(argument.parts())
            else:
                raise TypeError(f"must be part or section (not {argument}).")
        self.parts = parts
        self.sections = sections

    def __repr__(self):
        """
        Gets repr.
        """
        return f"{type(self).__name__}()"

    def expand(self, part_assignment):
        """
        Expands ``part_assignment``.

        ..  container:: example

            >>> part_manifest = baca.PartManifest(
            ...     baca.Section(
            ...         abbreviation="FL",
            ...         count=4,
            ...         name="Flute",
            ...     ),
            ...     baca.Section(
            ...         abbreviation="OB",
            ...         count=3,
            ...         name="Oboe",
            ...     ),
            ...     baca.Part("EnglishHorn"),
            ...     baca.Section(
            ...         abbreviation="VN-1",
            ...         count=18,
            ...         name="FirstViolin",
            ...     ),
            ...     baca.Section(
            ...         abbreviation="VN-2",
            ...         count=18,
            ...         name="SecondViolin",
            ...     ),
            ... )

            >>> part_assignment = baca.PartAssignment("Oboe")
            >>> for part in part_manifest.expand(part_assignment): part
            Part(name='Oboe', number=1)
            Part(name='Oboe', number=2)
            Part(name='Oboe', number=3)

        """
        assert isinstance(part_assignment, PartAssignment)
        parts = []
        for part in self.parts:
            if part.name == part_assignment.section:
                if part_assignment.token is None:
                    parts.append(part)
                elif part.number in part_assignment.members():
                    parts.append(part)
        return parts


def _global_rest_identifier(section_number):
    """
    Gets global rest identifier.

    ..  container:: example

        >>> baca.parts._global_rest_identifier("01")
        'section_number.01.Global.Rests'

        >>> baca.parts._global_rest_identifier("02")
        'section_number.02.Global.Rests'

    """
    identifier = f"section_number.{section_number}.Global.Rests"
    return identifier


def _import_score_package(contents_directory):
    assert contents_directory.name == contents_directory.parent.name
    try:
        module = importlib.import_module(contents_directory.name)
    except Exception:
        return
    return module


def _is_part_assignment_token(argument):
    if argument is None:
        return True
    if isinstance(argument, int) and 1 <= argument:
        return True
    if (
        isinstance(argument, tuple)
        and len(argument) == 2
        and isinstance(argument[0], int)
        and isinstance(argument[1], int)
    ):
        return True
    if isinstance(argument, list):
        for item in argument:
            if not isinstance(item, int):
                return False
            if not 1 <= item:
                return False
        return True
    return False


def _part_name_to_default_clef(path, part_name):
    contents_directory = _path.get_contents_directory(path)
    module = _import_score_package(contents_directory)
    library = getattr(module, "library")
    instruments = library.instruments
    words = abjad.string.delimit_words(part_name)
    if words[-1].isdigit():
        words = words[:-1]
    if words[0] in ("First", "Second"):
        words = words[1:]
    key = "".join(words)
    instrument = instruments.get(key, None)
    if not instrument:
        raise Exception(f"can not find {key!r}.")
    clef = abjad.Clef(instrument.clefs[0])
    return clef


def get_part_identifier(path):
    """
    Gets part identifier in layout.py only.
    """
    if not path.name.endswith("layout.py"):
        return None
    for line in path.read_text().split("\n"):
        if line.startswith("part_identifier ="):
            globals_ = globals()
            exec(line, globals_)
            part_identifier = globals_["part_identifier"]
            return part_identifier
    return None


def part_to_identifiers(path, part, container_to_part_assignment):
    """
    Changes ``part`` to (part container) identifiers (using
    ``container_to_part_assignment`` dictionary).
    """
    if not isinstance(part, Part):
        raise TypeError(f"must be part (not {part!r}).")
    identifiers = []
    default_clef = _part_name_to_default_clef(path, part.name)
    clef_string = default_clef._get_lilypond_format()
    assert clef_string.startswith("\\"), repr(clef_string)
    clef_string = clef_string[1:]
    identifiers.append(clef_string)
    dictionary = container_to_part_assignment
    if not dictionary:
        return "empty container-to-part-assignment dictionary"
    for i, (section_number, dictionary_) in enumerate(dictionary.items()):
        pairs = []
        for identifier, (part_assignment, timespan) in dictionary_.items():
            if part in part_assignment:
                pairs.append((identifier, timespan))
        if pairs:
            pairs.sort(key=lambda pair: pair[1])
            identifiers_ = [_[0] for _ in pairs]
            identifiers.extend(identifiers_)
        else:
            identifier = _global_rest_identifier(section_number)
            identifiers.append(identifier)
    return identifiers
