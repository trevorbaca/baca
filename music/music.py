'''Music-generation functions used in Cary, Sekka and Lidercfeny.
'''

import copy
import fractions
import math
import re
from abjad import *
from baca import util


def splitPitches(pitches, split=-1):
    '''Split list of probably aggregates into treble and bass.
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
                #treble.append(skiptools.Skip((1, 4)))
                components[register] = skiptools.Skip((1, 4))
            elif len(components[register]) == 1:
                #treble.append(notetools.Note(components[register], (1, 4)))
                components[register] = notetools.Note(components[register], (1, 4))
            else:
                components[register] = chordtools.Chord(components[register], (1, 4))

    return components['treble'], components['bass']


def makeFixedLayoutVoice(d, systems, alignments, offsets):

    alignment = ' '.join([str(n) for n in alignments])
    alignment = "(alignment-offsets . (%s))" % alignment

    v = voicetools.Voice([], name = 'layout voice')
    for system in range(systems):
        new = skiptools.Skip(*d)
        offset = offsets[system % len(offsets)]
        offset = "(Y-offset . %s)" % offset
        text = r'\overrideProperty #"Score.NonMusicalPaperColumn"'
        new.before.append(text)
        new.before.append("#'line-break-system-details")
        text = "#'(%s %s)" % (offset, alignment)
        new.before.append(text)
        if system % len(offsets) == len(offsets) - 1:
            new.right.append(r'\pageBreak')
        else:
            new.right.append(r'\break')
        v.music.append(new)

    return v


def traverse(expr, v):
    v.visit(expr)
    if isinstance(expr, (list, tuple)):
        for m in expr:
            traverse(m, v)
    if hasattr(expr, '_music'):
        for m in expr._music:
            traverse(m, v)
    if hasattr(v, 'unvisit'):
        v.unvisit(expr)


def change(expr, visitor):
    if isinstance(expr, list):
        for x in expr[:]:
            expr[expr.index(x)] = change(x, visitor)
        return expr
    elif hasattr(expr, 'music'):
        for m in expr.music[:]:
            expr.music[expr.music.index(m)] = change(m, visitor)
        return expr
    else:
        return visitor.visit(expr)


def changeslice(expr, visitor):
    if isinstance(expr, list):
        for x in expr[:]:
            expr[expr.index(x) : (expr.index(x) + 1)] = changeslice(x, visitor)
        return expr
    elif hasattr(expr, 'music'):
        for m in expr.music[:]:
            #print 'into   ', m
            expr.music[expr.music.index(m) : (expr.music.index(m) + 1)] = \
                changeslice(m, visitor)
            #print 'out of ', m
        return [expr]
    else:
        return visitor.visit(expr)


def effectiveDurations(m):
    '''List the effective durations of the leaves in m.

        >>> from baca.music import *

        >>> tuplet = Tuplet((2, 3), "c'16 c'16 c'16")

        >>> effectiveDurations(tuplet.select_leaves())
        [Duration(1, 24), Duration(1, 24), Duration(1, 24)]

    Return list of durations.
    '''
    return [
        l.get_duration() 
        for l in list(iterationtools.iterate_leaves_in_expr(m))
        ]


def effectiveDuration(m):
    '''Sum the effective durations of the leaves in m.

            >>> tuplet = Tuplet((2, 3), "c'16 c'16 c'16")

            >>> effectiveDuration(tuplet)
            Duration(1, 8)

            >>> effectiveDuration(tuplet.select_leaves())
            Duration(1, 8)

    Return duration.
    '''

    if m == []:
        return fractions.Fraction(0)
    else:
        return sum(effectiveDurations(m), fractions.Fraction(0))


def fill(l, positions):
    '''Fill in 1-indexed measures with middle C.
    '''

    result = []

    for i, m in enumerate(l):
        if (i + 1) in positions:
            n, d = m.get_duration().pair
            parts = mathtools.partition_integer_into_canonic_parts(n)
            l[i] = measuretools.Measure(
                m.meter.pair,
                [notetools.Note(0, (x, d)) for x in parts])


def blank(l, positions):
    '''Blank out 1-indexed measures.
    '''

    result = []

    for i, m in enumerate(l):
        if (i + 1) in positions:
            rests = resttools.make_rests(m.contents_duration)
            new_measure = measuretools.Measure(m.meter.effective, rests)
            l[i] = new_measure


def nest(measures, outer, inner):
    '''Structure time.
    '''

    #inner = partition(inner, [len(x) for x in outer], action = 'new')
    inner = sequencetools.partition_by_lengths(inner, [len(x) for x in outer])

    result = []

    for i in range(len(measures)):
        m = measures[i]
        o = outer[i]
        n = inner[i]
        #print i, m, o, n
        measure_numerator, measure_denominator = m
        tuplet = divide.pair(o, (measure_numerator, measure_denominator))
        #print tuplet
        #dd = writtenDurations([measuretools.Measure([divide.pair(o, (m[0], m[1]))])])
        tie_chains = list(iterationtools.iterate_tie_chains_in_expr(
            tuplet.select_leaves()))
        dd = [x.written_duration for x in tie_chains]
        body = []
        for j, d in enumerate(dd):
            if 0 < o[j]:
                body.append(divide.pair(n[j], (d._n, d._d)))
            else:
                body.append(restools.Rest(d))

        #t = tuplet.SmartTuplet(m[0], m[1], body)
        t = FixedDurationTuplet(m, body)
        result.append(measuretools.Measure(m, [t]))

    return result


def trill(l, p=False, indices='all', d=fractions.Fraction(0)):
    '''Cyclically trill notes at indices with scaled duration >= d.

    When p is set, cyclically applies pitches in p.

    trill(l)
    trill(l, indices = [0, 2])
    trill(l, d = fractions.Fraction(1, 4)
    trill(l, p = [pitch.Pitch(2)])
    trill(l, indices = [0, 2], p = [pitch.Pitch(2)])

    NOTE: temporarily sets note.trill to True only.
    '''

    if indices == 'all':
        indices = range(len(instances(l, 'Leaf')))

    for i, element in enumerate(instances(l, 'Leaf')):
        #if (i - 1) in indices:
        #  element.after.append(r'\stopTrillSpan')
        if hasattr(element, 'scaledDuration'):
            sd = element.scaledDuration
        else:
            sd = element.get_duration()
        if isinstance(element, notetools.Note) and i in indices and sd >= d:
            #if p:
            #  element.before.append(r'\pitchedTrill')
            #  element.after.append(r'\startTrillSpan ' + p[i % len(p)].lily)
            #else:
            #  element.after.append(r'\startTrillSpan')
            element.trill = True


def grace(l,
    k='Leaf', indices='all',
    m='Note', dm=(0, 1), check=True,
    s=[[notetools.Note(0, (1, 16))]], cyclic=True):

    if indices == 'all':
        indices = range(len(instances(l, k)))

    dm = fractions.Fraction(*dm)

    candidate = 0

    for i, element in enumerate(instances(l, k)):

        if hasattr(element, 'scaledDuration'):
            sd = element.scaledDuration
        else:
            sd = element.get_duration()

        if check and hasattr(element, 'grace'):
            ck = False
        else:
            ck = True

        if i in indices and isinstance(element, m) and sd >= dm and ck:
            new = 0
            if cyclic:
                new = s[candidate % len(s)]
            elif candidate <= len(s) - 1:
                new = s[candidate]
            if new != 0:
                element.grace = clean(new)

            candidate += 1


def color(l, p):

    i = 0
    for n in instances(l, 'Note'):
        try:
            #n.pitch = clean(p[i].pitch)
            n.pitch.setPitch(p[i].pitch.number)
            i += 1
            #if r'\pitchedTrill' in n.before:
            #  for j, s in enumerate(n.after):
            #     if s.startswith(r'\startTrillSpan'):
            #        n.after[j] = r'\startTrillSpan ' + p[i].pitch.lily
            #  i += 1
            if hasattr(n, 'trill'):
                i += 1
                #n.after.append(r'\trill')
            if hasattr(n, 'grace'):
                for g in n.grace:
                    g.pitch = p[i].pitch
                    i += 1
        except:
            pass


def untrill(l):
    for element in instances(l, 'Leaf'):
        if hasattr(element, 'trill'):
            delattr(element, 'trill')


def ungrace(l, keep='first', length=1):

    for element in instances(l, 'Leaf'):
        if hasattr(element, 'grace'):
            if keep == 'first':
                element.grace = element.grace[:length]
            elif keep == 'last':
                element.grace = element.grace[-length:]


def breaks(signatures, durations, pages, verticals, staves=None):

    if staves != None:
        staves = ' '.join([str(x) for x in staves])

    result = []

    total = 0
    for p, page in enumerate(pages):
        for l, line in enumerate(page):
            for measure in range(line):
                d = durations[total]
                s = skiptools.Skip((1))
                s.get_duration().multiplier = d
                tabs = ''.join(['\t'] * int(math.ceil((10 - len(s.body)) / 3.0)))
                result.append(s)
                result[-1].directives.before.append(signatures[total] + '\t')
                result[-1].directives.right = None
                result[-1].directives.right.append('%s\\noBreak\t\t' % tabs)
                result[-1].comments.before.append('measure %s' % (total + 1))
                if l == 0 and measure == 0:
                    result[-1].directives.before.append('\n%% page %s' % (p + 1))
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
                result[-(measure + 1)].directives.before.append(
                    "#'line-break-system-details #'((Y-offset . %s))" %
                    verticals[p][l])
            else:
                result[-(measure + 1)].directives.before.append(
                    "#'line-break-system-details #'((Y-offset . %s) (alignment-offsets . (%s)))" % (verticals[p][l], staves))
        result[-1].directives.right = None
        tabs = ''.join(['\t'] * int(math.ceil((10 - len(s.body)) / 3.0)))
        result[-1].directives.right = None
        result[-1].directives.right.append('%s\\pageBreak\t' % tabs)

    result = voicetools.Voice(result)
    result.name = 'breaks'
    return result


class Subdivide(object):
    def __init__(self, positions):
        self.positions = positions
        self.position = -1
    def visit(self, node):
        if isinstance(node, leaftools.Leaf):
            self.position += 1
            n = self.positions[self.position]
            if n > 0:
                denominator = int(2 ** (n + 2))
                quotient = \
                    node.get_duration() / fractions.Fraction(1, denominator)
                if quotient.d == 1 and quotient.n > 1:
                    new = expression.Expression(
                        [notetools.Note(0, 1, denominator) for x in range(quotient.n)])
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
    '''Subdivide leaves in m by according to positions.
    '''

    change(m, Subdivide(positions))


class FiveRemover(object):
    def visit(self, node):
        if isinstance(node, notetools.Note) and \
            node.get_duration().n == 5:
            denominator = node.get_duration().d
            return expression.Expression(
                [notetools.Note(0, 4, denominator), notetools.Note(0, 1, denominator)])
        else:
            return node


def unfive(music):
    change(music, FiveRemover())


def stellate(k, s, t, d, b, span='from duration', rests=True):
    '''Make running tuplets.

    Numerators k + s;
    denominators k;
    mask t;
    duration 1/d;
    beams b.

    s = [[0]] indicates zero-prolation;
    t = [[1]] leaves output unripped.

    TODO: prevent from-duration span from giving incorrect nibs.
    '''

    #from spannertools import beamRunsByDuration

    if t == [[0]]:
        print 't == [[0]] will cause an infinite loop.'
        raise ValueError

    debug = False

    prolation = util.helianthate(s, 1, 1)
    prolation = sequencetools.flatten_sequence(prolation)
    numerators = sequencetools.increase_sequence_elements_cyclically_by_addenda(k, prolation)
    mask = util.helianthate(t, 1, 1)
    mask = sequencetools.flatten_sequence(mask)
    mask = sequencetools.repeat_to_weight(mask, mathtools.weight(numerators))
    mask = util.replace_nested_elements_with_unary_subruns(mask)
    #signatures = partition(
    #    mask, numerators, mode = 'weight', overhang = 'true', action = 'new')
    signatures = sequencetools.split_sequence_once_by_weights_with_overhang(mask, numerators)
    for i, signature in enumerate(signatures):
        if signature == [1]:
            signatures[i] = [-1]
    signatures = util.partition_nested_into_canonic_parts(signatures)

    if not rests:
        part_counts = [len(x) for x in signatures]
        signatures = sequencetools.flatten(signatures)
        signatures = [abs(x) for x in signatures]
        signatures = sequencetools.partition_by_lengths(signatures, part_counts)

    denominators = copy.copy(k)
    pairs = zip(signatures, denominators)
    tuplets = [Tuplet.from_ratio_and_nonreduced_fraction(
        pair[0], (pair[1], d)) for pair in pairs]

    if span == 'from duration':
        span = int(math.log(d, 2)) - 3

    if isinstance(span, int) and span < 1:
        span = None

    dummy_container = Container(tuplets)
    #partition(tuplets, b, cyclic = True, overhang = True)
    tuplets = sequencetools.partition_by_lengths(tuplets, b, cyclic = True, overhang = True)
    for i, sublist in enumerate(tuplets):
        #if t == [[4, -5, 8], [4, -8], [-4, 6, -6, 8]] and i == 7:
        #   import pdb
        #   pdb.set_trace()
        if debug:
            #print i, sublist
            sublist[0][0].formatter.right.append(
                r'_ \markup \fontsize #6 { %s }' % i)
        durations = [tuplet.get_duration() for tuplet in sublist]
        #beamRunsByDuration(tmp.select_leaves(), durations, span = span)
        #ComplexBeam(sublist, durations, span = span)
        #BeamComplex(sublist, durations, span = span)
        #BeamComplexDurated(sublist, durations, span = span)
        spannertools.DuratedComplexBeamSpanner(sublist, durations, span = span)
        i += 1
    dummy_container[:] = []
    tuplets = sequencetools.flatten(tuplets)

    return tuplets


def coruscate(n, s, t, z, d, rests=True):
    '''Coruscate talea n;
    return list of fixed-duration tuplets.

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
    #from spannertools import beamRunsByDuration

    # zero-valued taleas not allowed
    talea = util.helianthate(n, 1, 1)
    talea = sequencetools.flatten_sequence(talea)
    assert all(talea)

    cut = util.helianthate(s, 1, 1)
    cut = sequencetools.flatten_sequence(cut)

    dilation = util.helianthate(z, 1, 1)
    dilation = sequencetools.flatten_sequence(dilation)
    fit = sequencetools.increase_sequence_elements_cyclically_by_addenda(t, dilation)

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
    def helper(x): return list(sequencetools.sum_consecutive_sequence_elements_by_sign(x, sign = [-1]))
    signatures = [helper(signature) for signature in signatures]
    signatures = util.partition_nested_into_canonic_parts(signatures)

    if not rests:
        part_counts = [len(x) for x in signatures]
        signatures = sequencetools.flatten(signatures)
        signatures = [abs(x) for x in signatures]
        signatures = sequencetools.partition_by_lengths(signatures, part_counts)

    if debug: print signatures

    pairs = zip(signatures, t)
    result = [Tuplet.from_ratio_and_nonreduced_fraction(
        pair[0], (pair[1], d)) for pair in pairs]

    for i, element in enumerate(result):
        if debug:
            element.music[0].right.append(r'_ \markup \fontsize #6 { %s }' % i)
        #beam(element)
        #beamRunsByDuration(element, [element.get_duration().pair])
        #ComplexBeam(element, [element.get_duration().pair])
        #BeamComplex(element, [element.get_duration().pair])
        spannertools.DuratedComplexBeamSpanner(
            element.select_leaves(), 
            [element.get_duration()],
            )

    return result


def makeMeasures(m, meters):
    '''For each voice in m,
    press contents into measures
    according to meters.
    '''

    durations = [fractions.Fraction(*meter) for meter in meters]
    for v in iterationtools.iterate_components_in_expr(
        m, component_class=voicetools.Voice,
        ):
        assert v.get_duration() == sum(durations, fractions.Fraction(0))
        d = 0
        #measure = measuretoools.Measure(meters[d], [])
        measure = measuretools.Measure(meters[d], [])
        for x in v[ : ]:
            measure.append(x)
            if measure.get_duration() >= durations[d]:
                v[d : 2 * d + len(measure) - 1] = [measure]
                d += 1
                if d == len(durations):
                    break
                else:
                    #measure = measuretools.Measure(meters[d], [])
                    measure = measuretools.Measure(meters[d], [])


def recombineVoices(target, s, insert, t, loci):
    '''Iterate simultaneously through the voices in target and insert;
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
            range(n), s, cyclic = True, overhang = True, action = 'new')

    def makeIndexPairs(n, s):
        return sequencetools.pairwise(
            sequencetools.cumulative_sums_zero([len(part) for part in P(n, s)]))

    targetIndexPairs = makeIndexPairs(len(targetVoices[0]), s)
    insertIndexPairs = makeIndexPairs(len(insertVoices[0]), t)

    #print targetIndexPairs
    #print insertIndexPairs

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
    '''Repeat voice elements in m
    according to s.
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
    '''Truly smart copy from i up to and including j;
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


def setLeafStartTimes(expr, offset=fractions.Fraction(0)):
    cur = fractions.Fraction(*offset.pair)
    for l in instances(expr, 'Leaf'):
        l.start = cur
        cur += l.get_duration()


def rankLeavesTimewise(exprList, name='Leaf'):
    '''Sets 'timewise' attribute on each of the leaves in the expr in exprList.

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
    '''Get lowest pitch in either note or chord.

    Otherwrise return none.
    '''

    if isinstance(arg, notetools.Note):
        return arg.pitch.number
    elif isinstance(arg, chordtools.Chord):
        return arg.pitches[0].number
    else:
        return None


def octavate(n, base=(-4, 30)):
    '''Octavate a single note.
    '''

    if not isinstance(notetools.Note):
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
    '''Octavate leaves from start to stop according to base.
    '''

    leaves = voice.select_leaves()
    for l in leaves[start : stop + 1]:
        octavate(l, base)


def setPitch(l, spec=0):
    '''Sets l.pitch based on l.core.
    '''

    if not isinstance(l, notetools.Note):
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
        if isinstance(l, notetools.Note):
            l.pitch = leaves[start + i + offset].pitch.pair


def setPitchesByPitchCycle(voice, start, stop, pcyc):
    leaves = voice.select_leaves()
    for j, l in enumerate(leaves[start : stop + 1]):
        i = j + start
        p = pcyc[j % len(pcyc)]
        l.pitch = p


def splitHands(l):
    '''
    Split list of numbers l into upper and lower.
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
    '''Examines RH leaves;
    splits core RH leaf pitches into one or two chords;
    places higher of (one or) two chords in RH;
    places lower of two chords in LH;
    uses splitHands as helper.
    '''

    for j, l in enumerate(leaves[start : stop + 1]):
        i = start + j
        if isinstance(l, notetools.Note):
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
    '''Iterate leaves and set articulations.
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
        if instance(l, (notetools.Note, chordtools.Chord)) or not exclude:
            if isinstance(articulations, str):
                l.articulations = [articulations]
            elif isinstance(articulations, list):
                l.articulations = articulations
            else:
                raise ValueError


def setArticulationsByPitch(voice, start, stop, articulations, min):
    '''Set articulations on notes & chord where safe pitch number is at least min.
    '''

    leaves = voice.select_leaves()
    for l in leaves[start : stop + 1]:
        if isinstance(l, (notetools.Note, chordtools.Chord)) and spget(l) >= min:
            l.articulations = articulations


def setArticulationsByDuration(voice, start, stop, long, min, short):
    '''Set long articulations on leaves where effective duration is
    at least min, else set short articulations.
    '''

    leaves = voice.select_leaves()
    min = fractions.Fraction(*min)
    for l in leaves[start : stop + 1]:
        if isinstance(l, (notetools.Note, chordtools.Chord)):
            if l.get_duration() >= min:
                l.articulations = long
            else:
                l.articulations = short


def clearAllArticulations(leaves, start=0, stop=None):
    '''Clear articulations from leaves.
    '''

    if isinstance(stop, int):
        stop += 1

    for l in instances(leaves[start : stop], 'Leaf'):
        l.articulations = []


def appendArticulations(voice, articulations, *args, **kwargs):
    '''Iterate leaves and append articulations.
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
        if isinstance(l, (notetools.Note, chordtools.Chord)) or not exclude:
            if isinstance(articulations, str):
                l.articulations.append(articulations)
            elif isinstance(articulations, list):
                for articulation in articulations:
                    l.articulations.extend(articulation)
            else:
                raise ValueError


def clear_dynamics(expr):
    '''Clear both dynamics and hairpins from leaves in expr.
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
        if isinstance(l, notetools.Note):
            l.add_artificial_harmonic(diatonicInterval)


def hpartition_notes_only(leaves, cut=(0,), gap=(0,)):
    '''Note runs only.
    '''

    cut = fractions.Fraction(*cut)
    gap = fractions.Fraction(*gap)
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
    '''Rest-terminated note runs.
    '''

    cut = fractions.Fraction(*cut)
    gap = fractions.Fraction(*gap)
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


def partitionLeaves(leaves, type='notes and rests', cut=(0,), gap=(0,)):
    '''Partition leaf list leaves into sublists.

    Chunking suitable for repeated hairpin application.

    >>> t = Tuplet((8, 9), "c'16 c'16 r16 r16 c'16 c'16 r16 r16 r16")

    >>> partitionLeaves(t.select_leaves())
    [[Note("c'16"), Note("c'16")], [Rest('r16'), Rest('r16')], [Note("c'16"), Note("c'16")], [Rest('r16'), Rest('r16'), Rest('r16')]]

    >>> partitionLeaves(t.select_leaves(), type='notes only')
    [[Note("c'16"), Note("c'16")], [Note("c'16"), Note("c'16")]]

    >>> partitionLeaves(t.select_leaves(), type='rests only')
    [[Rest('r16'), Rest('r16')], [Rest('r16'), Rest('r16'), Rest('r16')]]

    >>> partitionLeaves(t.select_leaves(), type='rest-terminated')
    [[Note("c'16"), Note("c'16"), Rest('r16')], [Note("c'16"), Note("c'16"), Rest('r16')]]

    >>> music.partitionLeaves(t.select_leaves(), type='rest-gapped')
    [([Note("c'16"), Note("c'16"), Rest('r16')],), ([Note("c'16"), Note("c'16"), Rest('r16')],)]

    >>> music.partitionLeaves(t.select_leaves(), type='rest-gapped', gap=(2, 18))
    [([Note("c'16"), Note("c'16"), Rest('r16')], [Note("c'16"), Note("c'16"), Rest('r16')])]

    >>> partitionLeaves(t.select_leaves(), type='paired notes')
    [([Note("c'16"), Note("c'16")],), ([Note("c'16"), Note("c'16")],)]

    >>> partitionLeaves(t.select_leaves(), type='paired notes', gap=(2, 18))
    [([Note("c'16"), Note("c'16")], [Note("c'16"), Note("c'16")])]

    >>> t = Container("c'16 r16 c'16 r8. c'16 r16 r16 c'16")

    >>> partitionLeaves(t.select_leaves(), type='cut notes', cut=(1, 16))
    [[Note("c'16"), Rest('r16'), Note("c'16")], [Note("c'16")], [Note("c'16")]]

    >>> partitionLeaves(t.select_leaves(), type='cut paired notes', cut=(1, 16), gap=(2, 16))
    [([Note("c'16"), Rest('r16'), Note("c'16")],), ([Note("c'16")], [Note("c'16")])]

    >>> partitionLeaves(t.select_leaves(), type='cut paired notes', cut=(1, 16), gap=(3, 16))
    [([Note("c'16"), Rest('r16'), Note("c'16")], [Note("c'16")]), ([Note("c'16")],)]

    Return list of components.
    '''

    cut = fractions.Fraction(*cut)
    gap = fractions.Fraction(*gap)
    result = [[]]

    if type == 'notes and rests':
        for l in leaves:
            lastChunk = result[-1]
            if len(lastChunk) == 0:
                lastChunk.append(l)
            else:
                lastLeaf = lastChunk[-1]
                if isinstance(lastLeaf, notetools.Note) == isinstance(l, notetools.Note):
                    lastChunk.append(l)
                else:
                    result.append([l])

    elif type == 'notes only':
        for l in leaves:
            lastChunk = result[-1]
            if isinstance(l, notetools.Note):
                lastChunk.append(l)
            else:
                if len(lastChunk) > 0:
                    result.append([])
        if result[-1] == []:
            result.pop()

    elif type == 'cut notes':
        firstResult = partitionLeaves(leaves, type = 'notes and rests')
        if not isinstance(firstResult[0][0], notetools.Note):
            firstResult.pop(0)
        result = [firstResult.pop(0)]
        for chunk in firstResult:
            lastChunk = result[-1]
            if isinstance(chunk[0], notetools.Note):
                # empty
                if len(lastChunk) == 0:
                    lastChunk.extend(chunk)
                # note-terminated
                elif isinstance(lastChunk[-1], notetools.Note):
                    result.append(chunk)
                # rest-terminated
                else:
                    lastChunk.extend(chunk)
            else:
                if effectiveDuration(chunk) <= cut:
                    lastChunk.extend(chunk)
                else:
                    result.append([])
        if result[-1] == []:
            result.pop()

    elif type == 'cut paired notes':
        firstResult = partitionLeaves(leaves, type = 'notes and rests')
        if not isinstance(firstResult[0][0], notetools.Note):
            firstResult.pop(0)
        result = [[[]]]
        for chunk in firstResult:
            lastPair = result[-1]
            lastChunk = lastPair[-1]
            if isinstance(chunk[0], notetools.Note):
                lastChunk.extend(chunk)
            else:
                if effectiveDuration(chunk) <= cut:
                    lastChunk.extend(chunk)
                elif cut < effectiveDuration(chunk) <= gap:
                    if len(lastPair) == 1:
                        lastPair.append([])
                    elif len(lastPair) == 2:
                        result.append([[]])
                    else:
                        raise Exception
                elif effectiveDuration(chunk) > gap:
                    result.append([[]])
                else:
                    raise Exception
        lastChunk = result[-1][-1]
        for m in reversed(lastChunk):
            if not isinstance(m, notetools.Note):
                lastChunk.pop(-1)
            else:
                break
        for i, sublist in enumerate(result):
            result[i] = tuple(sublist)

    elif type == 'rests only':
        for l in leaves:
            lastChunk = result[-1]
            if isinstance(l, resttools.Rest):
                lastChunk.append(l)
            else:
                if len(lastChunk) > 0:
                    result.append([])
        if result[-1] == []:
            result.pop()

    elif type == 'rest-terminated':
        for l in leaves:
            lastChunk = result[-1]
            if isinstance(l, notetools.Note):
                if len(lastChunk) == 0:
                    lastChunk.append(l)
                else:
                    lastLeaf = lastChunk[-1]
                    if isinstance(lastLeaf, notetools.Note):
                        lastChunk.append(l)
                    else:
                        result.append([l])
            elif isinstance(l, resttools.Rest):
                if len(lastChunk) > 0:
                    lastLeaf = lastChunk[-1]
                    if isinstance(lastLeaf, notetools.Note):
                        lastChunk.append(l)

    # the gap input parameter is the duration of rest run to bridge over;
    # accepting gap = (0,) makes rest-gapped return like rest-terminated
    elif type == 'rest-gapped':
        firstResult = partitionLeaves(leaves, type = 'notes and rests')
        if not isinstance(firstResult[0][0], notetools.Note):
            firstResult.pop(0)
        result = [[firstResult.pop(0)]]
        bridged = False
        bridgeNext = False
        for chunk in firstResult:
            if not isinstance(chunk[0], notetools.Note):
                result[-1][-1].append(chunk[0])
                if effectiveDuration(chunk) <= gap:
                    if not bridged:
                        bridgeNext = True
            else:
                if bridgeNext:
                    result[-1].append(chunk)
                    bridged = True
                    bridgeNext = False
                else:
                    result.append([chunk])
                    bridged = False
                    bridgeNext = False
        for i, sublist in enumerate(result):
            result[i] = tuple(sublist)

    elif type == 'paired notes':
        firstResult = partitionLeaves(leaves, type = 'notes and rests')
        if not isinstance(firstResult[0][0], notetools.Note):
            firstResult.pop(0)
        result = [[firstResult.pop(0)]]
        bridged = False
        bridgeNext = False
        for chunk in firstResult:
            if not isinstance(chunk[0], notetools.Note):
                if effectiveDuration(chunk) <= gap:
                    if not bridged:
                        bridgeNext = True
            else:
                if bridgeNext:
                    result[-1].append(chunk)
                    bridged = True
                    bridgeNext = False
                else:
                    result.append([chunk])
                    bridged = False
                    bridgeNext = False
        for i, sublist in enumerate(result):
            result[i] = tuple(sublist)

    else:
        raise ValueError

    return result


def segmentLeaves(leaves, cut=(0,), gap=(0,)):
    '''Partition leaves into segments each of one or more stages;
    include rests of duration less than or equal to cut in each stage;
    rests of duration greater than or equal to gap begin new stages.

    >>> t = Container("c'16 r16 c'16 r8 c'16 r16 c'16 r8. c'16 r16 c'16")

    >>> segmentLeaves(t.select_leaves())
    [([Note("c'16")],), ([Note("c'16")],), ([Note("c'16")],), ([Note("c'16")],), ([Note("c'16")],), ([Note("c'16")],)]

    >>> segmentLeaves(t.select_leaves(), (1, 16))
    [([Note("c'16"), Rest('r16'), Note("c'16")],), ([Note("c'16"), Rest('r16'), Note("c'16")],), ([Note("c'16"), Rest('r16'), Note("c'16")],)]

    >>> segmentLeaves(t.select_leaves(), (2, 16))
    [([Note("c'16"), Rest('r16'), Note("c'16"), Rest('r8'), Note("c'16"), Rest('r16'), Note("c'16")],), ([Note("c'16"), Rest('r16'), Note("c'16")],)]

    >>> segmentLeaves(t.select_leaves(), (3, 16))
    [([Note("c'16"), Rest('r16'), Note("c'16"), Rest('r8'), Note("c'16"), Rest('r16'), Note("c'16"), Rest('r8.'), Note("c'16"), Rest('r16'), Note("c'16")],)]

    >>> segmentLeaves(t.select_leaves(), (1, 16), (3, 16))
    [([Note("c'16"), Rest('r16'), Note("c'16")], [Note("c'16"), Rest('r16'), Note("c'16")]), ([Note("c'16"), Rest('r16'), Note("c'16")],)]

    Return list of components.
    '''

    cut = fractions.Fraction(*cut)
    gap = fractions.Fraction(*gap)
    parts = partitionLeaves(leaves)
    if not isinstance(parts[0][0], notetools.Note):
        parts.pop(0)
    segments = [[[]]]
    for part in parts:
        segment = segments[-1]
        stage = segment[-1]
        if isinstance(part[0], notetools.Note):
            stage.extend(part)
        else:
            if effectiveDuration(part) <= cut:
                stage.extend(part)
            elif cut < effectiveDuration(part) < gap:
                segment.append([])
            elif effectiveDuration(part) >= gap:
                segments.append([[]])
            else:
                raise Exception
    trimEmptyLists(segments[-1])
    trimEmptyLists(segments)
    trimRests(segments[-1][-1])
    for i, sublist in enumerate(segments):
        segments[i] = tuple(sublist)
    return segments


def trimRests(leaves):
    for l in reversed(leaves):
        #if isinstance(l, rest):
        if isinstance(l, resttools.Rest):
            leaves.pop(-1)
        else:
            break

def trimEmptyLists(l):
    for x in reversed(l):
        if x == []:
            l.pop(-1)
        else:
            break

### TODO - encapsulate this into some type of class;    ###
###        possibly TextSpanner or special CoverSpanner ###
def applyCoverSpanner(voice, *args):
    leaves = voice.select_leaves()
    if len(args) == 1:
        i = args[0]
        leaves[i].formatter.right.append(
            r'^ \markup { \italic \fontsize #2 "coperta" }')
    elif len(args) == 2:
        start, stop = args
        leaves[start].formatter.before.extend([
            r"\once \override TextSpanner #'bound-details #'left-broken " +
                r"#'X = #8",
            r"\once \override TextSpanner #'dash-fraction = #0.25",
            r"\once \override TextSpanner #'dash-period = #1",
            r"\once \override TextSpanner #'bound-details #'left " + \
                r"""#'text = \markup { \italic \fontsize #2 "coperta " }""",
            r"\once \override TextSpanner #'bound-details #'left " + \
                r"#'stencil-align-dir-y = #CENTER",
            r"\once \override TextSpanner #'bound-details #'right-broken " +
                r"#'text = ##f",
            r"\once \override TextSpanner #'bound-details #'right " +
                r"#'text = #(markup #:draw-line '(0 . -1))",
            r"\once \override TextSpanner #'staff-padding = #6",
            r"\once \override TextSpanner #'extra-offset = #'(0 . -2.5)"
            ])
        leaves[start].formatter.right.append(r'\startTextSpan')
        leaves[stop].formatter.right.append(r'\stopTextSpan')
    else:
        raise ValueError('can not apply cover spanner.')


def makeBreaksVoice(durationPairs, yOffsets, alignmentOffsets, start=0):
    '''Return page- and line-breaking skip voice;
    start at system start to allow first page title.

    >>> makeBreaksVoice([(10, 8), (10, 8), (9, 8)], [20, 120], [0, -36, -48], 1)
    Voice-"breaks voice"{3}

    >>> f(_) # doctest: +SKIP
    % breaks voice
    \\new Voice {
        \\overrideProperty #"Score.NonMusicalPaperColumn"
        #'line-break-system-details
        #'((Y-offset . 120)
        (alignment-offsets . (0 -36 -48)))
        s1 * 5/4 \\bar "" \\pageBreak
        \\overrideProperty #"Score.NonMusicalPaperColumn"
        #'line-break-system-details
        #'((Y-offset . 20)
        (alignment-offsets . (0 -36 -48)))
        s1 * 5/4 \\bar "" \\break
        \\overrideProperty #"Score.NonMusicalPaperColumn"
        #'line-break-system-details
        #'((Y-offset . 120)
        (alignment-offsets . (0 -36 -48)))
        s1 * 9/8 \\bar "" \\pageBreak
    }
    '''

    if not isinstance(yOffsets, list):
        yOffsets = [yOffsets]
    alignmentOffsets = ' '.join([str(x) for x in alignmentOffsets])
    breaks = []
    for p in durationPairs:
        try:
            skip = skiptools.Skip(p)
        except (ValueError, AssignabilityError):
            skip = skiptools.Skip((1, 1))
            skip.duration_multiplier = durationtools.Duration(p)
        breaks.append(skip)
    for i, b in enumerate(breaks):
        cyclicPosition = (start + i) % len(yOffsets)
        curYOffset = yOffsets[cyclicPosition]
        if cyclicPosition == len(yOffsets) - 1:
            curBreak = r'\pageBreak'
        else:
            curBreak = r'\break'
#        b.formatter.before.extend([
#            r'\overrideProperty #"Score.NonMusicalPaperColumn" ',
#            "#'line-break-system-details",
#            "#'((Y-offset . %s)" % curYOffset,
#            '(alignment-offsets . (%s)))' % alignmentOffsets])
#        b.formatter.right.extend([r'\bar ""', curBreak])
    voice = voicetools.Voice(breaks)
    voice.name = 'breaks voice'
    return voice


def makeMeasuresVoice(durationPairs):
    '''Return measure and time signature skip voice.

    >>> makeMeasuresVoice([(10, 8), (10, 8), (9, 8)])
    Voice-"measures voice"{3}

    >>> f(_)
    \context Voice = "measures voice" {
        {
            \time 10/8
            s1 * 5/4
        }
        {
            s1 * 5/4
        }
        {
            \time 9/8
            s1 * 9/8
        }
    }

    Return voice.
    '''

    measures = []
    for pair in durationPairs:
        skip = skiptools.Skip((1, 1))
        skip.duration_multiplier = durationtools.Duration(pair)
        measure = measuretools.Measure(pair, [skip])
        measures.append(measure)
    voice = voicetools.Voice(measures)
    voice.name = 'measures voice'
    return voice


def reddenSections(measuresVoice, sectionTuples, startMeasure=1):
    '''Redden section bars and label sections in red.

        >>> measuresVoice = makeMeasuresVoice([(10, 8), (10, 8), (9, 8)])
        >>> reddenSections(measuresVoice, [(1, 1, 2, 'I'), (2, 3, 3, 'II')])

    ::

        >>> f(measuresVoice)
        \context Voice = "measures voice" {
            {
                \time 10/8
                \once \override Score.BarLine #'color = #red
                \once \override Score.SpanBar #'color = #red
                s1 * 5/4
                    ^ \markup {
                        \fontsize
                            #2
                            \with-color
                                #red
                                \italic
                                    {
                                        1.
                                        I
                                    }
                        }
            }
            {
                s1 * 5/4
            }
            {
                \time 9/8
                \once \override Score.BarLine #'color = #red
                \once \override Score.SpanBar #'color = #red
                s1 * 9/8
                    ^ \markup {
                        \fontsize
                            #2
                            \with-color
                                #red
                                \italic
                                    {
                                        2.
                                        II
                                    }
                        }
            }
        }

    Return none.
    '''

    measureSkips = list(iterationtools.iterate_skips_in_expr(measuresVoice))

    for n, start, stop, description in sectionTuples:
        if start >= startMeasure:
            markup = markuptools.Markup(
                r'\fontsize #2 \with-color #red \italic { %s. %s }' % (n, description),
                direction=Up)
            try:
                ms = measureSkips[start - startMeasure]
                ms.override.score.bar_line.color = 'red'
                ms.override.score.span_bar.color = 'red'
                markup(ms)
            except:
                pass


def trimVoices(expr, nMeasures):
    '''Find each voice in expr and trim to n measures;
    useful for rendering only the first n measures of a score;
    accommodates attack, nucleus, release and reference contexts.
    '''

    customVoiceContexts = [
        'attack voice', 'nucleus voice', 'release voice', 'reference voice']
    voices = instances(expr, 'Voice') + scoretools.find(
        expr, *customVoiceContexts)
    for v in voices:
        v.music = v.music[:nMeasures]


def makeFluteGroup(*staves):
    '''Group staves together with 'Flute' id and 'flute group' name.
    '''

    return container.Container(list(staves),
        id = 'Flute', name = 'flute group')


def makeViolinGroup(*staves):
    '''Group staves together with 'Violin' id and 'violin group' name.
    '''

    return container.Container(list(staves),
        id = 'Violin', name = 'violin group')


def crossStavesDown(voice, start, stop, bp, target,
    includes=[], excludes=[],
    topBeamPositions=None, bottomBeamPositions=None):
    '''target is a reference to an actual Staff instance.

    TODO: run octavate at some time other than cross-determination time.
    '''

    leaves = voice.select_leaves()
    for j, l in enumerate(leaves[start : stop + 1]):
        i = start + j
        if isinstance(l, notetools.Note):
            #if (l.safePitchNumber >= bp or i in includes) and i not in excludes:
            if (spget(l) >= bp or i in includes) and i not in excludes:
                l.staff = target
            else:
                octavate(l, base = (-4, 30))


def crossStavesUp(leaves, start, stop, bp, target):
    '''target is a reference to an actual Staff instance.

    TODO: run octavate at some time other than cross-determination time.
    '''

    for i, l in enumerate(leaves[start : stop + 1]):
        if l.note:
            if l.pitch.number > bp:
                l.staff = target
            else:
                octavate(l, base = (-28, 4))
