from baca.scf.CatalogProxy import CatalogProxy
from baca.scf.SCFProxyObject import SCFProxyObject
from baca.scf.ScorePackageProxy import ScorePackageProxy
from baca.scf.SharedMaterialsProxy import SharedMaterialsProxy
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
        is_first_pass = True
        while True:
            is_redraw = False
            if is_first_pass:
                self.print_menu_title('Welcome to the studio.\n')
            score_titles_with_years = self.catalog.list_score_titles_with_years()
            kwargs = {}
            kwargs = {'values_to_number': score_titles_with_years, 'indent_level': 1}
            kwargs.update({'is_nearly': False, 'show_options': is_first_pass})
            named_pairs = [
                ('m', 'materials'),
                ]
            kwargs.update({'named_pairs': named_pairs})
            key, value = self.display_menu(**kwargs)
            result = None
            if key == 'b':
                break
            if key == 'm':
                shared_materials_proxy = SharedMaterialsProxy()
                result = shared_materials_proxy.manage_shared_materials()
                if result == 'b':
                    is_redraw = True
            elif key == 'q':
                raise SystemExit
            elif key == 'w':
                is_redraw = True
            elif key == 'x':
                self.exec_statement()
            else:
                score_package_name = self.catalog.score_title_to_score_package_name(value)
                if score_package_name is not None:
                    score_package_proxy = ScorePackageProxy(score_package_name)
                    result = score_package_proxy.manage_score()
            if is_redraw or result == 'b':
                is_first_pass = True
            else:
                is_first_pass = False
