from baca.scf.proxies.FileProxy import FileProxy


class ParsableFileProxy(FileProxy):

    def __init__(self, full_file_name, session=None):
        FileProxy.__init__(self, full_file_name, session=session)    
        self.encoding_directives = []
        self.docstring_lines = []
        self.setup_statements = []
        self.teardown_statements = []

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def format(self):
        return ''.join(self.formatted_lines)

    @property
    def formatted_lines(self):
        lines = []
        for section, is_sorted, blank_line_count in self.sections:
            if section:
                section = section[:]
                if is_sorted:
                    section.sort()
                lines.extend(section)
                for x in range(blank_line_count):
                    lines.append('\n')
        if lines:
            lines[-1] = lines[-1].strip('\n')
        return lines

    @property
    def is_parsable(self):
        return self.parse()

    @property
    def is_readable(self):
        if self.is_parsable:
            if self.is_exceptionless:
                return True
        return False

    ### PUBLIC METHODS ###

    def print_to_screen(self):
        print self.format

    def write_to_disk(self):
        initializer = file(self.full_file_name, 'w')
        initializer.write(self.format)
