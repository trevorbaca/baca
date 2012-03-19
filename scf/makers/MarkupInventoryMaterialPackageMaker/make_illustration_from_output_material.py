from abjad import *
from abjad.tools import layouttools
import copy


def make_illustration_from_output_material(markup_inventory, **kwargs):

    notes = []
    for markup in markup_inventory:
        note = Note("c'4")
        markup_copy = markuptools.Markup(markup)
        markup_copy(note)
        notes.append(note)

    staff = stafftools.RhythmicStaff(notes)
    score = Score([staff])
    illustration = lilypondfiletools.make_basic_lilypond_file(score)
    illustration.paper_block.top_system_spacing = layouttools.make_spacing_vector(0, 0, 6, 0)

    score.override.note_head.transparent = True
    score.override.bar_line.transparent = True
    score.override.clef.transparent = True
    score.override.span_bar.transparent = True
    score.override.staff_symbol.transparent = True
    score.override.stem.transparent = True
    score.override.time_signature.stencil = False
    score.set.proportional_notation_duration = schemetools.SchemeMoment(1, 24)

    return illustration
