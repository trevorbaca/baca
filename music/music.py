# -*- encoding: utf-8 -*-
r'''Music-generation functions used in Čáry, Sekka and Lidércfény.
'''
import math
import baca
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


def octavate(n, base=(-4, 30)):
    r'''Octavates a single note.
    '''
    if not isinstance(Note):
        return
    assert hasattr(n, 'core')
    assert isinstance(n.core, list)
    lower, upper = base
    p = spget(n)
    if upper < p <= upper + 12:
        Octavation(n, 1)
    elif p > upper + 12:
        Octavation(n, 2)
    elif lower > p >= lower - 12:
        Octavation(n, -1)
    elif p < lower - 12:
        Octavation(n, -2)


def octavateIterator(voice, start, stop, base):
    r'''Octavates leaves from start to stop according to base.
    '''
    leaves = voice.select_leaves()
    for l in leaves[start : stop + 1]:
        octavate(l, base)


def setPitch(l, spec=0):
    r'''Sets l.pitch based on l.core.
    '''
    if not isinstance(l, Note):
        return
    # setPitch(l, 'core'):
    if spec == 'core':
        #p = l.core[0]
        pp = l.core
        transposition = 0
    # setPitch(l, 12)
    elif isinstance(spec, int):
        #p = l.core[0] % 12
        pp = [p % 12 for p in l.core]
        transposition = spec
    elif isinstance(spec, list):
        # setPitch(l, ['by pitch', (-39, 0, 24), (1, 48, 36)])
        if spec[0] == 'by pitch':
            new = []
            for p in l.core:
                for start, stop, t in spec[1:]:
                    if p in range(start, stop + 1):
                        new.append(p % 12 + t)
            if len(new) == 1:
                #l.pitch = pitch.Pitch(new[0])
                l.pitch = new[0]
            else:
                #l.pitch = [pitch.Pitch(p) for p in new]
                l.caster.toChord()
                l.pitches = new
            return
        # setPitch(l, ['by pc', (0, 6, 36), (7, 11, 24)])
        elif spec[0] == 'by pc':
            #p = l.core[0] % 12
            pp = [p % 12 for p in l.core]
            for start, stop, t in spec[1:]:
                # TODO fix me
                if pp[0] in range(start, stop + 1):
                    transposition = t
                    break
        else:
            raise ValueError
    else:
        raise ValueError
    if len(pp) == 1:
        #l.pitch = pitch.Pitch(pp[0] + transposition)
        l.pitch = pp[0] + transposition
    else:
        #l.pitch = [pitch.Pitch(p + transposition) for p in pp]
        l.caster.toChord()
        l.pitches = [p + transposition for p in pp]


def setPitchIterator(voice, start, stop, spec=0):
    leaves = voice.select_leaves()
    for l in leaves[start : stop + 1]:
        setPitch(l, spec)


def clonePitches(voice, start, stop, offset):
    leaves = voice.select_leaves()
    for i, l in enumerate(leaves[start : stop + 1]):
        if isinstance(l, Note):
            l.pitch = leaves[start + i + offset].pitch.pair


def setPitchesByPitchCycle(voice, start, stop, pcyc):
    leaves = voice.select_leaves()
    for j, l in enumerate(leaves[start : stop + 1]):
        i = j + start
        p = pcyc[j % len(pcyc)]
        l.pitch = p


def splitHands(l):
    r'''Splits list of numbers l into upper and lower.
    First-round approximation for piano music.
    '''
    # within a 10th
    if max(l) - min(l) <= 14:
        upper = l[:]
        lower = []
    else:
        mid = (max(l) - min(l)) / 2 + min(l)
        upper = [n for n in l if n >= mid]
        lower = [n for n in l if n < mid]
    return upper, lower


### TODO - come back and make this work;
###        or, just completely reimplement
def setPitchesBySplitHands(leaves, start, stop, crossLeaves):
    r'''Examines RH leaves;
    splits core RH leaf pitches into one or two chords;
    places higher of (one or) two chords in RH;
    places lower of two chords in LH;
    uses splitHands as helper.
    '''
    for j, l in enumerate(leaves[start : stop + 1]):
        i = start + j
        if isinstance(l, Note):
            # upper will always be nonempty
            upper, lower = splitHands(l.core)
            if lower == []:
                if min(upper) > -4:
                    l.core = upper
                    #setPitch(l, 'core')
                    #l.setPitches(l.core)
                    if len(l.core) == 1:
                        l.pitch = l.core[0]
                    else:
                        raise Exception('Need to cast to chord here.')
                    octavate(l)
                else:
                    #l.formatAs('Rest')
                    l.caster.toRest()
                    # NOTE: pass crossLeaves as input parameter
                    cl = crossLeaves[i]
                    cl.core = upper
                    #cl.formatAs('Note')
                    cl.caster.toNote()
                    #setPitch(cl, 'core')
                    cl.setPitches(cl.core)
        else:
                l.core = upper
                #setPitch(l, 'core')
                #l.setPitches(l.core)
                if len(l.core) == 1:
                    l.pitch = l.core[0]
                else:
                    raise Exception('Cast to chord here.')
                octavate(l)
                # NOTE: pass crossLeaves as input parameter
                print i, lower
                cl = crossLeaves[i]
                cl.core = lower
                print cl, cl.core, 'hello'
                #cl.formatAs('Note')
                cl.caster.toNote()
                #setPitch(cl, 'core')
                #cl.setPitches(cl.core)
                if len(cl.core) == 1:
                    cl.pitch = cl.core[0]
                else:
                    raise Exception('cast to chord here.')


