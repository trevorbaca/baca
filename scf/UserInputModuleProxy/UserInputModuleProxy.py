from baca.scf.ModuleProxy import ModuleProxy
from baca.scf.helpers import safe_import


class UserInputModuleProxy(ModuleProxy):

    def __init__(self, module_importable_name, session=None):
        ModuleProxy.__init__(self, module_importable_name, session=session)
        self.user_input_wrapper_lines = []
        self.parse()

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def has_complete_user_input_wrapper(self):
        user_input_wrapper = self.import_user_input_wrapper()
        if user_input_wrapper is not None:
            return user_input_wrapper.is_complete
        return False
        
    @property
    def sections(self):
        return (
            (self.encoding_directives, False, 0),
            (self.docstring_lines, False, 1),
            (self.setup_statements, True, 2),
            (self.user_input_wrapper_lines, False, 0),
            )
            
    ### PUBLIC METHODS ###

    def import_user_input_wrapper(self):
        self.unimport()
        return safe_import(locals(), self.module_short_name, 'user_input',
            source_parent_module_importable_name=self.parent_module_importable_name)

    def parse(self):
        output_material_module = file(self.full_file_name, 'r')
        encoding_directives = []
        docstring_lines = []
        setup_statements = []
        user_input_wrapper_lines = []
        current_section = None
        for line in output_material_module.readlines():
            if line == '\n':
                if current_section == 'docstring':
                    current_section = 'setup'
                else:
                    current_section = 'user input wrapper'
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
            elif current_section == 'user input wrapper':
                user_input_wrapper_lines.append(line)
            else:
                raise ValueError('{!r}: can not parse line: {!r}.'.format(self.full_file_name, line))
        output_material_module.close()
        self.encoding_directives = encoding_directives
        self.docstring_lines = docstring_lines
        self.setup_statements = setup_statements
        self.user_input_wrapper_lines = user_input_wrapper_lines

    def write_stub_to_disk(self, prompt=True):
        self.clear()
        self.setup_statements.append('from baca.scf import UserInputWrapper\n')
        self.body_lines.append('user_input = UserInputWrapper([])]\n')
        self.write_to_disk()
        self.proceed('stub user input module written to disk.')

    def write_to_disk(self, user_input_wrapper):
        self.user_input_wrapper_lines[:] = user_input_wrapper.formatted_lines
        ModuleProxy.write_to_disk(self) 
