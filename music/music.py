'''Music-generation functions used in Cary and Sekka.'''

from abjad import *
from baca.utilities.utilities import *
import copy
import math
import re


# TODO clean this whole function up and remove or greatly simply beam spec
def music(*args):
   '''
   music() takes many different types of argument list.
   '''

   if len(args) == 1:
      return interpretMusic(args)
   else:
      return expression.Expression([interpretMusic(arg) for arg in args])

def interpretMusic(arg):
   """
   Helper function for music().
   """

   # get beam spec if there is one
   # '2 2 3' or '2 2=1=2' or '3=1=3 3=1=3 -2'
   try:
      B = arg[-1].split(' ')
      for i, b in enumerate(B):
         try:
            B[i] = int(b)
         except:
            # '3=1=3'
            try:
               B[i] = tuple([int(x) for x in b.split('=')])
            except:
               # '0,2=1,1=1,1=1,4=2,0'
               B[i] = tuple([tuple([int(y) for y in x.split(',')]) for \
                  x in b.split('=')])
      beamSpec = B
      if beamSpec.__class__.__name__ == 'list':
         beamSpec = [tuple(beamSpec)]
      print 'found beam spec %s' % str(beamSpec)
      arg = arg[:-1]
   except:
      try:
         if arg[-1] == 'all':
            #print 'found all beam spec.'
            beamSpec = ('all',)
            arg = arg[:-1]
         if arg[-1] == 'none':
            #print 'found none beam spec.'
            beamSpec = ('none',)
            arg = arg[:-1]
      except:
         beamSpec = None

   # QUESTION: why is this here?
   try:
      arg = arg[0]
   except:
      pass

   # music(2) or music(-2)
   if isinstance(arg, int):
      if arg >= 0:
         return Note(0, 1, 2 ** (arg + 2))
      else:
         return Rest(1, 2 ** (abs(arg) + 2))

   # music(-3.3)
   if isinstance(arg, float):
      flags = int(abs(arg))
      d = 2 ** (flags + 2)
      dots = int(abs(arg * 10)) % 10
      r = duration.dotRatio(dots)
      if arg > 0:
         return Note(0, r.effective.numerator, d * r.effective.denominator)
      elif arg < 0:
         return Rest(r.effective.numerator, d * r.effective.denominator)

   elif isinstance(arg, list):
      # [2, 1, 1, 1, 'eighth', 'music list']
      if arg[-1] == 'music list' and arg[-2] in duration.durationNames:
         m = music(arg[:-1])
         # clean() removes effectiveDurations
         #return expression.Expression(clean(m.music))
         removeEffectiveDurations(m)
         return expression.Expression(m.music)
      # [[7, 'thirtysecond'], [5, 'thirtysecond'], 'music list']
      elif arg[-1] == 'music list':
         m = [interpretMusic(x) for x in arg[:-1]]
         m = expression.Expression(m)
         #print 'now using %s' % str(beamSpec)
         try:
            m.beam(*beamSpec)
         except:
            pass
         return m
      # [7, 'thirtysecond']
      if arg[-1] in duration.durationNames and len(arg) == 2:
         body = []
         # [7, 'thirtysecond']
         if arg[0] > 0:
            for i in range(arg[0]):
               body.append(
                  Note(0, 1, 2 ** duration.durationNameToLog(arg[-1])))
         # [-1, 'eighth']
         elif arg[0] == -1:
            body.append(Rest(1, 2 ** duration.durationNameToLog(arg[-1])))
         m = tuplet.SmartTuplet(duration.phi(arg[0]), 
            2 ** duration.durationNameToLog(arg[-1]), body)
         try:
            m.beam(*beamSpec)
         except:
            pass
         return m

      # [2, 1, 1, 1, 'eighth']
      elif arg[-1] in duration.durationNames and len(arg) > 2:
         denominator = 2 ** duration.durationNameToLog(arg[-1])
         body = []
         for n in arg[:-1]:
            if n > 0:
               body.append(Note(0, n, denominator))
            elif n < 0:
               body.append(Rest(abs(n), denominator))
         bodyDuration = sum([m.duration for m in body], Rational(0))
         m = tuplet.SmartTuplet(
            bodyDuration.phi.effective.numerator, 
            bodyDuration.phi.effective.denominator, body)
         try:
            m.beam(*beamSpec)
         except:
            pass
         return m

      # [13, 'sixtyfourth', '13:10'] or [7, 5, 1, 'sixtyfourth', '13:10']
      elif len(arg) >= 3 and arg[-2] in duration.durationNames:
         body = interpretMusic(arg[:-1]).music
         bodyDuration = sum([m.duration for m in body], Rational(0))
         r = ratio(arg[-1]) * bodyDuration
         m = tuplet.SmartTuplet(
            r.effective.numerator, 
            r.effective.denominator, 
            body, 
            rewritten = tuple([int(part) for part in arg[-1].split(':')]))
         try:
            m.beam(*beamSpec)
         except:
            pass
         return m

      # [1, 1, 2] or [2, (1, 4)]
      elif arg[-1].__class__.__name__ != 'str':
         prolationIndicator = None
         body = arg[:]
      # [1, 1, 2, '5:6']
      elif arg[-1].__class__.__name__ == 'str' and \
         arg[-1] not in duration.durationNames:
         prolationIndicator = arg[-1]
         body = arg[:-1]
      #print prolationIndicator
      body = [interpretMusic(m) for m in body]
      #print body
      bodyDuration = sum([m.duration for m in body], Rational(0))
      #print bodyDuration
      if prolationIndicator == None:
         prolationRatio = Rational(
            duration.phi(bodyDuration.numerator), bodyDuration.numerator) 
      else:
         prolationRatio = Rational(
            int(prolationIndicator.split(':')[1]), 
            int(prolationIndicator.split(':')[0]))
      #print prolationRatio
      tupletDuration = bodyDuration * prolationRatio 
      #print tupletDuration
      #print 'writtenFraction is %s' % prolationIndicator
      m = tuplet.SmartTuplet(
         tupletDuration.effective.numerator, 
         tupletDuration.effective.denominator, 
         body, writtenFraction = prolationIndicator)
      try:
         m.beam(*beamSpec)
      except:
         pass
      return m
            
def removeEffectiveDurations(expr):
   '''
   Helper function for kludgy old divide() function;
   to deprecate clean().
   '''

   for l in expr.leaves:
      if hasattr(l, 'scaledDuration'):
         delattr(l, 'scaledDuration')

def beamable(expr):
   '''
   >>> beamable(Note(0, 1, 4))
   False

   >>> beamable(Note(0, 1, 8))
   True
   '''

   try:
      if expr.__class__.__name__ == 'Note' and expr.duration._flags > 0:
         return True
      else:
         return False
   except:
      return False

