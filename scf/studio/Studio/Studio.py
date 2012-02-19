# -*- encoding: utf-8 -*-
from abjad.tools import iotools
from abjad.tools import mathtools
from baca.scf.core.SCFObject import SCFObject
from baca.scf.proxies.HomePackageProxy import HomePackageProxy
from baca.scf.wranglers.ScorePackageWrangler import ScorePackageWrangler
import subprocess


class Studio(SCFObject):

    def __init__(self, session=None):
        SCFObject.__init__(self, session=session)
        self._home_package_proxy = HomePackageProxy(session=self.session)
        self._score_package_wrangler = ScorePackageWrangler(session=self.session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'studio'

    @property
    def home_package_proxy(self):
        return self._home_package_proxy

    @property
    def score_status_string(self):
        return '{} scores'.format(self.session.scores_to_show)

    @property
    def score_package_wrangler(self):
        return self._score_package_wrangler

    ### PUBLIC METHODS ###

    def edit_score_interactively(self, score_package_importable_name):
        score_package_proxy = self.score_package_wrangler.get_package_proxy(score_package_importable_name)
        score_package_proxy.session.current_score_package_short_name = score_package_importable_name
        # TODO: use cache keyword
        breadcrumbs = self.breadcrumb_stack[:]
        self.session._breadcrumb_stack = []
        score_package_proxy.run()
        self.session._breadcrumb_stack = breadcrumbs
        self.session.current_score_package_name = None

    def get_next_score_package_short_name(self):
        score_package_short_names = self.score_package_wrangler.list_wrangled_package_short_names_to_display()
        if self.session.current_score_package_short_name is None:
            return score_package_short_names[0]
        index = score_package_short_names.index(self.session.current_score_package_short_name)
        next_index = (index + 1) % len(score_package_short_names)
        return score_package_short_names[next_index]

    # TODO: write test
    def get_package_root_name_interactively(self, clear=True, cache=False):
        self.cache_breadcrumbs(cache=cache)
        while True:
            menu = self.make_score_selection_menu()
            last_section = menu.sections[-1]
            last_section.tokens.insert(0, ('baca', 'global (default)'))
            last_section.default_index = 0
            menu.explicit_title = 'select location:'
            package_root_name = menu.run(clear=clear)
            if self.backtrack():
                self.restore_breadcrumbs(cache=cache)
                return
            if package_root_name:
                self.restore_breadcrumbs(cache=cache)
                return package_root_name

    def get_prev_score_package_short_name(self):
        score_package_short_names = self.score_package_wrangler.list_wrangled_package_short_names_to_display()
        if self.session.current_score_package_short_name is None:
            return score_package_short_names[-1]
        index = score_package_short_names.index(self.session.current_score_package_short_name)
        prev_index = (index - 1) % len(score_package_short_names)
        return score_package_short_names[prev_index]

    def handle_main_menu_result(self, result):
        if not isinstance(result, str):
            raise TypeError('result must be string.')
        if result == 'active':
            self.session.show_active_scores()
        elif result == 'all':
            self.session.show_all_scores()
        elif result == 'k':
            self.print_not_implemented()
        elif result == 'm':
            breadcrumb = self.pop_breadcrumb()
            self.home_package_proxy.material_package_wrangler.run(head=self.studio_package_importable_name)
            self.push_breadcrumb(breadcrumb)
        elif result == 'new':
            breadcrumb = self.pop_breadcrumb()
            self.score_package_wrangler.make_package_interactively()
            self.push_breadcrumb(breadcrumb)
        elif result == 'mb':
            self.session.show_mothballed_scores()
        elif result == 'svn':
            self.manage_svn()
        elif result == 'profile':
            self.score_package_wrangler.profile_visible_package_structures()
        elif result in self.score_package_wrangler.list_wrangled_package_short_names_to_display():
            self.edit_score_interactively(result)
    
    def handle_svn_menu_result(self, result):
        '''Return true to exit the svn menu.
        '''
        this_result = False
        if result == 'add':
            self.home_package_proxy.svn_add()
        elif result == 'add_scores':
            self.score_package_wrangler.svn_add()
        elif result == 'ci':
            self.home_package_proxy.svn_ci()
            return True
        elif result == 'ci_scores':
            self.score_package_wrangler.svn_ci()
        elif result == 'pytest':
            self.home_package_proxy.run_py_test()
        elif result == 'pytest_scores':
            self.score_package_wrangler.run_py_test()
        elif result == 'pytest_all':
            self.run_py_test_all()
        elif result == 'st':
            self.home_package_proxy.svn_st()
        elif result == 'st_scores':
            self.score_package_wrangler.svn_st()
        elif result == 'up':
            self.home_package_proxy.svn_up()
            return True
        elif result == 'up_scores':
            self.score_package_wrangler.svn_up()
            return True
        return this_result

    def make_main_menu(self):
        menu = self.make_score_selection_menu()
        section = menu.make_section()
        section.append(('m', 'materials'))
        section.append(('k', 'sketches'))
        section.append(('new', 'new score'))
        hidden_section = menu.make_section(is_hidden=True)
        hidden_section.append(('svn', 'work with repository'))
        hidden_section.append(('active', 'show active scores only'))
        hidden_section.append(('all', 'show all scores'))
        hidden_section.append(('mb', 'show mothballed scores only'))
        hidden_section.append(('profile', 'profile packages'))
        return menu

    def make_score_selection_menu(self):
        menu, section = self.make_menu(where=self.where(), is_numbered=True, is_keyed=False)
        score_package_short_names = self.score_package_wrangler.list_wrangled_package_short_names_to_display()
        score_titles = self.score_package_wrangler.score_titles_with_years_to_display
        tokens = zip(score_package_short_names, score_titles)
        tmp = iotools.strip_diacritics_from_binary_string
        tokens.sort(lambda x, y: cmp(tmp(x[1]), tmp(y[1])))
        section.tokens = tokens
        return menu

    def make_svn_menu(self):
        menu, section = self.make_menu(where=self.where(), is_keyed=False)
        section.append(('add', 'add'))
        section.append(('ci', 'ci'))
        section.append(('st', 'st'))
        section.append(('up', 'up'))
        section = menu.make_section(is_keyed=False)
        section.append(('add_scores', 'add_scores'))
        section.append(('ci_scores', 'ci_scores'))
        section.append(('st_scores', 'st_scores'))
        section.append(('up_scores', 'up_scores'))
        section = menu.make_section(is_keyed=False)
        section.append(('pytest', 'pytest'))
        section.append(('pytest_scores', 'pytest_scores'))
        section.append(('pytest_all', 'pytest_all'))
        return menu

    def manage_svn(self, clear=True):
        while True:
            self.push_breadcrumb('repository commands')
            menu = self.make_svn_menu()
            result = menu.run(clear=clear)
            if self.session.is_backtracking_to_score:
                self.session.is_backtracking_to_score = False
                self.pop_breadcrumb()
                continue
            elif self.backtrack():
                break
            self.handle_svn_menu_result(result)
            if self.backtrack():
                break
            self.pop_breadcrumb()
        self.pop_breadcrumb()

    def run(self, user_input=None, clear=True, cache=False):
        type(self).__init__(self)
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        self.push_breadcrumb()
        run_main_menu = True
        while True:
            self.push_breadcrumb(self.score_status_string)
            if run_main_menu:
                menu = self.make_main_menu()
                result = menu.run(clear=clear)
            else:
                run_main_menu = True
            if self.backtrack(source='studio'):
                self.pop_breadcrumb()
                self.session.clean_up()
                break
            elif self.session.is_navigating_to_next_score:
                self.session.is_navigating_to_next_score = False
                self.session.is_backtracking_to_studio = False
                result = self.get_next_score_package_short_name()
            elif self.session.is_navigating_to_prev_score:
                self.session.is_navigating_to_prev_score = False
                self.session.is_backtracking_to_studio = False
                result = self.get_prev_score_package_short_name()
            elif not result:
                self.pop_breadcrumb()
                continue
            self.handle_main_menu_result(result)
            if self.backtrack(source='studio'):
                self.pop_breadcrumb()
                self.session.clean_up()
                break
            elif self.session.is_navigating_to_sibling_score:
                run_main_menu = False
            self.pop_breadcrumb()
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)

    def run_py_test_all(self, prompt=True):
        proc = subprocess.Popen(
            'py.test {} {}'.format(self.directory_name, self.score_package_wrangler.directory_name), 
            shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        if lines:
            self.display(lines, capitalize_first_character=False)
        line = 'tests complete.'
        self.proceed(line, prompt=prompt)
