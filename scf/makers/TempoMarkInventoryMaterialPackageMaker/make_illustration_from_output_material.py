from abjad import *
from abjad.tools import skiptools


def make_illustration_from_output_material(tempo_mark_inventory):

    notes = []
    for tempo_mark in tempo_mark_inventory:
        notes.append(Note("c'4"))

    staff = Staff(notes)
    score = Score([staff])
    illustration = lilypondfiletools.make_basic_lilypond_file(score)

    score.override.note_head.transparent = True
    score.override.bar_line.transparent = True
    score.override.span_bar.transparent = True
    score.override.stem.transparent = True
    score.override.time_signature.stencil = False
    score.set.proportional_notation_duration = schemetools.SchemeMoment(1, 4)

    return illustration
