from baca.scf.SCFProxyObject import SCFProxyObject
from baca.scf.ScorePackageProxy import ScorePackageProxy
import os


class CatalogProxy(SCFProxyObject):

    def __init__(self):
        self.scores_directory = os.environ.get('SCORES')

    ### PUBLIC METHODS ###

    def create_score_package(self, score_package_name):
        raise NotImplementedError

    def fix_score_package_directory_structures(self):
        for score_package_name in self.list_score_package_names():
            score_package_proxy = ScorePackageProxy(score_package_name)
            score_package_proxy.fix_score_package_directory_structure()
            score_package_proxy.profile_score_package_directory_structure()

    def list_score_directories(self):
        score_directories = []
        for score_package_name in self.list_score_package_names():
            score_directory = os.path.join(self.scores_directory, score_package_name)
            score_directories.append(score_directory)
        return score_directories

    def list_score_info_triples(self):
        score_info_triples = []
        for score_package_name in self.list_score_package_names():
            score_title = self.score_package_name_to_score_title(score_package_name)
            score_year = self.score_package_name_to_score_year(score_package_name)
            score_info_triple = (score_package_name, score_title, score_year)
            score_info_triples.append(score_info_triple)
        return score_info_triples

    def list_score_package_names(self):
        '''This method is primary.
        '''
        score_package_names = []
        for score_package_name in os.listdir(self.scores_directory):
            directory = os.path.join(self.scores_directory, score_package_name)
            if os.path.isdir(directory):
                initializer = os.path.join(directory, '__init__.py')
                if os.path.isfile(initializer):
                    if not self.score_package_name_to_hide_in_front_end(score_package_name):
                        score_package_names.append(score_package_name)
        return score_package_names

    def list_score_titles(self):
        score_titles = []
        for score_package_name in self.list_score_package_names():
            score_title = self.score_package_name_to_score_title(score_package_name)
            score_titles.append(score_title)
        return score_titles

    def list_materials_packages(self):
        materials_packages = []
        for score_package_name in self.list_well_formed_score_package_names():
            score_package_proxy = ScorePackageProxy(score_package_name)
            materials_packages.extend(score_package_proxy.list_materials_packages())
        return materials_packages

    def list_well_formed_score_package_names(self):
        score_package_names = os.listdir(self.scores_directory)
        score_package_names = [x for x in score_package_names if x[0].isalpha()]
        score_package_names.remove('poeme')
        return score_package_names

    def profile_score_package_directory_structures(self):
        for score_package_name in self.list_score_package_names():
            score_package_proxy = ScorePackageProxy(score_package_name)
            score_package_proxy.profile_score_package_directory_structure()
            print ''

    def remove_score_package(self, score_package_name):
        raise NotImplementedError

    def score_package_name_to_hide_in_front_end(self, score_package_name):
        try:
            exec('from %s import _hide_in_front_end' % score_package_name)
            return _hide_in_front_end
        except ImportError:
            return False

    def score_package_name_to_score_title(self, score_package_name):
        try:
            exec('from %s import score_title' % score_package_name)
            return score_title
        except ImportError:
            return None

    def score_package_name_to_score_year(self, score_package_name):
        try:
            exec('from %s import score_year' % score_package_name)
            return score_year
        except ImportError:
            return None
