import os
import types


def import_public_functions(directory, namespace):
   '''List the contents of directory. Import every public function
   from every public module from directory into namespace.'''
   
   module_names = os.listdir(os.path.dirname(directory))
   module_names = [x for x in module_names if x.endswith('.py')] 
   module_names = [x for x in module_names if not x.startswith('_')]
   module_names = [x[:-3] for x in module_names]

   for module_name in module_names:
      module = __import__(module_name, globals = namespace)
      for key, value in vars(module).items( ):
         if not key.startswith('_'):
            if isinstance(value, types.FunctionType):
               namespace[key] = value
