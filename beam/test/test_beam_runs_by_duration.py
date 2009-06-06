from abjad import *
from baca.beam.beamtools import beamRunsByDuration



def test_beam_runs_by_duration_01( ):
   v = Voice(Note(0, (1, 16)) * 8)
   ## TODO: FIXME ##
#   assert not v.spanners.get( )
#   beamRunsByDuration(v, [(1, 8)])
#   spanners = v.spanners.get( )
#   assert len(spanners) == 4
#   assert spanners[0].leaves == v[0 : 2]
#   assert spanners[1].leaves == v[2: 4]
#   assert spanners[2].leaves == v[4 : 6]
#   assert spanners[3].leaves == v[6: 8]


def test_beam_runs_by_duration_02( ):
   v = Voice(Note(0, (1, 16)) * 8)
   ## TODO: FIXME ##
#   assert not v.spanners.get( )
#   beamRunsByDuration(v, [(1, 4)])
#   spanners = v.spanners.get( )
#   assert len(spanners) == 2
#   assert spanners[0].leaves == v[0 : 4]
#   assert spanners[1].leaves == v[4 : 8]


def test_beam_runs_by_duration_03( ):
   v = Voice(Note(0, (1, 16)) * 8)
   ## TODO: FIXME ##
#   assert not v.spanners.get( )
#   beamRunsByDuration(v, [(1, 16), (3, 16)])
#   spanners = v.spanners.get( )
#   assert len(spanners) == 4
#   assert spanners[0].leaves == v[0 : 1]
#   assert spanners[1].leaves == v[1 : 4]
#   assert spanners[2].leaves == v[4 : 5]
#   assert spanners[3].leaves == v[5 : 8]


def test_beam_runs_by_duration_04( ):
   v = Voice(Note(0, (1, 16)) * 8)
   ## TODO: FIXME ##
#   assert not v.spanners.get( )
#   beamRunsByDuration(v, [(5, 16)])
#   spanners = v.spanners.get( )
#   assert len(spanners) == 2
#   assert spanners[0].leaves == v[0 : 5]
#   assert spanners[1].leaves == v[5 : 8]


def test_beam_runs_by_duration_05( ):
   '''No unclean nibs.'''
   t = Staff([
      Note(0, (1, 16)),
      Note(1, (1, 16)),
      Note(2, (1, 8)),
      Note(3, (1, 8)),
      Note(4, (1, 16)),
      Note(5, (1, 16))])
   beamRunsByDuration(t, [(2, 4)])
   assert t[0].beam.counts == (0, 2)
   assert t[1].beam.counts == (2, 1)
   assert t[2].beam.counts == (1, 1)
   assert t[3].beam.counts == (1, 1)
   assert t[4].beam.counts == (1, 2)
   assert t[5].beam.counts == (2, 0)


def test_beam_runs_by_duration_06( ):
   '''Inside beams, nibs point to rests.'''
   t = Staff([
      Rest((1, 16)),
      Note(0, (1, 16)),
      Note(0, (1, 16)),
      Rest((1, 16))])
   beamRunsByDuration(t, [(1, 4)])
   ## TODO: FIXME ##
   #assert t[1].beam.counts == (2, 2)
   #assert t[2].beam.counts == (2, 2)
