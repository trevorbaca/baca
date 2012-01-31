import baca


def test_MaterialPackageWrangler_run_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='m q')
    assert studio.ts == (4,)

    studio.run(user_input='m b q')
    assert studio.ts == (6, (0, 4))

    studio.run(user_input='m studio q')
    assert studio.ts == (6, (0, 4))

    studio.run(user_input='m score q')
    assert studio.ts == (6, (2, 4))

    studio.run(user_input='m asdf q')
    assert studio.ts == (6, (2, 4))


def test_MaterialPackageWrangler_run_02():
    '''Breadcrumbs work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='m q')
    assert studio.transcript[-2][0] == 'Studio - materials'


def test_MaterialPackageWrangler_run_03():
    '''Make data package. Delete package.
    '''
    
    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testdata')

    studio.run(user_input='m d testdata default default q')
    assert studio.package_exists('baca.materials.testdata')

    studio.run(user_input='m testdata del remove default q')
    assert not studio.package_exists('baca.materials.testdata')


def test_MaterialPackageWrangler_run_04():
    '''Make data package. Create output material. Delete package." 
    '''

    studio = baca.scf.Studio()
    assert not studio.package_exists('baca.materials.testdata')

    studio.run(user_input='m d testdata default default '
        'testdata mdcanned canned_testdata_material_definition.py default '
        'dc default q')
    assert studio.package_exists('baca.materials.testdata')

    studio.run(user_input='m testdata del remove default q')
    assert not studio.package_exists('baca.materials.testdata')
