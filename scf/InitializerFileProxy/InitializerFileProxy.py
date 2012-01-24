from baca.scf.FileProxy import FileProxy
import os


class InitializerFileProxy(FileProxy):

    def __init__(self, full_file_name, session=None):
        FileProxy.__init__(self, full_file_name, session=session)
        self._encoding_directives = []
        self._docstring_lines = []
        self._setup_statements = []
        self._protected_import_statements = []
        self._tag_lines = []
        self._teardown_statements = []
        self.parse()

    ### READ-ONLY PUBLIC ATTRIBUTES ##

    @property
    def content_chunks(self):
        return (
            (self.encoding_directives, True),
            (self.docstring_lines, False),
            (self.setup_statements, True),
            (self.protected_import_statements, True),
            (self.tag_lines, False),
            (self.teardown_statements, True),
            )

    @property
    def docstring_lines(self):
        return self._docstring_lines

    @property
    def encoding_directives(self):
        return self._encoding_directives

    @property
    def format(self):
        return ''.join(self.formatted_lines)

    @property
    def formatted_lines(self):
        lines = []
        for content_collection, is_sorted in self.content_chunks:
            if content_collection:
                content_collection = content_collection[:]
                if is_sorted:
                    content_collection.sort()
                lines.extend(content_collection)
                lines.append('\n')
        if lines: 
            lines.pop()
            lines[-1] = lines[-1].strip()
        return lines

    @property
    def protected_import_statements(self):
        return self._protected_import_statements

    @property
    def setup_statements(self):
        return self._setup_statements

    @property
    def tag_lines(self):
        return self._tag_lines

    @property
    def teardown_statements(self):
        return self._teardown_statements

    ### PUBLIC METHODS ###

    def display(self):
        print self.format

    def parse(self, initializer_file_name=None):
        if initializer_file_name is None:
            initializer_file_name = self.full_file_name
        initializer = file(initializer_file_name, 'r')
        encoding_directives = []
        docstring_lines = []
        setup_statements = []
        protected_import_statements = []
        tag_lines = []
        teardown_statements = []
        current_section = None
        for line in initializer.readlines():
            if line == '\n':
                continue
            elif line.startswith('# -*-'):
                current_section = 'encoding'
            elif line.startswith("'''"):
                current_section = 'docstring'
            elif line.startswith(('from', 'import')):
                current_section = 'setup'
            elif line.startswith('tags ='):
                current_section = 'tags'
            elif line.startswith('safe_import'):
                current_section = 'protected imports'
            elif line.startswith('del'):
                current_section = 'teardown'
            if current_section == 'encoding':
                encoding_directives.append(line)
            elif current_section == 'docstring':
                docstring_lines.append(line)
            elif current_section == 'setup':
                setup_statements.append(line)
            elif current_section == 'tags':
                tag_lines.append(line)
            elif current_section == 'protected imports':
                protected_import_statements.append(line)
            elif current_section == 'teardown':
                teardown_statements.append(line)
            else:
                raise ValueError('{!r}: can not parse line: {!r}.'.format(self.full_file_name, line))
        initializer.close()
        self._encoding_directives = encoding_directives
        self._docstring_lines = docstring_lines
        self._setup_statements = setup_statements
        self._protected_import_statements = protected_import_statements
        self._tag_lines = tag_lines
        self._teardown_statements = teardown_statements

    def view(self):
        os.system('vi -R {}'.format(self.full_file_name))

    def write_to_disk(self):
        initializer = file(self.full_file_name, 'w')
        initializer.write(self.format)
