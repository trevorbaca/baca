import baca


def test_Studio_run_01():
    '''Running studio establishes new sesssion correctly.
    '''

    studio = baca.scf.studio.Studio()
    old_session = studio.session
    assert studio.session is studio.home_package_proxy.session is studio.material_package_wrangler.session 
    
    studio.run(user_input='q')
    new_session = studio.session

    assert studio.session is studio.home_package_proxy.session is studio.material_package_wrangler.session 
    assert old_session is not new_session
