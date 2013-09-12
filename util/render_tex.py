import os


def render_tex(input_directory, input_file_name_stem, output_directory):

    print 'Rendering {}.tex ...'.format(input_file_name_stem)
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
