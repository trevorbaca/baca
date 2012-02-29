from scf.selectors.Selector import Selector
import os


class DirectoryContentSelector(Selector):

    ### CLASS ATTRIBUTES ###

    asset_container_path_names = []
    target_human_readable_name = 'file'

    ### READ / WRITE ATTRIBUTES ###

    @apply
    def items():
        def fget(self):
            if self._items:
                return self._items
            else:
                return self.list_public_asset_short_names()
        def fset(self, items):
            self._items = list(items)
        return property(**locals())

    ### PUBLIC METHODS ###

    def list_public_asset_short_names(self):
        from scf.proxies.DirectoryProxy import DirectoryProxy
        result = []
        for path_name in self.asset_container_path_names:
            directory_proxy = DirectoryProxy(path_name=path_name, session=self.session)
            result.extend(directory_proxy.public_content_short_names)
        return result