def beam(m, b = None, rip = True, span = False, nib = False, lone = 'flat'):
   '''
   NOTE: this beam() procedure is 14 times faster than LilyObject.beam();
   256 groups of 4 thirty-seconds take 7 seconds with LilyObject.beam();
   256 groups of 4 thirty-seconds take only 0.5 seconds with beam().
   TODO: deprecate LilyObject.beam().

   TODO: incorporate beamMany().

   TODO: large combinatorial beam regression battery. 

   >>> decompose((2, 4), [(1, 16)])
   [c'16, c'16, c'16, c'16, c'16, c'16, c'16, c'16]
   >>> m = _
   >>> beam(m, [(1, 8)])
   >>> f(voice.Voice(m))
   \\new Voice {
           \\beam #0 #2 c'16 [
           \\beam #2 #0 c'16 ]
           \\beam #0 #2 c'16 [
           \\beam #2 #0 c'16 ]
           \\beam #0 #2 c'16 [
           \\beam #2 #0 c'16 ]
           \\beam #0 #2 c'16 [
           \\beam #2 #0 c'16 ]
   }

   >>> beam(m, [(1, 8), (3, 16)])
   >>> f(voice.Voice(m))
   \\new Voice {
           \\beam #0 #2 c'16 [
           \\beam #2 #0 c'16 ]
           \\beam #0 #2 c'16 [
           \\beam #2 #2 c'16
           \\beam #2 #0 c'16 ]
           \\beam #0 #2 c'16 [
           \\beam #2 #0 c'16 ]
           \\beam #0 #2 c'16 [ ]
   }
   '''

   debug = False

   d = []
   if b == None:
      d.append(effectiveDuration(m))
   else:
      for part in b:
         if part.__class__.__name__ == 'Duration':
            d.append(Rational(part.n, part.d))
         elif isinstance(part, tuple):
            d.append(Rational(part[0], part[1]))
         else:
            raise ValueError

   leaves = instances(m, '_Leaf')
   t = len(leaves)

   curBeam = 0
   nextBeam = d[curBeam]

   curStartPoint = Rational(0)
   curStopPoint = Rational(0, 1)
   prevLeafEncounteredBeam = False
   curLeafEncountersBeam = False

   for i in range(t):

      if i == 0:
         prevLeaf = None
         prevLeafEncounteredBeam = True
         beamablePrevLeaf = False
         prevFlags = 0
      else:
         prevLeaf = leaves[i - 1]
         beamablePrevLeaf = beamable(prevLeaf)
         if beamablePrevLeaf:
            prevFlags = prevLeaf.duration._flags
         else:
            prevFlags = 0

      curLeaf = leaves[i]

      if i == t - 1:
         nextLeaf = None
         beamableNextLeaf = False
         nextFlags = 0
      else:
         nextLeaf = leaves[i + 1]
         beamableNextLeaf = beamable(nextLeaf)
         if beamableNextLeaf:
            nextFlags = nextLeaf.duration._flags
         else:
            nextFlags = 0

      curLeaf.unbeam()

      f = curLeaf.duration._flags
      curStopPoint += curLeaf.effectiveDuration
      if curStopPoint >= nextBeam:
         curLeafEncountersBeam = True
      else:
         curLeafEncountersBeam = False

      if debug:
         print curStartPoint.written, '\t',
         print curStopPoint.written, '\t',
         print nextBeam.written, '\t',
         print prevLeafEncounteredBeam, '\t',
         print curLeafEncountersBeam, '\t',

      if span:
         candidateBackSpan = max(prevFlags - 1, 1)
         candidateCurSpan = max(f - 1, 1)
         candidateForeSpan = max(nextFlags - 1, 1)
         backSpan = min(candidateCurSpan, candidateBackSpan, span)
         foreSpan = min(candidateCurSpan, candidateForeSpan, span)

      if beamable(curLeaf):
         # occupies full slot
         if prevLeafEncounteredBeam and curLeafEncountersBeam:
            if span:
               # occupies both full slot and full span
               if i == 0 == t - 1:
                  if debug: print '1a'
                  pass
               # occupies full slot only at beginning of span
               elif i == 0 and i < t - 1:
                  if beamableNextLeaf:
                     if debug: print '1b1'
                     curLeaf.right.append('[')
                     curLeaf.left.append(r'\beam #0 #%s' % f)
                  else:
                     if debug: print '1b2'
                     curLeaf.right.append('[')
                     curLeaf.right.append(']')
                     curLeaf.left.append(r'\beam #0 #%s' % f)
               # occupies full slot strictly in middle of span
               elif i > 0 and i < t - 1:
                  if beamablePrevLeaf and beamableNextLeaf:
                     if debug: print '1c1'
                     curLeaf.left.append(r'\beam #%s #%s' % (f, foreSpan))
                  elif beamablePrevLeaf and not beamableNextLeaf:
                     if debug: print '1c2'
                     curLeaf.left.append(r'\beam #%s #0' % f)
                     curLeaf.right.append(']')
                  elif not beamablePrevLeaf and beamableNextLeaf:
                     if debug: print '1c3'
                     curLeaf.right.append('[')
                     curLeaf.left.append(r'\beam #0 #%s' % f)
                  elif not beamablePrevLeaf and not beamableNextLeaf:
                     if debug: print '1c4'
                     curLeaf.right.append('[')
                     curLeaf.right.append(']')
                     curLeaf.left.append(r'\beam #%s #%s' % (f, f))
                  else:
                     if debug: print '1c5'
                     print 'Prev and next leaves should be beamable or not.'
                     raise ValueError
               # occupies full slot only at end of span
               elif i > 0 and i == t - 1:
                  if beamablePrevLeaf:
                     if debug: print '1d1'
                     curLeaf.right.append(']')
                     curLeaf.left.append(r'\beam #%s #0' % f)
                  else:
                     if debug: print '1d2'
                     curLeaf.right.append('[')
                     curLeaf.right.append(']')
                     curLeaf.left.append(r'\beam #%s #0' % f)
               else:
                  if debug: print '1e'
                  print 'Slot should be at beginning, middle or end of span.'
                  raise ValueError
         # occupies first part of slot only
         elif prevLeafEncounteredBeam and not curLeafEncountersBeam:
            if beamableNextLeaf:
               if debug: print '2'
               if span and i > 0 and beamablePrevLeaf:
                  curLeaf.left.append(r'\beam #%s #%s' % (backSpan, f))
               elif span and i > 0 and prevLeaf.kind('Rest'):
                  curLeaf.right.append('[')
                  if span == 1 and not nib:
                     curLeaf.left.append(r'\beam #0 #%s' % f)
                  else:
                     curLeaf.left.append(r'\beam #%s #%s' % (backSpan, f))
               else:
                  curLeaf.right.append('[')
                  curLeaf.left.append(r'\beam #0 #%s' % f)
            else:
               if rip:
                  if debug: print '3'
                  if span and i > 0 and beamablePrevLeaf:
                     curLeaf.right.append(']')
                     if f > 1:
                        curLeaf.left.append(r'\beam #%s #%s' % (backSpan, f))
                     else:
                        # not sure if following one is right
                        curLeaf.left.append(r'\beam #%s #0' % backSpan)
                  else:
                     curLeaf.right.append('[')
                     curLeaf.right.append(']')
                     curLeaf.left.append(r'\beam #0 #%s' % f)
         # occupies last part of slot only
         elif not prevLeafEncounteredBeam and curLeafEncountersBeam:
            if beamablePrevLeaf:
               if span and i < t - 1 and beamableNextLeaf:
                  if debug: print '4a'
                  curLeaf.left.append(r'\beam #%s #%s' % (f, foreSpan))
               elif span and i < t - 1 and nextLeaf.kind('Rest'):
                  curLeaf.right.append(']')
                  if span == 1 and not nib:
                     if debug: print '4b1'
                     curLeaf.left.append(r'\beam #%s #0' % f)
                  else:
                     if debug: print '4b2'
                     curLeaf.left.append(r'\beam #%s #%s' % (f, foreSpan))
               else:
                  if debug: print '4c'
                  curLeaf.right.append(']')
                  curLeaf.left.append(r'\beam #%s #0' % f)
            else:
               if rip:
                  if debug: print '5'
                  if span and i < t - 1 and beamableNextLeaf:
                     curLeaf.right.append('[')
                     if f > 1:
                        curLeaf.left.append(r'\beam #%s #%s' % (f, foreSpan))
                     else:
                        # not sure if following is right
                        curLeaf.left.append(r'\beam #0 #%s' % foreSpan)
                  else:
                     curLeaf.right.append('[')
                     curLeaf.right.append(']')
                     curLeaf.left.append(r'\beam #%s #0' % f)
         # occupies strictly middle part of slot
         elif not prevLeafEncounteredBeam and not curLeafEncountersBeam:
            if beamablePrevLeaf and beamableNextLeaf:
               if debug: print '6'
               if prevFlags  < f  < nextFlags:
                  curLeaf.left.append(r'\beam #%s #%s' % (prevFlags, f))
               if prevFlags  < f == nextFlags:
                  curLeaf.left.append(r'\beam #%s #%s' % (prevFlags, f))
               if prevFlags  < f  > nextFlags:
                  curLeaf.left.append(r'\beam #%s #%s' % (f, nextFlags))
               if prevFlags == f  < nextFlags:
                  curLeaf.left.append(r'\beam #%s #%s' % (f, f))
               if prevFlags == f == nextFlags:
                  curLeaf.left.append(r'\beam #%s #%s' % (f, f))
               if prevFlags == f  > nextFlags:
                  curLeaf.left.append(r'\beam #%s #%s' % (f, nextFlags))
               if prevFlags  > f  < nextFlags:
                  curLeaf.left.append(r'\beam #%s #%s' % (f, f))
               if prevFlags  > f == nextFlags:
                  curLeaf.left.append(r'\beam #%s #%s' % (f, f))
               if prevFlags  > f  > nextFlags:
                  curLeaf.left.append(r'\beam #%s #%s' % (f, nextFlags))

            if beamablePrevLeaf and not beamableNextLeaf:
               curLeaf.right.append(']')
               if rip:
                  if debug: print '7'
                  if f > 1:
                     #curLeaf.left.append(r'\beam #%s #%s' % (f, f))
                     if prevFlags <  f:
                        curLeaf.left.append(r'\beam #%s #%s' % (prevFlags, f))
                     if prevFlags == f:
                        curLeaf.left.append(r'\beam #%s #%s' % (f, f))
                     if prevFlags >  f:
                        curLeaf.left.append(r'\beam #%s #%s' % (f, f))
                  else:
                     curLeaf.left.append(r'\beam #%s #0' % f)
               else:
                  if debug: print '8'
                  curLeaf.left.append(r'\beam #%s #0' % f)
            if not beamablePrevLeaf and beamableNextLeaf:
               curLeaf.right.append('[')
               if rip:
                  if debug: print '9'
                  if f > 1:
                     #curLeaf.left.append(r'\beam #%s #%s' % (f, f))
                     if f  < nextFlags:
                        curLeaf.left.append(r'\beam #%s #%s' % (f, f))
                     if f == nextFlags:
                        curLeaf.left.append(r'\beam #%s #%s' % (f, f))
                     if f  > nextFlags:
                        curLeaf.left.append(r'\beam #%s #%s' % (f, nextFlags))
                  else:
                     curLeaf.left.append(r'\beam #0 #%s' % f)
               else:
                  if debug: print '10'
                  curLeaf.left.append(r'\beam #0 #%s' % f)
            if not beamablePrevLeaf and not beamableNextLeaf:
               if rip:
                  if debug: print '11'
                  curLeaf.right.append('[')
                  curLeaf.right.append(']')
                  curLeaf.left.append(r'\beam #%s #%s' % (f, f))
         else:
            print 'Leaf should occupy all, first, middle or last of slot.'
            raise ValueError
      else:
         if debug: print '0'
         
      curStartPoint = curStopPoint
      while curStartPoint >= nextBeam:
         curBeam += 1
         nextBeam += d[curBeam % len(d)]
      if curLeafEncountersBeam:
         prevLeafEncounteredBeam = True
      else:
         prevLeafEncounteredBeam = False

   if lone == 'flag' and len(leaves) == 1:
      leaves[i].unbeam()

def beamMany(m, partsList, rip = True, span = False, lone = 'flat'):
   '''
   Iterate over beam();
   partsList shows separate span groups as separate lists;
   subgroups as tuples within lists.

   TODO: incorporate into beam();
   TODO: create unified rhythmic specification.

   >>> t = divide([1, 1, 1], 2, 32)
   >>> m = clone(t, 3)
   >>> beamMany(m, [[(2, 32)], [(2, 32), (2, 32)]], span = 2)
   >>> f(voice.Voice(m))
   \\new Voice {
           \\once \override TupletBracket #'bracket-visibility = ##t
           \\times 2/3 {
                   \\beam #0 #3 c'32 [
                   \\beam #3 #3 c'32
                   \\beam #3 #0 c'32 ]
           }
           \\once \override TupletBracket #'bracket-visibility = ##t
           \\times 2/3 {
                   \\beam #0 #3 c'32 [
                   \\beam #3 #3 c'32
                   \\beam #3 #2 c'32
           }
           \\once \override TupletBracket #'bracket-visibility = ##t
           \\times 2/3 {
                   \\beam #2 #3 c'32
                   \\beam #3 #3 c'32
                   \\beam #3 #0 c'32 ]
           }
   }
   '''

   partition(m, [len(part) for part in partsList])

   for i, sublist in enumerate(m):
      beam(sublist, partsList[i], rip = rip, span = span, lone = lone)

   flatten(m)
   
def beams(music):
   '''
   Beam a freshly made list of tuplets or expressions.
   '''

   for m in music:
      try:
         m.beam('all left')
      except:
         pass

#def correctBeams(music, debug = False):
#   '''
#   Correct three of six different beam error cases.
#   '''
#
#   openBeam = False
#   for v in instances(music, 'Voice'):
#      for l in instances(v, '_Leaf'):
#         # if we're trying to open a beam within an open beam
#         if l.startBeam:
#            if openBeam:
#               if debug:
#                  print 'found 1'
#                  l.right.append(r' ^ \markup { ERROR 1 }')
#            else:
#               openBeam = True
#         # if we're trying to close a beam outside of an open beam
#         if not openBeam and l.stopBeam:
#            if debug:
#               print 'found 2'
#               l.right.append(r' ^ \markup { ERROR 2 }')
#         # if we're trying to beam over a quarter note or greater
#         if openBeam and l.duration >= Rational(1, 4):
#            if debug:
#               print 'found 3'
#               l.right.append(r' ^ \markup { ERROR 3 }')
#         # if we have a nibbed eighth note or greater
#         if l.duration >= Rational(1, 8) and l.startBeam and l.stopBeam:
#            if debug:
#               print 'found 4'
#               l.right.append(r' ^ \markup { ERROR 4 }')
#            l.unbeam()
#            openBeam = False
#         # if we have a left-pointing eighth note nib
#         if l.startBeam and l.leftCount == 1:
#            if debug:
#               print 'found 5'
#               l.right.append(r' ^ \markup { ERROR 5 }')
#            new = r'\beam #0 #%s' % l.rightCount
#            l.removeBeamCounts()
#            l.left.append(new)
#         # if we have a right-pointing eighth note nib
#         if l.stopBeam and l.rightCount == 1:
#            if debug:
#               print 'found 6'
#               l.right.append(r' ^ \markup { ERROR 6 }')
#            new = r'\beam #%s #0' % l.leftCount
#            l.removeBeamCounts()
#            l.left.append(new)
#         if l.stopBeam:
#            openBeam = False      


def trim_beam_nibs(expr):
   leaves = instances(expr, '_Leaf')
   for leaf in leaves:
      if hasattr(leaf, 'beam'):
         if not leaf.beam.only:
            if leaf.beam.first:
               leaf.beam.counts = 0, leaf.beam._flags
            if leaf.beam.last:
               leaf.beam.counts = leaf.beam._flags, 0


#def trim_beam_nibs(expr):
#   '''Use optionally immediately after copy to clean things up.'''
#   leaves = instances(expr, '_Leaf')
#   if len(leaves) == 1:
#      leaf = leaves[0]
#      if hasattr(leaf, 'beam') and leaf.beam.only:
#         leaf.beam.counts = 0, leaf.beam._flags
#   elif len(leaves) > 1:
#      left, right = leaves[0], leaves[-1] 
#      if hasattr(left, 'beam') and left.beam.first:
#         left.beam.counts = 0, left.beam._flags
#      if hasattr(right, 'beam') and right.beam.last:
#         right.beam.counts = right.beam._flags, 0


