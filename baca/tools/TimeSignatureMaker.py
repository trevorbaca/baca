# -*- coding: utf-8 -*-
import baca
from abjad import *


class TimeSignatureMaker(object):
    r'''Time signature maker.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_repeat_count',
        '_rotation',
        '_stage_specifier',
        '_tempo_map',
        '_time_signatures',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        time_signatures,
        repeat_count=None,
        rotation=None,
        stage_specifier=None,
        tempo_map=None,
        ):
        self._time_signatures = time_signatures 
        self._rotation = rotation
        self._stage_specifier = stage_specifier
        self._tempo_map = tempo_map
        self._repeat_count = repeat_count

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls time signature maker.

        Returns measures per stage, tempo map and time signatures.
        '''
        time_signatures = sequence(self.time_signatures)
        time_signatures = time_signatures.rotate(self.rotation)
        time_signatures = time_signatures.flatten(depth=1)
        items = []
        for item in self.stage_specifier:
            if isinstance(item, Fermata):
                item = TimeSignature((1, 4))
            items.append(item)
        stage_specifier = baca.tools.StageSpecifier(items=items)
        preprocessor = baca.tools.TimeSignaturePreprocessor(
            repeat_count=self.repeat_count,
            stage_specifier=stage_specifier,
            time_signatures=time_signatures,
            )
        time_signature_groups = preprocessor()
        measures_per_stage = [len(_) for _ in time_signature_groups]
        time_signatures = sequencetools.flatten_sequence(
            time_signature_groups,
            depth=1,
            )
        fermata_entries = self.stage_specifier.make_fermata_entries()
        items = self.tempo_map.items + fermata_entries
        tempo_map = baca.tools.TempoMap(items=items)
        return measures_per_stage, tempo_map, time_signatures

    ### PUBLIC PROPERTIES ###

    @property
    def repeat_count(self):
        r'''Gets repeat count.
        '''
        return self._repeat_count

    @property
    def rotation(self):
        r'''Gets rotation.
        '''
        return self._rotation

    @property
    def stage_specifier(self):
        r'''Gets stage specifier.
        '''
        return self._stage_specifier

    @property
    def tempo_map(self):
        r'''Gets tempo map.
        '''
        return self._tempo_map

    @property
    def time_signatures(self):
        r'''Gets time signatures.
        '''
        return self._time_signatures