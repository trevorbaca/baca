from baca.scf._MaterialPackageMaker import _MaterialPackageMaker
from baca.scf.SCFProxyObject import SCFProxyObject
import os


class SharedMaterialsProxy(SCFProxyObject,_MaterialPackageMaker):

    def __init__(self):
        self.baca_directory = os.environ.get('BACA')
        self.shared_materials_directory = os.path.join(self.baca_directory, 'materials')

    ### PUBLIC METHODS ###

    def create_shared_material_package(self):
        return self._create_materials_package(self.shared_materials_directory)

    def list_shared_material_directories(self):
        shared_material_directories = []
        for x in self.listdir(self.shared_materials_directory):
            shared_material_directories.append(x)
        return shared_material_directories

    def manage_shared_materials(self, command_string = None):
        #self.print_not_implemented()
        is_first_pass = True
        while True:
            is_redraw = False
            if command_string is None:
                if is_first_pass:
                    self.print_menu_title('Shared materials - main menu\n')
                named_pairs = [
                    ('n', 'new'),
                    ]
                kwargs = {'named_pairs': named_pairs, 'indent_level': 1} 
                kwargs.update({'is_nearly': True, 'show_options': is_first_pass})
                key, value = self.display_menu(**kwargs)
            result = None
            if key == 'b':
                return 'b'
            elif key == 'n':
                self.create_shared_material_package()
            elif key == 'q':
                raise SystemExit
            elif key == 'w':
                is_redraw = True
            elif key == 'x':
                self.exec_statement()
            if is_redraw or result == 'b':
                is_first_pass = True
            else:
                is_first_pass = False
            command_string = None
