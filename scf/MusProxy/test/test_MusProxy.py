import baca


def test_MusProxy_01():

    mus_proxy = baca.scf.MusProxy('manos')

    assert isinstance(mus_proxy.purview, baca.scf.ScoreProxy)
    assert mus_proxy.directory_name == '/Users/trevorbaca/Documents/scores/manos/mus'
    assert mus_proxy.package_short_name == 'mus'
    assert mus_proxy.package_importable_name == 'manos.mus'
