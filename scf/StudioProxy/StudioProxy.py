from baca.scf.CatalogProxy import CatalogProxy
from baca.scf.MenuSpecifier import MenuSpecifier
from baca.scf.DirectoryProxy import DirectoryProxy
from baca.scf.ScorePackageProxy import ScorePackageProxy
from baca.scf.SharedMaterialsProxy import SharedMaterialsProxy
import os


class StudioProxy(DirectoryProxy):

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
            menu_specifier = MenuSpecifier()
            menu_specifier.menu_title = 'Welcome to the studio'
            menu_specifier.items_to_number = self.catalog.list_score_titles_with_years()
            menu_specifier.sentence_length_items = [
                ('m', 'manage shared materials'),
                ]
            menu_specifier.include_back = False
            menu_specifier.indent_level = 1
            key, value = menu_specifier.display_menu()
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
