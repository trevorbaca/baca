from baca.utilities.utilities import binary, rotate, unique


U = [''.join(list(reversed(binary(x).zfill(12)))) for x in range(4096)]
def helper(binaryString):
   result = zip(binaryString, range(len(binaryString)))
   result = [x[1] for x in result if x[0] == '1']
   return result
U = [helper(pset) for pset in U]

def width(pset):
   st = sorted(pset)
   return st[-1] - st[0]

def T(pset, n):
   return [(p + n) % 12 for p in pset]

def M(pset, n):
   return [(p * n) % 12 for p in pset]

def I(pset):
   return [(12 - p) % 12 for p in pset]

def C(pset):
   st = sorted(pset)
   result = []
   for i in range(len(st)):
      result.append(rotate(st, 'left', i, action = 'new'))
   return result

def CI(pset):
   result = C(pset) + C(I(pset))
   unique(result)
   return result
   
def T0(pset):
   return [(p - pset[0]) % 12 for p in pset]

def CT0(pset):
   return [T0(x) for x in C(pset)]

def CIT0(pset):
   return [T0(x) for x in CI(pset)]

def P(pset, TTOs = 'TI'):
   if pset == []:
      return []
   if TTOs == 'T':
      S = CT0(pset)
   elif TTOs == 'TI':
      S = CIT0(pset)
   else:
      print 'Unknown TTOs %s.' % TTOs
      raise Exception
   mw = min([width(x) for x in S])
   candidates = [x for x in S if width(x) == mw]
   candidates.sort()
   return candidates[0]

def reps(TTOs = 'TI'):
   primeForms = unique([P(x, TTOs) for x in U], action = 'new')
   result = [[]] * 13
   for i in range(13):
      result[i] = sorted([x for x in primeForms if len(x) == i]) 
   return result

representatives = {}
representatives['TI'] = reps('TI')
representatives['T'] = reps('T')

def register(pcseg):
   '''
   Turn <0, 3, 2> into <0, 3, 14> 
   '''

   result = [pcseg[0]]
   
   for pc in pcseg[1:]:
      while pc <= result[-1]:
         pc += 12
      result.append(pc)
      '''
      p = int(math.ceil(result[-1] / 12.0) * 12) + pc
      result.append(p)
      '''

   return result

def center(pseg, r = [0, 18]):
   '''
   Center in range r to reduce ledger lines.

   Range r taken as [closed, open) interval.

   >>> pseg = [2, 3, 36]

   >>> pitchtheory.center(pseg)
   [-10, -9, 24]

   >>> pitchtheory.center(pseg, octave = 3)
   [-22, -21, 12]

   >>> pitchtheory.center(pseg, octave = 5)
   [2, 3, 36]
   '''

   midpoint = (max(pseg) + min(pseg)) / 2

   if max(r) - min(r) < 12:
      print 'Center range less than one octave may not converge.'

   transposition = 0

   if  midpoint > max(r):
      while midpoint > max(r):
         transposition -= 12
         midpoint += transposition
   elif midpoint < min(r):
      while midpoint < min(r):
         transposition += 12
         midpoint += transposition

   result = [p + transposition for p in pseg]

   return result

def split(pset):
   '''
   Turn [-12, -10, -1, 2, 24] into [[-12, -10], [-1, 2, 24]].
   '''

   treble = [p for p in pset if p >= -2]
   bass = [p for p in pset if p < -2]

   return treble, bass
