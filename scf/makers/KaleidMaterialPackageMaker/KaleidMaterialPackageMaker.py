from make_illustration_from_output_material import make_illustration_from_output_material
from scf.editors.get_kaleid_editor import get_kaleid_editor
from scf.makers.MaterialPackageMaker import MaterialPackageMaker
from scf.wizards.TimeTokenMakerCreationWizard import TimeTokenMakerCreationWizard
from abjad.tools.timetokentools.TimeTokenMaker import TimeTokenMaker


class KaleidMaterialPackageMaker(MaterialPackageMaker):

    ### CLASS ATTRIBUTES ###

    generic_output_name = 'kaleid'
    illustration_maker = staticmethod(make_illustration_from_output_material)
    output_material_checker = staticmethod(lambda x: isinstance(x, _RhytmicKaleid))
    output_material_editor = staticmethod(get_kaleid_editor)
    output_material_maker = TimeTokenMakerCreationWizard
    output_material_module_import_statements = ['import handlers']
