from baca.scf.ScorePackageProxy import ScorePackageProxy
import os


class CatalogProxy(object):

   def __init__(self):
      self.scores_directory = os.environ.get('SCORES')

   ## OVERLOADS ##

   def __repr__(self):
      return '%s( )' % self.__class__.__name__

   ## PUBLIC METHODS ##

   def create_score_package(self, score_package_name):
      raise NotImplementedError

   def fix_score_package_directory_structures(self):
      for score_package_name in self.list_score_package_names( ):
         score_package_proxy = ScorePackageProxy(score_package_name)
         score_package_proxy.fix_score_package_directory_structure( )
         score_package_proxy.profile_score_package_directory_structure( )

   def list_score_package_names(self):
      score_package_names = os.listdir(self.scores_directory)
      score_package_names = [x for x in score_package_names if x[0].isalpha( )]
      return score_package_names

   def profile_score_package_directory_structures(self):
      for score_package_name in self.list_score_package_names( ):
         score_package_proxy = ScorePackageProxy(score_package_name)
         score_package_proxy.profile_score_package_directory_structure( )
         print ''

   def remove_score_package(self, score_package_name):
      raise NotImplementedError
