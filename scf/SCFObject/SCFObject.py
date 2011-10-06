from abjad.tools import iotools
import os
import readline
import subprocess


class SCFObject(object):
    
    def __init__(self):
        self.baca_directory = os.environ.get('BACA')
        self.scores_directory = os.environ.get('SCORES')
        self.shared_materials_directory = os.path.join(self.baca_directory, 'materials')

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % type(self).__name__

    ### PUBLIC ATTRIBUTES ###

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
