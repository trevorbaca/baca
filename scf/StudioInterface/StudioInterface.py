# -*- encoding: utf-8 -*-
from baca.scf.GlobalProxy import GlobalProxy
from baca.scf.DirectoryProxy import DirectoryProxy
from baca.scf.ScoreWrangler import ScoreWrangler
import os
import subprocess


class StudioInterface(DirectoryProxy):

    def __init__(self):
        directory = os.environ.get('BACA', 'works')
        DirectoryProxy.__init__(self, directory)
        self._baca_proxy = GlobalProxy()
        self._score_wrangler = ScoreWrangler()

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % self.class_name

    ### PUBLIC ATTRIBUTES ###

    @property
    def baca_proxy(self):
        return self._baca_proxy

#    @property
#    def maker_wrangler(self):
#        return self._maker_wrangler
#
#    @property
#    def material_wrangler(self):
#        return self._material_wrangler

    @property
    def score_wrangler(self):
        return self._score_wrangler

    ### PUBLIC METHODS ###

    def get_materials_package_importable_name_interactively(self, menu_header=None):
        import baca
        while True:
            menu = self.Menu(client=self.where(), menu_header=menu_header)
            menu.menu_body = 'select materials directory'
            menu_section = self.MenuSection()
            score_titles = self.score_wrangler.list_numbered_score_titles_with_years()
            menu_section.menu_section_entries = score_titles
            menu_section.sentence_length_items.append(('baca', 'baca materials directory'))
            menu.menu_sections.append(menu_section)
            key, value = menu.display_menu()
            if key == 'baca':
                return self.baca_proxy.materials_package_importable_name
            else:
                score_title = value
                score_package_importable_name = self.score_wrangler.score_title_to_score_package_short_name(
                    score_title)
                score_proxy = baca.scf.ScoreProxy(score_package_importable_name)
                return score_proxy.materials_package_importable_name

    def manage_svn(self, menu_header=None):
        while True:
            menu = self.Menu(client=self.where())
            menu.menu_header = menu_header
            menu.menu_body = 'repository commands'
            menu_section = self.MenuSection()
            menu_section.sentence_length_items.append(('add', 'svn add'))
            menu_section.sentence_length_items.append(('ci', 'svn commit'))
            menu_section.sentence_length_items.append(('st', 'svn status'))
            menu_section.sentence_length_items.append(('up', 'svn update'))
            menu_section.layout = 'line'
            menu.menu_sections.append(menu_section)
            menu_section = self.MenuSection()
            menu_section.sentence_length_items.append(('add scores', 'svn add (scores)'))
            menu_section.sentence_length_items.append(('ci scores', 'svn commit (scores)'))
            menu_section.sentence_length_items.append(('st scores', 'svn status (scores)'))
            menu_section.sentence_length_items.append(('up scores', 'svn update (scores)'))
            menu_section.layout = 'line'
            menu.menu_sections.append(menu_section)
            menu_section = self.MenuSection()
            menu_section.sentence_length_items.append(('pytest', 'run regression tests'))
            menu_section.sentence_length_items.append(('pytest scores', 'run regression tests (scores)'))
            menu_section.sentence_length_items.append(('pytest all', 'run regression tests (all)'))
            menu_section.layout = 'line'
            menu.menu_sections.append(menu_section)
            key, value = menu.display_menu()
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
            elif key == 'pytest':
                self.run_py_test()
            elif key == 'pytest scores':
                self.score_wrangler.run_py_test()
            elif key == 'pytest all':
                self.run_py_test_all()
            elif key == 'st':
                self.svn_st()
            elif key == 'st scores':
                self.score_wrangler.svn_st_scores()
            elif key == 'up':
                self.svn_up()
                break
            elif key == 'up scores':
                self.score_wrangler.svn_up_scores()
                break

    def run_py_test_all(self, prompt_proceed=True):
        proc = subprocess.Popen('py.test %s %s' % 
            (self.directory_name, self.score_wrangler.directory_name), 
            shell=True, stdout=subprocess.PIPE)
        lines = proc.stdout.readlines()
        if lines:
            print ''.join(lines)
        if prompt_proceed:
            self.proceed()
    
    def work_in_studio(self, menu_header=None):
        import baca
        while True:
            menu = self.Menu(client=self.where(), menu_header=menu_header)
            menu.menu_body = 'welcome to the studio.'
            menu_section = self.MenuSection()
            score_titles = self.score_wrangler.list_numbered_score_titles_with_years()
            menu_section.menu_section_entries = score_titles
            menu_section.sentence_length_items.append(('k', 'work with material makers'))
            menu_section.sentence_length_items.append(('m', 'work with Bača materials'))
            menu_section.hidden_items.append(('svn', 'work with repository'))
            menu.menu_sections.append(menu_section)
            menu.include_back = False
            menu.include_studio = False
            key, value = menu.display_menu()
            if key == 'k':
                self.baca_proxy.maker_wrangler.manage_makers(menu_header='studio')
            elif key == 'm':
                self.baca_proxy.material_wrangler.manage_materials(menu_header='studio')
            elif key == 'svn':
                self.manage_svn(menu_header='studio')
            else:
                score_title = value
                score_package_importable_name = self.score_wrangler.score_title_to_score_package_short_name(
                    score_title)
                score_proxy = baca.scf.ScoreProxy(score_package_importable_name)
                score_proxy.manage_score()
