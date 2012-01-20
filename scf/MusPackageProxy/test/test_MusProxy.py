import baca


def test_MusPackageProxy_01():

    mus_proxy = baca.scf.MusPackageProxy('manos')

    assert mus_proxy.directory_name == '/Users/trevorbaca/Documents/scores/manos/mus'
    assert mus_proxy.package_short_name == 'mus'
    assert mus_proxy.package_importable_name == 'manos.mus'
