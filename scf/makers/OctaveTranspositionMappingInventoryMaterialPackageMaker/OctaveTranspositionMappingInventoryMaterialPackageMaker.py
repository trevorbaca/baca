from abjad.tools import pitchtools
from scf.makers.MaterialPackageMaker import MaterialPackageMaker
from make_illustration_from_output_material import make_illustration_from_output_material
from scf.editors.OctaveTranspositionMappingInventoryEditor import OctaveTranspositionMappingInventoryEditor


class OctaveTranspositionMappingInventoryMaterialPackageMaker(object):

    ### CLASS ATTRIBUTES ###

    generic_output_name = 'octave transposition mapping inventory'
    illustration_maker = staticmethod(make_illustration_from_output_material)
    output_material_checker = staticmethod(lambda x: isinstance(x, pitchtools.OctaveTranspositionMappingInventory))
    output_material_editor = OctaveTranspositionMappingInventoryEditor
    output_material_maker = pitchtools.OctaveTranspositionMappingInventory
    output_material_module_import_statements = ['from abjad.tools import pitchtools']

    ### PUBLIC METHODS ###

    # TODO: abstract up to InventoryMaterialPackageMaker
    def make_output_material_module_body_lines(self, output_material):
        lines = []
        lines.append('{} = {}(['.format(
            self.material_underscored_name, output_material._class_name_with_tools_package))
        for item in output_material[:-1]:
            lines.append('\t{},'.format(self.get_repr_with_tools_package(item)))
        item = output_material[-1]
        lines.append('\t{}])'.format(self.get_repr_with_tools_package(item)))
        lines = [line + '\n' for line in lines]
        return lines
