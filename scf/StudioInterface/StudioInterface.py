from baca.scf.DirectoryProxy import DirectoryProxy
from baca.scf.MakerWrangler import MakerWrangler
from baca.scf.MaterialWrangler import MaterialWrangler
from baca.scf.ScoreProxy import ScoreProxy
from baca.scf.ScoreWrangler import ScoreWrangler
from baca.scf.menuing import MenuSection
from baca.scf.menuing import Menu
import os


class StudioInterface(DirectoryProxy):

    def __init__(self):
        directory = os.environ.get('BACA', 'works')
        DirectoryProxy.__init__(self, directory)
        self._maker_wrangler = MakerWrangler()
        self._material_wrangler = MaterialWrangler(purview=self)
        self._score_wrangler = ScoreWrangler()

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % self.class_name

    ### PUBLIC ATTRIBUTES ###

    @property
    def maker_wrangler(self):
        return self._maker_wrangler

    @property
    def material_wrangler(self):
        return self._material_wrangler

    @property
    def score_wrangler(self):
        return self._score_wrangler

    ### PUBLIC METHODS ###

    def get_materials_package_importable_name_interactively(self, menu_header=None):
        while True:
            menu_specifier = Menu(client=self, menu_header=menu_header)
            menu_specifier.menu_body = 'select materials directory'
            menu_section = MenuSection()
            score_titles = self.score_wrangler.list_numbered_score_titles_with_years()
            menu_section.menu_section_entries = score_titles
            menu_section.sentence_length_items.append(('baca', 'baca materials directory'))
            menu_specifier.menu_sections.append(menu_section)
            key, value = menu_specifier.display_menu()
            if key == 'baca':
                return self.baca_materials_package_importable_name
            else:
                score_title = value
                score_package_importable_name = self.score_wrangler.score_title_to_score_package_importable_name(
                    score_title)
                score_proxy = ScoreProxy(score_package_importable_name)
                return score_proxy.materials_package_importable_name

    def manage_svn(self, menu_header=None):
        while True:
            menu_specifier = Menu(client=self)
            menu_specifier.menu_header = menu_header
            menu_specifier.menu_body = 'repository commands'
            menu_section = MenuSection()
            menu_section.sentence_length_items.append(('add', 'svn add'))
            menu_section.sentence_length_items.append(('ci', 'svn commit'))
            menu_section.sentence_length_items.append(('st', 'svn status'))
            menu_section.sentence_length_items.append(('up', 'svn update'))
            menu_section.layout = 'line'
            menu_specifier.menu_sections.append(menu_section)
            menu_section = MenuSection()
            menu_section.sentence_length_items.append(('add scores', 'svn add (scores)'))
            menu_section.sentence_length_items.append(('ci scores', 'svn commit (scores)'))
            menu_section.sentence_length_items.append(('st scores', 'svn status (scores)'))
            menu_section.sentence_length_items.append(('up scores', 'svn update (scores)'))
            menu_section.layout = 'line'
            menu_specifier.menu_sections.append(menu_section)
            key, value = menu_specifier.display_menu()
            if key == 'b':
                return key, None
            elif key == 'add':
                self.svn_add()
            elif key == 'add scores':
                self.score_wrangler.svn_add_scores()
            elif key == 'ci':
                self.svn_ci()
                break
            elif key == 'ci scores':
                self.score_wrangler.svn_ci_scores()
            elif key == 'st':
                self.svn_st()
            elif key == 'st scores':
                self.score_wrangler.svn_st_scores()
            elif key == 'up':
                self.svn_up()
            elif key == 'up scores':
                self.score_wrangler.svn_up_scores()

    def work_in_studio(self, menu_header=None):
        while True:
            menu_specifier = Menu(client=self, menu_header=menu_header)
            menu_specifier.menu_body = 'welcome to the studio.'
            menu_section = MenuSection()
            score_titles = self.score_wrangler.list_numbered_score_titles_with_years()
            menu_section.menu_section_entries = score_titles
            menu_section.sentence_length_items.append(('makers', 'work with material makers'))
            menu_section.sentence_length_items.append(('shared', 'work with shared materials'))
            menu_section.hidden_items.append(('svn', 'work with repository'))
            menu_specifier.menu_sections.append(menu_section)
            menu_specifier.include_back = False
            menu_specifier.include_studio = False
            key, value = menu_specifier.display_menu()
            if key == 'makers':
                self.maker_wrangler.manage_makers(menu_header='studio')
            elif key == 'shared':
                self.material_wrangler.manage_shared_materials(menu_header='studio')
            elif key == 'svn':
                self.manage_svn(menu_header='studio')
            else:
                score_title = value
                score_package_importable_name = self.score_wrangler.score_title_to_score_package_short_name(
                    score_title)
                score_proxy = ScoreProxy(score_package_importable_name)
                score_proxy.manage_score()
