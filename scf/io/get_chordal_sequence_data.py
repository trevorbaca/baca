from get_chordal_sequences_directory import get_chordal_sequences_directory
import os


def get_chordal_sequence_data(score_package_name, chordal_sequence_number):

   chordal_sequences_directory = get_chordal_sequences_directory(score_package_name)
   package_name = '%s_chordal_sequence_%s' % (score_package_name, str(chordal_sequence_number).zfill(2))
   package_path = os.path.join(chordal_sequences_directory, package_name)
   data_file_name = os.path.join(package_path, package_name + '.py')
   data_file = file(data_file_name, 'r')
   data_lines = data_file.readlines( )
   data_file.close( )
   data = data_lines[0]
   data = eval(data)

   return data
