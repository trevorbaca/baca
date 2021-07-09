import importlib
import pathlib

import abjad


class Job:
    """
    Job.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_activate",
        "_deactivate",
        "_deactivate_first",
        "_message_zero",
        "_path",
        "_prepend_empty_chord",
        "_skip_file_name",
        "_title",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        activate=None,
        deactivate=None,
        deactivate_first=None,
        message_zero=None,
        path=None,
        prepend_empty_chord=None,
        skip_file_name=None,
        title=None,
    ):
        self._activate = activate
        self._deactivate = deactivate
        self._deactivate_first = deactivate_first
        self._message_zero = message_zero
        self._path = path
        self._prepend_empty_chord = prepend_empty_chord
        self._skip_file_name = skip_file_name
        self._title = title

    ### SPECIAL METHODS ###

    def __call__(self):
        """
        Calls job on job ``path``.
        """
        messages = []
        if self.title is not None:
            messages.append(abjad.String(self.title).capitalize_start())
        total_count = 0
        if isinstance(self.path, str):
            text = self.path
        if self.deactivate_first is True:
            if self.deactivate is not None:
                assert isinstance(self.deactivate, tuple)
                match, name = self.deactivate
                if match is not None:
                    if isinstance(self.path, pathlib.Path):
                        result = self.path.deactivate(
                            match,
                            message_zero=True,
                            name=name,
                            prepend_empty_chord=self.prepend_empty_chord,
                            skip_file_name=self.skip_file_name,
                        )
                        assert result is not None
                        count, skipped, messages_ = result
                        messages.extend(messages_)
                        total_count += count
                    else:
                        assert isinstance(self.path, str), repr(self.path)
                        result = abjad.deactivate(
                            text,
                            match,
                            prepend_empty_chord=self.prepend_empty_chord,
                            skip_file_name=self.skip_file_name,
                            skipped=True,
                        )
                        assert result is not None
                        text, count, skipped = result
        if self.activate is not None:
            assert isinstance(self.activate, tuple)
            match, name = self.activate
            if match is not None:
                if isinstance(self.path, pathlib.Path):
                    result = self.path.activate(
                        match,
                        message_zero=True,
                        name=name,
                        skip_file_name=self.skip_file_name,
                    )
                    assert result is not None
                    count, skipped, messages_ = result
                    messages.extend(messages_)
                    total_count += count
                else:
                    assert isinstance(self.path, str)
                    text, count, skipped = abjad.activate(
                        text,
                        match,
                        skip_file_name=self.skip_file_name,
                        skipped=True,
                    )
        if self.deactivate_first is not True:
            if self.deactivate is not None:
                assert isinstance(self.deactivate, tuple)
                match, name = self.deactivate
                if match is not None:
                    if isinstance(self.path, pathlib.Path):
                        result = self.path.deactivate(
                            match,
                            message_zero=True,
                            name=name,
                            prepend_empty_chord=self.prepend_empty_chord,
                            skip_file_name=self.skip_file_name,
                        )
                        assert result is not None
                        count, skipped, messages_ = result
                        messages.extend(messages_)
                        total_count += count
                    else:
                        assert isinstance(self.path, str)
                        text, count, skipped = abjad.deactivate(
                            text,
                            match,
                            prepend_empty_chord=self.prepend_empty_chord,
                            skip_file_name=self.skip_file_name,
                            skipped=True,
                        )
        if total_count == 0 and not self.message_zero:
            messages = []
        if isinstance(self.path, pathlib.Path):
            return messages
        else:
            assert isinstance(self.path, str)
            return text

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def activate(self):
        """
        Gets activate match / message pair.
        """
        return self._activate

    @property
    def deactivate(self):
        """
        Gets deactivate match / message pair.
        """
        return self._deactivate

    @property
    def deactivate_first(self):
        """
        Is true when deactivate runs first.
        """
        return self._deactivate_first

    @property
    def message_zero(self):
        """
        Is true when job returns messages even when no matches are found.
        """
        return self._message_zero

    @property
    def path(self):
        """
        Gets path.
        """
        return self._path

    @property
    def prepend_empty_chord(self):
        """
        Is true when deactivate prepends LilyPond empty chord ``<>`` command.
        """
        return self._prepend_empty_chord

    @property
    def skip_file_name(self):
        """
        Gets skip file name.
        """
        return self._skip_file_name

    @property
    def title(self):
        """
        Gets title.
        """
        return self._title


class Momento:
    """
    Momento.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_context",
        "_edition",
        "_manifest",
        "_prototype",
        "_synthetic_offset",
        "_value",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        context=None,
        edition=None,
        manifest=None,
        prototype=None,
        synthetic_offset=None,
        value=None,
    ):
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        edition_ = None
        if edition is not None:
            edition_ = abjad.Tag(edition)
        self._edition = edition_
        if manifest is not None:
            assert isinstance(manifest, str), repr(manifest)
            assert prototype is None
        self._manifest = manifest
        if prototype is not None:
            assert isinstance(prototype, str), repr(prototype)
            assert manifest is None
        self._prototype = prototype
        if synthetic_offset is not None:
            assert isinstance(synthetic_offset, abjad.Offset), repr(synthetic_offset)
        self._synthetic_offset = synthetic_offset
        if value is not None:
            if not isinstance(value, (int, str, dict)):
                assert type(value).__name__ == "PersistentOverride", repr(value)
        self._value = value

    ### SPECIAL METHODS ###

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS###

    def _get_format_specification(self):
        return abjad.FormatSpecification(client=self)

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        """
        Gets (name of local) context.
        """
        return self._context

    @property
    def edition(self):
        """
        Gets edition.
        """
        return self._edition

    @property
    def manifest(self):
        """
        Gets manifest.
        """
        return self._manifest

    @property
    def prototype(self):
        """
        Gets prototype.
        """
        return self._prototype

    @property
    def synthetic_offset(self):
        """
        Gets synthetic offset.
        """
        return self._synthetic_offset

    @property
    def value(self):
        """
        Gets value.
        """
        return self._value


