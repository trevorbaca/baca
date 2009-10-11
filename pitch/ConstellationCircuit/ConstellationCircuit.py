from abjad.rational import Rational
from abjad.tools import listtools
from abjad.tools import scoretools
from abjad.tools.io.show import show
from baca.pitch.Constellation import Constellation


class ConstellationCircuit(object):

   def __init__(self, partitioned_generator_pnls, pitch_range):
      self._partitioned_generator_pnls = partitioned_generator_pnls
      self._pitch_range = pitch_range
      self._constellate_partitioned_generator_pnls( )

   ## OVERLOADS ##

   def __getitem__(self, i):
      return self._constellations[i]

   def __len__(self):
      return len(self._constellations)

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, len(self))

   ## PRIVATE ATTRIBUTES ##

   @property
   def _colored_generators(self):
      result = [ ]
      for constellation in self:
         result.append(constellation._colored_generator)
      return result

   @property
   def _generator_numbers(self):
      result = [ ]
      for constellation in self:
         result.append(constellation._generator_number)
      return result

   @property
   def _pivot_numbers(self):
      result = [ ]
      for constellation in self:
         result.append(constellation._pivot_number)
      return result

   ## PRIVATE METHODS ##

   def _constellate_partitioned_generator_pnls(self):
      self._constellations = [ ]
      for i, partitioned_generator_pnl in enumerate(
         self._partitioned_generator_pnls):
         constellation_number = i + 1
         constellation = Constellation(self, partitioned_generator_pnl)
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
   def generators(self):
      result = [ ]
      for constellation in self:
         result.append(constellation.generator)
      return result

   @property
   def pivots(self):
      result = [ ]
      for constellation in self:
         result.append(constellation.pivot)
      return result
         
   @property
   def pitch_range(self):
      return self._pitch_range

   ## PUBLIC METHODS ##

   def get(self, *args):
      if len(args) == 1:
         constellation_number = args[0]
         constellation_index = constellation_number - 1
         return self._constellations[constellation_index]
      elif len(args) == 2:
         constellation_number, chord_number = args
         constellation_index = constellation_number - 1
         constellation = self._constellations[constellation_index]
         return constellation.get(chord_number)
         
   def show_generators(self):
      self._show_chords(self.generators)

   def show_generators_and_pivots(self):
      chords = zip(self.generators, self.pivots)
      chords = listtools.flatten(chords, depth = 1)
      self._show_chords(chords)

   def show_generators_colored(self):
      self._show_chords(self._colored_generators)

   def show_generators_colored_and_pivots(self):
      chords = zip(self._colored_generators, self.pivots)
      chords = listtools.flatten(chords, depth = 1)
      self._show_chords(chords)

   def show_pivots(self):
      self._show_chords(self.pivots)
