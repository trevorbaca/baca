'''List tools used in Cary, Sekka and Lidercfeny.'''

from abjad.leaf.leaf import _Leaf
from abjad.note.note import Note
from abjad.rational.rational import Rational
from abjad.tools import clone
from abjad.tools import listtools
from abjad.tools import mathtools
from abjad.tools import pitchtools
import copy
import math
import sys


def segment(l, s, cycle = 'knife', action = 'in place'):
   '''
   Segment l into sublists of weights not less than s.

   >>> l = [1] * 10
   >>> segment(l, 2)
   >>> l
   [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1]]

   >>> l = [1] * 10
   >>> segment(l, [2, 3])
   >>> l
   [[1, 1], [1, 1, 1], [1, 1], [1, 1, 1]]

   >>> l = [1] * 10
   >>> segment(l, [2, 3], cycle = False)
   >>> l
   [[1, 1], [1, 1, 1]]

   >>> l = [1]
   >>> segment(l, [2, 3, 2, 3]) 
   >>> l
   [[1]]

   >>> l = [1]
   >>> segment(l, [2, 3, 2, 3], cycle = 'sheet')
   >>> l
   [[1, 1], [1, 1, 1], [1, 1], [1, 1, 1]]

   >>> l = [1] * 10
   >>> segment(l, [2, 3], action = 'new')
   [[1, 1], [1, 1, 1], [1, 1], [1, 1, 1]]
   >>> l
   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

   >>> segment(['(1, 1, 1)', 1, 2, -2, 3, '(1, 1, 1)', -2, 4], 8, action = 'new')
   [[1, 1, 1, 1, 2, -2], [3, 1, 1, 1, -2], [4]]
   '''

   if isinstance(s, int):
      s = [s]

   result = []

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

   if action == 'in place':
      l[:] = result
   else:
      return result


def bunch(l, s, cycle = True, action = 'in place'):
   '''
   Segment l into sublists of weights not greater than s.

   >>> l = [3] * 15
   >>> utilities.bunch(l, [8, 10], action = 'new')
   [[3, 3, 3], [3, 3], [3, 3, 3], [3, 3], [3, 3, 3], [3, 3]]

   >>> utilities.bunch(l, [8, 10], action = 'new', cycle = False)
   [[3, 3, 3], [3, 3]]
   '''

   result = [[]]

   curWeight = -1

   for element in l:
      if sum(result[-1]) + element > s[curWeight % len(s)]:
         curWeight += 1
         if not cycle and curWeight == len(s) - 1:
            break
         else:
            result.append([element])
      else:
         result[-1].append(element)

   if action == 'in place':
      l[:] = result
   else:
      return result


def circumrotate(l, outer, inner):
   '''
   >>> l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   >>> circumrotate('right', 'right', l)
   [[8, 6, 7], [3, 1, 2], [5, 4]]

   >>> circumrotate('right', 'left', l)
   [[7, 8, 6], [2, 3, 1], [5, 4]]

   >>> circumrotate('left', 'right', l)
   [[5, 4], [8, 6, 7], [3, 1, 2]]

   >>> circumrotate('left', 'left', l)
   [[5, 4], [7, 8, 6], [2, 3, 1]]
   '''

   if outer == 'right':
      if inner == 'right':
         return listtools.rotate(
            [listtools.rotate(x, 'right', action = 'new') for x in l], 
            'right', action = 'new')
      elif inner == 'left':
         return listtools.rotate(
            [listtools.rotate(x, 'left', action = 'new') for x in l], 
            'right', action = 'new')
   elif outer == 'left':
      if inner == 'right':
         return listtools.rotate(
            [listtools.rotate(x, 'right', action = 'new') for x in l], 
            'left', action = 'new')
      elif inner == 'left':
         return listtools.rotate(
            [listtools.rotate(x, 'left', action = 'new') for x in l], 
            'left', action = 'new')
   else:
      print 'Unknown direction %s.' % outer
      raise ValueError


def cycle(outer, inner, l, flattened = True):
   '''
   cycle('right', 'right', [[4, 5, 5], [5, 6], [3, 4, 5]])
   '''

   result = [copy.deepcopy(l)]
   while True:
      next = circumrotate(result[-1], outer, inner)
      if next == result[0]:
         if flattened == True:
            result = listtools.flatten(result)
            return result
         else:
            return result
      else:
         result.append(next)


