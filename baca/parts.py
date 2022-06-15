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

        >>> part = baca.Part(
        ...     member=18,
        ...     section="FirstViolin",
        ... )

        >>> part
        Part(member=18, section='FirstViolin')

    ..  container:: example

        >>> part_1 = baca.Part(
        ...     member=18,
        ...     section="FirstViolin",
        ... )
        >>> part_2 = baca.Part(
        ...     member=18,
        ...     section="FirstViolin",
        ... )
        >>> part_3 = baca.Part(
        ...     member=18,
        ...     section="SecondViolin",
        ... )

        >>> part_1 == part_1
        True
        >>> part_1 == part_2
        True
        >>> part_1 == part_3
        False

        >>> part_2 == part_1
        True
        >>> part_2 == part_2
        True
        >>> part_2 == part_3
        False

        >>> part_3 == part_1
        False
        >>> part_3 == part_2
        False
        >>> part_3 == part_3
        True

    """

    member: typing.Any = None
    section: typing.Any = None

    def __post_init__(self):
        if self.member is not None:
            if not isinstance(self.member, int):
                raise Exception("member must be integer (not {self.member!r}).")
        if self.section is not None:
            if not isinstance(self.section, str):
                raise Exception(f"section must be string (not {self.section!r}).")

    def identifier(self):
        """
        Gets identifier.

        ..  container:: example

            >>> part = baca.Part(
            ...     member=18,
            ...     section="FirstViolin",
            ... )

            >>> part.identifier()
            'FirstViolin-18'

        """
        if self.member is None:
            return self.section
        else:
            assert isinstance(self.member, int)
            return f"{self.section}-{self.member}"

    def name(self):
        if self.member is not None:
            name = f"{self.section}{self.member}"
        else:
            name = self.section
        return name


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

    ..  container:: example

        >>> part_assignment_1 = baca.PartAssignment("Horn", (1, 2))
        >>> part_assignment_2 = baca.PartAssignment("Horn", [1, 2])
        >>> part_assignment_3 = baca.PartAssignment("Horn")

        >>> part_assignment_1 == part_assignment_1
        True
        >>> part_assignment_1 == part_assignment_2
        False
        >>> part_assignment_1 == part_assignment_3
        False

        >>> part_assignment_2 == part_assignment_1
        False
        >>> part_assignment_2 == part_assignment_2
        True
        >>> part_assignment_2 == part_assignment_3
        False

        >>> part_assignment_3 == part_assignment_1
        False
        >>> part_assignment_3 == part_assignment_2
        False
        >>> part_assignment_3 == part_assignment_3
        True

    """

    section: typing.Any = None
    token: typing.Any = None

    def __post_init__(self):
        assert _is_part_assignment_token(self.token), repr(self.token)

    def __contains__(self, part: Part):
        """
        Is true when part assignment contains ``part``.

        ..  container:: example

            >>> parts = [
            ...     baca.Part(section="Horn", member=1),
            ...     baca.Part(section="Horn", member=2),
            ...     baca.Part(section="Horn", member=3),
            ...     baca.Part(section="Horn", member=4),
            ... ]

            >>> part_assignment = baca.PartAssignment("Horn")
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(member=1, section='Horn'), True)
            (Part(member=2, section='Horn'), True)
            (Part(member=3, section='Horn'), True)
            (Part(member=4, section='Horn'), True)

            >>> part_assignment = baca.PartAssignment("Horn", 1)
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(member=1, section='Horn'), True)
            (Part(member=2, section='Horn'), False)
            (Part(member=3, section='Horn'), False)
            (Part(member=4, section='Horn'), False)

            >>> part_assignment = baca.PartAssignment("Horn", 2)
            >>> for part in parts: part
            Part(member=1, section='Horn')
            Part(member=2, section='Horn')
            Part(member=3, section='Horn')
            Part(member=4, section='Horn')

            >>> part_assignment = baca.PartAssignment("Horn", (3, 4))
            >>> for part in parts: part
            Part(member=1, section='Horn')
            Part(member=2, section='Horn')
            Part(member=3, section='Horn')
            Part(member=4, section='Horn')

            >>> part_assignment = baca.PartAssignment("Horn", [1, 3])
            >>> for part in parts: part
            Part(member=1, section='Horn')
            Part(member=2, section='Horn')
            Part(member=3, section='Horn')
            Part(member=4, section='Horn')

        """
        assert isinstance(part, Part), repr(part)
        members = self.members()
        if part.section == self.section:
            if (
                part.member is None
                or members is None
                or part.member in members
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
            parts.append(Part(section=self.section))
        else:
            for member in members:
                part = Part(member=member, section=self.section)
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
            Part(member=1, section='FirstViolin')
            Part(member=2, section='FirstViolin')
            Part(member=3, section='FirstViolin')
            Part(member=4, section='FirstViolin')
            Part(member=5, section='FirstViolin')
            Part(member=6, section='FirstViolin')
            Part(member=7, section='FirstViolin')
            Part(member=8, section='FirstViolin')
            Part(member=9, section='FirstViolin')
            Part(member=10, section='FirstViolin')
            Part(member=11, section='FirstViolin')
            Part(member=12, section='FirstViolin')
            Part(member=13, section='FirstViolin')
            Part(member=14, section='FirstViolin')
            Part(member=15, section='FirstViolin')
            Part(member=16, section='FirstViolin')
            Part(member=17, section='FirstViolin')
            Part(member=18, section='FirstViolin')

        """
        parts = []
        if self.count is None:
            part = Part(self.name)
            parts.append(part)
        else:
            for member in range(1, self.count + 1):
                part = Part(
                    member=member,
                    section=self.name,
                )
                parts.append(part)
        return parts


class PartManifest:
    """
    Part manifest.

    ..  container:: example

        Initializes from parts:

        >>> part_manifest = baca.PartManifest(
        ...     baca.Part(section="BassClarinet"),
        ...     baca.Part(section="Violin"),
        ...     baca.Part(section="Viola"),
        ...     baca.Part(section="Cello"),
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
        ...     baca.Part(
        ...         section="EnglishHorn",
        ...     ),
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
        ...     baca.Part(section="BassClarinet"),
        ...     baca.Part(section="Violin"),
        ...     baca.Part(section="Viola"),
        ...     baca.Part(section="Cello"),
        ... )
        >>> for part in part_manifest.parts: part
        Part(member=None, section='BassClarinet')
        Part(member=None, section='Violin')
        Part(member=None, section='Viola')
        Part(member=None, section='Cello')

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
        ...     baca.Part(
        ...         section="EnglishHorn",
        ...     ),
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
        Part(member=1, section='Flute')
        Part(member=2, section='Flute')
        Part(member=3, section='Flute')
        Part(member=4, section='Flute')
        Part(member=1, section='Oboe')
        Part(member=2, section='Oboe')
        Part(member=3, section='Oboe')
        Part(member=None, section='EnglishHorn')
        Part(member=1, section='FirstViolin')
        Part(member=2, section='FirstViolin')
        Part(member=3, section='FirstViolin')
        Part(member=4, section='FirstViolin')
        Part(member=5, section='FirstViolin')
        Part(member=6, section='FirstViolin')
        Part(member=7, section='FirstViolin')
        Part(member=8, section='FirstViolin')
        Part(member=9, section='FirstViolin')
        Part(member=10, section='FirstViolin')
        Part(member=11, section='FirstViolin')
        Part(member=12, section='FirstViolin')
        Part(member=13, section='FirstViolin')
        Part(member=14, section='FirstViolin')
        Part(member=15, section='FirstViolin')
        Part(member=16, section='FirstViolin')
        Part(member=17, section='FirstViolin')
        Part(member=18, section='FirstViolin')
        Part(member=1, section='SecondViolin')
        Part(member=2, section='SecondViolin')
        Part(member=3, section='SecondViolin')
        Part(member=4, section='SecondViolin')
        Part(member=5, section='SecondViolin')
        Part(member=6, section='SecondViolin')
        Part(member=7, section='SecondViolin')
        Part(member=8, section='SecondViolin')
        Part(member=9, section='SecondViolin')
        Part(member=10, section='SecondViolin')
        Part(member=11, section='SecondViolin')
        Part(member=12, section='SecondViolin')
        Part(member=13, section='SecondViolin')
        Part(member=14, section='SecondViolin')
        Part(member=15, section='SecondViolin')
        Part(member=16, section='SecondViolin')
        Part(member=17, section='SecondViolin')
        Part(member=18, section='SecondViolin')

    ..  container:: example

        >>> baca.Part(section="FirstViolin", member=18) in part_manifest.parts
        True

        >>> baca.Part(section="FirstViolin", member=19) in part_manifest.parts
        False

    ..  container:: example

        Makes sections at initialization:

        >>> part_manifest = baca.PartManifest(
        ...     baca.Part(section="BassClarinet"),
        ...     baca.Part(section="Violin"),
        ...     baca.Part(section="Viola"),
        ...     baca.Part(section="Cello"),
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
        ...     baca.Part(
        ...         section="EnglishHorn",
        ...     ),
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
            ...     baca.Part(
            ...         section="EnglishHorn",
            ...     ),
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
            Part(member=1, section='Oboe')
            Part(member=2, section='Oboe')
            Part(member=3, section='Oboe')

        """
        assert isinstance(part_assignment, PartAssignment)
        parts = []
        for part in self.parts:
            if part.section == part_assignment.section:
                if part_assignment.token is None:
                    parts.append(part)
                elif part.member in part_assignment.members():
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