def splitPitches(pitches, split = -1):
   ''' 
   Split list of probably aggregates into treble and bass.
   '''

#   treble = []
#   bass = []

   for sublist in pitches:

      components = {'treble': [], 'bass': []}
      for n in sublist:
         if n >= split:
            components['treble'].append(n)
         else:
            components['bass'].append(n)

      for register in ('treble', 'bass'):
         if len(components[register]) == 0:
            #treble.append(skip.Skip((1, 4)))
            components[register] = Skip((1, 4))
         elif len(components[register]) == 1:
            #treble.append(Note(components[register], (1, 4)))
            components[register] = Note(components[register], (1, 4))
         else:
            #treble.append(Chord(components['treble'], (1, 4)))
            components[register] = Chord(components[register], (1, 4))
      
#      if len(components['treble']) == 0:
#         treble.append(skip.Skip((1, 4)))
#      elif len(components['treble']) == 1:
#         treble.append(Note(components['treble'], (1, 4)))
#      else:
#         treble.append(Chord(components['treble'], (1, 4)))
#
#      if len(components['bass']) == 0:
#         bass.append(skip.Skip((1, 4)))
#      elif len(components['bass']) == 1:
#         treble.append(Note(components['bass'], (1, 4)))
#      else:
#         bass.append(Chord(components['bass'], (1, 4)))

#   return treble, bass
   return components['treble'], components['bass']

def makeFixedLayoutVoice(d, systems, alignments, offsets):

   '''
   Doc.
   '''

   alignment = ' '.join([str(n) for n in alignments])
   alignment = "(alignment-offsets . (%s))" % alignment

   v = voice.Voice([], name = 'layout voice')
   for system in range(systems):
      new = skip.Skip(*d)
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

def getDurations(arg):
   if hasattr(arg, 'duration'):
      return arg.duration
   elif hasattr(arg, 'music'):
      return [getDurations(element) for element in arg.music]
   elif isinstance(arg, list):
      return [getDurations(element) for element in arg]
   else:
      return None

def getEffectiveDurations(music):
   return [l.effectiveDuration for l in instances(music, '_Leaf')]

# argument is a music list
def getListDurations(arg):
   def helper(arg):
      # note, rest, skip:
      if hasattr(arg, 'durations'):
         return arg.durations
      elif hasattr(arg, 'duration'):
         return [arg.duration]
      else:
         raise ValueError
   return [helper(element) for element in arg]
   
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
         
class Reconstructor(object):
   def __init__(self, visitor):
      self.visitor = visitor
      self.stack = [[]]
   def visit(self, node):
      if node.__class__.__name__ == 'list':
         pass
      elif hasattr(node, 'music'):
         self.stack.append([])
      else:
         self.stack[-1].append(self.visitor.visit(node))
   def unvisit(self, node):
      if node.__class__.__name__ == 'list':
         # FIXME: flatten now in-place
         self.stack = flatten(self.stack[-1])
      elif hasattr(node, 'music'):
         # FIXME: flatten now in-place
         node.music = flatten(self.stack.pop())
         self.stack[-1].append(node)

def reconstruct(music, reconstructor):
   # EXPENSIVE: deepcopy
   result = copy.deepcopy(music)
   traverse(result, reconstructor)
   return reconstructor.stack

class Painter(object):
   def __init__(self, pitches):
      self.pitches = pitches
   def visit(self, node):
      if len(self.pitches) > 0 and node.__class__.__name__ in ['Note', 'Chord']:
         p = self.pitches.pop(0)
         result = copy.deepcopy(node)
         if p.__class__.__name__ != 'list':
            if node.__class__.__name__ == 'Note':
               result.pitch = p
            elif node.__class__.__name__ == 'Chord':
               result.pitches = [p]
            else:
               raise ValueError
         elif p.__class__.__name__ == 'list':
            if node.__class__.__name__ == 'Note':
               result = chord(p, node.duration, *node.directives)
            elif node.__class__.__name__ == 'Chord':
               result.pitches = p
            else:
               raise ValueError
         return result
      else:
         return node
   
def paint(music, pitches):
   if pitches[0].__class__.__name__ == 'Pitch':
      processedPitches = pitches
   elif pitches[0].__class__.__name__ == 'int':
      processedPitches = [pitch(p) for p in pitches]
   reconstructor = Reconstructor(Painter(copy.deepcopy(processedPitches)))
   if music.__class__.__name__ == 'list':
      return reconstruct(music, reconstructor)
   else:
      return reconstruct([music], reconstructor)[0]

def divide(l, (n, d), together = False):
   '''
   Divide duration (n, d) according to list l.
   Note that denominator d is interpreter as the basic tuplet unit;
   this explains why the function accepts a pair rather than a Rational.

   >>> divide([1], 7, 16)
   (c'4..)

   >>> divide([1, 2], 7, 16)
   (6:7, c'8, c'4)

   >>> divide([1, 2, 4], 7, 16)
   (c'16, c'8, c'4)

   >>> divide([1, 2, 4, 1], 7, 16)
   (8:7, c'16, c'8, c'4, c'16)

   >>> divide([1, 2, 4, 1, 2], 7, 16)
   (10:7, c'16, c'8, c'4, c'16, c'8)

   >>> divide([1, 2, 4, 1, 2, 4], 7, 16)
   (c'32, c'16, c'8, c'32, c'16, c'8)
   '''

   from abjad.exceptions.exceptions import AssignabilityError
   from abjad.tools import construct
   from math import log

   duration = (n, d)

   if len(l) == 0:
      raise ValueError('must divide list l of length > 0.')

   if len(l) == 1:
      if l[0] > 0:
         try:
            return Container([Note(0, duration)])
         except AssignabilityError:
            return Container(construct.notes(0, duration))
      elif l[0] < 0:
         try:
            return Container([Rest(duration)])
         except AssignabilityError:
            return Container(construct.rests(duration))
      else:
         raise ValueError('no divide zero values.')

   if len(l) > 1:
      exponent = mathtools.chop(log(weight(l), 2) - log(n, 2))
      denominator = int(d * 2 ** exponent)
      music = [ ]
      for x in l:
         if not x:
            raise ValueError('no divide zero values.')
         if x > 0:
            try:
               music.append(Note(0, (x, denominator)))
            except AssignabilityError:
               music.extend(construct.notes(0, (x, denominator)))
         else:
            music.append(Rest((-x, denominator)))
      return FixedDurationTuplet(duration, music)
      
def olddivide(l, n, d, together = False):
   '''
   >>> divide([1], 7, 16)
   (c'4..)

   >>> divide([1, 2], 7, 16)
   (6:7, c'8, c'4)

   >>> divide([1, 2, 4], 7, 16)
   (c'16, c'8, c'4)

   >>> divide([1, 2, 4, 1], 7, 16)
   (8:7, c'16, c'8, c'4, c'16)

   >>> divide([1, 2, 4, 1, 2], 7, 16)
   (10:7, c'16, c'8, c'4, c'16, c'8)

   >>> divide([1, 2, 4, 1, 2, 4], 7, 16)
   (c'32, c'16, c'8, c'32, c'16, c'8)
   '''

   # divide([1], 7, 16)
   if len(l) == 1:

      contents = Note(0, n, d) if l[0] > 0 else Rest(n, d)
      result = expression.Expression([contents])

   else:

      r = float(sum([abs(x) for x in l])) / n
      if 0.5 < r < 2.0:
         #print 'normal'
         dn = duration.durationLogToName(math.log(d, 2))
         t = tuplet.SmartTuplet(n, d, music(l + [dn, 'music list']).music)
      elif r <= 0.5:
         #print 'protracted'
         adjustment = int(math.log(r, 2))
         dn = duration.durationLogToName(math.log(d, 2) + adjustment)
         t = tuplet.SmartTuplet(n, d, music(l + [dn, 'music list']).music)
      elif r >= 2.0:
         #print 'contracted'
         #print r
         adjustment = int(math.log(r, 2))
         #print adjustment
         dn = duration.durationLogToName(math.log(d, 2) + adjustment)
         #print dn
         t = tuplet.SmartTuplet(n, d, music(l + [dn, 'music list']).music)
         #print t

      # if cases like 7:14, 14:7, 7:28, 28:7, etc
      if int(math.log(r, 2)) == math.log(r, 2) and \
         t.music[0].__class__.__name__ == 'Tuplet':
         # strip outer music list, return inner music list
         result = t.music[0]
      else:
          result = t

   #if beam != None and hasattr(result, 'beam'):
   #   result.beam(beam)

   if together:
      beam(result, [(n, d)])

   return result

def skeleton(l):
   '''
   Return skeleton of LilyObject, list or tuple.
   '''

   print 'WARNING: skeleton() now deprecated;'
   print 'Use pickle and unpickle instead.'
   print 'Warning on %s.' % l
   print ''

   if hasattr(l, 'skeleton'):
      return l.skeleton
   elif l.__class__.__name__ == 'list':
      return '[%s]' % ', '.join([skeleton(x) for x in l])
   elif l.__class__.__name__ == 'tuple':
      return '(%s)' % ', '.join([skeleton(x) for x in l])
   else:
      print 'Unknown class %s.' % l.__class__.__name__
      raise ValueError

def clean(l):
   return eval(skeleton(l))

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

class TestVisitor(object):
   def __init__(self):
      self.i = 0
   def visit(self, node):
      self.i += 1
      if self.i % 2 == 0:
         return Rest(1, 8)
      else:
         return node

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

class TestSlice(object):
   def __init__(self):
      self.i = -1
   def visit(self, node):
      if node.kind('_Leaf'):
         self.i += 1
         if self.i % 2 == 0:
            try:
               return clone(node, 3)
            except:
               return [node] * 3
         else:
            return [node]
      else:
         return [node]

class TestCompress4(object):
   '''
   >>> l = [1, 1, 2, 1, 2, 1, 2, 1, 1, 1]
   >>> music.traverse(l, music.TestCompress4())
   >>> l
   ['replaced 3', 'replaced 2', 'replaced 2', 1, 1, 1]

   >>> l = [1, [1, 1, 1], 1]
   >>> music.traverse(l, music.TestCompress4())
   >>> l
   [1, [1, 1, 1], 1]

   >>> l = [[1, 2], 1, 1, 1] 
   >>> music.traverse(l, music.TestCompress4())
   >>> l
   [['replaced 2'], 1, 1, 1]

   >>> l = [[1, 1, 2], 1, 2, 1, 1, 2]
   >>> music.traverse(l, music.TestCompress4())
   >>> l
   ['replaced 3', 'replaced 3']

   >>> l = [1, [1, 2], 2, [1, 2], 2, 2, 1, 1, 2]
   >>> music.traverse(l, music.TestCompress4())
   >>> l
   ['replaced 3', 'replaced 2', 'replaced 1', 'replaced 3']
   '''
   def __init__(self):
      self.pairs = []
   def visit(self, node):
      #print 'visit entry', self.pairs
      if isinstance(node, list):
         self.pairs.append([['incomplete', 0]])
      else:
         self.pairs[-1][-1].append(self.pairs[-1][-1][-1] + 1)
         if node == 2:
            self.pairs[-1][-1][0] = 'complete'
            self.pairs[-1].append(['incomplete', self.pairs[-1][-1][-1]])
      #print 'visit exit', self.pairs
      #print ''
   def unvisit(self, node):
      if isinstance(node, list):
         #print 'unvisit entry', self.pairs
         for pair in reversed(self.pairs.pop()):
            #print pair
            if pair[0] == 'complete':
               node[pair[1] : pair[-1]] = ['replaced %s' % (pair[-1] - pair[1])]
         try:
            self.pairs[-1][-1].append(self.pairs[-1][-1][-1] + 1)
         except:
            pass
         #print 'unvisit exit', self.pairs
         #print ''
         
