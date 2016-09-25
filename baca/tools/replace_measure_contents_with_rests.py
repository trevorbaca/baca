# -*- coding: utf-8 -*-
import abjad


#def blank(l, positions):
def replace_measure_contents_with_rests(l, positions):
    r'''Replaces measures `l` with rests at `positions`.
    
    Numbers measures starting from 1.
    '''
    result = []
    for i, m in enumerate(l):
        if (i + 1) in positions:
            duration = inspect_(m).get_duration()
            rests = abjad.scoretools.make_rests(duration)
            new_measure = abjad.Measure(m.time_signature, rests)
            l[i] = new_measure
