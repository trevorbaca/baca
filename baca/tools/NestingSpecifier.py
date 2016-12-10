# -*- coding: utf-8 -*-
import abjad
import baca


class NestingSpecifier(abjad.abctools.AbjadObject):
    r'''Nesting specifier.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_lmr_specifier',
        '_time_treatments',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        lmr_specifier=None,
        time_treatments=None,
        ):
        if lmr_specifier is not None:
            prototype = baca.tools.LMRSpecifier
            assert isinstance(lmr_specifier, prototype)
        self._lmr_specifier = lmr_specifier
        if time_treatments is not None:
            assert isinstance(time_treatments, (list, tuple))
            is_time_treatment = baca.tools.FigureRhythmMaker._is_time_treatment
            for time_treatment in time_treatments:
                assert is_time_treatment(time_treatment), repr(time_treatment)
        self._time_treatments = time_treatments

    ### SPECIAL METHODS ###

    def __call__(self, selections):
        r'''Calls nesting specifier on selections.

        Returns new selections. 
        '''
        time_treatments = self._get_time_treatments()
        if time_treatments is None:
            return selections
        tuplets = []
        for selection in selections:
            if not isinstance(selection, abjad.selectiontools.Selection):
                message = 'should be selection: {!r}.'
                message = message.format(selection)
            assert len(selection) == 1, repr(selection)
            assert isinstance(selection[0], abjad.scoretools.Tuplet)
            tuplets.append(selection[0])
        if self.lmr_specifier is None:
            tuplet_selections = [abjad.select(tuplets)]
        else:
            tuplet_selections = self.lmr_specifier(tuplets)
            tuplet_selections = [
                abjad.select(list(_)) for _ in tuplet_selections]
        selections_ = []
        prototype = abjad.selectiontools.Selection
        for index, tuplet_selection in enumerate(tuplet_selections):
            assert isinstance(tuplet_selection, prototype), repr(
                tuplet_selection)
            time_treatment = time_treatments[index]
            if time_treatment is None:
                selections_.append(tuplet_selection)
            else:
                nested_tuplet = self._make_nested_tuplet(
                    tuplet_selection,
                    time_treatment,
                    )
                selection_ = abjad.selectiontools.Selection([nested_tuplet])
                selections_.append(selection_)
        return selections_

    ### PRIVATE METHODS ###

    def _get_time_treatments(self):
        if self.time_treatments:
            return abjad.datastructuretools.CyclicTuple(self.time_treatments)

    @staticmethod
    def _make_nested_tuplet(tuplet_selection, time_treatment):
        assert isinstance(tuplet_selection, abjad.selectiontools.Selection)
        for tuplet in tuplet_selection:
            assert isinstance(tuplet, abjad.scoretools.Tuplet), repr(tuplet)
        if isinstance(time_treatment, str):
            addendum = abjad.durationtools.Duration(time_treatment)
            duration = tuplet_selection.get_duration() + addendum
            tuplet = abjad.scoretools.FixedDurationTuplet(
                duration,
                tuplet_selection,
                )
        elif time_treatment.__class__ is abjad.durationtools.Multiplier:
            tuplet = abjad.scoretools.Tuplet(time_treatment, tuplet_selection)
        elif time_treatment.__class__ is abjad.durationtools.Duration:
            tuplet = abjad.scoretools.FixedDurationTuplet(
                time_treatment,
                tuplet_selection,
                )
        else:
            message = 'invalid time treatment: {!r}.'
            message = message.format(time_treatment)
            raise Exception(message)
        return tuplet

    ### PUBLIC PROPERTIES ###

    @property
    def lmr_specifier(self):
        r'''Gets LMR specifier.

        Defaults to none.

        Set to LMR specifier or none.

        Returns LMR specifier or none.
        '''
        return self._lmr_specifier

    @property
    def time_treatments(self):
        r'''Gets time treatments.

        Defaults to none.

        Set to time treatments or none.

        Returns time treatments or none.
        '''
        return self._time_treatments
