from abjad.tools import iotools
import datetime
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
        self._scores_directory_name = os.environ.get('SCORES')

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % self.class_name

    ### PUBLIC ATTRIBUTES ###

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
    def baca_materials_short_pacakge_name(self):
        return self._baca_materials_package_short_name

    @property
    def class_name(self):
        return type(self).__name__

    @property
    def scores_directory_name(self):
        return self._scores_directory_name

    @property
    def spaced_class_name(self):
        spaced_class_name = iotools.uppercamelcase_to_underscore_delimited_lowercase(self.class_name)
        spaced_class_name = spaced_class_name.replace('_', ' ')
        return spaced_class_name

    @property
    def source_file(self):
        parent_directory_name = os.path.dirname(os.path.abspath(self.__module__))
        module_path = self.__module__
        module_path = module_path.split('.')[1:]
        path = os.path.join(parent_directory_name, *module_path)
        source_file = path + '.py'
        return source_file

    ### PUBLIC METHODS ###

    def annotate_docstring(self):
        print self.source_file
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
        command = 'vi %s' % self.source_file
        os.system(command)

    def get_date(self):
        return datetime.date(*time.localtime()[:3])

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

    def package_importable_name_to_directory(self, package_importable_name):
        package_importable_name_parts = package_importable_name.split('.')
        if package_importable_name_parts[0] == 'baca':
            directory_parts = [os.environ.get('BACA')] + package_importable_name_parts[1:]
        elif package_importable_name_parts[0] in os.listdir(os.environ.get('SCORES')):
            directory_parts = [os.environ.get('SCORES')] + package_importable_name_parts[:]
        else:
            raise ValueError('Unknown importable module name %r.' % package_importable_name)
        directory = os.path.join(*directory_parts)
        return directory

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