class TestCompress5(object):
   def __init__(self):
      self.pairs = []
      self.justExitedList = False
   def visit(self, node):
      if isinstance(node, list):
         self.pairs.append([[]])
      else:
         #print 'visiting node'
         #print self.pairs

         if self.justExitedList:
            #print 'making new segment'
            self.pairs[-1].append([])
            #print self.pairs

         last = self.pairs[-1][-1]
         if len(self.pairs[-1]) > 1:
            penultimate = self.pairs[-1][-2]
         else:
            penultimate = None
         
         if last == []:
            if penultimate == None:
               last.append(0)
            else:
               if self.justExitedList:
                  last.append(penultimate[-1] + 2)
               else:
                  last.append(penultimate[-1] + 1)
         elif isinstance(last[-1], int):
            last.append(last[-1] + 1)
         elif self.justExitedList:
            last.pop()
            if penultimate == None:
               last.append(last[-1] + 2)
            else:
               last.append(penultimate[-1] + 2)
         else:
            print 'Unknown last %s and penultimate %s.' % (last, penultimate)
            print self.pairs
            raise ValueError

         if node == 2:
            last.insert(0, '.')
            self.pairs[-1].append([])
               
   def unvisit(self, node):
      if isinstance(node, list):
         #print self.pairs
         for pair in reversed(self.pairs[-1]):
            #print pair
            if len(pair) > 1 and pair[0] == '.':
               node[pair[1] : (pair[-1] + 1)] = [
                  'replaced %s' % (pair[-1] - pair[1] + 1)]
         try:
            self.pairs.pop()
         except:
            pass
         self.justExitedList = True
      else:
         self.justExitedList = False

def restsToNotes(expr):
   '''
   Cast rests to notes in expr.

   >>> t = music.divide([1, 1, 1, -2], 4, 16)
   >>> t
   (5:4, c'16, c'16, c'16, r8)

   >>> restsToNotes(t)
   >>> t
   (5:4, c'16, c'16, c'16, c'8)
   '''

   class RestsToNotes(object):
      def visit(self, node):
         if node.kind('Rest'):
            return Note(0, *node.duration.pair)
         else:
            return node

   change(expr, RestsToNotes())
         
#def instances(l, name):
#   class Visitor(object):
#      def __init__(self, name):
#         self.name = name
#         self.result = []
#      def visit(self, node):
#         if hasattr(node, 'kind') and node.kind(name):
#            self.result.append(node)
#   v = Visitor(name)
#   traverse(l, v)
#   return v.result         

def testForParents(expr):
   class Visitor(object):
      def __init__(self):
         self.total = 0
      def visit(self, node):
         if not hasattr(node, 'parent'):
            self.total += 1
            print node.lily
   v = Visitor()
   traverse(expr, v)
   print '%s total nodes incorrectly formatted without parents.' % v.total

def find(ll, *names):
   '''
   >>> ll = [
   ...     voice.Voice([Note(0, 1, 4)], name = 'v1'),
   ...     voice.Voice([Note(2, 1, 4)], name = 'v2')]

   >>> find(ll, 'v1')
   VOICE (1)

   >>> find(ll, 'v1', 'v2')
   [VOICE (1), VOICE (1)]
   '''

   class Visitor(object):
      def __init__(self, names):
         self.names = names
         self.result = []
      def visit(self, node):
         if hasattr(node, 'name') and node.name in self.names:
            self.result.append(node)
   v = Visitor(names)
   traverse(ll, v)
   if len(names) == 1 and len(v.result) > 0:
      return v.result[0]         
   elif len(names) > 1 and len(v.result) > 0:
      return v.result
   else:
      return None

def into(ll, ss, location):
   if hasattr(ll, 'music'):
      for i, l in enumerate(ll.music):
         eval('l.%s.append(ss[i])' % location)
   else:
      for i, l in enumerate(ll):
         eval('l.%s.append(ss[i])' % location)

def build(t):
   """
   >>> music.t1
   [(3, 8), [1]]
   >>> music.build(_)  
   c'4.
   >>> music.t2
   [(3, 8), [1, 2, 4]]
   >>> music.build(_)
   (7:6, c'16, c'8, c'4)
   >>> music.t3
   [(3, 8), [(3, 4), [[1], [1]]]]
   >>> music.build(_)
   (7:6, c'8., c'4)
   >>> music.t4
   [(3, 8), [(3, 4), [[1, 1], [2, 2, 1]]]]
   >>> music.build(_)
   (7:6, (4:3, c'8, c'8), (5:4, c'8, c'8, c'16))
   >>> music.t5
   [(3, 8), [(2, 3), [[1, 1], [(2, 2, 1), [[1], [1], [1, 1]]]]]]
   >>> music.build(_)
   (5:3, (c'8, c'8), (5:3, c'4, c'4, (c'16, c'16)))
   """

   # [(3, 8), [(3, 4), [[1, 1], [2, 2, 1]]]]
   if isinstance(t[1][0], tuple):
      s = sum(t[1][0])
      exponent = int(math.log(s / t[0][0], 2)) if s >= t[0][0] else 0
      denominator = t[0][1] * 2 ** exponent
      #print 'denominator is %s.' % denominator
      w = [[(x[0], x[1]), x[2]] 
         for x in zip(t[1][0], [denominator] * len(t[1][0]), t[1][1])]
      music = [build(token) for token in w]
      l = math.log(max(t[0][0], s) * 1.0 / min(t[0][0], s), 2)
      if l == int(l):
         return expression.Expression(music)
      else:
         return tuplet.SmartTuplet(t[0][0], t[0][1], music)

   # [(3, 8), [1]]
   elif len(t[1]) == 1:
      return Note(0, t[0][0], t[0][1]) if t[1][0] > 0 \
         else Rest(abs(t[0][0]), t[0][1])
   
   # [(3, 8), [1, 2, 4]]
   elif len(t[1]) > 1:
      s = sum([abs(element) for element in t[1]])
      exponent = int(math.log(s / t[0][0], 2)) if s >= t[0][0] else 0
      denominator = t[0][1] * 2 ** exponent
      #print 'denominator is %s.' % denominator
      music = [Note(0, n, denominator) if n > 0 
         else Rest(abs(n), denominator) for n in t[1]]
      l = math.log(max(t[0][0], s) * 1.0 / min(t[0][0], s), 2)
      if l == int(l):
         return expression.Expression(music)
      else:
         return tuplet.SmartTuplet(t[0][0], t[0][1], music)
       
def writtenDurations(m):
   #return clean([l.duration for l in instances(m, '_Leaf')])
   return [l.duration.clone() for l in m.leaves]

def writtenDuration(m):
   return sum(writtenDurations(m), Rational(0))

def effectiveDurations(m):
   '''
   List the effective durations of the leaves in m.

   >>> t = divide([1, 1, 1], 1, 8)

   >>> effectiveDurations(t)
   [DURATION 1/24, DURATION 1/24, DURATION 1/24]

   >>> effectiveDurations(t.leaves) 
   [DURATION 1/24, DURATION 1/24, DURATION 1/24]
   '''
   #return clean([l.effectiveDuration for l in instances(m, '_Leaf')])
   #return [l.effectiveDuration.clone() for l in m.leaves]
   #return [l.effectiveDuration.copy() for l in instances(m, '_Leaf')]
   return [l.duration.prolated for l in instances(m, '_Leaf')]

def effectiveDuration(m):
   '''
   Sum the effective durations of the leaves in m.

   >>> t = divide([1, 1, 1], 1, 8)

   >>> effectiveDuration(t)
   8

   >>> effectiveDuration(t.leaves)
   8
   '''

   if m == [ ]:
      return Rational(0)
   else:
      return sum(effectiveDurations(m), Rational(0))

def fill(l, positions):
   '''
   Fills in 1-indexed measures with c'.
   '''

   result = [ ]

   for i, m in enumerate(l):
      if (i + 1) in positions:
         n, d = m.duration.pair
         l[i] = Measure(
            m.meter.pair,
            [Note(0, (x, d)) for x in untie([n])])

def blank(l, positions):
   '''
   Blanks out 1-indexed measures.
   '''

   result = [ ]

   for i, m in enumerate(l):
      if (i + 1) in positions:
         n, d = m.duration.pair
         l[i] = Measure(
            m.meter.pair,
            [Rest((x, d)) for x in untie([n])])

# TODO combine blank() and cast() into a single function
def cast(m, source = '_Leaf', target = 'Rest', positions = 'all'):
   '''
   Cast instances of class source into class target.

   cast(m, target = 'Rest')
   cast(m, target = 'Skip') 
   '''

   change(m, ClassTransformer(source, target, positions))

class ClassTransformer(object):
   def __init__(self, source = '_Leaf', target = 'Rest', positions = 'all'):
      self.source = source
      self.target = target
      self.positions = positions
      self.i = -1
   def visit(self, node):
      if node.kind(self.source):
         self.i += 1
         if (self.positions == 'all') or (self.i in self.positions):
            if self.target == 'Rest':
               new = Rest(node.duration.n, node.duration.d)
            elif self.target == 'Skip':
               new = skip.Skip(node.duration.n, node.duration.d)
            elif self.target == 'Note':
               new = Note(0, node.duration.n, node.duration.d)
            else:
               print 'Unknown target %s.' % self.target
               raise ValueError
            # round-about way of setting new.effectiveDuration
            new.scaledDuration = Rational(
               node.effectiveDuration.n, node.effectiveDuration.d)
            return new
      return node

def number(music):
   for i, leaf in enumerate(instances(music, '_Leaf')):
      leaf.formatter.right.append(r'_ \markup { %s }' % i)

def unnumber(music):
   pattern = re.compile(r"_ \\markup { [0-9]+ }")
   for leaf in instances(music, '_Leaf'):
      leaf.formatter.right = [
         x for x in leaf.formatter.right
         if not pattern.match(x)]

#def number(l, leaves = False, notes = False, 
#   elements = False, beams = False, measures = False):
#   '''
#   Labels leaves, notes, elements, beams or measures.
#   Measures are 1-indexed; others are 0-indexed.
#   Leaves, notes, elements and measures can each equal False, True or 'markup'.
#   '''   
#
#   vv = instances(l, 'Voice')
#   rv = find(l, 'reference voice') # hack
#   if rv != None:
#      vv.append(rv)
#
#   for v in vv:
#
#      if measures:
#         i = 0
#         for element in v.instances('Measure'):
#            element.label.append('measure %s' % (i + 1))
#            if leaves == 'markup':
#               first = instances([element], '_Leaf')[0]
#               first.right.append(r'^ \markup { %s }' % (i + 1))
#            i += 1
#         
#      if elements: 
#         i = 0
#         for element in v.music:
#            element.label.append('element %s' % i)
#            if elements == 'markup':
#               first = instances([element], '_Leaf')[0]
#               first.right.append(r'^\markup { %s }' % i)
#            i += 1
#         
#      if beams:
#         i = 0
#         open = False
#         for element in v.instances('Note'):
#            if not open:
#               if beams == 'markup':
#                  element.right.append(r'^\markup { %s }' % i)
#               i += 1
#            if '[' in element.right:
#               open = True
#            if ']' in element.right:
#               open = False
#
#      if leaves:
#         i = 0
#         for element in instances(v, '_Leaf'):
#            element.number = i
#            if leaves == 'markup':
#               element._formatter.right.append(
#                  r' _ \markup \with-color #black { %s }' % i)
#            i += 1
#         
#      if notes:
#         i = 0
#         for element in instances(v, 'Note'):
#            element.number = i
#            if notes == 'markup':
#               element._formatter.right.append(
#                  r'^\markup { %s }' % i)
#            i += 1
#         
#   if isinstance(l, list):
#      for i, m in enumerate(instances(l, 'Measure')):
#         m.label.append('measure %s' % (i + 1))

