from abjad.tools.chordtools import Chord
from abjad.tools import chordtools
from abjad.tools import iotools
from abjad.tools import lilyfiletools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools import schemetools
from abjad.tools import scoretools
from abjad.tools import sequencetools
from baca.pitch.constellate import constellate
from fractions import Fraction


class Constellation(object):

    def __init__(self, circuit, partitioned_generator_chromatic_pitch_numbers):
        self._circuit = circuit
        self._partitioned_generator_chromatic_pitch_numbers = partitioned_generator_chromatic_pitch_numbers
        self._constellate_partitioned_generator_chromatic_pitch_numbers()
        self._chord_duration = Fraction(1, 4)
        self._chords = []

    ### OVERLOADS ###

    def __contains__(self, chord):
#      for pnl in self._pitch_number_lists:
#         if tuple(pnl) == chord.numbers:
#            return True
#      return False
        return chord in self._pitch_number_lists

    def __getitem__(self, i):
        return self._pitch_number_lists[i]

    def __len__(self):
        return len(self._pitch_number_lists)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, len(self))

    ### PRIVATE ATTRIBUTES ###

    @property
    def _color_map(self):
        pitches = self._partitioned_generator_chromatic_pitch_numbers
        colors = ['red', 'blue', 'green']
        return pitchtools.NumberedChromaticPitchClassColorMap(pitches, colors)

    @property
    def _colored_generator(self):
        generator_chord = self.generator_chord
        chordtools.color_chord_note_heads_by_pitch_class_color_map(generator_chord, self._color_map)
        return generator_chord

    @property
    def _constellation_number(self):
        constellation_index = self._circuit._constellations.index(self)
        constellation_number = constellation_index + 1
        return constellation_number

    @property
    def _generator_chord_number(self):
        return self.get_number_of_chord(self.generator_chord)

    @property
    def _generator_chromatic_pitch_numbers(self):
        return list(sorted(sequencetools.flatten_sequence(self._partitioned_generator_chromatic_pitch_numbers)))

    @property
    def _next(self):
        return self._advance(1)

    @property
    def _pivot_chord_number(self):
        pivot = self.pivot_chord
        return self.get_number_of_chord(pivot)

    @property
    def _prev(self):
        return self._advance(-1)

    ### PRIVATE METHODS ###

    def _advance(self, i):
        my_idx = self._circuit._constellations.index(self)
        len_circuit = len(self._circuit)
        next_idx = (my_idx + i) % len_circuit
        next_constellation = self._circuit._constellations[next_idx]
        return next_constellation

    def _constellate_partitioned_generator_chromatic_pitch_numbers(self):
        self._pitch_number_lists = constellate(self._partitioned_generator_chromatic_pitch_numbers, self.pitch_range)

    def _label_chord(self, chord):
        chord_number = self.get_number_of_chord(chord)
        label = '%s-%s' % (self._constellation_number, chord_number)
        #if not getattr(chord, '_already_ed', None):
        #   chord.markup.up.append(label)
        #   chord._already_labeled = True
        markuptools.Markup(label)(chord)

    def _make_lily_file_and_score_from_chords(self, chords):
        score, treble, bass = scoretools.make_piano_sketch_score_from_leaves(chords)
        score.override.text_script.staff_padding = 10
        score.set.proportional_notation_duration = schemetools.SchemeMoment(1, 30)
        lily_file = lilyfiletools.make_basic_lily_file(score)
        lily_file.default_paper_size = 'letter', 'landscape'
        lily_file.global_staff_size = 18
        lily_file.layout_block.indent = 0
        lily_file.layout_block.ragged_right = True
        lily_file.paper_block.system_system_spacing = schemetools.SchemeVector(
            schemetools.SchemePair('basic_distance', 0),
            schemetools.SchemePair('minimum_distance', 0),
            schemetools.SchemePair('padding', 12),
            schemetools.SchemePair('stretchability', 0))
        lily_file.paper_block.top_margin = 24
        return lily_file, score

    def _show_chords(self, chords):
        lily_file, score = self._make_lily_file_and_score_from_chords(chords)
        iotools.show(lily_file)

    ### PUBLIC ATTRIBUTES ###

    @property
    def constellation_number(self):
        return self._circuit._constellations.index(self) + 1

    @property
    def generator_chord(self):
        pitch_numbers = self._generator_chromatic_pitch_numbers
        generator_chord = Chord(pitch_numbers, (1, 4))
        self._label_chord(generator_chord)
        return generator_chord

    @property
    def partitioned_generator_chromatic_pitch_numbers(self):
        return self._partitioned_generator_chromatic_pitch_numbers

    @property
    def pitch_range(self):
        return self._circuit.pitch_range

    @property
    def pivot_chord(self):
        next_pitch_number_list = self._next._generator_chromatic_pitch_numbers
        pivot_chord = Chord(next_pitch_number_list, (1, 4))
        self._label_chord(pivot_chord)
        return pivot_chord

    ### PUBLIC METHODS ###

    def get_chord(self, chord_number):
        '''1-indexed chord number.'''
        assert 1 <= chord_number
        chord_index = chord_number - 1
        return self._pitch_number_lists[chord_index]

    def get_number_of_chord(self, chord):
        chord = Chord(chord, (1, 4))
        chromatic_pitch_numbers = [x.chromatic_pitch_number for x in chord.written_pitches]
        for pnl_index, pnl in enumerate(self):
            if pnl == chromatic_pitch_numbers:
                pnl_number = pnl_index + 1
                return pnl_number
        raise ValueError('%s not in %s' % (chord, self))

    def make_chords(self):
        result = []
        for pitch_number_list in self._pitch_number_lists:
            chord = Chord(pitch_number_list, self._chord_duration)
            result.append(chord)
        return result

    def make_labeled_chords(self):
        result = self.make_chords()
        for chord in result:
            self._label_chord(chord)
        return result

    def make_labeled_colored_chords(self):
        result = self.make_labeled_chords()
        for chord in result:
            chordtools.color_chord_note_heads_by_pitch_class_color_map(chord, self._color_map)
        return result

    def show_colored_generator_chord(self):
        colored_generator = self._colored_generator
        self._label_chord(colored_generator)
        self._show_chords([colored_generator])

    def show_colored_generator_chord_and_pivot_chord(self):
        colored_generator = self._colored_generator
        self._label_chord(colored_generator)
        pivot = self.pivot_chord
        self._label_chord(pivot)
        self._show_chords([colored_generator, pivot])

    def show_generator_chord(self):
        generator = self.generator_chord
        self._label_chord(generator)
        self._show_chords([generator])

    def show_generator_chord_and_pivot_chord(self):
        generator = self.generator_chord
        self._label_chord(generator)
        pivot = self.pivot_chord
        self._label_chord(pivot)
        self._show_chords([generator, pivot])

    def show_pivot_chord(self):
        pivot = self.pivot_chord
        self._label_chord(pivot)
        self._show_chords([pivot])
