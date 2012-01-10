from baca.scf.InteractiveMaterialProxy import InteractiveMaterialProxy
from baca.scf.UserInputWrapper import UserInputWrapper
from baca.scf.editors.InteractiveEditor import InteractiveEditor
import baca
import os


# TODO: finish migration to interactive editor
#class ZaggedPitchClassMaker(InteractiveMaterialProxy):
class ZaggedPitchClassMaker(InteractiveEditor):

    #def __init__(self, **kwargs):
    def __init__(self, session=None, target=None, **kwargs):
        #Maker.__init__(self, **kwargs)
        InteractiveEditor.__init__(self, session=session, target=target)
        self.stylesheet = os.path.join(os.path.dirname(__file__), 'stylesheet.ly')
        self._generic_output_name = 'zagged pitch-classes'

    ### PUBLIC ATTRIBUTES ###

    output_file_import_statements = [
        'from abjad.tools.sequencetools.CyclicTree import CyclicTree',]

    user_input_import_statements = [
        'from baca.scf.makers import ZaggedPitchClassMaker',
        'from baca.scf import UserInputWrapper',]

    user_input_template = UserInputWrapper([
        ('pc_cells', [[0, 7, 2, 10], [9, 6, 1, 8], [5, 4, 2, 11, 10, 9]]),
        ('division_cells', [[[1], [1], [1], [1, 1]], [[1], [1], [1], [1, 1, 1], [1, 1, 1]]]),
        ('grouping_counts', [1, 1, 2, 3]),
        ])

    ### PUBLIC METHODS ###

    def get_output_file_lines(self, material, material_underscored_name):
        output_file_lines = []
        output_file_lines.append('%s = %s' % (material_underscored_name, material))
        return output_file_lines

    def make(self, pc_cells, division_cells, grouping_counts):
        from abjad import *
        from abjad.tools import sequencetools
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

    def make_lilypond_file_from_output_material(self, material):
        from abjad import *
        from abjad.tools import sequencetools
        pcs = list(material.iterate_payload())
        leaves = leaftools.make_leaves(pcs, [Duration(1, 8)])
        voice = Voice(leaves)
        staff = Staff([voice])
        score = Score([staff])
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
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
        return lilypond_file
