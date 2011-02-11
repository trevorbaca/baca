from abjad.components import Chord
from abjad.tools import chordtools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools import seqtools
from baca.pitch.constellate import constellate
from fractions import Fraction


class Constellation(object):

   def __init__(self, circuit, partitioned_generator_pnl):
      self._circuit = circuit
      self._partitioned_generator_pnl = partitioned_generator_pnl
      self._constellate_partitioned_generator_pnl( )
      self._chord_duration = Fraction(1, 4)
      self._chords = [ ]

   ## OVERLOADS ##

   def __contains__(self, chord):
      for pnl in self._pitch_number_lists:
         if tuple(pnl) == chord.numbers:
            return True
      return False

   def __getitem__(self, i):
      return self._pitch_number_lists[i]

   def __len__(self):
      return len(self._pitch_number_lists)

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, len(self))

   ## PRIVATE ATTRIBUTES ##

   @property
   def _color_map(self):
      pitches = self._partitioned_generator_pnl
      colors = ['red', 'blue', 'green']
      return pitchtools.NumericPitchClassColorMap(pitches, colors)

   @property
   def _colored_generator(self):
      generator = self.generator
      chordtools.color_chord_note_heads_by_numeric_pitch_class(generator, self._color_map)
      return generator

   @property
   def _constellation_number(self):
      constellation_index = self._circuit._constellations.index(self)
      constellation_number = constellation_index + 1
      return constellation_number

   @property
   def _generator_number(self):
      return self.get_chord_number(self.generator)

   @property
   def _generator_pnl(self):
      return list(sorted(seqtools.flatten_sequence(self._partitioned_generator_pnl)))

   @property
   def _next(self):
      return self._advance(1)

   @property
   def _pivot_number(self):
      pivot = self.pivot
      return self.get_chord_number(pivot)

   @property
   def _prev(self):
      return self._advance(-1)

   ## PRIVATE METHODS ##

   def _advance(self, i):
      my_idx = self._circuit._constellations.index(self) 
      len_circuit = len(self._circuit)
      next_idx = (my_idx + i) % len_circuit
      next_constellation = self._circuit._constellations[next_idx]
      return next_constellation

   def _constellate_partitioned_generator_pnl(self):
      self._pitch_number_lists = constellate(self._partitioned_generator_pnl, self.pitch_range)

   def _label_chord(self, chord):
      chord_number = self.get_chord_number(chord)
      label = '%s-%s' % (self._constellation_number, chord_number)
      #if not getattr(chord, '_already_ed', None):
      #   chord.markup.up.append(label)
      #   chord._already_labeled = True
      markuptools.Markup(label)(chord)

   def _show_chords(self, chords):
      score, treble, bass = scoretools.make_piano_sketch_score_from_leaves(chords)
      score.spacing.proportional_notation_duration = Fraction(1, 20)
      score.lily_file.default_paper_size = 'letter', 'landscape'
      score.lily_file.global_staff_size = 18
      score.text.staff_padding = 10
      show(score.lily_file)

   ## PUBLIC ATTRIBUTES ##

   @property
   def generator(self):
      pitch_numbers = self._generator_pnl
      generator = Chord(pitch_numbers, (1, 4))
      self._label_chord(generator)
      return generator

   @property
   def number(self):
      return self._circuit._constellations.index(self) + 1

   @property
   def pitch_range(self):
      return self._circuit.pitch_range

   @property
   def pivot(self):
      next_pitch_number_list = self._next._generator_pnl
      pivot = Chord(next_pitch_number_list, (1, 4))
      self._label_chord(pivot)
      return pivot

   ## PUBLIC METHODS ##

   ## Maybe should be named self.get_chord_number( ) ##
   def get(self, chord_number):
      '''1-indexed chord number.'''
      assert 1 <= chord_number
      chord_index = chord_number - 1
      return self._pitch_number_lists[chord_index]

   def get_chord_number(self, arg):
      #arg_numbers = arg.numbers
      arg_numbers = tuple([abs(x) for x in arg.pitches])
      for pnl_index, pnl in enumerate(self):
         if tuple(pnl) == arg_numbers:
            pnl_number = pnl_index + 1
            return pnl_number
      raise ValueError('%s not in %s' % (arg, self))

   def make_chords(self):
      result = [ ]
      for pitch_number_list in self._pitch_number_lists:
         chord = Chord(pitch_number_list, self._chord_duration)
         result.append(chord)
      return result

   def make_labeled_chords(self):
      result = self.make_chords( )
      for chord in result:
         self._label_chord(chord)
      return result

   def make_labeled_colored_chords(self):
      result = self.make_labeled_chords( )
      for chord in result:
         chordtools.color_chord_note_heads_by_numeric_pitch_class(chord, self._color_map)
      return result

   def show_generator(self):
      generator = self.generator
      self._label_chord(generator)
      self._show_chords([generator])

   def show_generator_and_pivot(self):
      generator = self.generator
      self._label_chord(generator)
      pivot = self.pivot
      self._label_chord(pivot)
      self._show_chords([generator, pivot])

   def show_generator_colored(self):
      colored_generator = self._colored_generator
      self._label_chord(colored_generator)
      self._show_chords([colored_generator])

   def show_generator_colored_and_pivot(self):
      colored_generator = self._colored_generator
      self._label_chord(colored_generator)
      pivot = self.pivot
      self._label_chord(pivot)
      self._show_chords([colored_generator, pivot])

   def show_pivot(self):
      pivot = self.pivot
      self._label_chord(pivot)
      self._show_chords([pivot])
