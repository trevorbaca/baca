from abjad.tools import mathtools
from baca.music.make_zagged_pitch_classes import make_illustration_from_output_material
from baca.music.make_zagged_pitch_classes import make_zagged_pitch_classes
from experimental.tools import musicexpressiontools
from scoremanager.materialpackagemanagers.FunctionInputMaterialPackageManager import \
    FunctionInputMaterialPackageManager


class ZaggedPitchClassMaterialPackageManager(FunctionInputMaterialPackageManager):

    ### CLASS ATTRIBUTES ###

    generic_output_name = 'zagged pitch-classes'
    illustration_maker = staticmethod(make_illustration_from_output_material)
    output_material_checker = staticmethod(lambda x: isinstance(x, musicexpressiontools.StatalServer))
    output_material_maker = staticmethod(make_zagged_pitch_classes)
    output_material_module_import_statements = [
        'from abjad.tools import datastructuretools',
        'from experimental.tools import musicexpressiontools',
        ]

    user_input_demo_values = [
        ('pc_cells', [[0, 7, 2, 10], [9, 6, 1, 8], [5, 4, 2, 11, 10, 9]]),
        ('division_cells', [[[1], [1], [1], [1, 1]], [[1], [1], [1], [1, 1, 1], [1, 1, 1]]]),
        ('grouping_counts', [1, 1, 2, 3]),
        ]

    user_input_tests = [
        ('pc_cells', list),
        ('division_cells', list),
        ('grouping_counts', mathtools.all_are_nonnegative_integers),
        ]
