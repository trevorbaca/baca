from abjad.tools import contexttools
from scf.makers.MaterialPackageMaker import MaterialPackageMaker
from make_illustration_from_output_material import make_illustration_from_output_material
from scf.editors.TempoMarkInventoryEditor import TempoMarkInventoryEditor


class TempoMarkInventoryMaterialPackageMaker(MaterialPackageMaker):

    def __init__(self, package_importable_name=None, session=None):
        MaterialPackageMaker.__init__(self,
            package_importable_name=package_importable_name, 
            session=session)

    ### CLASS ATTRIBUTES ###

    generic_output_name = 'tempo mark inventory'
    illustration_maker = staticmethod(make_illustration_from_output_material)
    output_material_checker = staticmethod(lambda x: isinstance(x, contexttools.TempoMarkInventory))
    output_material_editor = TempoMarkInventoryEditor
    output_material_maker = contexttools.TempoMarkInventory
    
    output_material_module_import_statements = [
        'from abjad.tools import contexttools',
        'from abjad.tools import durationtools',
        ]
            
    user_input_demo_values = [
        ('tempo_mark_tokens', [((1, 8), 72), ('Allegro', (1, 8), 84)]),
        ]

    # TODO: remove self.user_input_module_import_statements from editable maker
    user_input_module_import_statements = [
        'from scf.editors import UserInputWrapper',
        ]

    ### PUBLIC METHODS ###

    def make_output_material_module_body_lines(self, output_material):
        lines = []
        lines.append('{} = {}(['.format(
            self.material_underscored_name, output_material._class_name_with_tools_package))
        for item in output_material[:-1]:
            lines.append('\t{},'.format(item._repr_with_tools_package))
        item = output_material[-1]
        lines.append('\t{}])'.format(item._repr_with_tools_package))
        lines = [line + '\n' for line in lines]
        return lines
