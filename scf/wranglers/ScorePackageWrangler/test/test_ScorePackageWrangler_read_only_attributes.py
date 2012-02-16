import baca


def test_ScorePackageWrangler_read_only_attributes_01():
    '''Attributes.
    '''

    score_wrangler = baca.scf.wranglers.ScorePackageWrangler()

    assert score_wrangler.class_name == 'ScorePackageWrangler'
    assert score_wrangler.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/wranglers/ScorePackageWrangler/ScorePackageWrangler.py'
    assert score_wrangler.spaced_class_name == 'score package wrangler'
