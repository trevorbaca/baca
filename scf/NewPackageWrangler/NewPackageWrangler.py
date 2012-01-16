from abjad.tools import iotools
from baca.scf.SCFObject import SCFObject
import os


# TODO: write tests
class NewPackageWrangler(SCFObject):

    def __init__(self, toplevel_global_package_importable_name=None, 
        toplevel_score_package_importable_name_body=None, session=None):
        SCFObject.__init__(self, session=session)
        if toplevel_global_package_importable_name is not None:
            assert iotools.is_underscore_delimited_lowercase_package_name(
                toplevel_global_package_importable_name)
        if toplevel_score_package_importable_name_body is not None:
            assert iotools.is_underscore_delimited_lowercase_package_name(
                toplevel_score_package_importable_name_body)
        self._toplevel_global_package_importable_name = toplevel_global_package_importable_name
        self._toplevel_score_package_importable_name_body = toplevel_score_package_importable_name_body

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def has_toplevel_packages(self):
        for toplevel_package_importable_name in self.toplevel_package_importable_names:
            return True
        return False

    @property
    def score_package_short_names(self):
        result = []
        scores_directory = os.environ.get('SCORES')        
        for x in os.listdir(scores_directory):
            if x[0].isalpha():
                result.append(x)
        return result

    @property
    def toplevel_global_package_directory_name(self):
        return self.package_importable_name_to_directory_name(self.toplevel_global_package_importable_name)

    @property
    def toplevel_global_package_importable_name(self):
        return self._toplevel_global_package_importable_name

    @property
    def toplevel_package_importable_names(self):
        result = [] 
        result.append(self.toplevel_global_package_importable_name)
        result.extend(self.toplevel_score_package_importable_names)
        return result

    @property
    def toplevel_score_package_importable_name_body(self):
        return self._toplevel_score_package_importable_name_body

    @property
    def toplevel_score_package_importable_names(self):
        result = []
        for score_package_short_name in self.score_package_short_names:
            toplevel_score_package_importable_name = '{}.{}'.format(
                score_package_short_name, self.toplevel_score_package_importable_name_body)
            result.append(toplevel_score_package_importable_name)
        return result

    ### PUBLIC METHODS ###