class Part:
    """
    Part.

    ..  container:: example

        >>> part = baca.Part(
        ...     member=18,
        ...     section='FirstViolin',
        ...     section_abbreviation='VN-1',
        ...     )

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
                message = "instrument must be string"
                message += f" (not {instrument!r})."
                raise Exception(message)
        self._instrument = instrument
        if member is not None:
            if not isinstance(member, int):
                message = "member must be integer"
                message += f" (not {member!r})."
                raise Exception(message)
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
        Is true when ``argument`` is a part with the same section and
        member as this part.

        ..  container:: example

            >>> part_1 = baca.Part(
            ...     member=18,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )
            >>> part_2 = baca.Part(
            ...     member=18,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )
            >>> part_3 = baca.Part(
            ...     member=18,
            ...     section='SecondViolin',
            ...     section_abbreviation='VN-2',
            ...     )

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
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def identifier(self):
        """
        Gets identifier.

        ..  container:: example

            >>> part = baca.Part(
            ...     instrument='Violin',
            ...     member=18,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

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
            ...     instrument='Violin',
            ...     member=18,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

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
            ...     instrument='Violin',
            ...     member=18,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

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
            ...     instrument='Violin',
            ...     member=1,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

            >>> part.name
            'FirstViolin1'

            >>> part = baca.Part(
            ...     instrument='Violin',
            ...     member=1,
            ...     zfill=2,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

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
            ...     instrument='Violin',
            ...     member=18,
            ...     number=107,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

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
            ...     instrument='Violin',
            ...     member=18,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

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
            ...     instrument='Violin',
            ...     member=18,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

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
            ...     instrument='Violin',
            ...     member=9,
            ...     number=99,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     zfill=2,
            ...     )

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

        >>> baca.PartAssignment('Horn')
        PartAssignment('Horn')

        >>> baca.PartAssignment('Horn', 1)
        PartAssignment('Horn', 1)

        >>> baca.PartAssignment('Horn', 2)
        PartAssignment('Horn', 2)

        >>> baca.PartAssignment('Horn', (3, 4))
        PartAssignment('Horn', (3, 4))

        >>> baca.PartAssignment('Horn', [1, 3])
        PartAssignment('Horn', [1, 3])

    ..  container:: example

        >>> part_assignment = baca.PartAssignment('Horn', [1, 3])

        >>> print(abjad.storage(part_assignment))
        baca.PartAssignment('Horn', [1, 3])

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_members", "_parts", "_section", "_token")

    ### INITIALIZER ###

    def __init__(self, section=None, token=None):
        self._section = section
        if token is not None:
            assert self._is_token(token), repr(token)
        self._token = token
        members = self._expand_members(token)
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
            ...     baca.Part(section='Horn', member= 1),
            ...     baca.Part(section='Horn', member= 2),
            ...     baca.Part(section='Horn', member= 3),
            ...     baca.Part(section='Horn', member= 4),
            ...     ]

            >>> part_assignment = baca.PartAssignment('Horn')
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, section='Horn'), True)
            (Part(instrument='Horn', member=2, section='Horn'), True)
            (Part(instrument='Horn', member=3, section='Horn'), True)
            (Part(instrument='Horn', member=4, section='Horn'), True)

            >>> part_assignment = baca.PartAssignment('Horn', 1)
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, section='Horn'), True)
            (Part(instrument='Horn', member=2, section='Horn'), False)
            (Part(instrument='Horn', member=3, section='Horn'), False)
            (Part(instrument='Horn', member=4, section='Horn'), False)

            >>> part_assignment = baca.PartAssignment('Horn', 2)
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, section='Horn'), False)
            (Part(instrument='Horn', member=2, section='Horn'), True)
            (Part(instrument='Horn', member=3, section='Horn'), False)
            (Part(instrument='Horn', member=4, section='Horn'), False)

            >>> part_assignment = baca.PartAssignment('Horn', (3, 4))
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, section='Horn'), False)
            (Part(instrument='Horn', member=2, section='Horn'), False)
            (Part(instrument='Horn', member=3, section='Horn'), True)
            (Part(instrument='Horn', member=4, section='Horn'), True)

            >>> part_assignment = baca.PartAssignment('Horn', [1, 3])
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, section='Horn'), True)
            (Part(instrument='Horn', member=2, section='Horn'), False)
            (Part(instrument='Horn', member=3, section='Horn'), True)
            (Part(instrument='Horn', member=4, section='Horn'), False)

        ..  container:: example

            Raises exception when input is not part:

            >>> part_assignment = baca.PartAssignment('Horn')
            >>> 'Horn' in part_assignment
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

            >>> part_assignment_1 = baca.PartAssignment('Horn', (1, 2))
            >>> part_assignment_2 = baca.PartAssignment('Horn', [1, 2])
            >>> part_assignment_3 = baca.PartAssignment('Horn')

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

            >>> part_assignment = baca.PartAssignment('Horn', [1, 3])
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
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    @staticmethod
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
            self,
            repr_args_values=repr_args_values,
            repr_is_indented=repr_is_indented,
            repr_keyword_names=repr_keyword_names,
            storage_format_args_values=repr_args_values,
            storage_format_is_indented=repr_is_indented,
            storage_format_keyword_names=repr_keyword_names,
        )

    @staticmethod
    def _is_token(argument):
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

    ### PUBLIC PROPERTIES ###

    @property
    def members(self):
        """
        Gets members.

        ..  container:: example

            >>> baca.PartAssignment('Horn').members is None
            True

            >>> baca.PartAssignment('Horn', 1).members
            [1]

            >>> baca.PartAssignment('Horn', 2).members
            [2]

            >>> baca.PartAssignment('Horn', (3, 4)).members
            [3, 4]

            >>> baca.PartAssignment('Horn', [1, 3]).members
            [1, 3]

        """
        return self._members

    @property
    def parts(self):
        """
        Gets parts.

        ..  container:: example

            >>> baca.PartAssignment('Horn').parts
            [Part(instrument='Horn', section='Horn')]

            >>> baca.PartAssignment('Horn', 1).parts
            [Part(instrument='Horn', member=1, section='Horn')]

            >>> baca.PartAssignment('Horn', 2).parts
            [Part(instrument='Horn', member=2, section='Horn')]

            >>> baca.PartAssignment('Horn', (3, 4)).parts
            [Part(instrument='Horn', member=3, section='Horn'), Part(instrument='Horn', member=4, section='Horn')]

            >>> baca.PartAssignment('Horn', [1, 3]).parts
            [Part(instrument='Horn', member=1, section='Horn'), Part(instrument='Horn', member=3, section='Horn')]

        """
        return self._parts

    @property
    def section(self):
        """
        Gets section.

        ..  container:: example

            >>> baca.PartAssignment('Horn').section
            'Horn'

            >>> baca.PartAssignment('Horn', 1).section
            'Horn'

            >>> baca.PartAssignment('Horn', 2).section
            'Horn'

            >>> baca.PartAssignment('Horn', (3, 4)).section
            'Horn'

            >>> baca.PartAssignment('Horn', [1, 3]).section
            'Horn'

        """
        return self._section

    @property
    def token(self):
        """
        Gets token.

        ..  container:: example

            >>> baca.PartAssignment('Horn').token is None
            True

            >>> baca.PartAssignment('Horn', 1).token
            1

            >>> baca.PartAssignment('Horn', 2).token
            2

            >>> baca.PartAssignment('Horn', (3, 4)).token
            (3, 4)

            >>> baca.PartAssignment('Horn', [1, 3]).token
            [1, 3]

        """
        return self._token


