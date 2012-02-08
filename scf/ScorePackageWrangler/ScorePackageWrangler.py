from baca.scf.PackageWrangler import PackageWrangler
from baca.scf.ScorePackageProxy import ScorePackageProxy
import os


class ScorePackageWrangler(PackageWrangler):

    def __init__(self, session=None):
        PackageWrangler.__init__(self, None, '', session=session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def score_package_short_names_to_display(self):
        result = []
        for score_proxy in self.score_proxies_to_display:
            result.append(score_proxy.package_short_name)
        return result

    @property
    def score_proxies_to_display(self):
        result = []
        scores_to_show = self.session.scores_to_show
        for score_proxy in self.list_wrangled_package_proxies():
            is_mothballed = score_proxy.get_tag('is_mothballed')
            if scores_to_show == 'all':
                result.append(score_proxy)
            elif scores_to_show == 'active' and not is_mothballed:
                result.append(score_proxy)
            elif scores_to_show == 'mothballed' and is_mothballed:
                result.append(score_proxy)
        return result

    @property
    def score_titles_with_years(self):
        result = []
        for score_proxy in self.score_proxies_to_display:
            result.append(score_proxy.title_with_year)
        return result

    ### PUBLIC METHODS ###

    def fix_score_package_structures(self):
        for score_proxy in self.score_proxies_to_display:
            score_proxy.fix_package_structure()
            score_proxy.profile_package_structure()

    def get_package_proxy(self, package_importable_name):
        return ScorePackageProxy(package_importable_name, session=self.session)

    def make_score_package_interactively(self, head=None):
        self.print_not_implemented()

    def profile_score_package_structures(self):
        for score_proxy in self.score_proxies_to_display:
            score_proxy.profile_package_structure()

    def select_score_proxy(self):
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
        section.tokens = self.score_titles_with_years
        score_package_short_name = self.title_to_score_package_short_name(value)
        score_proxy = ScorePackageProxy(score_package_short_name, session=self.session)
        return score_proxy
    
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
        for score_proxy in self.score_proxies_to_display:
            score_proxy.svn_ci(commit_message=commit_message, prompt=False)
        self.proceed(prompt=prompt)

    # TODO: move up to level of wrangler
    def svn_st(self, prompt=True):
        for score_proxy in self.score_proxies_to_display:
            score_proxy.svn_st(prompt=False)
        self.proceed(prompt=prompt)

    # TODO: move up to level of wrangler
    def svn_up(self, prompt=True):
        for score_proxy in self.score_proxies_to_display:
            score_proxy.svn_up(prompt=False)
        self.proceed(prompt=prompt)
