from baca.scf.DirectoryProxy import DirectoryProxy
from baca.scf.PackageWrangler import PackageWrangler
import os


class ScoreWrangler(PackageWrangler, DirectoryProxy):

    def __init__(self):
        PackageWrangler.__init__(self, directory_name=os.environ.get('SCORES'))
        self.package_importable_name = ''

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % self.class_name

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
        for score_proxy in self.iterate_score_proxies():
            score_proxy.fix_package_structure()
            score_proxy.profile_package_structure()
            print ''

    def get_package_proxy(self, package_importable_name):
        return self.ScoreProxy(package_importable_name)

    def iterate_score_package_short_names(self, hide_mothballed_scores=True):
        for score_proxy in self.iterate_package_proxies():
            if not score_proxy.get_tag('is_mothballed') or not hide_mothballed_scores:
                yield score_proxy.package_short_name

    def iterate_score_proxies(self, hide_mothballed_scores=True):
        for score_proxy in self.iterate_package_proxies():
            if not score_proxy.get_tag('is_mothballed') or not hide_mothballed_scores:
                yield score_proxy

    def iterate_score_titles_with_years(self, hide_mothballed_scores=True):
        for score_proxy in self.iterate_package_proxies():
            if not score_proxy.get_tag('is_mothballed') or not hide_mothballed_scores:
                yield '{0.title} ({0.year_of_completion})'.format(score_proxy)

    def profile_score_package_structures(self):
        for score_proxy in self.iterate_score_proxies():
            score_proxy.profile_package_structure()
            print ''

    def select_score_proxy(self, menu_header=None):
        menu = self.Menu(client=self.where())
        menu.menu_header = menu_header
        menu.menu_body = 'select score'
        menu_section = self.MenuSection()
        menu_section.items_to_number = self.iterate_score_titles_with_years()
        menu_section.sentence_length_items.append(('s', 'studio'))
        menu.menu_sections.append(menu_section)
        key, value = menu.display_menu()
        if key == 's':
            return None
        score_package_short_name = self.title_to_score_package_short_name(value)
        score_proxy = self.ScoreProxy(score_package_short_name)
        return score_proxy
    
    def svn_ci(self, prompt_proceed=True):
        commit_message = raw_input('Commit message> ')
        print ''
        print 'Commit message will be: "%s"\n' % commit_message
        if not self.confirm():
            return
        for score_proxy in self.iterate_score_proxies():
            score_proxy.svn_ci(commit_message=commit_message, prompt_proceed=False)
        if prompt_proceed:
            self.proceed()

    def svn_st(self, prompt_proceed=True):
        for score_proxy in self.iterate_score_proxies():
            score_proxy.svn_st(prompt_proceed=False)
        if prompt_proceed:
            self.proceed()

    def svn_up(self, prompt_proceed=True):
        for score_proxy in self.iterate_score_proxies():
            score_proxy.svn_up(prompt_proceed=False)
        if prompt_proceed:
            self.proceed()
