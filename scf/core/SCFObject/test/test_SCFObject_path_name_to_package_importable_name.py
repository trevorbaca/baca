import baca


def test_SCFObject_path_name_to_package_importable_name_01():

    scf_object = baca.scf.core.SCFObject()
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/other/baca') == 'baca'
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/other/baca/materials') == 'baca.materials'
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/other/baca/specifiers') == 'baca.specifiers'


def test_SCFObject_path_name_to_package_importable_name_02():

    scf_object = baca.scf.core.SCFObject()
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/other/baca/') == 'baca'
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/other/baca/materials/') == 'baca.materials'
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/other/baca/specifiers/') == 'baca.specifiers'


def test_SCFObject_path_name_to_package_importable_name_03():

    scf_object = baca.scf.core.SCFObject()
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/scores/aracilik') == 'aracilik'
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/scores/aracilik/mus') == 'aracilik.mus'
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/scores/aracilik/mus/materials') == 'aracilik.mus.materials'


def test_SCFObject_path_name_to_package_importable_name_04():

    scf_object = baca.scf.core.SCFObject()
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/scores/aracilik/') == 'aracilik'
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/scores/aracilik/mus/') == 'aracilik.mus'
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/scores/aracilik/mus/materials/') == 'aracilik.mus.materials'
