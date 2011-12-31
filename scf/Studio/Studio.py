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
    def breadcrumb(self):
        return 'studio'

    @property
    def global_proxy(self):
        return self._global_proxy

    @property
    def score_status_string(self):
        return '{} scores'.format(self.session.scores_to_show)

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
        while True:
            self.append_breadcrumb('select materials directory')
            menu, section = self.make_new_menu(where=self.where())
            section.menu_entry_tokens = self.score_wrangler.iterate_score_titles_with_years()
            section.number_menu_entries = True
            section = menu.make_new_section() 
            section.menu_entry_tokens.append(('baca', 'baca materials directory'))
            result = menu.run()
            if result == 'baca':
                return self.global_proxy.materials_package_importable_name
            else:
                score_title = value
                score_package_importable_name = self.score_wrangler.title_to_score_package_short_name(
                    score_title)
                score_proxy = self.score_wrangler.ScoreProxy(
                    score_package_importable_name, session=self.session)
                return score_proxy.materials_package_importable_name
            self.pop_breadcrumb()
        self.pop_breadcrumb()

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

    def handle_main_menu_result(self, result):
        if not isinstance(result, str):
            raise TypeError('result must be string.')
        if result == 'active':
            self.session.scores_to_show = 'active'
        elif result == 'all':
            self.session.scores_to_show = 'all'
        elif result == 'k':
            self.global_proxy.maker_wrangler.run()
        elif result == 'm':
            breadcrumb = self.pop_breadcrumb()
            self.global_proxy.material_wrangler.run()
            self.append_breadcrumb(breadcrumb)
        elif result == 'mb':
            self.session.scores_to_show = 'mothballed'
        elif result == 'svn':
            self.manage_svn()
        elif result in self.score_wrangler.iterate_score_package_short_names():
            self.edit_score_interactively(result)
    
    def handle_svn_menu_result(self, result):
        '''Return true to exit the svn menu.
        '''
        this_result = False
        if result == 'b':
            return 'back'
        elif result == 'add':
            self.global_proxy.svn_add()
        elif result == 'add_scores':
            self.score_wrangler.svn_add()
        elif result == 'ci':
            self.global_proxy.svn_ci()
            return True
        elif result == 'ci_scores':
            self.score_wrangler.svn_ci()
        elif result == 'pytest':
            self.global_proxy.run_py_test()
        elif result == 'pytest_scores':
            self.score_wrangler.run_py_test()
        elif result == 'pytest_all':
            self.run_py_test_all()
        elif result == 'st':
            self.global_proxy.svn_st()
        elif result == 'st_scores':
            self.score_wrangler.svn_st()
        elif result == 'up':
            self.global_proxy.svn_up()
            return True
        elif result == 'up_scores':
            self.score_wrangler.svn_up()
            return True
        return this_result

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
        section.menu_entry_tokens = zip(score_package_short_names, score_titles)
        section.number_menu_entries = True
        section.display_keys = False
        section = menu.make_new_section()
        section.menu_entry_tokens.append(('k', 'work with interactive material proxies'))
        section.menu_entry_tokens.append(('m', 'work with Bača materials'))
        menu.hidden_entries.append(('svn', 'work with repository'))
        menu.hidden_entries.append(('active', 'show active scores only'))
        menu.hidden_entries.append(('all', 'show all scores'))
        menu.hidden_entries.append(('mb', 'show mothballed scores only'))
        return menu

    def make_svn_menu(self):
        menu, section = self.make_new_menu(where=self.where())
        section.menu_entry_tokens.append(('add', 'add'))
        section.menu_entry_tokens.append(('ci', 'ci'))
        section.menu_entry_tokens.append(('st', 'st'))
        section.menu_entry_tokens.append(('up', 'up'))
        section.display_keys = False
        section = menu.make_new_section()
        section.menu_entry_tokens.append(('add_scores', 'add_scores'))
        section.menu_entry_tokens.append(('ci_scores', 'ci_scores'))
        section.menu_entry_tokens.append(('st_scores', 'st_scores'))
        section.menu_entry_tokens.append(('up_scores', 'up_scores'))
        section.display_keys = False
        section = menu.make_new_section()
        section.menu_entry_tokens.append(('pytest', 'pytest'))
        section.menu_entry_tokens.append(('pytest_scores', 'pytest_scores'))
        section.menu_entry_tokens.append(('pytest_all', 'pytest_all'))
        section.display_keys = False
        return menu

    def run(self, user_input=None):
        type(self).__init__(self)
        self.assign_user_input(user_input=user_input)
        self.append_breadcrumb()
        run_main_menu = True
        while True:
            self.append_breadcrumb(self.score_status_string)
            if run_main_menu:
                menu = self.make_main_menu()
                result = menu.run()
            else:
                run_main_menu = True
            if self.session.is_complete:
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
            elif self.session.is_backtracking_to_studio:
                self.session.is_backtracking_to_studio = False
                self.pop_breadcrumb()
                continue
            elif self.session.is_backtracking_to_score:
                self.session.is_backtracking_to_score = False
                self.pop_breadcrumb()
                continue
            elif not result:
                self.pop_breadcrumb()
                continue
            self.handle_main_menu_result(result)
            if self.session.is_complete:
                self.pop_breadcrumb()
                self.session.clean_up()
                break
            elif self.session.is_navigating_to_sibling_score:
                run_main_menu = False
            elif self.session.is_backtracking_to_studio:
                self.session.is_backtracking_to_studio = False
                self.pop_breadcrumb()
                continue
            elif self.session.is_backtracking_to_score:
                self.session.is_backtracking_to_score = False
                self.pop_breadcrumb()
                continue
            self.pop_breadcrumb()
        self.pop_breadcrumb()

    def manage_svn(self):
        while True:
            self.append_breadcrumb('repository commands')
            menu = self.make_svn_menu()
            result = menu.run()
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

    def run_py_test_all(self, prompt_proceed=True):
        proc = subprocess.Popen(
            'py.test {} {}'.format(self.directory_name, self.score_wrangler.directory_name), 
            shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        if lines:
            self.conditionally_display_lines(lines)
        if prompt_proceed:
            self.proceed()

    def select_interactive_material_proxy(self, klasses=None):
        material_proxies = list(self.iterate_interactive_material_proxies())
        menu, section = self.make_new_menu(where=self.where())
        section.menu_entry_tokens = material_proxies
        section.number_menu_entries = True
        result = menu.run()
        # TODO: probably backtrack here
        return result
