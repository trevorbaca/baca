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

    def manage_svn(self, menu_header=None):
        while True:
            menu_specifier = MenuSpecifier()
            menu_specifier.menu_header = menu_header
            menu_specifier.menu_body = 'repository commands'
            menu_section = MenuSectionSpecifier()
            menu_section.sentence_length_items.append(('st', 'svn status'))
            menu_section.sentence_length_items.append(('add', 'svn add'))
            menu_section.sentence_length_items.append(('ci', 'svn commit'))
            menu_section.layout = 'line'
            menu_specifier.menu_sections.append(menu_section)
            menu_section = MenuSectionSpecifier()
            menu_section.sentence_length_items.append(('st scores', 'svn status (scores)'))
            menu_section.sentence_length_items.append(('add scores', 'svn add (scores)'))
            menu_section.sentence_length_items.append(('ci scores', 'svn commit (scores)'))
            menu_section.layout = 'line'
            menu_specifier.menu_sections.append(menu_section)
            key, value = menu_specifier.display_menu()
            if key == 'b':
                return key, None
            elif key == 'add':
                self.svn_add()
            elif key == 'add scores':
                self.catalog.svn_add_scores()
            elif key == 'ci':
                self.svn_ci()
            elif key == 'ci scores':
                self.catalog.svn_ci_scores()
            elif key == 'st':
                self.svn_st()
            elif key == 'st scores':
                self.catalog.svn_st_scores()

    def work_in_studio(self, menu_header=None):
        while True:
            menu_specifier = MenuSpecifier(menu_header=menu_header)
            menu_specifier.menu_body = 'welcome to the studio.'
            menu_section = MenuSectionSpecifier()
            menu_section.menu_section_entries = self.catalog.list_numbered_score_titles_with_years()
            menu_section.sentence_length_items.append(('m', 'materials'))
            menu_section.sentence_length_items.append(('svn', 'repository'))
            menu_specifier.menu_sections.append(menu_section)
            menu_specifier.include_back = False
            menu_specifier.include_studio = False
            key, value = menu_specifier.display_menu()
            if key == 'm':
                shared_materials_proxy = SharedMaterialsProxy()
                result = shared_materials_proxy.manage_shared_materials(menu_header='studio')
            elif key == 'svn':
                self.manage_svn()
            else:
                score_package_name = self.catalog.score_title_to_score_package_name(value)
                if score_package_name is not None:
                    score_package_proxy = ScorePackageProxy(score_package_name)
                    result = score_package_proxy.manage_score()
