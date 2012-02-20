import baca


def test_ChunkPackageWrangler_read_only_attributes_01():

    studio = baca.scf.studio.Studio()
    wrangler = studio.chunk_package_wrangler
    assert not wrangler.session.is_in_score

    assert wrangler.breadcrumb == 'sketches'
    assert wrangler.current_wrangler_target_package_importable_name == 'baca.sketches'
    assert all([
        x.startswith('baca.sketches.') for x in wrangler.score_external_wrangled_package_importable_names])

    assert wrangler.score_external_wrangler_target_package_importable_name == 'baca.sketches'
    assert wrangler.score_internal_wrangler_target_package_importable_name_suffix == 'mus.chunks'

    assert wrangler.temporary_package_importable_name == 'baca.sketches.__temporary_package'

    assert 'baca.sketches' in wrangler.wrangler_target_package_importable_names
    assert 'aracilik.mus.chunks' in wrangler.wrangler_target_package_importable_names


def test_ChunkPackageWrangler_read_only_attributes_02():

    studio = baca.scf.studio.Studio()
    wrangler = studio.chunk_package_wrangler
    wrangler.session.current_score_package_short_name = 'aracilik'
    assert wrangler.session.is_in_score

    assert wrangler.breadcrumb == 'chunks'

    assert wrangler.current_wrangler_target_package_importable_name == 'aracilik.mus.chunks'

    assert all([
        x.startswith('baca.sketches.') for x in wrangler.score_external_wrangled_package_importable_names])
    assert wrangler.score_external_wrangler_target_package_importable_name == 'baca.sketches'

    assert wrangler.score_internal_wrangler_target_package_importable_name_suffix == 'mus.chunks'

    assert wrangler.temporary_package_importable_name == 'aracilik.mus.chunks.__temporary_package'

    assert 'baca.sketches' in wrangler.wrangler_target_package_importable_names
    assert 'aracilik.mus.chunks' in wrangler.wrangler_target_package_importable_names
