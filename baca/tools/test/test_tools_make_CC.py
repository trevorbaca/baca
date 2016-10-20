# -*- coding: utf-8 -*-
import baca
from abjad import *
CC = baca.tools.make_CC()


def test_tools_make_CC_01():
    r'''Test __getitem__.
    '''

    assert len(CC[0]) == 180
    assert len(CC[1]) == 140
    assert len(CC[2]) == 80
    assert len(CC[3]) == 100
    assert len(CC[4]) == 180
    assert len(CC[5]) == 150
    assert len(CC[6]) == 120
    assert len(CC[7]) == 108


def test_tools_make_CC_02():
    r'''Test __len__.
    '''

    assert len(CC) == 8


def test_tools_make_CC_03():
    r'''Test generator numbers.
    '''

    numbers = [80, 59, 56, 60, 83, 65, 79, 94]
    assert CC._generator_chord_numbers == numbers


def test_tools_make_CC_04():
    r'''Test pivot numbers.
    '''

    numbers = [80, 75, 60, 73, 117, 69, 108, 99]
    assert CC._pivot_chord_numbers == numbers


def test_tools_make_CC_05():
    r'''Test get signature one.
    '''

    assert CC.get(1) is CC[0]
    assert CC.get(2) is CC[1]
    assert CC.get(3) is CC[2]
    assert CC.get(4) is CC[3]
    assert CC.get(5) is CC[4]
    assert CC.get(6) is CC[5]
    assert CC.get(7) is CC[6]
    assert CC.get(8) is CC[7]


def test_tools_make_CCa06():
    r'''Test get signature two.
    '''

    assert CC.get(1, 1) is CC[0][0]
    assert CC.get(1, 2) is CC[0][1]
    assert CC.get(1, 3) is CC[0][2]
    assert CC.get(1, 4) is CC[0][3]


def test_tools_make_CC_07():
    r'''Test generators.
    '''

    staff = Staff(CC.generator_chords)

    assert systemtools.TestManager.compare(
        staff,
        r"""
        \new Staff {
            <c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4 - \markup { 1-80 }
            <c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4 - \markup { 2-59 }
            <e b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4 - \markup { 3-56 }
            <e c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4 - \markup { 4-60 }
            <c ef b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4 - \markup { 5-83 }
            <d g bf c' ef' f' b' cs'' e'' fs''' af''' a''''>4 - \markup { 6-65 }
            <d bf b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4 - \markup { 7-79 }
            <c b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4 - \markup { 8-94 }
        }
        """
        )


def test_tools_make_CC_08():
    r'''Test pitch range.
    '''

    assert CC.pitch_range == pitchtools.PitchRange('[A0, C8]')


def test_tools_make_CC_09():
    r'''Test pivots.
    '''

    staff = Staff(CC.pivot_chords)

    assert systemtools.TestManager.compare(
        staff,
        r"""
        \new Staff {
            <c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4 - \markup { 1-80 }
            <e b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4 - \markup { 2-75 }
            <e c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4 - \markup { 3-60 }
            <c ef b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4 - \markup { 4-73 }
            <d g bf c' ef' f' b' cs'' e'' fs''' af''' a''''>4 - \markup { 5-117 }
            <d bf b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4 - \markup { 6-69 }
            <c b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4 - \markup { 7-108 }
            <c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4 - \markup { 8-99 }
        }
        """
        )
