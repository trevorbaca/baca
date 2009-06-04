Functions migrated from baca/utilities.py to Abjad:


   utilities.chunk(ll, s)
   ==>
   listtools.partition_by_weights(l, s, overhang = overhang, cyclic = cyclic)


   utilities.partition(l, s, mode = 'length', overhang = False, cyclic = False)
   ==>
   listtools.partition_by_counts(l, counts, overhang = False, cyclic = False)
   listtools.partition_by_weights(l, counts, overhang = False, cyclic = False)


   utilities.snip(l, weight, i) 
   ==> 
   listtools.remove_weighted_subrun_at(l, weight, i)


   utilities.spot(l, s, positions, action = 'in place')
   ==>
   listtools.increase_at_indices(l, addenda, indices)
