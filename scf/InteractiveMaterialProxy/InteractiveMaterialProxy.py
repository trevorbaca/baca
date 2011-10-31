from baca.scf.MaterialProxy import MaterialProxy


class InteractiveMaterialProxy(MaterialProxy):

    ### PUBLIC METHODS ###

    def create(self, package_importable_name):
        self.print_not_implemented()
        print 'Interactive material package %s created.\n' % package_importable_name

    def create_interactively(self, menu_header=None):
        while True:
            key, value = self.maker_wrangler.select_maker(menu_header=menu_header)
            if value is None:
                break
            else:
                maker = value
            maker.score = self
            result = maker.edit_interactively(menu_header=menu_header)
            if result:
                break
        self.proceed()
        return True, None
