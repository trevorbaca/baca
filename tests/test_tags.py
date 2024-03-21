import baca


def test_clef_color_tags():

    assert baca.tags.clef_color_tags() == [
        baca.tags.EXPLICIT_CLEF_COLOR,
        baca.tags.EXPLICIT_CLEF_REDRAW_COLOR,
        baca.tags.REAPPLIED_CLEF_COLOR,
        baca.tags.REAPPLIED_CLEF_REDRAW_COLOR,
        baca.tags.REDUNDANT_CLEF_COLOR,
        baca.tags.REDUNDANT_CLEF_REDRAW_COLOR,
    ]

    assert baca.tags.clef_color_tags(build=True) == [
        baca.tags.EXPLICIT_CLEF_COLOR,
        baca.tags.EXPLICIT_CLEF_REDRAW_COLOR,
        baca.tags.REAPPLIED_CLEF_COLOR,
        baca.tags.REAPPLIED_CLEF_REDRAW_COLOR,
        baca.tags.REDUNDANT_CLEF_COLOR,
        baca.tags.REDUNDANT_CLEF_REDRAW_COLOR,
        baca.tags.REAPPLIED_CLEF,
    ]


def test_dynamic_color_tags():

    assert baca.tags.dynamic_color_tags() == [
        baca.tags.EXPLICIT_DYNAMIC_COLOR,
        baca.tags.REAPPLIED_DYNAMIC,
        baca.tags.REAPPLIED_DYNAMIC_COLOR,
        baca.tags.REDUNDANT_DYNAMIC_COLOR,
    ]


def test_instrument_color_tags():

    assert baca.tags.instrument_color_tags() == [
        baca.tags.EXPLICIT_INSTRUMENT_ALERT,
        baca.tags.EXPLICIT_INSTRUMENT_COLOR,
        baca.tags.REAPPLIED_INSTRUMENT_COLOR,
        baca.tags.REAPPLIED_INSTRUMENT_ALERT,
        baca.tags.REDRAWN_EXPLICIT_INSTRUMENT_COLOR,
        baca.tags.REDRAWN_REAPPLIED_INSTRUMENT_COLOR,
        baca.tags.REDUNDANT_INSTRUMENT_ALERT,
        baca.tags.REDUNDANT_INSTRUMENT_COLOR,
        baca.tags.REDRAWN_REDUNDANT_INSTRUMENT_COLOR,
    ]


def test_layout_removal_tags():

    assert baca.tags.layout_removal_tags() == [
        baca.tags.EXPLICIT_TIME_SIGNATURE_COLOR,
        baca.tags.LOCAL_MEASURE_NUMBER,
        baca.tags.MEASURE_NUMBER,
        baca.tags.RED_START_BAR,
        baca.tags.REDUNDANT_TIME_SIGNATURE_COLOR,
        baca.tags.STAGE_NUMBER,
    ]


def test_metronome_mark_color_expression_tags():

    assert baca.tags.metronome_mark_color_expression_tags() == [
        baca.tags.EXPLICIT_METRONOME_MARK_WITH_COLOR,
        baca.tags.REAPPLIED_METRONOME_MARK_WITH_COLOR,
        baca.tags.REDUNDANT_METRONOME_MARK_WITH_COLOR,
    ]


def test_metronome_mark_color_suppression_tags():

    assert baca.tags.metronome_mark_color_suppression_tags() == [
        baca.tags.EXPLICIT_METRONOME_MARK,
        baca.tags.REDUNDANT_METRONOME_MARK,
    ]


def test_music_annotation_tags():

    assert baca.tags.music_annotation_tags() == [
        baca.tags.CLOCK_TIME,
        baca.tags.FIGURE_LABEL,
        baca.tags.INVISIBLE_MUSIC_COLORING,
        baca.tags.LOCAL_MEASURE_NUMBER,
        baca.tags.MATERIAL_ANNOTATION_MARKUP,
        baca.tags.MATERIAL_ANNOTATION_SPANNER,
        baca.tags.MOCK_COLORING,
        baca.tags.MOMENT_ANNOTATION_SPANNER,
        baca.tags.NOT_YET_PITCHED_COLORING,
        baca.tags.OCTAVE_COLORING,
        baca.tags.REPEAT_PITCH_CLASS_COLORING,
        baca.tags.SPACING,
        baca.tags.SPACING_OVERRIDE,
        baca.tags.STAFF_HIGHLIGHT,
        baca.tags.STAGE_NUMBER,
    ]


