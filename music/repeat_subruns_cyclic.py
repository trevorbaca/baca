from abjad.note.note import Note
from abjad.tools import clone


def repeat_subruns_cyclic(notes, pairs, history = False):
   '''Repeat components according to pairs.

   >>> l = [Note(n, (1, 4)) for n in [0, 2, 4, 5, 7, 9, 11]]
   >>> draw(l, [(0, 4), (2, 4)])
   >>> l
   [c'4, d'4, e'4, f'4, c'4, d'4, e'4, f'4, 
   g'4, a'4, e'4, f'4, g'4, a'4, b'4]'''

   assert all([isinstance(x, Note) for x in notes])
   assert isinstance(pairs, list)
   assert all([len(x) == 3 for x in pairs])

   instructions = [ ]
   len_notes = len(notes)
   for pair in reversed(pairs):
      new = [ ]
      for i in range(pair[0], pair[0] + pair[1]):
         source = notes[i % len_notes]
         newest = Note(source.pitch.number, source.duration.written)
         if source.history.get('tag', None):
            newest.history['tag'] = source.history['tag']
         if isinstance(history, str):
            newest.history['tag'] += history
         new.append(newest)
      reps = pair[-1]
      instruction = (pair[0] + pair[1], new, reps)
      instructions.append(instruction)

   for index, new_slice, reps in reversed(sorted(instructions)):
      notes[index:index] = clone.unspan(new_slice, reps)