#def unnumber(m):
#   '''
#   Remove numbers, labels and markup.
#   '''
#
#   for element in instances(m, 'LilyObject'):
#      #if hasattr(element, 'label'):
#      #   element.label = []
#      #if hasattr(element, 'number'):
#      #   delattr(element, 'number')
#      element._formatter.right = [
#         x for x in element._formatter.right if x.rfind('markup') == -1]

class TupletBeamer(object):
   '''
   Beams lowest-level tuplets and expressions in place.
   '''

   def __init__(self, style):
      self.current = 0
      self.style = style

   def visit(self, node):
      if hasattr(node, 'kind') and (node.kind('Tuplet') or \
         node.kind('Expression')):
         self.current = id(node)

   def unvisit(self, node):
      if hasattr(node, 'kind') and (node.kind('Tuplet') or \
         node.kind('Expression')):
         if id(node) == self.current:
            node.beam(self.style)

def nest(measures, outer, inner):
   '''
   Structures time.
   '''
   
#  dd = durations([measure.Measure([divide(x[0], *x[1])]) for x in zip(outer, measures)])
#  mm = [divide(x[0], x[1].n, x[1].d) for x in zip(inner, dd)]
#  partition(mm, [len(x) for x in outer])
#  result = [measure.Measure([tuplet.SmartTuplet(x[1][0], x[1][1], x[0])]) for x in zip(mm, measures)]

   inner = partition(inner, [len(x) for x in outer], action = 'new')

   result = []
   
   for i in range(len(measures)):
      m = measures[i]
      o = outer[i]
      n = inner[i]
      dd = writtenDurations([measure.Measure([divide(o, m[0], m[1])])])
      body = []
      for j, d in enumerate(dd):
         if o[j] > 0:
            body.append(divide(n[j], d.n, d.d))
         else:
            body.append(Rest(d.n, d.d))
      
      t = tuplet.SmartTuplet(m[0], m[1], body)
      result.append(measure.Measure([t]))
      
   #into(result, [r'\time %s/%s' % (x[0], x[1]) for x in measures], 'before')
   for i, element in enumerate(result):
      result[i].time = measures[i]
   
   return result

def build(measures, outer):
   """
   Structures time.
   """

   result = []
   for o, m in zip(outer, measures):
      print o
      print m
      print ''
      result.append(measure.Measure([divide(o, m[0], m[1])]))
      result[-1].before.append(r'\time %s/%s' % (m[0], m[1]))

   return result

def trill(l, p = False, indices = 'all', d = Rational(0)):
   """
   Cyclically trills notes at indices with scaled duration >= d.

   When p is set, cyclically applies pitches in p.

   trill(l)
   trill(l, indices = [0, 2])
   trill(l, d = Rational(1, 4)
   trill(l, p = [pitch.Pitch(2)])
   trill(l, indices = [0, 2], p = [pitch.Pitch(2)])

   NOTE: temporarily sets note.trill to True only.
   """

   if indices == 'all':
      indices = range(len(instances(l, '_Leaf')))

   for i, element in enumerate(instances(l, '_Leaf')):
      #if (i - 1) in indices:
      #  element.after.append(r'\stopTrillSpan')
      if hasattr(element, 'scaledDuration'):
         sd = element.scaledDuration
      else:
         sd = element.duration
      if element.kind('Note') and i in indices and sd >= d:
         #if p:
         #  element.before.append(r'\pitchedTrill')
         #  element.after.append(r'\startTrillSpan ' + p[i % len(p)].lily)
         #else:
         #  element.after.append(r'\startTrillSpan')
         element.trill = True

def grace(l, 
   k = '_Leaf', indices = 'all', 
   m = 'Note', dm = (0, 1), check = True,
   s = [[Note(0, (1, 16))]], cyclic = True):
   '''
   '''

   if indices == 'all':
      indices = range(len(instances(l, k)))

   dm = Rational(*dm)

   candidate = 0
   
   for i, element in enumerate(instances(l, k)):

      if hasattr(element, 'scaledDuration'):
         sd = element.scaledDuration
      else:
         sd = element.duration

      if check and hasattr(element, 'grace'):
         ck = False
      else:
         ck = True

      if i in indices and element.kind(m) and sd >= dm and ck:
         new = 0
         if cyclic:
            new = s[candidate % len(s)]
         elif candidate <= len(s) - 1:
            new = s[candidate]
         if new != 0:
            element.grace = clean(new)

         candidate += 1

def color(l, p):
   '''
   TODO: change trills and graces to first-class note attributes.
   '''
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
   for element in instances(l, '_Leaf'):
      if hasattr(element, 'trill'):
         delattr(element, 'trill')

def ungrace(l, keep = 'first', length = 1):
   """
   """

   for element in instances(l, '_Leaf'):
      if hasattr(element, 'grace'):
         if keep == 'first':
            element.grace = element.grace[:length]
         elif keep == 'last':
            element.grace = element.grace[-length:]

def clone(m, n):
   '''
   Clone m n times.

   >>> clone(Note(0, 1, 8), 4)
   [c'8, c'8, c'8, c'8]
   >>> [id(n) for n in _]
   [17387440, 8015952, 8015920, 8016144]
   '''

#   result = []
#
#   for i in range(n):
#      result.append(clean(m))
#
#   return result

   return m * n

def breaks(signatures, durations, pages, verticals, staves = None):
   '''
   '''

   if staves != None:
      staves = ' '.join([str(x) for x in staves])

   result = []

   total = 0
   for p, page in enumerate(pages):
      for l, line in enumerate(page):
         for measure in range(line):
            d = durations[total] 
            s = skip.Skip(
               d.written.numerator, 
               d.written.denominator, 
               d.multiplier.numerator, 
               d.multiplier.denominator)
            tabs = ''.join(['\t'] * int(math.ceil((10 - len(s.body)) / 3.0)))
            result.append(s)
            result[-1].left.append(signatures[total] + '\t')
            result[-1].right = ['%s\\noBreak\t\t' % tabs]
            result[-1].label.append('measure %s' % (total + 1))
            if l == 0 and measure == 0:
               result[-1].before = ['\n%% page %s' % (p + 1)]
            total += 1
         result[-1].right = []
         tabs = ''.join(['\t'] * int(math.ceil((10 - len(s.body)) / 3.0)))
         result[-1].right = ['%s\\break\t\t' % tabs]
         if len(result[-(measure + 1)].before) == 0:
            result[-(measure + 1)].before.append('')
         result[-(measure + 1)].before.append(
            '\overrideProperty #"Score.NonMusicalPaperColumn"')
         if staves == None:
            result[-(measure + 1)].before.append(
               "#'line-break-system-details #'((Y-offset . %s))" % 
               verticals[p][l])
         else:
            result[-(measure + 1)].before.append(
               "#'line-break-system-details #'((Y-offset . %s) (alignment-offsets . (%s)))" % (verticals[p][l], staves))
      result[-1].right = []
      tabs = ''.join(['\t'] * int(math.ceil((10 - len(s.body)) / 3.0)))
      result[-1].right = ['%s\\pageBreak\t' % tabs]

   result = voice.Voice(result, name = 'breaks')
   return result

def sectionalize(m, pairs, kind = '_Leaf'):
   '''
   Add horizontal brackets over elements in pairs.
   Make sure context \consists Horizontal_bracket_engraver.

   >>> sectionalize(snow, [(0, 12), (12, 24), (24, 35), (35, 59)])

   '''

   starts = [p[0] for p in pairs]
   stops  = [p[1] - 1 for p in pairs]

   for i, node in enumerate(m.instances(kind)):
      if i in stops:
         node.right.append (r'\stopGroup')
      if i in starts:
         node.right.append(r'\startGroup')

class Subdivide(object):
   def __init__(self, positions):
      self.positions = positions
      self.position = -1
   def visit(self, node):
      if node.kind('_Leaf'):
         self.position += 1
         n = self.positions[self.position]
         if n > 0:
            denominator = int(2 ** (n + 2))
            quotient = node.duration / Rational(1, denominator)
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
   '''
   Subdivide leaves in m by according to positions.

   >>> subdivide(keys, [0, 0, 1, 1, 2, 0, 0, 1, 2, 2])
   '''
   
   change(m, Subdivide(positions))

class FiveRemover(object):
   '''
   TODO: generalize to TieRemover.
   '''

   def visit(self, node):
      if node.kind('Note') and node.duration.n == 5:
         denominator = node.duration.d
         return expression.Expression(
            [Note(0, 4, denominator), Note(0, 1, denominator)])
      else:
         return node

def unfive(music):
   '''
   TODO: generalize to untie()
   '''

   change(music, FiveRemover())

class BeamBalancer(object):
   def __init__(self):
      self.open = False
      self.last = None
   def visit(self, node):
      if hasattr(node, 'right') and '[' in node.right:
         if self.open:
            self.last.right.remove('[')
         self.open = True
         self.last = node
      if hasattr(node, 'right') and ']' in node.right:
         self.open = False

def equibeam(m):
   '''
   Remove accidentally nested beams in the same voice.
   '''

   traverse(m, BeamBalancer())

def unbeam(m):
   '''
   Call self.unbeam() on leaves in m.
   '''

   for l in instances(m, '_Leaf'):
      try:
         l.unbeam()
      except:
         pass

def decompose(d, parts, r = 'rest'):
   '''
   Decompose duration d into parts with rest or note remainder r.

   Return a list of unbeamed notes.

   >>> decompose((4, 4), [(3, 16)], r = 'rest')
   [c'8., c'8., c'8., c'8., c'8., r16]

   >>> decompose((4, 4), [(3, 16), (4, 16)], r = 'rest')
   [c'8., c'4, c'8., c'4, r8]
   '''

   d = Rational(d[0], d[1])
   p = []
   for part in parts:
      p.append(Rational(part[0], part[1]))
      
   m = []
   i = 0

   while d > Rational(0, 1):
      curPart = p[i % len(p)]
      if curPart <= d:
         m.append(Note(0, curPart.n, curPart.d))
         d -= curPart
      else:
         if r == 'note':
            m.append(Note(0, d.n, d.d))
         elif r == 'rest':
            m.append(Rest(d.n, d.d))
         else:
            raise ValueError
         d = Rational(0, 1)
      i += 1

   return m

def sand(d, p, q):
   '''
   Decompose duration d into parts p according to beam spec q.

   >>> sand((4, 4), [(1, 16), (3, 16)], [(1, 4)])
   [c'16, c'8., c'16, c'8., c'16, c'8., c'16, c'8.]
   >>> f(voice.Voice(_))
   \\new Voice {
           \\beam #0 #2 c'16 [
           \\beam #1 #1 c'8.
           \\beam #1 #2 c'16
           \\beam #1 #1 c'8.
           \\beam #1 #2 c'16
           \\beam #1 #1 c'8.
           \\beam #1 #2 c'16
           \\beam #1 #0 c'8. ]
   }
   '''

   m = decompose(d, p, r = 'rest')
   
   beam(m, q, rip = True, span = True, lone = 'flag') 

   return m

