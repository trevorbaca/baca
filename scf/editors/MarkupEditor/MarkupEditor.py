from abjad.tools import markuptools
from scf import getters
from scf.editors.InteractiveEditor import InteractiveEditor
from scf.editors.TargetManifest import TargetManifest


class MarkupEditor(InteractiveEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(markuptools.Markup,
        ('arg', 'arg', 'ag', getters.get_string, True),
        ('direction', 'direction', 'dr', getters.get_direction_string, False),
        ('markup_name', 'name', 'nm', getters.get_string, False),
        ('style_string', 'style', 'st', getters.get_markup_style_string, False),
    )
