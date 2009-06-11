'''List tools used in Cary, Sekka and Lidercfeny.'''

from abjad.leaf.leaf import _Leaf
from abjad.note.note import Note
from abjad.rational.rational import Rational
from abjad.tools import clone
from abjad.tools import listtools
from abjad.tools import mathtools
from abjad.tools import pitchtools
import copy
import math
import sys


def caulk(l, s, action = 'in place'):
   '''
   Transforms sublists-with-negatives to sublists-with-positives;
   'caulks' sublists in l according to elements in s.

   >>> l = [[-1, 1, 1], [1, -1, 1], [1, 1, -1]]
   >>> caulk(l, [-1, -1, -1])
   >>> l
   [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

   >>> l = [[-1, 1, 1], [1, -1, 1], [1, 1, -1]]
   >>> caulk(l, [-1, 1, 1])
   >>> l
   [[1, 1, 1], [1, -1, 1], [1, 1, -1]]

   >>> l = [[-1, 1, 1], [1, -1, 1], [1, 1, -1]]
   >>> caulk(l, [1, 1, 1])
   >>> l
   [[-1, 1, 1], [1, -1, 1], [1, 1, -1]]
   '''

   result = []

   i = 0

   for sublist in l:

      # if the sublist is all positive, like [1, 1, 1, 1, 1]
      if len([x for x in sublist if x < 0]) == 0:
         result.append(sublist)

      # elif the sublist is like [1, 1, -3] and contains a negative sublist
      elif len([x for x in sublist if x < 0]) > 0:

         # check the directives list ...
         # if the current directive == 1, keep the sublist
         if s[i % len(s)] == 1:
            result.append(sublist)

         # but if the current directive == -1, remove all rests from the sublist
         elif s[i % len(s)] == -1:
            result.append([abs(x) for x in sublist])

         # increment ONLY when we've just processed a sublist-with-negatives
         i += 1
   
   if action == 'in place':
      l[:] = result
   else:
      return result


def within(i, indices):
   '''
   Returns True if i in indices token, and False otherwise.

   >>> within(7, [0, 1, 2, 3, 4])
   False

   >>> within(7, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
   True

   >>> within(7, ([0, 1, 2, 3, 4], 5))
   True

   >>> within(7, ([0, 1, 2, 3, 4], 10))
   False
   '''

   if isinstance(indices, tuple):
      return i % indices[-1] in indices[0]
   else:
      return i in indices  


def pick(i, token):
   '''
   Picks element i from material in token.

   >>> material = [2, 3, 7, 5]
   >>> pick(0, material)
   2

   >>> pick(10, material)

   >>> pick(0, (material, 4))
   2

   >>> pick(10, (material, 4))
   7
   '''

   if isinstance(token, tuple):
      material = token[0]
      period = token[-1]
      try:
         return material[i % period]
      except:
         return None
   else:
      material = token
      try:
         return material[i]
      except:
         return None


def replace(l, indices, material, action = 'in place'):
   '''
   Replace elements at indices in l with material.

   >>> l = range(20)
   >>> replace(l, ([0], 2), (['A', 'B'], 3))
   >>> l
   ['A', 1, 'B', 3, 4, 5, 'A', 7, 'B', 9, 10, 11, 'A', 13, 'B', 15, 16, 17, 'A', 19]

   >>> l = range(20)
   >>> replace(l, ([0], 2), (['*'], 1))
   >>> l
   ['*', 1, '*', 3, '*', 5, '*', 7, '*', 9, '*', 11, '*', 13, '*', 15, '*', 17, '*', 19]

   >>> l = range(20)
   >>> replace(l, ([0], 2), ['A', 'B', 'C', 'D'])
   >>> l
   ['A', 1, 'B', 3, 'C', 5, 'D', 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

   >>> l = range(20)
   >>> replace(l, [0, 1, 8, 13], ['A', 'B', 'C', 'D'])
   >>> l
   ['A', 'B', 2, 3, 4, 5, 6, 7, 'C', 9, 10, 11, 12, 'D', 14, 15, 16, 17, 18, 19]
   '''

   result = []
   j = 0

   for i, element in enumerate(l):
      if within(i, indices):
         if pick(j, material):
            result.append(pick(j, material))
         else:
            result.append(element)
         j += 1
      else:
         result.append(element)

   if action == 'in place':
      l[:] = result
   else:
      return result  


def intize(w, action = 'in place'):
   '''
   Map 1.0, 2.0, 3.0, ... to 1, 2, 3, ....

   Leave noninteger floats unchanged.

   >>> w = [[1.0, 2, 4], [2, 4.0], [2, 4.0, 4.0, 4.5]]
   >>> intize(w)
   >>> w
   [[1, 2, 4], [2, 4], [2, 4, 4, 4.5]]
   '''

   result = []

   if isinstance(w[0], list):
      for sublist in w:
         result.append(intize(sublist, action = 'new'))
   else:
      for element in w:
         if isinstance(element, float) and element - int(element) == 0:
            result.append(int(element))
         else:
            result.append(element)

   if action == 'in place':
      w[:] = result
   else:
      return result


