from abjad import *


def beamRunsByDuration(
   m, b = None, rip = True, span = False, nib = False, lone = True):
   '''
   >>> decompose((2, 4), [(1, 16)])
   [c'16, c'16, c'16, c'16, c'16, c'16, c'16, c'16]
   >>> m = _
   >>> beamRunsByDuration(m, [(1, 8)])
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

   >>> beamRunsByDuration(m, [(1, 8), (3, 16)])
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

   >>> m = [divide([1, -4, 1], 1, 4), divide([1, -4, 1, 1], 1, 4)]
   >>> beamRunsByDuration(m, [(1, 4), (1, 4)], span = 1)
   >>> f(voice.Voice(m))
   \\new Voice {
           \\times 2/3 {
                   \\beam #0 #2 c'16 [ ]
                   r4
                   \\beam #2 #1 c'16 [
           }
           \\times 4/7 {
                   \\beam #1 #2 c'16 ]
                   r4
                   \\beam #2 #2 c'16 [
                   \\beam #2 #0 c'16 ]
           }
   }
   '''

   from music import instances, partitionLeavesByDurations

#   print m
#   print b
#   print rip
#   print span
#   print nib
#   print lone
#   print ''

   #import pdb
   #pdb.set_trace( )

   runs = partitionLeavesByDurations(instances(m, '_Leaf'), b)
   for run in runs:
      applyBeamSpanners(run, lone) # ok
      setBeamCountsForRun(run, rip = rip, lone = lone) # bad
      # this helper doesn't generate nibs-pointing-towards-rests

   if span:
      for run in runs:
         run[-1].beam.bridge(span, 'right')


def partitionLeavesByBeamability(leaves):
   '''
   >>> t = divide([1, 1, 2, 1, 1, -1, -1], 7, 8)
   >>> t
   (8:7, c'8, c'8, c'4, c'8, c'8, r8, r8)

   >>> partitionLeavesByBeamability(t.leaves)
   [[c'8, c'8], [c'4], [c'8, c'8], [r8, r8]]
   '''

   result = [[leaves[0]]]
   for l in leaves[1: ]:
      if l.beam.beamable == result[-1][-1].beam.beamable:
         result[-1].append(l)
      else:
         result.append([l])
   return result


def applyBeamSpanners(leaves, lone = True):
   '''
   >>> t = divide([1, 1, 2, 1, 1, -1, -1], 7, 8)
   >>> applyBeamSpanners(t.leaves)
   \\fraction \\times 7/8 {
           c'8 [
           c'8 ]
           c'4
           c'8 [
           c'8 ]
           r8
           r8
   }
   '''

   if len(leaves) == 1:
      if lone and leaves[0].beam.beamable:
         #Beam(leaves, None, None)
         Beam(leaves[ : ])
   else:
      for part in partitionLeavesByBeamability(leaves):
         if part[0].beam.beamable:
            if lone:
               Beam(part[ : ])
            else:
               if len(part) > 1:
                  Beam(part[ : ])


def setBeamCountsForRun(leaves, rip = True, lone = True):
   if len(leaves) == 1:
      if leaves[0].beam.beamable and lone:
         leaves[0].beam.counts = None
   else:
      _setBeamCountsForFirstLeafInRun(leaves[0], rip)
      for l in leaves[1 : -1]:
         _setBeamCountsForMiddleLeafInRun(l, rip)
      _setBeamCountsForLastLeafInRun(leaves[-1], rip)


def _setBeamCountsForFirstLeafInRun(l, rip = True):
   if l.beam.spanned:
      if l.beam.only:
         if rip:
            l.beam.counts = 0, l.beam._flags
      else:
         l.beam.counts = 0, l.beam._flags


def _setBeamCountsForMiddleLeafInRun(l, rip = True):
   if l.beam.spanned:
      if l.beam.only:
         if rip:
            l.beam.counts = l.beam._flags, l.beam._flags
      elif l.beam.first:
         l.beam.counts = 0, l.beam._flags
      elif l.beam.last:
         l.beam.counts = l.beam._flags, 0
      else:
         if l.prev:
            prev = l.prev.beam._flags
         else:
            prev = 0
         if l.next:
            next = l.next.beam._flags
         else:
            next = 0
         #print l, prev, l.beam._flags, next,
         left = min(l.beam._flags, prev)
         right = min(l.beam._flags, next)
         if l.beam._flags == left or l.beam._flags == right:
            l.beam.counts = left, right
         else:
            l.beam.counts = l.beam._flags, right
         #print l.beam.counts
          

def _setBeamCountsForLastLeafInRun(l, rip = True):
   if l.beam.spanned:
      if l.beam.only:
         if rip:
            l.beam.counts = l.beam._flags, 0
      elif l.beam.last:
         l.beam.counts = l.beam._flags, 0


### TODO - port instances( ) into ajbad and uncomment ###
### TODO - write regtests ###
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


def unbeam_lone_eighths(expr):
   for leaf in expr.leaves:
      if hasattr(leaf, 'beam'):
         if leaf.beam.only and leaf.beam._flags == 1:
            leaf.beam.spanners[0].die( ) 
