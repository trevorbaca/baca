import abjad
import baca
import typing
from .Command import Command
from .Typing import Selector


class PartAssignmentCommand(Command):
    """
    Part assignment command.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_part_assignment',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        part_assignment: abjad.PartAssignment = None,
        selector: Selector = 'baca.leaves()',
        ) -> None:
        Command.__init__(self, selector=selector)
        if part_assignment is not None:
            if not isinstance(part_assignment, abjad.PartAssignment):
                message = 'part_assignment must be part assignment'
                message += f' (not {part_assignment!r}).'
                raise Exception(message)
        self._part_assignment = part_assignment

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Inserts ``selector`` output in container and sets part assignment.
        """
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        first_leaf = abjad.inspect(argument).get_leaf(0)
        if first_leaf is None:
            return
        parentage = abjad.inspect(first_leaf).get_parentage()
        voice = parentage.get_first(abjad.Voice)
        if voice is not None and self.part_assignment is not None:
            if not self.runtime['score_template'].allows_part_assignment(
                voice.name,
                self.part_assignment,
                ):
                message = f'{voice.name} does not allow'
                message += f' {self.part_assignment.section} part assignment:'
                message += f'\n  {self.part_assignment}'
                raise Exception(message)
        identifier = f'%*% {self.part_assignment!s}'
        container = abjad.Container(identifier=identifier)
        components = baca.select(argument).leaves().top()
        abjad.mutate(components).wrap(container)

    ### PUBLIC PROPERTIES ###

    @property
    def part_assignment(self) -> typing.Optional[abjad.PartAssignment]:
        """
        Gets part assignment.
        """
        return self._part_assignment
