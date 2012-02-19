from abjad.tools import iotools
from baca.scf.wranglers.PackageWrangler import PackageWrangler
from baca.scf.proxies.ScorePackageProxy import ScorePackageProxy
import os
import shutil
import sys


class ScorePackageWrangler(PackageWrangler):

    def __init__(self, session=None):
        PackageWrangler.__init__(self, 
            toplevel_global_package_importable_name=None, 
            toplevel_score_package_importable_name_body='', session=session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def current_containing_directory_name(self):
        return self.scores_directory_name

    @property
    def score_titles_with_years_to_display(self):
        result = []
        for score_package_proxy in self.list_wrangled_package_proxies_to_display():
            result.append(score_package_proxy.title_with_year or '(untitled score)')
        return result

    ### PUBLIC METHODS ###

    def get_package_proxy(self, package_importable_name):
        return ScorePackageProxy(package_importable_name, session=self.session)

    def list_wrangled_package_proxies_to_display(self, head=None):
        result = []
        scores_to_show = self.session.scores_to_show
        for score_package_proxy in PackageWrangler.list_wrangled_package_proxies(
            self, head=head):
            is_mothballed = score_package_proxy.get_tag('is_mothballed')
            if scores_to_show == 'all':
                result.append(score_package_proxy)
            elif scores_to_show == 'active' and not is_mothballed:
                result.append(score_package_proxy)
            elif scores_to_show == 'mothballed' and is_mothballed:
                result.append(score_package_proxy)
        return result

    def make_package_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.indent_level = 1
        getter.prompt_character = ':'
        getter.capitalize_prompts = False
        getter.include_newlines = False
        getter.number_prompts = True
        getter.append_string('score title')
        getter.append_underscore_delimited_lowercase_package_name('package name')
        getter.append_integer_in_range('year', start=1, allow_none=True)
        result = getter.run()
        if self.backtrack():
            return
        title, score_package_short_name, year = result
        self.make_package(score_package_short_name)
        score_package_proxy = self.get_package_proxy(score_package_short_name)
        score_package_proxy.add_tag('title', title)
        score_package_proxy.year_of_completion = year
        
    # TODO: move up to level of wrangler
    def svn_add(self, prompt=True):
        for score_package_proxy in self.list_wrangled_package_proxies_to_display():
            score_package_proxy.svn_add(prompt=False)
        self.proceed(prompt=prompt)

    # TODO: move up to level of wrangler
    def svn_ci(self, prompt=True):
        getter = self.make_getter(where=self.where())
        getter.append_string('commit message')
        commit_message = getter.run()
        if self.backtrack():
            return
        line = 'commit message will be: "{}"\n'.format(commit_message)
        self.display(line)
        if not self.confirm():
            return
        for score_package_proxy in self.list_wrangled_package_proxies_to_display():
            score_package_proxy.svn_ci(commit_message=commit_message, prompt=False)
        self.proceed(prompt=prompt)

    # TODO: move up to level of wrangler
    def svn_st(self, prompt=True):
        for score_package_proxy in self.list_wrangled_package_proxies_to_display():
            score_package_proxy.svn_st(prompt=False)
        self.proceed(prompt=prompt)

    # TODO: move up to level of wrangler
    def svn_up(self, prompt=True):
        for score_package_proxy in self.list_wrangled_package_proxies_to_display():
            score_package_proxy.svn_up(prompt=False)
        self.proceed(prompt=prompt)
