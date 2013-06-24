from make_illustration_from_output_material import make_illustration_from_output_material
from baca.score_manager.editors.ConstellationCircuitSelectionEditor import \
    ConstellationCircuitSelectionEditor
from experimental.tools.scoremanagertools.materialpackagemakers.MaterialPackageMaker import \
    MaterialPackageMaker


class ConstellationCircuitSelectionMaterialPackageMaker(MaterialPackageMaker):

    ### CLASS ATTRIBUTES ###

    generic_output_name = 'constellation circuit selection'
    illustration_maker = staticmethod(make_illustration_from_output_material)
    output_material_checker = staticmethod(lambda x: isinstance(x, list))
    output_material_editor = ConstellationCircuitSelectionEditor

    ### PUBLIC METHODS ###

    def run_first_time(self):
        self._session.is_autoadding = True
        self._run(pending_user_input='omi')
        self._session.is_autoadding = False
