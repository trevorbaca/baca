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


   utilities.clump(w, action = 'in place')
   ==>
   [list(listtools.sum_by_sign(x, sign = [-1])) for x in w]


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


   utilities.flip(l, s, action = 'in place')
   ==>
   cary.transforms.flip_sublist_element_signs(l, s)


   utilities.glom(l)
   ==>
   utilities.clump(l)


   utilities.lump(w, action = 'in place')
   ==>
   [list(listtools.sum_by_sign(x, sign = [1])) for x in w]


   utilities.mapInto(M, n)
   ==>
   pitchtools.send_pitch_number_to_octave(pitch_number, mapping)


   utilities.negate(l, s, action = 'in place')
   ==>
   cary.transforms.negate_one_element_sublists_cyclic(l, specification)


   utilities.ones(l, action = 'in place')
   ==>
   use [[1] * x for x in l] instead
   
   
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


   utilities.pick( )
   ==>
   use %


   utilities.picket(l, ins, overhang = (0, 0))
   ==>
   listtools.insert_slice_cyclic(l, s, overhang = (0, 0))

   
   utilities.piles(ll)
   ==> 
   unused: cumulative sums of absolute values of elements in ll.


   utilities.pleat(l, n)
   ==>
   listtools.repeat_elements_to_length(l, n)


   utilities.plough(w, s, cur = 0, action = 'in place')
   ==>
   s = period_s
   s = listtools.true_indices(s)
   w_part_counts = [len(x) for x in w]
   w = listtools.flatten(w)
   w = listtools.negate_elements_at_indices(w, s, period = period_s)
   w = listtools.partition_by_counts(w, w_part_counts)
   

   utilities.project(l, spec, history = False)
   ==>
   pitchtools.insert_transposed_pc_subruns(notes, subrun_indicators, history = False)


   utilities.replace(l, indices, material)
   ==>
   listtools.overwrite_elements_at(l, indices, material)


   utilities.ripple(l, [(anchor, (length, total_appearances)), ...])
   ie, utilities.ripple(l, [(i, (length, n), ...])
   ==>
   listtools.repeat_subruns_cyclic(l, [(achor, length, new_appearances), ...])
   ie, listtools.repeat_subruns_cyclic(l, [(i, length, n - 1), ...])


   utilities.rout(l, s, cur = 0, recurse = False)
   ==>
   period_s = len(s)
   s_true_indices = listtools.true_indices(s)
   listtools.negate_elements_at_indices_absolutely(l, s_true_indices, period_s)


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


   utilities.untie(expr, signs = 'all positive')
   ==>
   utilities.partition_nested_into_canonic_parts(expr, direction = 'big-endian')


   utilities.within( )
   ==>
   use %