class Section:
    """
    Section.

    ..  container:: example

        >>> baca.Section(
        ...     abbreviation='VN-1',
        ...     count=18,
        ...     instrument='Violin',
        ...     name='FirstViolin',
        ...     )
        Section(abbreviation='VN-1', count=18, instrument='Violin', name='FirstViolin')

        >>> baca.Section(
        ...     abbreviation='VN-2',
        ...     count=18,
        ...     instrument='Violin',
        ...     name='SecondViolin',
        ...     )
        Section(abbreviation='VN-2', count=18, instrument='Violin', name='SecondViolin')

        >>> baca.Section(
        ...     abbreviation='VA',
        ...     count=18,
        ...     name='Viola',
        ...     )
        Section(abbreviation='VA', count=18, instrument='Viola', name='Viola')

        >>> baca.Section(
        ...     abbreviation='VC',
        ...     count=14,
        ...     name='Cello',
        ...     )
        Section(abbreviation='VC', count=14, instrument='Cello', name='Cello')

        >>> baca.Section(
        ...     abbreviation='CB',
        ...     count=6,
        ...     name='Contrabass',
        ...     )
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
        Is true when ``argument`` is a section with the same name,
        abbreviation and count as this section.

        ..  container:: example

            >>> section_1 = baca.Section(
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )
            >>> section_2 = baca.Section(
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )
            >>> section_3 = baca.Section(
            ...     abbreviation='VN-2',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='SecondViolin',
            ...     )

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
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def abbreviation(self):
        """
        Gets abbreviation.

        ..  container:: example

            >>> section = baca.Section(
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )

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
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )

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
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )

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
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )

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
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )

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
        ...    baca.Part(section='BassClarinet', section_abbreviation='BCL'),
        ...    baca.Part(section='Violin', section_abbreviation='VN'),
        ...    baca.Part(section='Viola', section_abbreviation='VA'),
        ...    baca.Part(section='Cello', section_abbreviation='VC'),
        ...    )
        >>> len(part_manifest)
        4

    ..  container:: example

        Initializes from orchestra sections:

        >>> part_manifest = baca.PartManifest(
        ...    baca.Section(
        ...         abbreviation='FL',
        ...         count=4,
        ...         name='Flute',
        ...         ),
        ...    baca.Section(
        ...         abbreviation='OB',
        ...         count=3,
        ...         name='Oboe',
        ...         ),
        ...    baca.Part(
        ...         section_abbreviation='EH',
        ...         section='EnglishHorn',
        ...         ),
        ...    baca.Section(
        ...         abbreviation='VN-1',
        ...         count=18,
        ...         instrument='Violin',
        ...         name='FirstViolin',
        ...         ),
        ...    baca.Section(
        ...         abbreviation='VN-2',
        ...         count=18,
        ...         instrument='Violin',
        ...         name='SecondViolin',
        ...         ),
        ...    )
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
            ...    baca.Section(
            ...         abbreviation='FL',
            ...         count=4,
            ...         name='Flute',
            ...         ),
            ...    baca.Section(
            ...         abbreviation='OB',
            ...         count=3,
            ...         name='Oboe',
            ...         ),
            ...    baca.Part(
            ...         section_abbreviation='EH',
            ...         section='EnglishHorn',
            ...         ),
            ...    baca.Section(
            ...         abbreviation='VN-1',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='FirstViolin',
            ...         ),
            ...    baca.Section(
            ...         abbreviation='VN-2',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='SecondViolin',
            ...         ),
            ...    )

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
            ...    baca.Part(section='BassClarinet', section_abbreviation='BCL'),
            ...    baca.Part(section='Violin', section_abbreviation='VN'),
            ...    baca.Part(section='Viola', section_abbreviation='VA'),
            ...    baca.Part(section='Cello', section_abbreviation='VC'),
            ...    )
            >>> len(part_manifest)
            4

        ..  container:: example

            >>> part_manifest = baca.PartManifest(
            ...    baca.Section(
            ...         abbreviation='FL',
            ...         count=4,
            ...         name='Flute',
            ...         ),
            ...    baca.Section(
            ...         abbreviation='OB',
            ...         count=3,
            ...         name='Oboe',
            ...         ),
            ...    baca.Part(
            ...         section_abbreviation='EH',
            ...         section='EnglishHorn',
            ...         ),
            ...    baca.Section(
            ...         abbreviation='VN-1',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='FirstViolin',
            ...         ),
            ...    baca.Section(
            ...         abbreviation='VN-2',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='SecondViolin',
            ...         ),
            ...    )

            >>> len(part_manifest)
            44

        """
        return len(self.parts)

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def parts(self):
        """
        Gets parts in manifest.

        ..  container:: example

            >>> part_manifest = baca.PartManifest(
            ...    baca.Part(section='BassClarinet', section_abbreviation='BCL'),
            ...    baca.Part(section='Violin', section_abbreviation='VN'),
            ...    baca.Part(section='Viola', section_abbreviation='VA'),
            ...    baca.Part(section='Cello', section_abbreviation='VC'),
            ...    )
            >>> for part in part_manifest:
            ...     part
            ...
            Part(instrument='BassClarinet', number=1, section='BassClarinet', section_abbreviation='BCL')
            Part(instrument='Violin', number=2, section='Violin', section_abbreviation='VN')
            Part(instrument='Viola', number=3, section='Viola', section_abbreviation='VA')
            Part(instrument='Cello', number=4, section='Cello', section_abbreviation='VC')

        ..  container:: example

            >>> part_manifest = baca.PartManifest(
            ...    baca.Section(
            ...         abbreviation='FL',
            ...         count=4,
            ...         name='Flute',
            ...         ),
            ...    baca.Section(
            ...         abbreviation='OB',
            ...         count=3,
            ...         name='Oboe',
            ...         ),
            ...    baca.Part(
            ...         section_abbreviation='EH',
            ...         section='EnglishHorn',
            ...         ),
            ...    baca.Section(
            ...         abbreviation='VN-1',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='FirstViolin',
            ...         ),
            ...    baca.Section(
            ...         abbreviation='VN-2',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='SecondViolin',
            ...         ),
            ...    )

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
            ...    baca.Part(section='BassClarinet', section_abbreviation='BCL'),
            ...    baca.Part(section='Violin', section_abbreviation='VN'),
            ...    baca.Part(section='Viola', section_abbreviation='VA'),
            ...    baca.Part(section='Cello', section_abbreviation='VC'),
            ...    )
            >>> part_manifest.sections
            []

        ..  container:: example

            >>> part_manifest = baca.PartManifest(
            ...    baca.Section(
            ...         abbreviation='FL',
            ...         count=4,
            ...         name='Flute',
            ...         ),
            ...    baca.Section(
            ...         abbreviation='OB',
            ...         count=3,
            ...         name='Oboe',
            ...         ),
            ...    baca.Part(
            ...         section_abbreviation='EH',
            ...         section='EnglishHorn',
            ...         ),
            ...    baca.Section(
            ...         abbreviation='VN-1',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='FirstViolin',
            ...         ),
            ...    baca.Section(
            ...         abbreviation='VN-2',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='SecondViolin',
            ...         ),
            ...    )

            >>> for section in part_manifest.sections:
            ...     section
            ...
            Section(abbreviation='FL', count=4, instrument='Flute', name='Flute')
            Section(abbreviation='OB', count=3, instrument='Oboe', name='Oboe')
            Section(abbreviation='VN-1', count=18, instrument='Violin', name='FirstViolin')
            Section(abbreviation='VN-2', count=18, instrument='Violin', name='SecondViolin')

        ..  container:: example

            >>> section = baca.Section(
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )
            >>> section in part_manifest.sections
            True

            >>> section = baca.Section(
            ...     abbreviation='VN-1',
            ...     count=36,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )
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
            ...    baca.Section(
            ...         abbreviation='FL',
            ...         count=4,
            ...         name='Flute',
            ...         ),
            ...    baca.Section(
            ...         abbreviation='OB',
            ...         count=3,
            ...         name='Oboe',
            ...         ),
            ...    baca.Part(
            ...         section_abbreviation='EH',
            ...         section='EnglishHorn',
            ...         ),
            ...    baca.Section(
            ...         abbreviation='VN-1',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='FirstViolin',
            ...         ),
            ...    baca.Section(
            ...         abbreviation='VN-2',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='SecondViolin',
            ...         ),
            ...    )

            >>> part_assignment = baca.PartAssignment('Oboe')
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


