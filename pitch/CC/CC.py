from abjad.tools import pitchtools
from baca.pitch.ConstellationCircuit import ConstellationCircuit


starting_partitions = [
    [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]],
    [[-12, -10, -2], [4, 11, 27, 33, 37], [8, 17, 19, 30]],
    [[-8, 2, 15, 25], [-1, 20, 29, 31], [0, 10, 21, 42]],
    [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]],
    [[-12, -9, 1, 4], [-1, 18, 20, 33], [14, 19, 22, 29]],
    [[-10, -2, 0, 5], [-5, 3, 13, 16], [11, 30, 32, 45]],
    [[-10, -2, 5, 15, 25], [-1, 7, 18, 20], [0, 28, 33]],
    [[-12, 17, 27, 37], [-1, 7, 18, 21], [2, 10, 16, 20]]]

total_range = pitchtools.PitchRange((-39, 'inclusive'), (48, 'inclusive'))

CC = ConstellationCircuit(starting_partitions, total_range)
