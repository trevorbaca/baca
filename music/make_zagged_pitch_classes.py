#from abjad import *
from abjad.tools import sequencetools
import baca


def make_zagged_pitch_classes(pc_cells, division_cells, grouping_counts):
    pc_cells = baca.util.helianthate(pc_cells, -1, 1)
    division_cells = baca.util.helianthate(division_cells, -1, 1)
    division_cells = sequencetools.flatten_sequence(division_cells, depth=1)
    division_cells = sequencetools.CyclicTuple(division_cells)
    tmp = []
    for i, pc_segment in enumerate(pc_cells):
        parts = sequencetools.partition_sequence_by_ratio_of_lengths(pc_segment, division_cells[i])
        tmp.extend(parts)
    pc_cells = tmp
    pc_cells = sequencetools.partition_sequence_cyclically_by_counts_with_overhang(pc_cells, grouping_counts)
    pc_cells = [sequencetools.join_subsequences(x) for x in pc_cells]
    pc_cells = sequencetools.partition_sequence_cyclically_by_counts_with_overhang(pc_cells, grouping_counts)
    material = sequencetools.CyclicTree(pc_cells)
    return material
