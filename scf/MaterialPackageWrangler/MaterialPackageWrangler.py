from baca.scf._MaterialPackageMaker import _MaterialPackageMaker
from baca.scf.DirectoryProxy import DirectoryProxy
from baca.scf.InteractiveMaterialPackageProxy import InteractiveMaterialPackageProxy
from baca.scf.MakerWrangler import MakerWrangler
from baca.scf.MenuSpecifier import MenuSpecifier
from baca.scf.PackageProxy import PackageProxy
from baca.scf.StaticMaterialPackageProxy import StaticMaterialPackageProxy
import os


class MaterialPackageWrangler(DirectoryProxy, _MaterialPackageMaker):

    #def __init__(self, score_title=None):
    def __init__(self, purview=None):
        from baca.scf.StudioInterface import StudioInterface
        directory = os.path.join(os.environ.get('BACA'), 'materials')
        DirectoryProxy.__init__(self, directory)
        #self.score_title = score_title
        if purview is None:
            self._purview = StudioInterface()
        else:
            self._purview = purview

    ### PUBLIC ATTRIBUTES ###

    @property
    def has_score_local_purview(self):
        from baca.scf.ScorePackageProxy import ScorePackageProxy
        return isinstance(self.purview, ScorePackageProxy)

    @property
    def has_studio_global_purview(self):
        from baca.scf.StudioInterface import StudioInterface
        return isinstance(self.purview, StudioInterface)    

    @property
    def purview(self):
        return self._purview

    ### PUBLIC METHODS ###

    def create_shared_material_package(self, menu_header=None, is_interactive=False):
        if is_interactive:
            makers_proxy = MakerWrangler(score_title=self.score_title)
            return makers_proxy.manage_makers(menu_header=menu_header)
        else:
            response = raw_input('Make material interactively? ')
            if response == 'y':
                makers_proxy = MakerWrangler()
                makers_proxy.manage_makers(menu_header=menu_header)
            else:
                return self._create_materials_package(self.directory)

    def create_interactive_material_package(self, importable_module_name):
        self.print_not_implemented()
        print 'Interactive material package %s created.\n' % package_name

    def create_interactive_material_package_interactively(self):
        self.print_not_implemented()
        self.create_interactive_material_package(importable_module_name)

    def create_static_material_package(self, importable_module_name, has_visualizer=True):
        static_material_proxy = StaticMaterialProxy(importable_module_name)
        static_material_proxy.create(has_visualizer=has_visualizer)
        print 'Static material package %s created.\n' % package_name

    def create_static_material_package_interactively(self):
        materials_directory = self.get_materials_directory_of_new_material()
        material_package_name = self.get_package_name_of_new_material_interactively()
        has_visualizer = self.get_visualizer_status_of_new_material_package_interactively()
        importable_module_name = '%s.%s' % (materials_directory, material_package_name)
        self.create_static_material_package(importable_module_name, has_visualizer)

    def get_materials_directory_of_new_material(self):
        if self.has_studio_global_purview:
            return self.purview.get_materials_directory_interactively()
        else: return self.purview.materials_directory

    def get_package_name_of_new_material_interactively(self):
        response = raw_input('Material name: ')
        print ''
        response = response.lower()
        response = response.replace(' ', '_')
        if self.has_score_local_purview:
            material_package_name = '%s_%s' % (self.purview.package_name, response)
        else:
            material_package_name = response
        print 'Package name will be %s.\n' % material_package_name
        return material_package_name

    def get_visualizer_status_of_new_material_package_interactively(self):
        response = raw_input('Include visualizer? ')
        print ''
        if response == 'y':
            return True
        else:
            return False

    def iterate_shared_material_proxies(self):
        for shared_material_directory in self.list_shared_material_directories():
            module_name = os.path.basename(shared_material_directory)
            importable_module_name = 'baca.materials.%s' % module_name
            proxy = PackageProxy(importable_module_name)
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
            summary = shared_material_proxy.base_name
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
                score_package_name = 'baca.materials'
                material_name = value
                if material_name.endswith('(@)'):
                    importable_module_name = '%s.%s' % (score_package_name, material_name.strip(' (@)'))
                    material_package_proxy = StaticMaterialPackageProxy(importable_module_name)
                else:
                    importable_module_name = '%s.%s' % (score_package_name, material_name)
                    material_package_proxy = InteractiveMaterialPackageProxy(importable_module_name)
                material_package_proxy.score_title = 'Materials'
                material_package_proxy.manage_material(menu_header=menu_specifier.menu_title)
