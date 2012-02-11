from baca.scf.predicates import predicates


def test_predicates_01():

    assert predicates.is_available_underscore_delimited_lowercase_package_name('asdf')
    assert predicates.is_available_underscore_delimited_lowercase_package_name('baca.asdf')
    assert predicates.is_available_underscore_delimited_lowercase_package_name('baca.scf.asdf')
    assert predicates.is_available_underscore_delimited_lowercase_package_name('baca.materials.asdf')
    assert predicates.is_available_underscore_delimited_lowercase_package_name('baca.sketches.asdf')

    assert not predicates.is_available_underscore_delimited_lowercase_package_name('baca')
    assert not predicates.is_available_underscore_delimited_lowercase_package_name('baca.scf')
    assert not predicates.is_available_underscore_delimited_lowercase_package_name('baca.materials')
    assert not predicates.is_available_underscore_delimited_lowercase_package_name('baca.sketches')


def test_predicates_02():

    assert predicates.is_existing_package_name('baca')
    assert predicates.is_existing_package_name('baca.scf')
    assert predicates.is_existing_package_name('baca.materials')
    assert predicates.is_existing_package_name('baca.sketches')

    assert not predicates.is_existing_package_name('asdf')
    assert not predicates.is_existing_package_name('baca.asdf')
    assert not predicates.is_existing_package_name('baca.scf.asdf')
    assert not predicates.is_existing_package_name('baca.materials.asdf')
    assert not predicates.is_existing_package_name('baca.sketches.asdf')



def test_predicates_03():

    assert predicates.is_boolean(True)
    assert predicates.is_boolean(False)

    assert not predicates.is_boolean(None)
    assert not predicates.is_boolean('')
    assert not predicates.is_boolean(0)
    assert not predicates.is_boolean(1)
