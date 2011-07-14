import os


class ScorePackageProxy(object):

   def __init__(self, score_package_name):
      self.chunks_directory = os.path.join(score_package_name, 'mus', 'chunks')
      self.materials_directory = os.path.join(score_package_name, 'mus', 'materials')
      self.score_package_directory = os.path.join(os.environ.get('SCORES'), score_package_name)
      self.score_package_name = score_package_name

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, repr(self.score_package_name))

   ## PRIVATE METHODS ##

   def _get_conditional_user_input(self, is_interactive, prompt = None):
      if not is_interactive:
         return True
      response = raw_input(prompt)
      return response.lower( ) == 'y'
      
   ## PUBLIC METHODS ##

   def create_materials_package(self):
      response = raw_input('material name: ')
      print ''
      response = response.lower( )
      response = response.replace(' ', '-')
      material_package_name = '%s_%s' % (self.score_package_name, response)
      print 'package name will be %s.' % material_package_name
      reponse = raw_input('ok? ')
      if not response.lower == 'y':
         return 
      target = os.path.join(self.score_package_name, 'materials', material_package_name)
      if os.path.exists(target):
         raise OSError('directory %s already exists.' % repr(target))
      os.mkdir(target)
      initializer = file(os.path.join(target, '__init__.py'), 'w')
      initializer.write('from %s_output_data import *\n' % material_package_name)
      initializer.close( )
      input_code = '%s_input_code.py' % material_package_name
      input_code = file(os.path.join(target, input_code), 'w')
      input_code.write('')
      input_code.close( )
      output_data = '%s_output_data.py' % material_package_name
      output_data = file(os.path.join(target, output_data), 'w')
      output_data.write('')
      output_data.close( )
      print '%s created.' % material_package_name
      print ''
      
   def create_score_package_directory_structure(self):
      self.fix_score_package_directory_structure(is_interactive = False)

   def fix_score_package_directory_structure(self, is_interactive = True):
      if not os.path.exists(self.score_package_directory):
         raise OSError('directory %s does not exist.' % repr(self.score_package_directory))

      if self.score_package_name == 'poeme':
         return

      target = os.path.join(self.score_package_directory, '__init__.py')
      if not os.path.exists(target):
         prompt = 'Create %s/__init__.py? ' % self.score_package_name
         if self._get_conditional_user_input(is_interactive, prompt = prompt):
            initializer = file(target, 'w')
            initializer.write('')
            initializer.close( )

      target = os.path.join(self.score_package_directory, 'dist')
      if not os.path.exists(target):
         prompt = 'Create %s/dist/? ' % self.score_package_name
         if self._get_conditional_user_input(is_interactive, prompt = prompt):
            os.mkdir(target)

      target = os.path.join(self.score_package_directory, 'dist', 'pdf')
      if not os.path.exists(target):
         prompt = 'Create %s/dist/pdf/? ' % self.score_package_name
         if self._get_conditional_user_input(is_interactive, prompt = prompt):
            os.mkdir(target)

      target = os.path.join(self.score_package_directory, 'etc')
      if not os.path.exists(target):
         prompt = 'Create %s/etc/? ' % self.score_package_name
         if self._get_conditional_user_input(is_interactive, prompt = prompt):
            os.mkdir(target)

      target = os.path.join(self.score_package_directory, 'exg')
      if not os.path.exists(target):
         prompt = 'Create %s/exg/? ' % self.score_package_name
         if self._get_conditional_user_input(is_interactive, prompt = prompt):
            os.mkdir(target)

      target = os.path.join(self.score_package_directory, 'mus')
      if not os.path.exists(target):
         prompt = 'Create %s/mus/? ' % self.score_package_name
         if self._get_conditional_user_input(is_interactive, prompt = prompt):
            os.mkdir(target)

      target = os.path.join(self.score_package_directory, 'mus', '__init__.py')
      if not os.path.exists(target):
         prompt = 'Create %s/mus/__init__.py? ' % self.score_package_name
         if self._get_conditional_user_input(is_interactive, prompt = prompt):
            initializer = file(target, 'w')
            initializer.write('import materials\n')
            initializer.close( )

      target = os.path.join(self.score_package_directory, 'mus', 'chunks')
      if not os.path.exists(target):
         prompt = 'Create %s/mus/chunks? ' % self.score_package_name
         if self._get_conditional_user_input(is_interactive, prompt = prompt):
            os.mkdir(target)

      target = os.path.join(self.score_package_directory, 'mus', 'chunks', '__init__.py')
      if not os.path.exists(target):
         prompt = 'Create %s/mus/chunks/__init__.py? ' % self.score_package_name
         if self._get_conditional_user_input(is_interactive, prompt = prompt):
            initializer = file(target, 'w')
            initializer.write('')
            initializer.close( )

      target = os.path.join(self.score_package_directory, 'mus', 'materials')
      if not os.path.exists(target):
         prompt = 'Create %s/mus/materials? ' % self.score_package_name
         if self._get_conditional_user_input(is_interactive, prompt = prompt):
            os.mkdir(target)

      target = os.path.join(self.score_package_directory, 'mus', 'materials', '__init__.py')
      if not os.path.exists(target):
         prompt = 'Create %s/mus/materials/__init__.py? ' % self.score_package_name
         if self._get_conditional_user_input(is_interactive, prompt = prompt):
            initializer = file(target, 'w')
            initializer.write('')
            initializer.close( )

   def list_materials_packages(self):
      materials_packages = os.listdir(self.materials_directory)
      materials_packages = [x for x in materials_packages if x[0].isalpha( )]
      return materials_packages

   def profile_score_package_directory_structure(self):
      if not os.path.exists(self.score_package_directory):
         raise OSError('directory %s does not exist.' % repr(self.score_package_directory))
      if self.score_package_name == 'poeme':
         return
      print '%s/__init__.py              ' % self.score_package_name,
      print str(os.path.exists(os.path.join(self.score_package_directory, '__init__.py')))
      print '%s/dist/                    ' % self.score_package_name,
      print str(os.path.exists(os.path.join(self.score_package_directory, 'dist')))
      print '%s/dist/pdf                 ' % self.score_package_name,
      print str(os.path.exists(os.path.join(self.score_package_directory, 'dist', 'pdf')))
      print '%s/etc/                     ' % self.score_package_name,
      print str(os.path.exists(os.path.join(self.score_package_directory, 'etc')))
      print '%s/exg/                     ' % self.score_package_name,
      print str(os.path.exists(os.path.join(self.score_package_directory, 'exg')))
      print '%s/mus/                     ' % self.score_package_name,
      print str(os.path.exists(os.path.join(self.score_package_directory, 'mus')))
      print '%s/mus/__init__.py          ' % self.score_package_name,
      print str(os.path.exists(os.path.join(self.score_package_directory, 'mus', '__init__.py')))
      print '%s/mus/chunks/              ' % self.score_package_name,
      print str(os.path.exists(os.path.join(self.score_package_directory, 'mus', 'chunks')))
      print '%s/mus/chunks/__init__.py   ' % self.score_package_name,
      print str(os.path.exists(os.path.join(self.score_package_directory, 'mus', 'chunks', '__init__.py')))
      print '%s/mus/materials/           ' % self.score_package_name,
      print str(os.path.exists(os.path.join(self.score_package_directory, 'mus', 'materials')))
      print '%s/mus/materials/__init__.py' % self.score_package_name,
      print str(os.path.exists(os.path.join(self.score_package_directory, 'mus', 'materials', '__init__.py')))
