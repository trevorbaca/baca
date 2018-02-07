import abjad
import baca
from typing import Union
from .Command import Command


class TieCorrectionCommand(Command):
    r'''Tie correction command.

    ..  container:: example

        >>> baca.TieCorrectionCommand()
        TieCorrectionCommand(selector=baca.pleaf(-1))

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_direction',
        '_repeat',
        '_untie',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        direction=None,
        repeat=None,
        selector='baca.pleaf(-1)',
        untie=None,
        ):
        Command.__init__(self, selector=selector)
        if direction is not None:
            assert direction in (abjad.Right, abjad.Left)
        self._direction = direction
        if repeat is not None:
            repeat = bool(repeat)
        self._repeat = repeat
        if untie is not None:
            untie = bool(untie)
        self._untie = untie

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Applies command to result of selector called on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        leaves = baca.select(argument).leaves()
        for leaf in leaves:
            if self.untie is True:
                self._sever_tie(leaf)
            else:
                self._add_tie(leaf)

    ### PRIVATE METHODS ###

    def _add_tie(self, current_leaf):
        left_broken, right_broken = None, None
        direction = self.direction
        if direction is None:
            direction = abjad.Right
        current_tie = abjad.inspect(current_leaf).get_spanner(abjad.Tie)
        if direction == abjad.Right:
            next_leaf = abjad.inspect(current_leaf).get_leaf(1)
            if next_leaf is None:
                right_broken = True
                new_leaves = list(current_tie.leaves)
                new_tie = abjad.new(current_tie)
            else:
                next_tie = abjad.inspect(next_leaf).get_spanner(abjad.Tie)
                if current_tie is not None and next_tie is not None:
                    if current_tie is next_tie:
                        return
                    else:
                        new_leaves = list(current_tie) + list(next_tie)
                        new_tie = abjad.new(current_tie)
                elif current_tie is not None and next_tie is None:
                    new_leaves = list(current_tie) + [next_leaf]
                    new_tie = abjad.new(current_tie)
                elif current_tie is None and next_tie is not None:
                    new_leaves = [current_leaf] + list(next_tie)
                    new_tie = abjad.Tie(repeat=self.repeat)
                else:
                    assert current_tie is None and next_tie is None
                    new_leaves = [current_leaf, next_leaf]
                    new_tie = abjad.Tie(repeat=self.repeat)
        else:
            previous_leaf = abjad.inspect(current_leaf).get_leaf(-1)
            if previous_leaf is None:
                left_broken = True
                new_leaves = list(current_tie.leaves)
                new_tie = abjad.new(current_tie)
            else:
                previous_tie = abjad.inspect(previous_leaf).get_spanner(
                    abjad.Tie)
                if previous_tie is not None and current_tie is not None:
                    if previous_tie is current_tie:
                        return
                    else:
                        new_leaves = list(previous_tie) + list(current_tie)
                        new_tie = abjad.new(previous_tie)
                elif previous_tie is not None and current_tie is None:
                    new_leaves = list(previous_tie) + [current_leaf]
                    new_tie = abjad.new(previous_tie)
                elif previous_tie is None and current_tie is not None:
                    new_leaves = [previous_leaf] + list(current_tie)
                    new_tie = abjad.Tie(repeat=self.repeat)
                else:
                    assert previous_tie is None and current_tie is None
                    new_leaves = [previous_leaf, current_leaf]
                    new_tie = abjad.Tie(repeat=self.repeat)
        new_leaves = abjad.select(new_leaves)
        for leaf in new_leaves:
            abjad.detach(abjad.Tie, leaf)
        abjad.attach(
            new_tie,
            new_leaves,
            left_broken=left_broken,
            right_broken=right_broken,
            tag='TCC',
            )

    def _sever_tie(self, current_leaf):
        current_tie = abjad.inspect(current_leaf).get_spanner(abjad.Tie)
        if current_tie is None:
            return
        direction = self.direction
        if direction is None:
            direction = abjad.Right
        leaf_index = current_tie.index(current_leaf)
        current_tie._fracture(leaf_index, direction=direction)
            
    ### PUBLIC PROPERTIES ###

    @property
    def direction(self):
        r'''Gets direction.

        Defaults to none.

        Interprets none equal to right.

        Set to left, right or none.
        '''
        return self._direction

    @property
    def repeat(self):
        r'''Is true when newly created ties should be repeat ties.

        Defaults to none.

        Set to true, false or none.
        '''
        return self._repeat

    @property
    def untie(self) -> Union[bool, None]:
        r'''Is true when command severs tie instead of creating tie.

        Defaults to none.
        '''
        return self._untie
