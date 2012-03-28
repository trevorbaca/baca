from abjad import *
from abjad.tools import sequencetools
import baca
import os


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


def make_illustration_from_output_material(material, **kwargs):
    pcs = list(material.iterate_payload())
    leaves = leaftools.make_leaves(pcs, [Duration(1, 8)])
    voice = Voice(leaves)
    staff = Staff([voice])
    score = Score([staff])
    illustration = lilypondfiletools.make_basic_lilypond_file(score)

    stylesheet = os.path.join(os.environ.get('SCFPATH'), 'stylesheets', 'rhythm_letter_16.ly')
    illustration.file_initial_user_includes.append(stylesheet)
    
    voice.engraver_consists.add('Horizontal_bracket_engraver')
    for level in (1, 2):
        level_sizes = []
        for x in material.iterate_at_level(level):
            size = len(list(x.iterate_payload()))
            level_sizes.append(size)
        for part in sequencetools.partition_sequence_once_by_counts_without_overhang(
            voice.leaves, level_sizes):
            spannertools.HorizontalBracketSpanner(part)
    cur_group = 0
    for leaf in voice.leaves:
        brackets = list(spannertools.get_spanners_attached_to_component(
            leaf, klass=spannertools.HorizontalBracketSpanner))
        if brackets[0][0] is leaf:
            if brackets[1][0] is leaf:
                markuptools.Markup(r'\bold { %s }' % cur_group, 'up')(leaf)
                cur_group += 1
    bar_line = scoretools.add_double_bar_to_end_of_score(score)
    spanner = spannertools.Spanner(voice.leaves)

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
