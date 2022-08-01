"""
Other commands.
"""
import dataclasses
import typing

import abjad

from . import command as _command
from . import parts as _parts
from . import select as _select


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


def assign_part(
    part_assignment: _parts.PartAssignment,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> PartAssignmentCommand:
    """
    Note that the selector must include all leaves, including hidden ones.
    """
    assert isinstance(part_assignment, _parts.PartAssignment), repr(part_assignment)
    return PartAssignmentCommand(part_assignment=part_assignment, selector=selector)


def assign_part_function(
    argument,
    part_assignment: _parts.PartAssignment,
) -> None:
    assert isinstance(part_assignment, _parts.PartAssignment), repr(part_assignment)
    _do_part_assignment_command(argument, part_assignment)
