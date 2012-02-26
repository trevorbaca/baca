from scf.selectors.Selector import Selector


class PerformerSelector(Selector):

    def __init__(self, session=None):
        Selector.__init__(self, session=session)

    ### CLASS ATTRIBUTES ###

    target_human_readable_name = 'performer'

    ### PUBLIC METHODS ###

    def make_menu_tokens(self, head=None):
        from scf.proxies.ScorePackageProxy import ScorePackageProxy
        tokens = []
        if self.session.is_in_score:
            score_package_proxy = ScorePackageProxy(
                score_package_short_name=self.session.current_score_package_short_name,
                session=self.session)
            instrumentation = score_package_proxy.instrumentation
            if instrumentation:
                for performer in instrumentation.performers:
                    token = (repr(performer), repr(performer), performer)
                    tokens.append(token)
        return tokens
