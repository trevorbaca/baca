from scf.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from scf.editors.TargetManifest import TargetManifest
from scf.specifiers.RhythmSpecifier import RhythmSpecifier
from scf import selectors


class RhythmSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_class = RhythmSpecifier
    target_manifest = TargetManifest(RhythmSpecifier,
        ('kaleid', 'kl', selectors.KaleidSelector),
        )

    ### READ-ONLY ATTRIBUTES ###

    @property
    def target_name(self):
        try:
            return self.target.kaleid.kaleid_name
        except AttributeError:
            pass
