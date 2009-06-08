Functions migrated from baca/utilities.py to Abjad:


   utilities.bunch(l, s, cycle = True)
   ==>
   listtools.group_by_weights(l, s, fill = 'exact', cyclic = False, overhang = False)


   utilities.chunk(ll, s)
   ==>
   listtools.partition_by_weights(l, s, overhang = overhang, cyclic = cyclic)


   utilities.circumrotate(l, inner, outer)
   ==>
   utilities.rotate_nested(l, inner, outer)


   utilities.convolve(l, s, action = 'in place')
   ==>
   utilities.increase_sublist_end_elements(l, s) 

   
   utilities.cycle(outer, inner, l, flattened = True)
   ==>
   utilities.helianthate(l, outer, inner, flattened = True)


   utilities.draw(l, s, history = False)
   ==>
   music.repeat_subruns_cyclic(notes, subrun_indicators, history = False)


   utilities.flamingo(l, s, period = None)
   ==>
   listtools.negate_elements_at_indices(l, indices, period = None)


   utilities.mapInto(M, n)
   ==>
   pitchtools.send_pitch_number_to_octave(pitch_number, mapping)


   utilities.partition(l, s, mode = 'length', overhang = False, cyclic = False)
   ==>
   listtools.partition_by_counts(l, counts, overhang = False, cyclic = False)
   listtools.partition_by_weights(l, counts, overhang = False, cyclic = False)

   
   utilities.permIter(seq)
   ==>
   listtools.permtutations(l)

   
   utilities.permute(l, s, action = 'in place')
   ==>
   pitchtools.permute_by_row(pitches, row)


   utilities.picket(l, ins, overhang = (0, 0))
   ==>
   listtools.insert_slice_cyclic(l, s, overhang = (0, 0))


   utilities.project(l, spec, history = False)
   ==>
   pitchtools.insert_transposed_pc_subruns(notes, subrun_indicators, history = False)


   utilities.scan(l)
   ==>
   for i, leaf in enumerate(l)
   next, prev, = leaf.next, leaf.prev 


   utilities.smear(l, s)
   ==>
   listtools.overwrite_slices_at(l, pairs)


   utilities.snip(l, weight, i) 
   ==> 
   listtools.remove_weighted_subrun_at(l, weight, i)


   utilities.spot(l, s, positions, action = 'in place')
   ==>
   listtools.increase_at_indices(l, addenda, indices)

