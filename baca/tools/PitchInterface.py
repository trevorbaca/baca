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
    def constellate(cells, range, flatten=True):
        '''Constellates `cells` in `range`.

        ..  container:: example

            ::

                >>> pitches = [[0, 2, 10], [16, 19, 20]]
                >>> range_ = abjad.PitchRange('[C4, C#7]')
                >>> segments = baca.pitch.constellate(pitches, range_)
                >>> for segment in segments:
                ...     segment
                Sequence([0, 2, 4, 7, 8, 10])
                Sequence([0, 2, 10, 16, 19, 20])
                Sequence([0, 2, 10, 28, 31, 32])
                Sequence([4, 7, 8, 12, 14, 22])
                Sequence([12, 14, 16, 19, 20, 22])
                Sequence([12, 14, 22, 28, 31, 32])
                Sequence([4, 7, 8, 24, 26, 34])
                Sequence([16, 19, 20, 24, 26, 34])
                Sequence([24, 26, 28, 31, 32, 34])

        ..  container:: example

            ::

                >>> pitches = [[4, 8, 11], [7, 15, 17]]
                >>> range_ = abjad.PitchRange('[C4, C#7]')
                >>> segments = baca.pitch.constellate(pitches, range_)
                >>> for segment in segments:
                ...     segment
                Sequence([4, 7, 8, 11, 15, 17])
                Sequence([4, 8, 11, 19, 27, 29])
                Sequence([7, 15, 16, 17, 20, 23])
                Sequence([16, 19, 20, 23, 27, 29])
                Sequence([7, 15, 17, 28, 32, 35])
                Sequence([19, 27, 28, 29, 32, 35])

        Returns outer product of octave transpositions of `cells` in `range`.
        '''
        if not isinstance(range, abjad.PitchRange):
            message = 'must be pitch range: {!r}.'
            message = message.format(range)
            raise TypeError(message)
        transposition_list = []
        for cell in cells:
            transpositions = range.list_octave_transpositions(cell)
            transposition_list.append(transpositions)
        enumeration = abjad.sequencetools.Enumeration(transposition_list)
        result = enumeration.yield_outer_product()
        result = list(result)
        if flatten:
            for i, part in enumerate(result):
                result[i] = baca.Sequence(part).flatten()
        for i, cell in enumerate(result[:]):
            result[i] = cell.sort()
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
