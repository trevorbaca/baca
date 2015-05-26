# -*- encoding: utf-8 -*-
r'''Music-generation functions used in Čáry, Sekka and Lidércfény.
'''
import copy
import math
import re
from abjad import *
import baca


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


class Subdivide(object):
    def __init__(self, positions):
        self.positions = positions
        self.position = -1
    def visit(self, node):
        if isinstance(node, scoretools.Leaf):
            self.position += 1
            n = self.positions[self.position]
            if n > 0:
                denominator = int(2 ** (n + 2))
                quotient = \
                    inspect_(node).get_duration() / Fraction(1, denominator)
                if quotient.d == 1 and quotient.n > 1:
                    new = expression.Expression(
                        [Note(0, 1, denominator) for x in range(quotient.n)])
                    if len(new.music) > 1:
                        #new.music[0].right.append('[')
                        #new.music[-1].right.append(']')
                        new.beam('all left')
                    return new
                else:
                    return node
            else:
                return node
        else:
            return node


def subdivide(m, positions):
    r'''Subdivides leaves in m by according to positions.
    '''
    baca.utilities.change(m, Subdivide(positions))


class FiveRemover(object):
    def visit(self, node):
        if (isinstance(node, Note) and
            inspect_(node).get_duration().n == 5):
            denominator = inspect_(node).get_duration().d
            return expression.Expression(
                [Note(0, 4, denominator), Note(0, 1, denominator)])
        else:
            return node


def unfive(music):
    baca.utilities.change(music, FiveRemover())


def stellate(k, s, t, d, b, span='from duration', rests=True):
    r'''Makes running tuplets.

    Numerators k + s;
    denominators k;
    mask t;
    duration 1/d;
    beams b.

    s = [[0]] indicates zero-prolation;
    t = [[1]] leaves output unripped.

    TODO: prevent from-duration span from giving incorrect nibs.
    '''
    if t == [[0]]:
        print 't == [[0]] will cause an infinite loop.'
        raise ValueError
    debug = False
    prolation = baca.utilities.helianthate(s, 1, 1)
    prolation = sequencetools.flatten_sequence(prolation)
    numerators = sequencetools.increase_elements(k, prolation)
    mask = baca.utilities.helianthate(t, 1, 1)
    mask = sequencetools.flatten_sequence(mask)
    mask = sequencetools.repeat_to_weight(mask, mathtools.weight(numerators))
    mask = baca.utilities.replace_nested_elements_with_unary_subruns(mask)
    signatures = sequencetools.split_sequence_once_by_weights_with_overhang(
        mask, numerators)
    for i, signature in enumerate(signatures):
        if signature == [1]:
            signatures[i] = [-1]
    signatures = baca.utilities.partition_nested_into_canonic_parts(signatures)
    if not rests:
        part_counts = [len(x) for x in signatures]
        signatures = sequencetools.flatten(signatures)
        signatures = [abs(x) for x in signatures]
        signatures = \
            sequencetools.partition_by_lengths(signatures, part_counts)
    denominators = copy.copy(k)
    pairs = zip(signatures, denominators)
    tuplets = [Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        pair[0], (pair[1], d)) for pair in pairs]
    if span == 'from duration':
        span = int(math.log(d, 2)) - 3
    if isinstance(span, int) and span < 1:
        span = None
    dummy_container = Container(tuplets)
    tuplets = sequencetools.partition_by_lengths(
        tuplets, b, cyclic=True, overhang=True)
    for i, sublist in enumerate(tuplets):
        if debug:
            sublist[0][0].formatter.right.append(
                r'_ \markup \fontsize #6 { %s }' % i)
        durations = [inspect_(tuplet).get_duration() for tuplet in sublist]
        spanner = spannertools.DuratedComplexBeam(
            durations=durations, span=span)
        attach(spanner, sublist)
        i += 1
    dummy_container[:] = []
    tuplets = sequencetools.flatten(tuplets)
    return tuplets


