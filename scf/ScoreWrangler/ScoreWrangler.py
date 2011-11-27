from baca.scf.PackageWrangler import PackageWrangler
import os


class ScoreWrangler(PackageWrangler):

    def __init__(self, session=None):
        PackageWrangler.__init__(self, directory_name=os.environ.get('SCORES'), session=session)

    ### OVERLOADS ###

    def __repr__(self):
        return '{}()'.format(self.class_name)

    ### PUBLIC ATTRIBUTES ###

    @property
    def ScoreProxy(self):
        import baca
        return baca.scf.ScoreProxy

    ### PUBLIC METHODS ###

    def create_score_package_interactively(self, score_package_importable_name):
        score_proxy = self.ScoreProxy()
        score_proxy.create_score_package_creation_wizard()

    def fix_score_package_structures(self):
        for score_proxy in self.iterate_score_proxies(scores_to_show=self.session.scores_to_show):
            score_proxy.fix_package_structure()
            score_proxy.profile_package_structure()
            print ''

    def get_package_proxy(self, package_importable_name):
        return self.ScoreProxy(package_importable_name)

    def iterate_score_package_short_names(self, scores_to_show='active'):
        for score_proxy in self.iterate_score_proxies(scores_to_show=scores_to_show):
            yield score_proxy.package_short_name

    def iterate_score_proxies(self, scores_to_show='active'):
        for score_proxy in self.iterate_package_proxies():
            is_mothballed = score_proxy.get_tag('is_mothballed')
            if scores_to_show == 'all':
                yield score_proxy
            elif scores_to_show == 'active' and not is_mothballed:
                yield score_proxy
            elif scores_to_show == 'mothballed' and is_mothballed:
                yield score_proxy

    def iterate_score_titles_with_years(self, scores_to_show='active'):
        for score_proxy in self.iterate_score_proxies(scores_to_show=scores_to_show):
            yield score_proxy.title_with_year

    def profile_score_package_structures(self):
        for score_proxy in self.iterate_score_proxies(scores_to_show=self.session.scores_to_show):
            score_proxy.profile_package_structure()
            print ''

    def select_score_proxy(self):
        menu = self.make_new_menu(where=self.where())
        menu_section = self.MenuSection()
        menu_section.items_to_number = self.iterate_score_titles_with_years()
        menu_section.sentence_length_items.append(('s', 'studio'))
        menu.menu_sections.append(menu_section)
        key, value = menu.run()
        if key == 's':
            return None
        score_package_short_name = self.title_to_score_package_short_name(value)
        score_proxy = self.ScoreProxy(score_package_short_name)
        return score_proxy
    
    def svn_ci(self, prompt_proceed=True):
        commit_message = self.handle_raw_input('Commit message')
        line = 'Commit message will be: "{}"\n'.format(commit_message)
        self.display_lines([line])
        if not self.confirm():
            return
        for score_proxy in self.iterate_score_proxies(scores_to_show=self.session.scores_to_show):
            score_proxy.svn_ci(commit_message=commit_message, prompt_proceed=False)
        if prompt_proceed:
            self.proceed()

    def svn_st(self, prompt_proceed=True):
        for score_proxy in self.iterate_score_proxies(scores_to_show=self.session.scores_to_show):
            score_proxy.svn_st(prompt_proceed=False)
        if prompt_proceed:
            self.proceed()

    def svn_up(self, prompt_proceed=True):
        for score_proxy in self.iterate_score_proxies(scores_to_show=self.session.scores_to_show):
            score_proxy.svn_up(prompt_proceed=False)
        if prompt_proceed:
            self.proceed()
