from abjad.tools import pitchtools
from baca.scf.MaterialPackageMaker import MaterialPackageMaker
from make_illustration_from_output_material import make_illustration_from_output_material
from baca.scf.editors.PitchRangeInventoryEditor import PitchRangeInventoryEditor


class PitchRangeInventoryMaterialPackageMaker(MaterialPackageMaker):

    def __init__(self, package_importable_name=None, session=None):
        MaterialPackageMaker.__init__(self, 
            package_importable_name=package_importable_name, session=session)

    ### PUBLIC CLASS ATTRIBUTES ###

    generic_output_name = 'pitch range inventory'

    illustration_maker = staticmethod(make_illustration_from_output_material)

    output_material_checker = staticmethod(lambda x: isinstance(x, pitchtools.PitchRangeInventory))

    output_material_editor = PitchRangeInventoryEditor

    output_material_maker = pitchtools.PitchRangeInventory

    output_material_module_import_statements = [
        'from abjad.tools.pitchtools.PitchRange import PitchRange',
        'from abjad.tools.pitchtools.PitchRangeInventory import PitchRangeInventory',
        ]

    user_input_demo_values = [
        ('pitch_range_tokens', ['[A0, C8]', '[C3, F#5]']),
        ]

    user_input_module_import_statements = [
        'from baca.scf import UserInputWrapper',
        ]
