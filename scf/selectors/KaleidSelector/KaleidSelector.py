from scf.selectors.Selector import Selector
import os


class KaleidSelector(Selector):

    def __init__(self, session=None):
        Selector.__init__(self, session=session)

    ### CLASS ATTRIBUTES ###
    
    target_asset_container_path_names = [os.environ.get('KALEIDPATH')]
    target_human_readable_name = 'kaleid'

    ### PUBLIC METHODS ###

    def make_menu_tokens(self, head=None):
        from scf.proxies.PackageProxy import PackageProxy
        tokens = []
