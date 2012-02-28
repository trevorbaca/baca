from scf.selectors.Selector import Selector


class TempoMarkSelector(Selector):

    ### CLASS ATTRIBUTES ###
    
    target_human_readable_name = 'tempo'

    ### PUBLIC METHODS ###

    def make_menu_tokens(self, head=None):
        from scf.proxies.ScorePackageProxy import ScorePackageProxy
        tokens = []
        if self.session.is_in_score:
            score_package_proxy = ScorePackageProxy(
                score_package_short_name=self.session.current_score_package_short_name,
                session=self.session)
            tempo_inventory = score_package_proxy.tempo_inventory
            if tempo_inventory:
                for tempo_mark in tempo_inventory:
                    tokens.append(self.change_expr_to_menu_token(tempo_mark))
            return tokens
