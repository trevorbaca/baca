from scf.editors.ListEditor import ListEditor


class ConstellationCircuitSelectionEditor(ListEditor):

    ### CLASS ATTRIBUTES ###

    target_item_class = tuple
    target_item_getter_configuration_method = None # baca.menuing.append_constellation_circuit_id_pair
    target_item_identifier = 'constellation circuit id pair'
