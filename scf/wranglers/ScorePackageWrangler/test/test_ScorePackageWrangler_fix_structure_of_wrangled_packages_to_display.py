import baca


def test_ScorePackageWrangler_fix_structure_of_visible_wrangled_packages_01():

    studio = baca.scf.studio.Studio()
    wrangler = studio.score_package_wrangler
    wrangler.session.show_all_scores()

    assert all(wrangler.fix_structure_of_visible_wrangled_packages(prompt=False))