def helianthate(l, outer, inner, action = 'in place', flattened = True):
   '''
   >>> l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   >>> helianthate(l, 'left', 'right')                   
   >>> l[:24]
   [1, 2, 3, 4, 5, 6, 7, 8, 5, 4, 8, 6, 7, 3, 1, 2, 7, 8, 6, 2, 3, 1, 4, 5]

   >>> l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   >>> helianthate(l, 'left', 'right', flattened = False)
   >>> l[:9]
   [[1, 2, 3], [4, 5], [6, 7, 8], [5, 4], [8, 6, 7], [3, 1, 2], [7, 8, 6], [2, 3, 1], [4, 5]]

   >>> l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   >>> helianthate(l, 'left', 'right', action = 'new')[:24]
   [1, 2, 3, 4, 5, 6, 7, 8, 5, 4, 8, 6, 7, 3, 1, 2, 7, 8, 6, 2, 3, 1, 4, 5]

   >>> l = [note.Note(n, 1, 4) for n in range(1, 9)]
   >>> l = listtools.partition_by_counts(l, [3, 2, 3])
   >>> helianthate(l, 'left', 'right')  
   >>> l[:24]
   >>> l[:18]
   [cs'4, d'4, ef'4, e'4, f'4, fs'4, g'4, af'4, f'4, e'4, af'4, fs'4, g'4, ef'4, cs'4, d'4, g'4, af'4]
   '''

   if isinstance(l[0][0], _Leaf):
      start = [[n.pitch.pc for n in sublist] for sublist in l]
      result = [ ]
      for sublist in l:
         result.append([clone.unspan(element) for element in sublist])
   else:
      start = l[:]
      result = l[:]

   while True:
      last = result[-len(start):]

      if isinstance(last[0][0], int) or isinstance(last[0][0], str) or \
         isinstance(last[0][0], float) or isinstance(last[0][0], tuple):
         input = last
      else:
         input = []
         for sublist in last:
            new = []
            print sublist
            for n in sublist:
               new.append(clone.unspan(n))
            input.append(new)
               
      next = circumrotate(input, outer, inner)

      if next == start or (isinstance(next[0][0], Note) and \
         [[n.pitch.pc for n in sublist] for sublist in next] == start):
         if flattened == True:
            result = listtools.flatten(result)
         break
      else:
         result.extend(next)

   if action == 'in place':
      l[:] = result
   else:
      return result


def draw(l, pairs, history = False):
   '''In-line repetition, in-place.

      Defined on both notes and arbitrary elements.

      >>> l = [note.Note(n, 1, 4) for n in [0, 2, 4, 5, 7, 9, 11]]
      >>> draw(l, [(0, 4), (2, 4)])
      >>> l
      [c'4, d'4, e'4, f'4, c'4, d'4, e'4, f'4, g'4, a'4, e'4, f'4, g'4, a'4, b'4]
                           ^    ^    ^    ^              ^    ^    ^    ^

      >>> l = range(7)
      >>> draw(l, [(0, 4), (2, 4)])
      >>> l
      [0, 1, 2, 3, 0, 1, 2, 3, 4, 5, 2, 3, 4, 5, 6]
                   ^  ^  ^  ^        ^  ^  ^  ^     '''

   inserts = [ ]

   if isinstance(l[0], Note):
      for pair in reversed(pairs):
         new = [ ]
         for i in range(pair[0], pair[0] + pair[1]):
            source = l[i % len(l)]
            #newest = source.__class__(
            #   source.pitch.number, source.duration.n, source.duration.d)
            newest = Note(source.pitch.number, source.duration.written)
#            if isinstance(history, basestring):
#               newest.history = source.history + history if \
#                  hasattr(source, 'history') else history
            if isinstance(history, str):
               newest.history['tag'] = source.history.get('tag', history)
            new.append(newest)
         if len(pair) == 2:
            reps = 1
         else:
            reps = pair[-1]
         inserts.append((pair[0] + pair[1], new, reps))

   if isinstance(l[0], int):
      for pair in reversed(pairs):
         new = []
         for i in range(pair[0], pair[0] + pair[1]):
            new.append(l[i % len(l)])
         if len(pair) == 2:
            reps = 1
         else:
            reps = pair[-1]
         inserts.append(((pair[0] + pair[1]) % len(l), new, reps))

   for insert in reversed(sorted(inserts)):
      l[insert[0]:insert[0]] = clone.unspan(insert[1], reps)


def project(l, spec, history = False):
   '''
   Interval project, in-place.

   Defined on both notes and integer pcs.

   >>> l = [Note(n, (1, 4)) for n in [0, 2, 7, 9, 5, 11, 4]]
   >>> project(l, [(0, [2, 4]), (4, [3, 1])])
   >>> l
   [c'4, f'4, g'4, d'4, e'4, c'4, fs'4, b'4, g'4, a'4, f'4, bf'4, fs'4, af'4, b'4, g'4, e'4]
         ^    ^         ^    ^    ^     ^                   ^     ^     ^          ^

   >>> l = [0, 2, 7, 9, 5, 11, 4]
   >>> project(l, [(0, [2, 4]), (4, [3, 1])])
   >>> l
   [0, 5, 7, 2, 4, 0, 6, 11, 7, 9, 5, 10, 6, 8, 11, 7, 4]
       ^  ^     ^  ^  ^  ^            ^   ^  ^      ^
   '''

   inserts = [ ]

   if isinstance(l[0], Note):
      # for (0, [2, 4])
      for token in spec:
         # pairs are [(0, 2), (1, 4)]
         for pair in [
            (token[0] + i, token[1][i]) for i in range(len(token[1]))]:
            anchor = l[pair[0] % len(l)]
            #anchor = anchor.__class__(
            #   anchor.pitch.number, anchor.duration.n, anchor.duration.d)
            anchor = clone.unspan([anchor])[0]
            if hasattr(l[pair[0] % len(l)], 'history'):
               #anchor.history = l[pair[0] % len(l)].history
               anchor.history['tag'] = l[pair[0] % len(l)].history['tag']
            new = [anchor]
            for index in range(pair[0] + 1, pair[0] + pair[-1] + 1):
               stop = l[(index + 1) % len(l)]
               start = l[index % len(l)]
               interval = stop.pitch.pc - start.pitch.pc
               source = new[-1]
               
               #newest = source.__class__(
               #   (source.pitch.pc + interval) % 12, 
               #   source.duration.n, source.duration.d)

               new_pitch = (source.pitch.pc + interval) % 12
               newest = Note(new_pitch, source.duration.written)

               #if isinstance(history, basestring):
               #   newest.history = anchor.history + history if \
               #      hasattr(anchor, 'history') else history
               if isinstance(history, str):
                  newest.history['tag'] = anchor.history['tag'] + history if \
                     anchor.history.has_key('tag') else history
               new.append(newest)
            inserts.append((pair[0], new))

   elif isinstance(l[0], int):
      # for (0, [2, 4])
      for token in spec:
         # pairs are [(0, 2), (1, 4)]
         for pair in [
            (token[0] + i, token[1][i]) for i in range(len(token[1]))]:
            anchor = l[pair[0] % len(l)]
            new = [anchor]
            for index in range(pair[0] + 1, pair[0] + pair[-1] + 1):
               stop = l[(index + 1) % len(l)]
               start = l[index % len(l)]
               interval = stop - start
               new.append((new[-1] + interval) % 12)
            inserts.append((pair[0], new))

   for insert in reversed(sorted(inserts)):
      l[insert[0] : insert[0] + 1] = insert[-1]
      

