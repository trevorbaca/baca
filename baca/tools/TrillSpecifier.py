# -*- coding: utf-8 -*-
from abjad import *


class TrillSpecifier(abctools.AbjadObject):
    r'''Trill specifier.

    ..  container:: example

        **Example 1.** Trills all notes a quarter note in duration or greater:

        ::

            >>> import baca
            >>> specifier = baca.tools.TrillSpecifier(
            ...     minimum_written_duration=Duration(1, 4),
            ...     maximum_written_duration=None,
            ...     )

        ::
            
            >>> print(format(specifier))
            baca.tools.TrillSpecifier(
                is_harmonic=False,
                minimum_written_duration=durationtools.Duration(1, 4),
                )

    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_deposit_annotations',
        '_forbidden_annotations',
        '_is_harmonic',
        '_interval',
        '_maximum_written_duration',
        '_minimum_written_duration',
        '_pitch',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        deposit_annotations=None,
        forbidden_annotations=None,
        interval=None,
        is_harmonic=False,
        minimum_written_duration=None,
        maximum_written_duration=None,
        pitch=None,
        ):
        if deposit_annotations is not None:
            assert isinstance(deposit_annotations, (tuple, list))
            deposit_annotations = tuple(deposit_annotations)
        self._deposit_annotations = deposit_annotations
        if forbidden_annotations is not None:
            assert isinstance(forbidden_annotations, (tuple, list))
            assert all(isinstance(_, str) for _ in forbidden_annotations)
            forbidden_annotations = tuple(forbidden_annotations)
        self._forbidden_annotations = forbidden_annotations
        self._interval = interval
        self._is_harmonic = bool(is_harmonic)
        if minimum_written_duration is not None:
            minimum_written_duration = durationtools.Duration(
                minimum_written_duration)
        self._minimum_written_duration = minimum_written_duration
        if maximum_written_duration is not None:
            maximum_written_duration = durationtools.Duration(
                maximum_written_duration)
        self._maximum_written_duration = maximum_written_duration
        if pitch is not None:
            pitch = pitchtools.NamedPitch(pitch)
        self._pitch = pitch

    ### SPECIAL METHODS ###

    def __call__(self, logical_ties):
        for logical_tie in logical_ties:
            written_duration = durationtools.Duration(0)
            for note in logical_tie:
                written_duration += note.written_duration
            if self.minimum_written_duration is not None:
                if written_duration < self.minimum_written_duration:
                    continue
            if self.maximum_written_duration is not None:
                if self.maximum_written_duration <= written_duration:
                    continue
            spanner = spannertools.TrillSpanner(
                interval=self.interval,
                is_harmonic=self.is_harmonic,
                pitch=self.pitch,
                )
            leaves = []
            for note in logical_tie:
                leaves.append(note)
            skip_spanner = False
            for leaf in leaves:
                if self._has_forbidden_annotation(leaf):
                    skip_spanner = True
                    break
            if skip_spanner:
                continue
            next_leaf = inspect_(leaves[-1]).get_leaf(1)
            if next_leaf is not None:
                leaves.append(next_leaf)
            attach(spanner, leaves)

    def _has_forbidden_annotation(self, leaf):
        if self.forbidden_annotations is None:
            return False
        for forbidden_annotation in self.forbidden_annotations:
            if inspect_(leaf).get_annotation(forbidden_annotation):
                return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def deposit_annotations(self):
        r'''Gets annotations to deposit on affected components.

        Set to annotations or none.
        '''
        return self._deposit_annotations

    @property
    def forbidden_annotations(self):
        r'''Gets annotations that indiate a component is forbidden
        from being affected.

        Set to annotations or none.
        '''
        return self._forbidden_annotations

    @property
    def interval(self):
        r'''Gets interval of trill specifier.

        Defaults to none.

        Set to interval or none.

        Returns interval or none.
        '''
        return self._interval

    @property
    def is_harmonic(self):
        r'''Is true when trill pitch note head should format as a white
        diamond. Otherwise false.

        Defaults to false.

        Set to true or false.

        Returns true or false.
        '''
        return self._is_harmonic

    @property
    def maximum_written_duration(self):
        r'''Gets maximum written duration of trill specifier.

        Set to duration or none.
        '''
        return self._maximum_written_duration

    @property
    def minimum_written_duration(self):
        r'''Gets minimum written duration of trill specifier.

        Set to duration or none.
        '''
        return self._minimum_written_duration

    @property
    def pitch(self):
        r'''Gets pitch of trill specifier.

        Set to pitch or none.
        '''
        return self._pitch