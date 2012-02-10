from abjad.tools import iotools
from baca.scf.PackageWrangler import PackageWrangler
from baca.scf.ScorePackageProxy import ScorePackageProxy
import os, shutil, sys


class ScorePackageWrangler(PackageWrangler):

    def __init__(self, session=None):
        PackageWrangler.__init__(self, None, '', session=session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def score_package_short_names_to_display(self):
        result = []
        for score_package_proxy in self.score_package_proxies_to_display:
            result.append(score_package_proxy.package_short_name)
        return result

    @property
    def score_package_proxies_to_display(self):
        result = []
        scores_to_show = self.session.scores_to_show
        for score_package_proxy in self.list_wrangled_package_proxies():
            is_mothballed = score_package_proxy.get_tag('is_mothballed')
            if scores_to_show == 'all':
                result.append(score_package_proxy)
            elif scores_to_show == 'active' and not is_mothballed:
                result.append(score_package_proxy)
            elif scores_to_show == 'mothballed' and is_mothballed:
                result.append(score_package_proxy)
        return result

    @property
    def score_titles_with_years(self):
        result = []
        for score_package_proxy in self.score_package_proxies_to_display:
            result.append(score_package_proxy.title_with_year or '(untitled score)')
        return result

    @property
    def temporary_score_package_directory_name(self):
        return os.path.join(os.environ.get('SCORES'), '__temporary_score_package')

    @property
    def temporary_score_package_importable_name(self):
        return '__temporary_score_package'

    ### PUBLIC METHODS ###

    def fix_score_package_structures(self):
        for score_package_proxy in self.score_package_proxies_to_display:
            score_package_proxy.fix_package_structure()
            score_package_proxy.profile_package_structure()

    def get_package_proxy(self, package_importable_name):
        return ScorePackageProxy(package_importable_name, session=self.session)

    def get_score_package_importable_name_interactively(self, prompt=True):
        getter = self.make_new_getter(where=self.where())
        getter.append_underscore_delimited_lowercase_package_name('score package name')
        self.push_backtrack()
        score_package_importable_name = getter.run()
        self.pop_backtrack()
        if self.backtrack():
            return 
        return score_package_importable_name

    def make_score_package(self, score_package_short_name):
        assert iotools.is_underscore_delimited_lowercase_package_name(score_package_short_name)
        score_package_directory_name = os.path.join(os.environ.get('SCORES'), score_package_short_name)
        os.mkdir(score_package_directory_name)
        score_package_proxy = self.get_package_proxy(score_package_short_name)
        score_package_proxy.fix_package_structure(is_interactive=False)

    def make_score_package_interactively(self):
        getter = self.make_new_getter(where=self.where())
        getter.indent_level = 1
        getter.prompt_character = ':'
        getter.capitalize_prompts = False
        getter.include_newlines = False
        getter.append_string('score title')
        getter.append_underscore_delimited_lowercase_package_name('package name')
        getter.append_integer_in_closed_range('year', 0, sys.maxint)
        result = getter.run()
        if self.backtrack():
            return
        title, score_package_short_name, year = result
        self.make_score_package(score_package_short_name)
        score_package_proxy = self.get_package_proxy(score_package_short_name)
        score_package_proxy.add_tag('title', title)
        score_package_proxy.year_of_completion = year
        
    def profile_score_package_structures(self):
        for score_package_proxy in self.score_package_proxies_to_display:
            score_package_proxy.profile_package_structure()

    def select_score_package_proxy(self):
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
        section.tokens = self.score_titles_with_years
        score_package_short_name = self.title_to_score_package_short_name(value)
        score_package_proxy = ScorePackageProxy(score_package_short_name, session=self.session)
        return score_package_proxy
    
    # TODO: move up to level of wrangler
    def svn_ci(self, prompt=True):
        getter = self.make_new_getter(where=self.where())
        getter.append_string('commit message')
        commit_message = getter.run()
        if self.backtrack():
            return
        line = 'commit message will be: "{}"\n'.format(commit_message)
        self.display(line)
        if not self.confirm():
            return
        for score_package_proxy in self.score_package_proxies_to_display:
            score_package_proxy.svn_ci(commit_message=commit_message, prompt=False)
        self.proceed(prompt=prompt)

    # TODO: move up to level of wrangler
    def svn_st(self, prompt=True):
        for score_package_proxy in self.score_package_proxies_to_display:
            score_package_proxy.svn_st(prompt=False)
        self.proceed(prompt=prompt)

    # TODO: move up to level of wrangler
    def svn_up(self, prompt=True):
        for score_package_proxy in self.score_package_proxies_to_display:
            score_package_proxy.svn_up(prompt=False)
        self.proceed(prompt=prompt)