def piles(ll):
   '''
   Return the cumulative sums of the absolute values of the l in ll.

   >>> l = [1, -1, -2, 3, -5, -5, 6]
   >>> piles(l)
   [1, 2, 4, 7, 12, 17, 23]
   '''

   result = [abs(ll[0])]

   for l in ll[1 : ]:
      result.append(result[-1] + abs(l))

   return result


def smear(l, s):
   '''
   Repeatedly overwrite elements in l according to s.

   >>> l = range(10)
   >>> smear(l, [(0, 3), (5, 3)])
   >>> l
   [0, 0, 0, 3, 4, 5, 5, 5, 8, 9]
   '''

   cp = copy.deepcopy(l)

   for pair in s:
      for i in range(pair[0], pair[0] + pair[1]):
         l[i] = cp[pair[0]]


def ripple(l, s):
   '''
   Repeat elements in l according to s.

   >>> l = [1, 1, 2, 3, 5, 5, 6]
   >>> ripple(l, [(2, [2, 3]), (6, [1, 4])])
   [1, 1, 2, 3, 2, 3, 2, 3, 5, 5, 6, 6, 6, 6]
   '''

   spec = dict(s)
   result = l[:]

   for i in reversed(range(len(result))):
      try:
         length = spec[i][0]
         reps = spec[i][1]
      except:
         length = 1
         reps = 1
      cur = l[i : i + length]
      new = []
      for j in range(reps):
         new.extend(cur)
      result[i : i + length] = new
   
   return result
   

def plough(w, s, cur = 0, action = 'in place'):
   '''
   Cyclically negate elements in w according to s.

   >>> l = [1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
   >>> plough(l, [0, 0, 0, 1, 1])
   >>> l
   [1, 2, 3, -5, -5, 1, 2, 5, -5, -6]

   >>> w = [[1, 2, 2], [1, 2, 3, 5, 5], [1, 2, 5, 5, 6]]
   >>> plough(w, [0, 0, 0, 1, 1])
   >>> w
   [[1, 2, 2], [-1, -2, 3, 5, 5], [-1, -2, 5, 5, 6]]
   '''
   
   result = []

   if isinstance(w[0], list):
      for sublist in w:
         cur, new = plough(sublist, s, cur, action = 'recurse')
         result.append(new)
   else:
      for element in w:
         if s[cur % len(s)] == 1:
            result.append(-element)
         else:
            result.append(element)
         cur += 1

   if action == 'in place':
      w[:] = result
   elif action == 'new':
      return result
   elif action == 'recurse':
      return cur, result


def rout(w, s, cur = 0, recurse = False):
   '''
   Cyclically turn elements in w absolutely negative according to s;
   
   stronger form of plough().

   >>> l = [1, 1, 2, 3, 5, 5, 6]
   >>> rout(l, [0, 1, 1])
   [1, -1, -2, 3, -5, -5, 6]

   >>> rout(_, [1])
   [-1, -1, -2, -3, -5, -5, -6]
   '''
   
   result = []

   if isinstance(w[0], list):
      for sublist in w:
         cur, new = rout(sublist, s, cur, recurse = True)
         result.append(new)
   else:
      for element in w:
         if s[cur % len(s)] == 1:
            result.append(-abs(element))
         else:
            result.append(element)
         cur += 1

   if recurse:
      return cur, result
   else:
      return result


def stack(l, n, until = 'under'):
   if len(l) >= n:
      return l
   else:
      reps = float(n) / len(l)
      if until == 'under':
         reps = int(math.floor(reps))
      else:
         reps = int(math.ceil(reps))
      return l * reps
         

