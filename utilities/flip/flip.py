import math


def flip(l, s, action = 'in place'):
   '''
   Flip elements in sublists of w according to directives cyclically in s.

   >>> l = [[-1, -1, -1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, -1, -1, 1, 1], [1, 1]]
   >>> flip(l, [0])
   >>> l
   [[-1, -1, -1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, -1, -1, 1, 1], [1, 1]]

   >>> l = [[-1, -1, -1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, -1, -1, 1, 1], [1, 1]]
   >>> flip(l, [-1])
   >>> l
   [[1, 1, 1, 1, 1], [-1, -1, -1, -1, -1, 1, 1, 1, 1], [-1, 1, 1, 1, 1], [-1, 1]]

   >>> l = [[-1, -1, -1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, -1, -1, 1, 1], [1, 1]]
   >>> flip(l, [1]) 
   >>> l
   [[-1, -1, 1, -1, -1], [1, 1, 1, 1, -1, -1, -1, -1, -1], [1, -1, 1, -1, -1], [1, -1]]

   >>> l = [[-1, -1, -1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, -1, -1, 1, 1], [1, 1]]
   >>> flip(l, ['C'])
   >>> l
   [[-1, 1, 1, 1, 1], [1, 1, -1, -1, -1, -1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1]]
   '''

   result = []

   for i, element in enumerate(l):
      if s[i % len(s)] == 0:
         result.append(element)
      elif s[i % len(s)] == -1:
         result.append(_flip_helper(element, 'left+1', 1, 2))
      elif s[i % len(s)] == 1:
         result.append(_flip_helper(element, 'right+1', 1, 2))
      elif s[i % len(s)] == 'C':
         result.append(_flip_helper(element, 'center-left', 1, 2))
      else:
         print 'Unknown flip directive.'
         raise Exception

   if action == 'in place':
      l[:] = result
   else:
      return result


def _flip_helper(l, part, n, d):
   '''
   >>> _flip_helper([1, 2, 3, 4, 5, 6, 7, 8], 'left', 1, 4)
   [-1, -2, 3, 4, 5, 6, 7, 8]
   >>> _flip_helper([1, 2, 3, 4, 5, 6, 7, 8], 'right', 1, 4)
   [1, 2, 3, 4, 5, 6, -7, -8]
   >>> _flip_helper([1, 2, 3, 4, 5, 6, 7, 8], 'sides', 1, 4)
   [-1, -2, 3, 4, 5, 6, -7, -8]
   >>> _flip_helper([1, 2, 3, 4, 5, 6, 7, 8], 'center-left', 1, 4)
   [1, 2, 3, -4, -5, 6, 7, 8]
   '''

   amt = int(float(n) / float(d) * len(l))
   if amt < 1:
      amt = 1

   #print 'amt is ' + str(amt)
         
   if part == 'left':
      ind = [i for i in range(amt) if i != len(l) - 1]
      for i in ind:
         l[i] *= -1
   elif part == 'left+1':
      if amt < len(l):
         amt += 1
      ind = [i for i in range(amt) if i != len(l) - 1]
      for i in ind:
         l[i] *= -1
   elif part == 'right':
      ind = [len(l) - (i + 1) for i in range(amt)]
      ind = [i for i in ind if i != 0]
      for i in ind:
         l[i] *= -1
   elif part == 'right+1':
      if amt < len(l):
         amt += 1
      ind = [len(l) - (i + 1) for i in range(amt)]
      ind = [i for i in ind if i != 0]
      for i in ind:
         l[i] *= -1
   elif part == 'sides':
      ind = range(amt)
      for i in [len(l) - (x + 1) for x in range(amt)]:
         if i not in ind:
            ind.append(i)
      centerIndex = int(math.ceil(len(l) / 2.)) - 1
      ind = [i for i in ind if i != centerIndex]
      for i in ind:
         l[i] *= -1
   elif part == 'center-left':
      centerIndex = int(math.ceil(len(l) / 2.)) - 1
      ind = [centerIndex]
      i = 1
      while len(ind) < amt:
         if len(l) % 2 == 1:
            try:
               if (centerIndex - i) not in ind:
                  ind.append(centerIndex - i)
            except:
               pass
            try:
               if (centerIndex + i) not in ind:
                  ind.append(centerIndex + i)
            except:
               pass
         else:
            try:
               if (centerIndex + i) not in ind:
                  ind.append(centerIndex + i)
            except:
               pass
            try:
               if (centerIndex - i) not in ind:
                  ind.append(centerIndex - i)
            except:
               pass
         i += 1
      ind = ind[:amt]
      ind = [i for i in ind if i not in [0, len(l)]]
      for i in ind:
         l[i] *= -1
   else:
      print 'Unknown flip spec.'
      raise ValueError
            
   return l    
