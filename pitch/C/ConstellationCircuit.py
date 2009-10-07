from abjad.tools import listtools
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
      self._constellations = [
         Constellation(x, self.total_range) for x in self.starting_partitions]

   ## PUBLIC ATTRIBUTES ##

   @property
   def portal_chords(self):
      result = self.starting_partitions[:]
      result = [listtools.flatten(partition) for partition in result]
      result = [list(sorted(portal)) for portal in result]
      return result

   @property
   def portal_chord_labels(self):
      result = [ ]
      portal_chord_numbers = self.portal_chord_numbers
      for i in range(len(self)):
         constellation_number = i + 1
         portal_chord_number = portal_chord_numbers[i]
         label = '%s-%s' % (constellation_number, portal_chord_number)
         result.append(label)
      return result
      
   @property
   def portal_chord_numbers(self):
      result = [ ]
      constellations = self._constellations
      portal_chords = self.portal_chords
      for i in range(len(constellations)):
         constellation = self[i + 1]
         portal_chord = portal_chords[i]
         portal_chord_number = constellation.number(portal_chord)
         result.append(portal_chord_number)
      return result

   @property
   def starting_partitions(self):
      return self._starting_partitions

   @property
   def total_range(self):
      return self._total_range
