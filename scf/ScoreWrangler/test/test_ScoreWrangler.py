import baca


def test_ScoreWrangler_01():
    '''Attributes.
    '''

    score_wrangler = baca.scf.ScoreWrangler()

    assert score_wrangler.class_name == 'ScoreWrangler'
    assert score_wrangler.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/ScoreWrangler/ScoreWrangler.py'
    assert score_wrangler.spaced_class_name == 'score wrangler'
