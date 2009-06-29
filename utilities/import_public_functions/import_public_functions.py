import os
import types


def import_public_functions(directory, namespace, 
   functions = True, abjad = False):
   '''Import into `namespace` every public name in every public 
   module resident in `directory.

   When `functions` is True, do not import public functions.
   When `functions` is False, do import public functions.

   When `abjad` is True, import Abjad functions and classes imported by
   `directory` functions and classes.
   When `abjad` is False, import neither Abjad functions nor Abjad classes
   imported by `directory` functions and classes.
   '''
   
   module_names = os.listdir(os.path.dirname(directory))
   module_names = [x for x in module_names if x.endswith('.py')] 
   module_names = [x for x in module_names if not x.startswith('_')]
   module_names = [x[:-3] for x in module_names]

   for module_name in module_names:
      module = __import__(module_name, globals = namespace)
#      for key, value in vars(module).items( ):
#         if not key.startswith('_'):
#            if functions == True:
#               if isinstance(value, types.FunctionType):
#                  namespace[key] = value
#            else:
#               if not isinstance(value, types.ModuleType):
#                  namespace[key] = value
      for key, value in vars(module).items( ):
         if functions == True or not isinstance(value, types.FunctionType):
            if abjad == True or not _is_abjad(value):
               if not key.startswith('_'):
                  namespace[key] = value


def _is_abjad(value):
   path = getattr(value, '__module__', None)
   if path is None:
      path = getattr(value, '__name__', '')
   return path.startswith('abjad.')
