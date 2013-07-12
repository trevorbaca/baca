from abjad import *
import baca


def test_baca_pitch_CC_01():
    r'''Test __getitem__.
    '''

    assert len(baca.pitch.CC[0]) == 180
    assert len(baca.pitch.CC[1]) == 140
    assert len(baca.pitch.CC[2]) == 80
    assert len(baca.pitch.CC[3]) == 100
    assert len(baca.pitch.CC[4]) == 180
    assert len(baca.pitch.CC[5]) == 150
    assert len(baca.pitch.CC[6]) == 120
    assert len(baca.pitch.CC[7]) == 108


def test_baca_pitch_CC_02():
    r'''Test __len__.
    '''

    assert len(baca.pitch.CC) == 8


def test_baca_pitch_CC_03():
    r'''Test generator numbers.
    '''

    numbers = [80, 59, 56, 60, 83, 65, 79, 94]
    assert baca.pitch.CC._generator_chord_numbers == numbers


def test_baca_pitch_CC_04():
    r'''Test pivot numbers.
    '''

    numbers = [80, 75, 60, 73, 117, 69, 108, 99]
    assert baca.pitch.CC._pivot_chord_numbers == numbers


def test_baca_pitch_CC_05():
    r'''Test get signature one.
    '''

    assert baca.pitch.CC.get(1) is baca.pitch.CC[0]
    assert baca.pitch.CC.get(2) is baca.pitch.CC[1]
    assert baca.pitch.CC.get(3) is baca.pitch.CC[2]
    assert baca.pitch.CC.get(4) is baca.pitch.CC[3]
    assert baca.pitch.CC.get(5) is baca.pitch.CC[4]
    assert baca.pitch.CC.get(6) is baca.pitch.CC[5]
    assert baca.pitch.CC.get(7) is baca.pitch.CC[6]
    assert baca.pitch.CC.get(8) is baca.pitch.CC[7]


def test_baca_pitch_CCa06():
    r'''Test get signature two.
    '''

    assert baca.pitch.CC.get(1, 1) is baca.pitch.CC[0][0]
    assert baca.pitch.CC.get(1, 2) is baca.pitch.CC[0][1]
    assert baca.pitch.CC.get(1, 3) is baca.pitch.CC[0][2]
    assert baca.pitch.CC.get(1, 4) is baca.pitch.CC[0][3]


def test_baca_pitch_CC_07():
    r'''Test generators.
    '''

    staff = Staff(baca.pitch.CC.generator_chords)

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


def test_baca_pitch_CC_08():
    r'''Test pitch range.
    '''

    assert baca.pitch.CC.pitch_range == pitchtools.PitchRange(-39, 48)


def test_baca_pitch_CC_09():
    r'''Test pivots.
    '''

    staff = Staff(baca.pitch.CC.pivot_chords)

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
