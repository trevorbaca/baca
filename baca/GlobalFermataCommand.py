import abjad
import baca
import typing
from .Command import Command
from . import typings


class GlobalFermataCommand(Command):
    """
    Global fermata command.

    ..  container:: example

        >>> baca.GlobalFermataCommand()
        GlobalFermataCommand(selector=baca.leaf(0))

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_description',
        )

    description_to_command = {
        'short': 'shortfermata',
        'fermata': 'fermata',
        'long': 'longfermata',
        'very_long': 'verylongfermata',
        }

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        description: str = None,
        selector: typings.Selector = 'baca.leaf(0)',
        ) -> None:
        Command.__init__(self, selector=selector)
        if description is not None:
            assert description in GlobalFermataCommand.description_to_command
        self._description = description

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Applies command to ``argument`` selector output.
        """
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if isinstance(self.description, str):
            command = self.description_to_command.get(self.description)
        else:
            command = 'fermata'
        for leaf in abjad.iterate(argument).leaves():
            assert isinstance(leaf, abjad.MultimeasureRest)
            string = f'scripts.u{command}'
            directive = abjad.Markup.musicglyph(string)
            directive = abjad.new(directive, direction=abjad.Up)
            abjad.attach(directive, leaf, tag='GFC1')
            strings = []
            string = r'\once \override'
            string += ' Score.MultiMeasureRest.transparent = ##t'
            strings.append(string)
            string = r'\once \override Score.TimeSignature.stencil = ##f'
            strings.append(string)
            literal = abjad.LilyPondLiteral(strings)
            abjad.attach(literal, leaf, tag='GFC2')
            abjad.attach(
                abjad.tags.FERMATA_MEASURE,
                leaf,
                tag=abjad.tags.FERMATA_MEASURE,
                )

    ### PUBLIC PROPERTIES ###

    @property
    def description(self) -> typing.Optional[str]:
        """
        Gets description.
        """
        return self._description