class PersistentOverride:
    """
    Persistent override.

    ..  container:: example

        >>> override = baca.PersistentOverride(
        ...     attribute='bar_extent',
        ...     context='Staff',
        ...     grob='bar_line',
        ...     value=(-2, 0),
        ...     )

        >>> print(abjad.storage(override))
        baca.PersistentOverride(
            attribute='bar_extent',
            context='Staff',
            grob='bar_line',
            value=(-2, 0),
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_after",
        "_attribute",
        "_context",
        "_grob",
        "_hide",
        "_value",
    )

    _persistent = True

    ### INITIALIZER ###

    def __init__(
        self,
        after=None,
        attribute=None,
        context=None,
        grob=None,
        hide=None,
        value=None,
    ):
        if after is not None:
            after = bool(after)
        self._after = after
        if attribute is not None:
            assert isinstance(attribute, str), repr(attribute)
        self._attribute = attribute
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        if grob is not None:
            assert isinstance(grob, str), repr(grob)
        self._grob = grob
        if hide is not None:
            hide = bool(hide)
        self._hide = hide
        self._value = value

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is persistent override with attribute,
        context, grob, value equal to those of this persistent override.

        ..  container:: example

            >>> override_1 = baca.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )
            >>> override_2 = baca.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )
            >>> override_3 = baca.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Score',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )

            >>> override_1 == override_1
            True
            >>> override_1 == override_2
            True
            >>> override_1 == override_3
            False

            >>> override_2 == override_1
            True
            >>> override_2 == override_2
            True
            >>> override_2 == override_3
            False

            >>> override_3 == override_1
            False
            >>> override_3 == override_2
            False
            >>> override_3 == override_3
            True

        """
        if not isinstance(argument, type(self)):
            return False
        if (
            self.attribute == argument.attribute
            and self.context == argument.context
            and self.grob == argument.grob
            and self.value == argument.value
        ):
            return True
        return False

    def __hash__(self):
        """
        Hashes persistent override.
        """
        return super().__hash__()

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return abjad.FormatSpecification(client=self)

    def _get_lilypond_format(self, context=None):
        if isinstance(context, abjad.Context):
            assert isinstance(context.lilypond_type, str), repr(context)
            lilypond_type = context.lilypond_type
        else:
            lilypond_type = self.context
        string = abjad.overrides.make_lilypond_override_string(
            self.grob,
            self.attribute,
            self.value,
            context=lilypond_type,
            once=False,
        )
        return string

    def _get_lilypond_format_bundle(self, component=None):
        bundle = abjad.LilyPondFormatBundle()
        if self.hide:
            return bundle
        strings = [self._get_lilypond_format()]
        if self.after:
            bundle.after.commands.extend(strings)
        else:
            bundle.before.commands.extend(strings)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def after(self):
        r"""
        Is true when override formats after leaf.

        ..  container:: example

            Formats override before leaf:

            >>> override = baca.PersistentOverride(
            ...     attribute='color',
            ...     grob='note_head',
            ...     value='red',
            ...     )

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(override, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \override NoteHead.color = #red
                    c'4
                    d'4
                    e'4
                    f'4
                }

        ..  container:: example

            Formats override after leaf:

            >>> override = baca.PersistentOverride(
            ...     after=True,
            ...     attribute='color',
            ...     grob='note_head',
            ...     value='red',
            ...     )

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(override, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    \override NoteHead.color = #red
                    d'4
                    e'4
                    f'4
                }

        """
        return self._after

    @property
    def attribute(self):
        """
        Gets attribute.

        ..  container:: example

            >>> override = baca.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )

            >>> override.attribute
            'bar_extent'

        """
        return self._attribute

    @property
    def context(self):
        """
        Gets context.

        ..  container:: example

            >>> override = baca.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )

            >>> override.context
            'Staff'

        """
        return self._context

    @property
    def grob(self):
        """
        Gets grob.

        ..  container:: example

            >>> override = baca.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )

            >>> override.grob
            'bar_line'

        """
        return self._grob

    @property
    def hide(self):
        """
        Is true when staff lines should not appear in output.

        ..  container:: example

            >>> override = baca.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )

            >>> override.hide is None
            True

        """
        return self._hide

    @property
    def persistent(self):
        """
        Is true.

        ..  container:: example

            >>> override = baca.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )

            >>> override.persistent
            True

        Class constant.
        """
        return self._persistent

    @property
    def value(self):
        """
        Gets value.

        ..  container:: example

            >>> override = baca.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )

            >>> override.value
            (-2, 0)

        """
        return self._value


