# -*- coding: utf-8 -*-
import abjad


def split_pitches(pitches, split=-1):
    r'''Splits `pitches`.
    
    Set `pitches` to (probably) a list of aggregates.
    
    Set `split` to a pitch number.

    Returns dictionary of `'treble'` and `'bass'` pitches.
    '''
    for sublist in pitches:
        components = {'treble': [], 'bass': []}
        for n in sublist:
            if n >= split:
                components['treble'].append(n)
            else:
                components['bass'].append(n)
        for register in ('treble', 'bass'):
            if len(components[register]) == 0:
                components[register] = abjad.scoretools.Skip((1, 4))
            elif len(components[register]) == 1:
                components[register] = abjad.Note(components[register], (1, 4))
            else:
                components[register] = abjad.Chord(
                    components[register], (1, 4))
    return components['treble'], components['bass']
