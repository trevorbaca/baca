'''Tools (primarily list tools) used in Cary, Sekka and Lidercfeny.'''

from abjad.tools import listtools
from abjad.tools import mathtools
import types


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


## TODO: Read partitioned insert cyclically? ##

def recombine(target, s, insert, t, loci):
   '''
   Partition target list cyclically according to s;
   partition insert list cyclically according to t;
   overwrite parts of target with parts of insert 
   at positions in loci.

   abjad> target = range(12)
   abjad> insert = [9] * 10
   abjad> loci = [0, 3, 5]
   abjad> recombine(target, 2, insert, [2, 2, 6], loci)
   [9, 9, 2, 3, 4, 5, 9, 9, 8, 9, 9, 9, 9, 9, 9, 9]
   '''

   ## TODO: assert isinstance(loci, pair) and len(loci) == 2 ##
   ## TODO: loci_values, loci_period = loci
   ## TODO: assert isinstance(loci_values, list)
   ## TODO: assert isinstance(loci_period, (int, long, types.NoneType))

   a = listtools.partition_by_counts(
      target, [s], cyclic = True, overhang = True)
   b = listtools.partition_by_counts(
      insert, [t], cyclic = True, overhang = True)
   #a = replace(a, loci, b)
   a = replace(a, (loci, None), (b, len(b)))
   
   #result = [ ]
   #for sublist in a:
   #   result.extend(sublist)

   result = listtools.flatten(a)

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
