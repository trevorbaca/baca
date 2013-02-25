import py
import scf


def test_TargetManifest_change_retrievable_attribute_name_to_initializer_argument_name_01():

    editor = scf.editors.MarkupEditor()

    assert editor.target_manifest.change_retrievable_attribute_name_to_initializer_argument_name(
        'contents_string') == 'arg'
    assert editor.target_manifest.change_retrievable_attribute_name_to_initializer_argument_name(
        'direction') == 'direction'


def test_TargetManifest_change_retrievable_attribute_name_to_initializer_argument_name_02():

    editor = scf.editors.MarkupEditor()

    assert py.test.raises(Exception,
        "editor.target_manifest.change_retrievable_attribute_name_to_initializer_argument_name('asdfasdf')")
