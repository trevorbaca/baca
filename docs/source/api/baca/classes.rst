.. _baca--classes:

classes
=======

.. automodule:: baca.classes

.. currentmodule:: baca.classes

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.classes

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~Counter
   ~Cursor
   ~PaddedTuple
   ~Tree

.. autoclass:: Counter

   .. autosummary::
      :nosignatures:

      current
      start

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Counter.__call__

   .. container:: inherited

      .. automethod:: Counter.__format__

   .. container:: inherited

      .. automethod:: Counter.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Counter.current

   .. autoattribute:: Counter.start

.. autoclass:: Cursor

   .. autosummary::
      :nosignatures:

      next
      reset

   .. autosummary::
      :nosignatures:

      cyclic
      is_exhausted
      position
      singletons
      source
      suppress_exception

   .. autosummary::
      :nosignatures:

      __eq__
      __getitem__
      __hash__
      __iter__
      __len__

   .. autosummary::
      :nosignatures:

      from_pitch_class_segments

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Cursor.__eq__

   .. container:: inherited

      .. automethod:: Cursor.__format__

   .. automethod:: Cursor.__getitem__

   .. automethod:: Cursor.__hash__

   .. automethod:: Cursor.__iter__

   .. automethod:: Cursor.__len__

   .. container:: inherited

      .. automethod:: Cursor.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: Cursor.next

   .. automethod:: Cursor.reset

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. automethod:: Cursor.from_pitch_class_segments

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Cursor.cyclic

   .. autoattribute:: Cursor.is_exhausted

   .. autoattribute:: Cursor.position

   .. autoattribute:: Cursor.singletons

   .. autoattribute:: Cursor.source

   .. autoattribute:: Cursor.suppress_exception

.. autoclass:: PaddedTuple

   .. autosummary::
      :nosignatures:

      items
      pad

   .. autosummary::
      :nosignatures:

      __contains__
      __eq__
      __getitem__
      __hash__
      __iter__
      __len__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: PaddedTuple.__contains__

   .. automethod:: PaddedTuple.__eq__

   .. container:: inherited

      .. automethod:: PaddedTuple.__format__

   .. automethod:: PaddedTuple.__getitem__

   .. automethod:: PaddedTuple.__hash__

   .. automethod:: PaddedTuple.__iter__

   .. automethod:: PaddedTuple.__len__

   .. container:: inherited

      .. automethod:: PaddedTuple.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: PaddedTuple.items

   .. autoattribute:: PaddedTuple.pad

.. autoclass:: Tree

   .. autosummary::
      :nosignatures:

      get_payload
      iterate

   .. autosummary::
      :nosignatures:

      item_class
      items

   .. autosummary::
      :nosignatures:

      __contains__
      __eq__
      __format__
      __getitem__
      __hash__
      __len__
      __repr__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Tree.__contains__

   .. automethod:: Tree.__eq__

   .. automethod:: Tree.__format__

   .. automethod:: Tree.__getitem__

   .. automethod:: Tree.__hash__

   .. automethod:: Tree.__len__

   .. automethod:: Tree.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: Tree.get_payload

   .. automethod:: Tree.iterate

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Tree.item_class

   .. autoattribute:: Tree.items