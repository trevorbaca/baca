from scf.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from scf.editors.TargetManifest import TargetManifest
from scf.specifiers.PitchClassSpecifier import PitchClassSpecifier
from scf import getters
from scf import selectors
from scf import wizards


class PitchClassSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_class = PitchClassSpecifier
    target_manifest = TargetManifest(PitchClassSpecifier,
        ('name', 'nm', getters.get_string),
        ('description', 'ds', getters.get_string),
        (),
        ('pitch_class_reservoir', 'pc', selectors.PitchClassReservoirSelector),
        ('pitch_class_transform', 'tr', wizards.PitchClassTransformCreationWizard),
        ('reservoir_start_helper', 'hp', wizards.ReservoirStartHelperCreationWizard),
        )

    ### READ-ONLY ATTRIBUTES ###

    @property
    def target_name(self):
        return self.target.name
