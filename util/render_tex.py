import os


def render_tex(input_directory, input_file_name_stem, output_directory):
    print 'Rendering %s.tex ...' % input_file_name_stem
    command = 'pdflatex --jobname=%s -output-directory=%s %s/%s.tex'
    command %= (input_file_name_stem, output_directory, input_directory, input_file_name_stem)
    os.system(command)
    os.system('rmlx %s' % output_directory)
