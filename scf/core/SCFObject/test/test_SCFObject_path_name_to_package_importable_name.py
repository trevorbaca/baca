import os
import scf

scf_object = scf.core.SCFObject()


def test_SCFObject_path_name_to_package_importable_name_01():

    assert scf_object.path_name_to_package_importable_name(os.environ.get('SCFMATERIALSPATH')) == 'materials'
    assert scf_object.path_name_to_package_importable_name(os.environ.get('SCFSPECIFIERSPATH')) == 'specifiers'
    # TODO: make this work
    #assert scf_object.path_name_to_package_importable_name(os.environ.get('SCFCHUNKSPATH')) == 'sketches'


def test_SCFObject_path_name_to_package_importable_name_02():

    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/scores/aracilik/') == 'aracilik'
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/scores/aracilik/mus/') == 'aracilik.mus'
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/scores/aracilik/mus/materials/') == 'aracilik.mus.materials'


def test_SCFObject_path_name_to_package_importable_name_03():

    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/scores/aracilik/foo') == 'aracilik.foo'
    assert scf_object.path_name_to_package_importable_name(
        '/Users/trevorbaca/Documents/scores/aracilik/foo.py') == 'aracilik.foo'
