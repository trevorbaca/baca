from baca.scf.proxies.MusicSpecifierModuleProxy import MusicSpecifierModuleProxy
from baca.scf.wranglers.PackageWrangler import PackageWrangler
import os


class MusicSpecifierModuleWrangler(PackageWrangler):

    def __init__(self, session=None):
        PackageWrangler.__init__(self,
            score_external_wrangler_target_package_importable_name= \
                self.score_external_specifiers_package_importable_name,
            score_internal_wrangler_target_package_importable_name_suffix= \
                self.score_internal_specifiers_package_importable_name_suffix,
            session=session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'music specifiers'

    ### PUBLIC METHODS ###

    def get_wrangled_asset_proxy(self, package_importable_name):
        return MusicSpecifierModuleProxy(package_importable_name, session=self.session)

    def handle_main_menu_result(self, result):
        if result == 'new':
            self.make_wrangled_package_interactively()
        elif result == 'missing':
            self.conditionally_make_wrangler_target_packages(is_interactive=True)
        elif result == 'profile':
            self.profile_visible_wrangled_package_structures()
        else:
            package_proxy = self.get_wrangled_asset_proxy(result)
            package_proxy.run()

    def make_main_menu(self, head=None):
        menu, section = self.make_menu(where=self.where(), is_parenthetically_numbered=True)
        section.tokens = self.list_wrangled_asset_menuing_pairs(head=head)
        section = menu.make_section()
        section.append(('new', 'new music specifier'))
        hidden_section = menu.make_section(is_hidden=True)
        hidden_section.append(('missing', 'create missing packages'))
        hidden_section.append(('profile', 'profile packages'))
        return menu

    def make_wrangled_package_interactively(self):
        getter = self.make_getter()
        getter.append_space_delimited_lowercase_string('music specifier name')
        specifier_name = getter.run()
        if self.backtrack():
            return
        package_short_name = specifier_name.replace(' ', '_')
        self.make_wrangled_package(package_short_name)

    def run(self, user_input=None, clear=True, cache=False):
        self.conditionally_make_wrangler_target_packages()
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.push_breadcrumb()
            menu = self.make_main_menu()
            result = menu.run(clear=clear)
            if self.backtrack():
                break
            elif not result:
                self.pop_breadcrumb()
                continue
            self.handle_main_menu_result(result)
            if self.backtrack():
                break
            self.pop_breadcrumb()
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)

    # TODO: write test
    def select_specifier_spaced_name_interactively(self, cache=False, clear=True, head=None):
        self.cache_breadcrumbs(cache=cache)
        menu, section = self.make_menu(where=self.where(), is_parenthetically_numbered=True)
        section.tokens = self.list_wrangled_asset_menuing_pairs(head=head)
        while True:
            self.push_breadcrumb('select music specifier')
            result = menu.run(clear=clear)
            if self.backtrack():
                break
            elif not result:
                self.pop_breadcrumb()
                continue
            else:
                break
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)
        return result
