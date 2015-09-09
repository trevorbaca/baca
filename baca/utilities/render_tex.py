# -*- coding: utf-8 -*-
import os


def render_tex(input_directory, input_file_name_stem, output_directory):

    message = 'Rendering {}.tex ...'
    message = message.format(input_file_name_stem)
    print(message)
    command = 'pdflatex --jobname={} -output-directory={} {}/{}.tex'
    command = command.format(
        input_file_name_stem, 
        output_directory, 
        input_directory, 
        input_file_name_stem,
        )
    os.system(command)
    command = 'rm {}/*.aux'.format(output_directory)
    os.system(command)
    command = 'rm {}/*.log'.format(output_directory)
    os.system(command)