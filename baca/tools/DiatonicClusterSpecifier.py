# -*- coding: utf-8 -*-
import abjad


class DiatonicClusterSpecifier(abjad.abctools.AbjadObject):
    r'''Diatonic cluster specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c' d' e' f'")
            >>> specifier = baca.tools.DiatonicClusterSpecifier(
            ...     cluster_widths=[4, 6],
            ...     )
            >>> specifier(staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                <c' d' e' f'>4
                <d' e' f' g' a' b'>4
                <e' f' g' a'>4
                <f' g' a' b' c'' d''>4
            }

    '''

    ### CLASS ATTRIBUTES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_cluster_widths',
        ) 

    ### INITIALIZER ###

    def __init__(self, cluster_widths=None):
        if cluster_widths is not None:
            cluster_widths = abjad.datastructuretools.CyclicTuple(
                cluster_widths)
        self._cluster_widths = cluster_widths

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        r'''Calls specifier on `argument`.

        Returns none.
        '''
        for i, note in enumerate(
            abjad.iterate(argument).by_class(abjad.Note)):
            cluster_width = self.cluster_widths[i]
            start = note.written_pitch.diatonic_pitch_number
            diatonic_numbers = range(start, start + cluster_width)
            chromatic_numbers = [
                (12 * (x // 7)) +
                abjad.pitchtools.PitchClass._diatonic_pitch_class_number_to_pitch_class_number[
                    x % 7]
                for x in diatonic_numbers
                ]
            chord_pitches = [abjad.NamedPitch(_) for _ in chromatic_numbers]
            chord = abjad.Chord(note)
            chord.note_heads[:] = chord_pitches
            abjad.mutate(note).replace(chord)

    ### PUBLIC PROPERTIES ###

    @property
    def cluster_widths(self):
        r'''Gets cluster widths.

        Defaults to none.

        Set to positive integers or none.

        Returns tuple of positive integers or none.
        '''
        return self._cluster_widths
