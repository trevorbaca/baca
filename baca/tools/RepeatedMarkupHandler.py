# -*- coding: utf-8 -*-
import abjad
from baca.tools.ArticulationHandler import ArticulationHandler


class RepeatedMarkupHandler(ArticulationHandler):
    r'''Repeated markup handler.

    ::

        >>> import baca

    ..  container:: example

        **Example 1.** Attaches markup to every leaf:

        ::

            >>> handler = baca.tools.RepeatedMarkupHandler(
            ...     markups=[Markup('sec.', direction=Up)],
            ...     )
            >>> staff = Staff("c'4 d' e' f'")
            >>> logical_ties = iterate(staff).by_logical_tie(pitched=True)
            >>> logical_ties = list(logical_ties)
            >>> handler(logical_ties)
            >>> show(staff)  # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4 ^ \markup { sec. }
                d'4 ^ \markup { sec. }
                e'4 ^ \markup { sec. }
                f'4 ^ \markup { sec. }
            }

    '''

    ### CLASS ATTRIBUTES ###

    __documentation_section__ = 'Handlers'

    __slots__ = (
        '_markups',
        )

    ### INITIALIZER ###

    def __init__(self, markups=None):
        if markups is not None:
            markups = [abjad.markuptools.Markup(_) for _ in markups]
            markups = tuple(markups)
        self._markups = markups

    ### SPECIAL METHODS ###

    def __call__(self, logical_ties):
        r'''Calls handler on `logical_ties`.

        Returns none.
        '''
        markups = abjad.datastructuretools.CyclicTuple(self.markups)
        for i, logical_tie in enumerate(logical_ties):
            markup = markups[i]
            markup = abjad.markuptools.Markup(markup)
            abjad.attach(markup, logical_tie.head)

    ### PUBLIC PROPERTIES ###

    @property
    def markups(self):
        r'''Gets markups of handler.

        Returns tuple or none.
        '''
        return self._markups