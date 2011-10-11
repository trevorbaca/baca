from baca.scf.DirectoryProxy import DirectoryProxy
from baca.scf.InteractiveMaterialProxy import InteractiveMaterialProxy
from baca.scf.MakerWrangler import MakerWrangler
from baca.scf.menuing import Menu
from baca.scf.PackageProxy import PackageProxy
from baca.scf.StaticMaterialProxy import StaticMaterialProxy
import os


class MaterialWrangler(DirectoryProxy):

    def __init__(self, purview=None):
        from baca.scf.StudioInterface import StudioInterface
        directory = os.path.join(os.environ.get('BACA'), 'materials')
        DirectoryProxy.__init__(self, directory)
        if purview is None:
            self._purview = StudioInterface()
        else:
            self._purview = purview
        self._maker_wrangler = MakerWrangler()

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % self.class_name

    ### PUBLIC ATTRIBUTES ###

    @property
    def has_score_local_purview(self):
        from baca.scf.ScoreProxy import ScoreProxy
        return isinstance(self.purview, ScoreProxy)

    @property
    def has_studio_global_purview(self):
        from baca.scf.StudioInterface import StudioInterface
        return isinstance(self.purview, StudioInterface)    

    @property
    def maker_wrangler(self):
        return self._maker_wrangler

    @property
    def purview(self):
        return self._purview

    ### PUBLIC METHODS ###

    def create_interactive_material_package(self, package_importable_name):
        self.print_not_implemented()
        print 'Interactive material package %s created.\n' % package_importable_name

    def create_interactive_material_package_interactively(self, menu_header=None):
        while True:
            key, value = self.maker_wrangler.select_interactive_maker(menu_header=menu_header)
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

    def create_material_by_hand(self):
        self.print_not_implemented()

    def create_static_material_package(self, package_importable_name, has_visualizer=True):
        static_material_proxy = StaticMaterialProxy(package_importable_name)
        static_material_proxy.create(has_visualizer=has_visualizer)
        print 'Static material package %s created.\n' % package_importable_name

    def create_static_material_package_interactively(self, menu_header=None):
        self.clear_terminal()
        menu_body = 'create static material package'
        menu_title = self.make_menu_title(menu_header, menu_body)
        materials_package_importable_name = self.get_materials_package_importable_name_of_new_material(
            menu_header=menu_title)
        package_short_name = self.get_package_short_name_of_new_material_interactively(menu_header)
        has_visualizer = self.get_visualizer_status_of_new_material_package_interactively()
        package_importable_name = '%s.%s' % (materials_package_importable_name, package_short_name)
        self.create_static_material_package(package_importable_name, has_visualizer)
        self.proceed()

    def get_materials_package_importable_name_of_new_material(self):
        if self.has_studio_global_purview:
            return self.purview.get_materials_package_importable_name_interactively()
        else:
            return self.purview.materials_package_importable_name

    def get_package_short_name_of_new_material_interactively(self):
        response = raw_input('Material name: ')
        print ''
        response = response.lower()
        response = response.replace(' ', '_')
        if self.has_score_local_purview:
            package_short_name = '%s_%s' % (self.purview.package_short_name, response)
        else:
            package_short_name = response
        print 'Short package name will be %s.\n' % package_short_name
        return package_short_name

    def get_visualizer_status_of_new_material_package_interactively(self):
        response = raw_input('Include visualizer? ')
        print ''
        if response == 'y':
            return True
        else:
            return False

    def iterate_shared_material_proxies(self):
        for shared_material_directory in self.list_shared_material_directories():
            package_short_name = os.path.basename(shared_material_directory)
            package_importable_name = 'baca.materials.%s' % package_short_name
            proxy = PackageProxy(package_importable_name)
            yield proxy

    def list_shared_material_directories(self):
        shared_material_directories = []
        for x in self.list_shared_material_package_short_names():
            directory = os.path.join(self.directory, x)
            shared_material_directories.append(directory)
        return shared_material_directories

    def list_shared_material_names(self):
        shared_material_names = []
        for x in self.list_shared_material_package_short_names():
            shared_material_name = x.replace('_', ' ')
            shared_material_names.append(shared_material_name)
        return shared_material_names
        
    def list_shared_material_package_short_names(self):
        shared_material_package_short_names = []
        for x in os.listdir(self.directory):
            if x[0].isalpha():
                directory = os.path.join(self.directory, x)
                if os.path.isdir(directory):
                    initializer = os.path.join(directory, '__init__.py')
                    if os.path.isfile(initializer):
                        shared_material_package_short_names.append(x)
        return shared_material_package_short_names

    def list_shared_material_summaries(self):
        summaries = []
        for shared_material_proxy in self.iterate_shared_material_proxies():
            summary = shared_material_proxy.base_name
            if not shared_material_proxy.has_tag('maker'):
                summary = summary + ' (@)'
            summaries.append(summary)
        return summaries

    def manage_shared_materials(self, menu_header=None, command_string=None):
        while True:
            menu = Menu(client=self, menu_header=menu_header)
            menu.menu_body = 'shared materials'
            menu.items_to_number = self.list_shared_material_summaries()
            menu.sentence_length_items.append(('h', '[create material by hand]'))
            menu.sentence_length_items.append(('i', 'create material interactively'))
            key, value = menu.display_menu()
            if key == 'b':
                return key, None
            elif key == 'h':
                self.create_material_by_hand()
            elif key == 'i':
                menu_title = menu.menu_title
                self.material_wrangler.create_interactie_material_package_interactively(menu_header=menu_title)
            else:
                score_package_importable_name = 'baca.materials'
                material_name = value
                if material_name.endswith('(@)'):
                    package_importable_name = '%s.%s' % (score_package_importable_name, material_name.strip(' (@)'))
                    material_package_proxy = StaticMaterialProxy(package_importable_name)
                else:
                    package_importable_name = '%s.%s' % (score_package_importable_name, material_name)
                    material_package_proxy = InteractiveMaterialProxy(package_importable_name)
                material_package_proxy.score_title = 'Materials'
                material_package_proxy.manage_material(menu_header=menu.menu_title)
