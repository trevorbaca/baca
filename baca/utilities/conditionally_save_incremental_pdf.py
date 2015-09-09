# -*- coding: utf-8 -*-
import os
from abjad import *
from baca.utilities.get_next_file_number import get_next_file_number


def conditionally_save_incremental_pdf(output_directory, base_file_name):
    save = raw_input('save pdf? ')
    if save.lower() == 'y':
        next_file_number = get_next_file_number(output_directory, 'pdf')
        next_file_number = str(next_file_number).zfill(2)
        next_file_name = '%s%s.pdf' % (base_file_name, next_file_number)
        next_full_file_name = os.path.join(output_directory, next_file_name)
        lilypondfiletools.save_last_pdf_as(next_full_file_name)
        message = 'saved as %s.'
        message = message.format(next_file_name)
        print(message)