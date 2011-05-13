from abjad.tools import seqtools


class ChunkArray(list):
   '''Chunk array.
   '''

   def __init__(self, args):
      from archipel.mus.py.make.ArchipelChunk import ArchipelChunk
      assert all([isinstance(arg, ArchipelChunk) for arg in args])
      list.__init__(self, args)
      self._update_chunk_pointers( )

   ## OVERLOADS ##

   def __delitem__(self, i):
      self[i].prev_chunk, self[i].next_chunk = None, None
      list.__delitem__(self, i)
      self._update_chunk_pointers( )

   def __delslice__(self, start, stop):
      for chunk in self[start:stop]:
         chunk.prev_chunk, chunk.next_chunk = None, None
      list.__delslice__(self, start, stop)
      self._update_chunk_pointers( )

   def __setitem__(self, i, arg):
      self[i].prev_chunk, self[i].next_chunk = None, None
      list.__setitem__(self, i, arg)
      self._update_chunk_pointers( )

   def __setslice__(self, start, stop, arg):
      for chunk in self[start:stop]:
         chunk.prev_chunk, chunk.next_chunk = None, None
      list.__setslice__(self, start, stop, arg)
      self._update_chunk_pointers( )
      
   ## PRIVATE METHODS ##

   def _update_chunk_pointers(self):
      for left, right in seqtools.iterate_sequence_pairwise_strict(self):
         left.next_chunk = right
         right.prev_chunk = left
      if len(self):
         self[0].prev_chunk, self[-1].next_chunk = None, None

   ## PUBLIC METHODS ##

   def append(self, arg):
      list.append(self, arg)
      self._update_chunk_pointers( ) 

   def extend(self, args):
      list.extend(self, args)
      self._update_chunk_pointers( )

   def get(self, name_string):
      for chunk in self:
         if chunk.name_string == name_string:
            return chunk
      raise AttributeError

   def insert(self, i, arg):
      list.insert(self, i, arg)
      self._update_chunk_pointers( )

   def pop(self, i):
      self[i].prev_chunk, self[i].next_chunk = None, None
      list.pop(self, i)
      self._update_chunk_pointers( )   

   def remove(self, arg):
      arg.prev_chunk, arg.next_chunk = None, None
      list.remove(self, arg)
      self._update_chunk_pointers( )

   def reverse(self):
      list.reverse(self)
      self._update_chunk_pointers( )
