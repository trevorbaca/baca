from scf.selectors.Selector import Selector


class TempoMarkSelector(Selector):

    ### CLASS ATTRIBUTES ###
    
    target_human_readable_name = 'tempo'

    ### READ / WRITE ATTRIBUTES ###

    @apply
    def items():
        def fget(self):
            if self._items:
                return self._items
            else:
                return self.current_score_tempo_marks
        def fset(self, items):
            self._items = list(items)
        return property(**locals())

    ### PUBLIC ATTRIBUTES ###

    @property
    def current_score_tempo_marks(self):
        result = []
        current_score_package_proxy = self.session.current_score_package_proxy
        try:
            result.extend(current_score_package_proxy.tempo_inventory)
        except AttributeError:
            pass
        return result
