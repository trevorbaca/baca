from baca.scf._MaterialPackageMaker import _MaterialPackageMaker
from baca.scf.MakersProxy import MakersProxy
from baca.scf.MaterialPackageProxy import MaterialPackageProxy
from baca.scf.MenuSpecifier import MenuSpecifier
from baca.scf.DirectoryProxy import DirectoryProxy
import os


class SharedMaterialsProxy(DirectoryProxy, _MaterialPackageMaker):

    ### PUBLIC METHODS ###

    def create_shared_material_package(self, is_interactive=False):
        if is_interactive:
            makers_proxy = MakersProxy()
            return makers_proxy.manage_makers()
        else:
            response = raw_input('Make material interactively? ')
            if response == 'y':
                makers_proxy = MakersProxy()
                makers_proxy.manage_makers()
            else:
                return self._create_materials_package(self.shared_materials_directory)

    def list_shared_material_directories(self):
        shared_material_directories = []
        for x in self.list_shared_material_package_names():
            directory = os.path.join(self.shared_materials_directory, x)
            shared_material_directories.append(directory)
        return shared_material_directories

    def list_shared_material_names(self):
        shared_material_names = []
        for x in self.list_shared_material_package_names():
            shared_material_name = x.replace('_', ' ')
            shared_material_names.append(shared_material_name)
        return shared_material_names
        
    def list_shared_material_package_names(self):
        shared_material_package_names = []
        for x in os.listdir(self.shared_materials_directory):
            if x[0].isalpha():
                directory = os.path.join(self.shared_materials_directory, x)
                if os.path.isdir(directory):
                    initializer = os.path.join(directory, '__init__.py')
                    if os.path.isfile(initializer):
                        shared_material_package_names.append(x)
        return shared_material_package_names

    def make_new_material_by_hand(self):
        self.print_not_implemented()
        self.proceed()

    def manage_shared_materials(self, command_string=None):
        while True:
            menu_specifier = MenuSpecifier()
            menu_specifier.menu_title = 'Shared manterials'
            menu_specifier.items_to_number = self.list_shared_material_names()
            menu_specifier.sentence_length_items.append(('h', '[make new material by hand]'))
            menu_specifier.sentence_length_items.append(('i', 'make new material interactively'))
            key, value = menu_specifier.display_menu()
            if key == 'b':
                return key, None
            elif key == 'h':
                self.make_new_material_by_hand()
            elif key == 'i':
                result = self.create_shared_material_package(is_interactive=True)
                if result == 'studio':
                    return 'S', None
            elif key == 'S':
                return key, None
            else:
                material_name = value
                score_package_name = ''
                material_package_proxy = MaterialPackageProxy(
                    score_package_name, material_name, is_shared_material=True)
                material_package_proxy.score_title = 'Shared materials'
                material_package_proxy.manage_material()
