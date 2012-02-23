from baca.scf.proxies.MusicSpecifierModuleProxy import MusicSpecifierModuleProxy
from baca.scf.wranglers.ModuleWrangler import ModuleWrangler
import os


class MusicSpecifierModuleWrangler(ModuleWrangler):

    def __init__(self, session=None):
        ModuleWrangler.__init__(self,
            score_external_asset_container_importable_names=\
                [self.score_external_specifiers_package_importable_name],
            score_internal_asset_container_importable_name_infix=\
                self.score_internal_specifiers_package_importable_name_infix,
            session=session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'music specifiers'

    @property
    def asset_class(self):
        return MusicSpecifierModuleProxy

    ### PUBLIC METHODS ###

    def handle_main_menu_result(self, result):
        if result == 'new':
            self.make_asset_interactively()
        elif result == 'missing':
            self.conditionally_make_asset_container_packages(is_interactive=True)
        elif result == 'profile':
            self.profile_visible_assets()
        else:
            package_proxy = self.get_asset_proxy(result)
            package_proxy.run()

    def make_main_menu(self, head=None):
        menu, section = self.make_menu(where=self.where(), is_parenthetically_numbered=True)
        section.tokens = self.make_visible_asset_menu_tokens(head=head)
        section = menu.make_section()
        section.append(('new', 'new music specifier'))
        hidden_section = menu.make_section(is_hidden=True)
        hidden_section.append(('missing', 'create missing packages'))
        hidden_section.append(('profile', 'profile packages'))
        return menu

    def make_asset_interactively(self):
        getter = self.make_getter()
        getter.append_space_delimited_lowercase_string('music specifier name')
        specifier_name = getter.run()
        if self.backtrack():
            return
        package_short_name = specifier_name.replace(' ', '_')
        self.make_asset(package_short_name)

    # TODO: write test
    def select_specifier_spaced_name_interactively(self, cache=False, clear=True, head=None):
        self.cache_breadcrumbs(cache=cache)
        menu, section = self.make_menu(where=self.where(), is_parenthetically_numbered=True)
        section.tokens = self.make_visible_asset_menu_tokens(head=head)
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
