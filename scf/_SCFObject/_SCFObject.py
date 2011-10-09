from abjad.tools import iotools
import datetime
import os
import readline
import subprocess
import time


class _SCFObject(object):
    
    def __init__(self):
        self.baca_directory = os.environ.get('BACA')
        self.scores_directory = os.environ.get('SCORES')
        self.shared_materials_directory = os.path.join(self.baca_directory, 'materials')

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % self.class_name

    ### PUBLIC ATTRIBUTES ###

    @property
    def class_name(self):
        return type(self).__name__

    @property
    def spaced_class_name(self):
        spaced_class_name = iotools.uppercamelcase_to_underscore_delimited_lowercase(self.class_name)
        spaced_class_name = spaced_class_name.replace('_', ' ')
        return spaced_class_name

    @property
    def source_file(self):
        parent_directory = os.path.dirname(os.path.abspath(self.__module__))
        module_path = self.__module__
        module_path = module_path.split('.')[1:]
        path = os.path.join(parent_directory, *module_path)
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

    def get_material_package_proxy(self, importable_module_name):
        from baca.scf.InteractiveMaterialPackageProxy import InteractiveMaterialPackageProxy
        from baca.scf.StaticMaterialPackageProxy import StaticMaterialPackageProxy
        if self.is_interactive_material_package(importable_module_name):
            return InteractiveMaterialPackageProxy(importable_module_name)
        else:
            return StaticMaterialPackageProxy(importable_module_name)

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

    def importable_module_name_to_directory(self, importable_module_name):
        module_parts = importable_module_name.split('.')
        if module_parts[0] == 'baca':
            directory_parts = [os.environ.get('BACA')] + module_parts[1:]
        elif module_parts[0] in os.listdir(os.environ.get('SCORES')):
            directory_parts = [os.environ.get('SCORES')] + module_parts[:]
        else:
            raise ValueError('Unknown importable module name %r.' % importable_module_name)
        directory = os.path.join(*directory_parts)
        return directory

    def directory_to_importable_module_name(self, directory):
        pass

    def is_interactive_material_package(self, importable_module_name):
        from baca.scf.PackageProxy import PackageProxy
        package_proxy = PackageProxy(importable_module_name)
        return package_proxy.has_tag('maker')

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
