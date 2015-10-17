# -*- coding: utf-8 -*-
import copy
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import spannertools
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate


class TransitionSpecifier(AbjadObject):
    r'''Transition specifier.

    ..  container:: example

        **Example 1.** Specifies transition from ordinario to ponticello:

        ::

            >>> import baca

        ::

            >>> start_markup = Markup('ord.').upright()
            >>> stop_markup = Markup('pont.').upright()
            >>> specifier = baca.tools.TransitionSpecifier(
            ...     start_markup=start_markup,
            ...     stop_markup=stop_markup,
            ...     )

        ::

            >>> print(format(specifier))
            baca.tools.TransitionSpecifier(
                start_markup=markuptools.Markup(
                    contents=(
                        markuptools.MarkupCommand(
                            'upright',
                            'ord.'
                            ),
                        ),
                    ),
                stop_markup=markuptools.Markup(
                    contents=(
                        markuptools.MarkupCommand(
                            'upright',
                            'pont.'
                            ),
                        ),
                    ),
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_solid',
        '_start_markup',
        '_stop_markup',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        solid=None,
        start_markup=None,
        stop_markup=None,
        ):
        assert start_markup is not None or stop_markup is not None
        if solid is not None:
            solid = bool(solid)
        self._solid = solid
        self._start_markup = start_markup
        self._stop_markup = stop_markup

    ### SPECIAL METHODS ###

    def __call__(self, components):
        r'''Calls transition specifier on `components`.

        Returns none.
        '''
        if isinstance(components[0], selectiontools.LogicalTie):
            leaves = iterate(components).by_leaf()
            leaves = list(leaves)
        else:
            assert isinstance(components[0], scoretools.Leaf)
            leaves = components
        start_leaf = leaves[0]
        stop_leaf = leaves[-1]
        if self.start_markup is not None:
            start_markup = copy.copy(self.start_markup)
            start_markup = start_markup.override(('font-name', 'Palatino'))
            attach(start_markup, start_leaf, is_annotation=True)
        arrow = self._get_arrow()
        attach(arrow, start_leaf)
        if self.stop_markup is not None:
            stop_markup = copy.copy(self.stop_markup)
            stop_markup = stop_markup.override(('font-name', 'Palatino'))
            attach(stop_markup, stop_leaf, is_annotation=True)
        attach(spannertools.TextSpanner(), leaves)

    ### PRIVATE METHODS ###

    def _get_arrow(self):
        if self.solid:
            return indicatortools.Arrow()
        return self._make_dashed_arrow()

    @staticmethod
    def _make_dashed_arrow():
        return indicatortools.Arrow(
            dash_fraction=0.25,
            dash_period=1.5,
            left_broken_text=False,
            left_hspace=0.5,
            right_broken_arrow=False,
            right_broken_padding=0,
            right_padding=1.75,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def solid(self):
        r'''Is true when transition should be a solid line instead of a 
        dashed line.

        Is false when transition should be a dashed line.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._solid

    @property
    def start_markup(self):
        r'''Gets start markup of transition specifier.

        Set to markup.

        Returns markup.
        '''
        return self._start_markup

    @property
    def stop_markup(self):
        r'''Gets stop markup of transition specifier.

        Set to markup.

        Returns markup.
        '''
        return self._stop_markup