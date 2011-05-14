from abjad.tools import durtools
from abjad.tools import pitchtools
from fractions import Fraction


class ArticulationsSpecifier(object):
   '''Articulations specifier.
   '''

   def __init__(self, minimum_prolated_duration = None, maximum_prolated_duration = None,
      minimum_written_pitch = None, maximum_written_pitch = None):
      if minimum_prolated_duration is None:
         self.minimum_prolated_duration = minimum_prolated_duration
      else:
         self.minimum_prolated_duration = Fraction(
            *durtools.duration_token_to_duration_pair(minimum_prolated_duration))
      if maximum_prolated_duration is None:
         self.maximum_prolated_duration = maximum_prolated_duration
      else:
         self.maximum_prolated_duration = Fraction(
            *durtools.duration_token_to_duration_pair(maximum_prolated_duration))
      if minimum_written_pitch is None:
         self.minimum_written_pitch = minimum_written_pitch
      else:
         self.minimum_written_pitch = pitchtools.NamedChromaticPitch(minimum_written_pitch)
      if maximum_written_pitch is None:
         self.maximum_written_pitch = maximum_written_pitch
      else:
         self.maximum_written_pitch = pitchtools.NamedChromaticPitch(maximum_written_pitch)

   ## OVERLOADS ##

   def __repr__(self):
      return '%s( )' % self.__class__.__name__
