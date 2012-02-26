import scf

scf_object = scf.core.SCFObject()


def test_SCFObject_path_name_to_package_importable_name_01():

    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/other/baca') == 'baca'
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/other/baca/materials') == 'materials'
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/other/baca/specifiers') == 'specifiers'


def test_SCFObject_path_name_to_package_importable_name_02():

    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/other/baca/') == 'baca'
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/other/baca/materials/') == 'materials'
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/other/baca/specifiers/') == 'specifiers'


def test_SCFObject_path_name_to_package_importable_name_03():

    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/scores/aracilik') == 'aracilik'
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/scores/aracilik/mus') == 'aracilik.mus'
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/scores/aracilik/mus/materials') == 'aracilik.mus.materials'


def test_SCFObject_path_name_to_package_importable_name_04():

    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/scores/aracilik/') == 'aracilik'
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/scores/aracilik/mus/') == 'aracilik.mus'
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/scores/aracilik/mus/materials/') == 'aracilik.mus.materials'


def test_SCFObject_path_name_to_package_importable_name_05():

    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/scores/aracilik/foo') == 'aracilik.foo'
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/scores/aracilik/foo.py') == 'aracilik.foo'
