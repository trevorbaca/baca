import baca


def test_Studio_run_01():
    '''Running studio establishes new sesssion correctly.
    '''

    studio = baca.scf.studiopackage.Studio()
    old_session = studio.session
    assert studio.session is studio.global_proxy.session is studio.global_proxy.material_package_wrangler.session 
    
    studio.run(user_input='q')
    new_session = studio.session

    assert studio.session is studio.global_proxy.session is studio.global_proxy.material_package_wrangler.session 
    assert old_session is not new_session
