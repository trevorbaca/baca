import baca


def test_ScorePackageWrangler_fix_structure_of_wrangled_packages_to_display_01():

    studio = baca.scf.studio.Studio()
    wrangler = studio.score_package_wrangler
    wrangler.session.show_all_scores()

    assert all(wrangler.fix_visible_wrangled_package_structures(prompt=False))
