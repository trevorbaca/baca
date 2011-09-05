from baca.scf.SCFProxyObject import SCFProxyObject
import os


class MaterialPackageProxy(SCFProxyObject):

   def __init__(self, score_package_name, material_name):
      self.score_package_name = score_package_name
      self.material_name = material_name
      self.material_directory = os.path.join(
         os.environ.get('SCORES'), score_package_name, 'mus', 'materials', material_name)
      self.material_input_code = os.path.join(self.material_directory, '%s_input_code.py' % material_name)
      self.material_output_data = os.path.join(self.material_directory, '%s_output_data.py' % material_name)
      self.material_pdf = os.path.join(self.material_directory, '%s.pdf' % material_name)
      self.material_ly = os.path.join(self.material_directory, '%s.ly' % material_name)

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, repr(self.material_name))

   ## PUBLIC METHODS ##

   def edit_material_input_code(self):
      material = os.path.join(self.material_directory)
      command = 'vi %s' % self.material_input_code 
      os.system(command)

   def get_material_output_data(self):
      exec('from %s.mus.materials import %s' % (self.score_package_name, self.material_name))
      exec('result = %s' % self.material_name)
      return result

   def open_material_pdf(self):
      command = 'open %s' % self.material_pdf
      os.system(command)

   def run_startup_interface(self):
      self.print_menu_title('%s - %s' % (self.score_title, self.material_name))
      first_pass = True
      while True:
         named_pairs = [('d', 'data'), ('i', 'input'), ('p', 'pdf'), ('w', 'write')]
         letter, action = self.present_menu(named_pairs = named_pairs, show_options = first_pass)
         if letter == 'b':
            break
         if letter == 'd':
            print self.get_material_output_data()
            print ''
         elif letter == 'i':
            self.edit_material_input_code()
         elif letter == 'p':
            self.open_material_pdf()
         elif letter == 'q':
            raise SystemExit
         elif letter == 'w':
            self.write_material_to_disk()
            print ''
         first_pass = False

   def write_material_to_disk(self):
      command = 'from %s.mus.materials.%s.%s_input_code import %s' % (
         self.score_package_name, self.material_name, self.material_name, self.material_name)
      exec(command)
      exec('_material = %s' % self.material_name)
      output_line = '%s = %s' % (self.material_name, repr(_material))
      output_file = file(self.material_output_data, 'w')
      output_file.write(output_line)
      output_file.close()
      print 'Output written to %s_output_data.py.' % self.material_name
