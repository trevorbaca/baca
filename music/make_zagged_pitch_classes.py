import os
import baca
from experimental import *


# TODO: make into class
def make_zagged_pitch_classes(pc_cells, division_cells, grouping_counts):
    from experimental.tools import musicexpressiontools
    pc_cells = baca.utilities.helianthate(pc_cells, -1, 1)
    division_cells = baca.utilities.helianthate(division_cells, -1, 1)
    division_cells = sequencetools.flatten_sequence(division_cells, depth=1)
    division_cells = datastructuretools.CyclicTuple(division_cells)
    tmp = []
    for i, pc_segment in enumerate(pc_cells):
        parts = sequencetools.partition_sequence_by_ratio_of_lengths(
            pc_segment, 
            division_cells[i],
            )
        tmp.extend(parts)
    pc_cells = tmp
    pc_cells = sequencetools.partition_sequence_by_counts(
        pc_cells, grouping_counts, cyclic=True, overhang=True)
    pc_cells = [sequencetools.join_subsequences(x) for x in pc_cells]
    pc_cells = sequencetools.partition_sequence_by_counts(
        pc_cells, grouping_counts, cyclic=True, overhang=True)
    material = datastructuretools.CyclicPayloadTree(pc_cells)
    material = musicexpressiontools.StatalServer(material)
    return material


def make_illustration_from_output_material(statal_server, **kwargs):
    material = statal_server.cyclic_tree
    pcs = list(material.iterate_payload())
    leaves = leaftools.make_leaves(pcs, [Duration(1, 8)])
    voice = Voice(leaves)
    staff = Staff([voice])
    score = Score([staff])
    illustration = lilypondfiletools.make_basic_lilypond_file(score)

    configuration = scoremanager.core.ScoreManagerConfiguration()
    stylesheet = os.path.join(
        configuration.built_in_stylesheets_directory_path,
        'rhythm-letter-16.ly',
        )
    illustration.file_initial_user_includes.append(stylesheet)

    voice.consists_commands.append('Horizontal_bracket_engraver')
    for level in (1, 2):
        level_sizes = []
        for x in material.iterate_at_level(level):
            size = len(list(x.iterate_payload()))
            level_sizes.append(size)
        for part in sequencetools.partition_sequence_by_counts(
            voice.select_leaves(), 
            level_sizes, 
            cyclic=False, 
            overhang=False,
            ):
            spannertools.HorizontalBracketSpanner(part)
    current_group = 0
    for leaf in voice.select_leaves():
        spanner_classes = spannertools.HorizontalBracketSpanner
        brackets = inspect_(leaf).get_spanners(spanner_classes)
        brackets = tuple(brackets)
        if brackets[0][0] is leaf:
            if brackets[1][0] is leaf:
                string = r'\bold {{ {} }}'.format(current_group)
                markup = markuptools.Markup(string, Up)
                markup.attach(leaf)
                current_group += 1
    bar_line = score.add_double_bar()

    score.override.bar_line.stencil = False
    score.override.flag.stencil = False
    score.override.stem.stencil = False
    score.override.text_script.staff_padding = 3
    score.override.time_signature.stencil = False

    if 'title' in kwargs:
        markup = markuptools.Markup(kwargs.get('title'))
        illustration.header_block.title = markup
    if 'subtitle' in kwargs:
        markup = markuptools.Markup(kwargs.get('subtitle'))
        illustration.header_block.subtitle = markup
    command = marktools.LilyPondCommandMark('accidentalStyle forget')
    illustration.layout_block.append(command)
    score.override.note_head.color = 'red'

    return illustration
