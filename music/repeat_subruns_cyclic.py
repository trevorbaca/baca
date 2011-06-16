from abjad.tools.notetools.Note import Note
from abjad.tools import componenttools


## TODO: Rename to repeat_subruns_to_count() to match Abjad sequencetools. ##

def repeat_subruns_cyclic(notes, pairs, history = False):
    '''Repeat components according to pairs.

    >>> l = [Note(n, (1, 4)) for n in [0, 2, 4, 5, 7, 9, 11]]
    >>> music.repeat_subruns_cyclic(l, [(0, 4, 1), (2, 4, 1)])
    >>> l
    [c'4, d'4, e'4, f'4, c'4, d'4, e'4, f'4,
    g'4, a'4, e'4, f'4, g'4, a'4, b'4]'''

    assert all([isinstance(x, Note) for x in notes])
    assert isinstance(pairs, list)
    assert all([len(x) == 3 for x in pairs])

    instructions = []
    len_notes = len(notes)
    for pair in reversed(pairs):
        new_notes = []
        for i in range(pair[0], pair[0] + pair[1]):
            source = notes[i % len_notes]
            #new_note = Note(source.written_pitch.number, source.written_duration)
            new_note = Note(abs(source.written_pitch), source.written_duration)
            #if hasattr(source.history, 'tag'):
            #   new_note.history['tag'] = source.history['tag']
            #if isinstance(history, str):
            #   new_note.history['tag'] += history
            new_notes.append(new_note)
        reps = pair[-1]
        instruction = (pair[0] + pair[1], new_notes, reps)
        instructions.append(instruction)

    for index, new_notes, reps in reversed(sorted(instructions)):
        notes[index:index] = componenttools.copy_components_and_remove_all_spanners(new_notes, reps)
