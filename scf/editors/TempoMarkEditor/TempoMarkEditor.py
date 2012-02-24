from abjad.tools import contexttools
from abjad.tools import durationtools
from baca.scf.editors.InteractiveEditor import InteractiveEditor
from baca.scf.editors.TargetManifest import TargetManifest
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
        self.target = self.target

    def initialize_target_from_attributes_in_memory(self):
        initializer_token = []
        for attribute_name in ('textual_description', 'duration', 'units_per_minute'):
            if attribute_name in self.attributes_in_memory:
                initializer_token.append(self.attributes_in_memory.get(attribute_name))
        initializer_token = tuple(initializer_token)
        self.target = self.target_class(*initializer_token)
