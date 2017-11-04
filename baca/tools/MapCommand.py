import abjad
import baca
import collections
from .Command import Command


class MapCommand(Command):
    r'''Map command.

    ..  container:: example

        >>> baca.MapCommand()
        MapCommand()

    ..  container:: example

        Attaches accents to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(baca.accents(), baca.tuplet(1)),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5
                            r8
                            c'16 [
                            d'16 ]
                            bf'4 ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16 -\accent [
                            e''16 -\accent ]
                            ef''4 -\accent ~
                            ef''16
                            r16
                            af''16 -\accent [
                            g''16 -\accent ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding
                        }
                    }
                }
            >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_commands',
        '_selector',
        )

    ### INITIALIZER ###

    def __init__(self, commands=None, selector=None):
        Command.__init__(self, selector=selector)
        if isinstance(commands, baca.Command):
            commands = abjad.CyclicTuple([commands])
        elif isinstance(commands, collections.Iterable):
            commands = abjad.CyclicTuple(commands)
        self._commands = commands

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Maps commands to result of selector called on `argument`.

        Returns none.
        '''
        if not self.commands:
            return
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
            if self.selector._is_singular_get_item():
                argument = [argument]
        for i, item in enumerate(argument):
            command = self.commands[i]
            command(item)

    ### PUBLIC PROPERTIES ###

    @property
    def commands(self):
        r'''Gets commands.

        Returns cylic tuple or none.
        '''
        return self._commands
