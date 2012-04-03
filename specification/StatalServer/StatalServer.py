# TODO: write tests
class StatalServer(object):

    ### INITIALIZER ###

    def __init__(self, cyclic_tree):
        self.cyclic_tree = cyclic_tree
        self.last_result = cyclic_tree

    ### SPECIAL METHODS ###

    def __call__(self, request):
        if request.complete:
            result = self.last_result.get_next_n_complete_nodes_at_level(
                request.n, request.level)
        else:
            result = self.last_result.get_next_n_nodes_at_level(
                request.n, request.level)
        self.last_result = result
        return result
