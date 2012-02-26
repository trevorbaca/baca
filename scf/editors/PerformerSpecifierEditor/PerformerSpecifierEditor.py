from scf.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from scf.editors.TargetManifest import TargetManifest
from scf.specifiers.PerformerSpecifier import PerformerSpecifier
from scf import selectors


class PerformerSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_class = PerformerSpecifier
    target_manifest = TargetManifest(PerformerSpecifier,
        ('performer', 'pf', selectors.select_performer_interactively),
        )

    ### READ-ONLY ATTRIBUTES ###

    @property
    def target_name(self):
        if self.target:
            if self.target.performer:
                return self.target.performer.performer_name
