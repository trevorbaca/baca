from abjad.tools import sequencetools
from baca.music.make_zagged_pitch_classes import make_illustration_from_output_material
from baca.scf.MaterialPackageMaker import MaterialPackageMaker
from baca.scf.UserInputWrapper import UserInputWrapper
from baca.scf.editors.InteractiveEditor import InteractiveEditor
import baca


class ZaggedPitchClassMaterialPackageMaker(MaterialPackageMaker):

    def __init__(self, package_importable_name=None, session=None):
        MaterialPackageMaker.__init__(
            self, package_importable_name=package_importable_name, session=session)

    ### PUBLIC CLASS ATTRIBUTES ###

    generic_output_name = 'zagged pitch-classes'

    illustration_maker = staticmethod(make_illustration_from_output_material)

    output_material_checker = staticmethod(lambda x: isinstance(x, sequencetools.CyclicTree))

    output_material_maker = staticmethod(baca.music.make_zagged_pitch_classes)

    output_material_module_import_statements = [
        'from abjad.tools.sequencetools.CyclicTree import CyclicTree',]

    user_input_demo_values = [
        ('pc_cells', [[0, 7, 2, 10], [9, 6, 1, 8], [5, 4, 2, 11, 10, 9]]),
        ('division_cells', [[[1], [1], [1], [1, 1]], [[1], [1], [1], [1, 1, 1], [1, 1, 1]]]),
        ('grouping_counts', [1, 1, 2, 3]),
        ]

    user_input_module_import_statements = [
        'from baca.scf.materialpackagemakers import ZaggedPitchClassMaterialPackageMaker',
        'from baca.scf import UserInputWrapper',
        ]

    user_input_tests = [
        ('pc_cells', list),
        ('division_cells', list),
        ('grouping_counts', sequencetools.all_are_nonnegative_integers),
        ]
