from abjad.chord import Chord
from abjad.tools import chordtools
from abjad.tools import leaftools
from abjad.tools import listtools
from abjad.tools import pitchtools
from baca.pitch import constellate


class Constellation(object):

   def __init__(self, number, starting_partition, total_range):
      self._number = number
      self._starting_partition = starting_partition
      self._total_range = total_range
      self._constellate_starting_partition( )

   ## OVERLOADS ##

   def __contains__(self, arg):
      return arg in self._chords

   def __getitem__(self, i):
      if isinstance(i, int):
         if i < 1:
            raise IndexError('list index out of range')
         return self._chords[i - 1]

   def __len__(self):
      return len(self._chords)

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, len(self))

   ## PRIVATE ATTRIBUTES ##

   @property
   def _next(self):
      my_idx = self._circuit._constellations.index(self) 
      len_circuit = len(self._circuit)
      next_idx = (my_idx + 1) % len_circuit
      next_constellation = self._circuit._constellations[next_idx]
      return next_constellation

   ## TODO: remove next / prev code duplication ##

   @property
   def _prev(self):
      my_idx = self._circuit._constellations.index(self) 
      len_circuit = len(self._circuit)
      next_idx = (my_idx - 1) % len_circuit
      next_constellation = self._circuit._constellations[next_idx]
      return next_constellation

   ## PRIVATE METHODS ##

   def _constellate_starting_partition(self):
      self._chords = constellate(self.starting_partition, self.total_range)

   ## PUBLIC ATTRIBUTES ##

   @property
   def color_map(self):
      pitches = self.starting_partition
      colors = ['red', 'blue', 'green']
      return pitchtools.PitchClassColorMap(pitches, colors)

   @property
   def colored_generator(self):
      constellation_number = self.number
      chord_number = self.get_chord_number(self.generator)
      generator_label = '%s-%s' % (constellation_number, chord_number)
      generator = Chord(self.generator, (1, 4))
      chordtools.color_noteheads_by_pc(generator, self.color_map)
      generator.markup.up.append(generator_label)
      return generator

   @property
   def generator(self):
      return list(sorted(listtools.flatten(self.starting_partition)))

   @property
   def number(self):
      return self._number

   @property
   def pivot(self):
      next_generator = self._next.generator
      pivot_chord_number = self.get_chord_number(next_generator)
      pivot = self[pivot_chord_number]
      return pivot

   @property
   def starting_partition(self):
      return self._starting_partition

   @property
   def total_range(self):
      return self._total_range

   ## PUBLIC METHODS ##

   def get_chord_number(self, chord):
      return self._chords.index(chord) + 1

   def show_generator(self):
      leaftools.show_leaves([self.colored_generator])
