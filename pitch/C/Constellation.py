from abjad.tools import listtools
from baca.pitch import constellate


class Constellation(object):

   def __init__(self, starting_partition, total_range):
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

   ## PRIVATE METHODS ##

   def _constellate_starting_partition(self):
      self._chords = constellate(self.starting_partition, self.total_range)

   ## PUBLIC ATTRIBUTES ##

   @property
   def portal_chord(self):
      return list(sorted(listtools.flatten(self.starting_partition)))

   @property
   def starting_partition(self):
      return self._starting_partition

   @property
   def total_range(self):
      return self._total_range

   ## PUBLIC METHODS ##

   def number(self, chord):
      return self._chords.index(chord) + 1
