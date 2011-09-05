from abjad import *
from baca import music
import py.test


def test_music_coruscate_01():
   '''Uniform signal and no cut / no dilation;
   result are unscaled beamed tuplets.
   '''

   signal, cut, dilation = [[1]], [[0]], [[0]]
   t = Container(music.coruscate(signal, cut, [4, 8, 8], dilation, 32))

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

   assert len(t) == 3
   assert t.format == "{\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32 [\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #0\n\t\tc'32 ]\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32 [\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #0\n\t\tc'32 ]\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32 [\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #0\n\t\tc'32 ]\n\t}\n}"


def test_music_coruscate_02():
   '''Uniform signal with some cut / no dilation;
      result are unscaled tuplets with cuts.'''

   signal, cut, dilation = [[1]], [[0, 0, 0, 1]], [[0]]
   t = Container(music.coruscate(signal, cut, [4, 4, 4, 4], dilation, 32))

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

   assert len(t) == 4
   ## TODO: Make this work by changing some 0s to 3s and vice versa ##
   #assert t.format == "{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32 [\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #0\n\t\tc'32 ]\n\t\tr32\n\t\tr32\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32 [\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #0\n\t\tc'32 ]\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32 []\n\t\tr32\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32 [\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #0\n\t\tc'32 ]\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32 [\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #0\n\t\tc'32 ]\n\t\tr32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #0\n\t\tc'32 []\n}"


def test_music_coruscate_03():
   '''Uniform signal / no cut with some dilation;
      result are even tuplets, some scaled, some not.'''
   signal, cut, dilation = [[1]], [[0]], [[0, 3, 3]]
   t = Container(music.coruscate(signal, cut, [4, 4, 4], dilation, 32))
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
   ## TODO: fix me ##
   #assert t.format == "\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32 [\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #0\n\t\tc'32 ]\n\t\\times 4/7 {\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32 [\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #0\n\t\tc'32 ]\n\t}\n\t\\times 4/7 {\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32 [\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #0\n\t\tc'32 ]\n\t}"


def test_music_coruscate_04():
   '''Varied signal / no cut / no dilation ... with neat fit;
      gives splotchy but unscaled tuplets.'''
   signal, cut, dilation = [[1, 3]], [[0]], [[0]]
   t = Container(music.coruscate(signal, cut, [4, 4, 4], dilation, 32))
   '''
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
   ## TODO: FIXME ##
   #assert t.format == "\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tc'16. ]\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tc'16. [\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #0\n\t\tc'32 ]\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #3\n\t\tc'32 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tc'16. ]"


def test_music_coruscate_05():
   '''Varied signal / no cut / no dilation ... with uneven fit;
      gives scaled and sploty tuplets.'''
   t = Container(music.coruscate([[2, 3]], [[0]], [4, 4, 4], [[0]], 32))
   '''
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
   ## TODO: FIXME ##
   #assert t.format == "\t\\times 4/5 {\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tc'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tc'16. ]\n\t}\n\t\\times 4/5 {\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tc'16. [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tc'16 ]\n\t}\n\t\\times 4/5 {\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tc'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\tc'16. ]\n\t}"


def test_music_coruscate_06():
   '''Negative signal is allowed;
      negative elements congeal.'''

   t = Container(music.coruscate([[-1]], [[0]], [4, 4, 4], [[0]], 32))

   '''{
           {
                   r8
           }
           {
                   r8
           }
           {
                   r8
           }
   }'''

   assert t.format == '{\n\t{\n\t\tr8\n\t}\n\t{\n\t\tr8\n\t}\n\t{\n\t\tr8\n\t}\n}'


def test_music_coruscate_07():
   '''Tie-valued rests split apart.'''

   t = Container(music.coruscate([[-1]], [[0]], [4, 4, 5], [[0]], 32))

   '''
   {
           {
                   r8
           }
           {
                   r8
           }
           {
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #1
            r8 [
            \set stemLeftBeamCount = #3
            \set stemRightBeamCount = #0
            r32 ]
           }
   }
   '''

   assert t.format == '{\n\t{\n\t\tr8\n\t}\n\t{\n\t\tr8\n\t}\n\t{\n\t\tr8\n\t\tr32\n\t}\n}'
   #assert t.format == '{\n\t{\n\t\tr8\n\t}\n\t{\n\t\tr8\n\t}\n\t{\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #1\n\t\tr8 [\n\t\t\\set stemLeftBeamCount = #3\n\t\t\\set stemRightBeamCount = #0\n\t\tr32 ]\n\t}\n}'


def test_music_coruscate_08():
   '''Zero-valued signal not allowed.'''

   signal, cut, dilation = [[0]], [[0]], [[0]]

   assert py.test.raises(AssertionError, 
      'music.coruscate(signal, cut, [4, 4, 4], dilation, 32)')
