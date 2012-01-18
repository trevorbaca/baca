from abjad.tools import sequencetools
from baca.music.make_zagged_pitch_classes import make_lilypond_file_from_output_material
from baca.scf.UserInputHandlingMaterialProxy import UserInputHandlingMaterialProxy
from baca.scf.UserInputWrapper import UserInputWrapper
from baca.scf.editors.InteractiveEditor import InteractiveEditor
import baca


class ZaggedPitchClassMaterialProxy(UserInputHandlingMaterialProxy):

    def __init__(self, package_importable_name=None, session=None):
        UserInputHandlingMaterialProxy.__init__(
            self, package_importable_name=package_importable_name, session=session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    generic_output_name = 'zagged pitch-classes'

    lilypond_file_make = make_lilypond_file_from_output_material

    # TODO: implement baca.pitchtools.is_cyclic_pitch_class_tree
    output_data_checker = lambda x: True

    output_data_maker = baca.music.make_zagged_pitch_classes

    output_data_module_import_statements = [
        'from abjad.tools.sequencetools.CyclicTree import CyclicTree',]

    user_input_demo_values = UserInputWrapper([
        ('pc_cells', [[0, 7, 2, 10], [9, 6, 1, 8], [5, 4, 2, 11, 10, 9]]),
        ('division_cells', [[[1], [1], [1], [1, 1]], [[1], [1], [1], [1, 1, 1], [1, 1, 1]]]),
        ('grouping_counts', [1, 1, 2, 3]),])

    user_input_module_import_statements = [
        'from baca.scf.materialproxies import ZaggedPitchClassMaterialProxy',
        'from baca.scf import UserInputWrapper',]

    # TODO: implement pitchtools.are_pitch_class_tokens()
    # TODO: implement sequencetools.all_are_nonnegative_integers(depth=n) keyword
    user_input_tests = [
        ('pc_cells', list),
        ('division_cells', list),
        ('grouping_counts', sequencetools.all_are_nonnegative_integers),]

    ### PUBLIC METHODS ###

    # TODO: MaterialProxy.make_output_data_module_body_lines() should do
    #def make_output_data_module_body_lines(self):
    #    lines = []
    #    output_data = self.make_output_data()
    #    lines.append('{} = {!r}'.format(self.material_underscored_name, output_data))
    #    return lines
