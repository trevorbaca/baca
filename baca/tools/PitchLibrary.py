# -*- coding: utf-8 -*-
import abjad
import baca


class PitchLibrary(object):
    r'''Pitch interface.

    ::

        >>> import abjad
        >>> import baca

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Library'

    ### PUBLIC METHODS ###

    @staticmethod
    def arpeggiate_down(pattern=None):
        return baca.tools.ArpeggiationSpacingSpecifier(
            direction=Down,
            pattern=pattern,
            )

    @staticmethod
    def arpeggiate_up(pattern=None):
        return baca.tools.ArpeggiationSpacingSpecifier(
            direction=Up,
            pattern=pattern,
            )

    @staticmethod
    def bass_to_octave(octave_number):
        return baca.tools.RegisterToOctaveSpecifier(
            anchor=Bottom,
            octave_number=octave_number,
            )

    @staticmethod
    def center_to_octave(octave_number):
        return baca.tools.RegisterToOctaveSpecifier(
            anchor=Center,
            octave_number=octave_number,
            )

    @staticmethod
    def chord():
        return baca.tools.SimultaneitySpecifier()

    @staticmethod
    def chord_spacing_down(bass=None, pattern=None, soprano=None):
        return baca.tools.ChordalSpacingSpecifier(
            bass=bass,
            direction=Down,
            pattern=pattern,
            soprano=soprano,
            )

    @staticmethod
    def chord_spacing_up(bass=None, pattern=None, soprano=None):
        return baca.tools.ChordalSpacingSpecifier(
            bass=bass,
            direction=Up,
            pattern=pattern,
            soprano=soprano,
            )

    @staticmethod
    def clef(name):
        clef = abjad.Clef(name)
        return baca.wrap.leaves(clef)

    @staticmethod
    def coat(argument):
        r'''Coats `argument`.
        '''
        return baca.tools.Coat(argument)

    @staticmethod
    def constellate(cells, range, flatten=True):
        '''Constellates `cells` in `range`.

        ..  container:: example

            ::

                >>> pitches = [[0, 2, 10], [16, 19, 20]]
                >>> range_ = abjad.PitchRange('[C4, C#7]')
                >>> segments = baca.constellate(pitches, range_)
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
                >>> segments = baca.constellate(pitches, range_)
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
    def invert_segments(axis=None):
        operator = baca.pitch_class_segment().invert(axis=axis)
        expression = baca.sequence().map(operator)
        return baca.tools.FigurePitchSpecifier(
            expressions=[expression],
            to_pitch_classes=True,
            )

    @staticmethod
    def pitches(source, allow_repeat_pitches=True):
        return baca.tools.ScorePitchSpecifier(
            allow_repeat_pitches=True,
            source=source,
            )

    @staticmethod
    def register(start_pitch, stop_pitch=None):
        if stop_pitch is None:
            return baca.tools.RegisterSpecifier(
                registration=abjad.Registration(
                    [('[A0, C8]', start_pitch)],
                    ),
                )
        return baca.tools.RegisterInterpolationSpecifier(
            start_pitch=start_pitch,
            stop_pitch=stop_pitch
            )

    @staticmethod
    def remove_duplicate_pitch_classes():
        return baca.tools.FigurePitchSpecifier(
            remove_duplicate_pitch_classes=True,
            )

    @staticmethod
    def remove_duplicate_pitches():
        return baca.tools.FigurePitchSpecifier(
            remove_duplicate_pitches=True,
            )

    @staticmethod
    def soprano_to_octave(octave_number):
        return baca.tools.RegisterToOctaveSpecifier(
            anchor=Top,
            octave_number=octave_number,
            )

    @staticmethod
    def transpose(n=0):
        return baca.tools.ScorePitchSpecifier(
            operators=[abjad.Transposition(n=n)],
            )

    @staticmethod
    def transpose_segments(n=0):
        operator = baca.pitch_class_segment().transpose(n=n)
        expression = baca.sequence().map(operator)
        return baca.tools.FigurePitchSpecifier(
            expressions=[expression],
            to_pitch_classes=True,
            )
