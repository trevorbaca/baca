from scf.selectors.Selector import Selector


class PerformerSelector(Selector):

    def __init__(self, session=None):
        Selector.__init__(self, session=session)

    ### CLASS ATTRIBUTES ###

    target_human_readable_name = 'performer'

    ### READ-ONLY ATTRIBUTES ###

    @property
    def current_score_performers(self):
        result = []
        current_score_package_proxy = self.session.current_score_package_proxy
        try:
            result.extend(current_score_package_proxy.instrumentation.performers)
        except AttributeError:
            pass
        return result

    ### READ / WRITE ATTRIBUTES ###

    @apply
    def items():
        def fget(self):
            if self._items:
                return self._items
            else:
                return self.current_score_performers
        def fset(self, items):
            self._items = list(items)
        return property(**locals())
