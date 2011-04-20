def increase_sublist_end_elements(l, s):
   '''Add elements in s to the first and last elements of
   corresponding sublists in l.
   That is: 

      l[0][0] += s[0-1] and l[0][-1] += s[0+1]
      l[1][0] += s[1-1] and l[1][-1] += s[1+1]
      l[2][0] += s[2-1] and l[2][-1] += s[2+1]
      l[3][0] += s[3-1] and l[3][-1] += s[3+1]
      ...
      l[n][0] += s[n-1] and l[n][-1] += s[n+1]

   Note that only the end elements of the sublists of l change.
   Any middle elements in the sublists of l are left untouched.

   abjad> l = [[2, 2, 2], [2, 2], [2, 2, 2]]     
   abjad> util.increase_sublist_end_elements(l, [1, 5, 10])
   [[12, 2, 7], [3, 12], [7, 2, 3]]

   Note too that there is special handling of 1-element sublists in l:
   ie, 1-element sublists are left untouched.'''

   assert len(l) == len(s)
   assert isinstance(l, list)
   assert all([isinstance(x, list) for x in l])
   assert isinstance(s, list)

   result = [ ]

   len_s = len(s)
   for i, sublist in enumerate(l):
      if 1 < len(sublist):
         left_neighbor = s[(i - 1) % len_s]
         right_neighbor = s[(i + 1) % len_s] 
         sublist[0] += left_neighbor
         sublist[-1] += right_neighbor
      result.append(sublist)
  
   return result
