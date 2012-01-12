import baca


def test_MaterialProxy_run_screenscrapes_01():
    '''Score material run from studio.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='all las m 2 q')
    
    assert studio.transcript[-2] == \
    ['Las manos m\xc3\xa1gicas - materials - black pcs',
      '',
      '     material definition - edit (mde)',
      '     material definition - execute (mdx)',
      '',
      '     score builder - edit (sbe)',
      '     score builder - execute (sbx)',
      '',
      '     score stylesheet - select (sss)',
      '',
      '     output data - recreate (dc)',
      '     output data - inspect (di)',
      '',
      '     output pdf - recreate (pdfc)',
      '     output pdf - inspect (pdfi)',
      '']


def test_MaterialProxy_run_screenscrapes_02():
    '''Score material run independently.
    '''

    material_proxy = baca.scf.MaterialProxy('manos.mus.materials.black_pcs')
    material_proxy.run('q')

    assert material_proxy.transcript[-2] == \
    ['Black pcs',
      '',
      '     material definition - edit (mde)',
      '     material definition - execute (mdx)',
      '',
      '     score builder - edit (sbe)',
      '     score builder - execute (sbx)',
      '',
      '     score stylesheet - select (sss)',
      '',
      '     output data - recreate (dc)',
      '     output data - inspect (di)',
      '',
      '     output pdf - recreate (pdfc)',
      '     output pdf - inspect (pdfi)',
      '']
