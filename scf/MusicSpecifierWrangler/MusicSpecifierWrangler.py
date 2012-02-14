from baca.scf.PackageWrangler import PackageWrangler


class MusicSpecifierWrangler(PackageWrangler):

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
