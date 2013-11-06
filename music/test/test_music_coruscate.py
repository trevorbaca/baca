import py.test
from abjad import *
from baca import music


def test_music_coruscate_01():
    r'''Uniform talea and no cut / no dilation;
    result are unscaled beamed tuplets.
    '''

    talea, cut, dilation = [[1]], [[0]], [[0]]
    t = Container(music.coruscate(talea, cut, [4, 8, 8], dilation, 32))

    assert testtools.compare(
        t,
        r'''
        {
            {
                \set stemLeftBeamCount = #0
                \set stemRightBeamCount = #3
                c'32 [
                \set stemLeftBeamCount = #3
                \set stemRightBeamCount = #3
                c'32
                \set stemLeftBeamCount = #3
                \set stemRightBeamCount = #3
                c'32
                \set stemLeftBeamCount = #3
                \set stemRightBeamCount = #0
                c'32 ]
            }
            {
                \set stemLeftBeamCount = #0
                \set stemRightBeamCount = #3
                c'32 [
                \set stemLeftBeamCount = #3
                \set stemRightBeamCount = #3
                c'32
                \set stemLeftBeamCount = #3
                \set stemRightBeamCount = #3
                c'32
                \set stemLeftBeamCount = #3
                \set stemRightBeamCount = #3
                c'32
                \set stemLeftBeamCount = #3
                \set stemRightBeamCount = #3
                c'32
                \set stemLeftBeamCount = #3
                \set stemRightBeamCount = #3
                c'32
                \set stemLeftBeamCount = #3
                \set stemRightBeamCount = #3
                c'32
                \set stemLeftBeamCount = #3
                \set stemRightBeamCount = #0
                c'32 ]
            }
            {
                \set stemLeftBeamCount = #0
                \set stemRightBeamCount = #3
                c'32 [
                \set stemLeftBeamCount = #3
                \set stemRightBeamCount = #3
                c'32
                \set stemLeftBeamCount = #3
                \set stemRightBeamCount = #3
                c'32
                \set stemLeftBeamCount = #3
                \set stemRightBeamCount = #3
                c'32
                \set stemLeftBeamCount = #3
                \set stemRightBeamCount = #3
                c'32
                \set stemLeftBeamCount = #3
                \set stemRightBeamCount = #3
                c'32
                \set stemLeftBeamCount = #3
                \set stemRightBeamCount = #3
                c'32
                \set stemLeftBeamCount = #3
                \set stemRightBeamCount = #0
                c'32 ]
            }
        }
        '''
        )

    assert len(t) == 3


def test_music_coruscate_02():
    r'''Uniform talea with some cut / no dilation; 
    result are unscaled tuplets with cuts.
    '''

    talea, cut, dilation = [[1]], [[0, 0, 0, 1]], [[0]]
    t = Container(music.coruscate(talea, cut, [4, 4, 4, 4], dilation, 32))

    # TODO: make work again
    testtools.compare(
        t,
        r'''
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #3
            c'32 [
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #3
            c'32
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #0
            c'32 ]
            r32

            r32
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #3
            c'32 [
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #3
            c'32
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #0
            c'32 ]

            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #3
            c'32 []
            r32
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #3
            c'32 [
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #0
            c'32 ]

            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #3
            c'32 [
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #0
            c'32 ]
            r32
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #0
            c'32 []
        '''
        )

    assert len(t) == 4


def test_music_coruscate_03():
    r'''Uniform talea / no cut with some dilation;
    result are even tuplets, some scaled, some not.
    '''

    talea, cut, dilation = [[1]], [[0]], [[0, 3, 3]]
    t = Container(music.coruscate(talea, cut, [4, 4, 4], dilation, 32))

    # TODO: make work again
    testtools.compare(
        t,
        '''
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #3
            c'32 [
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #3
            c'32
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #3
            c'32
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #0
            c'32 ]
        \times 4/7 {
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #3
            c'32 [
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #3
            c'32
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #3
            c'32
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #3
            c'32
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #3
            c'32
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #3
            c'32
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #0
            c'32 ]
        }
        \times 4/7 {
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #3
            c'32 [
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #3
            c'32
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #3
            c'32
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #3
            c'32
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #3
            c'32
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #3
            c'32
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #0
            c'32 ]
        }
        \times 4/7 {
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #3
            c'32 [
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #3
            c'32
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #3
            c'32
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #3
            c'32
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #3
            c'32
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #3
            c'32
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #0
            c'32 ]
        }
        '''
        )


def test_music_coruscate_04():
    r'''Varied talea / no cut / no dilation ... with neat fit;
    gives splotchy but unscaled tuplets.
    '''

    talea, cut, dilation = [[1, 3]], [[0]], [[0]]
    t = Container(music.coruscate(talea, cut, [4, 4, 4], dilation, 32))

    # TOOD: make work again
    testtools.compare(
        t,
        r'''
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #3
            c'32 [
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #0
            c'16. ]

            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #2
            c'16. [
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #0
            c'32 ]

            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #3
            c'32 [
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #0
            c'16. ]
        '''
        )


def test_music_coruscate_05():
    r'''Varied talea / no cut / no dilation ... with uneven fit;
    gives scaled and sploty tuplets.
    '''

    t = Container(music.coruscate([[2, 3]], [[0]], [4, 4, 4], [[0]], 32))

    # TODO: make work again
    testtools.compare(
        t,
        r'''
        \times 4/5 {
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #2
            c'16 [
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #0
            c'16. ]
        }
        \times 4/5 {
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #2
            c'16. [
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #0
            c'16 ]
        }
        \times 4/5 {
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #2
            c'16 [
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #0
            c'16. ]
        }
        '''
        )


def test_music_coruscate_06():
    r'''Negative talea is allowed; negative elements congeal.
    '''

    t = Container(music.coruscate([[-1]], [[0]], [4, 4, 4], [[0]], 32))

    assert testtools.compare(
        t,
        r'''
        {
            {
                r8
            }
            {
                r8
            }
            {
                r8
            }
        }
        '''
        )


def test_music_coruscate_07():
    r'''Tie-valued rests split apart.
    '''

    t = Container(music.coruscate([[-1]], [[0]], [4, 4, 5], [[0]], 32))

    assert testtools.compare(

        t,
        r'''
        {
            {
                r8
            }
            {
                r8
            }
            {
                r8
                r32
            }
        }
        '''
        )


def test_music_coruscate_08():
    r'''Zero-valued talea not allowed.
    '''

    talea, cut, dilation = [[0]], [[0]], [[0]]

    statement = 'music.coruscate(talea, cut, [4, 4, 4], dilation, 32)'
    assert py.test.raises(AssertionError, statement)
