from baca.scf.ModuleProxy import ModuleProxy
from baca.scf.helpers import safe_import
import os


class MaterialDefinitionModuleProxy(ModuleProxy):

    def __init__(self, module_importable_name, session=None):
        ModuleProxy.__init__(self, module_importable_name, session=session)
        self.output_material_module_import_lines = []
        self.body_lines = []
        self.parse()

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def output_material_module_import_statements(self):
        self.unimport()
        result = safe_import(locals(), self.module_short_name, 'output_material_module_import_statements',
            source_parent_module_importable_name=self.parent_module_importable_name)
        # keep list from persisting between multiple calls to this method
        if result:
            result = list(result)
            return result

    @property
    def sections(self):
        return (
            (self.encoding_directives, False, 0),
            (self.docstring_lines, False, 1),
            (self.setup_statements, True, 0),
            (self.output_material_module_import_lines, True, 2),
            (self.body_lines, False, 0),
            )

    ### PUBLIC METHODS ###

    def edit(self):
        columns = len(self.module_short_name) + 3
        os.system("vi + -c'norm {}l' {}".format(columns, self.full_file_name))

    def import_material_definition(self):
        self.unimport()
        return safe_import(locals(), self.module_short_name, self.material_underscored_name,                 
            source_parent_module_importable_name=self.parent_module_importable_name)

    def parse(self):
        material_definition_module = file(self.full_file_name, 'r')
        encoding_directives = []
        docstring_lines = []
        setup_statements = []
        output_material_module_import_lines = []
        body_lines = []
        current_section = None
        for line in material_definition_module.readlines():
            if line == '\n':
                if current_section == 'docstring':
                    current_section = 'setup'
                else:
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
                output_material_module_import_lines.append(line)
            elif current_section == 'body':
                body_lines.append(line)
            else:
                raise ValueError('{!r}: can not parse line: {!r}.'.format(self.full_file_name, line))
        material_definition_module.close()
        self.encoding_directives = encoding_directives[:]
        self.docstring_lines = docstring_lines[:]
        self.setup_statements = setup_statements[:]
        self.output_material_module_import_lines = output_material_module_import_lines[:]
        self.body_lines = body_lines[:]
