# -*- coding: utf-8 -*-
import os


def get_next_file_number(output_directory, extension):
    r'''Gets next file number.
    '''

    file_numbers = []
    for file_name in os.listdir(output_directory):
        if file_name.endswith(extension):
            try:
                file_numbers.append(int(file_name[-6:-4]))
            except ValueError:
                pass
    if file_numbers:
        max_file_number = max(file_numbers)
    else:
        max_file_number = 0
    next_file_number = max_file_number + 1
    return next_file_number