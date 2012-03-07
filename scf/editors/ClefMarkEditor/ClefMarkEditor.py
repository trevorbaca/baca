from abjad.tools import contexttools
from scf.editors.InteractiveEditor import InteractiveEditor
from scf.editors.TargetManifest import TargetManifest
from scf import getters


class ClefMarkEditor(InteractiveEditor):

    ### CLASS ATTRIBUTES ###

    target_class = contexttools.ClefMark
    target_manifest = TargetManifest(contexttools.ClefMark,
        ('clef_name', 'nm', getters.get_string),
        )        