### FUNCTIONS ####


def _context_name_to_first_appearance_margin_markup(path, context_name):
    module = _import_score_package(path)
    margin_markups = getattr(module, "margin_markups", None)
    if not margin_markups:
        return []
    dictionary = abjad.OrderedDict()
    string = "first_appearance_margin_markup"
    for segment in path.segments.list_paths():
        dictionary_ = segment.get_metadatum(string, [])
        dictionary.update(dictionary_)
    key = dictionary.get(context_name)
    if key is None:
        return []
    margin_markup = margin_markups.get(key)
    if margin_markup is None:
        return []
    markup = margin_markup.markup
    assert markup is not None, repr(margin_markup)
    strings = markup._get_format_pieces()
    strings.insert(0, "shortInstrumentName =")
    indent = abjad.LilyPondFormatBundle.indent
    strings = [indent + _ for _ in strings]
    strings = [r"\with", "{"] + strings + ["}"]
    return strings


def _global_rest_identifier(segment_name):
    """
    Gets global rest identifier.

    ..  container:: example

        >>> baca.segments._global_rest_identifier("_")
        'i_Global_Rests'

        >>> baca.segments._global_rest_identifier("_1")
        'i_a_Global_Rests'

        >>> baca.segments._global_rest_identifier("_2")
        'i_b_Global_Rests'

        >>> baca.segments._global_rest_identifier("A")
        'A_Global_Rests'

        >>> baca.segments._global_rest_identifier("A1")
        'A_a_Global_Rests'

        >>> baca.segments._global_rest_identifier("A2")
        'A_b_Global_Rests'

    """
    identifier = abjad.String(segment_name).to_segment_lilypond_identifier()
    identifier = abjad.String(f"{identifier}_Global_Rests")
    return identifier