def untie(expr, signs = 'all positive'):
   '''
   TODO: deprecate unfive(); will require a direction input parameter here.

   >>> untie(41, action = 'new')
   (32, 8, 1)
   >>> untie(41, action = 'new', signs = 'change head')
   (-32, 8, 1)
   >>> untie(41, action = 'new', signs = 'change tail')
   (32, -8, -1)
   >>> untie(41, action = 'new', signs = 'change all')
   (-32, -8, -1)

   >>> untie(-41, action = 'new')
   (-32, -8, -1)
   >>> untie(-41, action = 'new', signs = 'change head')
   (32, -8, -1)
   >>> untie(-41, action = 'new', signs = 'change tail')
   (-32, 8, 1)
   >>> untie(-41, action = 'new', signs = 'change all')
   (32, 8, 1)

   >>> untie([2, 3, 9, 41], action = 'new')
   [2, 3, 8, 1, 32, 8, 1]
   >>> untie([2, 3, 9, 41], action = 'new', signs = 'change head')
   [-2, -3, -8, 1, -32, 8, 1]
   >>> untie([2, 3, 9, 41], action = 'new', signs = 'change tail')
   [2, 3, 8, -1, 32, -8, -1]
   >>> untie([2, 3, 9, 41], action = 'new', signs = 'change all')
   [-2, -3, -8, -1, -32, -8, -1]

   >>> untie([-2, -3, -9, -41], action = 'new')
   [-2, -3, -8, -1, -32, -8, -1]
   >>> untie([-2, -3, -9, -41], action = 'new', signs = 'change head')
   [2, 3, 8, -1, 32, -8, -1]
   >>> untie([-2, -3, -9, -41], action = 'new', signs = 'change tail')
   [-2, -3, -8, 1, -32, 8, 1]
   >>> untie([-2, -3, -9, -41], action = 'new', signs = 'change all')
   [2, 3, 8, 1, 32, 8, 1]

   >>> untie([2, [3, 9], 41], action = 'new')
   [2, [3, 8, 1], 32, 8, 1]
   '''

   if isinstance(expr, int):
      exponent = 1
      result = []
      total = 0
      for cur in reversed(mathtools.binary_string(abs(expr))):
         if cur == '1':
            total += exponent
         else:
            if total > 0:
               result.append(total)
            total = 0
         exponent *= 2
      result.append(total)
      result.reverse()
      if expr < 0:
         result = [-n for n in result]
      if signs == 'change head':
         result[0] = -result[0]
      elif signs == 'change tail':
         result[1:] = [-n for n in result[1:]]
      elif signs == 'change all':
         result = [-n for n in result]
      result = tuple(result)
      #if action == 'in place': 
      #   expr[:] = result
      #else:
      #   return tuple(result)
      return tuple(result)

   elif isinstance(expr, list):
      result = []
      for subexpr in expr:
         new = untie(subexpr, signs)
         if isinstance(subexpr, int):
            result.extend(new)
         elif isinstance(subexpr, list):
            result.append(new)
      #if action == 'in place':
      #   expr[:] = result
      #else:
      #   return result
      return result


def unfive(l, target = 'negative', action = 'in place'):
   '''
   TODO - fully implement target, including 'both' value.

   >>> l = [[1, 1, 5]]
   >>> unfive(l)
   >>> l
   [[1, 1, 5]]

   >>> l = [[1, 1, -5]]
   >>> unfive(l)
   >>> l
   [[1, 1, 1, -4]]

   >>> l = [[1], [5], [5, 1], [1, 5], [5, 5], [1, 5, 1]]
   >>> unfive(l, target = 'positive')
   >>> l
   [[1], [4, 1], [4, 1, 1], [1, 1, 4], [4, 1, 1, 4], [1, 4, 1, 1]]

   >>> l = [[1, 1, -5]]
   >>> unfive(l, action = 'new')
   [[1, 1, 1, -4]]
   >>> l
   [[1, 1, 5]]
   '''

   result = []

   if target == 'negative':

      for element in l:

         # -5 at beginning
         if element[0] == -5:
            result.append([-4, 1] + element[1:])

         # -5 at end
         elif element[-1] == -5:
            result.append(element[:-1] + [1, -4])

         # -5 in middle 
         elif -5 in element:
            new = []
            for x in element:
               if x != -5:
                  new.append(x)
               else:
                  new.append(-4)
                  new.append(1)

         # no -5
         else:
            result.append(element)

   if target == 'positive':

      for sublist in l:
   
         new = sublist

         # 5 at beginning
         if new[0] == 5:
            new = [4, 1] + new[1:]

         # 5 at end
         if new[-1] == 5:
            new = new[:-1] + [1, 4]

         # 5 in middle
         if 5 in new:
            new = [(4, 1) if element == 5 else element for element in new]
            new = listtools.flatten(new)

         result.append(new)

   if action == 'in place':
      l[:] = result
   else:
      return result


def convolve(l, s, action = 'in place'):
   '''
   Add elements in s to the first and last positions of corresponding elements in l.

   >>> l = [[2, 2, 2], [2, 2], [2, 2, 2]]     
   >>> convolve(l, [1, 5, 10])
   >>> l
   [[12, 2, 7], [3, 12], [7, 2, 3]]

   >>> l = [[2, 2, 2], [2, 2], [2, 2, 2]]
   >>> convolve(l, [1, 5, 10], action = 'new')
   [[12, 2, 7], [3, 12], [7, 2, 3]]
   >>> l
   [[2, 2, 2], [2, 2], [2, 2, 2]]
   '''

   if len(l) != len(s):
      print 'convolve(l, s): len(l) must equal len(s).'
      raise ValueError

   result = []

   for i in range(len(l)):

      new = []
      for element in l[i]:
         new.append(element)

      if len(new) > 1:

         if i == 0:
            new[0] += int(s[-1])
            new[-1] += int(s[i + 1])
         elif 0 < i < len(l) - 1:
            new[0] += int(s[i - 1])
            new[-1] += int(s[i + 1])
         elif i == len(l) - 1:
            new[0] += int(s[i - 1])
            new[-1] += int(s[0])

      result.append(new)
   
   if action == 'in place':
      l[:] = result
   else:
      return result


