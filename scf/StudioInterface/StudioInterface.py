# -*- encoding: utf-8 -*-
from baca.scf.SCFObject import SCFObject
from baca.scf.GlobalProxy import GlobalProxy
from baca.scf.ScoreWrangler import ScoreWrangler
import subprocess


class StudioInterface(SCFObject):

    def __init__(self, session=None):
        SCFObject.__init__(self, session=session)
        self._global_proxy = GlobalProxy(session=session)
        self._score_wrangler = ScoreWrangler(session=session)

    ### PUBLIC ATTRIBUTES ###

    @property
    def global_proxy(self):
        return self._global_proxy

    @property
    def score_wrangler(self):
        return self._score_wrangler

    ### PUBLIC METHODS ###

    def get_materials_package_importable_name_interactively(self):
        self.session.menu_pieces.append('select materials directory')
        while True:
            menu = self.Menu(where=self.where(), session=self.session)
            menu_section = self.MenuSection()
            menu_section.items_to_number = self.score_wrangler.iterate_score_titles_with_years()
            menu_section.sentence_length_items.append(('baca', 'baca materials directory'))
            menu.menu_sections.append(menu_section)
            key, value = menu.run()
            if key == 'baca':
                return self.global_proxy.materials_package_importable_name
            else:
                score_title = value
                score_package_importable_name = self.score_wrangler.title_to_score_package_short_name(
                    score_title)
                score_proxy = self.score_wrangler.ScoreProxy(
                    score_package_importable_name, session=self.session)
                return score_proxy.materials_package_importable_name
        self.session.menu_pieces.pop()

    def handle_main_menu_response(self, key, value):
        if key is None:
            pass
        elif key == 'active':
            self.session.scores_to_show = 'active'
        elif key == 'all':
            self.session.scores_to_show = 'all'
        elif key == 'k':
            self.global_proxy.maker_wrangler.manage_makers()
        elif key == 'm':
            self.global_proxy.material_wrangler.manage_materials()
        elif key == 'mb':
            self.session.scores_to_show = 'mothballed'
        elif key == 'some':
            self.session.hide_mothballed_scores = True
        elif key == 'svn':
            self.manage_svn()
        else:
            score_package_importable_name = value
            score_proxy = self.score_wrangler.ScoreProxy(
                score_package_importable_name, session=self.session)
            menu_pieces = self.session.menu_pieces[:]
            self.session.menu_pieces = []
            score_proxy.manage_score()
            self.session.menu_pieces = menu_pieces
    
    def handle_svn_response(self, key, value):
        if key == 'b':
            value = None
            return True
        elif key == 'add':
            self.global_proxy.svn_add()
        elif key == 'add scores':
            self.score_wrangler.svn_add()
        elif key == 'ci':
            self.global_proxy.svn_ci()
            return True
        elif key == 'ci scores':
            self.score_wrangler.svn_ci()
        elif key == 'pytest':
            self.global_proxy.run_py_test()
        elif key == 'pytest scores':
            self.score_wrangler.run_py_test()
        elif key == 'pytest all':
            self.run_py_test_all()
        elif key == 'st':
            self.global_proxy.svn_st()
        elif key == 'st scores':
            self.score_wrangler.svn_st()
        elif key == 'up':
            self.global_proxy.svn_up()
            return True
        elif key == 'up scores':
            self.score_wrangler.svn_up()
            return True

    def iterate_interactive_material_proxies(self):
        for material_proxy in self.iterate_material_proxies():
            if material_proxy.is_interactive:
                yield material_proxy

    def iterate_material_proxies(self, class_names=None):
        for score_proxy in self.iterate_score_proxies():
            for material_proxy in score_proxy.iterate_material_proxies():
                if class_names is None or material_proxy.get_tag('maker') in class_names:
                    yield material_proxy
        for material_proxy in self.global_proxy.material_wrangler.iterate_package_proxies():
            yield material_proxy

    def make_main_menu(self):
        menu = self.Menu(where=self.where(), session=self.session)
        menu_section = self.MenuSection()
        menu.menu_sections.append(menu_section)
        score_titles = list(self.score_wrangler.iterate_score_titles_with_years(
            scores_to_show=self.session.scores_to_show))
        score_package_short_names = list(self.score_wrangler.iterate_score_package_short_names(
            scores_to_show=self.session.scores_to_show))
        menu_section.items_to_number = zip(score_titles, score_package_short_names)
        menu_section.sentence_length_items.append(('k', 'work with interactive material proxies'))
        menu_section.sentence_length_items.append(('m', 'work with Bača materials'))
        menu_section.hidden_items.append(('svn', 'work with repository'))
        menu_section.hidden_items.append(('active', 'show active scores only'))
        menu_section.hidden_items.append(('all', 'show all scores'))
        menu_section.hidden_items.append(('mb', 'show mothballed scores only'))
        menu.include_back = False
        menu.include_studio = False
        return menu

    def make_svn_menu(self):
        menu = self.Menu(where=self.where(), session=self.session)
        menu_section = self.MenuSection()
        menu_section.sentence_length_items.append(('add', 'svn add'))
        menu_section.sentence_length_items.append(('ci', 'svn commit'))
        menu_section.sentence_length_items.append(('st', 'svn status'))
        menu_section.sentence_length_items.append(('up', 'svn update'))
        menu.menu_sections.append(menu_section)
        menu_section = self.MenuSection()
        menu_section.sentence_length_items.append(('add scores', 'svn add (scores)'))
        menu_section.sentence_length_items.append(('ci scores', 'svn commit (scores)'))
        menu_section.sentence_length_items.append(('st scores', 'svn status (scores)'))
        menu_section.sentence_length_items.append(('up scores', 'svn update (scores)'))
        menu.menu_sections.append(menu_section)
        menu_section = self.MenuSection()
        menu_section.sentence_length_items.append(('pytest', 'run regression tests'))
        menu_section.sentence_length_items.append(('pytest scores', 'run regression tests (scores)'))
        menu_section.sentence_length_items.append(('pytest all', 'run regression tests (all)'))
        menu.menu_sections.append(menu_section)
        return menu

    def manage_svn(self):
        self.session.menu_pieces.append('repository commands')
        while True:
            menu = self.make_svn_menu()
            key, value = menu.run()
            if self.handle_svn_response(key, value):
                break
            if self.session.session_is_complete:
                break
        self.session.menu_pieces.pop()

    def run_py_test_all(self, prompt_proceed=True):
        proc = subprocess.Popen('py.test %s %s' % 
            (self.directory_name, self.score_wrangler.directory_name), 
            shell=True, stdout=subprocess.PIPE)
        lines = proc.stdout.readlines()
        if lines:
            print ''.join(lines)
        if prompt_proceed:
            self.proceed()

    def select_interactive_material_proxy(self, klasses=None):
        material_proxies = list(self.iterate_interactive_material_proxies())
        menu = self.Menu(where=self.where(), session=self.session)
        menu.items_to_number = material_proxies
        key, value = menu.run()
        return value

    def work_in_studio(self):
        self.session.menu_pieces.append('studio')
        while True:
            self.session.menu_pieces.append('{} scores'.format(self.session.scores_to_show))
            menu = self.make_main_menu()
            key, value = menu.run()
            if self.handle_main_menu_response(key, value):
                break
            if self.session.session_is_complete:
                break
            self.session.menu_pieces.pop()
        self.session.menu_pieces.pop()
