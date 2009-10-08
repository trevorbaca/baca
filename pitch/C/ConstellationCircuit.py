from abjad.markup import Markup
from abjad.rational import Rational
from abjad.tools import listtools
from abjad.tools import lilytools
from abjad.tools import scoretools
from abjad.tools.io.show import show
from Constellation import Constellation


class ConstellationCircuit(object):

   def __init__(self, starting_partitions, total_range):
      self._starting_partitions = starting_partitions
      self._total_range = total_range
      self._constellate_starting_partitions( )

   ## OVERLOADS ##

   def __getitem__(self, i):
      if isinstance(i, int):
         if i < 1:
            raise IndexError('list index out of range')
         return self._constellations[i - 1]

   def __len__(self):
      return len(self._constellations)

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, len(self))

   ## PRIVATE METHODS ##

   def _constellate_starting_partitions(self):
      self._constellations = [ ]
      for i, starting_partition in enumerate(self.starting_partitions):
         constellation_number = i + 1
         constellation = Constellation(
            constellation_number, starting_partition, self.total_range)
         constellation._circuit = self
         self._constellations.append(constellation)

   def _show_chords(self, chords):
      score, treble, bass = \
         scoretools.make_piano_sketch_score(chords)
      score.spacing.proportional_notation_duration = Rational(1, 24)
      score.lily_file.default_paper_size = 'letter', 'landscape'
      score.lily_file.global_staff_size = 18
      score.text.staff_padding = 10
      show(score.lily_file)

   ## PUBLIC ATTRIBUTES ##

   @property
   def colored_generators(self):
      result = [ ]
      for i in range(1, len(self) + 1):
         result.append(self[i].colored_generator)
      return result
         
   @property
   def generators(self):
      result = self.starting_partitions[:]
      result = [listtools.flatten(partition) for partition in result]
      result = [list(sorted(portal)) for portal in result]
      return result

   @property
   def generator_labels(self):
      result = [ ]
      generator_numbers = self.generator_numbers
      for i in range(len(self)):
         constellation_number = i + 1
         generator_number = generator_numbers[i]
         label = '%s-%s' % (constellation_number, generator_number)
         result.append(label)
      return result
      
   @property
   def generator_numbers(self):
      result = [ ]
      constellations = self._constellations
      generators = self.generators
      for i in range(len(constellations)):
         constellation = self[i + 1]
         generator = generators[i]
         generator_number = constellation.get_chord_number(generator)
         result.append(generator_number)
      return result

   @property
   def pivots(self):
      result = [ ]
      for i in range(1, len(self) + 1):
         result.append(self[i].pivot)
      return result
         
   @property
   def starting_partitions(self):
      return self._starting_partitions

   @property
   def total_range(self):
      return self._total_range

   ## PUBLIC METHODS ##

   def show_generators(self):
      self._show_chords(self.colored_generators)

   def show_generators_and_pivots(self):
      chords = zip(self.colored_generators, self.pivots)
      chords = listtools.flatten(chords, depth = 1)
      self._show_chords(chords)

   def show_pivots(self):
      self._show_chords(self.pivots)
