from abjad.chord import Chord
from abjad.markup import Markup
from abjad.rational import Rational
from abjad.tools import chordtools
from abjad.tools import clone
from abjad.tools import listtools
from abjad.tools import lilytools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.io.show import show
from baca.pitch.constellate import constellate


class Constellation(object):

   def __init__(self, circuit, partitioned_generator_pnl):
      self._circuit = circuit
      self._partitioned_generator_pnl = partitioned_generator_pnl
      self._constellate_partitioned_generator_pnl( )

   ## OVERLOADS ##

   def __contains__(self, chord):
      for pnl in self._chords:
         if tuple(pnl) == chord.numbers:
            return True
      return False

   def __getitem__(self, i):
      return self._chords[i]

   def __len__(self):
      return len(self._chords)

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, len(self))

   ## PRIVATE ATTRIBUTES ##

   @property
   def _color_map(self):
      pitches = self._partitioned_generator_pnl
      colors = ['red', 'blue', 'green']
      return pitchtools.PitchClassColorMap(pitches, colors)

   @property
   def _colored_generator(self):
      generator = self.generator
      chordtools.color_noteheads_by_pc(generator, self._color_map)
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
      return list(sorted(listtools.flatten(self._partitioned_generator_pnl)))

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
      pitch_number_lists = self._partitioned_generator_pnl
      self._chords = constellate(pitch_number_lists, self.pitch_range)

   def _label_chord(self, chord):
      chord_number = self.get_chord_number(chord)
      label = '%s-%s' % (self._constellation_number, chord_number)
      if not getattr(chord, '_already_labelled', None):
         chord.markup.up.append(label)
         chord._already_labelled = True

   def _show_chords(self, chords):
      score, treble, bass = \
         scoretools.make_piano_sketch_score(chords)
      score.spacing.proportional_notation_duration = Rational(1, 20)
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
      return self._chords[chord_index]

   def get_chord_number(self, arg):
      arg_numbers = arg.numbers
      for pnl_index, pnl in enumerate(self):
         if tuple(pnl) == arg_numbers:
            pnl_number = pnl_index + 1
            return pnl_number
      raise ValueError('%s not in %s' % (arg, self))

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
