from baca.scf.MakerWrangler import MakerWrangler
from baca.scf.MaterialWrangler import MaterialWrangler
from baca.scf.PackageProxy import PackageProxy


class GlobalProxy(PackageProxy):
    
    def __init__(self, session=None):
        PackageProxy.__init__(self, 'baca', session=session)
        self._maker_wrangler = MakerWrangler(session=self.session)
        self._material_wrangler = MaterialWrangler('baca', session=self.session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def is_score_local_purview(self):
        return False

    @property
    def is_studio_global_purview(self):
        return True

    @property
    def maker_wrangler(self):
        return self._maker_wrangler

    @property
    def material_wrangler(self):
        return self._material_wrangler
  
    @property
    def materials_package_importable_name(self):
        return 'baca.materials' 

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