def test_ottava_color_tags():

    assert baca.tags.ottava_color_tags() == [
        baca.tags.EXPLICIT_OTTAVA_COLOR,
        baca.tags.REAPPLIED_OTTAVA,
        baca.tags.REAPPLIED_OTTAVA_COLOR,
        baca.tags.REDUNDANT_OTTAVA_COLOR,
    ]


def test_persistent_indicator_color_expression_tags():

    assert baca.tags.persistent_indicator_color_expression_tags() == [
        baca.tags.EXPLICIT_CLEF_COLOR,
        baca.tags.EXPLICIT_CLEF_REDRAW_COLOR,
        baca.tags.REAPPLIED_CLEF_COLOR,
        baca.tags.REAPPLIED_CLEF_REDRAW_COLOR,
        baca.tags.REDUNDANT_CLEF_COLOR,
        baca.tags.REDUNDANT_CLEF_REDRAW_COLOR,
        baca.tags.EXPLICIT_DYNAMIC_COLOR,
        baca.tags.REAPPLIED_DYNAMIC,
        baca.tags.REAPPLIED_DYNAMIC_COLOR,
        baca.tags.REDUNDANT_DYNAMIC_COLOR,
        baca.tags.EXPLICIT_INSTRUMENT_ALERT,
        baca.tags.EXPLICIT_INSTRUMENT_COLOR,
        baca.tags.REAPPLIED_INSTRUMENT_COLOR,
        baca.tags.REAPPLIED_INSTRUMENT_ALERT,
        baca.tags.REDRAWN_EXPLICIT_INSTRUMENT_COLOR,
        baca.tags.REDRAWN_REAPPLIED_INSTRUMENT_COLOR,
        baca.tags.REDUNDANT_INSTRUMENT_ALERT,
        baca.tags.REDUNDANT_INSTRUMENT_COLOR,
        baca.tags.REDRAWN_REDUNDANT_INSTRUMENT_COLOR,
        baca.tags.EXPLICIT_METRONOME_MARK_WITH_COLOR,
        baca.tags.REAPPLIED_METRONOME_MARK_WITH_COLOR,
        baca.tags.REDUNDANT_METRONOME_MARK_WITH_COLOR,
        baca.tags.EXPLICIT_OTTAVA_COLOR,
        baca.tags.REAPPLIED_OTTAVA,
        baca.tags.REAPPLIED_OTTAVA_COLOR,
        baca.tags.REDUNDANT_OTTAVA_COLOR,
        baca.tags.EXPLICIT_SHORT_INSTRUMENT_NAME_ALERT,
        baca.tags.EXPLICIT_SHORT_INSTRUMENT_NAME_COLOR,
        baca.tags.REAPPLIED_SHORT_INSTRUMENT_NAME_ALERT,
        baca.tags.REAPPLIED_SHORT_INSTRUMENT_NAME_COLOR,
        baca.tags.REDRAWN_EXPLICIT_SHORT_INSTRUMENT_NAME,
        baca.tags.REDRAWN_EXPLICIT_SHORT_INSTRUMENT_NAME_COLOR,
        baca.tags.REDRAWN_REAPPLIED_SHORT_INSTRUMENT_NAME,
        baca.tags.REDRAWN_REAPPLIED_SHORT_INSTRUMENT_NAME_COLOR,
        baca.tags.REDUNDANT_SHORT_INSTRUMENT_NAME_ALERT,
        baca.tags.REDUNDANT_SHORT_INSTRUMENT_NAME_COLOR,
        baca.tags.REDRAWN_REDUNDANT_SHORT_INSTRUMENT_NAME_COLOR,
        baca.tags.EXPLICIT_STAFF_LINES_COLOR,
        baca.tags.REAPPLIED_STAFF_LINES_COLOR,
        baca.tags.REDUNDANT_STAFF_LINES_COLOR,
        baca.tags.EXPLICIT_TIME_SIGNATURE_COLOR,
        baca.tags.REAPPLIED_TIME_SIGNATURE_COLOR,
        baca.tags.REDUNDANT_TIME_SIGNATURE_COLOR,
    ]

    assert baca.tags.persistent_indicator_color_expression_tags(build=True) == [
        baca.tags.EXPLICIT_CLEF_COLOR,
        baca.tags.EXPLICIT_CLEF_REDRAW_COLOR,
        baca.tags.REAPPLIED_CLEF_COLOR,
        baca.tags.REAPPLIED_CLEF_REDRAW_COLOR,
        baca.tags.REDUNDANT_CLEF_COLOR,
        baca.tags.REDUNDANT_CLEF_REDRAW_COLOR,
        baca.tags.REAPPLIED_CLEF,
        baca.tags.EXPLICIT_DYNAMIC_COLOR,
        baca.tags.REAPPLIED_DYNAMIC,
        baca.tags.REAPPLIED_DYNAMIC_COLOR,
        baca.tags.REDUNDANT_DYNAMIC_COLOR,
        baca.tags.EXPLICIT_INSTRUMENT_ALERT,
        baca.tags.EXPLICIT_INSTRUMENT_COLOR,
        baca.tags.REAPPLIED_INSTRUMENT_COLOR,
        baca.tags.REAPPLIED_INSTRUMENT_ALERT,
        baca.tags.REDRAWN_EXPLICIT_INSTRUMENT_COLOR,
        baca.tags.REDRAWN_REAPPLIED_INSTRUMENT_COLOR,
        baca.tags.REDUNDANT_INSTRUMENT_ALERT,
        baca.tags.REDUNDANT_INSTRUMENT_COLOR,
        baca.tags.REDRAWN_REDUNDANT_INSTRUMENT_COLOR,
        baca.tags.EXPLICIT_METRONOME_MARK_WITH_COLOR,
        baca.tags.REAPPLIED_METRONOME_MARK_WITH_COLOR,
        baca.tags.REDUNDANT_METRONOME_MARK_WITH_COLOR,
        baca.tags.EXPLICIT_OTTAVA_COLOR,
        baca.tags.REAPPLIED_OTTAVA,
        baca.tags.REAPPLIED_OTTAVA_COLOR,
        baca.tags.REDUNDANT_OTTAVA_COLOR,
        baca.tags.EXPLICIT_SHORT_INSTRUMENT_NAME_ALERT,
        baca.tags.EXPLICIT_SHORT_INSTRUMENT_NAME_COLOR,
        baca.tags.REAPPLIED_SHORT_INSTRUMENT_NAME_ALERT,
        baca.tags.REAPPLIED_SHORT_INSTRUMENT_NAME_COLOR,
        baca.tags.REDRAWN_EXPLICIT_SHORT_INSTRUMENT_NAME,
        baca.tags.REDRAWN_EXPLICIT_SHORT_INSTRUMENT_NAME_COLOR,
        baca.tags.REDRAWN_REAPPLIED_SHORT_INSTRUMENT_NAME,
        baca.tags.REDRAWN_REAPPLIED_SHORT_INSTRUMENT_NAME_COLOR,
        baca.tags.REDUNDANT_SHORT_INSTRUMENT_NAME_ALERT,
        baca.tags.REDUNDANT_SHORT_INSTRUMENT_NAME_COLOR,
        baca.tags.REDRAWN_REDUNDANT_SHORT_INSTRUMENT_NAME_COLOR,
        baca.tags.EXPLICIT_STAFF_LINES_COLOR,
        baca.tags.REAPPLIED_STAFF_LINES_COLOR,
        baca.tags.REDUNDANT_STAFF_LINES_COLOR,
        baca.tags.REAPPLIED_STAFF_LINES,
        baca.tags.EXPLICIT_TIME_SIGNATURE_COLOR,
        baca.tags.REAPPLIED_TIME_SIGNATURE_COLOR,
        baca.tags.REDUNDANT_TIME_SIGNATURE_COLOR,
        baca.tags.REAPPLIED_TIME_SIGNATURE,
    ]


