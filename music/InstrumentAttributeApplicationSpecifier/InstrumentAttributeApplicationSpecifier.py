class InstrumentAttributeApplicationSpecifier(object):
   '''Class to encapsulate all settings for one instrument playing one score chunk.
   '''

   #def __init__(self, instrument_name, proportions = None, tokens = None):
   def __init__(self, instrument_name, proportions = None, tokens = None):
      #self.instrument_name = instrument_name
      self.proportions = proportions
      self.tokens = tokens

   ## PUBLIC ATTRIBUTES ##

   @apply
   def proportions():
      def fget(self):
         return self._proportions
      def fset(self, proportions):
         if isinstance(proportions, (list, tuple)):
            self._proportions = proportions
         elif proportions is None:
            self._proportions = []
         else:
            raise TypeError
      return property(**locals())

   @apply
   def tokens():
      def fget(self):
         return self._tokens
      def fset(self, tokens):
         if isinstance(tokens, (list, tuple)):
            self._tokens = tokens
         elif tokens is None:
            self._tokens = []
         else:
            raise TypeError
      return property(**locals())
