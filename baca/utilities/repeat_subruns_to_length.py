# -*- coding: utf-8 -*-
from abjad import *


def repeat_subruns_to_length(notes, pairs, history=False):
    '''Repeat notes according to pairs.

    ::

        >>> import baca

    ::

        >>> l = [Note(n, (1, 4)) for n in [0, 2, 4, 5, 7, 9, 11]]
        >>> baca.utilities.repeat_subruns_to_length(l, [(0, 4, 1), (2, 4, 1)])

    ::

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
            source = notes[i%len_notes]
            pitch_number = source.written_pitch.pitch_number
            new_note = Note(pitch_number, source.written_duration)
            if history:
                attach(history, new_note)
            new_notes.append(new_note)
        reps = pair[-1]
        instruction = (pair[0] + pair[1], new_notes, reps)
        instructions.append(instruction)
    for index, new_notes, reps in reversed(sorted(instructions)):
        new_notes = selectiontools.ContiguousSelection(new_notes)
        new_notes = mutate(new_notes).copy(n=reps)
        notes[index:index] = new_notes