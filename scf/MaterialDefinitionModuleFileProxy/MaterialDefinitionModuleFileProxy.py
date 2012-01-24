from baca.scf.FileProxy import FileProxy


class MaterialDefinitionModuleFileProxy(FileProxy):

    def __init__(self, full_file_name, session=None):
        FileProxy.__init__(self, full_file_name, session=session)
        # TODO: rename from statements to lines
        self._output_material_module_import_statements = []
        self._body_lines = []
        self.parse()

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def body_lines(self):
        return self._body_lines

    @property
    def output_material_module_import_statements(self):
        return self._output_material_module_import_statements

    ### PUBLIC METHODS ###

    # TODO: customize with has_blank_line value
    @property
    def content_chunks(self):
        return (
            (self._encoding_directives, True,),
            (self._docstring_lines, False),
            (self._setup_statements, True),
            (self._output_material_module_import_statements, True),
            (self._body_lines, False),
            )

    def parse(self):
        definition_module = file(self.full_file_name, 'r')
        encoding_directives = []
        docstring_lines = []
        setup_statements = []
        output_material_module_import_statements = []
        body_lines = []
        current_section = None
        for line in definition_module.readlines():
            if line == '\n':
                current_section = 'body'
                continue
            elif line.startswith('# -*-'):
                current_section = 'encoding'
            elif line.startswith("'''"):
                current_section = 'docstring'
            elif line.startswith(('from', 'import')):
                current_section = 'setup'
            elif line.startswith('output_material_module_import_statements'):
                current_section = 'output material module imports'
            if current_section == 'encoding':
                encoding_directives.append(line)
            elif current_section == 'docstring':
                docstring_lines.append(line)
            elif current_section == 'setup':
                setup_statements.append(line)
            elif current_section == 'output material module imports':
                output_material_module_import_statements.append(line)
            elif current_section == 'body':
                body_lines.append(line)
            else:
                raise ValueError('{!r}: can not parse line: {!r}.'.format(self.full_file_name, line))
        definition_module.close()
        self._encoding_directives = encoding_directives
        self._docstring_lines = docstring_lines
        self._setup_statements = setup_statements
        self._output_material_module_import_statements = output_material_module_import_statements
        self._body_lines = body_lines