def coruscate(n, s, t, z, d, rests=True):
    r'''Coruscates talea n;
    returns list of fixed-duration tuplets.

    Input talea n (2d, passed to helianthate);
    cut s (2d, passed to helianthate);
    fit t (list);
    dilation z (2d, passed to helianthate);
    duration 1/d.

    n = [[1]] gives uniform talea;
    s = [[0]] gives no cut;
    z = [[0]] gives no dilation.

    Length of result equals length of fit.
    Coruscated lines contain no span beams.
    '''
    debug = False
    # zero-valued taleas not allowed
    talea = baca.utilities.helianthate(n, 1, 1)
    talea = sequencetools.flatten_sequence(talea)
    assert all(talea)
    cut = baca.utilities.helianthate(s, 1, 1)
    cut = sequencetools.flatten_sequence(cut)
    dilation = baca.utilities.helianthate(z, 1, 1)
    dilation = sequencetools.flatten_sequence(dilation)
    fit = sequencetools.increase_elements(t, dilation)
    j = 0
    signatures = []
    for i, element in enumerate(fit):
        new = []
        while mathtools.weight(new) < element:
            if cut[j % len(cut)] == 0:
                new.append(talea[j % len(talea)])
            elif cut[j % len(cut)] == 1:
                new.append(-talea[j % len(talea)])
            else:
                raise ValueError
            j += 1
        signatures.append(new)
    def helper(x):
        return list(
        sequencetools.sum_consecutive_elements_by_sign(x, sign=[-1]))
    signatures = [helper(signature) for signature in signatures]
    signatures = baca.utilities.partition_nested_into_canonic_parts(signatures)
    if not rests:
        part_counts = [len(x) for x in signatures]
        signatures = sequencetools.flatten(signatures)
        signatures = [abs(x) for x in signatures]
        signatures = \
            sequencetools.partition_by_lengths(signatures, part_counts)
    if debug: print signatures
    pairs = zip(signatures, t)
    result = [Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        pair[0], (pair[1], d)) for pair in pairs]
    for i, element in enumerate(result):
        if debug:
            element.music[0].right.append(r'_ \markup \fontsize #6 { %s }' % i)
        spanner = spannertools.DuratedComplexBeam(
            durations=[inspect_(element).get_duration()],
            )
        attach(spanner, element.select_leaves()) 
    return result


def make_measures(expr, meters):
    r'''For each voice in expr, presses contents into measures
    according to meters.
    '''
    durations = [Duration(*meter) for meter in meters]
    for voice in iterate(expr).by_class(Voice):
        assert inspect_(voice).get_duration() == sum(durations, Duration(0))
        meter_index = 0
        measure = Measure(meters[meter_index], [])
        for component in voice[:]:
            measure.append(component)
            if inspect_(measure).get_duration() >= durations[meter_index]:
                voice[meter_index:2*meter_index+len(measure)-1] = [measure]
                meter_index += 1
                if meter_index == len(durations):
                    break
                else:
                    measure = Measure(meters[meter_index], [])


def recombineVoices(target, s, insert, t, loci):
    r'''Iterate simultaneously through the voices in target and insert;
    partition each target voice according to lengths in s;
    partition each insert voice according to lengths in t;
    overwrite the parts of each (partitioned) target voice
    with the parts of each (partitioned) insert voice
    according to the positions in loci.
    '''
    targetVoices = instances(target, 'Voice')
    insertVoices = instances(insert, 'Voice')
    if len(targetVoices) != len(insertVoices):
        print 'ERROR: target voices and insert voices do not match.'
        raise ValueError
