import abjad
import baca
from .Command import Command


class BowContactPointCommand(Command):
    r'''Bow contact point command.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(4) Commands'
    
    __slots__ = (
        '_bow_contact_points',
        '_rotation',
        )

    _default_bow_contact_points = (
        [(0, 7), (4, 7), (5, 7), (6, 7), (7, 7), (6, 7)],
        [(7, 7), (0, 7), (7, 7), (0, 7), (7, 7)],
        [(0, 7), (4, 7), (5, 7), (6, 7), (7, 7), (6, 7), (7, 7)],
        [(0, 4), (1, 4), (2, 4), (1, 4)],
        )

    ### INITIALIZER ###

    def __init__(self, bcps=None, rotation=None, selector=None):
        baca.Command.__init__(self, selector=selector)
        if bcps is None:
            bcps = BowContactPointCommand._default_bow_contact_points
        self._bow_contact_points = bcps
        self._rotation = rotation

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if self.selector:
            argument = self.selector(argument)
        bcps = baca.sequence(self.bow_contact_points)
        bcps = bcps.rotate(n=self.rotation)
        bcps = bcps.flatten(depth=1)
        bcps = abjad.CyclicTuple(bcps)
        leaves = baca.select(argument).leaves()
        spanner = abjad.TextSpanner()
        abjad.attach(spanner, leaves)
        lts = baca.select(argument).lts()
        total = len(lts)
        previous_bcp, i = None, 0
        for lt in lts:
            previous_leaf = abjad.inspect(lt.head).get_leaf(-1)
            if (isinstance(lt.head, abjad.Rest) and
                isinstance(previous_leaf, (abjad.Rest, type(None)))):
                continue
            if (isinstance(lt.head, abjad.Note) and
                isinstance(previous_leaf, abjad.Rest) and
                previous_bcp is not None):
                numerator, denominator = previous_bcp
            else:
                bcp = bcps[i]
                numerator, denominator = bcp
                i += 1
            markup = abjad.Markup.fraction(numerator, denominator)
            spanner.attach(markup, lt.head)
            if lts is lts[-1]:
                continue
            if isinstance(lt.head, abjad.Note):
                arrow = abjad.ArrowLineSegment()
                spanner.attach(arrow, lt.head)
            bcp_fraction = abjad.Fraction(*bcp)
            next_bcp_fraction = abjad.Fraction(*bcps[i])
            if isinstance(lt.head, abjad.Rest):
                pass
            elif isinstance(previous_leaf, abjad.Rest) or previous_bcp is None:
                if bcp_fraction > next_bcp_fraction:
                    abjad.attach(abjad.Articulation('upbow'), lt.head)
                elif bcp_fraction < next_bcp_fraction:
                    abjad.attach(abjad.Articulation('downbow'), lt.head)
            else:
                previous_bcp_fraction = abjad.Fraction(*previous_bcp)
                if previous_bcp_fraction < bcp_fraction > next_bcp_fraction:
                    abjad.attach(abjad.Articulation('upbow'), lt.head)
                elif previous_bcp_fraction > bcp_fraction < next_bcp_fraction:
                    abjad.attach(abjad.Articulation('downbow'), lt.head)
            previous_bcp = bcp

    ### PUBLIC PROPERTIES ###

    @property
    def bow_contact_points(self):
        r'''Gets bow contact points.

        ..  container:: example

            >>> command = baca.BowContactPointCommand()
            >>> for list_ in command.bow_contact_points:
            ...     list_
            ...
            [(0, 7), (4, 7), (5, 7), (6, 7), (7, 7), (6, 7)]
            [(7, 7), (0, 7), (7, 7), (0, 7), (7, 7)]
            [(0, 7), (4, 7), (5, 7), (6, 7), (7, 7), (6, 7), (7, 7)]
            [(0, 4), (1, 4), (2, 4), (1, 4)]

        Class constant.

        Returns list of list of pairs.
        '''
        return self._bow_contact_points

    @property
    def rotation(self):
        r'''Gets rotation.

        ..  container:: example

            >>> command = baca.BowContactPointCommand(rotation=-1)
            >>> command.rotation
            -1

        Returns integer or none.
        '''
        return self._rotation
