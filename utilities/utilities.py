'''Tools (primarily list tools) used in Cary, Sekka and Lidercfeny.'''

from abjad.tools import listtools
import types


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
