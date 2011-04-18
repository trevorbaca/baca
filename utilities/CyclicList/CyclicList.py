class CyclicList(list):

   ## OVERLOADS ##

   def __getitem__(self, expr):
      if isinstance(expr, int):
         return list.__getitem__(self, expr % len(self))
      else:
         raise NotImplementedError('TODO: implement slice-handling.')
