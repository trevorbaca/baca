from abjad.components import Chord
from abjad.tools import pitchtools
import baca


## TEST OVERRIDES ##

def test_baca_pitch_CC_01( ):
   '''Test __getitem__.'''

   assert len(baca.pitch.CC[0]) == 180
   assert len(baca.pitch.CC[1]) == 140
   assert len(baca.pitch.CC[2]) == 80
   assert len(baca.pitch.CC[3]) == 100
   assert len(baca.pitch.CC[4]) == 180
   assert len(baca.pitch.CC[5]) == 150
   assert len(baca.pitch.CC[6]) == 120
   assert len(baca.pitch.CC[7]) == 108


def test_baca_pitch_CC_02( ):
   '''Test __len__.'''

   assert len(baca.pitch.CC) == 8


## TEST PRIVATE ATTRIBUTES ##

def test_baca_pitch_CC_03( ):
   '''Test generator numbers.'''

   assert baca.pitch.CC._generator_chord_numbers == [80, 59, 56, 60, 83, 65, 79, 94]


def test_baca_pitch_CC_04( ):
   '''Test pivot numbers.'''

   assert baca.pitch.CC._pivot_chord_numbers == [80, 75, 60, 73, 117, 69, 108, 99]


## TEST PUBLIC METHODS ## 

def test_baca_pitch_CC_05( ):
   '''Test get signature one.'''

   assert baca.pitch.CC.get(1) is baca.pitch.CC[0]
   assert baca.pitch.CC.get(2) is baca.pitch.CC[1]
   assert baca.pitch.CC.get(3) is baca.pitch.CC[2]
   assert baca.pitch.CC.get(4) is baca.pitch.CC[3]
   assert baca.pitch.CC.get(5) is baca.pitch.CC[4]
   assert baca.pitch.CC.get(6) is baca.pitch.CC[5]
   assert baca.pitch.CC.get(7) is baca.pitch.CC[6]
   assert baca.pitch.CC.get(8) is baca.pitch.CC[7]


def test_baca_pitch_CCaab( ):
   '''Test get signature two.'''

   assert baca.pitch.CC.get(1, 1) is baca.pitch.CC[0][0]
   assert baca.pitch.CC.get(1, 2) is baca.pitch.CC[0][1]
   assert baca.pitch.CC.get(1, 3) is baca.pitch.CC[0][2]
   assert baca.pitch.CC.get(1, 4) is baca.pitch.CC[0][3]


## TEST PUBLIC ATTRIBUTES ##

def test_baca_pitch_CC_06( ):
   '''Test generators.'''
   
   assert baca.pitch.CC.generator_chords == [
      Chord("<c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4"),
      Chord("<c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4"),
      Chord("<e b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4"),
      Chord("<e c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4"),
      Chord("<c ef b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4"),
      Chord("<d g bf c' ef' f' b' cs'' e'' fs''' af''' a''''>4"),
      Chord("<d bf b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4"),
      Chord("<c b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4")]


def test_baca_pitch_CC_07( ):
   '''Test pitch range.'''

   assert baca.pitch.CC.pitch_range == pitchtools.PitchRange(-39, 48)


def test_baca_pitch_CC_08( ):
   '''Test pivots.'''

   assert baca.pitch.CC.pivot_chords == [
      Chord("<c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4"),
      Chord("<e b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4"),
      Chord("<e c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4"),
      Chord("<c ef b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4"),
      Chord("<d g bf c' ef' f' b' cs'' e'' fs''' af''' a''''>4"),
      Chord("<d bf b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4"),
      Chord("<c b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4"),
      Chord("<c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4")]
