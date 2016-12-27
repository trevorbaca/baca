# -*- coding: utf-8 -*-
import abjad
import baca


class PitchInterface(object):
    r'''Pitch interface.

    ::

        >>> import abjad
        >>> import baca

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Interfaces'

    ### PUBLIC METHODS ###

    @staticmethod
    def constellate(cells, range_, flatten=True):
        '''Constellates `cells` in `range_`.

        ..  container:: example

            ::

                >>> pitches = [[0, 2, 10], [16, 19, 20]]
                >>> range_ = abjad.PitchRange('[C4, C#7]')
                >>> segments = baca.pitch.constellate(pitches, range_)
                >>> for segment in segments:
                ...     segment
                [0, 2, 4, 7, 8, 10]
                [0, 2, 10, 16, 19, 20]
                [0, 2, 10, 28, 31, 32]
                [4, 7, 8, 12, 14, 22]
                [12, 14, 16, 19, 20, 22]
                [12, 14, 22, 28, 31, 32]
                [4, 7, 8, 24, 26, 34]
                [16, 19, 20, 24, 26, 34]
                [24, 26, 28, 31, 32, 34]

        ..  container:: example

            ::

                >>> pitches = [[4, 8, 11], [7, 15, 17]]
                >>> range_ = abjad.PitchRange('[C4, C#7]')
                >>> segments = baca.pitch.constellate(pitches, range_)
                >>> for segment in segments:
                ...     segment
                [4, 7, 8, 11, 15, 17]
                [4, 8, 11, 19, 27, 29]
                [7, 15, 16, 17, 20, 23]
                [16, 19, 20, 23, 27, 29]
                [7, 15, 17, 28, 32, 35]
                [19, 27, 28, 29, 32, 35]

        Returns outer product of octave transpositions of `cells` in `range_`.
        '''
        if not isinstance(range_, abjad.PitchRange):
            message = 'must be pitch range: {!r}.'
            message = message.format(range_)
            raise TypeError(message)
        transposition_list = []
        for cell in cells:
            transpositions = range_.list_octave_transpositions(cell)
            transposition_list.append(transpositions)
        result = abjad.sequencetools.yield_outer_product_of_sequences(
            transposition_list)
        result = list(result)
        if flatten:
            for i, part in enumerate(result):
                result[i] = abjad.sequencetools.flatten_sequence(part)
        for cell in result:
            cell.sort()
        return result

    @staticmethod
    def displacement(displacements):
        return baca.tools.OctaveDisplacementSpecifier(
            displacements=displacements,
            )

    @staticmethod
    def fixed_pitches(source):
        return baca.tools.ScorePitchSpecifier(
            acyclic=True,
            source=source,
            )

    @staticmethod
    def infinite_pitches(source, repetition_intervals):
        return baca.tools.ScorePitchSpecifier(
            repetition_intervals=repetition_intervals,
            source=source,
            )

    @staticmethod
    def invert(axis=None):
        return baca.tools.ScorePitchSpecifier(
            operators=[
                abjad.Inversion(axis=axis),
                ]
            )

    @staticmethod
    def pitches(source, allow_repeated_pitches=True):
        return baca.tools.ScorePitchSpecifier(
            allow_repeated_pitches=True,
            source=source,
            )

    @staticmethod
    def protect(payload):
        r'''Protects `payload` with shell. 
        '''
        return baca.tools.Shell(payload)

    @staticmethod
    def register(start_pitch, stop_pitch=None):
        if stop_pitch is None:
            return baca.tools.RegisterSpecifier(
                registration=abjad.pitchtools.Registration(
                    [('[A0, C8]', start_pitch)],
                    ),
                )
        return baca.tools.RegisterInterpolationSpecifier(
            start_pitch=start_pitch,
            stop_pitch=stop_pitch
            )

    @staticmethod
    def transpose(n=0):
        return baca.tools.ScorePitchSpecifier(
            operators=[
                abjad.Transposition(n=n),
                ]
            )
