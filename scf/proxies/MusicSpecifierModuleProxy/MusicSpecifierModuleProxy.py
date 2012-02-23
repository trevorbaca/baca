from baca.scf.proxies.ModuleProxy import ModuleProxy
import os


class MusicSpecifierModuleProxy(ModuleProxy):

    def __init__(self, module_importable_name, session=None):
        ModuleProxy.__init__(self, module_importable_name, session=session)
        self._music_specifier_editor = MusicSpecifierEditor(session=self.session)
        self.music_specifier_lines = []
        #self.conditionally_make_file()
        self.parse() 

    ### READ-ONLY ATTRIBUTES ###

    @property
    def music_specifier_editor(self):
        return self._music_specifier_editor

    @property
    def music_specifier_in_memory(self):
        if self._music_specifier_in_memory is not None:
            return self._music_specifier_in_memory
        self.read_music_specifier_from_disk()
        return self._music_specifier_in_memory

    @property
    def sections(self):
        return (
            (self.encoding_directives, False, 0),
            (self.docstring_lines, False, 1),
            (self.setup_statements, True, 2),
            (self.music_specifier_lines, False, 0),
            )

    ### PUBLIC METHODS ###

    # MusicSpecifierEditor must handle reading from disk and writing to disk
    def edit_music_specifier_at_number(self, number, include_newline=True):
        number = int(number)
        self.music_specifier_editor.edit_at_number(number)
        
    def fix(self):
        self.print_not_implemented()

    def handle_main_menu_result(self, result):
        assert isinstance(result, str)
        if result == 'rm':
            self.remove()
        elif mathtools.is_integer_equivalent_expr(result):
            self.edit_music_specifier_at_number(result, include_newline=False)
        else:
            raise ValueError

    def make_main_menu(self):
        menu, section = self.make_menu(where=self.where(), is_keyed=False, is_parenthetically_numbered=True)
        section.tokens = self.make_music_specifier_menu_tokens()
        section = menu.make_section()
        section.append(('rm', 'remove music specifier'))
        return menu

    def make_music_specifier_menu_tokens(self):
        return self.music_specifier_editor.make_menu_tokens()

    def parse(self):
        is_parsable = True
        output_material_module = file(self.path_name, 'r')
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
        if os.path.exists(self.path_name):
            file_pointer = open(self.path_name, 'r')
            file_contents_string = file_pointer.read()
            file_pointer.close()
            exec(file_contents_string)
            #return locals().get('music_specifier', None)
            self._music_speciifer_in_memory = music_specifier

    def run(self, user_input=None, clear=True, cache=False):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.push_breadcrumb()
            menu = self.make_main_menu()
            result = menu.run(clear=clear)
            if self.backtrack():
                break
            elif not result:
                self.pop_breacrumb()
                continue
            self.handle_main_menu_result(result)
            if self.backtrack():
                break
            self.pop_breadcrumb()
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)

    #def write_music_specifier_to_disk(self, music_specifier_in_memory):
    def write_music_specifier_to_disk(self):
        self.setup_statements[:] = self.conditionally_add_terminal_newlines(
            self.music_specifier_in_memory.music_specifier_module_import_statements)[:]
        self.user_input_wrapper_lines[:] = self.conditionally_add_terminal_newlines(
            self.music_specifier_in_memory.formatted_lines)
        ModuleProxy.write_to_disk(self)
