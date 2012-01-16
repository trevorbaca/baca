from abjad.tools import iotools
from baca.scf.SCFObject import SCFObject
import os


class NewPackageWrangler(SCFObject):

    def __init__(self, global_package_importable_name=None, 
        scores_package_importable_name_body=None, session=session):
        SCFObject.__init__(self, session=session)
        if global_package_importable_name is not None:
            assert iotools.is_underscore_delimited_lowercase_package_name(global_package_importable_name)
        if scores_package_importable_name_body is not None:
            assert iotools.is_underscore_delimited_lowercase_package_name(scores_package_importable_name_body)
        self._global_package_importable_name = global_package_importable_name
        self._scores_package_importable_name_body = score_package_importable_name_body

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def global_package_improtable_name(self):
        return self._global_package_importable_name

    @property
    def has_packages(self):
        for 

    @property
    def scores_package_improtable_name_body(self):
        return self._scores_package_importable_name_body

    ### PUBLIC METHODS ###

    def list_package_importable_names(self):
        result = [] 
