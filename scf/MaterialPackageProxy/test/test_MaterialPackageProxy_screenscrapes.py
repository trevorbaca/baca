import baca


def test_MaterialPackageProxy_screenscrapes_01():
    '''Score material run from studio.
    '''


    studio = baca.scf.Studio()
    studio.run(user_input='all las m black q')
    
    assert studio.transcript[-2] == \
    ['Las manos m\xc3\xa1gicas - materials - black pcs',
      '',
      '     material definition - edit (mde)',
      '     material definition - execute (mdx)',
      '',
      '     output data - create (dc)',
      '     output data - inspect (di)',
      '',
      '     illustration builder - edit (ibe)',
      '     illustration builder - execute (ibx)',
      '',
      '     score stylesheet - select (sss)',
      '',
      '     output pdf - create (pdfc)',
      '     output pdf - inspect (pdfi)',
      '']


def test_MaterialPackageProxy_screenscrapes_02():
    '''Score material run independently.
    '''

    material_proxy = baca.scf.MaterialPackageProxy('manos.mus.materials.black_pcs')
    material_proxy.run('q')

    assert material_proxy.transcript[-2] == \
    ['Black pcs',
      '',
      '     material definition - edit (mde)',
      '     material definition - execute (mdx)',
      '',
      '     output data - create (dc)',
      '     output data - inspect (di)',
      '',
      '     illustration builder - edit (ibe)',
      '     illustration builder - execute (ibx)',
      '',
      '     score stylesheet - select (sss)',
      '',
      '     output pdf - create (pdfc)',
      '     output pdf - inspect (pdfi)',
      '']
