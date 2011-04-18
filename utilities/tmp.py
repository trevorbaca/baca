import math

def tmp(m, n):
   r'''Do something with m mod n.

      for x in range(15):
         print x, 7, '\t', baca.utilities.tmp(x, 7), 7

      0 7   4 7
      1 7   5 7
      2 7   6 7
      3 7   7 7
      4 7   4 7
      5 7   5 7
      6 7   6 7
      7 7   7 7
      8 7   8 7
      9 7   9 7
      10 7  10 7
      11 7  11 7
      12 7  12 7
      13 7  13 7
      14 7  7 7
   '''

   if n <= m:
      return m % n + n
   else:
      return n - ((n - m) % int(math.ceil(n / 2.0)))
