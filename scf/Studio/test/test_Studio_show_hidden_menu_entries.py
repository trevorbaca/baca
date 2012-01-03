import baca


def test_Studio_show_hidden_menu_entries_01():

    studio = baca.scf.Studio()
    studio.run(user_input='hidden q')    
    assert studio.transcript[-2] == \
     ['     back (b)',
      '     exec statement (exec)',
      '     grep baca directories (grep)',
      '     edit client source (here)',
      '     show hidden items (hidden)',
      '     next score (next)',
      '     prev score (prev)',
      '     quit (q)',
      '     redraw (redraw)',
      '     score (score)',
      '     studio (studio)',
      '     show menu client (where)',
      '',
      '     work with repository (svn)',
      '     show active scores only (active)',
      '     show all scores (all)',
      '     show mothballed scores only (mb)',
      '']

