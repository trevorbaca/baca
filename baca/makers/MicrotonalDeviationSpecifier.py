# -*- coding: utf-8 -*-
import copy
import itertools
from abjad import *


class MicrotonalDeviationSpecifier(abctools.AbjadObject):
    r'''MicrotonalDeviationSpecifier specifier.

    ..  container:: example

        ::

            >>> import baca
            >>> specifier = baca.makers.MicrotonalDeviationSpecifier(
            ...     number_lists=(
            ...         [0, 0.5, 0, -0.5],
            ...         ),
            ...     )

        ::
            
            >>> print(format(specifier))
            baca.makers.MicrotonalDeviationSpecifier(
                number_lists=(
                    [0, 0.5, 0, -0.5],
                    ),
                )

    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_deposit_annotations',
        '_number_lists',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        deposit_annotations=None,
        number_lists=None,
        ):
        from abjad.tools import pitchtools
        if deposit_annotations is not None:
            deposit_annotations = tuple(deposit_annotations)
        self._deposit_annotations = deposit_annotations
        if number_lists is not None:
            number_lists = tuple(number_lists)
            for number_list in number_lists:
                assert isinstance(number_list, (list, tuple)), number_list
        self._number_lists = number_lists

    ### SPECIAL METHODS ###

    def __call__(self, logical_ties, timespan):
        if self.number_lists is None:
            return
        number_lists = datastructuretools.CyclicTuple(self.number_lists)
        number_list_index = 0
        pairs = itertools.groupby(
            logical_ties,
            lambda _: _.head.written_pitch,
            )
        for key, values in pairs:
            values = list(values)
            if len(values) == 1:
                continue
            number_list = number_lists[number_list_index]
            number_list = datastructuretools.CyclicTuple(number_list)
            for i, logical_tie in enumerate(values):
                number = number_list[i]
                for note in logical_tie:
                    self._adjust_pitch(note, number)
                    self._attach_deposit_annotations(note)
            number_list_index += 1

    ### PRIVATE METHODS ###

    def _adjust_pitch(self, note, number):
        assert number in (0.5, 0, -0.5)
        if number == 0:
            return
        written_pitch = note.written_pitch
        written_pitch = \
            pitchtools.transpose_named_pitch_by_numbered_interval_and_respell(
            written_pitch, 0, number)
        note.written_pitch = written_pitch

    def _attach_deposit_annotations(self, note):
        if not self.deposit_annotations:
            return
        for annotation_name in self.deposit_annotations:
            annotation = indicatortools.Annotation(annotation_name, True)
            attach(annotation, note)

    ### PUBLIC PROPERTIES ###

    @property
    def deposit_annotations(self):
        r'''Gets deposit annotations of specifier.

        These will be attached to every note affected at call time.

        Set to annotations or none.
        '''
        return self._deposit_annotations

    @property
    def number_lists(self):
        r'''Gets number lists of color fingering specifier.

        ..  container:: example

            ::

                >>> specifier = baca.makers.MicrotonalDeviationSpecifier(
                ...     number_lists=(
                ...         [0, 1, 2, 1],
                ...         ),
                ...     )
        
            ::

                >>> specifier.number_lists
                ([0, 1, 2, 1],)

        Set to nested list of nonnegative integers or none.
        '''
        return self._number_lists