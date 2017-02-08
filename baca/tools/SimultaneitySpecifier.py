# -*- coding: utf-8 -*-
import abjad
import baca


class SimultaneitySpecifier(abjad.abctools.AbjadValueObject):
    r'''Simultaneity specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> baca.tools.SimultaneitySpecifier()
            SimultaneitySpecifier()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_partition_specifier',
        )

    _publish_storage_format = True
    
    ### INITIALIZER ###

    def __init__(self, partition_specifier=None):
        self._partition_specifier = partition_specifier

    ### SPECIAL METHODS ###

    def __call__(self, pitch_classes=None):
        r'''Calls specifier on `pitch_classes`.

        ..  container:: example

            ::

                >>> specifier = baca.tools.SimultaneitySpecifier()
                >>> specifier([])
                []

        ..  container:: example

            ::

                >>> specifier = baca.tools.SimultaneitySpecifier()
                >>> specifier() is None
                True

        Returns nested sequence, empty sequence or none.
        '''
        if pitch_classes is None:
            return
        if pitch_classes == []:
            return []
        pitch_classes = baca.Sequence(pitch_classes).flatten()
        partition_specifier = self.partition_specifier
        if partition_specifier is None:
            partition_specifier = baca.tools.LMRSpecifier()
        parts = partition_specifier(pitch_classes)
        parts = [abjad.PitchSegment(_) for _ in parts]
        return baca.tools.SegmentList(segments=parts, as_chords=True)

    ### PUBLIC PROPERTIES ###

    @property
    def partition_specifier(self):
        r'''Gets partition specifier.

        ..  container:: example

            Default:

            ::

                >>> specifier = baca.tools.SimultaneitySpecifier()
                >>> specifier([[-6, -3, -5, -1, 7], [2, 4, -4]])
                SegmentList([<-6, -3, -5, -1, 7, 2, 4, -4>])

        ..  container:: example

            With LMR specifier:

            ::

                >>> specifier = baca.tools.SimultaneitySpecifier(
                ...     partition_specifier=baca.tools.LMRSpecifier(
                ...         left_length=3,
                ...         right_length=3,
                ...         ),
                ...     )
                >>> pitch_classes = [[-6, -3, -5, -1, 7], [2, 4, -4]]
                >>> for segment in specifier(pitch_classes):
                ...     segment
                ...
                PitchSegment([-6, -3, -5])
                PitchSegment([-1, 7])
                PitchSegment([2, 4, -4])

        Set to LMR specifier or partition expression.

        Returns LMR specifier, partition expression or none.
        '''
        return self._partition_specifier
