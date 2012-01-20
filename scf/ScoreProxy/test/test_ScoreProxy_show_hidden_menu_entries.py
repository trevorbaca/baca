import baca


def test_ScoreProxy_show_hidden_menu_entries_01():

    studio = baca.scf.Studio()
    studio.run(user_input='1 hidden q')

    assert studio.transcript[-2] == \
     ['     back (b)',
      '     exec statement (exec)',
      '     grep baca directories (grep)',
      '     edit client source (here)',
      '     show hidden items (hidden)',
      '     next score (next)',
      '     prev score (prev)',
      '     quit (q)',
      '     redraw (r)',
      '     score (score)',
      '     studio (studio)',
      '     toggle menu (tm)',
      '     show menu client (where)',
      '',
      '     manage repository (svn)',
      '     manage tags (tags)',
      '']
