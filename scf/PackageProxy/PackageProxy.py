from baca.scf.DirectoryProxy import DirectoryProxy
import os


class PackageProxy(DirectoryProxy):

    def __init__(self, directory, importable_module_name):
        DirectoryProxy.__init__(self, directory)
        self.importable_module_name = importable_module_name

    ### PUBLIC ATTRIBUTES ###

    @property
    def creation_date(self):
        pass
        
    @property
    def initializer(self):
        return os.path.join(self.directory, '__init__.py')

    @property
    def package_name(self):
        return self.basename
        
    @property
    def parent_initializer(self):
        return os.path.join(self.parent_directory, '__init__.py')

    ### PUBLIC METHODS ###

    def add_line_to_initializer(self, line):
        file_pointer = file(self.initializer, 'r')
        initializer_lines = set(file_pointer.readlines())
        file_pointer.close()
        initializer_lines.add(line)
        initializer_lines = list(initializer_lines)
        initializer_lines = [x for x in initializer_lines if not x == '\n']
        initializer_lines.sort()
        file_pointer = file(self.initializer, 'w')
        file_pointer.write(''.join(initializer_lines))
        file_pointer.close()

    def add_tag(self, tag_name, tag_value):
        tags = self.get_tags()
        tags[tag_name] = tag_value
        self.write_tags_to_initializer(tags)

    def delete_tag(self, tag_name):
        pass

    def import_attribute_from_initializer(self, attribute_name):
        try:
            exec('from %s import %s' % (self.importable_module_name, attribute_name))
            exec('result = %s' % attribute_name)
            return result
        except ImportError:
            return None

    def get_tag(self, tag_name):
        pass

    def get_tags(self):
        try:
            exec('from %s import tags' % self.importable_module_name)
            return tags
        except ImportError:    
            return {}

    def show_tags(self):
        self.clear_terminal()
        tags = self.get_tags()
        if tags:
            print 'Tags:\n'
            for key in sorted(tags):
                print '%s: %s' % (key, tags[key])
        else:
            print 'No tags found.'
        print ''
        self.proceed()

    def write_tags_to_initializer(self, tags):
        lines = []
        fp = file(self.initializer, 'r')
        found_tags = False
        for line in fp.readlines():
            if line.startswith('tags ='):
                found_tags = True
                lines.append('tags = %s\n' % tags)
            else:
                lines.append(line)
        if not found_tags:
            lines.append('tags = %s\n' % tags)
        fp.close()
        fp = file(self.initializer, 'w')
        fp.write(''.join(lines))
        fp.close()
