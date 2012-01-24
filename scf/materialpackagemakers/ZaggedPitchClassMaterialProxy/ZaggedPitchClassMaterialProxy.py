from abjad.tools import sequencetools
from baca.music.make_zagged_pitch_classes import make_illustration_from_output_material
from baca.scf.UserInputHandlingMaterialPackageProxy import UserInputHandlingMaterialPackageProxy
from baca.scf.UserInputWrapper import UserInputWrapper
from baca.scf.editors.InteractiveEditor import InteractiveEditor
import baca


class ZaggedPitchClassMaterialPackageProxy(UserInputHandlingMaterialPackageProxy):

    def __init__(self, package_importable_name=None, session=None):
        UserInputHandlingMaterialPackageProxy.__init__(
            self, package_importable_name=package_importable_name, session=session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    generic_output_name = 'zagged pitch-classes'

    illustration_maker = make_illustration_from_output_material

    # TODO: implement baca.pitchtools.is_cyclic_pitch_class_tree
    output_material_checker = lambda x: True

    output_material_maker = baca.music.make_zagged_pitch_classes

    output_material_module_import_statements = [
        'from abjad.tools.sequencetools.CyclicTree import CyclicTree',]

    user_input_demo_values = UserInputWrapper([
        ('pc_cells', [[0, 7, 2, 10], [9, 6, 1, 8], [5, 4, 2, 11, 10, 9]]),
        ('division_cells', [[[1], [1], [1], [1, 1]], [[1], [1], [1], [1, 1, 1], [1, 1, 1]]]),
        ('grouping_counts', [1, 1, 2, 3]),])

    user_input_module_import_statements = [
        'from baca.scf.materialpackagemakers import ZaggedPitchClassMaterialPackageProxy',
        'from baca.scf import UserInputWrapper',]

    # TODO: implement pitchtools.are_pitch_class_tokens()
    # TODO: implement sequencetools.all_are_nonnegative_integers(depth=n) keyword
    user_input_tests = [
        ('pc_cells', list),
        ('division_cells', list),
        ('grouping_counts', sequencetools.all_are_nonnegative_integers),]
