from experimental.tools import scoremanagementtools
from experimental.tools.scoremanagementtools.editors.ListEditor import ListEditor


class ConstellationCircuitSelectionEditor(ListEditor):

    ### CLASS ATTRIBUTES ###

    item_getter_configuration_method = scoremanagementtools.menuing.UserInputGetter.append_constellation_circuit_id_pair
    item_identifier = 'constellation circuit id pair'
