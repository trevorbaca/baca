from abjad import *
from music import traverse

class TestVisitor(object):
   def __init__(self):
      self.visited = 0
      self.unvisited = 0
   def visit(self, node):
      self.visited += 1
   def unvisit(self, node):
      self.unvisited += 1

def test_traverse_01( ):
   t = Container(Note(0, (1, 16)) * 4)
   v = TestVisitor( )
   traverse(t, v)
   assert v.visited == 1 + 4
   assert v.unvisited == 1 + 4

def test_traverse_02( ):
   t = FixedDurationTuplet((4, 16), Note(0, (1, 16)) * 4)
   v = TestVisitor( )
   traverse(t, v)
   assert v.visited == 1 + 4
   assert v.unvisited == 1 + 4

def test_traverse_03( ):
   t = FixedMultiplierTuplet((4, 5), Note(0, (1, 16)) * 4)
   v = TestVisitor( )
   traverse(t, v)
   assert v.visited == 1 + 4
   assert v.unvisited == 1 + 4

def test_traverse_04( ):
   t = Measure((4, 16), Note(0, (1, 16)) * 4)
   v = TestVisitor( )
   traverse(t, v)
   assert v.visited == 1 + 4
   assert v.unvisited == 1 + 4

def test_traverse_05( ):
   t = Voice(Note(0, (1, 8)) * 8)
   v = TestVisitor( )
   traverse(t, v)
   assert v.visited == 1 + 8
   assert v.unvisited == 1 + 8

def test_traverse_06( ):
   t = Staff(Note(0, (1, 8)) * 8)
   v = TestVisitor( )
   traverse(t, v)
   assert v.visited == 1 + 8
   assert v.unvisited == 1 + 8

def test_traverse_07( ):
   t = Score(Staff(Note(0, (1, 8)) * 8) * 2)
   v = TestVisitor( )
   traverse(t, v)
   assert v.visited == 1 + (2 * (1 + 8))
   assert v.unvisited == 1 + (2 * (1 + 8))

def test_traverse_08( ):
   t = Score(Staff([ ]) * 4)
   v = TestVisitor( )
   traverse(t, v)
   assert v.visited == 1 + 4
   assert v.unvisited == 1 + 4
