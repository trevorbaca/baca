import baca


def test_Studio___init___01():
    '''Init creates shared sesssion.
    '''

    studio = baca.scf.studiopackage.Studio()
    assert studio.session is studio.global_proxy.session is studio.score_package_wrangler.session
