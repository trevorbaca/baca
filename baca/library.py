import abjad
import typing
from .Command import Command
from .MapCommand import MapCommand


def map(
    selector: typing.Union[abjad.Expression, str],
    *commands: typing.Union[Command, abjad.Expression],
    ) -> MapCommand:
    """
    Calls each command in ``commands`` on the output of ``selector``.
    """
    if not isinstance(selector, (abjad.Expression, str)):
        message = '\n  Map selector must be expression or string.'
        message += f'\n  Not {format(selector)}.'
        raise Exception(message)
    if not commands:
        raise Exception('map commands must not be empty.')
    commands_ = []
    for item in commands:
        if isinstance(item, (list, tuple)):
            commands_.extend(item)
        else:
            commands_.append(item)
    for command in commands_:
        if not isinstance(command, (Command, abjad.Expression)):
            message = '\n  Must be command or expression.'
            message += f'\n  Not {type(command).__name__}: {command!r}.'
            raise Exception(message)
    return MapCommand(selector, *commands_)
