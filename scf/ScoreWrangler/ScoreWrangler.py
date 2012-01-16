from baca.scf.PackageWrangler import PackageWrangler
from baca.scf.ScoreProxy import ScoreProxy
import os


class ScoreWrangler(PackageWrangler):

    def __init__(self, session=None):
        PackageWrangler.__init__(self, directory_name=os.environ.get('SCORES'), session=session)

    ### OVERLOADS ###

    def __repr__(self):
        return '{}()'.format(self.class_name)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def score_package_short_names(self):
        result = []
        for score_proxy in self.score_proxies:
            result.append(score_proxy.package_short_name)
        return result

    @property
    def score_proxies(self):
        result = []
        #scores_to_show = scores_to_show or self.session.scores_to_show
        scores_to_show = self.session.scores_to_show
        for score_proxy in self.package_proxies:
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
        for score_proxy in self.score_proxies:
            result.append(score_proxy.title_with_year)
        return result

    ### PUBLIC METHODS ###

    def create_score_package_interactively(self, score_package_importable_name):
        score_proxy = ScoreProxy(session=self.session)
        score_proxy.create_score_package_creation_wizard()

    def fix_score_package_structures(self):
        for score_proxy in self.score_proxies:
            score_proxy.fix_package_structure()
            score_proxy.profile_package_structure()

    def get_package_proxy(self, package_importable_name):
        return ScoreProxy(package_importable_name, session=self.session)

    def profile_score_package_structures(self):
        for score_proxy in self.score_proxies:
            score_proxy.profile_package_structure()

    def select_score_proxy(self):
        menu, section = self.make_new_menu(where=self.where(), is_numbered=True)
        section.tokens = self.score_titles_with_years
        score_package_short_name = self.title_to_score_package_short_name(value)
        score_proxy = ScoreProxy(score_package_short_name, session=self.session)
        return score_proxy
    
    def svn_ci(self, prompt_proceed=True):
        commit_message = self.handle_raw_input('commit message')
        line = 'commit message will be: "{}"\n'.format(commit_message)
        self.conditionally_display_lines([line])
        if not self.confirm():
            return
        for score_proxy in self.score_proxies:
            score_proxy.svn_ci(commit_message=commit_message, prompt_proceed=False)
        if prompt_proceed:
            self.proceed()

    def svn_st(self, prompt_proceed=True):
        for score_proxy in self.score_proxies:
            score_proxy.svn_st(prompt_proceed=False)
        if prompt_proceed:
            self.proceed()

    def svn_up(self, prompt_proceed=True):
        for score_proxy in self.score_proxies:
            score_proxy.svn_up(prompt_proceed=False)
        if prompt_proceed:
            self.proceed()
