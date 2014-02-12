from experimental.tools import scoremanager
from experimental.tools.scoremanager.editors.ListEditor import ListEditor


class ConstellationCircuitSelectionEditor(ListEditor):

    ### CLASS ATTRIBUTES ###

    item_getter_configuration_method = \
        scoremanager.iotools.UserInputGetter.append_constellation_circuit_id_pair

    item_identifier = 'constellation circuit id pair'
