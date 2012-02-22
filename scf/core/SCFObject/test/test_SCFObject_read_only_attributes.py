import baca


def test_SCFObject_read_only_attributes_01():

    scf = baca.scf.core.SCFObject()

    assert scf.boilerplate_directory == '/Users/trevorbaca/Documents/other/baca/scf/boilerplate'
    assert isinstance(scf.breadcrumb_stack, list)
    assert scf.class_name == 'SCFObject'
    assert scf.help_item_width == 5
    assert scf.makers_directory_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/makers'
    assert scf.makers_package_importable_name == 'baca.scf.makers'
    assert scf.scf_package_importable_name == 'baca.scf'
    assert scf.scf_root_directory == '/Users/trevorbaca/Documents/other/baca/scf'
    assert isinstance(scf.session, baca.scf.core.Session)
    assert scf.score_external_chunks_package_importable_name == 'baca.sketches'
    assert scf.source_file_name == '/Users/trevorbaca/Documents/other/baca/scf/core/SCFObject/SCFObject.py'
    assert scf.spaced_class_name == 's c f object'
    assert scf.studio_directory_name == '/Users/trevorbaca/Documents/other/baca'
    assert scf.score_external_materials_package_importable_name == 'baca.materials'
    assert scf.home_package_importable_name == 'baca'
    assert scf.stylesheets_directory_name == '/Users/trevorbaca/Documents/other/baca/scf/stylesheets'
    assert scf.stylesheets_package_importable_name == 'baca.scf.stylesheets'
    assert isinstance(scf.transcript, list)
    assert isinstance(scf.transcript_signature, tuple)
    assert isinstance(scf.ts, tuple)
