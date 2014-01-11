import os
from baca.utilities.get_parent_directory import get_parent_directory


def cache_output(output, output_file_name, location):
    '''Cache `output` string to output file with name equal to
    `output_file_name` in ../_output directory.
    '''

    assert isinstance(output, str)
    assert isinstance(output_file_name, str)
    assert not ' ' in output_file_name

    parent_directory = get_parent_directory(location)
    output_directory = os.path.join(parent_directory, '_output')
    outfile = os.path.join(output_directory, output_file_name + '.py')
    outfile = file(outfile, 'w')
    outfile.write(output)
    outfile.close()