def makeMeasure(d, process, **kwargs):
   '''
   1. comprehension

      >>> makeMeasure(5, 4, 'comprehension')
      <5/4, c'1, c'4>

      >>> makeMeasure(5, 4, 'comprehension', signs = 'change all')
      <5/4, r1, r4>

      >>> makeMeasure(5, 4, 'comprehension', signs = 'change tail')
      <5/4, c'1, r4>

   2. sand

      >>> music.makeMeasure((5, 4), 'sand', p = [(3, 16)], q = [(3, 8)])
      <5/4, c'8., c'8., c'8., c'8., c'8., c'8., r8>
      >>> f(_)
      \\beam #0 #1 c'8. [
      \\beam #1 #1 c'8.
      \\beam #1 #1 c'8.
      \\beam #1 #1 c'8.
      \\beam #1 #1 c'8.
      \\beam #1 #0 c'8. ]
      r8
   '''

   if process == 'comprehension':
      numerators = untie(d[0], **kwargs)
      m = []
      for numerator in numerators:
         if numerator > 0:
            m.append(Note(0, numerator, d[1]))
         else:
            m.append(Rest(-numerator, d[1]))
      return measure.Measure(m, d)

   elif process == 'sand':
      return measure.Measure(sand(d, **kwargs), d)

   else:
      print 'Unknown process %s.' % process
      raise ValueError

def specify(s, t, span = None):
   '''
   Make list of even divisions according to s;
   three-dimensional specification s;
   unit duration with denominator t.

   Wrapper around divide() and beam().

   >>> s = [[[-3, 1, 1], [1, 1, -3]], [[1, 1, -2], [-2, 1, 1]]]
   >>> specify(s, 32, span = 2)
   [(r16., c'32, c'32, c'32, c'32, r16.), (c'32, c'32, r16, r16, c'32, c'32)]

   >>> f(voice.Voice(_))
   \\new Voice {
           r16.
           \\beam #3 #3 c'32 [
           \\beam #3 #2 c'32
           \\beam #2 #3 c'32
           \\beam #3 #3 c'32 ]
           r16.
           \\beam #0 #3 c'32 [
           \\beam #3 #3 c'32 ]
           r16
           r16
           \\beam #3 #3 c'32 [
           \\beam #3 #0 c'32 ]
   }
   '''

   result = []

   for beamfig in s:
      parts = [weight(subbeam) for subbeam in beamfig]
      parts = [(n, t) for n in parts]
      stream = flatten(beamfig, action = 'new')
      new = divide(stream, weight(stream), t)
      beam(new, parts, span = span)
      result.append(new)

   return result

def stellate(k, s, t, d, b, span ='from duration', rests = True):
   '''
   Make running tuplets.

   Numerators k + s;
   denominators k;
   mask t;
   duration 1/d;
   beams b.

   s = [[0]] signals zero-prolation;
   t = [[1]] leaves output unripped.

   TODO: prevent from-duration span from giving incorrect nibs.
   '''

   #from beamtools import beamRunsByDuration
   from complexbeam import ComplexBeam

   if t == [[0]]:
      print 't == [[0]] will cause an infinite loop.'
      raise ValueError

   debug = False

   prolation = helianthate(s, 'right', 'right', action = 'new')
   numerators = listtools.increase_cyclic(k, prolation, action = 'new')
   mask = helianthate(t, 'right', 'right', action = 'new')
   repeat(mask, weight = weight(numerators))
   corrugate(mask)
   signatures = partition(
      mask, numerators, mode = 'weight', overhang = 'true', action = 'new')
   for i, signature in enumerate(signatures):
      if signature == [1]:
         signatures[i] = [-1]
   signatures = untie(signatures)

   if not rests:
      signatures = positivize(signatures)

   denominators = copy.copy(k)
   pairs = zip(signatures, denominators)
   tuplets = [divide(pair[0], (pair[1], d)) for pair in pairs]

   if span == 'from duration':
      span = int(math.log(d, 2)) - 3

   if isinstance(span, int) and span < 1:
      span = None

   partition(tuplets, b, cyclic = True, overhang = True)
   for i, sublist in enumerate(tuplets):
      #if t == [[4, -5, 8], [4, -8], [-4, 6, -6, 8]] and i == 7:
      #   import pdb
      #   pdb.set_trace( )
      if debug:
         #print i, sublist
         sublist[0][0].formatter.right.append(
            r'_ \markup \fontsize #6 { %s }' % i)
      #tmp = Voice(sublist)
      durations = [tuplet.duration.pair for tuplet in sublist]
      #beamRunsByDuration(tmp.leaves, durations, span = span)
      ComplexBeam(sublist, durations, span = span)
      i += 1
   flatten(tuplets)

   return tuplets

def coruscate(n, s, t, z, d, rests = True):
   '''
   Coruscate signal n;
   return list of fixed-duration tuplets.

   Input signal n (2d, passed to helianthate);
   cut s (2d, passed to helianthate);
   fit t (list);
   dilation z (2d, passed to helianthate);
   duration 1/d.

   n = [[1]] gives uniform signal;
   s = [[0]] gives no cut;
   z = [[0]] gives no dilation.

   Length of result equals length of fit.
   Coruscated lines contain no span beams.
   '''

   debug = False
   #from beamtools import beamRunsByDuration
   from complexbeam import ComplexBeam

   # zero-valued signals not allowed
   signal = helianthate(n, 'right', 'right', action = 'new')
   assert all(signal)

   cut = helianthate(s, 'right', 'right', action = 'new')

   dilation = helianthate(z, 'right', 'right', action = 'new')
   fit = listtools.increase_cyclic(t, dilation, action = 'new')

   j = 0
   signatures = []
   for i, element in enumerate(fit):
      new = []
      while weight(new) < element:
         if cut[j % len(cut)] == 0:
            new.append(signal[j % len(signal)])
         elif cut[j % len(cut)] == 1:
            new.append(-signal[j % len(signal)])
         else:
            raise ValueError
         j += 1
      signatures.append(new)
   clump(signatures)
   signatures = untie(signatures)

   if not rests:
      signatures = positivize(signatures)

   if debug: print signatures

   pairs = zip(signatures, t)
   result = [divide(pair[0], (pair[1], d)) for pair in pairs]
   
   for i, element in enumerate(result):
      if debug:
         element.music[0].right.append(r'_ \markup \fontsize #6 { %s }' % i)
      #beam(element)
      #beamRunsByDuration(element, [element.duration.pair])
      ComplexBeam(element, [element.duration.pair])

   return result

#def partitionMusicListByDurations(ml, durations):
#   '''
#   Partition music list ml into sublists equal to durations.
#   '''
#
#   result = []
#
#   cur = 0
#   new = []
#
#   for m in ml:
#      new.append(m)
#      if effectiveDuration(new) >= durations[cur]:
#         result.append(new)
#         cur += 1
#         new = []
#
#   ml[:] = result 

#def openBeam(m, continuation):
#   '''
#   Docs.
#
#   continuation either True or False.
#   '''
#
#   if continuation:
#      open = True
#   else:
#      open = False
#
#   leaves = instances(m, '_Leaf')
#
#   for l in leaves:
#      if l.startBeam and not l.stopBeam:
#         open = True
#      #if l.cleanClosedRight:
#      if l.stopBeam:
#         open = False
#
#   return open
      
#def closeLeftBeamEdge(m):
#   '''
#   Adds [ to first Leaf in m where typographically appropriate.
#   '''
#
#   leaves = instances(m, '_Leaf')
#
#   if len(leaves) == 1:
#      if leaves[0].kind('Note'):
#         leaves[0].unbeam()
#   elif len(leaves) >= 2:
#      if leaves[0].kind('Note'):
#         # 4er then something
#         if leaves[0].duration._flags < 1:
#            leaves[0].unbeam()
#         # 8th then something
#         elif leaves[0].duration._flags == 1:
#            # 8th then rest
#            if not leaves[1].kind('Note'):
#               leaves[0].unbeam()
#            # 8th then nonbeaming note
#            elif leaves[1].duration._flags < 1:
#               leaves[0].unbeam()
#            # 8th then new beam start
#            elif leaves[1].startBeam:
#               leaves[0].unbeam()
#            # 8th then beaming note
#            else:
#               leaves[0].unbeam()
#               leaves[0].right.append(r'[')
#               leaves[0].left.append(r'\beam #0 #1')
#         # 16th then something
#         elif leaves[0].duration._flags > 1:
#            if '[' not in leaves[0].right:
#               leaves[0].right.append('[')
#            leaves[0].removeBeamCounts()
#            f = leaves[0].duration._flags
#            leaves[0].left.append(r'\beam #0 #%s' % f)

#def closeRightBeamEdge(m):
#   '''
#   Adds ] to last Leaf in m where typographically appropriate.
#   '''
#
#   leaves = instances(m, '_Leaf')
#
#   if len(leaves) == 1:
#      if leaves[-1].kind('Note'):
#         leaves[-1].unbeam()
#   elif len(leaves) >= 2:
#      if leaves[-1].kind('Note'):
#         # something then 4er
#         if leaves[-1].duration._flags < 1:
#            leaves[-1].unbeam()
#         # something then 8th
#         elif leaves[-1].duration._flags == 1:
#            # rest then 8th
#            if not leaves[-2].kind('Note'):
#               leaves[-1].unbeam()
#            # nonbeaming note then 8th
#            elif leaves[-2].duration._flags < 1:
#               leaves[-1].unbeam()
#            # beaming note then 8th
#            else:
#               leaves[-1].unbeam()
#               leaves[-1].right.append(r']')
#               leaves[-1].left.append(r'\beam #1 #0')
#         # something then 16th
#         elif leaves[-1].duration._flags > 1:
#            if ']' not in leaves[-1].right:
#               leaves[-1].right.append(']')
#            leaves[-1].removeBeamCounts()
#            f = leaves[-1].duration._flags
#            leaves[-1].left.append(r'\beam #%s #0' % f)

#def partitionBeams(ml, l):
#   '''
#   Partition beams in music list ml according to elements in l;
#   always cyclic overhang.
#   '''
#
#   period = sum(l)
#   positions = [x % period for x in sums(l, action = 'new')]
#
#   result = []
#   new = []
#   total = len(ml)
#   openPrev = False
#   openCur = None
#   
#   for i, m in enumerate(ml):
#      new.append(m)
#
#      if ((i + 1) % period) in positions or i + 1 == total:
#
#         if openPrev:
#            closeLeftBeamEdge(new)
#
#         openCur = openBeam(new, openPrev)
#
#         if openCur:
#            closeRightBeamEdge(new)
#
#         openPrev = openCur
#         openCur = None
#         result.append(new)
#         new = []
#
#   flatten(result)
#   ml[:] = result

#def severBeams(m, start, length):
#   '''
#   For all voices in m, sever length elements from start.
#   '''
#
#   voices = instances(m, 'Voice')
#   for v in voices:
#      s = [start, length, len(v.music) - (start + length)]
#      partitionBeams(v.music, s)

def makeMeasures(m, meters):
   '''
   For each voice in m, 
   press contents into measures 
   according to meters. 
   '''

   durations = [Rational(*meter) for meter in meters]
   voices = instances(m, 'Voice')
   for v in voices:
      assert v.duration == sum(durations, Rational(0))
      d = 0
      measure = Measure(meters[d], [ ])
      for x in v[ : ]:
         measure.append(x)
         if measure.duration >= durations[d]:
            v[d : 2 * d + len(measure) - 1] = [measure]
            d += 1
            if d == len(durations):
               break
            else:
               measure = Measure(meters[d], [ ])

