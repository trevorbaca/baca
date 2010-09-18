def resegment(w, s, max = False, overhang = True):
   '''Resegment two-dimensional list w into sublists 
   of weights not less than s.

   Use on measure division lists for overlapping beams.

   >>> w = [[10], [10, 10, 10], [1], [3], [4], [5], [1], [2], [10, 10]]

   >>> utilities.resegment(w, [10])
   [[10], [10], [10], [10], [1, 3, 4, 5], [1, 2, 10], [10]]

   >>> utilities.resegment(w, [10, 15])
   [[10], [10, 10], [10], [1, 3, 4, 5, 1, 2], [10], [10]]

   >>> utilities.resegment(w, [15])
   [[10, 10], [10, 10], [1, 3, 4, 5, 1, 2], [10, 10]]

   Use max to limit sublist maximum length.

   >>> utilities.resegment(w, [15], max = 3)
   [[10, 10], [10, 10], [1, 3], [4, 5, 1], [2, 10, 10]]

   ### TODO - max doesn't work completely correctly yet;
   ###        try setting max = 1 and notice that there
   ###        will be sublists greater than 1;
   ###        change this, but only after porting Lidercfeny.
   '''

   result = [ ]

   i = 0
   cur = s[i % len(s)]
   new = [ ]
   visitedSublists = 0

   for sublist in w:
      for element in sublist:
         new.append(element)
         if sum(new) >= cur:
            result.append(new)
            i += 1
            cur = s[i % len(s)]
            new = [ ]
            visitedSublists = 0
      visitedSublists += 1
      if max and visitedSublists >= max:
         result.append(new)
         i += 1
         cur = s[i % len(s)]
         new = [ ]
         visitedSublists = 0
   if overhang and len(new) > 0:
      result.append(new)

   if result[-1] == [ ]:
      result.pop( )

   return result


