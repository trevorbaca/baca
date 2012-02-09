from abjad.tools import pitchtools
from baca.scf.MaterialPackageMaker import MaterialPackageMaker
from make_illustration_from_output_material import make_illustration_from_output_material
import baca


class PitchRangeInventoryMaterialPackageMaker(MaterialPackageMaker):

    ### PUBLIC CLASS ATTRIBUTES ###

    generic_output_name = 'pitch range inventory'

    illustration_maker = staticmethod(make_illustration_from_output_material)

    output_material_checker = staticmethod(lambda x: isinstance(x, pitchtools.PitchRangeInventory))

    output_material_maker = pitchtools.PitchRangeInventory # staticmethod? or directly callable?

    output_material_module_import_statements = [
        'from abjad.tools.pitchtools.PitchRangeInventory import PitchRangeInventory',
        ]
