import baca


def test_ScorePackageWrangler_fix_visible_wrangled_assets_01():

    studio = baca.scf.studio.Studio()
    wrangler = studio.score_package_wrangler
    wrangler.session.show_all_scores()

    assert all(wrangler.fix_visible_wrangled_assets(prompt=False))