def test_persistent_indicator_color_suppression_tags():

    assert baca.tags.persistent_indicator_color_suppression_tags() == [
        baca.tags.EXPLICIT_METRONOME_MARK,
        baca.tags.REDUNDANT_METRONOME_MARK,
    ]


def test_persistent_indicator_tags():

    assert baca.tags.persistent_indicator_tags() == [
        baca.tags.EXPLICIT_CLEF,
        baca.tags.REAPPLIED_CLEF,
        baca.tags.REDUNDANT_CLEF,
        baca.tags.EXPLICIT_DYNAMIC,
        baca.tags.REAPPLIED_DYNAMIC,
        baca.tags.REDUNDANT_DYNAMIC,
        baca.tags.EXPLICIT_INSTRUMENT,
        baca.tags.REAPPLIED_INSTRUMENT,
        baca.tags.REDUNDANT_INSTRUMENT,
        baca.tags.EXPLICIT_SHORT_INSTRUMENT_NAME,
        baca.tags.REAPPLIED_SHORT_INSTRUMENT_NAME,
        baca.tags.REDUNDANT_SHORT_INSTRUMENT_NAME,
        baca.tags.EXPLICIT_METRONOME_MARK,
        baca.tags.REAPPLIED_METRONOME_MARK,
        baca.tags.REDUNDANT_METRONOME_MARK,
        baca.tags.EXPLICIT_OTTAVA,
        baca.tags.REAPPLIED_OTTAVA,
        baca.tags.REDUNDANT_OTTAVA,
        baca.tags.EXPLICIT_PERSISTENT_OVERRIDE,
        baca.tags.REAPPLIED_PERSISTENT_OVERRIDE,
        baca.tags.REDUNDANT_PERSISTENT_OVERRIDE,
        baca.tags.EXPLICIT_STAFF_LINES,
        baca.tags.REAPPLIED_STAFF_LINES,
        baca.tags.REDUNDANT_STAFF_LINES,
        baca.tags.EXPLICIT_TIME_SIGNATURE,
        baca.tags.REAPPLIED_TIME_SIGNATURE,
        baca.tags.REDUNDANT_TIME_SIGNATURE,
    ]


