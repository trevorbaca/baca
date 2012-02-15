from baca.scf.ModuleProxy import ModuleProxy
import os


class MusicSpecifierModuleProxy(ModuleProxy):

    def __init__(self, module_importable_name, session=None):
        ModuleProxy.__init__(self, module_importable_name, session=session)
        self.music_specifier_lines = []
        self.parse() 

    ### READ-ONLY ATTRIBUTES ###

    @property
    def sections(self):
        return (
            (self.encoding_directives, False, 0),
            (self.docstring_lines, False, 1),
            (self.setup_statements, True, 2),
            (self.music_specifier_lines, False, 0),
            )

    ### PUBLIC METHODS ###

    def parse(self):
        is_parsable = True
        output_material_module = file(self.full_file_name, 'r')
        encoding_directives = []
        docstring_lines = []
        setup_statements = []
        music_specifier_lines = []
        current_section = None
        for line in output_material_module.readlines():
            if line == '\n':
                if current_section == 'docstring':
                    current_section = 'setup'
                else:
                    current_section = 'music specifier'
                continue
            elif line.startswith('# -*-'):
                current_section = 'encoding'
            elif line.startswith("'''"):
                current_section = 'docstring'
            elif line.startswith(('from', 'import')):
                current_section = 'setup'
            if current_section == 'encoding':
                encoding_directives.append(line)
            elif current_section == 'docstring':
                docstring_lines.append(line)
            elif current_section == 'setup':
                setup_statements.append(line)
            elif current_section == 'music specifier':
                user_input_wrapper_lines.append(line)
            else:
                is_parsable = False
        output_material_module.close()
        self.encoding_directives = encoding_directives
        self.docstring_lines = docstring_lines
        self.setup_statements = setup_statements
        self.music_specifier_lines = music_specifier_lines
        return is_parsable

    def read_music_specifier_from_disk(self):
        self.unimport()
        if os.path.exists(self.full_file_name):
            file_pointer = open(self.full_file_name, 'r')
            file_contents_string = file_pointer.read()
            file_pointer.close()
            exec(file_contents_string)
            return locals().get('music_specifier', None)

    def write_music_specifier_to_disk(self, music_specifier_in_memory):
        self.setup_statements[:] = self.conditionally_add_terminal_newlines(
            music_specifier_in_memory.music_specifier_module_import_statements)[:]
        self.user_input_wrapper_lines[:] = self.conditionally_add_terminal_newlines(
            music_specifier_in_memory.formatted_lines)
        ModuleProxy.write_to_disk(self)
