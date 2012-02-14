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
