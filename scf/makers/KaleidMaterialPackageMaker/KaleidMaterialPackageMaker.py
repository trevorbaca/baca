from make_illustration_from_output_material import make_illustration_from_output_material
from scf.editors.get_kaleid_editor import get_kaleid_editor
from scf.makers.MaterialPackageMaker import MaterialPackageMaker
from scf.wizards.KaleidCreationWizard import KaleidCreationWizard
from kaleids._RhythmicKaleid import _RhythmicKaleid


class KaleidMaterialPackageMaker(MaterialPackageMaker):

    ### CLASS ATTRIBUTES ###

    generic_output_name = 'kaleid'
    illustration_maker = staticmethod(make_illustration_from_output_material)
    output_material_checker = staticmethod(lambda x: isinstance(x, _RhytmicKaleid))
    output_material_creation_wizard = KaleidCreationWizard
    output_material_editor = staticmethod(get_kaleid_editor)
    output_material_module_import_statements = ['import kaleids']

    ### PUBLIC METHODS ###

    def make_output_material_module_body_lines(self, output_material):
        lines = []
        formatted_input_parameters = output_material._formatted_input_parameters
        if formatted_input_parameters:
            lines.append('{} = {}('.format(
                self.material_underscored_name, output_material._class_name_with_tools_package))
            for item in output_material._formatted_input_parameters[:-1]:
                lines.append('\t{},'.format(item))
            item = output_material._formatted_input_parameters[-1]
            lines.append('\t{})'.format(item))
        else:
            lines.append('{} = {}()'.format(
                self.material_underscored_name, output_material._class_name_with_tools_package))
        lines = [line + '\n' for line in lines]
        return lines
