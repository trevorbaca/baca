from abjad.tools import iotools
from baca.scf.wranglers.PackageWrangler import PackageWrangler
from baca.scf.proxies.ScorePackageProxy import ScorePackageProxy


class ScorePackageWrangler(PackageWrangler):

    def __init__(self, session=None):
        PackageWrangler.__init__(self, 
            score_external_wrangler_target_package_importable_name=None, 
            score_internal_wrangler_target_package_importable_name_suffix=None,
            session=session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'scores'

    @property
    def current_wrangler_target_directory_name(self):
        return self.scores_directory_name

    @property
    def visible_score_titles_with_years(self):
        result = []
        for score_package_proxy in self.list_visible_wrangled_asset_proxies():
            result.append(score_package_proxy.title_with_year or '(untitled score)')
        return result

    ### PUBLIC METHODS ###

    def get_wrangled_asset_proxy(self, package_importable_name):
        return ScorePackageProxy(package_importable_name, session=self.session)

    def list_visible_wrangled_asset_proxies(self, head=None):
        result = []
        scores_to_show = self.session.scores_to_show
        for asset_proxy in PackageWrangler.list_wrangled_asset_proxies(self, head=head):
            is_mothballed = asset_proxy.get_tag('is_mothballed')
            if scores_to_show == 'all':
                result.append(asset_proxy)
            elif scores_to_show == 'active' and not is_mothballed:
                result.append(asset_proxy)
            elif scores_to_show == 'mothballed' and is_mothballed:
                result.append(asset_proxy)
        return result

    def list_wrangled_asset_menuing_pairs(self, head=None):
        keys = self.list_visible_wrangled_package_short_names()
        bodies = self.visible_score_titles_with_years
        menuing_pairs = zip(keys, bodies)
        tmp = iotools.strip_diacritics_from_binary_string
        menuing_pairs.sort(lambda x, y: cmp(tmp(x[1]), tmp(y[1])))
        return menuing_pairs

    def make_wrangled_asset_interactively(self):
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
        self.make_wrangled_asset(score_package_short_name)
        score_package_proxy = self.get_wrangled_asset_proxy(score_package_short_name)
        score_package_proxy.add_tag('title', title)
        score_package_proxy.year_of_completion = year
