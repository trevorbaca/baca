from baca.pitch.constellate import constellate


'''Each constellation must be an (ordered) list rather than
   an (unordered) set because lists are not hashable.'''

D = [
      constellate(p, [0, 37]) for p in [
         [[0, 2, 10], [16, 19, 20], [23, 30, 33], [27, 29, 37]],
         [[4, 8, 11], [7, 15, 17], [18, 21, 24], [25, 26, 34]],
         [[6, 9, 13], [12, 14, 22], [19, 27, 29], [28, 32, 35]]
      ]
   ]