def _global_rest_identifiers(path):
    """
    Gets global rest identifiers.
    """
    assert not path.is_external(), repr(path)
    identifiers = []
    if path.segments is not None:
        paths = path.segments.list_paths()
    else:
        paths = []
    for segment in paths:
        identifier = abjad.String(segment.name).to_segment_lilypond_identifier()
        identifier = abjad.String(f"{identifier}_Global_Rests")
        identifiers.append(identifier)
    return identifiers


def _import_score_package(path):
    assert path.is_score_package_path()
    try:
        module = importlib.import_module(path.contents.name)
    except Exception:
        return
    return module


def _import_score_template(path):
    module = _import_score_package(path)
    if not module:
        raise Exception(f"can not import score package: {path}, {path.contents}.")
    score_template = getattr(module, "ScoreTemplate", None)
    if not score_template:
        raise Exception("can not import score template.")
    return score_template


def _instrument_to_staff_identifiers(path, instrument):
    """
    Changes ``instrument`` to staff identifiers dictionary.
    """
    assert not path.is_external(), repr(path)
    alive_during_segment = abjad.OrderedDict()
    if path.segments is not None:
        paths = path.segments.list_paths()
    else:
        paths = []
    for segment in paths:
        dictionary = segment.get_metadatum(
            "alive_during_segment", [], file_name="__persist__.py"
        )
        alive_during_segment[segment.name] = dictionary
    staves_in_score = []
    for segment_name, contexts in alive_during_segment.items():
        for context in contexts:
            if context.startswith(instrument):
                words = abjad.String(context).delimit_words()
                if words[-2] == "Staff" and abjad.String(words[-1]).is_roman():
                    if context not in staves_in_score:
                        staves_in_score.append(context)
    staves_in_score = abjad.String.sort_roman(staves_in_score)
    dictionary = abjad.OrderedDict()
    for staff in staves_in_score:
        dictionary[staff] = identifiers = []
        for segment_name, contexts in alive_during_segment.items():
            identifier = abjad.String(segment_name)
            identifier = identifier.to_segment_lilypond_identifier()
            if staff in contexts:
                identifier_ = f"{identifier}_{staff}"
            else:
                identifier_ = f"{identifier}_Global_Rests"
            identifier = abjad.String(identifier_)
            identifiers.append(identifier)
    return dictionary


