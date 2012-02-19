from baca.scf.wranglers.PackageWrangler import PackageWrangler
from baca.scf.proxies.ScorePackageProxy import ScorePackageProxy


class ScorePackageWrangler(PackageWrangler):

    def __init__(self, session=None):
        PackageWrangler.__init__(self, 
            toplevel_wrangler_target_package_importable_name=None, 
            wrangled_score_package_importable_name_prefix=None,
            session=session)

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
