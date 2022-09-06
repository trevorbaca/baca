"""
Other commands.
"""
import abjad

from . import parts as _parts


def assign_part_function(
    argument,
    part_assignment: _parts.PartAssignment,
) -> None:
    assert isinstance(part_assignment, _parts.PartAssignment), repr(part_assignment)
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
