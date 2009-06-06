'''Music-generation functions used in Cary and Sekka.'''


import music
import types

for key, value in music.__dict__.items( ):
   if isinstance(value, types.FunctionType):
      locals( )[key] = value

del key
del music
del types
del value
