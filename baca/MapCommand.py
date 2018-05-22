import abjad
import baca
import collections
import typing
from .Command import Command
from .Typing import Selector


class MapCommand(Command):
    r"""
    Map command.

    ..  container:: example

        >>> baca.MapCommand()
        MapCommand()

    ..  container:: example

        Attaches accents to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.accent(selector=baca.pheads()),
        ...         baca.tuplet(1),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            -\accent                                                                 %! IC
                            [
                            e''16
                            -\accent                                                                 %! IC
                            ]
                            ef''4
                            -\accent                                                                 %! IC
                            ~
                            ef''16
                            r16
                            af''16
                            -\accent                                                                 %! IC
                            [
                            g''16
                            -\accent                                                                 %! IC
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_commands',
        '_selector',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        commands: typing.Union[
            abjad.Expression, Command, typing.Iterable] = None,
        selector: Selector = None,
        ) -> None:
        Command.__init__(self, selector=selector)
        if isinstance(commands, (abjad.Expression, Command)):
            commands = abjad.CyclicTuple([commands])
        elif isinstance(commands, collections.Iterable):
            commands = abjad.CyclicTuple(commands)
        elif commands is not None:
            raise TypeError(commands)
        self._commands = commands

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> typing.Optional[typing.List]:
        """
        Maps commands to result of selector called on ``argument``.
        """
        if argument is None:
            return None
        if not self.commands:
            return None
        if self.selector is not None:
            argument = self.selector(argument)
            if self.selector._is_singular_get_item():
                argument = [argument]
        items_ = []
        for i, item in enumerate(argument):
            command = self.commands[i]
            item_ = command(item)
            items_.append(item_)
        return items_

    ### PUBLIC PROPERTIES ###

    @property
    def commands(self) -> typing.Optional[abjad.CyclicTuple]:
        """
        Gets commands.
        """
        return self._commands
