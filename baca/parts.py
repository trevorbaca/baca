"""
Parts.
"""

import dataclasses

import abjad


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

        >>> baca.PartAssignment("Horn", 1)
        PartAssignment(name='Horn', token=1)

        >>> baca.PartAssignment("Horn", 2)
        PartAssignment(name='Horn', token=2)

        >>> baca.PartAssignment("Horn", (3, 4))
        PartAssignment(name='Horn', token=(3, 4))

        >>> baca.PartAssignment("Horn", [1, 3])
        PartAssignment(name='Horn', token=[1, 3])

    ..  container:: example

        >>> baca.PartAssignment("BassClarinet")
        PartAssignment(name='BassClarinet', token=None)

    """

    name: str
    token: int | tuple[int, int] | list[int] | None = None

    def __post_init__(self):
        assert isinstance(self.name, str), repr(self.name)
        assert self._validate_token(self.token), repr(self.token)

    @staticmethod
    def _validate_token(argument):
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

    def numbers(self):
        numbers = []
        if self.token is None:
            pass
        elif isinstance(self.token, int):
            numbers.append(self.token)
        elif isinstance(self.token, tuple):
            assert len(self.token) == 2, repr(self.token)
            for number in range(self.token[0], self.token[1] + 1):
                numbers.append(number)
        else:
            assert isinstance(self.token, list), repr(self.token)
            numbers.extend(self.token)
        return numbers

    def make_parts(self):
        parts = []
        if self.token is None:
            part = Part(self.name)
            parts.append(part)
        else:
            for number in self.numbers():
                part = Part(self.name, number)
                parts.append(part)
        return parts


def assign_part(
    argument,
    part_assignment: PartAssignment,
) -> None:
    assert isinstance(part_assignment, PartAssignment), repr(part_assignment)
    first_leaf = abjad.get.leaf(argument, 0)
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
