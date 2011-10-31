from abjad.tools import iotools
from abjad.tools import lilypondfiletools
from abjad.tools import markuptools
from baca.scf.PackageProxy import PackageProxy
import copy
import os
import shutil


# TODO: maybe Maker class doesn't exist at all? Maybe replaced by (Interactive)MaterialProxy?
class Maker(PackageProxy):

    def __init__(self, material_underscored_name=None, score=None):
        package_importable_name = 'baca.makers.%s' % self.class_name
        PackageProxy.__init__(self, package_importable_name=package_importable_name)
        self.material_underscored_name = material_underscored_name
        self.score = score

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % type(self).__name__
