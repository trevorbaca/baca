from baca.scf.ScorePackageWrangler import ScorePackageWrangler
from baca.scf.MakerWrangler import MakerWrangler
from baca.scf.MenuSection import MenuSection
from baca.scf.MenuSpecifier import MenuSpecifier
from baca.scf.DirectoryProxy import DirectoryProxy
from baca.scf.ScorePackageProxy import ScorePackageProxy
from baca.scf.MaterialPackageWrangler import MaterialPackageWrangler
import os


class StudioInterface(DirectoryProxy):

    def __init__(self):
        directory = os.environ.get('BACA', 'works')
        DirectoryProxy.__init__(self, directory)

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % type(self).__name__

    ### PUBLIC ATTRIBUTES ###

    @property
    def score_package_wrangler(self):
        return ScorePackageWrangler()

    ### PUBLIC METHODS ###

    def manage_svn(self, menu_header=None):
        while True:
            menu_specifier = MenuSpecifier()
            menu_specifier.menu_header = menu_header
            menu_specifier.menu_body = 'repository commands'
            menu_section = MenuSection()
            menu_section.sentence_length_items.append(('st', 'svn status'))
            menu_section.sentence_length_items.append(('add', 'svn add'))
            menu_section.sentence_length_items.append(('ci', 'svn commit'))
            menu_section.layout = 'line'
            menu_specifier.menu_sections.append(menu_section)
            menu_section = MenuSection()
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
                self.score_package_wrangler.svn_add_scores()
            elif key == 'ci':
                self.svn_ci()
            elif key == 'ci scores':
                self.score_package_wrangler.svn_ci_scores()
            elif key == 'st':
                self.svn_st()
            elif key == 'st scores':
                self.score_package_wrangler.svn_st_scores()

    def work_in_studio(self, menu_header=None):
        while True:
            menu_specifier = MenuSpecifier(menu_header=menu_header)
            menu_specifier.menu_body = 'welcome to the studio.'
            menu_section = MenuSection()
            score_titles = self.score_package_wrangler.list_numbered_score_titles_with_years()
            print score_titles
            menu_section.menu_section_entries = score_titles
            menu_section.sentence_length_items.append(('min', 'work with interactive materials'))
            menu_section.sentence_length_items.append(('mst', 'work with static materials'))
            menu_section.sentence_length_items.append(('svn', 'work with repository'))
            menu_specifier.menu_sections.append(menu_section)
            menu_specifier.include_back = False
            menu_specifier.include_studio = False
            key, value = menu_specifier.display_menu()
            if key == 'min':
                makers_proxy = MakerWrangler()
                makers_proxy.manage_makers(menu_header='studio')
            elif key == 'mst':
                shared_materials_proxy = MaterialPackageWrangler()
                shared_materials_proxy.manage_shared_materials(menu_header='studio')
            elif key == 'svn':
                self.manage_svn(menu_header='studio')
            else:
                score_title = value
                print score_title
                score_package_name = self.score_package_wrangler.score_title_to_score_package_name(score_title)
                score_package_proxy = ScorePackageProxy(score_package_name)
                score_package_proxy.manage_score()
