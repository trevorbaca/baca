# -*- encoding: utf-8 -*-
r'''Music-generation functions used in Čáry, Sekka and Lidércfény.
'''
import math
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


def make_breaks_voice(signatures, durations, pages, verticals, staves=None):
    if staves != None:
        staves = ' '.join([str(x) for x in staves])
    result = []
    total = 0
    for p, page in enumerate(pages):
        for l, line in enumerate(page):
            for measure in range(line):
                d = durations[total]
                s = scoretools.Skip((1))
                #inspect_(s).get_duration().multiplier = d
                attach(d, s)
                tabs = ''.join(
                    #['\t'] * int(math.ceil((10 - len(s.body)) / 3.0))
                    ['\t'] * int(math.ceil((10 - len(str(s))) / 3.0))
                    )
                result.append(s)
                result[-1].directives.before.append(signatures[total] + '\t')
                result[-1].directives.right = None
                result[-1].directives.right.append('%s\\noBreak\t\t' % tabs)
                result[-1].comments.before.append('measure %s' % (total + 1))
                if l == 0 and measure == 0:
                    string = '\n%% page %s' % (p + 1)
                    result[-1].directives.before.append(string)
                total += 1
            result[-1].right = []
            tabs = ''.join(['\t'] * int(math.ceil((10 - len(s.body)) / 3.0)))
            result[-1].directives.right = None
            result[-1].directives.right.append('%s\\break\t\t' % tabs)
            if len(result[-(measure + 1)].directives.before) == 0:
                result[-(measure + 1)].directives.before.append('')
            result[-(measure + 1)].directives.before.append(
                '\overrideProperty #"Score.NonMusicalPaperColumn"')
            if staves == None:
                string = "#'line-break-system-details #'((Y-offset . {}))"
                string = string.format(verticals[p][l])
                result[-(measure + 1)].directives.before.append(string)
            else:
                string = "#'line-break-system-details #'((Y-offset . {})"
                string += " (alignment-offsets . ({})))"
                string = string.format(verticals[p][l], staves)
                result[-(measure + 1)].directives.before.append(string)
        result[-1].directives.right = None
        tabs = ''.join(['\t'] * int(math.ceil((10 - len(s.body)) / 3.0)))
        result[-1].directives.right = None
        string = '{}\\pageBreak\t'.format(tabs)
        result[-1].directives.right.append(string)
    result = Voice(result)
    result.name = 'breaks'
    return result