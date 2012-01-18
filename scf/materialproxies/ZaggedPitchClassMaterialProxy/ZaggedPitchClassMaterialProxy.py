from abjad.tools import sequencetools
from baca.scf.UserInputHandlingMaterialProxy import UserInputHandlingMaterialProxy
from baca.scf.UserInputWrapper import UserInputWrapper
from baca.scf.editors.InteractiveEditor import InteractiveEditor


class ZaggedPitchClassMaterialProxy(UserInputHandlingMaterialProxy):

    def __init__(self, package_importable_name=None, session=None):
        UserInputHandlingMaterialProxy.__init__(
            self, package_importable_name=package_importable_name, session=session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    generic_output_name = 'zagged pitch-classes'

    output_data_module_import_statements = [
        'from abjad.tools.sequencetools.CyclicTree import CyclicTree',]

    user_input_demo_values = UserInputWrapper([
        ('pc_cells', [[0, 7, 2, 10], [9, 6, 1, 8], [5, 4, 2, 11, 10, 9]]),
        ('division_cells', [[[1], [1], [1], [1, 1]], [[1], [1], [1], [1, 1, 1], [1, 1, 1]]]),
        ('grouping_counts', [1, 1, 2, 3]),])

    user_input_module_import_statements = [
        'from baca.scf.materialproxies import ZaggedPitchClassMaterialProxy',
        'from baca.scf import UserInputWrapper',]

    # TODO: implement pitchtools.is_sequence_of_pitch_class_token_sequences()
    # TODO: implement sequencetools.all_are_nonnegative_integers(depth=n) keyword
    user_input_tests = [
        ('pc_cells', list),
        ('division_cells', list),
        ('grouping_counts', sequencetools.all_are_nonnegative_integers),]

    ### PUBLIC METHODS ###

    def get_output_data_file_lines(self, material, material_underscored_name):
        output_file_lines = []
        output_file_lines.append('%s = %s' % (material_underscored_name, material))
        return output_file_lines

    def make(self, pc_cells, division_cells, grouping_counts):
        import baca
        return baca.music.make_zagged_pitch_classes(pc_cells, division_cells, grouping_counts)

    def make_lilypond_file_from_output_material(self, material):
        from baca.music.make_zagged_pitch_classes import make_lilypond_file_from_output_material
        return make_lilypond_file_from_output_material(material)
