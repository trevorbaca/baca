"""
Parts.
"""
import dataclasses
import importlib
import typing

import abjad

from . import path as _path


# TODO: frozen=True
@dataclasses.dataclass(order=True, slots=True, unsafe_hash=True)
class Part:
    """
    Part.

    ..  container:: example

        >>> part = baca.Part(
        ...     member=18,
        ...     section="FirstViolin",
        ...     section_abbreviation="VN-1",
        ... )

        >>> part
        Part(instrument='FirstViolin', member=18, number=None, section='FirstViolin', section_abbreviation='VN-1', zfill=None)

    ..  container:: example

        >>> part_1 = baca.Part(
        ...     member=18,
        ...     section="FirstViolin",
        ...     section_abbreviation="VN-1",
        ... )
        >>> part_2 = baca.Part(
        ...     member=18,
        ...     section="FirstViolin",
        ...     section_abbreviation="VN-1",
        ... )
        >>> part_3 = baca.Part(
        ...     member=18,
        ...     section="SecondViolin",
        ...     section_abbreviation="VN-2",
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

    ..  container:: example

        >>> part = baca.Part(
        ...     instrument="Violin",
        ...     member=9,
        ...     number=99,
        ...     section="FirstViolin",
        ...     section_abbreviation="VN-1",
        ...     zfill=2,
        ... )

        >>> part.zfill
        2

        >>> str(part.member).zfill(part.zfill)
        '09'

    """

    instrument: typing.Any = dataclasses.field(compare=False, default=None)
    member: typing.Any = None
    name: str | None = dataclasses.field(compare=False, init=False, repr=False)
    number: typing.Any = dataclasses.field(compare=False, default=None)
    section: typing.Any = None
    section_abbreviation: typing.Any = dataclasses.field(compare=False, default=None)
    zfill: typing.Any = dataclasses.field(compare=False, default=None)

    def __post_init__(self):
        self.instrument = self.instrument or self.section
        if self.instrument is not None:
            if not isinstance(self.instrument, str):
                raise Exception("instrument must be string (not {self.instrument!r}).")
        if self.member is not None:
            if not isinstance(self.member, int):
                raise Exception("member must be integer (not {self.member!r}).")
        if self.number is not None:
            assert isinstance(self.number, int), repr(self.number)
            assert 1 <= self.number, repr(self.number)
        if self.section is not None:
            if not isinstance(self.section, str):
                raise Exception(f"section must be string (not {self.section!r}).")
        if self.section_abbreviation is not None:
            if not isinstance(self.section_abbreviation, str):
                message = "section_abbreviation must be string"
                message += f" (not {self.section_abbreviation!r})."
                raise Exception(message)
        if self.zfill is not None:
            assert isinstance(self.zfill, int), repr(self.zfill)
            assert 1 <= self.zfill, repr(self.zfill)
        if self.member is not None:
            member_ = str(self.member)
            if self.zfill is not None:
                member_ = member_.zfill(self.zfill)
            name = f"{self.section}{member_}"
        else:
            name = self.section
        self.name = name

    @property
    def identifier(self):
        """
        Gets identifier.

        ..  container:: example

            >>> part = baca.Part(
            ...     instrument="Violin",
            ...     member=18,
            ...     section="FirstViolin",
            ...     section_abbreviation="VN-1",
            ... )

            >>> part.identifier
            'VN-1-18'

        """
        assert isinstance(self.section_abbreviation, str)
        if self.member is None:
            return self.section_abbreviation
        else:
            assert isinstance(self.member, int)
            return f"{self.section_abbreviation}-{self.member}"


