#def present_menu(values_to_number, additional_pairs = None):
#
#   number_keys = range(1, len(values_to_number) + 1)
#   number_keys = [str(x) for x in number_keys]
#   numbered_pairs = zip(number_keys, values_to_number)
#   
#   for number_key, value_to_number in numbered_pairs:
#      print '%3s: %s' % (number_key, value_to_number)
#   print ''
#
#   all_keys = number_keys[:]
#   all_values = values_to_number[:]
#
#   if additional_pairs:
#      for additional_key, additional_value in additional_pairs:
#         print '%3s: %s' % (additional_key, additional_value)
#         all_keys.append(additional_key)
#         all_values.append(additional_value)
#      print ''
#
#   while True:
#      choice = raw_input('scf> ')
#      print ''
#      if choice in all_keys:
#         break
#    
#   pair_dictionary = dict(zip(number_keys, values_to_number) + additional_pairs)
#   value = pair_dictionary[choice]
#
#   return choice, value
