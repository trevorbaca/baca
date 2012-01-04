import baca


def test_MaterialProxy_run_screenscrapes_01():
    '''Score material run from studio.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='all las m 2 q')
    
    assert studio.transcript[-2] == \
     ['Las manos m\xc3\xa1gicas - materials - manos black pcs',
      '',
      '     material definition - edit (mde)',
      '     material definition - execute (mdx)',
      '',
      '     score builder - edit (sbe)',
      '     score builder - execute (sbx)',
      '',
      '     output data - recreate (dc)',
      '     output data - inspect (di)',
      '',
      '     output ly - recreate (lyc)',
      '     output ly - inspect (lyi)',
      '',
      '     output pdf - recreate (pdfc)',
      '     output pdf - inspect (pdfi)',
      '',
      '     delete material (del)',
      '     edit initializer (init)',
      '     regenerate material (reg)',
      '     rename material (ren)',
      '     summarize material (sum)',
      '']


def test_MaterialProxy_run_screenscrapes_02():
    '''Score material run independently.
    '''

    material_proxy = baca.scf.MaterialProxy('manos.mus.materials.manos_black_pcs')
    material_proxy.run('q')

    assert material_proxy.transcript[-2] == \
     ['Manos black pcs',
      '',
      '     material definition - edit (mde)',
      '     material definition - execute (mdx)',
      '',
      '     score builder - edit (sbe)',
      '     score builder - execute (sbx)',
      '',
      '     output data - recreate (dc)',
      '     output data - inspect (di)',
      '',
      '     output ly - recreate (lyc)',
      '     output ly - inspect (lyi)',
      '',
      '     output pdf - recreate (pdfc)',
      '     output pdf - inspect (pdfi)',
      '',
      '     delete material (del)',
      '     edit initializer (init)',
      '     regenerate material (reg)',
      '     rename material (ren)',
      '     summarize material (sum)',
      '']