#   for i in range(n):
#      tgtm = targetVoices[i].music
#      insm = insertVoices[i].music
#      partitionBeams(tgtm, s)
#      #partition(tgtm, s)
#      partition(tgtm, s, cyclic = True, overhang = True)
#      print tgtm
#      partitionBeams(insm, t)
#      #partition(insm, t)
#      partition(insm, t, cyclic = True, overhang = True)
#      print insm
#      replace(tgtm, loci, insm)
#      sequencetools.flatten(tgtm)
    def P(n, s):
        return partition(
            range(n), s, cyclic=True, overhang=True, action='new')
    def makeIndexPairs(n, s):
        return sequencetools.pairwise(
            sequencetools.cumulative_sums_zero(
            [len(part) for part in P(n, s)]))
    targetIndexPairs = makeIndexPairs(len(targetVoices[0]), s)
    insertIndexPairs = makeIndexPairs(len(insertVoices[0]), t)
    if len(insertIndexPairs) < len(loci):
        print 'ERROR: insert partitions into only %s parts;' \
            % len(insertIndexPairs)
        print '         not enough to fill the %s loci specified.' \
            % len(loci)
        print ''
    for targetVoice, insertVoice in zip(targetVoices, insertVoices):
        for j, locus in enumerate(reversed(sorted(loci))):
            first, last = insertIndexPairs[len(loci) - 1 - j]
            insert = copyMusicList(insertVoice, first, last - 1)
            first, last = targetIndexPairs[locus]
            targetVoice[first : last] = insert


def rippleVoices(m, s):
    r'''Repeat voice elements in m according to s.
    '''
    spec = dict(s)
    voices = instances(m, 'Voice')
    for v in voices:
        for i in reversed(range(len(v))):
            if spec.has_key(i):
                length, reps = spec[i]
                source = v.copy(i, i + length - 1)
                leaves = instances(source, 'Leaf')
                left, right = leaves[0], leaves[-1]
                #left.spanners.fractureLeft()
                #right.spanners.fractureRight()
                left.spanners.fracture(direction = 'left')
                right.spanners.fracture(direction = 'right')
                new = []
                for j in range(reps):
                    new.extend(copyMusicList(source))
                v[i : i + 1] = new


def copyMusicList(ll, i=None, j=None):
    r'''Truly smart copy from i up to and including j;
    fracture external and preserve internal spanners;
    return new list.
    '''
    if i is None and j is None:
        source = ll[ : ]
    else:
        source = ll[i : j + 1]
    if source == []:
        print 'WARNING: copyMusicList(ll, %s, %s) gives empty source;' % (i, j)
        print '           len(ll) is %s.' % len(ll)
        print ''
    result = Container(source)
    result = result.copy()
    result = result[ : ]
    return result


def setLeafStartTimes(expr, offset=Fraction(0)):
    cur = Fraction(*offset.pair)
    for l in instances(expr, 'Leaf'):
        l.start = cur
        cur += inspect_(l).get_duration()


def rankLeavesTimewise(exprList, name='Leaf'):
    r'''Sets 'timewise' attribute on each of the leaves in the expr in 
    exprList.

    Can be list of Voices, list of Staves, list of anything with leaves;
    order of expr in exprList matters;
    absolute start times must be already set on all leaves.
    '''
    result = []
    leafLists = [instances(expr, name) for expr in exprList]
    #print 'starting ...'
    #cur = 0
    while len(leafLists) > 0:
        candidateLeaves = [leafList[0] for leafList in leafLists]
        minStart = min([l.start for l in candidateLeaves])
        for leafList in leafLists:
            if leafList[0].start == minStart:
                #print 'found %s' % cur
                #cur += 1
                result.append(leafList.pop(0))
                if len(leafList) == 0:
                    leafLists.remove(leafList)
                break
    for i, l in enumerate(result):
        l.timewise = i


def spget(arg):
    r'''Gets lowest pitch in either note or chord.

    Otherwise returns none.
    '''
    if isinstance(arg, Note):
        return arg.pitch.number
    elif isinstance(arg, Chord):
        return arg.pitches[0].number
    else:
        return None


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