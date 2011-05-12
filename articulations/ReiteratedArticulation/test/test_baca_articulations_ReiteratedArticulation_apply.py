from abjad import *
import baca


def test_baca_articulations_ReiteratedArticulation_apply_01( ):

   reiterated_articulation = baca.articulations.ReiteratedArticulation(['^', '.'])
   staff = Staff("c'8 d'8 r8 e'8 f'8 r8 g'8 r8")
   reiterated_articulation.apply(staff)

   r'''
   \new Staff {
      c'8 -\marcato -\staccato
      d'8 -\marcato -\staccato
      r8
      e'8 -\marcato -\staccato
      f'8 -\marcato -\staccato
      r8
      g'8 -\marcato -\staccato
      r8
   }
   '''

   assert staff.format == "\\new Staff {\n\tc'8 -\\marcato -\\staccato\n\td'8 -\\marcato -\\staccato\n\tr8\n\te'8 -\\marcato -\\staccato\n\tf'8 -\\marcato -\\staccato\n\tr8\n\tg'8 -\\marcato -\\staccato\n\tr8\n}"
