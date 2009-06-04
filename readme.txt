Functions migrated from baca/utilities.py to Abjad:


   utilities.snip(l, weight, i) 
   ==> 
   listtools.remove_weighted_subrun_at(l, weight, i)


   utilities.partition(l, s, mode = 'length', overhang = False, cyclic = False)
   ==>
   listtools.partition_by_counts(l, counts, overhang = False, cyclic = False)
   listtools.partition_by_weights(l, counts, overhang = False, cyclic = False)


   utilities.chunk(ll, s)
   ==>
   listtools.partition_by_weights(l, s, overhang = overhang, cyclic = cyclic)
