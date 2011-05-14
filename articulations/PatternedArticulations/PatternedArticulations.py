from abjad.components import Chord
from abjad.components import Note
from abjad.tools import leaftools
from abjad.tools import marktools
from abjad.tools import seqtools
from baca.articulations.ArticulationsSpecifier import ArticulationsSpecifier


class PatternedArticulations(ArticulationsSpecifier):
   '''Patterned articulations.
   '''

   def __init__(self, articulations = None, 
      minimum_prolated_duration = None, maximum_prolated_duration = None,
      minimum_written_pitch = None, maximum_written_pitch = None):
      ArticulationsSpecifier.__init__(self, 
         minimum_prolated_duration = minimum_prolated_duration, 
         maximum_prolated_duration = maximum_prolated_duration,
         minimum_written_pitch = minimum_written_pitch,
         maximum_written_pitch = maximum_written_pitch)
      if articulations is None:
         articulations = [ ]
      self.articulations = articulations

   ## OVERLOADS ##

   def __call__(self, articulations):
      new = type(self)( )
      new.articulations = articulations
      return new

   ## PUBLIC ATTRIBUTES ##

   @apply
   def articulations( ):
      def fget(self):
         return self._articulations
      def fset(self, articulations):
         if all([isinstance(x, str) for x in articulations]):
            self._articulations = articulations
         else:
            raise TypeError(articulations)
      return property(**locals( ))

   ## PUBLIC METHODS ##

   def apply(self, expr, offset = 0, skip_first = 0, skip_last = 0):
      articulations = seqtools.CyclicList(self.articulations)
      notes_and_chords = list(leaftools.iterate_notes_and_chords_forward_in_expr(expr))
      notes_and_chords = notes_and_chords[skip_first:]
      if skip_last:
         notes_and_chords = notes_and_chords[:-skip_last]
      for i, note_or_chord in enumerate(notes_and_chords):
         articulation = articulations[offset+i]
         if self.minimum_prolated_duration is not None:
            if note_or_chord.duration.prolated < self.minimum_prolated_duration:
               continue
         if self.maximum_prolated_duration is not None:
            if self.maximum_prolated_duration < note_or_chord.duration.prolated:
               continue
         if self.minimum_written_pitch is not None:
            if isinstance(note_or_chord, Note):
               minimum_written_pitch = note_or_chord.pitch
            else:
               minimum_written_pitch = note_or_chord.pitches[0]
            if minimum_written_pitch < self.minimum_written_pitch:
               continue
         if self.maximum_written_pitch is not None:
            if isinstance(note_or_chord, Note):
               maximum_written_pitch = note_or_chord.pitch
            else:
               maximum_written_pitch = note_or_chord.pitches[-1]
            if self.maximum_written_pitch < maximum_written_pitch:
               continue
         marktools.apply_articulations_to_notes_and_chords_in_expr(note_or_chord, articulation)
      return expr
