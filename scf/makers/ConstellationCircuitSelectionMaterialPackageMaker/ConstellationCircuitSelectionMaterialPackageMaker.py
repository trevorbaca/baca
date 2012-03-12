from make_illustration_from_output_material import make_illustration_from_output_material
from scf.makers.MaterialPackageMaker import MaterialPackageMaker


class ConstellationCircuitSelectionMaterialPackageMaker(MaterialPackageMaker):

    ### CLASS ATTRIBUTES ###

    generic_output_name = 'constellation circuit selection'
    illustration_maker = staticmethod(make_illustration_from_output_material)
    output_material_checker = staticmethod(lambda x: isinstance(x, list))
