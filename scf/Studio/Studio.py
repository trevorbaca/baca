# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from baca.scf.SCFObject import SCFObject
from baca.scf.GlobalProxy import GlobalProxy
from baca.scf.ScoreWrangler import ScoreWrangler
import subprocess


class Studio(SCFObject):

    def __init__(self, session=None):
        SCFObject.__init__(self, session=session)
        self._global_proxy = GlobalProxy(session=self.session)
        self._score_wrangler = ScoreWrangler(session=self.session)

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
        score_proxy.session.current_score_package_short_name = score_package_importable_name
        breadcrumbs = self.breadcrumbs[:]
        self.session.breadcrumbs = []
        score_proxy.run()
        self.session.breadcrumbs = breadcrumbs

    def get_materials_package_importable_name_interactively(self):
        self.breadcrumbs.append('select materials directory')
        while True:
            menu, section = self.make_new_menu(where=self.where())
            section.keyed_menu_entry_tuples = [('', x) for x in self.score_wrangler.iterate_score_titles_with_years()]
            section.number_menu_entries = True
            section = menu.make_new_section() 
            section.keyed_menu_entry_tuples.append(('baca', 'baca materials directory'))
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

    def get_next_score_package_short_name(self):
        score_package_short_names = list(self.score_wrangler.iterate_score_package_short_names(
            scores_to_show=self.session.scores_to_show))
        if self.session.current_score_package_short_name is None:
            return score_package_short_names[0]
        index = score_package_short_names.index(self.session.current_score_package_short_name)
        next_index = (index + 1) % len(score_package_short_names)
        return score_package_short_names[next_index]

    def get_prev_score_package_short_name(self):
        score_package_short_names = list(self.score_wrangler.iterate_score_package_short_names(
            scores_to_show=self.session.scores_to_show))
        if self.session.current_score_package_short_name is None:
            return score_package_short_names[-1]
        index = score_package_short_names.index(self.session.current_score_package_short_name)
        prev_index = (index - 1) % len(score_package_short_names)
        return score_package_short_names[prev_index]

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
        elif mathtools.is_integer_equivalent_expr(key):
            self.edit_score_interactively(value)
    
    def handle_svn_response(self, key, value):
        '''Return true to exit the svn menu.
        '''
        result = False
        if key == 'b':
            return 'back'
        elif key == 'add':
            self.global_proxy.svn_add()
        elif key == 'add_scores':
            self.score_wrangler.svn_add()
        elif key == 'ci':
            self.global_proxy.svn_ci()
            return True
        elif key == 'ci_scores':
            self.score_wrangler.svn_ci()
        elif key == 'pytest':
            self.global_proxy.run_py_test()
        elif key == 'pytest_scores':
            self.score_wrangler.run_py_test()
        elif key == 'pytest_all':
            self.run_py_test_all()
        elif key == 'st':
            self.global_proxy.svn_st()
        elif key == 'st_scores':
            self.score_wrangler.svn_st()
        elif key == 'up':
            self.global_proxy.svn_up()
            return True
        elif key == 'up_scores':
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
#        section.keyed_menu_entry_tuples = zip(score_package_short_names, score_titles)
#        section.number_menu_entries = True
#        section.display_keys = False
        section = menu.make_new_section()
        section.keyed_menu_entry_tuples.append(('k', 'work with interactive material proxies'))
        section.keyed_menu_entry_tuples.append(('m', 'work with Bača materials'))
        menu.hidden_items.append(('svn', 'work with repository'))
        menu.hidden_items.append(('active', 'show active scores only'))
        menu.hidden_items.append(('all', 'show all scores'))
        menu.hidden_items.append(('mb', 'show mothballed scores only'))
        return menu

    def make_svn_menu(self):
        menu, section = self.make_new_menu(where=self.where())
        section.keyed_menu_entry_tuples.append(('add', 'add'))
        section.keyed_menu_entry_tuples.append(('ci', 'ci'))
        section.keyed_menu_entry_tuples.append(('st', 'st'))
        section.keyed_menu_entry_tuples.append(('up', 'up'))
        section.display_keys = False
        section = menu.make_new_section()
        section.keyed_menu_entry_tuples.append(('add_scores', 'add_scores'))
        section.keyed_menu_entry_tuples.append(('ci_scores', 'ci_scores'))
        section.keyed_menu_entry_tuples.append(('st_scores', 'st_scores'))
        section.keyed_menu_entry_tuples.append(('up_scores', 'up_scores'))
        section.display_keys = False
        section = menu.make_new_section()
        section.keyed_menu_entry_tuples.append(('pytest', 'pytest'))
        section.keyed_menu_entry_tuples.append(('pytest_scores', 'pytest_scores'))
        section.keyed_menu_entry_tuples.append(('pytest_all', 'pytest_all'))
        section.display_keys = False
        return menu

    def run(self, user_input=None):
        self.session = None
        if user_input is not None:
            self.session.user_input = user_input
        self.breadcrumbs.append('studio')
        run_main_menu = True
        while True:
            self.breadcrumbs.append('{} scores'.format(self.session.scores_to_show))
            if run_main_menu:
                menu = self.make_main_menu()
                key, value = menu.run()
                #print 'FEE', repr(key), repr(value)
            else:
                run_main_menu = True
            if self.session.is_complete:
                self.breadcrumbs.pop()
                self.session.clean_up()
                break
            elif self.session.is_navigating_to_next_score:
                self.session.is_navigating_to_next_score = False
                self.session.is_backtracking_to_studio = False
                key, value = '99', self.get_next_score_package_short_name()
            elif self.session.is_navigating_to_prev_score:
                self.session.is_navigating_to_prev_score = False
                self.session.is_backtracking_to_studio = False
                key, value = '99', self.get_prev_score_package_short_name()
            elif self.session.is_backtracking_to_studio:
                self.session.is_backtracking_to_studio = False
                self.breadcrumbs.pop()
                continue
            elif self.session.is_backtracking_to_score:
                self.session.is_backtracking_to_score = False
                self.breadcrumbs.pop()
                continue
            elif key is None:
                self.breadcrumbs.pop()
                continue
            self.handle_main_menu_response(key, value)
            if self.session.is_complete:
                self.breadcrumbs.pop()
                self.session.clean_up()
                break
            elif self.session.is_navigating_to_sibling_score:
                run_main_menu = False
            elif self.session.is_backtracking_to_studio:
                self.session.is_backtracking_to_studio = False
                self.breadcrumbs.pop()
                continue
            elif self.session.is_backtracking_to_score:
                self.session.is_backtracking_to_score = False
                self.breadcrumbs.pop()
                continue
            self.breadcrumbs.pop()
        self.breadcrumbs.pop()

    def manage_svn(self):
        self.breadcrumbs.append('repository commands')
        while True:
            menu = self.make_svn_menu()
            key, value = menu.run()
            if self.session.is_backtracking_to_score:
                self.session.is_backtracking_to_score = False
                continue
            elif self.backtrack():
                break
            self.handle_svn_response(key, value)
            if self.backtrack():
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
        section.keyed_menu_entry_tuples = [('', x) for x in material_proxies]
        section.number_menu_entries = True
        key, value = menu.run()
        return value
