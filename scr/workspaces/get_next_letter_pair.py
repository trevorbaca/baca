import os


def get_next_letter_pair(directory):
   '''Get first unused letter pair in alphabetic order.'''

   files = os.listdir(directory)
   files = [x for x in files if x[0] == x[1]]
   files = [x for x in files if 'a' <= x[0] <= 'z']
   files.sort( )
   last_file = files[-1]
   last_file_starting_letter = last_file[0]
   if last_file_starting_letter == 'z':
      raise Exception('Twenty-six workspaces in parent directory!')
   else:
      next_letter = chr(ord(last_file_starting_letter) + 1)
   letter_pair = 2 * next_letter

   return letter_pair
