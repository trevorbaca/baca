'''Tools (primarily list tools) used in Cary, Sekka and Lidercfeny.'''

from abjad.tools import listtools
from abjad.tools import mathtools
from baca.utilities.replace_nested_elements_with_unary_subruns import \
   replace_nested_elements_with_unary_subruns as \
   utilities_replace_nested_elements_with_unary_subruns
import types


def emboss(l, s, p, action = 'in place'):
   '''   
   Corrugate elements of l.
   Strikethrough according to s.
   Group according to p.
   '''

   result = []

   result = listtools.repeat_to_weight(s, sum(l))
   result = listtools.partition_by_weights(result, l, overhang = True)
   result = utilities.replace_nested_elements_with_unary_subruns(result)
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