def recombineVoices(target, s, insert, t, loci):
   '''
   Iterate simultaneously through the voices in target and insert;
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
#      flatten(tgtm)

   def P(n, s):
      return partition(
         range(n), s, cyclic = True, overhang = True, action = 'new')

   def makeIndexPairs(n, s):
      return listtools.pairwise(
         sums([0] + [len(part) for part in P(n, s)], action = 'new'))

   targetIndexPairs = makeIndexPairs(len(targetVoices[0]), s)
   insertIndexPairs = makeIndexPairs(len(insertVoices[0]), t)

   #print targetIndexPairs
   #print insertIndexPairs

   if len(insertIndexPairs) < len(loci):
      print 'ERROR: insert partitions into only %s parts;' \
         % len(insertIndexPairs)
      print '       not enough to fill the %s loci specified.' \
         % len(loci)
      print ''

   for targetVoice, insertVoice in zip(targetVoices, insertVoices):
      for j, locus in enumerate(reversed(sorted(loci))):
         first, last = insertIndexPairs[len(loci) - 1 - j]
         insert = copyMusicList(insertVoice, first, last - 1)
         first, last = targetIndexPairs[locus]
         targetVoice[first : last] = insert

def rippleVoices(m, s):
   '''
   Repeat voice elements in m 
   according to s.
   '''

   spec = dict(s)
   voices = instances(m, 'Voice')

   for v in voices:
      for i in reversed(range(len(v))):
         if spec.has_key(i):
            length, reps = spec[i]
            source = v.copy(i, i + length - 1)
            leaves = instances(source, '_Leaf')
            left, right = leaves[0], leaves[-1]
            #left.spanners.fractureLeft( )
            #right.spanners.fractureRight( )
            left.spanners.fracture(direction = 'left')
            right.spanners.fracture(direction = 'right')
            new = [ ]
            for j in range(reps):
               new.extend(copyMusicList(source))
            v[i : i + 1] = new

def copyMusicList(ll, i = None, j = None):
   '''
   Truly smart copy from i up to and including j;
   fracture external and preserve internal spanners;
   return new list.
   '''

   if i is None and j is None:
      source = ll[ : ]
   else:
      source = ll[i : j + 1]
   if source == [ ]:
      print 'WARNING: copyMusicList(ll, %s, %s) gives empty source;' % (i, j)
      print '         len(ll) is %s.' % len(ll)
      print ''
   result = Container(source)
   result = result.copy( )
   result = result[ : ]
   return result

def setLeafStartTimes(expr, offset = Rational(0)):
   '''
   Doc.
   '''
  
   cur = Rational(*offset.pair)
   for l in instances(expr, '_Leaf'):
      l.start = cur
      cur += l.duration.prolated

def rankLeavesTimewise(exprList, name = '_Leaf'):
   '''
   Sets 'timewise' attribute on each of the leaves in the expr in exprList.

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
   '''Get lowest pitch in either Note or Chord;
      else None.'''

   if arg.kind('Note'):
      return arg.pitch.number
   elif arg.kind('Chord'):
      return arg.pitches[0].number
   else:
      #raise ValueError('arg %s must be note or chord.' % str(arg))
      return None

def octavate(n, base = (-4, 30)):
   '''
   Octavate a single note.

   TODO: move to bound Leaf method.
   '''

   if not n.kind('Note'):
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
   '''
   Octavate leaves from start to stop according to base.
   '''
   leaves = voice.leaves
   for l in leaves[start : stop + 1]:
      octavate(l, base)
      
def previous(leaves, cur, name):
   '''
   Doc.
   '''

   j = 1
   while True:
      if leaves[cur - j].kind(name):
         return leaves[cur - j]
      else:
         j += 1

def doubleNote(structure, index, before, right, write = None):
   '''
   Replace sourceNote at structure[index] with simultaneous music; 
   simultaneous music comprises << up down >>;
   both up and down are copies of sourceNote;
   up is an exact deepcopy of sourceNote;
   down reinstantiates sourceNote and extends with any before, right, write.
   '''

   sourceNote = structure[index]
   up = expression.Expression(
      [copy.deepcopy(sourceNote)], enclosure = 'sequential')
   down = Note(sourceNote.pitch.number, *sourceNote.duration.pair)
   down.before.extend(before)
   down.right.extend(right)
   if write:
      down.duration.write(*write)
   down = voice.Voice([down])
   new = expression.Expression([up, down], enclosure = 'simultaneous')
   structure[index : index + 1] = [new]

### DEPRECATED in favor of Octavation( ... ) ###
#def applyOctavation(leaves, start, stop, away, home):
#   leaves[start].before.append(
#      r'#(set-octavation %s)' % away)
#   leaves[stop].after.append(
#      r'#(set-octavation %s)' % home)

def setPitch(l, spec = 0):
   '''
   Sets l.pitch based on l.core.
   '''

   if not l.kind('Note'):
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
            l.caster.toChord( )
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
      l.caster.toChord( )
      l.pitches = [p + transposition for p in pp]

def setPitchIterator(voice, start, stop, spec = 0):
   leaves = voice.leaves
   for l in leaves[start : stop + 1]:
      setPitch(l, spec)

def clonePitches(voice, start, stop, offset):
   leaves = voice.leaves 
   for i, l in enumerate(leaves[start : stop + 1]):
      if l.kind('Note'):
         l.pitch = leaves[start + i + offset].pitch.pair

def setPitchesByPitchCycle(voice, start, stop, pcyc):
   leaves = voice.leaves
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
   '''
   Examines RH leaves;
   splits core RH leaf pitches into one or two chords;
   places higher of (one or) two chords in RH;
   places lower of two chords in LH;
   uses splitHands as helper.
   '''

   for j, l in enumerate(leaves[start : stop + 1]):
      i = start + j
      if l.kind('Note'):
         # upper will always be nonempty
         upper, lower = splitHands(l.core)
         if lower == [ ]:
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
               l.caster.toRest( )
               # NOTE: pass crossLeaves as input parameter
               cl = crossLeaves[i]
               cl.core = upper
               #cl.formatAs('Note')
               cl.caster.toNote( )
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
            cl.caster.toNote( )
            #setPitch(cl, 'core')
            #cl.setPitches(cl.core)
            if len(cl.core) == 1:
               cl.pitch = cl.core[0]
            else:
               raise Exception('cast to chord here.')

def setArticulations(voice, articulations, *args, **kwargs):
   '''
   Iterate leaves and set articulations.
   '''

   leaves = voice.leaves

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
      if l.kind(('Note', 'Chord')) or not exclude:
         if isinstance(articulations, str):
            l.articulations = [articulations]
         elif isinstance(articulations, list):
            l.articulations = articulations
         else:
            raise ValueError

def setArticulationsByPitch(voice, start, stop, articulations, min):
   '''
   Set articulations on notes & chord where safe pitch number is at least min.
   '''

   leaves = voice.leaves
   for l in leaves[start : stop + 1]:
      if l.kind(('Note', 'Chord')) and spget(l) >= min:
         l.articulations = articulations

def setArticulationsByDuration(voice, start, stop, long, min, short):
   '''
   Set long articulations on leaves where effective duration is 
   at least min, else set short articulations.
   '''
   
   leaves = voice.leaves
   min = Rational(*min)
   for l in leaves[start : stop + 1]:
      if l.kind(('Note', 'Chord')):
         if l.duration.prolated >= min:
            l.articulations = long
         else:
            l.articulations = short

def clearAllArticulations(leaves, start = 0, stop = None):
   '''
   Clears articulations from leaves.
   '''

   if isinstance(stop, int):
      stop += 1

   for l in instances(leaves[start : stop], '_Leaf'):
      l.articulations = [ ]

def appendArticulations(voice, articulations, *args, **kwargs):
   '''
   Iterate leaves and append articulations.
   '''

   leaves = voice.leaves
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
      if l.kind(('Note', 'Chord')) or not exclude:
         if isinstance(articulations, str):
            l.articulations.append(articulations)
         elif isinstance(articulations, list):
            for articulation in articulations:
               l.articulations.extend(articulation)
         else:
            raise ValueError

def clear_hairpins(expr):
   '''Clear hairpins from leaves; leave dynamics in place.'''
   for l in instances(expr, '_Leaf'):
      l.dynamics.unspan( )

def clear_dynamics(expr):
   '''Clear both dynamics and hairpins from leaves in expr.'''
   for l in instances(expr, '_Leaf'):
      l.dynamics = None
      l.dynamics.unspan( )

def applyArtificialHarmonic(voice, *args):
   leaves = voice.leaves
   from abjad.tools.harmonics import add_artificial_harmonic
   if len(args) == 2:
      start, diatonicInterval = args
      stop = start
   elif len(args) == 3:
      start, stop, diatonicInterval = args
   else:
      raise ValueError
   for l in leaves[start : stop + 1]:
      if l.kind('Note'):
         add_artificial_harmonic(l, diatonicInterval)


def hpartition_notes_only(leaves, cut = (0,), gap = (0,)):
   '''Note runs only.'''
   cut = Rational(*cut)
   gap = Rational(*gap)
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


def hpartition_rest_terminated(leaves, cut = (0,), gap = (0,)):
   '''Rest-terminated note runs.'''
   cut = Rational(*cut)
   gap = Rational(*gap)
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


def partitionLeaves(leaves, type = 'notes and rests', cut = (0,), gap = (0,)):
   '''
   Partition leaf list leaves into sublists;
   chunking suitable for repeated hairpin application.

   >>> t = divide([1, 1, -1, -1, 1, 1, -1, -1, -1], 8, 16)
   >>> t
   (9:8, c'16, c'16, r16, r16, c'16, c'16, r16, r16, r16)

   >>> partitionLeaves(t.leaves) 
   [[c'16, c'16], [r16, r16], [c'16, c'16], [r16, r16, r16]]

   >>> partitionLeaves(t.leaves, type = 'notes only')
   [[c'16, c'16], [c'16, c'16]]

   >>> partitionLeaves(t.leaves, type = 'rests only')
   [[r16, r16], [r16, r16, r16]]

   >>> partitionLeaves(t.leaves, type = 'rest-terminated')
   [[c'16, c'16, r16], [c'16, c'16, r16]]

   >>> music.partitionLeaves(t.leaves, type = 'rest-gapped')
   [([c'16, c'16, r16],), ([c'16, c'16, r16],)]

   >>> music.partitionLeaves(t.leaves, type = 'rest-gapped', gap = (2, 18))
   [([c'16, c'16, r16], [c'16, c'16, r16])]

   >>> partitionLeaves(t.leaves, type = 'paired notes')           
   [([c'16, c'16],), ([c'16, c'16],)]

   >>> partitionLeaves(t.leaves, type = 'paired notes', gap = (2, 18))
   [([c'16, c'16], [c'16, c'16])]

   >>> t = divide([1, -1, 1, -3, 1, -1, -1, 1], 10, 16)
   >>> t
   (c'16, r16, c'16, r8., c'16, r16, r16, c'16)

   >>> partitionLeaves(t.leaves, type = 'cut notes', cut = (1, 16))
   [[c'16, r16, c'16], [c'16], [c'16]]

   >>> partitionLeaves(t.leaves, type = 'cut paired notes', cut = (1, 16), gap = (2, 16))
   [([c'16, r16, c'16],), ([c'16], [c'16])]

   >>> partitionLeaves(t.leaves, type = 'cut paired notes', cut = (1, 16), gap = (3, 16))
   [([c'16, r16, c'16], [c'16]), ([c'16],)]
      '''

   cut = Rational(*cut)
   gap = Rational(*gap)
   result = [[]]
   
   if type == 'notes and rests':
      for l in leaves:
         lastChunk = result[-1]
         if len(lastChunk) == 0:
            lastChunk.append(l)
         else:
            lastLeaf = lastChunk[-1]
            if lastLeaf.kind('Note') == l.kind('Note'):
               lastChunk.append(l)
            else:
               result.append([l])

   elif type == 'notes only':
      for l in leaves:
         lastChunk = result[-1]
         if l.kind('Note'):
            lastChunk.append(l)
         else:
            if len(lastChunk) > 0:
               result.append([])
      if result[-1] == []:
         result.pop()

   elif type == 'cut notes':
      firstResult = partitionLeaves(leaves, type = 'notes and rests')
      if not firstResult[0][0].kind('Note'):
         firstResult.pop(0)
      result = [firstResult.pop(0)]
      for chunk in firstResult:
         lastChunk = result[-1]
         if chunk[0].kind('Note'):
            # empty
            if len(lastChunk) == 0:
               lastChunk.extend(chunk)
            # note-terminated
            elif lastChunk[-1].kind('Note'):
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
      if not firstResult[0][0].kind('Note'):
         firstResult.pop(0)
      result = [[[]]]
      for chunk in firstResult:
         lastPair = result[-1]
         lastChunk = lastPair[-1]
         if chunk[0].kind('Note'):
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
         if not m.kind('Note'):
            lastChunk.pop(-1)
         else:
            break
      for i, sublist in enumerate(result):
         result[i] = tuple(sublist)

   elif type == 'rests only':
      for l in leaves:
         lastChunk = result[-1]
         if l.kind('Rest'):
            lastChunk.append(l)
         else:
            if len(lastChunk) > 0:
               result.append([])
      if result[-1] == []:
         result.pop()

   elif type == 'rest-terminated':
      for l in leaves:
         lastChunk = result[-1]
         if l.kind('Note'):
            if len(lastChunk) == 0:
               lastChunk.append(l)
            else:
               lastLeaf = lastChunk[-1]
               if lastLeaf.kind('Note'):
                  lastChunk.append(l)
               else:
                  result.append([l])
         elif l.kind('Rest'):
            if len(lastChunk) > 0:
               lastLeaf = lastChunk[-1]
               if lastLeaf.kind('Note'):
                  lastChunk.append(l)

   # the gap input parameter is the duration of rest run to bridge over;
   # accepting gap = (0,) makes rest-gapped return like rest-terminated
   elif type == 'rest-gapped':
      firstResult = partitionLeaves(leaves, type = 'notes and rests')
      if not firstResult[0][0].kind('Note'):
         firstResult.pop(0)
      result = [[firstResult.pop(0)]]
      bridged = False
      bridgeNext = False
      for chunk in firstResult:
         if not chunk[0].kind('Note'):
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
      if not firstResult[0][0].kind('Note'):
         firstResult.pop(0)
      result = [[firstResult.pop(0)]]
      bridged = False
      bridgeNext = False
      for chunk in firstResult:
         if not chunk[0].kind('Note'):
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

