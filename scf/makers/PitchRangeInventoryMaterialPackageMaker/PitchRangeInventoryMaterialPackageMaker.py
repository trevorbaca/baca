from abjad.tools import pitchtools
from make_illustration_from_output_material import make_illustration_from_output_material
from scf.makers.MaterialPackageMaker import MaterialPackageMaker
from scf.editors.PitchRangeInventoryEditor import PitchRangeInventoryEditor


class PitchRangeInventoryMaterialPackageMaker(MaterialPackageMaker):

    ### CLASS ATTRIBUTES ###

    generic_output_name = 'pitch range inventory'
    illustration_maker = staticmethod(make_illustration_from_output_material)
    output_material_checker = staticmethod(lambda x: isinstance(x, pitchtools.PitchRangeInventory))
    output_material_editor = PitchRangeInventoryEditor
    output_material_maker = pitchtools.PitchRangeInventory
    output_material_module_import_statements = ['from abjad.tools import pitchtools' ]

    ### PUBLIC METHODS ###

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
