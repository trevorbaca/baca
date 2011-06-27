import os


def list_score_package_names( ):
   
   scores_directory = os.environ.get('SCORES')
   score_package_names = os.listdir(scores_directory)
   score_package_names = [x for x in score_package_names if x[0].isalpha( )]

   return score_package_names
