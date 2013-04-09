from scftools import menuing
from scftools.editors.ListEditor import ListEditor


class ConstellationCircuitSelectionEditor(ListEditor):

    ### CLASS ATTRIBUTES ###

    item_getter_configuration_method = menuing.UserInputGetter.append_constellation_circuit_id_pair
    item_identifier = 'constellation circuit id pair'