# TODO: frozen=True
@dataclasses.dataclass(order=True, slots=True, unsafe_hash=True)
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

        Compares ``section``, ``members``:

        >>> part_assignment_1 = baca.PartAssignment("Horn", (1, 2))
        >>> part_assignment_2 = baca.PartAssignment("Horn", [1, 2])
        >>> part_assignment_3 = baca.PartAssignment("Horn")

        >>> part_assignment_1 == part_assignment_1
        True
        >>> part_assignment_1 == part_assignment_2
        True
        >>> part_assignment_1 == part_assignment_3
        False

        >>> part_assignment_2 == part_assignment_1
        True
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

    ..  container:: example

        Expands parts on initialization:

        >>> baca.PartAssignment("Horn").parts
        [Part(instrument='Horn', member=None, number=None, section='Horn', section_abbreviation=None, zfill=None)]

        >>> baca.PartAssignment("Horn", 1).parts
        [Part(instrument='Horn', member=1, number=None, section='Horn', section_abbreviation=None, zfill=None)]

        >>> baca.PartAssignment("Horn", 2).parts
        [Part(instrument='Horn', member=2, number=None, section='Horn', section_abbreviation=None, zfill=None)]

        >>> baca.PartAssignment("Horn", (3, 4)).parts
        [Part(instrument='Horn', member=3, number=None, section='Horn', section_abbreviation=None, zfill=None), Part(instrument='Horn', member=4, number=None, section='Horn', section_abbreviation=None, zfill=None)]

        >>> baca.PartAssignment("Horn", [1, 3]).parts
        [Part(instrument='Horn', member=1, number=None, section='Horn', section_abbreviation=None, zfill=None), Part(instrument='Horn', member=3, number=None, section='Horn', section_abbreviation=None, zfill=None)]

    """

    members: typing.Any = dataclasses.field(init=False, repr=False)
    parts: typing.Any = dataclasses.field(compare=False, init=False, repr=False)
    section: typing.Any = None
    token: typing.Any = dataclasses.field(compare=False, default=None)

    def __post_init__(self):
        if self.token is not None:
            assert _is_part_assignment_token(self.token), repr(self.token)
        self.members = _expand_members(self.token)
        self.parts = self._expand_parts()
        assert isinstance(self.parts, list), repr(self.parts)

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
            (Part(instrument='Horn', member=1, number=None, section='Horn', section_abbreviation=None, zfill=None), True)
            (Part(instrument='Horn', member=2, number=None, section='Horn', section_abbreviation=None, zfill=None), True)
            (Part(instrument='Horn', member=3, number=None, section='Horn', section_abbreviation=None, zfill=None), True)
            (Part(instrument='Horn', member=4, number=None, section='Horn', section_abbreviation=None, zfill=None), True)

            >>> part_assignment = baca.PartAssignment("Horn", 1)
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, number=None, section='Horn', section_abbreviation=None, zfill=None), True)
            (Part(instrument='Horn', member=2, number=None, section='Horn', section_abbreviation=None, zfill=None), False)
            (Part(instrument='Horn', member=3, number=None, section='Horn', section_abbreviation=None, zfill=None), False)
            (Part(instrument='Horn', member=4, number=None, section='Horn', section_abbreviation=None, zfill=None), False)

            >>> part_assignment = baca.PartAssignment("Horn", 2)
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, number=None, section='Horn', section_abbreviation=None, zfill=None), False)
            (Part(instrument='Horn', member=2, number=None, section='Horn', section_abbreviation=None, zfill=None), True)
            (Part(instrument='Horn', member=3, number=None, section='Horn', section_abbreviation=None, zfill=None), False)
            (Part(instrument='Horn', member=4, number=None, section='Horn', section_abbreviation=None, zfill=None), False)

            >>> part_assignment = baca.PartAssignment("Horn", (3, 4))
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, number=None, section='Horn', section_abbreviation=None, zfill=None), False)
            (Part(instrument='Horn', member=2, number=None, section='Horn', section_abbreviation=None, zfill=None), False)
            (Part(instrument='Horn', member=3, number=None, section='Horn', section_abbreviation=None, zfill=None), True)
            (Part(instrument='Horn', member=4, number=None, section='Horn', section_abbreviation=None, zfill=None), True)

            >>> part_assignment = baca.PartAssignment("Horn", [1, 3])
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, number=None, section='Horn', section_abbreviation=None, zfill=None), True)
            (Part(instrument='Horn', member=2, number=None, section='Horn', section_abbreviation=None, zfill=None), False)
            (Part(instrument='Horn', member=3, number=None, section='Horn', section_abbreviation=None, zfill=None), True)
            (Part(instrument='Horn', member=4, number=None, section='Horn', section_abbreviation=None, zfill=None), False)

        ..  container:: example

            Raises exception when input is not part:

            >>> part_assignment = baca.PartAssignment("Horn")
            >>> "Horn" in part_assignment
            Traceback (most recent call last):
                ...
            TypeError: must be part (not 'Horn').

        """
        if not isinstance(part, Part):
            raise TypeError(f"must be part (not {part!r}).")
        if part.section == self.section:
            if (
                part.member is None
                or self.members is None
                or part.member in self.members
                or []
            ):
                return True
            return False
        return False

    def __iter__(self):
        """
        Iterates parts in assignment.

        ..  container:: example

            >>> part_assignment = baca.PartAssignment("Horn", [1, 3])
            >>> for part in part_assignment:
            ...     part
            ...
            Part(instrument='Horn', member=1, number=None, section='Horn', section_abbreviation=None, zfill=None)
            Part(instrument='Horn', member=3, number=None, section='Horn', section_abbreviation=None, zfill=None)

        """
        return iter(self.parts)

    def _expand_parts(self):
        parts = []
        if self.members is None:
            parts.append(Part(section=self.section))
        else:
            for member in self.members:
                part = Part(member=member, section=self.section)
                parts.append(part)
        return parts

    def __repr__(self):
        """
        Custom repr for __persist__ files.
        """
        if self.token is not None:
            return f"baca.{type(self).__name__}({self.section!r}, {self.token!r})"
        else:
            return f"baca.{type(self).__name__}({self.section!r})"


