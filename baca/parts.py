"""
Parts.
"""
import importlib

import abjad

from . import path as _path


class Part:
    """
    Part.

    ..  container:: example

        >>> part = baca.Part(
        ...     member=18,
        ...     section="FirstViolin",
        ...     section_abbreviation="VN-1",
        ... )

        >>> string = abjad.storage(part)
        >>> print(string)
        baca.Part(
            instrument='FirstViolin',
            member=18,
            section='FirstViolin',
            section_abbreviation='VN-1',
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_section_abbreviation",
        "_instrument",
        "_member",
        "_name",
        "_number",
        "_section",
        "_zfill",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        instrument=None,
        member=None,
        number=None,
        section=None,
        section_abbreviation=None,
        zfill=None,
    ):
        instrument = instrument or section
        if instrument is not None:
            if not isinstance(instrument, str):
                raise Exception("instrument must be string (not {instrument!r}).")
        self._instrument = instrument
        if member is not None:
            if not isinstance(member, int):
                raise Exception("member must be integer (not {member!r}).")
        self._member = member
        if number is not None:
            assert isinstance(number, int), repr(number)
            assert 1 <= number, repr(number)
        self._number = number
        if section is not None:
            if not isinstance(section, str):
                raise Exception(f"section must be string (not {section!r}).")
        self._section = section
        if section_abbreviation is not None:
            if not isinstance(section_abbreviation, str):
                message = "section_abbreviation must be string"
                message += f" (not {section_abbreviation!r})."
                raise Exception(message)
        self._section_abbreviation = section_abbreviation
        if zfill is not None:
            assert isinstance(zfill, int), repr(zfill)
            assert 1 <= zfill, repr(zfill)
        self._zfill = zfill
        if member is not None:
            member_ = str(member)
            if self.zfill is not None:
                member_ = member_.zfill(self.zfill)
            name = f"{section}{member_}"
        else:
            name = section
        self._name = name

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a part with the same section and member as this
        part.

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

        """
        if isinstance(argument, type(self)):
            if argument.section == self.section:
                return argument.member == self.member
        return False

    def __hash__(self):
        """
        Hashes part.
        """
        return super().__hash__()

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return abjad.format.get_repr(self)

    ### PUBLIC PROPERTIES ###

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

    @property
    def instrument(self):
        """
        Gets instrument.

        ..  container:: example

            >>> part = baca.Part(
            ...     instrument="Violin",
            ...     member=18,
            ...     section="FirstViolin",
            ...     section_abbreviation="VN-1",
            ... )

            >>> part.instrument
            'Violin'

        """
        return self._instrument

    @property
    def member(self):
        """
        Gets member.

        ..  container:: example

            >>> part = baca.Part(
            ...     instrument="Violin",
            ...     member=18,
            ...     section="FirstViolin",
            ...     section_abbreviation="VN-1",
            ... )

            >>> part.member
            18

        """
        return self._member

    @property
    def name(self):
        """
        Gets name.

        ..  container:: example

            >>> part = baca.Part(
            ...     instrument="Violin",
            ...     member=1,
            ...     section="FirstViolin",
            ...     section_abbreviation="VN-1",
            ... )

            >>> part.name
            'FirstViolin1'

            >>> part = baca.Part(
            ...     instrument="Violin",
            ...     member=1,
            ...     zfill=2,
            ...     section="FirstViolin",
            ...     section_abbreviation="VN-1",
            ... )

            >>> part.name
            'FirstViolin01'

        """
        return self._name

    @property
    def number(self):
        """
        Gets number.

        ..  container:: example

            >>> part = baca.Part(
            ...     instrument="Violin",
            ...     member=18,
            ...     number=107,
            ...     section="FirstViolin",
            ...     section_abbreviation="VN-1",
            ... )

            >>> part.number
            107

        """
        return self._number

    @property
    def section(self):
        """
        Gets section.

        ..  container:: example

            >>> part = baca.Part(
            ...     instrument="Violin",
            ...     member=18,
            ...     section="FirstViolin",
            ...     section_abbreviation="VN-1",
            ... )

            >>> part.section
            'FirstViolin'

        """
        return self._section

    @property
    def section_abbreviation(self):
        """
        Gets section_abbreviation.

        ..  container:: example

            >>> part = baca.Part(
            ...     instrument="Violin",
            ...     member=18,
            ...     section="FirstViolin",
            ...     section_abbreviation="VN-1",
            ... )

            >>> part.section_abbreviation
            'VN-1'

        """
        return self._section_abbreviation

    @property
    def zfill(self):
        """
        Gets zfill.

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
        return self._zfill


class PartAssignment:
    """
    Part assignment.

    ..  container:: example

        >>> baca.PartAssignment("Horn")
        PartAssignment('Horn')

        >>> baca.PartAssignment("Horn", 1)
        PartAssignment('Horn', 1)

        >>> baca.PartAssignment("Horn", 2)
        PartAssignment('Horn', 2)

        >>> baca.PartAssignment("Horn", (3, 4))
        PartAssignment('Horn', (3, 4))

        >>> baca.PartAssignment("Horn", [1, 3])
        PartAssignment('Horn', [1, 3])

    ..  container:: example

        >>> part_assignment = baca.PartAssignment("Horn", [1, 3])

        >>> print(abjad.storage(part_assignment))
        baca.PartAssignment('Horn', [1, 3])

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_members", "_parts", "_section", "_token")

    ### INITIALIZER ###

    def __init__(self, section=None, token=None):
        self._section = section
        if token is not None:
            assert _is_part_assignment_token(token), repr(token)
        self._token = token
        members = _expand_members(token)
        self._members = members
        parts = self._expand_parts()
        assert isinstance(parts, list), repr(parts)
        self._parts = parts

    ### SPECIAL METHODS ###

    def __contains__(self, part: Part):
        """
        Is true when part assignment contains ``part``.

        ..  container:: example

            >>> parts = [
            ...     baca.Part(section="Horn", member= 1),
            ...     baca.Part(section="Horn", member= 2),
            ...     baca.Part(section="Horn", member= 3),
            ...     baca.Part(section="Horn", member= 4),
            ...     ]

            >>> part_assignment = baca.PartAssignment("Horn")
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, section='Horn'), True)
            (Part(instrument='Horn', member=2, section='Horn'), True)
            (Part(instrument='Horn', member=3, section='Horn'), True)
            (Part(instrument='Horn', member=4, section='Horn'), True)

            >>> part_assignment = baca.PartAssignment("Horn", 1)
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, section='Horn'), True)
            (Part(instrument='Horn', member=2, section='Horn'), False)
            (Part(instrument='Horn', member=3, section='Horn'), False)
            (Part(instrument='Horn', member=4, section='Horn'), False)

            >>> part_assignment = baca.PartAssignment("Horn", 2)
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, section='Horn'), False)
            (Part(instrument='Horn', member=2, section='Horn'), True)
            (Part(instrument='Horn', member=3, section='Horn'), False)
            (Part(instrument='Horn', member=4, section='Horn'), False)

            >>> part_assignment = baca.PartAssignment("Horn", (3, 4))
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, section='Horn'), False)
            (Part(instrument='Horn', member=2, section='Horn'), False)
            (Part(instrument='Horn', member=3, section='Horn'), True)
            (Part(instrument='Horn', member=4, section='Horn'), True)

            >>> part_assignment = baca.PartAssignment("Horn", [1, 3])
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, section='Horn'), True)
            (Part(instrument='Horn', member=2, section='Horn'), False)
            (Part(instrument='Horn', member=3, section='Horn'), True)
            (Part(instrument='Horn', member=4, section='Horn'), False)

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

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a part assignment with section and
        members equal to this part assignment.

        ..  container:: example

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

        """
        if isinstance(argument, type(self)):
            if argument.section == self.section:
                return argument.members == self.members
        return False

    def __hash__(self):
        """
        Hashes part assignment.
        """
        return super().__hash__()

    def __iter__(self):
        """
        Iterates parts in assignment.

        ..  container:: example

            >>> part_assignment = baca.PartAssignment("Horn", [1, 3])
            >>> for part in part_assignment:
            ...     part
            ...
            Part(instrument='Horn', member=1, section='Horn')
            Part(instrument='Horn', member=3, section='Horn')

        """
        return iter(self.parts)

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return abjad.format.get_repr(self)

    ### PRIVATE METHODS ###

    def _expand_parts(self):
        parts = []
        if self.members is None:
            parts.append(Part(section=self.section))
        else:
            for member in self.members:
                part = Part(member=member, section=self.section)
                parts.append(part)
        return parts

    def _get_format_specification(self):
        repr_args_values = [self.section]
        if self.token is not None:
            repr_args_values.append(self.token)
        repr_is_indented = False
        repr_keyword_names = []
        return abjad.FormatSpecification(
            repr_args_values=repr_args_values,
            repr_is_indented=repr_is_indented,
            repr_keyword_names=repr_keyword_names,
            storage_format_args_values=repr_args_values,
            storage_format_is_not_indented=not repr_is_indented,
            storage_format_keyword_names=repr_keyword_names,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def members(self):
        """
        Gets members.

        ..  container:: example

            >>> baca.PartAssignment("Horn").members is None
            True

            >>> baca.PartAssignment("Horn", 1).members
            [1]

            >>> baca.PartAssignment("Horn", 2).members
            [2]

            >>> baca.PartAssignment("Horn", (3, 4)).members
            [3, 4]

            >>> baca.PartAssignment("Horn", [1, 3]).members
            [1, 3]

        """
        return self._members

    @property
    def parts(self):
        """
        Gets parts.

        ..  container:: example

            >>> baca.PartAssignment("Horn").parts
            [Part(instrument='Horn', section='Horn')]

            >>> baca.PartAssignment("Horn", 1).parts
            [Part(instrument='Horn', member=1, section='Horn')]

            >>> baca.PartAssignment("Horn", 2).parts
            [Part(instrument='Horn', member=2, section='Horn')]

            >>> baca.PartAssignment("Horn", (3, 4)).parts
            [Part(instrument='Horn', member=3, section='Horn'), Part(instrument='Horn', member=4, section='Horn')]

            >>> baca.PartAssignment("Horn", [1, 3]).parts
            [Part(instrument='Horn', member=1, section='Horn'), Part(instrument='Horn', member=3, section='Horn')]

        """
        return self._parts

    @property
    def section(self):
        """
        Gets section.

        ..  container:: example

            >>> baca.PartAssignment("Horn").section
            'Horn'

            >>> baca.PartAssignment("Horn", 1).section
            'Horn'

            >>> baca.PartAssignment("Horn", 2).section
            'Horn'

            >>> baca.PartAssignment("Horn", (3, 4)).section
            'Horn'

            >>> baca.PartAssignment("Horn", [1, 3]).section
            'Horn'

        """
        return self._section

    @property
    def token(self):
        """
        Gets token.

        ..  container:: example

            >>> baca.PartAssignment("Horn").token is None
            True

            >>> baca.PartAssignment("Horn", 1).token
            1

            >>> baca.PartAssignment("Horn", 2).token
            2

            >>> baca.PartAssignment("Horn", (3, 4)).token
            (3, 4)

            >>> baca.PartAssignment("Horn", [1, 3]).token
            [1, 3]

        """
        return self._token


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

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_abbreviation", "_count", "_instrument", "_name", "_parts")

    ### INITIALIZER ###

    def __init__(
        self,
        abbreviation=None,
        count=1,
        instrument=None,
        name=None,
    ):
        if abbreviation is not None:
            assert isinstance(abbreviation, str), repr(abbreviation)
        self._abbreviation = abbreviation
        if not isinstance(count, int):
            raise Exception(f"Count must be integer (not {count!r}).")
        if not 1 <= count:
            raise Exception(f"Count must be positive (not {count!r}).")
        self._count = count
        if instrument is not None:
            assert isinstance(instrument, str), repr(instrument)
        else:
            instrument = name
        self._instrument = instrument
        if name is not None:
            assert isinstance(name, str), repr(name)
        self._name = name
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
        self._parts = parts

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a section with the same name, abbreviation and count
        as this section.

        ..  container:: example

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

        """
        if (
            isinstance(argument, type(self))
            and argument.name == self.name
            and argument.abbreviation == self.abbreviation
            and argument.count == self.count
        ):
            return True
        return False

    def __hash__(self):
        """
        Hashes section.
        """
        return super().__hash__()

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return abjad.format.get_repr(self)

    ### PUBLIC PROPERTIES ###

    @property
    def abbreviation(self):
        """
        Gets abbreviation.

        ..  container:: example

            >>> section = baca.Section(
            ...     abbreviation="VN-1",
            ...     count=18,
            ...     instrument="Violin",
            ...     name="FirstViolin",
            ... )

            >>> section.abbreviation
            'VN-1'

        """
        return self._abbreviation

    @property
    def count(self):
        """
        Gets section count.

        ..  container:: example

            >>> section = baca.Section(
            ...     abbreviation="VN-1",
            ...     count=18,
            ...     instrument="Violin",
            ...     name="FirstViolin",
            ... )

            >>> section.count
            18

        """
        return self._count

    @property
    def instrument(self):
        """
        Gets section instrument.

        ..  container:: example

            >>> section = baca.Section(
            ...     abbreviation="VN-1",
            ...     count=18,
            ...     instrument="Violin",
            ...     name="FirstViolin",
            ... )

            >>> section.instrument
            'Violin'

        """
        return self._instrument

    @property
    def name(self):
        """
        Gets section name.

        ..  container:: example

            >>> section = baca.Section(
            ...     abbreviation="VN-1",
            ...     count=18,
            ...     instrument="Violin",
            ...     name="FirstViolin",
            ... )

            >>> section.name
            'FirstViolin'

        """
        return self._name

    @property
    def parts(self):
        """
        Gets parts.

        ..  container:: example

            >>> section = baca.Section(
            ...     abbreviation="VN-1",
            ...     count=18,
            ...     instrument="Violin",
            ...     name="FirstViolin",
            ... )

            >>> for part in section.parts:
            ...     part
            ...
            Part(instrument='Violin', member=1, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=2, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=3, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=4, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=5, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=6, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=7, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=8, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=9, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=10, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=11, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=12, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=13, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=14, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=15, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=16, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=17, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=18, section='FirstViolin', section_abbreviation='VN-1', zfill=2)

        """
        return list(self._parts)


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

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_parts", "_sections")

    ### INITIALIZER ###

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
            part._number = number
        self._parts = parts
        self._sections = sections

    ### SPECIAL METHODS ###

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
            Part(instrument='Flute', member=1, number=1, section='Flute', section_abbreviation='FL')
            Part(instrument='Flute', member=2, number=2, section='Flute', section_abbreviation='FL')
            Part(instrument='Flute', member=3, number=3, section='Flute', section_abbreviation='FL')
            Part(instrument='Flute', member=4, number=4, section='Flute', section_abbreviation='FL')
            Part(instrument='Oboe', member=1, number=5, section='Oboe', section_abbreviation='OB')
            Part(instrument='Oboe', member=2, number=6, section='Oboe', section_abbreviation='OB')
            Part(instrument='Oboe', member=3, number=7, section='Oboe', section_abbreviation='OB')
            Part(instrument='EnglishHorn', number=8, section='EnglishHorn', section_abbreviation='EH')
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
        Gets interpreter representation.
        """
        return abjad.format.get_repr(self)

    ### PUBLIC PROPERTIES ###

    @property
    def parts(self):
        """
        Gets parts in manifest.

        ..  container:: example

            >>> part_manifest = baca.PartManifest(
            ...     baca.Part(section="BassClarinet", section_abbreviation="BCL"),
            ...     baca.Part(section="Violin", section_abbreviation="VN"),
            ...     baca.Part(section="Viola", section_abbreviation="VA"),
            ...     baca.Part(section="Cello", section_abbreviation="VC"),
            ... )
            >>> for part in part_manifest:
            ...     part
            ...
            Part(instrument='BassClarinet', number=1, section='BassClarinet', section_abbreviation='BCL')
            Part(instrument='Violin', number=2, section='Violin', section_abbreviation='VN')
            Part(instrument='Viola', number=3, section='Viola', section_abbreviation='VA')
            Part(instrument='Cello', number=4, section='Cello', section_abbreviation='VC')

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
            Part(instrument='Flute', member=1, number=1, section='Flute', section_abbreviation='FL')
            Part(instrument='Flute', member=2, number=2, section='Flute', section_abbreviation='FL')
            Part(instrument='Flute', member=3, number=3, section='Flute', section_abbreviation='FL')
            Part(instrument='Flute', member=4, number=4, section='Flute', section_abbreviation='FL')
            Part(instrument='Oboe', member=1, number=5, section='Oboe', section_abbreviation='OB')
            Part(instrument='Oboe', member=2, number=6, section='Oboe', section_abbreviation='OB')
            Part(instrument='Oboe', member=3, number=7, section='Oboe', section_abbreviation='OB')
            Part(instrument='EnglishHorn', number=8, section='EnglishHorn', section_abbreviation='EH')
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

        """
        return list(self._parts)

    @property
    def sections(self):
        """
        Gets sections in manifest.

        ..  container:: example

            >>> part_manifest = baca.PartManifest(
            ...     baca.Part(section="BassClarinet", section_abbreviation="BCL"),
            ...     baca.Part(section="Violin", section_abbreviation="VN"),
            ...     baca.Part(section="Viola", section_abbreviation="VA"),
            ...     baca.Part(section="Cello", section_abbreviation="VC"),
            ... )
            >>> part_manifest.sections
            []

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

            >>> for section in part_manifest.sections:
            ...     section
            ...
            Section(abbreviation='FL', count=4, instrument='Flute', name='Flute')
            Section(abbreviation='OB', count=3, instrument='Oboe', name='Oboe')
            Section(abbreviation='VN-1', count=18, instrument='Violin', name='FirstViolin')
            Section(abbreviation='VN-2', count=18, instrument='Violin', name='SecondViolin')

        ..  container:: example

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
        return list(self._sections)

    ### PUBLIC METHODS ###

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
            Part(instrument='Oboe', member=1, number=5, section='Oboe', section_abbreviation='OB')
            Part(instrument='Oboe', member=2, number=6, section='Oboe', section_abbreviation='OB')
            Part(instrument='Oboe', member=3, number=7, section='Oboe', section_abbreviation='OB')

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


def _global_rest_identifier(segment_number):
    """
    Gets global rest identifier.

    ..  container:: example

        >>> baca.parts._global_rest_identifier("01")
        'segment.01.Global.Rests'

        >>> baca.parts._global_rest_identifier("02")
        'segment.02.Global.Rests'

    """
    identifier = abjad.String(f"segment.{segment_number}.Global.Rests")
    assert "_" not in identifier, repr(identifier)
    return identifier


def _import_score_package(contents_directory):
    assert contents_directory.name == contents_directory.parent.name
    try:
        module = importlib.import_module(contents_directory.name)
    except Exception:
        return
    return module


def _import_score_template(contents_directory):
    assert contents_directory.name == contents_directory.parent.name
    module = _import_score_package(contents_directory)
    library = getattr(module, "library")
    score_template = library.ScoreTemplate
    return score_template


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
    words = abjad.String(part_name).delimit_words()
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
    for i, (segment_number, dictionary_) in enumerate(dictionary.items()):
        pairs = []
        for identifier, (part_assignment, timespan) in dictionary_.items():
            if part in part_assignment:
                pairs.append((identifier, timespan))
        if pairs:
            pairs.sort(key=lambda pair: pair[1])
            identifiers_ = [_[0] for _ in pairs]
            identifiers.extend(identifiers_)
        else:
            identifier = _global_rest_identifier(segment_number)
            identifiers.append(identifier)
    return identifiers
