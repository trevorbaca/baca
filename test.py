from abjad import *
from beamtools import beamRunsByDuration

t = Staff([Note(0, (1, 16)),
     Note(1, (1, 16)),
     Note(2, (1, 8)),
     Note(3, (1, 8)),
     Note(4, (1, 16)),
     Note(5, (1, 16))])

beamRunsByDuration(t, [(2, 4)])

t = Container([Note(n, (1, 8)) for n in range(8)])

t = Staff([Note(0, (1, 8)), Rest((1, 8)),
   Note(0, (1, 8)), Rest((1, 8)),
   Note(0, (1, 8)), Rest((1, 8)),
   Note(0, (1, 8)), Rest((1, 8)),
   Note(0, (1, 8)), Rest((1, 8))])