def caulk(l, s, action = 'in place'):
   '''
   Transforms sublists-with-negatives to sublists-with-positives;
   'caulks' sublists in l according to elements in s.

   >>> l = [[-1, 1, 1], [1, -1, 1], [1, 1, -1]]
   >>> caulk(l, [-1, -1, -1])
   >>> l
   [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

   >>> l = [[-1, 1, 1], [1, -1, 1], [1, 1, -1]]
   >>> caulk(l, [-1, 1, 1])
   >>> l
   [[1, 1, 1], [1, -1, 1], [1, 1, -1]]

   >>> l = [[-1, 1, 1], [1, -1, 1], [1, 1, -1]]
   >>> caulk(l, [1, 1, 1])
   >>> l
   [[-1, 1, 1], [1, -1, 1], [1, 1, -1]]
   '''

   result = []

   i = 0

   for sublist in l:

      # if the sublist is all positive, like [1, 1, 1, 1, 1]
      if len([x for x in sublist if x < 0]) == 0:
         result.append(sublist)

      # elif the sublist is like [1, 1, -3] and contains a negative sublist
      elif len([x for x in sublist if x < 0]) > 0:

         # check the directives list ...
         # if the current directive == 1, keep the sublist
         if s[i % len(s)] == 1:
            result.append(sublist)

         # but if the current directive == -1, remove all rests from the sublist
         elif s[i % len(s)] == -1:
            result.append([abs(x) for x in sublist])

         # increment ONLY when we've just processed a sublist-with-negatives
         i += 1
   
   if action == 'in place':
      l[:] = result
   else:
      return result


def glob(l, s, action = 'in place'):
   '''
   >>> glob([[1, 2, 3], [4, 5], [6, 7, 8, 9]], (1, 1, 1))
   [[-6], [-9], [-30]]
   >>> glob([[1, 2, 3], [4, 5], [6, 7, 8, 9]], (1, 1, 0))
   [[-6], [-9], [6, 7, 8, 9]]
   >>> glob([[1, 2, 3], [4, 5], [6, 7, 8, 9]], (1, 0, 0))
   [[-6], [4, 5], [6, 7, 8, 9]]
   >>> glob([[1, 2, 3], [4, 5], [6, 7, 8, 9]], (0, 0, 0))
   [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
   '''

   result = []

   for i, sublist in enumerate(l):
      if s[i % len(s)] == 0:
         result.append(sublist)
      else:
         result.append([-sum([abs(element) for element in sublist])])

   if action == 'in place':
      l[:] = result
   else:
      return result


# TODO merge flamingo() and negate()
def flamingo(l, s, period = False, action = 'in place'):
   '''
   Negate elements in l at indices in s.

   >>> s = [0, 1, 2]
   >>> l = range(10)
   >>> flamingo(l, s)
   >>> l
   [0, -1, -2, 3, 4, 5, 6, 7, 8, 9]

   >>> l = range(10)
   >>> flamingo(l, s, period = 5)
   >>> l
   [0, -1, -2, 3, 4, -5, -6, -7, 8, 9]
   '''

   result = []

   for i, element in enumerate(l):  
      if (i in s) or (period and i % period in s):
         result.append(-element)
      else:
         result.append(element)

   if action == 'in place':
      l[:] = result
   else:
      return result


def negate(l, s, action = 'in place'):
   '''
   Cyclically negate 1-element sublists in l according to s.

   >>> l = [[1], [2, 3], [4], [5, 6]]
   >>> negate(l, [0])
   >>> l
   [[1], [2, 3], [4], [5, 6]]

   >>> l = [[1], [2, 3], [4], [5, 6]]
   >>> negate(l, [1])
   >>> l
   [[-1], [2, 3], [-4], [5, 6]]

   >>> l = [[1], [2, 3], [4], [5, 6]]
   >>> negate(l, [0, 1])
   >>> l
   [[1], [2, 3], [-4], [5, 6]]
   '''

   result = []
   
   k = 0

   # scan every sublist in l
   for i, sublist in enumerate(l):

      # if the sublist has length 1 like [-9] or [9]
      if len(sublist) == 1: 

         # and if directed, negate sublist
         if s[k % len(s)] == 1:
            result.append([-sublist[0]])

         # otherwise copy sublist over directly
         else:
            result.append(sublist)

         # increment only after a length-1 sublist
         k += 1

      else:
         result.append(sublist)

   if action == 'in place':
      l[:] = result
   else:
      return result


def permute(l, s, action = 'in place'):
   '''
   Permutes integer pitch list or note list l by integer pc list s.

   >>> l = [note.Note(n, 1, 4) for n in [17, -10, -2, 11]]
   >>> permute(l, [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
   >>> l
   [bf4, d4, f''4, b'4]

   >>> permute(
   ...     [note.Note(n, 1, 4) for n in [17, -10, -2, 11]],
   ...     [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11],
   ...     action = 'new')
   [bf4, d4, f''4, b'4]
   '''

   result = []

   if isinstance(l[0], int):
      for element in s:
         result.extend([note for note in l if note % 12 == element])
   else:
      for element in s:
         result.extend([note for note in l if note.pitch.pc == element])

   if action == 'in place':
      l[:] = result
   else:
      return result 
      

