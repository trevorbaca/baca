from baca.scf._MaterialPackageMaker import _MaterialPackageMaker
from baca.scf.DirectoryProxy import DirectoryProxy
from baca.scf.PackageProxy import PackageProxy
from baca.scf.MakersWrangler import MakersWrangler
from baca.scf.MaterialPackageProxy import MaterialPackageProxy
from baca.scf.MenuSpecifier import MenuSpecifier
import os


class MaterialPackageWrangler(DirectoryProxy, _MaterialPackageMaker):

    def __init__(self, score_title=None):
        directory = os.path.join(os.environ.get('BACA'), 'materials')
        DirectoryProxy.__init__(self, directory)
        self.score_title = score_title

    ### PUBLIC METHODS ###

    def create_shared_material_package(self, menu_header=None, is_interactive=False):
        if is_interactive:
            makers_proxy = MakersWrangler(score_title=self.score_title)
            return makers_proxy.manage_makers(menu_header=menu_header)
        else:
            response = raw_input('Make material interactively? ')
            if response == 'y':
                makers_proxy = MakersWrangler()
                makers_proxy.manage_makers(menu_header=menu_header)
            else:
                return self._create_materials_package(self.directory)

    def iterate_shared_material_proxies(self):
        for shared_material_directory in self.list_shared_material_directories():
            module_name = os.path.basename(shared_material_directory)
            importable_module_name = 'baca.materials.%s' % module_name
            proxy = PackageProxy(shared_material_directory, importable_module_name)
            yield proxy

    def list_shared_material_directories(self):
        shared_material_directories = []
        for x in self.list_shared_material_package_names():
            directory = os.path.join(self.directory, x)
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
        for x in os.listdir(self.directory):
            if x[0].isalpha():
                directory = os.path.join(self.directory, x)
                if os.path.isdir(directory):
                    initializer = os.path.join(directory, '__init__.py')
                    if os.path.isfile(initializer):
                        shared_material_package_names.append(x)
        return shared_material_package_names

    def list_shared_material_summaries(self):
        summaries = []
        for shared_material_proxy in self.iterate_shared_material_proxies():
            summary = shared_material_proxy.basename
            if not shared_material_proxy.has_tag('maker'):
                summary = summary + ' (@)'
            summaries.append(summary)
        return summaries

    def make_new_material_by_hand(self):
        self.print_not_implemented()

    def manage_shared_materials(self, menu_header=None, command_string=None):
        while True:
            menu_specifier = MenuSpecifier(menu_header=menu_header)
            menu_specifier.menu_body = 'materials'
            menu_specifier.items_to_number = self.list_shared_material_summaries()
            menu_specifier.sentence_length_items.append(('h', '[make new material by hand]'))
            menu_specifier.sentence_length_items.append(('i', 'make new material interactively'))
            key, value = menu_specifier.display_menu()
            if key == 'b':
                return key, None
            elif key == 'h':
                self.make_new_material_by_hand()
            elif key == 'i':
                result = self.create_shared_material_package(
                    menu_header=menu_specifier.menu_title, is_interactive=True)
            else:
                material_name = value.strip(' (@)')
                score_package_name = ''
                material_package_proxy = MaterialPackageProxy(
                    score_package_name, material_name, is_shared_material=True)
                material_package_proxy.score_title = 'Materials'
                material_package_proxy.manage_material(menu_header=menu_specifier.menu_title)
