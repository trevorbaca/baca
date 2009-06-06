## TODO: Break out 'sheet' case into separate function. ##

def segment(l, s, cycle = 'knife'):
   '''Segment l into sublists of weights not less than s.

   >>> l = [1] * 10
   >>> utilities.segment(l, 2)
   [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1]]

   >>> l = [1] * 10
   >>> utilities.segment(l, [2, 3])
   [[1, 1], [1, 1, 1], [1, 1], [1, 1, 1]]

   >>> l = [1] * 10
   >>> utilities.segment(l, [2, 3], cycle = False)
   [[1, 1], [1, 1, 1]]

   >>> l = [1]
   >>> utilities.segment(l, [2, 3, 2, 3], cycle = 'sheet')
   >>> l
   [[1, 1], [1, 1, 1], [1, 1], [1, 1, 1]]'''

   assert isinstance(l, list)
   assert isinstance(s, list)
   assert all([isinstance(x, int) for x in s])

   result = [ ]

   if cycle == False:
      j = 0
      k = 0
      while True:
         try:
            element = s[k]
            new = []
            while sum([abs(x) for x in new]) < element:
               try:
                  new.extend(eval(l[j]))
               except:
                  new.append(l[j])
               j += 1
               if j >= len(l):
                  raise IndexError
            result.append(new)
            k += 1
         except IndexError:
            break

   elif cycle == 'knife':
      k = 0
      new = []
      for element in l:
         try:
            new.extend(eval(element))
         except:
            new.append(element)
         if sum([abs(x) for x in new]) >= s[k]:
            result.append(new)
            new = []
            k = (k + 1) % len(s)

   elif cycle == 'sheet':
      j = 0
      for element in s:
         new = []
         while sum([abs(x) for x in new]) < element:
            try:
               new.extend(eval(l[j % len(l)]))
            except:
               new.append(l[j % len(l)])
            j += 1
         result.append(new)

   else:
      print 'Unknown value %s for cycle.' % cycle
      raise ValueError

   return result
