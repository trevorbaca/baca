from abjad.tools import iotools
import datetime
import inspect
import os
import readline
import subprocess
import time


class _SCFObject(object):
    
    def __init__(self):
        self._baca_directory_name = os.environ.get('BACA')
        self._baca_materials_directory_name = os.path.join(self.baca_directory_name, 'materials')
        self._baca_materials_package_importable_name = 'baca.materials'
        self._baca_materials_package_short_name = 'materials'
        self._makers_directory_name = os.path.join(self.baca_directory_name, 'makers')
        self._scores_directory_name = os.environ.get('SCORES')

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % self.class_name

    ### PUBLIC ATTRIBUTES ###

    @property
    def Menu(self):
        from baca.scf.menuing import Menu
        return Menu

    @property
    def MenuSection(self):
        from baca.scf.menuing import MenuSection
        return MenuSection

    @property
    def UserInputGetter(self):
        from baca.scf.menuing import UserInputGetter
        return UserInputGetter

    @property
    def baca_directory_name(self):
        return self._baca_directory_name

    @property
    def baca_materials_directory_name(self):
        return self._baca_materials_directory_name

    @property
    def baca_materials_package_importable_name(self):
        return self._baca_materials_package_importable_name

    @property
    def baca_materials_package_short_name(self):
        return self._baca_materials_package_short_name

    @property
    def class_name(self):
        return type(self).__name__

    @property
    def makers_directory_name(self):
        return self._makers_directory_name

    @property
    def scores_directory_name(self):
        return self._scores_directory_name

    @property
    def spaced_class_name(self):
        spaced_class_name = iotools.uppercamelcase_to_underscore_delimited_lowercase(self.class_name)
        spaced_class_name = spaced_class_name.replace('_', ' ')
        return spaced_class_name

    @property
    def source_file_name(self):
        directory_name = self.package_importable_name_to_directory_name(self.__module__)
        source_file_name = directory_name + '.py'
        return source_file_name

    ### PUBLIC METHODS ###

    def annotate_docstring(self):
        print self.source_file_name
        print ''
        self.proceed()

    def clear_terminal(self):
        iotools.clear_terminal()

    def confirm(self):
        response = raw_input('Ok? ')
        if not response.lower() == 'y':
            print ''
            return False
        return True

    def edit_source_file(self):
        command = 'vi %s' % self.source_file_name
        os.system(command)

    # TODO: move to helpers package
    def get_date(self):
        return datetime.date(*time.localtime()[:3])

    # this is weird and should be elimiated
    def get_chunk_proxy(self, package_importable_name):
        from baca.scf.ChunkProxy import ChunkProxy
        return ChunkProxy(package_importable_name)
        
    # this is weird and should be eliminated
    def get_material_proxy(self, package_importable_name):
        from baca.scf.InteractiveMaterialProxy import InteractiveMaterialProxy
        from baca.scf.StaticMaterialProxy import StaticMaterialProxy
        if self.is_interactive_material_package(package_importable_name):
            return InteractiveMaterialProxy(package_importable_name)
        else:
            return StaticMaterialProxy(package_importable_name)
   
    def globally_replace_in_file(self, file_name, old, new):
        file_pointer = file(file_name, 'r')
        new_file_lines = []
        for line in file_pointer.readlines():
            line = line.replace(old, new)
            new_file_lines.append(line)
        file_pointer.close()
        file_pointer = file(file_name, 'w')
        file_pointer.write('\n'.join(new_file_lines))
        file_pointer.close()

    # TODO: move to material proxy or eliminate
    def is_interactive_material_package(self, package_importable_name):
        from baca.scf.PackageProxy import PackageProxy
        package_proxy = PackageProxy(package_importable_name)
        return package_proxy.has_tag('maker')

    def make_menu_title(self, menu_header, menu_body):
        if menu_header is None:
            menu_title = menu_body
        else:
            menu_title = '%s - %s' % (menu_header, menu_body)
        menu_title = menu_title + '\n'
        return  menu_title.capitalize()

    # TODO: move to package proxy
    def package_importable_name_to_directory_name(self, package_importable_name):
        if package_importable_name is None:
            return
        package_importable_name_parts = package_importable_name.split('.')
        if package_importable_name_parts[0] == 'baca':
            directory_parts = [os.environ.get('BACA')] + package_importable_name_parts[1:]
        elif package_importable_name_parts[0] in os.listdir(os.environ.get('SCORES')):
            directory_parts = [os.environ.get('SCORES')] + package_importable_name_parts[:]
        else:
            raise ValueError('Unknown package importable name %r.' % package_importable_name)
        directory = os.path.join(*directory_parts)
        return directory

    # TODO: move to package proxy
    def package_importable_name_to_purview(self, package_importable_name):
        from baca.scf.StudioInterface import StudioInterface
        from baca.scf.ScoreProxy import ScoreProxy
        if package_importable_name is None:
            return
        elif package_importable_name.split('.')[0] == 'baca':
            return StudioInterface()
        elif package_importable_name.split('.')[0] in os.listdir(os.environ.get('SCORES')):
            return ScoreProxy(package_importable_name.split('.')[0])
        else:
            raise ValueError('Unknown package importable name %r.' % package_importable_name)

    def print_not_implemented(self):
        print 'Not yet implemented.\n'
        self.proceed()
        return True, None

    def proceed(self):
        response = raw_input('Press return to continue. ')
        self.clear_terminal()

    def query(self, prompt):
        response = raw_input(prompt)
        return response.lower().startswith('y')

    def raw_input_with_default(self, prompt, default=''):
        if default == 'None':
            default = ''
        readline.set_startup_hook(lambda: readline.insert_text(default))
        try:
           return raw_input(prompt)
        finally:
           readline.set_startup_hook()

    def where(self):
        return inspect.stack()[1]
