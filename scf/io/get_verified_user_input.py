def get_verified_user_input(prompt = 'scf> '):
   
   while True:
      input = raw_input(prompt)
      print ''
      accept = raw_input('Ok? ')
      if accept.lower( ) in ('1', 'y', 'yes'):
         print ''
         return input
      else:
         print ''
