from abjad import *


def cross_staves_down(local_leaves, remote_staff, breakpitch, 
   local_beam_positions, remote_beam_positions):
   for leaf in instances(local_leaves, '_Leaf'):
      if (isinstance(leaf, Note) and leaf.pitch.number <= breakpitch) or \
         (isinstance(leaf, Chord) and leaf.pitches[0].number <= breakpitch):
            leaf.staff = remote_staff
            Override(leaf, 'Stem', 'direction', 'up')
            #if leaf.beam.first:
            if leaf.beam.opening:
               Override(leaf, 'Beam', 'positions', remote_beam_positions)
      elif isinstance(leaf, (Note, Chord)):
         Override(leaf, 'Stem', 'direction', 'down')
         #if leaf.beam.first:
         if leaf.beam.opening:
            Override(leaf, 'Beam', 'positions', local_beam_positions)
