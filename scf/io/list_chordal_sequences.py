import os
from list_score_package_names import list_score_package_names


def list_chordal_sequences(score_package_name):

   assert score_package_name in list_score_package_names( )

   scores = os.environ.get('SCORES')
   chordal_sequences_path = os.path.join(scores, score_package_name, 'mus', 'materials', 'chordal_sequences')
   
   if not os.path.exists(chordal_sequences_path):
      return 0
   
   entries = os.listdir(chordal_sequences_path)
   sequences = [entry for entry in entries if entry[0].isalpha( )]
   
   return sequences
