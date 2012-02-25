import scf


def test_SCFObject_read_only_attributes_01():

    scf_object = scf.core.SCFObject()

    assert scf_object.boilerplate_directory == '/Users/trevorbaca/Documents/other/baca/scf/boilerplate'
    assert isinstance(scf_object.breadcrumb_stack, list)
    assert scf_object.class_name == 'SCFObject'
    assert scf_object.help_item_width == 5
    assert scf_object.makers_directory_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/makers'
    assert scf_object.makers_package_importable_name == 'scf.makers'
    assert scf_object.scf_package_importable_name == 'scf'
    assert scf_object.scf_package_path_name == '/Users/trevorbaca/Documents/other/baca/scf'
    assert isinstance(scf_object.session, scf.core.Session)
    assert scf_object.score_external_chunks_package_importable_name == 'baca.sketches'
    assert scf_object.source_file_name == '/Users/trevorbaca/Documents/other/baca/scf/core/SCFObject/SCFObject.py'
    assert scf_object.spaced_class_name == 's c f object'
    assert scf_object.studio_directory_name == '/Users/trevorbaca/Documents/other/baca'
    assert scf_object.score_external_materials_package_importable_name == 'baca.materials'
    assert scf_object.home_package_importable_name == 'baca'
    assert scf_object.stylesheets_directory_name == '/Users/trevorbaca/Documents/other/baca/scf/stylesheets'
    assert scf_object.stylesheets_package_importable_name == 'scf.stylesheets'
    assert isinstance(scf_object.transcript, list)
    assert isinstance(scf_object.transcript_signature, tuple)
    assert isinstance(scf_object.ts, tuple)
