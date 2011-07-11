import os


def write_materials_package_to_disk(score_package_name, materials_directory_name, base_file_name, 
   data, pdf = None, ly = None):

   scores = os.environ.get('SCORES')
   target_directory = os.path.join(score, score_package_name, 'mus', 'materials', materials_directory_name)

   data_file_name = base_file_name + '.py'
   data_file = file(data_file_name, 'w')
   data_file.write(str(data))
   data_file.close( )

   if pdf is not None:
      pass

   if ly is not None:
      pass
