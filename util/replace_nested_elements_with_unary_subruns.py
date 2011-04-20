def replace_nested_elements_with_unary_subruns(l):
   '''
   Replace positive integers with 1-sequences;
   flat or nested w.

   >>> l = [1, 2, 2, -4]
   >>> util.replace_nested_elements_with_unary_subruns(l)
   [1, 1, 1, 1, 1, -4]

   >>> util.replace_nested_elements_with_unary_subruns(l, target = 'negatives')
   [1, 2, 2, -1, -1, -1, -1]

   >>> util.replace_nested_elements_with_unary_subruns(l, target = 'all')
   [1, 1, 1, 1, 1, -1, -1, -1, -1]

   >>> w = [[1, 3, -4], [1, 2, -2, -4]]
   >>> util.replace_nested_elements_with_unary_subruns(w)
   [[1, 1, 1, 1, -4], [1, 1, 1, -2, -4]]
   '''

   result = [ ]

#   # two-dimensional w
#   if isinstance(w[0], list):
#      for sublist in w:
#         result.append(util.replace_nested_elements_with_unary_subruns(sublist, target = target))
#   # one-dimensional w
#   else:
#      for element in reversed(w):
#         if target == 'positives':
#            if element < 0:
#               result.insert(0, element)
#            else:
#               result[0:0] = [1] * element 
#         elif target == 'negatives':
#            if element > 0:
#               result.insert(0, element)
#            else:
#               result[0:0] = [-1] * abs(element)
#         elif target == 'all':
#            if element == 0:
#               result.insert(0, element)
#            else:
#               result[0:0] = [mathtools.sign(element) * 1] * abs(element)
#         else:
#            print 'Unkown target %s.' % target
#            raise ValueError
#      
#   return result

   result = [ ]

   for sublist in l:
      new_sublist = [ ]
      for element in sublist:
         print element
         if 0 < element:
            new_sublist.extend([1] * element)
         else:
            new_sublist.append(element)
      result.append(new_sublist)

   return result
