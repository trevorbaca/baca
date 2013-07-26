import os
import baca
from abjad import *


# TODO: make into class
def make_zagged_pitch_classes(pc_cells, division_cells, grouping_counts):
    from experimental.tools import musicexpressiontools
    pc_cells = baca.util.helianthate(pc_cells, -1, 1)
    division_cells = baca.util.helianthate(division_cells, -1, 1)
    division_cells = sequencetools.flatten_sequence(division_cells, depth=1)
    division_cells = sequencetools.CyclicTuple(division_cells)
    tmp = []
    for i, pc_segment in enumerate(pc_cells):
        parts = sequencetools.partition_sequence_by_ratio_of_lengths(pc_segment, division_cells[i])
        tmp.extend(parts)
    pc_cells = tmp
    pc_cells = sequencetools.partition_sequence_by_counts(
        pc_cells, grouping_counts, cyclic=True, overhang=True)
    pc_cells = [sequencetools.join_subsequences(x) for x in pc_cells]
    pc_cells = sequencetools.partition_sequence_by_counts(
        pc_cells, grouping_counts, cyclic=True, overhang=True)
    material = sequencetools.CyclicTree(pc_cells)
    material = musicexpressiontools.StatalServer(material)
    return material


def make_illustration_from_output_material(material, **kwargs):
    pcs = list(material.iterate_payload())
    leaves = leaftools.make_leaves(pcs, [Duration(1, 8)])
    voice = Voice(leaves)
    staff = Staff([voice])
    score = Score([staff])
    illustration = lilypondfiletools.make_basic_lilypond_file(score)

    stylesheet = os.path.join(os.environ.get('SCFPATH'), 'stylesheets', 'rhythm_letter_16.ly')
    illustration.file_initial_user_includes.append(stylesheet)

    voice.engraver_consists.append('Horizontal_bracket_engraver')
    for level in (1, 2):
        level_sizes = []
        for x in material.iterate_at_level(level):
            size = len(list(x.iterate_payload()))
            level_sizes.append(size)
        for part in sequencetools.partition_sequence_by_counts(
            voice.leaves, level_sizes, cyclic=False, overhang=False):
            spannertools.HorizontalBracketSpanner(part)
    cur_group = 0
    for leaf in voice.leaves:
        brackets = list(spannertools.get_spanners_attached_to_component(
            leaf, klass=spannertools.HorizontalBracketSpanner))
        if brackets[0][0] is leaf:
            if brackets[1][0] is leaf:
                markuptools.Markup(r'\bold { %s }' % cur_group, 'up')(leaf)
                cur_group += 1
    bar_line = score.add_double_bar()

    score.override.bar_line.stencil = False
    score.override.flag.stencil = False
    score.override.stem.stencil = False
    score.override.text_script.staff_padding = 3
    score.override.time_signature.stencil = False

    if 'title' in kwargs:
        illustration.header_block.title = markuptools.Markup(kwargs.get('title'))
    if 'subtitle' in kwargs:
        illustration.header_block.subtitle = markuptools.Markup(kwargs.get('subtitle'))

    contexttools.set_accidental_style_on_sequential_contexts_in_expr(score, 'forget')

    return illustration
