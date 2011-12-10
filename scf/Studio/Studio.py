# -*- encoding: utf-8 -*-
from baca.scf.SCFObject import SCFObject
from baca.scf.GlobalProxy import GlobalProxy
from baca.scf.ScoreWrangler import ScoreWrangler
import subprocess


class Studio(SCFObject):

    def __init__(self, session=None, user_input=None):
        SCFObject.__init__(self, session=session)
        self._global_proxy = GlobalProxy(session=self.session)
        self._score_wrangler = ScoreWrangler(session=self.session)
        if user_input is not None:
            self.session.user_input = user_input

    ### PUBLIC ATTRIBUTES ###

    @property
    def global_proxy(self):
        return self._global_proxy

    @property
    def score_wrangler(self):
        return self._score_wrangler

    ### PUBLIC METHODS ###

    def edit_score_interactively(self, score_package_importable_name):
        score_proxy = self.score_wrangler.ScoreProxy(score_package_importable_name, session=self.session)
        breadcrumbs = self.breadcrumbs[:]
        self.session.breadcrumbs = []
        score_proxy.run()
        self.session.breadcrumbs = breadcrumbs

    def get_materials_package_importable_name_interactively(self):
        self.breadcrumbs.append('select materials directory')
        while True:
            menu, section = self.make_new_menu(where=self.where())
            section.items_to_number = self.score_wrangler.iterate_score_titles_with_years()
            section.sentence_length_items.append(('baca', 'baca materials directory'))
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
        self.breadcrumbs.pop()

    def handle_main_menu_response(self, key, value):
        if not isinstance(key, str):
            raise TypeError('key must be string.')
        if key == 'active':
            self.session.scores_to_show = 'active'
        elif key == 'all':
            self.session.scores_to_show = 'all'
        elif key == 'k':
            self.global_proxy.maker_wrangler.run()
        elif key == 'm':
            self.global_proxy.material_wrangler.run()
        elif key == 'mb':
            self.session.scores_to_show = 'mothballed'
        elif key == 'svn':
            self.manage_svn()
        else:
            self.edit_score_interactively(value)
    
    def handle_svn_response(self, key, value):
        '''Return true to exit the svn menu.
        '''
        result = False
        if key == 'b':
            return 'back'
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
        return result

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
        menu, section = self.make_new_menu(where=self.where())
        score_titles = list(self.score_wrangler.iterate_score_titles_with_years(
            scores_to_show=self.session.scores_to_show))
        score_package_short_names = list(self.score_wrangler.iterate_score_package_short_names(
            scores_to_show=self.session.scores_to_show))
        section.items_to_number = zip(score_titles, score_package_short_names)
        section.sentence_length_items.append(('k', 'work with interactive material proxies'))
        section.sentence_length_items.append(('m', 'work with Bača materials'))
        section.hidden_items.append(('svn', 'work with repository'))
        section.hidden_items.append(('active', 'show active scores only'))
        section.hidden_items.append(('all', 'show all scores'))
        section.hidden_items.append(('mb', 'show mothballed scores only'))
        menu.include_back = False
        menu.include_studio = False
        return menu

    def make_svn_menu(self):
        menu, section = self.make_new_menu(where=self.where())
        section.sentence_length_items.append(('add', 'svn add'))
        section.sentence_length_items.append(('ci', 'svn commit'))
        section.sentence_length_items.append(('st', 'svn status'))
        section.sentence_length_items.append(('up', 'svn update'))
        section = self.MenuSection()
        section.sentence_length_items.append(('add scores', 'svn add (scores)'))
        section.sentence_length_items.append(('ci scores', 'svn commit (scores)'))
        section.sentence_length_items.append(('st scores', 'svn status (scores)'))
        section.sentence_length_items.append(('up scores', 'svn update (scores)'))
        menu.sections.append(section)
        section = self.MenuSection()
        section.sentence_length_items.append(('pytest', 'run regression tests'))
        section.sentence_length_items.append(('pytest scores', 'run regression tests (scores)'))
        section.sentence_length_items.append(('pytest all', 'run regression tests (all)'))
        menu.sections.append(section)
        return menu

    def run(self, user_input=None):
        if user_input is not None:
            self.session.user_input = user_input
        self.breadcrumbs.append('studio')
        while True:
            self.breadcrumbs.append('{} scores'.format(self.session.scores_to_show))
            menu = self.make_main_menu()
            key, value = menu.run()
            if self.session.is_complete:
                self.breadcrumbs.pop()
                self.session.clean_up()
                break
            if self.session.is_backtracking_to_studio:
                self.session.is_backtracking_to_studio = False
                self.breadcrumbs.pop()
                continue
            if key is None:
                self.breadcrumbs.pop()
                continue
            self.handle_main_menu_response(key, value)
            if self.session.is_complete:
                self.breadcrumbs.pop()
                self.session.clean_up()
                break
            if self.session.is_backtracking_to_studio:
                self.session.is_backtracking_to_studio = False
                self.breadcrumbs.pop()
                continue
            self.breadcrumbs.pop()

    def manage_svn(self):
        self.breadcrumbs.append('repository commands')
        while True:
            menu = self.make_svn_menu()
            key, value = menu.run()
            if self.session.backtrack():
                break
            self.handle_svn_response(key, value)
            if self.session.backtrack():
                break
        self.breadcrumbs.pop()

    def run_py_test_all(self, prompt_proceed=True):
        proc = subprocess.Popen(
            'py.test {} {}'.format(self.directory_name, self.score_wrangler.directory_name), 
            shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        if lines:
            self.display_lines(lines)
        if prompt_proceed:
            self.proceed()

    def select_interactive_material_proxy(self, klasses=None):
        material_proxies = list(self.iterate_interactive_material_proxies())
        menu, section = self.make_new_menu(where=self.where())
        menu.items_to_number = material_proxies
        key, value = menu.run()
        return value
