from baca.scf.InteractiveMaterialProxy import InteractiveMaterialProxy
from baca.scf.UserInputWrapper import UserInputWrapper
from baca.scf.editors.InteractiveEditor import InteractiveEditor
import baca
import os


class ZaggedPitchClassMaker(InteractiveEditor):

    def __init__(self, session=None, target=None, **kwargs):
        InteractiveEditor.__init__(self, session=session, target=target)
        self.stylesheet = os.path.join(os.path.dirname(__file__), 'stylesheet.ly')
        self._generic_output_name = 'zagged pitch-classes'

    ### READ-ONLY PUBLIC ATTRIBUTES ###

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
        import baca
        return baca.music.make_zagged_pitch_classes(pc_cells, division_cells, grouping_counts)

    def make_lilypond_file_from_output_material(self, material):
        from baca.music.make_zagged_pitch_classes import make_lilypond_file_from_output_material
        return make_lilypond_file_from_output_material(material)
