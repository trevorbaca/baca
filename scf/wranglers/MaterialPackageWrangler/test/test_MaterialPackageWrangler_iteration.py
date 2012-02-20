import baca


def test_MaterialPackageWrangler_iteration_01():

    studio = baca.scf.studio.Studio()
    wrangler = studio.material_package_wrangler
    assert not wrangler.session.is_in_score

    assert 'manos.mus.materials.aggregates' in wrangler.list_score_internal_wrangled_package_importable_names()
    assert 'manos.mus.materials.aggregates' not in \
        wrangler.list_score_internal_wrangled_package_importable_names(head='aracilik')
    assert wrangler.list_score_internal_wrangled_package_importable_names(head='asdf') == []
