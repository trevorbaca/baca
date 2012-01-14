from baca.scf.MaterialProxy import MaterialProxy
from baca.scf.PackageProxy import PackageProxy
import os


class MakerProxy(PackageProxy):

    def __init__(self, client_material_package_importable_name, session=None):
        #foo = type(self).__name__
        #mpin = self.makers_package_importable_name
        foo = 'SargassoMeasureMaker'
        mpin = 'baca.scf.makers'
        package_importable_name = '{}.{}'.format(mpin, foo)
        print 'ZZZ: {!r}'.format(package_importable_name)
        PackageProxy.__init__(self, package_importable_name=package_importable_name, session=session)
        self._client = MaterialProxy(client_material_package_importable_name, session=self.session)

    ### READ-ONLY PUBLIC ATTRIBUTES ###
    
    @property
    def breadcrumb(self):
        return self.class_name

    @property
    def client(self):
        return self._client

    @property
    def generic_output_name(self):
        return self._generic_output_name

    @property
    def stylesheet_file_name(self):
        return os.path.join(self.directory_name, 'stylesheet.ly')

    ### PUBLIC METHODS ###

    def create_user_input(self):
        self.print_not_implemented()
        self.proceed()

    def display_user_input(self):
        self.print_not_implemented()
        self.proceed()

    def handle_main_menu_result(self, result):
        if result == 'ind':
            self.display_user_input()
        elif result == 'inc':
            self.create_user_input()
        else:
            raise ValueError
    
    def make_main_menu(self):
        menu, section = self.make_new_menu(where=self.where())
        if self.client.has_user_input:
            section.append(('ind', 'user input - display'))
        else:
            section.append(('inc', 'user input - create'))
        return menu

    def run(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        while True:
            self.append_breadcrumb()
            menu = self.make_main_menu()
            result = menu.run()
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
