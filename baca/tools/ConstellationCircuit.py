# -*- coding: utf-8 -*-
import abjad
import baca


class ConstellationCircuit(abjad.abctools.AbjadObject):
    r'''Constellation circuit.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    ### INITIALIZER ###

    def __init__(self, partitioned_generator_pnls, pitch_range):
        self._partitioned_generator_pnls = partitioned_generator_pnls
        self._pitch_range = pitch_range
        self._constellate_partitioned_generator_pnls()

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        return self._constellations[i]

    def __len__(self):
        return len(self._constellations)

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, len(self))

    ### PRIVATE PROPERTIES ###

    ## FIXME
    @property
    def _colored_generator_chords(self):
        result = []
        for constellation in self:
            result.append(constellation._colored_generator_chord)
        return result

    @property
    def _generator_chord_numbers(self):
        result = []
        for constellation in self:
            result.append(constellation._generator_chord_number)
        return result

    @property
    def _pivot_chord_numbers(self):
        result = []
        for constellation in self:
            result.append(constellation._pivot_chord_number)
        return result

    ### PRIVATE METHODS ###

    def _constellate_partitioned_generator_pnls(self):
        self._constellations = []
        enumeration = enumerate(self._partitioned_generator_pnls)
        for i, partitioned_generator_pnl in enumeration:
            constellation_number = i + 1
            constellation = baca.tools.Constellation(
                self,
                partitioned_generator_pnl,
                )
            self._constellations.append(constellation)

    def _make_lilypond_file_and_score_from_chords(self, chords):
        result = abjad.scoretools.make_piano_sketch_score_from_leaves(chords)
        score, treble, bass = result
        score.override.text_script.staff_padding = 10
        moment = abjad.schemetools.SchemeMoment(1, 30)
        score.set.proportional_notation_duration = moment
        lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(score)
        lilypond_file.default_paper_size = 'letter', 'landscape'
        lilypond_file.global_staff_size = 18
        lilypond_file.layout_block.indent = 0
        lilypond_file.layout_block.ragged_right = True
        vector = layouttools.make_spacing_vetor(0, 0, 12, 0)
        lilypond_file.paper_block.system_system_spacing = vector
        lilypond_file.paper_block.top_margin = 24
        return lilypond_file, score

    def _show_chords(self, chords):
        result = self._make_lilypond_file_and_score_from_chords(chords)
        lilypond_file, score = result
        show(lilypond_file)

    ### PUBLIC PROPERTIES ###

    @property
    def generator_chords(self):
        result = []
        for constellation in self:
            result.append(constellation.generator_chord)
        return result

    @property
    def pitch_range(self):
        return self._pitch_range

    @property
    def pivot_chords(self):
        result = []
        for constellation in self:
            result.append(constellation.pivot_chord)
        return result

    ### PUBLIC METHODS ###

    def get(self, *args):
        if len(args) == 1:
            constellation_number = args[0]
            constellation_index = constellation_number - 1
            return self._constellations[constellation_index]
        elif len(args) == 2:
            constellation_number, chord_number = args
            constellation_index = constellation_number - 1
            constellation = self._constellations[constellation_index]
            return constellation.get_chord(chord_number)

    def show_colored_generator_chords(self):
        self._show_chords(self._colored_generator_chords)

    def show_colored_generator_chords_and_pivot_chords(self):
        chords = zip(self._colored_generators, self.pivot_chords)
        chords = abjad.sequencetools.flatten_sequence(chords, depth = 1)
        self._show_chords(chords)

    def show_generator_chords(self):
        self._show_chords(self.generator_chords)

    def show_generator_chords_and_pivot_chords(self):
        chords = zip(self.generator_chords, self.pivot_chords)
        chords = abjad.sequencetools.flatten_sequence(chords, depth = 1)
        self._show_chords(chords)

    def show_pivot_chords(self):
        self._show_chords(self.pivot_chords)
