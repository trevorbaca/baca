from baca.scf.CatalogProxy import CatalogProxy
from baca.scf.MenuSectionSpecifier import MenuSectionSpecifier
from baca.scf.MenuSpecifier import MenuSpecifier
from baca.scf.DirectoryProxy import DirectoryProxy
from baca.scf.ScorePackageProxy import ScorePackageProxy
from baca.scf.SharedMaterialsProxy import SharedMaterialsProxy
import os


class StudioProxy(DirectoryProxy):

    def __init__(self):
        directory = os.environ.get('BACA', 'works')
        DirectoryProxy.__init__(self, directory)

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % type(self).__name__

    ### PUBLIC ATTRIBUTES ###

    @property
    def catalog(self):
        return CatalogProxy()

    ### PUBLIC METHODS ###

    def work_in_studio(self):
        while True:
            menu_specifier = MenuSpecifier()
            menu_specifier.menu_title = 'Welcome to the studio.'
            menu_section = MenuSectionSpecifier()
            menu_section.menu_section_entries = self.catalog.list_numbered_score_titles_with_years()
            menu_section.sentence_length_items.append(('m', 'materials'))
            menu_specifier.menu_sections.append(menu_section)
            menu_section = MenuSectionSpecifier()
            menu_section.sentence_length_items.append(('st', 'svn st studio'))
            menu_section.sentence_length_items.append(('cm', 'svn commit studio'))
            menu_specifier.menu_sections.append(menu_section)
            menu_section = MenuSectionSpecifier()
            menu_section.sentence_length_items.append(('all-st', 'svn st scores'))
            menu_section.sentence_length_items.append(('all-cm', 'svn commit scores'))
            menu_specifier.menu_sections.append(menu_section)
            menu_specifier.include_back = False
            menu_specifier.include_studio = False
            key, value = menu_specifier.display_menu()
            if key == 'all-cm':
                self.catalog.svn_cm_scores()
            elif key == 'all-st':
                self.catalog.svn_st_scores()
            elif key == 'cm':
                self.svn_cm()
            elif key == 'm':
                shared_materials_proxy = SharedMaterialsProxy(score_title='Materials')
                result = shared_materials_proxy.manage_shared_materials()
            elif key == 'st':
                self.svn_st()
            else:
                score_package_name = self.catalog.score_title_to_score_package_name(value)
                if score_package_name is not None:
                    score_package_proxy = ScorePackageProxy(score_package_name)
                    result = score_package_proxy.manage_score()
