from baca.scf.CatalogProxy import CatalogProxy
from baca.scf.SCFProxyObject import SCFProxyObject
import os


class StudioProxy(SCFProxyObject):

    def __init__(self):
        self.baca_directory = os.environ.get('BACA')

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % type(self).__name__

    ### PUBLIC ATTRIBUTES ###

    @property
    def catalog(self):
        return CatalogProxy()

    ### PUBLIC METHODS ###

    def work_in_studio(self):
        catalog = CatalogProxy()
        kwargs = {}
        kwargs.update({'values_to_number': catalog.list_score_package_names()})
        named_pairs = [
            ('m', 'materials'),
        ]
        kwargs.update({'named_pairs': named_pairs})
        key, value = self.display_menu(**kwargs)
        print key, value
