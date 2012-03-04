from abc import ABCMeta
from scf.makers.MaterialPackageMaker import MaterialPackageMaker


class InventoryMaterialPackageMaker(MaterialPackageMaker):
    
    ### CLASS ATRIBUTES ###

    __metaclass__ = ABCMeta

    ### PUBLIC METHODS ###

    def make_output_material_module_body_lines(self, output_material):
        lines = []
        lines = output_material._tools_package_qualified_repr_pieces
        lines[0] = '{} = {}'.format(self.material_underscored_name, lines[0])
        lines = [line + '\n' for line in lines]
        return lines
