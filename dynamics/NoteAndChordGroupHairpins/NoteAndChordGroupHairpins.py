from abjad.components import Chord
from abjad.components import Note
from abjad.tools import componenttools
from abjad.tools import leaftools
from abjad.tools import marktools
from abjad.tools import seqtools
from abjad.tools import spannertools
from baca.dynamics.DynamicsManager import DynamicsManager


class NoteAndChordGroupHairpins(DynamicsManager):
   '''Note and chord run hairpins.
   '''

   def __init__(self, hairpin_tokens = None):
      if hairpin_tokens is None:
         self.hairpin_tokens = [ ]
      else:
         self.hairpin_tokens = hairpin_tokens

   ## OVERLOADS ##

   def __call__(self, expr, offset = 0):
      leaves = list(leaftools.iterate_leaves_forward_in_expr(expr))
      groups = list(componenttools.yield_groups_of_mixed_klasses_in_sequence(leaves, (Note, Chord)))
      hairpin_tokens = seqtools.CyclicList(self.hairpin_tokens)
      for i, group in enumerate(groups):
         if len(group) == 1:
            start_dynamic = hairpin_token[0]
            ## TODO: fix dynamci mark and replace below with dynamic mark
            marktools.LilyPondCommandMark(start_dynamic, 'right')(group[0])
         else:
            hairpin_token = hairpin_tokens[offset+i]
            descriptor = ' '.join([x for x in hairpin_token if x])
            spannertools.HairpinSpanner(group, descriptor, include_rests = False)
      return expr
