from abjad.tools import mathtools


def partition_nested_into_canonic_parts(expr):
   '''
   abjad> utilities.partition_nested_into_canonic_parts(41)
   (32, 8, 1)

   abjad> utilities.partition_nested_into_canonic_parts(-41)
   (-32, -8, -1)

   abjad> utilities.partition_nested_into_canonic_parts([2, 3, 9, 41])
   [2, 3, 8, 1, 32, 8, 1]

   abjad> utilities.partition_nested_into_canonic_parts([-2, -3, -9, -41])
   [-2, -3, -8, -1, -32, -8, -1]

   abjad> utilities.partition_nested_into_canonic_parts([2, [3, 9], 41])
   [2, [3, 8, 1], 32, 8, 1]
   '''

   if isinstance(expr, (int, long)):
      return mathtools.partition_integer_into_canonic_parts(expr)
   elif isinstance(expr, list):
      result = [ ]
      for subexpr in expr:
         new = partition_nested_into_canonic_parts(subexpr)
         if isinstance(subexpr, int):
            result.extend(new)
         elif isinstance(subexpr, list):
            result.append(new)
      return result
   else:
      raise ValueError
