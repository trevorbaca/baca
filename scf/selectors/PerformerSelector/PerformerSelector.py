from scf.selectors.Selector import Selector


class PerformerSelector(Selector):

    def __init__(self, session=None):
        Selector.__init__(self, session=session)

    ### CLASS ATTRIBUTES ###

    target_human_readable_name = 'performer'

    ### PUBLIC METHODS ###

    def list_target_items(self):
        result = []
        current_score_package_proxy = self.session.current_score_package_proxy
        try:
            result.extend(current_score_package_proxy.instrumentation.performers)
        except AttributeError:
            pass
        return result
