from make_illustration_from_output_material import make_illustration_from_output_material
from scf.makers.MaterialPackageMaker import MaterialPackageMaker
from scf.editors.UserInputWrapper import UserInputWrapper
from scf.editors.InteractiveEditor import InteractiveEditor
from scf.wizards.KaleidWizard import KaleidWizard
from baca.rhythm.kaleids._RhythmicKaleid import _RhythmicKaleid
import baca


class KaleidMaterialPackageMaker(MaterialPackageMaker):

    ### CLASS ATTRIBUTES ###

    generic_output_name = 'kaleid'
    illustration_maker = staticmethod(make_illustration_from_output_material)
    output_material_checker = staticmethod(lambda x: isinstance(x, _RhytmicKaleid))
    output_material_editor = KaleidWizard
    output_material_maker = KaleidWizard

    output_material_module_import_statements = [
        'from baca.rhythm.kaleids import *',
        ]

    user_input_demo_values = [
        ]

    # TODO: possibly remove?
    user_input_module_import_statements = [
        'from scf.editors.UserInputWrapper import UserInputWrapper',
        ]
