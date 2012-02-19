import baca


def test_ScorePackageWrangler_fix_package_structures_01():

    studio = baca.scf.studio.Studio()
    wrangler = studio.score_package_wrangler
    wrangler.session.show_all_scores()

    assert all(wrangler.fix_package_structures(prompt=False))
