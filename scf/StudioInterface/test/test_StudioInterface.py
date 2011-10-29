import baca


def test_StudioInterface_01():
    '''Attributes.
    '''

    studio_interface = baca.scf.StudioInterface()

    assert studio_interface.class_name == 'StudioInterface'
    assert isinstance(studio_interface.global_proxy, baca.scf.GlobalProxy)
    assert isinstance(studio_interface.score_wrangler, baca.scf.ScoreWrangler)
    assert studio_interface.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/StudioInterface/StudioInterface.py'
    assert studio_interface.spaced_class_name == 'studio interface'