def ones(l, action = 'in place'):
   '''
   >>> l = range(1, 5)
   >>> ones(l)
   >>> l
   [[1], [1, 1], [1, 1, 1], [1, 1, 1, 1]]

   >>> l = range(1, 5)
   >>> ones(l, action = 'new')
   [[1], [1, 1], [1, 1, 1], [1, 1, 1, 1]]
   >>> l
   [1, 2, 3, 4]
   '''

   result = []
   for element in l:
      result.append([1] * element)

   if action == 'in place':
      l[:] = result
   else:
      return result


def within(i, indices):
   '''
   Returns True if i in indices token, and False otherwise.

   >>> within(7, [0, 1, 2, 3, 4])
   False

   >>> within(7, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
   True

   >>> within(7, ([0, 1, 2, 3, 4], 5))
   True

   >>> within(7, ([0, 1, 2, 3, 4], 10))
   False
   '''

   if isinstance(indices, tuple):
      return i % indices[-1] in indices[0]
   else:
      return i in indices  


def pick(i, token):
   '''
   Picks element i from material in token.

   >>> material = [2, 3, 7, 5]
   >>> pick(0, material)
   2

   >>> pick(10, material)

   >>> pick(0, (material, 4))
   2

   >>> pick(10, (material, 4))
   7
   '''

   if isinstance(token, tuple):
      material = token[0]
      period = token[-1]
      try:
         return material[i % period]
      except:
         return None
   else:
      material = token
      try:
         return material[i]
      except:
         return None


def replace(l, indices, material, action = 'in place'):
   '''
   Replace elements at indices in l with material.

   >>> l = range(20)
   >>> replace(l, ([0], 2), (['A', 'B'], 3))
   >>> l
   ['A', 1, 'B', 3, 4, 5, 'A', 7, 'B', 9, 10, 11, 'A', 13, 'B', 15, 16, 17, 'A', 19]

   >>> l = range(20)
   >>> replace(l, ([0], 2), (['*'], 1))
   >>> l
   ['*', 1, '*', 3, '*', 5, '*', 7, '*', 9, '*', 11, '*', 13, '*', 15, '*', 17, '*', 19]

   >>> l = range(20)
   >>> replace(l, ([0], 2), ['A', 'B', 'C', 'D'])
   >>> l
   ['A', 1, 'B', 3, 'C', 5, 'D', 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

   >>> l = range(20)
   >>> replace(l, [0, 1, 8, 13], ['A', 'B', 'C', 'D'])
   >>> l
   ['A', 'B', 2, 3, 4, 5, 6, 7, 'C', 9, 10, 11, 12, 'D', 14, 15, 16, 17, 18, 19]
   '''

   result = []
   j = 0

   for i, element in enumerate(l):
      if within(i, indices):
         if pick(j, material):
            result.append(pick(j, material))
         else:
            result.append(element)
         j += 1
      else:
         result.append(element)

   if action == 'in place':
      l[:] = result
   else:
      return result  


def series(start = 0, step = 0, offsets = [0], max = sys.maxint):
   '''
   >>> s = series()
   >>> [s.next(), s.next(), s.next(), s.next(), s.next(), s.next()]
   [0, 0, 0, 0, 0, 0]

   >>> s = series(24)      
   >>> [s.next(), s.next(), s.next(), s.next(), s.next(), s.next()]
   [24, 24, 24, 24, 24, 24]

   >>> s = series(24, 3)
   >>> [s.next(), s.next(), s.next(), s.next(), s.next(), s.next()]
   [24, 27, 30, 33, 36, 39]

   >>> s = series(0, 0, [0, 2, 7])
   >>> [s.next(), s.next(), s.next(), s.next(), s.next(), s.next()]
   [0, 0, 2, 9, 9, 11]

   >>> s = series(0, 4, [1, 2])
   >>> [s.next(), s.next(), s.next(), s.next(), s.next(), s.next()]
   [0, 5, 11, 16, 22, 27]
   '''

   n = start
   i = 0

   while n < sys.maxint:
      yield n
      n += step
      n += offsets[i % len(offsets)]
      i += 1

   raise StopIteration


def intize(w, action = 'in place'):
   '''
   Map 1.0, 2.0, 3.0, ... to 1, 2, 3, ....

   Leave noninteger floats unchanged.

   >>> w = [[1.0, 2, 4], [2, 4.0], [2, 4.0, 4.0, 4.5]]
   >>> intize(w)
   >>> w
   [[1, 2, 4], [2, 4], [2, 4, 4, 4.5]]
   '''

   result = []

   if isinstance(w[0], list):
      for sublist in w:
         result.append(intize(sublist, action = 'new'))
   else:
      for element in w:
         if isinstance(element, float) and element - int(element) == 0:
            result.append(int(element))
         else:
            result.append(element)

   if action == 'in place':
      w[:] = result
   else:
      return result


