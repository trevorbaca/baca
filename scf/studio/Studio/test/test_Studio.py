import scf


def test_Studio_01():
    '''Attributes.
    '''

    studio = scf.studio.Studio()

    assert studio.class_name == 'Studio'
    assert isinstance(studio.home_package_proxy, scf.proxies.HomePackageProxy)
    assert isinstance(studio.score_package_wrangler, scf.wranglers.ScorePackageWrangler)
    assert studio.source_file_name == \
        '/Users/trevorbaca/Documents/other/baca/scf/studio/Studio/Studio.py'
    assert studio.spaced_class_name == 'studio'


def test_Studio_02():
    '''Main menu.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='q')
    
    assert studio.transcript[-2] == \
    ['Studio - active scores',
     '',
     '     1: Betörung (2012)',
     '     2: Čáry (2006)',
     "     3: L'archipel du corps (2011)",
     "     4: L'imaginare (2010)",
     '     5: Lidércfény (2008)',
     '     6: Mon seul désir (2009)',
     '     7: Poème récursif (2005)',
     '     8: Red Shift Hijinks (2005)',
     '     9: Sekka (2007)',
     '',
     '     materials (m)',
     '     sketches (k)',
     '     new score (new)',
     '']


def test_Studio_03():
    '''Main menu to score menu.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='1 q')

#    assert studio.transcript[-2] == [
#     "L'archipel du corps (2011)",
#     '',
#     '     Chunks',
#     '',
#     '     [create chunk] (ch)',
#     '',
#     '     Materials',
#     '',
#     '     create interactive material (mi)',
#     '     create static material (ms)',
#     '',
#     '     Setup',
#     '',
#     '     forces tagline (ft)',
#     '     performers (pf)',
#     '     title (tl)',
#     '     year of completion (yr)',
#     '']


def test_Studio_04():
    '''Main menu. Mothballed scores only.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='mb q')
    
    assert studio.transcript[-2] == \
    ['Studio - mothballed scores',
     '',
     '     1: Arac\xc4\xb1l\xc4\xb1k',
     '     2: Chrysanthemums (1995)',
     '     3: Jivan Mukti',
     '     4: Las manos mágicas',
     '     5: Manifolds',
     '     6: Tack (1996)',
     '     7: Territoires',
     '     8: Zeit (1998)',
     '',
     '     materials (m)',
     '     sketches (k)',
     '     new score (new)',
     '']


def test_Studio_05():
    '''Main menu to score menu to tags menu.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='1 tags q')
    assert studio.ts == (6,)


def test_Studio_06():
    '''Main menu to svn menu.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='svn q')

    assert studio.transcript[-2] == [
      'Studio - active scores - repository commands',
      '',
      '     add',
      '     ci',
      '     st',
      '     up',
      '',
      '     add_scores',
      '     ci_scores',
      '     st_scores',
      '     up_scores',
      '',
      '     pytest',
      '     pytest_scores',
      '     pytest_all',
      '']


def test_Studio_07():
    '''Main menu header is the same even after state change to secondary menu.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='q')
    assert studio.transcript[-2][0] == 'Studio - active scores'

    studio.run(user_input='svn q')
    assert studio.transcript[-2][0] == 'Studio - active scores - repository commands'

    studio.run(user_input='svn b q')
    assert studio.transcript[-2][0] == 'Studio - active scores'


def test_Studio_08():
    '''Junk works.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='foo q')
    assert studio.ts == (4, (0, 2))

    studio.run(user_input='foo bar q')
    assert studio.ts == (6, (0, 2, 4))


def test_Studio_09():
    '''Back is handled correctly.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='b q')
    assert studio.ts == (4, (0, 2))


def test_Studio_10():
    '''Exec works.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='exec 2**30 q')

    assert studio.transcript[1] == ['SCF> exec', '']
    assert studio.transcript[2] == ['XCF> 2**30']
    assert studio.transcript[3] == ['1073741824', '']
    assert studio.transcript[4] == ['SCF> q', '']


def test_Studio_11():
    '''Exec protects against senseless input.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='exec foo q')

    assert studio.transcript[1] == ['SCF> exec', '']
    assert studio.transcript[2] == ['XCF> foo']
    assert studio.transcript[3] == ['Expression not executable.', '']
    assert studio.transcript[4] == ['SCF> q', '']


def test_Studio_12():
    '''Shared session.
    '''

    studio = scf.studio.Studio()

    assert studio.session is studio.home_package_proxy.session
    assert studio.session is studio.score_package_wrangler.session


def test_Studio_13():
    '''Backtracking stu* shortcut.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='Mon perf studio q')
    ts_1 = studio.ts

    studio = scf.studio.Studio()
    studio.run(user_input='Mon perf stu q')
    ts_2 = studio.ts
    
    assert ts_1 == ts_2


def test_Studio_14():
    '''Backtracking sco* shortcut.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='Mon perf score q')
    ts_1 = studio.ts

    studio = scf.studio.Studio()
    studio.run(user_input='Mon perf sco q')
    ts_2 = studio.ts
    
    assert ts_1 == ts_2