def setArticulations(voice, articulations, *args, **kwargs):
    r'''Iterates leaves and sets articulations.
    '''
    leaves = voice.select_leaves()
    if len(args) == 0:
        start = 0
        stop = len(leaves)
    elif len(args) == 1:
        start = stop = args
    elif len(args) == 2:
        start, stop = args
    else:
        raise ValueError
    leafSlice = leaves[start : stop + 1]
    if kwargs.has_key('exclude'):
        exclude = kwargs['exclude']
    else:
        exclude = True
    for l in leafSlice:
        if instance(l, (Note, Chord)) or not exclude:
            if isinstance(articulations, str):
                l.articulations = [articulations]
            elif isinstance(articulations, list):
                l.articulations = articulations
            else:
                raise ValueError


def setArticulationsByPitch(voice, start, stop, articulations, min):
    r'''Sets articulations on notes & chord where safe pitch number 
    is at least min.
    '''
    leaves = voice.select_leaves()
    for l in leaves[start : stop + 1]:
        if isinstance(l, (Note, Chord)) and spget(l) >= min:
            l.articulations = articulations


def setArticulationsByDuration(voice, start, stop, long, min, short):
    r'''Sets long articulations on leaves where effective duration is
    at least min, else set short articulations.
    '''
    leaves = voice.select_leaves()
    min = Fraction(*min)
    for l in leaves[start : stop + 1]:
        if isinstance(l, (Note, Chord)):
            if inspect_(l).get_duration() >= min:
                l.articulations = long
            else:
                l.articulations = short


def clearAllArticulations(leaves, start=0, stop=None):
    r'''Clears articulations from leaves.
    '''
    if isinstance(stop, int):
        stop += 1
    for l in instances(leaves[start : stop], 'Leaf'):
        l.articulations = []


def appendArticulations(voice, articulations, *args, **kwargs):
    r'''Iterate leaves and append articulations.
    '''
    leaves = voice.select_leaves()
    if len(args) == 0:
        start = 0
        stop = len(leaves)
    elif len(args) == 1:
        start = stop = args
    elif len(args) == 2:
        start, stop = args
    else:
        raise ValueError
    leafSlice = leaves[start : stop + 1]
    if kwargs.has_key('exclude'):
        exclude = kwargs['exclude']
    else:
        exclude = True
    for l in leaves:
        if isinstance(l, (Note, Chord)) or not exclude:
            if isinstance(articulations, str):
                l.articulations.append(articulations)
            elif isinstance(articulations, list):
                for articulation in articulations:
                    l.articulations.extend(articulation)
            else:
                raise ValueError


def clear_dynamics(expr):
    r'''Clears dynamics and hairpins from leaves in expr.
    '''
    for l in instances(expr, 'Leaf'):
        l.dynamics = None
        l.dynamics.unspan()


def applyArtificialHarmonic(voice, *args):
    leaves = voice.select_leaves()
    if len(args) == 2:
        start, diatonicInterval = args
        stop = start
    elif len(args) == 3:
        start, stop, diatonicInterval = args
    else:
        raise ValueError
    for l in leaves[start : stop + 1]:
        if isinstance(l, Note):
            l.add_artificial_harmonic(diatonicInterval)


def hpartition_notes_only(leaves, cut=(0,), gap=(0,)):
    r'''Note runs only.
    '''
    cut = Fraction(*cut)
    gap = Fraction(*gap)
    result = [[]]
    for l in leaves:
        lastChunk = result[-1]
        if len(lastChunk) == 0:
            lastChunk.append(l)
        else:
            lastLeaf = lastChunk[-1]
            if lastLeaf.history['class'] == l.history['class']:
                lastChunk.append(l)
            else:
                result.append([l])
    result = [
        x for x in result
        if x[0].history['class'] == 'Note']
    return result


def hpartition_rest_terminated(leaves, cut=(0,), gap=(0,)):
    r'''Rest-terminated note runs.
    '''
    cut = Fraction(*cut)
    gap = Fraction(*gap)
    result = [[]]
    for l in leaves:
        lastChunk = result[-1]
        if l.history['class'] == 'Note':
            if len(lastChunk) == 0:
                lastChunk.append(l)
            else:
                lastLeaf = lastChunk[-1]
                if lastLeaf.history['class'] == 'Note':
                    lastChunk.append(l)
                else:
                    result.append([l])
        elif l.history['class'] == 'Rest':
            if len(lastChunk) > 0:
                lastLeaf = lastChunk[-1]
                if lastLeaf.history['class'] == 'Note':
                    lastChunk.append(l)
    return result