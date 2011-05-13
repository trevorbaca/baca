class DynamicsManager(object):
   '''Dynamics manager.
   '''

   ## OVERLOADS ##

   def __repr__(self):
      return '%s( )' % (self.__class__.__name__)

   ## PUBLIC METHODS ##

   @staticmethod
   def is_hairpin_token(arg):
      from abjad.tools import contexttools
      from abjad.tools import spannertools
      if isinstance(arg, tuple) and \
         len(arg) == 3 and \
         (not arg[0] or contexttools.DynamicMark.is_dynamic_name(arg[0])) and \
         spannertools.HairpinSpanner.is_hairpin_shape_string(arg[1]) and \
         (not arg[2] or contexttools.DynamicMark.is_dynamic_name(arg[2])):
         return True
      return False
