import abjad
import baca
import collections
import typing
from .Command import Command
from .Suite import Suite
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
        ...         baca.tuplet(1),
        ...         baca.apply(
        ...             baca.pheads(),
        ...             baca.marcato(),
        ...             baca.staccato(),
        ...             ),
        ...         baca.slur(
        ...             abjad.tweak(abjad.Down).direction,
        ...             ),
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
                            -\marcato                                                                %! IC
                            -\staccato                                                               %! IC
                            [
                            - \tweak direction #down                                                 %! SC
                            (                                                                        %! SC
                            e''16
                            -\marcato                                                                %! IC
                            -\staccato                                                               %! IC
                            ]
                            ef''4
                            -\marcato                                                                %! IC
                            -\staccato                                                               %! IC
                            ~
                            ef''16
                            r16
                            af''16
                            -\marcato                                                                %! IC
                            -\staccato                                                               %! IC
                            [
                            g''16
                            -\marcato                                                                %! IC
                            -\staccato                                                               %! IC
                            ]
                            )                                                                        %! SC
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
        selector: Selector = None,
        *commands: typing.Union[abjad.Expression, Command],
        ) -> None:
        Command.__init__(self, selector=selector)
        command_list: typing.List[
            typing.Union[abjad.Expression, Command, Suite]
            ] = []
        for command in commands:
            if not isinstance(command, (abjad.Expression, Command, Suite)):
                message = '\n  Commands must contain only commands and expressions.'
                message += f'\n  Not {type(command).__name__}: {command!r}.'
                raise Exception(message)
            command_list.append(command)
        self._commands = tuple(command_list)

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> typing.Optional[typing.List]:
        """
        Maps each command in ``commands`` to each item in output of selector
        called on ``argument``.
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
        for command in self.commands:
            for item in argument:
                item_ = command(item)
                items_.append(item_)
        return items_

    ### PUBLIC PROPERTIES ###

    @property
    def commands(self) -> typing.Optional[typing.Tuple]:
        """
        Gets commands.
        """
        return self._commands
