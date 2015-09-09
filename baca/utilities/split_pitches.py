# -*- coding: utf-8 -*-
from abjad import *


def split_pitches(pitches, split=-1):
    r'''Splits list of probably aggregates into treble and bass.
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
                components[register] = scoretools.Skip((1, 4))
            elif len(components[register]) == 1:
                components[register] = Note(components[register], (1, 4))
            else:
                components[register] = Chord(components[register], (1, 4))
    return components['treble'], components['bass']