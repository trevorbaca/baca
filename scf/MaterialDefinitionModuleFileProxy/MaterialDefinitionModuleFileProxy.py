from baca.scf.FileProxy import FileProxy


class MaterialDefinitionModuleFileProxy(FileProxy):

    def __init__(self, full_file_name, session=None):
        FileProxy.__init__(self, full_file_name, session=session)
        self._output_material_module_import_statements = []
        self._body_lines = []

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def body_lines(self):
        return self._body_lines

    @property
    def output_material_module_import_statements(self):
        return self._output_material_module_import_statements

    ### PUBLIC METHODS ###

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
        self.print_not_implemented()
