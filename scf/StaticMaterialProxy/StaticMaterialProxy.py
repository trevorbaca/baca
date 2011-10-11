from baca.scf._MaterialPackageProxy import _MaterialPackageProxy
import os


class StaticMaterialProxy(_MaterialPackageProxy):

    ### PUBLIC METHODS ###

    def create(self, has_visualizer=True):
        if os.path.exists(self.directory_name):
            print 'Directory %r already exists.' % self.directory_name
            return False
        os.mkdir(self.directory_name)
        initializer = file(self.initializer, 'w')
        initializer.write('from output import *\n')
        initializer.close()
        input_file = file(self.input_file_name, 'w')
        input_file.write('%s = None\n' % self.package_name)
        input_file.write('output_preamble_lines = []\n')
        input_file.write('')
        input_file.close()
        output_file = file(self.output_file_name, 'w')
        output_file.write('%s = None\n' % self.package_name)
        output_file.write('')
        output_file.close()
        if has_visualizer:
            visualizer = file(self.visualizer_file_name, 'w')
            visualizer.write('from abjad import *\n')
            visualizer.write('from abjad.tools import layouttools\n')
            visualizer.write('from output import *\n')
            visualizer.write('\n\n')
            visualizer.write('lilypond_file = None\n')
            visualizer.close()
