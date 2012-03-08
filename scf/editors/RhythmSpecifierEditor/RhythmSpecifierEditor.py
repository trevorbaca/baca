from scf.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from scf.editors.TargetManifest import TargetManifest
from scf.specifiers.RhythmSpecifier import RhythmSpecifier
from scf import getters
from scf import selectors


class RhythmSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(RhythmSpecifier,
        ('name', 'nm', getters.get_string),
        ('description', 'ds', getters.get_string),
        (),
        ('kaleid_package_importable_name', 'kaleid', 'kl', selectors.KaleidPackageSelector),
        )

    ### READ-ONLY ATTRIBUTES ###

    @property
    def target_name(self):
        return self.target.one_line_menuing_summary
