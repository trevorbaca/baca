from scf.editors.ListEditor import ListEditor


class ConstellationCircuitSelectionEditor(ListEditor):

    ### CLASS ATTRIBUTES ###

    item_class = tuple
    item_getter_configuration_method = None # baca.menuing.append_constellation_circuit_id_pair
    item_identifier = 'constellation circuit id pair'
