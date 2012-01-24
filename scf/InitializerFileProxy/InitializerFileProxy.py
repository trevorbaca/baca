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
            (self._encoding_directives, True),
            (self._docstring_lines, False),
            (self._setup_statements, True),
            (self._protected_import_statements, True),
            (self._tag_lines, False),
            (self._teardown_statements, True),
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

    def add_protected_import_statement(self, source_module_short_name, source_attribute_name):
        import_statement = 'safe_import(globals(), {!r}, {!r})'
        import_statement = import_statement.format(source_module_short_name, source_attribute_name)
        self.protected_import_statements.append(import_statement)
        
    def clear(self):
        for content_chunk, is_sorted in self.content_chunks:
            content_chunk[:] = []

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

    def pprint_tags(self, tags):
        if tags:
            lines = []
            for key, value in sorted(tags.iteritems()):
                key = repr(key)
                if hasattr(value, '_get_multiline_repr'):
                    repr_lines = value._get_multiline_repr(include_tools_package=True)
                    value = '\n    '.join(repr_lines)
                    lines.append('({}, {})'.format(key, value))
                else:
                    value = getattr(value, '_repr_with_tools_package', repr(value))
                    lines.append('({}, {})'.format(key, value))
            lines = ',\n    '.join(lines)
            result = 'tags = OrderedDict([\n    {}])'.format(lines)
        else:
            result = 'tags = OrderedDict([])'
        return result

    def view(self):
        os.system('vi -R {}'.format(self.full_file_name))

    def write_stub_to_disk(self, tags=None):
        self.clear()
        initializer.setup_statements.append('from collections import OrderedDict\n')
        tag_lines = initializer.pprint_tags(tags)
        initializer.tag_lines.extend(tag_lines[:])
        initializer.write_to_disk()

    def write_to_disk(self):
        initializer = file(self.full_file_name, 'w')
        initializer.write(self.format)
