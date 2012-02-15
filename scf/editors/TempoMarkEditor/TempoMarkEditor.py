from abjad.tools import contexttools
from abjad.tools import durationtools
from baca.scf.editors.InteractiveEditor import InteractiveEditor
from baca.scf.TargetManifest import TargetManifest
from baca.scf import getters


class TempoMarkEditor(InteractiveEditor):

    target_class = contexttools.TempoMark
    target_manifest = TargetManifest(contexttools.TempoMark,
        ('duration', 'd', getters.get_duration),
        ('units_per_minute', 'm', getters.get_integer),
        )

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'tempo mark editor'

    ### PUBLIC METHODS ###

    def conditionally_initialize_target(self):
        self.target = self.target or contexttools.TempoMark(durationtools.Duration(1, 4), 60)
