from abjad.tools import pitchtools
from scf.makers.MaterialPackageMaker import MaterialPackageMaker
from make_illustration_from_output_material import make_illustration_from_output_material
from scf.editors.OctaveTranspositionMappingInventoryEditor import OctaveTranspositionMappingInventoryEditor


class OctaveTranspositionMappingInventoryMaterialPackageMaker(MaterialPackageMaker):

    ### CLASS ATTRIBUTES ###

    generic_output_name = 'octave transposition mapping inventory'
    illustration_maker = staticmethod(make_illustration_from_output_material)
    output_material_checker = staticmethod(lambda x: isinstance(x, 
        pitchtools.OctaveTranspositionMappingInventory))
    output_material_editor = OctaveTranspositionMappingInventoryEditor
    output_material_maker = pitchtools.OctaveTranspositionMappingInventory
    output_material_module_import_statements = ['from abjad.tools import pitchtools']

    ### PUBLIC METHODS ###

    # TODO: abstract up to InventoryMaterialPackageMaker
    def make_output_material_module_body_lines(self, output_material):
        lines = []
        lines = output_material._tools_package_qualified_repr_pieces
        lines[0] = '{} = {}'.format(self.material_underscored_name, lines[0])
        lines = [line + '\n' for line in lines]
        return lines
