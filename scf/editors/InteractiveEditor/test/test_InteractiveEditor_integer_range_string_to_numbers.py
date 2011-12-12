import baca


def test_InteractiveEditor_integer_range_string_to_numbers_01():

    editor = baca.scf.editors.InteractiveEditor()
    assert editor.integer_range_string_to_numbers('all', 9, 12) == [9, 10, 11, 12]
    assert editor.integer_range_string_to_numbers('1') == [1]
    assert editor.integer_range_string_to_numbers('1,8') == [1, 8]
    assert editor.integer_range_string_to_numbers('1,8,9-12') == [1, 8, 9, 10, 11, 12]
    assert editor.integer_range_string_to_numbers('1,8,12-9') == [1, 8, 12, 11, 10, 9]