def test_short_instrument_name_color_tags():

    assert baca.tags.short_instrument_name_color_tags() == [
        baca.tags.EXPLICIT_SHORT_INSTRUMENT_NAME_ALERT,
        baca.tags.EXPLICIT_SHORT_INSTRUMENT_NAME_COLOR,
        baca.tags.REAPPLIED_SHORT_INSTRUMENT_NAME_ALERT,
        baca.tags.REAPPLIED_SHORT_INSTRUMENT_NAME_COLOR,
        baca.tags.REDRAWN_EXPLICIT_SHORT_INSTRUMENT_NAME,
        baca.tags.REDRAWN_EXPLICIT_SHORT_INSTRUMENT_NAME_COLOR,
        baca.tags.REDRAWN_REAPPLIED_SHORT_INSTRUMENT_NAME,
        baca.tags.REDRAWN_REAPPLIED_SHORT_INSTRUMENT_NAME_COLOR,
        baca.tags.REDUNDANT_SHORT_INSTRUMENT_NAME_ALERT,
        baca.tags.REDUNDANT_SHORT_INSTRUMENT_NAME_COLOR,
        baca.tags.REDRAWN_REDUNDANT_SHORT_INSTRUMENT_NAME_COLOR,
    ]


def test_spacing_markup_tags():

    assert baca.tags.spacing_markup_tags() == [
        baca.tags.SPACING,
        baca.tags.SPACING_OVERRIDE,
    ]


def test_spacing_tags():

    assert baca.tags.spacing_tags() == [
        baca.tags.SPACING_COMMAND,
        baca.tags.SPACING,
        baca.tags.SPACING_OVERRIDE_COMMAND,
        baca.tags.SPACING_OVERRIDE,
    ]


def test_staff_lines_color_tags():

    assert baca.tags.staff_lines_color_tags() == [
        baca.tags.EXPLICIT_STAFF_LINES_COLOR,
        baca.tags.REAPPLIED_STAFF_LINES_COLOR,
        baca.tags.REDUNDANT_STAFF_LINES_COLOR,
    ]

    assert baca.tags.staff_lines_color_tags(build=True) == [
        baca.tags.EXPLICIT_STAFF_LINES_COLOR,
        baca.tags.REAPPLIED_STAFF_LINES_COLOR,
        baca.tags.REDUNDANT_STAFF_LINES_COLOR,
        baca.tags.REAPPLIED_STAFF_LINES,
    ]


def test_time_signature_color_tags():

    assert baca.tags.time_signature_color_tags() == [
        baca.tags.EXPLICIT_TIME_SIGNATURE_COLOR,
        baca.tags.REAPPLIED_TIME_SIGNATURE_COLOR,
        baca.tags.REDUNDANT_TIME_SIGNATURE_COLOR,
    ]

    assert baca.tags.time_signature_color_tags(build=True) == [
        baca.tags.EXPLICIT_TIME_SIGNATURE_COLOR,
        baca.tags.REAPPLIED_TIME_SIGNATURE_COLOR,
        baca.tags.REDUNDANT_TIME_SIGNATURE_COLOR,
        baca.tags.REAPPLIED_TIME_SIGNATURE,
    ]
