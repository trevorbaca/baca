from abjad import *
import scf


def test_UserInputWrapper_public_attributes_01():

    wrapper = scf.editors.UserInputWrapper()
    wrapper['flavor'] = 'cherry'
    wrapper['duration'] = Duration(1, 4)
    
    assert wrapper.editable_lines == ["flavor: 'cherry'", 'duration: Duration(1, 4)']
    assert wrapper.formatted_lines == ['user_input_wrapper = UserInputWrapper([', "\t('flavor', 'cherry'),", "\t('duration', Duration(1, 4))])"]
    assert wrapper.is_complete
    assert not wrapper.is_empty
    assert not wrapper.is_partially_complete
    assert wrapper.user_input_module_import_statements == []

    assert wrapper.list_items() == [('flavor', 'cherry'), ('duration', Duration(1, 4))]
    assert wrapper.list_keys() == ['flavor', 'duration']
    assert wrapper.list_values() == ['cherry', Duration(1, 4)]
