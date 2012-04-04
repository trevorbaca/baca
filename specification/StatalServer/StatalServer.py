from abjad.tools.abctools.AbjadObject import AbjadObject


class StatalServer(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, cyclic_tree):
        self.cyclic_tree = cyclic_tree
        self.last_nodes = [cyclic_tree]

    ### SPECIAL METHODS ###

    def __call__(self, request):
        if request.complete:
            last_nodes = self.last_node.get_next_n_complete_nodes_at_level(request.n, request.level)
        else:
            last_nodes = self.last_node.get_next_n_nodes_at_level(request.n, request.level)
        self.last_nodes = last_nodes
        result = [node.payload for node in self.last_nodes]
        return result

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def last_node(self):
        return self.last_nodes[-1]