def corrugate(w, target = 'positives', action = 'in place'):
   '''
   Replace positive integers with 1-sequences;
   flat or nested w.

   >>> l = [1, 2, 2, -4]
   >>> corrugate(l, action = 'new')
   [1, 1, 1, 1, 1, -4]

   >>> corrugate(l, target = 'negatives', action = 'new')
   [1, 2, 2, -1, -1, -1, -1]

   >>> corrugate(l, target = 'all', action = 'new')
   [1, 1, 1, 1, 1, -1, -1, -1, -1]

   >>> w = [[1, 3, -4], [1, 2, -2, -4]]
   >>> corrugate(w)
   >>> w
   [[1, 1, 1, 1, -4], [1, 1, 1, -2, -4]]
   '''

   result = []

   # two-dimensional w
   if isinstance(w[0], list):
      for sublist in w:
         result.append(corrugate(sublist, target = target, action = 'new')) 
   # one-dimensional w
   else:
      for element in reversed(w):
         if target == 'positives':
            if element < 0:
               result.insert(0, element)
            else:
               result[0:0] = [1] * element 
         elif target == 'negatives':
            if element > 0:
               result.insert(0, element)
            else:
               result[0:0] = [-1] * abs(element)
         elif target == 'all':
            if element == 0:
               result.insert(0, element)
            else:
               result[0:0] = [mathtools.sign(element) * 1] * abs(element)
         else:
            print 'Unkown target %s.' % target
            raise ValueError
      
   if action == 'in place':
      w[:] = result
   elif action == 'new':
      return result


def emboss(l, s, p, action = 'in place'):
   '''   
   Corrugate elements of l;
   strikethrough according to s;
   group according to p.

   Examples.
   '''

   result = []

   result = listtools.repeat_to_weight(s, sum(l))
   result = listtools.partition_by_weights(result, l, overhang = True)
   corrugate(result)
   part_lengths = [len(part) for part in p]
   result = listtools.partition_by_counts(result, part_lengths)

   if action == 'in place':
      l[:] = result
   elif action == 'new':
      return result


def recombine(target, s, insert, t, loci):
   '''
   Partition target list cyclically according to s;
   partition insert list cyclically according to t;
   overwrite parts of target with parts of insert 
   at positions in loci.

   >>> target = range(12)
   >>> insert = [9] * 10
   >>> loci = [0, 3, 5]
   >>> recombine(target, 2, insert, [2, 2, 6], loci)
   [9, 9, 2, 3, 4, 5, 9, 9, 8, 9, 9, 9, 9, 9, 9, 9]
   '''

   a = listtools.partition_by_counts(
      target, [s], cyclic = True, overhang = True)
   b = listtools.partition_by_counts(
      insert, [t], cyclic = True, overhang = True)
   replace(a, loci, b)
   
   result = [ ]
   for sublist in a:
      result.extend(sublist)

   return result


def read(l, start, length):
   '''
   >>> l = [1, 1, 2, 3, 5, 5, 6]
   >>> read(l, 4, 18)
   [5, 5, 6, 1, 1, 2, 3, 5, 5, 6, 1, 1, 2, 3, 5, 5, 6, 1]
   '''

   result = []
   m = len(l)

   for i in range(start, start + length):
      result.append(l[i % m])

   return result


def positivize(w):
   '''Turn all negative numbers positive.
      Leave nonpositive numbers unchanged.

      >>> w = [[-1, -1, 2, 3, -5], [1, 2, 5, -5, -6]]
      >>> positivize(w)
      [[1, 1, 2, 3, 5], [1, 2, 5, 5, 6]]'''

   result = [ ]

   if isinstance(w[0], list):
      for sublist in w:
         result.append(positivize(sublist))
   else:
      for x in w:
         if x < 0:
            result.append(-x)
         else:
            result.append(x)

   return result


def smelt(ll):
   '''Return positive subsequences in the absolute cumulative sums of ll.

      >>> ll = [1, -1, -2, 1, -2, -1, -2, 2, 1, -3, -1, 2, -2, -1, -1]
      >>> smelt(ll)
      [[1], [5], [11, 12, 13], [18, 19]]'''

   result = list(listtools.sum_by_sign(ll))
   first  = result[0]

   result = piles(result)
   result = [0] + result
   result = [1 + n for n in result]
   result = listtools.pairwise(result)

   new = [ ]
   if mathtools.sign(first) == 1:
      for i, pair in enumerate(result):
         if i % 2 == 0:
            new.append(pair)
   else:
      for i, pair in enumerate(result):
         if i % 2 == 1:
            new.append(pair)

   result = [range(*pair) for pair in new]
      
   return result
