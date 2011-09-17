from abjad.tools import durationtools
from abjad.tools import iotools
from abjad.tools import leaftools
from abjad.tools import lilypondfiletools
from abjad.tools import markuptools
from abjad.tools import schemetools
from abjad.tools import scoretools
from get_chordal_sequences_directory import get_chordal_sequences_directory
from get_next_chordal_sequence_package_name import get_next_chordal_sequence_package_name
from get_next_chordal_sequence_subtitle import get_next_chordal_sequence_subtitle
#from get_score_title import get_score_title
from get_verified_user_input import get_verified_user_input
#from run_go_on_menu import run_go_on_menu
import baca
import os
import re


def make_chordal_sequence(score_package_name):

    aggregate_ids_regex = re.compile('([1-8]?-\d+\s*)*')

    while True:
        prompt = 'Enter aggregate numbers: '
        aggregate_ids = get_verified_user_input(prompt)
        match = aggregate_ids_regex.match(aggregate_ids)
        if match is not None:
            break

    aggregate_id_string = match.group()
    aggregate_ids = aggregate_id_string.split()
    aggregates = []
    for aggregate_id in aggregate_ids:
        constellation_number, aggregate_number = aggregate_id.split('-')
        constellation_number = int(constellation_number)
        aggregate_number = int(aggregate_number)
        constellation_index = constellation_number - 1
        aggregate_index = aggregate_number - 1
        aggregate = baca.pitch.CC[constellation_index][aggregate_index]
        aggregates.append(aggregate)

    chords = leaftools.make_leaves(aggregates, [durationtools.Duration(1, 4)])
    score, treble_staff, bass_staff = scoretools.make_piano_sketch_score_from_leaves(chords)

    score.set.proportional_notation_duration = schemetools.SchemeMoment(1, 16)
    score.override.spacing_spanner.uniform_stretching = True
    score.override.spacing_spanner.strict_spacing = True
    score.override.stem.transparent = True
    scoretools.add_double_bar_to_end_of_score(score)

    lily_file = lilypondfiletools.make_basic_lily_file(score)
    lily_file.layout_block.ragged_right = True
    lily_file.layout_block.indent = 0

    score_title = get_score_title(score_package_name)
    lily_file.header_block.title = markuptools.Markup(score_title)
    subtitle = get_next_chordal_sequence_subtitle(score_package_name)
    lily_file.header_block.subtitle = markuptools.Markup(subtitle)

    chordal_sequences_directory = get_chordal_sequences_directory(score_package_name)
    chordal_sequence_name = get_next_chordal_sequence_package_name(score_package_name)
    chordal_sequence_path = os.path.join(chordal_sequences_directory, chordal_sequence_name)

    if not os.path.exists(chordal_sequence_path):
        os.mkdir(chordal_sequence_path)

    data_file_name = os.path.join(chordal_sequence_path, chordal_sequence_name + '.py')
    data_file = file(data_file_name, 'w')
    data_file.write(str(aggregates))
    data_file.close()

    ly_file_name = os.path.join(chordal_sequence_path, chordal_sequence_name + '.ly')
    iotools.write_expr_to_ly(lily_file, ly_file_name, print_status = False)

    pdf_file_name = os.path.join(chordal_sequence_path, chordal_sequence_name + '.pdf')
    iotools.write_expr_to_pdf(lily_file, pdf_file_name, print_status = False)

    print '%s %s written to disk.\n' % (score_title, subtitle)

    response = raw_input('Show chordal sequence PDF? ')
    print ''
    if response.lower() in ('1', 'y', 'yes'):
        command = 'open %s' % pdf_file_name
        os.system(command)

    run_go_on_menu()
