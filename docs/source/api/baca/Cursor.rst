.. _baca--Cursor:

Cursor
======

.. automodule:: baca.Cursor

.. currentmodule:: baca.Cursor

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.Cursor

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