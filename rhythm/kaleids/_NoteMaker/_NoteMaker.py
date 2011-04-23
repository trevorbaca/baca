from baca.rhythm.kaleids._RhythmicKaleid import _RhythmicKaleid


class _NoteMaker(_RhythmicKaleid):
   '''Big-endian note maker.
   '''
   
   ## OVERLOADS ##

   def __call__(self, duration_tokens, seeds = None):
      seeds = self._handle_none_seeds(seeds)
      note_lists = self._make_note_lists(duration_tokens)
      return note_lists
