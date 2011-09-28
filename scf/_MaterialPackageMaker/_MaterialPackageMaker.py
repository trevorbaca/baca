import os


class _MaterialPackageMaker(object):

    def __init__(self):
        self.baca_directory = os.environ.get('BACA')
        self.scores_directory = os.environ.get('SCORES')
        self.shared_materials_directory = os.path.join(self.baca_directory, 'materials')

    ### PRIVATE METHODS ###

    def _create_materials_package(self, materials_directory, package_prefix=''):
        response = raw_input('Material name: ')
        print ''
        response = response.lower()
        response = response.replace(' ', '_')
        if package_prefix:
            material_package_name = '%s_%s' % (package_prefix, response)
        else:
            material_package_name = response
        print 'Package name will be %s.\n' % material_package_name
        self.confirm()
        print ''
        target = os.path.join(materials_directory, material_package_name)
        if os.path.exists(target):
            raise OSError('Directory %r already exists.' % target)
        os.mkdir(target)
        response = raw_input('Include visualizer? ')
        print ''
        if response == 'y':
            is_visualized_material = True
        else:
            is_visualized_material = False
        initializer = file(os.path.join(target, '__init__.py'), 'w')
        initializer.write('from output import *\n')
        initializer.close()
        input_file = file(os.path.join(target, 'input.py'), 'w')
        input_file.write('%s = None\n' % material_package_name)
        input_file.write('output_preamble_lines = []\n')
        input_file.write('')
        input_file.close()
        output_file = file(os.path.join(target, 'output.py'), 'w')
        output_file.write('%s = None\n' % material_package_name)
        output_file.write('')
        output_file.close()
        if is_visualized_material:
            visualizer = file(os.path.join(target, 'visualization.py'), 'w')
            visualizer.write('from abjad import *\n')
            visualizer.write('from abjad.tools import layouttools\n')
            visualizer.write('from output import *\n')
            visualizer.write('\n\n')
            visualizer.write('lilypond_file = None\n')
            visualizer.close()
        print 'Created %s ...\n' % material_package_name