def resegment(w, s, max = False, overhang = True):
   '''
   Resegment two-dimensional list w into sublists of weights not less than s.

   Use on measure division lists for overlapping beams.

   >>> w = [[10], [10, 10, 10], [1], [3], [4], [5], [1], [2], [10, 10]]

   >>> resegment(w, [10])
   [[10], [10], [10], [10], [1, 3, 4, 5], [1, 2, 10], [10]]

   >>> resegment(w, [10, 15])
   [[10], [10, 10], [10], [1, 3, 4, 5, 1, 2], [10], [10]]

   >>> resegment(w, [15])
   [[10, 10], [10, 10], [1, 3, 4, 5, 1, 2], [10, 10]]

   Use max to limit sublist maximum length.

   >>> resegment(w, [15], max = 3)
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


def stripe(w, s, action = 'in place'):
   '''
   Cyclically negate every sth element in flattened w.

   >>> w = [[3, 3, 2], [1, 3, 3, 3, 2], [1, 3], [3, 3, 3, 3, 3, 1]]
   >>> utilities.stripe(w, [0, 0, 1])
   >>> w
   [[3, 3, -2], [1, 3, -3, 3, 2], [-1, 3], [3, -3, 3, 3, -3, 1]]
   '''

   result = []
   cur = 0

   for sublist in w:
      new = []
      for element in sublist:
         if s[cur % len(s)] == 1:
            new.append(-element)
         else:
            new.append(element)
         cur += 1
      result.append(new)

   if action == 'in place':
      w[:] = result
   else:
      return result


def corrugate(w, target = 'positives', action = 'in place'):
   '''
   Replace positive integers with 1-sequences;
   flat or nested w.

   >>> l = [1, 2, 2, -4]
   >>> corrugate(l, action = 'new')
   [1, 1, 1, 1, 1, -4]

   >>> corrugate(l, target = 'negatives', action = 'new')
   [1, 2, 2, -1, -1, -1, -1]

   >>> corrugate(l, target = 'all', action = 'new')
   [1, 1, 1, 1, 1, -1, -1, -1, -1]

   >>> w = [[1, 3, -4], [1, 2, -2, -4]]
   >>> corrugate(w)
   >>> w
   [[1, 1, 1, 1, -4], [1, 1, 1, -2, -4]]
   '''

   result = []

   # two-dimensional w
   if isinstance(w[0], list):
      for sublist in w:
         result.append(corrugate(sublist, target = target, action = 'new')) 
   # one-dimensional w
   else:
      for element in reversed(w):
         if target == 'positives':
            if element < 0:
               result.insert(0, element)
            else:
               result[0:0] = [1] * element 
         elif target == 'negatives':
            if element > 0:
               result.insert(0, element)
            else:
               result[0:0] = [-1] * abs(element)
         elif target == 'all':
            if element == 0:
               result.insert(0, element)
            else:
               result[0:0] = [mathtools.sign(element) * 1] * abs(element)
         else:
            print 'Unkown target %s.' % target
            raise ValueError
      
   if action == 'in place':
      w[:] = result
   elif action == 'new':
      return result


def intaglio(l, s, t = 1):
   '''
   Repeat s and weight-partition according to l.

   >>> intaglio([3, 5, 10, 10], [4])
   [[3], [1, 4], [4, 4, 2], [2, 4, 4]]

   >>> intaglio([3, 5, 10, 10], [5])
   [[3], [2, 3], [2, 5, 3], [2, 5, 3]]

   >>> intaglio([3, 5, 5, 10, 10], [4, 5])
   [[3], [1, 4], [1, 4], [5, 4, 1], [4, 4, 2]]

   Negative values work fine in s.

   >>> intaglio([3, 5, 10, 10], [4, -5])
   [[3], [1, -4], [-1, 4, -5], [4, -5, 1]]

   Optional t gloms light-weight sublists.

   >>> intaglio([3, 5, 6, 6], [1])
   [[1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]

   >>> intaglio([3, 5, 6, 6], [1], t = 5)
   [[3], [5], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]

   Large values of t glom all sublists.

   >>> intaglio([3, 5, 6, 6], [1], t = 99)
   [[3], [5], [6], [6]]
   '''

   assert all([isinstance(x, int) and x > 0 for x in l])
   assert all([isinstance(x, int) and x != 0 for x in s])
   assert len(l) > 0
   assert len(s) > 0

   result = [ ]

   result = listtools.repeat_to_weight(s, sum(l))
   result = listtools.partition_by_weights(result, l, overhang = True)

   for i, sublist in enumerate(result):
      if listtools.weight(sublist) <= t:
         result[i] = [listtools.weight(sublist)]

   return result


def emboss(l, s, p, action = 'in place'):
   '''   
   Corrugate elements of l;
   strikethrough according to s;
   group according to p.

   Examples.
   '''

   result = []

   result = listtools.repeat_to_weight(s, sum(l))
   result = listtools.partition_by_weights(result, l, overhang = True)
   corrugate(result)
   part_lengths = [len(part) for part in p]
   result = listtools.partition_by_counts(result, part_lengths)

   if action == 'in place':
      l[:] = result
   elif action == 'new':
      return result


def times(w, n, action = 'in place'):
   '''
   Multiply sublists or elements of w by n.

   >>> w = [[1, 2, 4], [2, 4], [2, 4, 4, 5]]
   >>> times(w, 3)
   >>> w
   [[3, 6, 12], [6, 12], [6, 12, 12, 15]]
   '''

   result = []

   if isinstance(w[0], list):
      for sublist in w:
         result.append(times(sublist, n, action = 'new'))
   else:
      result = [element * n for element in w]

   if action == 'in place':
      w[:] = result
   elif action == 'new':
      return result


def clump(w, action = 'in place'):
   '''
   Add together runs of negative numbers.

   >>> w = [[-1, -1, 2, 3, -5], [1, 2, 5, -5, -6]]
   >>> clump(w)
   >>> w
   [[-2, 2, 3, -5], [1, 2, 5, -11]]
   '''

   result = []

   if isinstance(w[0], list):
      for sublist in w:
         result.append(clump(sublist, action = 'new'))
   else:
      total = 0
      for x in w:
         if x >= 0:
            if total != 0:
               result.append(total)
               total = 0
            result.append(x)
         else:
            total += x
      if total != 0:
         result.append(total)

   if action == 'in place':
      w[:] = result
   elif action == 'new':
      return result


def lump(w):
   '''
   Add together runs of positive numbers.

   [[-1, -1, 2, 3, -5], [1, 2, 5, -5, -6]]
   >>> lump(w) 
   [[-1, -1, 5, -5], [8, -5, -6]]
   '''

   result = []

   if isinstance(w[0], list):
      for sublist in w:
         result.append(lump(sublist))
   else:
      total = 0
      for x in w:
         if x <= 0:
            if total != 0:
               result.append(total)
               total = 0
            result.append(x)
         else:
            total += x
      if total != 0:
         result.append(total)

   return result


def recombine(target, s, insert, t, loci):
   '''
   Partition target list cyclically according to s;
   partition insert list cyclically according to t;
   overwrite parts of target with parts of insert 
   at positions in loci.

   >>> target = range(12)
   >>> insert = [9] * 10
   >>> loci = [0, 3, 5]
   >>> recombine(target, 2, insert, [2, 2, 6], loci)
   [9, 9, 2, 3, 4, 5, 9, 9, 8, 9, 9, 9, 9, 9, 9, 9]
   '''

   a = listtools.partition_by_counts(
      target, [s], cyclic = True, overhang = True)
   b = listtools.partition_by_counts(
      insert, [t], cyclic = True, overhang = True)
   replace(a, loci, b)
   
   result = [ ]
   for sublist in a:
      result.extend(sublist)

   return result


def read(l, start, length):
   '''
   >>> l = [1, 1, 2, 3, 5, 5, 6]
   >>> read(l, 4, 18)
   [5, 5, 6, 1, 1, 2, 3, 5, 5, 6, 1, 1, 2, 3, 5, 5, 6, 1]
   '''

   result = []
   m = len(l)

   for i in range(start, start + length):
      result.append(l[i % m])

   return result


def positivize(w):
   '''Turn all negative numbers positive.
      Leave nonpositive numbers unchanged.

      >>> w = [[-1, -1, 2, 3, -5], [1, 2, 5, -5, -6]]
      >>> positivize(w)
      [[1, 1, 2, 3, 5], [1, 2, 5, 5, 6]]'''

   result = [ ]

   if isinstance(w[0], list):
      for sublist in w:
         result.append(positivize(sublist))
   else:
      for x in w:
         if x < 0:
            result.append(-x)
         else:
            result.append(x)

   return result


def sieve(pairs, window):
   '''
   Xenakis sieves;

   return all integers in window congruent to some residue in pairs.

   >>> sieve([(5, 0), (5, 1)], [(0, 20)])
   [0, 1, 5, 6, 10, 11, 15, 16]

   >>> sieve([(5, 0), (5, 1)], [(0, 20), (50, 20)])
   [0, 1, 5, 6, 10, 11, 15, 16, 50, 51, 55, 56, 60, 61, 65, 66]
   '''

   result = []

   domain = []
   for start, length in window:
      domain.extend(range(start, start + length))

   for i in domain:
      for modulus, residue in pairs:
         if i % modulus == residue % modulus:
            result.append(i)
            break

   return result


def pleat(ll, n):
   '''Return n of each of the l in ll.

      >>> pleat([1, 1, 2, 3, 5, 5, 6], 2)
      [1, 1, 1, 1, 2, 2, 3, 3, 5, 5, 5, 5, 6, 6]'''

   result = [ ]

   for l in ll:
      result.extend([l] * n)

   return result


def smelt(ll):
   '''Return positive subsequences in the absolute cumulative sums of ll.

      >>> ll = [1, -1, -2, 1, -2, -1, -2, 2, 1, -3, -1, 2, -2, -1, -1]
      >>> smelt(ll)
      [[1], [5], [11, 12, 13], [18, 19]]'''

   result = clump(ll, action = 'new')
   result = lump(result)
   first  = result[0]

   result = piles(result)
   result = [0] + result
   result = [1 + n for n in result]
   result = listtools.pairwise(result)

   new = [ ]
   if mathtools.sign(first) == 1:
      for i, pair in enumerate(result):
         if i % 2 == 0:
            new.append(pair)
   else:
      for i, pair in enumerate(result):
         if i % 2 == 1:
            new.append(pair)

   result = [range(*pair) for pair in new]
      
   return result


def constellate(psets, r):
   '''Return outer product of octave transpositions of psets in r.'''

   transpositions = [
      pitchtools.octave_transpositions(pset, r) for pset in psets]
   result = listtools.outer_product(transpositions)
   #[listtools.flatten(x) for x in result]
   for i, part in enumerate(result):
      result[i] = listtools.flatten(part)
   [x.sort( ) for x in result]
   return result