# TODO: frozen=True
@dataclasses.dataclass(order=True, slots=True, unsafe_hash=True)
class Section:
    """
    Section.

    ..  container:: example

        >>> baca.Section(
        ...     abbreviation="VN-1",
        ...     count=18,
        ...     instrument="Violin",
        ...     name="FirstViolin",
        ... )
        Section(abbreviation='VN-1', count=18, instrument='Violin', name='FirstViolin')

        >>> baca.Section(
        ...     abbreviation="VN-2",
        ...     count=18,
        ...     instrument="Violin",
        ...     name="SecondViolin",
        ... )
        Section(abbreviation='VN-2', count=18, instrument='Violin', name='SecondViolin')

        >>> baca.Section(
        ...     abbreviation="VA",
        ...     count=18,
        ...     name="Viola",
        ... )
        Section(abbreviation='VA', count=18, instrument='Viola', name='Viola')

        >>> baca.Section(
        ...     abbreviation="VC",
        ...     count=14,
        ...     name="Cello",
        ... )
        Section(abbreviation='VC', count=14, instrument='Cello', name='Cello')

        >>> baca.Section(
        ...     abbreviation="CB",
        ...     count=6,
        ...     name="Contrabass",
        ... )
        Section(abbreviation='CB', count=6, instrument='Contrabass', name='Contrabass')

    ..  container:: example

        Compares ``name``, ``abbreviation``, ``count``:

        >>> section_1 = baca.Section(
        ...     abbreviation="VN-1",
        ...     count=18,
        ...     instrument="Violin",
        ...     name="FirstViolin",
        ... )
        >>> section_2 = baca.Section(
        ...     abbreviation="VN-1",
        ...     count=18,
        ...     instrument="Violin",
        ...     name="FirstViolin",
        ... )
        >>> section_3 = baca.Section(
        ...     abbreviation="VN-2",
        ...     count=18,
        ...     instrument="Violin",
        ...     name="SecondViolin",
        ... )

        >>> section_1 == section_1
        True
        >>> section_1 == section_2
        True
        >>> section_1 == section_3
        False

        >>> section_2 == section_1
        True
        >>> section_2 == section_2
        True
        >>> section_2 == section_3
        False

        >>> section_3 == section_1
        False
        >>> section_3 == section_2
        False
        >>> section_3 == section_3
        True


    ..  container:: example

        Makes parts at initialization:

        >>> section = baca.Section(
        ...     abbreviation="VN-1",
        ...     count=18,
        ...     instrument="Violin",
        ...     name="FirstViolin",
        ... )

        >>> for part in section.parts:
        ...     part
        ...
        Part(instrument='Violin', member=1, number=None, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=2, number=None, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=3, number=None, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=4, number=None, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=5, number=None, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=6, number=None, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=7, number=None, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=8, number=None, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=9, number=None, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=10, number=None, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=11, number=None, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=12, number=None, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=13, number=None, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=14, number=None, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=15, number=None, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=16, number=None, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=17, number=None, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=18, number=None, section='FirstViolin', section_abbreviation='VN-1', zfill=2)

    """

    abbreviation: typing.Any = None
    count: int = 1
    instrument: typing.Any = dataclasses.field(compare=False, default=None)
    name: typing.Any = None
    parts: typing.Any = dataclasses.field(
        compare=False, default=None, init=False, repr=False
    )

    def __post_init__(self):
        if self.abbreviation is not None:
            assert isinstance(self.abbreviation, str), repr(self.abbreviation)
        if not isinstance(self.count, int):
            raise Exception(f"Count must be integer (not {self.count!r}).")
        if not 1 <= self.count:
            raise Exception(f"Count must be positive (not {self.count!r}).")
        if self.instrument is not None:
            assert isinstance(self.instrument, str), repr(self.instrument)
        else:
            self.instrument = self.name
        if self.name is not None:
            assert isinstance(self.name, str), repr(self.name)
        parts = []
        if self.count is None:
            part = Part(self.name)
            parts.append(part)
        else:
            if 1 < len(str(self.count)):
                zfill = len(str(self.count))
            else:
                zfill = None
            for member in range(1, self.count + 1):
                part = Part(
                    member=member,
                    instrument=self.instrument,
                    section=self.name,
                    section_abbreviation=self.abbreviation,
                    zfill=zfill,
                )
                parts.append(part)
        self.parts = parts


