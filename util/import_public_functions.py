import os


def import_public_functions(directory, namespace, functions = True):
   '''Import into `namespace` every public name in every public 
   module resident in `directory.

   DEPRECATED: `functions` keyword.

   When `functions` is True, do not import public functions.
   When `functions` is False, do import public functions.
   '''
   
   module_names = os.listdir(os.path.dirname(directory))
   module_names = [x for x in module_names if x.endswith('.py')] 
   module_names = [x for x in module_names if not x.startswith('_')]
   module_names = [x[:-3] for x in module_names]

   for module_name in module_names:
      module = __import__(module_name, globals = namespace)
      for key, value in vars(module).items( ):
         if _is_defined_in_module(value, module) or \
            isinstance(value, (list, dict)):
            if not key.startswith('_'):
               namespace[key] = value


def _is_defined_in_module(value, module):

   ## get string name of module
   module_name = module.__name__
   
   ## name string name of module in which value is defined
   value_module_name = getattr(value, '__module__', None)

   ## return True when value is defined in module
   return module_name == value_module_name
