# -*- coding: utf-8 -*-
import abjad
import baca


class SelectLibrary(object):
    r'''Select interface.

    ::

        >>> import abjad
        >>> import baca

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Library'

    ### PUBLIC METHODS ###

    @staticmethod
    def chord(n=0):
        selector = abjad.select()
        selector = selector.by_class(flatten=True, prototype=abjad.Chord)
        selector = selector.get_item(n, apply_to_each=False)
        return selector

    @staticmethod
    def first_leaf():
        selector = abjad.select()
        selector = selector.by_leaf(flatten=True)
        selector = selector.get_slice(stop=1, apply_to_each=False)
        return selector

    @staticmethod
    def leaf(n=0):
        selector = abjad.select()
        selector = selector.by_leaf(flatten=True)
        selector = selector.get_item(n, apply_to_each=False)
        return selector

    @staticmethod
    def logical_tie(n=0):
        selector = abjad.select()
        selector = selector.by_logical_tie(flatten=True)
        selector = selector.get_item(n, apply_to_each=False)
        return selector

    @staticmethod
    def note(n=0):
        selector = abjad.select()
        selector = selector.by_class(flatten=True, prototype=abjad.Note)
        selector = selector.get_item(n, apply_to_each=False)
        return selector

    @staticmethod
    def pitched_logical_tie(n=0):
        selector = abjad.select()
        selector = selector.by_logical_tie(flatten=True, pitched=True)
        selector = selector.get_item(n, apply_to_each=False)
        return selector

    @staticmethod
    def pitched_logical_ties(n=0):
        selector = abjad.select()
        selector = selector.by_logical_tie(flatten=True, pitched=True)
        if 0 <= n:
            selector = selector.get_slice(stop=n, apply_to_each=False)
        else:
            selector = selector.get_slice(start=n, apply_to_each=False)
        return selector

    @staticmethod
    def rest(n=0):
        selector = abjad.select()
        selector = selector.by_class(flatten=True, prototype=abjad.Rest)
        selector = selector.get_item(n, apply_to_each=False)
        return selector

    @staticmethod
    def stages(stage_start_number, stage_stop_number=None):
        if stage_stop_number is None:
            stage_stop_number = stage_start_number
        return baca.tools.StageExpression(
            stage_start_number=stage_start_number, 
            stage_stop_number=stage_stop_number,
            )
