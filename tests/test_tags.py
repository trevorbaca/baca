import baca


def test_layout_removal_tags():

    assert baca.section._layout_removal_tags() == [
        baca.tags.EXPLICIT_TIME_SIGNATURE_COLOR,
        baca.tags.LOCAL_MEASURE_NUMBER,
        baca.tags.MEASURE_NUMBER,
        baca.tags.RED_START_BAR,
        baca.tags.REDUNDANT_TIME_SIGNATURE_COLOR,
        baca.tags.STAGE_NUMBER,
    ]


def test_metronome_mark_color_suppression_tags():

    assert baca.build._metronome_mark_color_suppression_tags() == [
        baca.tags.EXPLICIT_METRONOME_MARK,
        baca.tags.REDUNDANT_METRONOME_MARK,
    ]


def test_music_annotation_tags():

    assert baca.build._music_annotation_tags() == [
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
        baca.tags.STAFF_HIGHLIGHT,
        baca.tags.STAGE_NUMBER,
    ]


def test_persistent_indicator_color_expression_tags():

    assert baca.build._persistent_indicator_color_expression_tags() == [
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

    assert baca.build._persistent_indicator_color_expression_tags(build=True) == [
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

    assert baca.build._persistent_indicator_color_suppression_tags() == [
        baca.tags.EXPLICIT_METRONOME_MARK,
        baca.tags.REDUNDANT_METRONOME_MARK,
    ]


def test_persistent_indicator_tags():

    assert baca.section._persistent_indicator_tags() == [
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
