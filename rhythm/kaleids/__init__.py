import os

for name in os.listdir(__path__[0]):
   if os.path.isdir(os.path.join(__path__[0], name)):
      if name[0].isupper( ):
         command = 'from %s import *' % name
         exec(command)