def _part_name_to_default_clef(path, part_name):
    module = _import_score_package(path)
    instruments = getattr(module, "instruments", None)
    if not instruments:
        raise Exception(f"can not find instruments: {path!r}.")
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


def get_measure_profile_metadata(path):
    """
    Gets measure profile metadata.

    Reads segment metadata when path is segment.

    Reads score metadata when path is not segment.

    Returns tuple of three metadata: first measure number; measure count;
    list of fermata measure numbers.
    """
    if path.parent.is_segment():
        string = "first_measure_number"
        first_measure_number = path.parent.get_metadatum(string)
        time_signatures = path.parent.get_metadatum("time_signatures")
        if bool(time_signatures):
            measure_count = len(time_signatures)
        else:
            measure_count = 0
        string = "fermata_measure_numbers"
        fermata_measure_numbers = path.parent.get_metadatum(string)
    else:
        first_measure_number = 1
        dictionary = path.contents.get_metadatum("time_signatures")
        dictionary = dictionary or abjad.OrderedDict()
        measure_count = 0
        for segment, time_signatures in dictionary.items():
            measure_count += len(time_signatures)
        string = "fermata_measure_numbers"
        dictionary = path.contents.get_metadatum(string)
        dictionary = dictionary or abjad.OrderedDict()
        fermata_measure_numbers = []
        for segment, fermata_measure_numbers_ in dictionary.items():
            fermata_measure_numbers.extend(fermata_measure_numbers_)
    return (first_measure_number, measure_count, fermata_measure_numbers)


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


def get_part_manifest(path):
    """
    Gets part manifest from ``path``.
    """
    assert path.is_score_package_path()
    score_template = _import_score_template(path)
    score_template = score_template()
    part_manifest = score_template.part_manifest
    return part_manifest


def get_preamble_page_count_overview(path):
    """
    Gets preamble page count overview.
    """
    assert path.is_file(), repr(path)
    first_page_number, page_count = 1, None
    with open(path) as pointer:
        for line in pointer.readlines():
            if line.startswith("% first_page_number = "):
                line = line.strip("% first_page_number = ")
                first_page_number = eval(line)
            if line.startswith("% page_count = "):
                line = line.strip("% page_count = ")
                page_count = eval(line)
    if isinstance(page_count, int):
        final_page_number = first_page_number + page_count - 1
        return first_page_number, page_count, final_page_number
    return None


def get_preamble_partial_score(path):
    """
    Gets preamble time signatures.
    """
    assert path.is_file(), repr(path)
    prefix = "% partial_score ="
    with open(path) as pointer:
        for line in pointer.readlines():
            if line.startswith(prefix):
                line = line[len(prefix) :]
                partial_score = eval(line)
                return partial_score
    return False


def get_preamble_time_signatures(path):
    """
    Gets preamble time signatures.
    """
    assert path.is_file(), repr(path)
    start_line = "% time_signatures = ["
    stop_line = "%  ]"
    lines = []
    with open(path) as pointer:
        for line in pointer.readlines():
            if line.startswith(stop_line):
                lines.append("]")
                break
            if lines:
                lines.append(line.strip("%").strip("\n"))
            elif line.startswith(start_line):
                lines.append("[")
        string = "".join(lines)
        try:
            time_signatures = eval(string)
        except Exception:
            return []
        return time_signatures
    return None


def global_skip_identifiers(path):
    """
    Gets global skip identifiers.
    """
    assert not path.is_external(), repr(path)
    identifiers = []
    if path.segments is not None:
        paths = path.segments.list_paths()
    else:
        paths = []
    for segment in paths:
        identifier = abjad.String(segment.name).to_segment_lilypond_identifier()
        identifier = abjad.String(f"{identifier}_GlobalSkips")
        identifiers.append(identifier)
    return identifiers


