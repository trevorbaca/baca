from abjad import *
import baca


def test_baca_dynamics_NoteAndChordRunHairpins___call___01( ):

   
   hairpins = baca.dynamics.NoteAndChordGroupHairpins( )
   hairpins.hairpin_tokens.append(('p', '<', 'f'))
   hairpins.hairpin_tokens.append(('p', '<', 'f'))
   hairpins.hairpin_tokens.append(('pp', '<', 'p'))

   staff = Staff("c'8 d'8 r8 e'8 f'8 r8 g'8")
   hairpins(staff)

   r'''
   \new Staff {
      c'8 \< \p
      d'8 \f
      r8
      e'8 \< \p
      f'8 \f
      r8
      g'8 \p
   }
   '''

   assert staff.format == "\\new Staff {\n\tc'8 \\< \\p\n\td'8 \\f\n\tr8\n\te'8 \\< \\p\n\tf'8 \\f\n\tr8\n\tg'8 \\p\n}"
