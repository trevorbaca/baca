import baca


def test_StylesheetFileWrangler_read_only_attributes_01():

    studio = baca.scf.studio.Studio()
    wrangler = studio.stylesheet_file_wrangler

    assert '/Users/trevorbaca/Documents/other/baca/scf/stylesheets/clean_letter_14.ly' in \
        wrangler.score_external_asset_path_names
