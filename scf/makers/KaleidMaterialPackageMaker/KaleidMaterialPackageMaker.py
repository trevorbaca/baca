from make_illustration_from_output_material import make_illustration_from_output_material
from scf.makers.MaterialPackageMaker import MaterialPackageMaker
from scf.editors.UserInputWrapper import UserInputWrapper
from scf.editors.InteractiveEditor import InteractiveEditor
from baca.rhythm.kaleids._RhythmicKaleid import _RhythmicKaleid
import baca


class KaleidMaterialPackageMaker(MaterialPackageMaker):

    ### CLASS ATTRIBUTES ###

    generic_output_name = 'kaleid'
    illustration_maker = staticmethod(make_illustration_from_output_material)
    output_material_checker = staticmethod(lambda x: isinstance(x, _RhytmicKaleid))
    output_material_editor = 'need some way of picking kaleid editor'
    output_material_maker = 'need some type of wizard to choose kaleid type'

    output_material_module_import_statements = [
        'from baca.rhythm.kaleids import *',
        ]

    user_input_demo_values = [
        ]

    user_input_module_import_statements = [
        ]