class PartManifest:
    """
    Part manifest.

    ..  container:: example

        Initializes from parts:

        >>> part_manifest = baca.PartManifest(
        ...     baca.Part(section="BassClarinet", section_abbreviation="BCL"),
        ...     baca.Part(section="Violin", section_abbreviation="VN"),
        ...     baca.Part(section="Viola", section_abbreviation="VA"),
        ...     baca.Part(section="Cello", section_abbreviation="VC"),
        ... )
        >>> len(part_manifest)
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
        ...         section_abbreviation="EH",
        ...         section="EnglishHorn",
        ...     ),
        ...     baca.Section(
        ...         abbreviation="VN-1",
        ...         count=18,
        ...         instrument="Violin",
        ...         name="FirstViolin",
        ...     ),
        ...     baca.Section(
        ...         abbreviation="VN-2",
        ...         count=18,
        ...         instrument="Violin",
        ...         name="SecondViolin",
        ...         ),
        ... )
        >>> len(part_manifest)
        44

    ..  container:: example

        Makes parts on initialization:

        >>> part_manifest = baca.PartManifest(
        ...     baca.Part(section="BassClarinet", section_abbreviation="BCL"),
        ...     baca.Part(section="Violin", section_abbreviation="VN"),
        ...     baca.Part(section="Viola", section_abbreviation="VA"),
        ...     baca.Part(section="Cello", section_abbreviation="VC"),
        ... )
        >>> for part in part_manifest.parts:
        ...     part
        ...
        Part(instrument='BassClarinet', member=None, number=1, section='BassClarinet', section_abbreviation='BCL', zfill=None)
        Part(instrument='Violin', member=None, number=2, section='Violin', section_abbreviation='VN', zfill=None)
        Part(instrument='Viola', member=None, number=3, section='Viola', section_abbreviation='VA', zfill=None)
        Part(instrument='Cello', member=None, number=4, section='Cello', section_abbreviation='VC', zfill=None)

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
        ...         section_abbreviation="EH",
        ...         section="EnglishHorn",
        ...     ),
        ...     baca.Section(
        ...         abbreviation="VN-1",
        ...         count=18,
        ...         instrument="Violin",
        ...         name="FirstViolin",
        ...     ),
        ...     baca.Section(
        ...         abbreviation="VN-2",
        ...         count=18,
        ...         instrument="Violin",
        ...         name="SecondViolin",
        ...     ),
        ... )

        >>> for part in part_manifest.parts:
        ...     part
        ...
        Part(instrument='Flute', member=1, number=1, section='Flute', section_abbreviation='FL', zfill=None)
        Part(instrument='Flute', member=2, number=2, section='Flute', section_abbreviation='FL', zfill=None)
        Part(instrument='Flute', member=3, number=3, section='Flute', section_abbreviation='FL', zfill=None)
        Part(instrument='Flute', member=4, number=4, section='Flute', section_abbreviation='FL', zfill=None)
        Part(instrument='Oboe', member=1, number=5, section='Oboe', section_abbreviation='OB', zfill=None)
        Part(instrument='Oboe', member=2, number=6, section='Oboe', section_abbreviation='OB', zfill=None)
        Part(instrument='Oboe', member=3, number=7, section='Oboe', section_abbreviation='OB', zfill=None)
        Part(instrument='EnglishHorn', member=None, number=8, section='EnglishHorn', section_abbreviation='EH', zfill=None)
        Part(instrument='Violin', member=1, number=9, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=2, number=10, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=3, number=11, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=4, number=12, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=5, number=13, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=6, number=14, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=7, number=15, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=8, number=16, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=9, number=17, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=10, number=18, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=11, number=19, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=12, number=20, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=13, number=21, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=14, number=22, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=15, number=23, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=16, number=24, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=17, number=25, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=18, number=26, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
        Part(instrument='Violin', member=1, number=27, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
        Part(instrument='Violin', member=2, number=28, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
        Part(instrument='Violin', member=3, number=29, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
        Part(instrument='Violin', member=4, number=30, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
        Part(instrument='Violin', member=5, number=31, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
        Part(instrument='Violin', member=6, number=32, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
        Part(instrument='Violin', member=7, number=33, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
        Part(instrument='Violin', member=8, number=34, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
        Part(instrument='Violin', member=9, number=35, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
        Part(instrument='Violin', member=10, number=36, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
        Part(instrument='Violin', member=11, number=37, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
        Part(instrument='Violin', member=12, number=38, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
        Part(instrument='Violin', member=13, number=39, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
        Part(instrument='Violin', member=14, number=40, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
        Part(instrument='Violin', member=15, number=41, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
        Part(instrument='Violin', member=16, number=42, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
        Part(instrument='Violin', member=17, number=43, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
        Part(instrument='Violin', member=18, number=44, section='SecondViolin', section_abbreviation='VN-2', zfill=2)

    ..  container:: example

        >>> baca.Part(section='FirstViolin', member=18) in part_manifest.parts
        True

        >>> baca.Part(section='FirstViolin', member=19) in part_manifest.parts
        False

    ..  container:: example

        Makes sections at initialization:

        >>> part_manifest = baca.PartManifest(
        ...     baca.Part(section="BassClarinet", section_abbreviation="BCL"),
        ...     baca.Part(section="Violin", section_abbreviation="VN"),
        ...     baca.Part(section="Viola", section_abbreviation="VA"),
        ...     baca.Part(section="Cello", section_abbreviation="VC"),
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
        ...         section_abbreviation="EH",
        ...         section="EnglishHorn",
        ...     ),
        ...     baca.Section(
        ...         abbreviation="VN-1",
        ...         count=18,
        ...         instrument="Violin",
        ...         name="FirstViolin",
        ...     ),
        ...     baca.Section(
        ...         abbreviation="VN-2",
        ...         count=18,
        ...         instrument="Violin",
        ...         name="SecondViolin",
        ...     ),
        ... )

        >>> for section in part_manifest.sections:
        ...     section
        ...
        Section(abbreviation='FL', count=4, instrument='Flute', name='Flute')
        Section(abbreviation='OB', count=3, instrument='Oboe', name='Oboe')
        Section(abbreviation='VN-1', count=18, instrument='Violin', name='FirstViolin')
        Section(abbreviation='VN-2', count=18, instrument='Violin', name='SecondViolin')

        >>> section = baca.Section(
        ...     abbreviation="VN-1",
        ...     count=18,
        ...     instrument="Violin",
        ...     name="FirstViolin",
        ... )
        >>> section in part_manifest.sections
        True

        >>> section = baca.Section(
        ...     abbreviation="VN-1",
        ...     count=36,
        ...     instrument="Violin",
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
                parts.extend(argument.parts)
            else:
                raise TypeError(f"must be part or section (not {argument}).")
        for i, part in enumerate(parts):
            number = i + 1
            part.number = number
        self.parts = parts
        self.sections = sections

    # TODO: eliminate in favor of PartManifest.parts
    def __iter__(self):
        """
        Iterates parts in manifest.

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
            ...         section_abbreviation="EH",
            ...         section="EnglishHorn",
            ...     ),
            ...     baca.Section(
            ...         abbreviation="VN-1",
            ...         count=18,
            ...         instrument="Violin",
            ...         name="FirstViolin",
            ...     ),
            ...     baca.Section(
            ...         abbreviation="VN-2",
            ...         count=18,
            ...         instrument="Violin",
            ...         name="SecondViolin",
            ...     ),
            ... )

            >>> for part in part_manifest:
            ...     part
            ...
            Part(instrument='Flute', member=1, number=1, section='Flute', section_abbreviation='FL', zfill=None)
            Part(instrument='Flute', member=2, number=2, section='Flute', section_abbreviation='FL', zfill=None)
            Part(instrument='Flute', member=3, number=3, section='Flute', section_abbreviation='FL', zfill=None)
            Part(instrument='Flute', member=4, number=4, section='Flute', section_abbreviation='FL', zfill=None)
            Part(instrument='Oboe', member=1, number=5, section='Oboe', section_abbreviation='OB', zfill=None)
            Part(instrument='Oboe', member=2, number=6, section='Oboe', section_abbreviation='OB', zfill=None)
            Part(instrument='Oboe', member=3, number=7, section='Oboe', section_abbreviation='OB', zfill=None)
            Part(instrument='EnglishHorn', member=None, number=8, section='EnglishHorn', section_abbreviation='EH', zfill=None)
            Part(instrument='Violin', member=1, number=9, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=2, number=10, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=3, number=11, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=4, number=12, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=5, number=13, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=6, number=14, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=7, number=15, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=8, number=16, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=9, number=17, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=10, number=18, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=11, number=19, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=12, number=20, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=13, number=21, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=14, number=22, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=15, number=23, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=16, number=24, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=17, number=25, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=18, number=26, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=1, number=27, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=2, number=28, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=3, number=29, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=4, number=30, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=5, number=31, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=6, number=32, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=7, number=33, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=8, number=34, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=9, number=35, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=10, number=36, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=11, number=37, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=12, number=38, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=13, number=39, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=14, number=40, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=15, number=41, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=16, number=42, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=17, number=43, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=18, number=44, section='SecondViolin', section_abbreviation='VN-2', zfill=2)

        """
        return iter(self.parts)

    # TODO: eliminate in favor of PartManifest.parts
    def __len__(self):
        """
        Gets number of parts in manifest.

        ..  container:: example

            >>> part_manifest = baca.PartManifest(
            ...     baca.Part(section="BassClarinet", section_abbreviation="BCL"),
            ...     baca.Part(section="Violin", section_abbreviation="VN"),
            ...     baca.Part(section="Viola", section_abbreviation="VA"),
            ...     baca.Part(section="Cello", section_abbreviation="VC"),
            ... )
            >>> len(part_manifest)
            4

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
            ...         section_abbreviation="EH",
            ...         section="EnglishHorn",
            ...     ),
            ...     baca.Section(
            ...         abbreviation="VN-1",
            ...         count=18,
            ...         instrument="Violin",
            ...         name="FirstViolin",
            ...     ),
            ...     baca.Section(
            ...         abbreviation="VN-2",
            ...         count=18,
            ...         instrument="Violin",
            ...         name="SecondViolin",
            ...     ),
            ... )

            >>> len(part_manifest)
            44

        """
        return len(self.parts)

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
            ...         section_abbreviation="EH",
            ...         section="EnglishHorn",
            ...     ),
            ...     baca.Section(
            ...         abbreviation="VN-1",
            ...         count=18,
            ...         instrument="Violin",
            ...         name="FirstViolin",
            ...     ),
            ...     baca.Section(
            ...         abbreviation="VN-2",
            ...         count=18,
            ...         instrument="Violin",
            ...         name="SecondViolin",
            ...     ),
            ... )

            >>> part_assignment = baca.PartAssignment("Oboe")
            >>> for part in part_manifest.expand(part_assignment):
            ...     part
            ...
            Part(instrument='Oboe', member=1, number=5, section='Oboe', section_abbreviation='OB', zfill=None)
            Part(instrument='Oboe', member=2, number=6, section='Oboe', section_abbreviation='OB', zfill=None)
            Part(instrument='Oboe', member=3, number=7, section='Oboe', section_abbreviation='OB', zfill=None)

        """
        assert isinstance(part_assignment, PartAssignment)
        parts = []
        for part in self.parts:
            if part.section == part_assignment.section:
                if part_assignment.token is None:
                    parts.append(part)
                elif part.member in part_assignment.members:
                    parts.append(part)
        return parts


def _expand_members(token):
    if token is None:
        return
    members = []
    if isinstance(token, int):
        members.append(token)
    elif isinstance(token, tuple):
        assert len(token) == 2, repr(token)
        for member in range(token[0], token[1] + 1):
            members.append(member)
    else:
        assert isinstance(token, list), repr(token)
        members.extend(token)
    return members


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
    clef = abjad.Clef(instrument.allowable_clefs[0])
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
