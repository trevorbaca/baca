from baca.scf.PackageWrangler import PackageWrangler


class MusicSpecifierModuleProxyWrangler(PackageWrangler):

    def __init__(self, session=None):
        PackageWrangler.__init__(self,
            toplevel_global_package_importable_name=self.studio_specifiers_package_importable_name,
            toplevel_score_package_importable_name_body=self.score_specifiers_package_importable_name_body,
            session=session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'specifiers'

    @property
    def specifiers_directory_name(self):
        return self.package_importable_name_to_directory_name(self.specifiers_package_importable_name)

    @property
    def specifiers_package_importable_name(self):
        if self.session.is_in_score:
            score_package_short_name = self.session.current_score_package_importable_name
            return self.dot_join([score_package_short_name, self.toplevel_score_package_importable_name_body])
        else:
            return self.toplevel_global_package_importable_name
            
    ### PUBLIC METHODS ###

    def handle_main_menu_result(self, result):
        if result == 'new':
            self.make_specifier_interactively()
        else:
            specifier_module_name = self.dot_join(self.specifiers_package_importable_name, result)
            specifier_proxy = MusicSpecifierModuleProxy(specifier_module_importable_name, session=self.session)
            specifier_proxy.run()

    def make_main_menu(self):
        menu, section = self.make_menu(where=self.where(), is_parenthetically_numbered=True)
        section.tokens = self.specifier_file_names
        section.make_section()
        section.append(('new', 'new specifier'))
        return menu

    def make_specifier_interactively(self):
        getter = self.make_getter()
        getter.append_space_delimited_lowercase_string('specifier name')
        specifier_name = getter.run()
        if self.backtrack():
            return
        specifier_module_short_name = specifier_name.replace(' ', '_')
        specifier_module_importable_name = self.join(
            self.specifiers_package_importable_name, specifier_module_short_name)
        specifier_module_proxy = MusicSpecifierModuleProxy(specifier_module_importable_name)
        specifier_module_proxy.run()

    def run(self, user_input=None, clear=True, cache=False):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.push_breadcrumb()
            menu = make_main_menu()
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
    def select_specifier_spaced_name_interactively(self, clear=True, cache=False):
        self.cache_breadcrumbs(cache=cache)
        menu, section = self.make_menu(where=self.where(), is_parenthetically_numbered=True)
        section.tokens = self.specifier_spaced_names
        while True:
            self.push_breadcrumb('select specifier')
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