def segmentLeaves(leaves, cut = (0,), gap = (0,)):
   '''
   Partition leaves into segments each of one or more stages;
   include rests of duration less than or equal to cut in each stage;
   rests of duration greater than or equal to gap begin new stages.

   >>> t = divide([1, -1, 1, -2, 1, -1, 1, -3, 1, -1, 1], 14, 16)
   >>> t
   (c'16, r16, c'16, r8, c'16, r16, c'16, r8., c'16, r16, c'16)

   >>> segmentLeaves(t.leaves)
   [([c'16],), ([c'16],), ([c'16],), ([c'16],), ([c'16],), ([c'16],)]

   >>> segmentLeaves(t.leaves, (1, 16))
   [([c'16, r16, c'16],), ([c'16, r16, c'16],), ([c'16, r16, c'16],)]

   >>> segmentLeaves(t.leaves, (2, 16))
   [([c'16, r16, c'16, r8, c'16, r16, c'16],), ([c'16, r16, c'16],)]

   >>> segmentLeaves(t.leaves, (3, 16))
   [([c'16, r16, c'16, r8, c'16, r16, c'16, r8., c'16, r16, c'16],)]

   >>> segmentLeaves(t.leaves, (1, 16), (3, 16))
   [([c'16, r16, c'16], [c'16, r16, c'16]), ([c'16, r16, c'16],)]
   '''
   cut = Rational(*cut)
   gap = Rational(*gap)
   parts = partitionLeaves(leaves)
   if not parts[0][0].kind('Note'):
      parts.pop(0)
   segments = [[[]]]
   for part in parts:
      segment = segments[-1]
      stage = segment[-1]
      if part[0].kind('Note'):
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
      if l.kind('Rest'):
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
   leaves = voice.leaves
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




def makeBreaksVoice(durationPairs, yOffsets, alignmentOffsets, start = 0):
   '''
   Return page- and line-breaking skip voice;
   start at system start to allow first page title.

   >>> makeBreaksVoice([(10, 8), (10, 8), (9, 8)], [20, 120], [0, -36, -48], 1)
   VOICE (3)
   >>> f(_)

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
   breaks = [ ]
   for p in durationPairs:
      try:
         skip = Skip(p)
      except ValueError:
         skip = Skip((1, 1))
         skip.duration.multiplier = p
      breaks.append(skip)
   for i, b in enumerate(breaks):
      cyclicPosition = (start + i) % len(yOffsets)
      curYOffset = yOffsets[cyclicPosition]
      if cyclicPosition == len(yOffsets) - 1:
         curBreak = r'\pageBreak'
      else:
         curBreak = r'\break'
      b.formatter.before.extend([
         r'\overrideProperty #"Score.NonMusicalPaperColumn" ',
         "#'line-break-system-details",
         "#'((Y-offset . %s)" % curYOffset,
         '(alignment-offsets . (%s)))' % alignmentOffsets])
      b.formatter.right.extend([r'\bar ""', curBreak])
   voice = Voice(breaks)
   voice.name = 'breaks voice'
   return voice

def makeMeasuresVoice(durationPairs):
   '''
   Return measure and time signature skip voice.

   >>> makeMeasuresVoice([(10, 8), (10, 8), (9, 8)])
   VOICE (3)
   >>> f(_)

   % measures voice
   \\new Voice {
           \\time 10/8 s1 * 5/4
           \\time 10/8 s1 * 5/4
           \\time 9/8 s1 * 9/8
   }
   '''

   measures = [ ]
   for pair in durationPairs:
      skip = Skip((1, 1))
      skip.duration.multiplier = pair
      measure = Measure(pair, [skip])
      measures.append(measure)
   voice = Voice(measures)
   voice.name = 'measures voice'
   return voice

def reddenSections(measuresVoice, sectionTuples, startMeasure = 1):
   '''
   Redden section bars and label sections in red.

   >>> measuresVoice = makeMeasuresVoice([(10, 8), (10, 8), (9, 8)])
   >>> reddenSections(measuresVoice, [(1, 1, 2, 'I'), (2, 3, 3, 'II')])
   >>> f(measuresVoice)

   % measures voice
   \\new Voice {
           \\once \\override Score.BarLine #'color = #red
           \\once \\override Score.SpanBar #'color = #red
           \\time 10/8 s1 * 5/4 ^ \\markup 
               \\fontsize #2 \\with-color #red \\italic { 1. I }
           \\time 10/8 s1 * 5/4
           \\once \\override Score.BarLine #'color = #red
           \\once \\override Score.SpanBar #'color = #red
           \\time 9/8 s1 * 9/8 ^ \\markup 
               \\fontsize #2 \\with-color #red \\italic { 2. II }
   }
   '''

   barText = r"\once \override Score.BarLine #'color = #red"
   spanBarText = r"\once \override Score.SpanBar #'color = #red"
   measureSkips = measuresVoice.skips

   for n, start, stop, description in sectionTuples:
      if start >= startMeasure:
         sectionText = r'^ \markup \fontsize #2 \with-color #red \italic '
         sectionText += '{ %s. %s }' % (n, description)
         try:
            ms = measureSkips[start - startMeasure]
            ms.before.extend([barText, spanBarText])
            ms.right.append(sectionText)
         except:
            pass

def trimVoices(expr, nMeasures):
   '''
   Find each voice in expr and trim to n measures;
   useful for rendering only the first n measures of a score;
   accommodates attack, nucleus, release and reference contexts.
   '''

   customVoiceContexts = [
      'attack voice', 'nucleus voice', 'release voice', 'reference voice']
   voices = instances(expr, 'Voice') + find(expr, *customVoiceContexts)
   for v in voices:
      v.music = v.music[:nMeasures]

def makeFluteGroup(*staves):
   '''
   Group staves together with 'Flute' id and 'flute group' name.
   '''

   return container.Container(list(staves), 
      id = 'Flute', name = 'flute group')

def makeViolinGroup(*staves):
   '''
   Group staves together with 'Violin' id and 'violin group' name.
   '''

   return container.Container(list(staves), 
      id = 'Violin', name = 'violin group')

def crossStavesDown(voice, start, stop, bp, target,
   includes = [], excludes = [], 
   topBeamPositions = None, bottomBeamPositions = None):
   '''
   target is a reference to an actual Staff instance.

   TODO: run octavate at some time other than cross-determination time.
   '''
   
   leaves = voice.leaves
   for j, l in enumerate(leaves[start : stop + 1]):
      i = start + j
      if l.kind('Note'):
         #if (l.safePitchNumber >= bp or i in includes) and i not in excludes:
         if (spget(l) >= bp or i in includes) and i not in excludes:
            l.staff = target
         else:
            octavate(l, base = (-4, 30))

def crossStavesUp(leaves, start, stop, bp, target):
   '''
   target is a reference to an actual Staff instance.

   TODO: run octavate at some time other than cross-determination time.
   '''

   for i, l in enumerate(leaves[start : stop + 1]):
      if l.note:
         if l.pitch.number > bp:
            l.staff = target
         else:
            octavate(l, base = (-28, 4))

# TODO: merge cauterizeSpanners into cauterize
def cauterizeSpanners(leaves, start, stop, name):
   exec('leaves[start].%s.fractureAllLeft( )' % name)
   exec('leaves[stop].next.%s.fractureAllLeft( )' % name)
   
def cauterize(leaves, start, stop):
   for receptor in leaves[0].getReceptors( ):
      exec('leaves[start].%s.fractureAllLeft( )' % 
         receptor.grob)
   if leaves[-1].next:
      for receptor in leaves[-1].next.getReceptors( ):
         exec('leaves[stop].next.%s.fractureAllLeft( )' % 
            receptor.grob)

def partitionLeavesByDurations(leaves, durations = None):
   '''
   >>> v = Voice([divide([1, -4, 1], (1, 4)), divide([1, -4, 1, 1], (1, 4))])
   >>> v.leaves
   [c'16, r4, c'16, c'16, r4, c'16, c'16]

   >>> partitionLeavesByDurations(v.leaves, [(1, 4)])
   [[c'16, r4, c'16], [c'16, r4, c'16, c'16]]

   >>> partitionLeavesByDurations(v.leaves, [(1, 2)])
   [[c'16, r4, c'16, c'16, r4, c'16, c'16]]

   >>> v = Voice(Note(0, (1, 32)) * 8)
   >>> v.leaves
   [c'32, c'32, c'32, c'32, c'32, c'32, c'32, c'32]

   >>> partitionLeavesByDurations(v.leaves, [(1, 32), (3, 32)])
   [[c'32], [c'32, c'32, c'32], [c'32], [c'32, c'32, c'32]]

   >>> partitionLeavesByDurations(v.leaves, [(3, 32)])
   [[c'32, c'32, c'32], [c'32, c'32, c'32], [c'32, c'32]]
   '''

   if not durations:
      return leaves

   result = [[ ]]

   j = 0
   for l in leaves:
      total = effectiveDuration(result[-1])
      next = Rational(*durations[j % len(durations)])
      #if total + l.effectiveDuration < next:
      if total + l.duration.prolated < next:
         result[-1].append(l)
      #elif total + l.effectiveDuration == next:
      elif total + l.duration.prolated == next:
         result[-1].append(l)
         result.append([ ])
         j += 1
      #elif total + l.effectiveDuration > next:
      elif total + l.duration.prolated > next:
         print 'WARNING: part greater than duration.'
         result[-1].append(l)
         result.append([ ])
         j += 1

   if result[-1] == [ ]:
      result.pop( )

   return result
