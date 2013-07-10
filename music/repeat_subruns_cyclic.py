from abjad.tools.notetools.Note import Note
from abjad.tools import componenttools


# TODO: Rename to repeat_subruns_to_count() to match Abjad sequencetools.
def repeat_subruns_cyclic(notes, pairs, history=False):
    '''Repeat components according to pairs.

    >>> from baca import music

    >>> l = [Note(n, (1, 4)) for n in [0, 2, 4, 5, 7, 9, 11]]
    >>> music.repeat_subruns_cyclic(l, [(0, 4, 1), (2, 4, 1)])

    >>> l
    [Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4"), Note("c'4"), 
     Note("d'4"), Note("e'4"), Note("f'4"), Note("g'4"), Note("a'4"), 
     Note("e'4"), Note("f'4"), Note("g'4"), Note("a'4"), Note("b'4")]

    Return list of components.
    '''

    assert all([isinstance(x, Note) for x in notes])
    assert isinstance(pairs, list)
    assert all([len(x) == 3 for x in pairs])

    instructions = []
    len_notes = len(notes)
    for pair in reversed(pairs):
        new_notes = []
        for i in range(pair[0], pair[0] + pair[1]):
            source = notes[i % len_notes]
            new_note = Note(abs(source.written_pitch), source.written_duration)
            new_notes.append(new_note)
        reps = pair[-1]
        instruction = (pair[0] + pair[1], new_notes, reps)
        instructions.append(instruction)

    for index, new_notes, reps in reversed(sorted(instructions)):
        notes[index:index] = \
            componenttools.copy_components_and_detach_spanners(new_notes, reps)
