#! /usr/bin/env python
import os
os.system('ajv clean .')


for directory, subdirectories, file_names in os.walk('.'):
    for file_name in file_names:
        search_string = 'to_top_level'
        replacement_string = 'home'
        if search_string in file_name:
            old_path = os.path.join(directory, file_name)
            new_path = old_path.replace(search_string, replacement_string)
            command = 'git mv {} {}'.format(old_path, new_path)
            #print command
            os.system(command)