from baca.scf.MaterialProxyWrangler import MaterialProxyWrangler
from baca.scf.MaterialWrangler import MaterialWrangler
from baca.scf.PackageProxy import PackageProxy


class GlobalProxy(PackageProxy):
    
    def __init__(self, session=None):
        PackageProxy.__init__(self, self.studio_package_importable_name, session=session)
        self._material_proxy_wrangler = MaterialProxyWrangler(session=self.session)
        self._material_wrangler = MaterialWrangler(session=self.session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def is_score_local_purview(self):
        return False

    @property
    def is_studio_global_purview(self):
        return True

    @property
    def material_proxy_wrangler(self):
        return self._material_proxy_wrangler

    @property
    def material_wrangler(self):
        return self._material_wrangler
  
    @property
    def materials_package_importable_name(self):
        return self.studio_materials_package_importable_name

    ### PUBLIC METHODS ###

    # TODO: write test
    def import_attribute_from_initializer(self, attribute_name):
        try:
            command = 'from {} import {}'.format(self.package_importable_name, attribute_name)
            exec(command)
            command = 'result = {}'.format(attribute_name)
            exec(command)
            return result
        except ImportError:
            return None