def part_to_identifiers(path, part, container_to_part_assignment):
    """
    Changes ``part`` to (part container) identifiers (using
    ``container_to_part_assignment`` dictionary).
    """
    assert not path.is_external(), repr(path)
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
        message = "empty container-to-part-assignment dictionary"
        return message
    for i, (segment_name, dictionary_) in enumerate(dictionary.items()):
        pairs = []
        for identifier, (part_assignment, timespan) in dictionary_.items():
            if part in part_assignment:
                pairs.append((identifier, timespan))
        if pairs:
            pairs.sort(key=lambda pair: pair[1])
            identifiers_ = [_[0] for _ in pairs]
            identifiers.extend(identifiers_)
        else:
            identifier = _global_rest_identifier(segment_name)
            identifiers.append(identifier)
    return identifiers


def path_to_part(path):
    """
    Changes path to part.
    """
    assert path.parent.is_part(), repr(path)
    words = path.parent.name.split("-")
    part_manifest = get_part_manifest(path)
    if not part_manifest:
        raise Exception(f"no part manifest: {path}.")
    assert isinstance(part_manifest, PartManifest), repr(part_manifest)
    words = [abjad.String(_).capitalize_start() for _ in words]
    part_name = "".join(words)
    for part in part_manifest:
        if abjad.String(part.name).to_upper_camel_case() == part_name:
            return part
    raise Exception(f"can not find {part_name!r} in part manifest.")


def remove_lilypond_warnings(
    path,
    crescendo_too_small=None,
    decrescendo_too_small=None,
    overwriting_glissando=None,
):
    """
    Removes LilyPond warnings from ``.log``.
    """
    assert path.name.endswith(".log"), repr(path)
    lines = []
    skip = 0
    with open(path) as pointer:
        for line in pointer.readlines():
            if 0 < skip:
                skip -= 1
                continue
            if crescendo_too_small and "crescendo too small" in line:
                skip = 2
                continue
            if decrescendo_too_small and "decrescendo too small" in line:
                skip = 2
                continue
            if overwriting_glissando and "overwriting glissando" in line:
                skip = 1
                continue
            lines.append(line)
    text = "".join(lines)
    path.write_text(text)


def score_skeleton(path):
    """
    Makes score skeleton.

    Only works when score template defines ``skeleton()`` method.
    """
    assert not path.is_external(), repr(path)
    score_template = _import_score_template(path)
    if not hasattr(score_template, "skeleton"):
        return None
    skeleton = score_template.skeleton()
    indent = abjad.LilyPondFormatBundle.indent
    context = skeleton["Global_Skips"]
    identifiers = global_skip_identifiers(path)
    strings = ["\\" + _ for _ in identifiers]
    literal = abjad.LilyPondLiteral(strings)
    abjad.attach(literal, context)
    context = skeleton["Global_Rests"]
    identifiers = _global_rest_identifiers(path)
    strings = ["\\" + _ for _ in identifiers]
    literal = abjad.LilyPondLiteral(strings)
    abjad.attach(literal, context)
    module = _import_score_package(path)
    instruments = getattr(module, "instruments", None)
    for staff_group in abjad.Iteration(skeleton).components(abjad.StaffGroup):
        if staff_group:
            continue
        assert len(staff_group) == 0, repr(staff_group)
        instrument = staff_group.name
        words = abjad.String(staff_group.name).delimit_words()
        if words[-3:] == ["Square", "Staff", "Group"]:
            words = words[:-3]
        elif words[-2:] == ["Piano", "Staff"]:
            words = words[:-2]
        elif words == ["Percussion", "Staff", "Group"]:
            words = [abjad.String("Percussion")]
        else:
            raise ValueError(staff_group)
        instrument = "".join(words)
        dictionary = _instrument_to_staff_identifiers(path, instrument)
        if instrument in ("FirstViolin", "SecondViolin"):
            key = "Violin"
        else:
            key = instrument
        abjad_instrument = instruments.get(key, None)
        if not abjad_instrument:
            raise Exception(f"can not find {key!r}.")
        clef = abjad.Clef(abjad_instrument.allowable_clefs[0])
        clef_string = clef._get_lilypond_format()
        strings = []
        method = _context_name_to_first_appearance_margin_markup
        for staff_name, identifiers in dictionary.items():
            strings.append("{")
            for i, identifier in enumerate(identifiers):
                string = indent + rf'\context Staff = "{staff_name}"'
                strings.append(string)
                if i == 0:
                    margin_markup_strings = method(path, staff_name)
                    for string_ in margin_markup_strings:
                        strings.append(indent + string_)
                    strings.append(indent + clef_string)
                string = indent + "\\" + identifier
                strings.append(string)
            strings.append("}")
        literal = abjad.LilyPondLiteral(strings)
        abjad.attach(literal, staff_group)
    return skeleton
