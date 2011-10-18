import baca


def test_DistProxy_01():

    dist_proxy = baca.scf.DistProxy('manos')

    assert dist_proxy.directory_name == '/Users/trevorbaca/Documents/scores/manos/dist'
    assert dist_proxy.has_directory
    assert dist_proxy.is_in_repository
    assert dist_proxy.source_file_name == '/Users/trevorbaca/Documents/other/baca/scf/DistProxy/DistProxy.py'
    assert dist_proxy.spaced_class_name == 'dist proxy'
