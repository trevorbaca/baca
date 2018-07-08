.. _baca--indicatorlib:

indicatorlib
============

.. automodule:: baca.indicatorlib

.. currentmodule:: baca.indicatorlib

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.indicatorlib

.. raw:: html

   <hr/>

.. rubric:: (5) Utilities
   :class: section-header

.. autosummary::
   :nosignatures:

   ~LBSD
   ~StaffLines

.. autoclass:: LBSD

   .. autosummary::
      :nosignatures:

      alignment_distances
      y_offset

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: LBSD.__format__

   .. container:: inherited

      .. automethod:: LBSD.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: LBSD.alignment_distances

   .. autoattribute:: LBSD.y_offset

.. autoclass:: StaffLines

   .. autosummary::
      :nosignatures:

      context
      hide
      line_count
      persistent

   .. autosummary::
      :nosignatures:

      __eq__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: StaffLines.__eq__

   .. container:: inherited

      .. automethod:: StaffLines.__format__

   .. container:: inherited

      .. automethod:: StaffLines.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: StaffLines.context

   .. autoattribute:: StaffLines.hide

   .. autoattribute:: StaffLines.line_count

   .. autoattribute:: StaffLines.persistent

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~Accelerando
   ~Ritardando

.. autoclass:: Accelerando

   .. autosummary::
      :nosignatures:

      context
      hide
      markup
      persistent
      tweaks

   .. autosummary::
      :nosignatures:

      __str__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Accelerando.__copy__

   .. container:: inherited

      .. automethod:: Accelerando.__eq__

   .. container:: inherited

      .. automethod:: Accelerando.__format__

   .. container:: inherited

      .. automethod:: Accelerando.__hash__

   .. container:: inherited

      .. automethod:: Accelerando.__repr__

   .. automethod:: Accelerando.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Accelerando.context

   .. autoattribute:: Accelerando.hide

   .. autoattribute:: Accelerando.markup

   .. autoattribute:: Accelerando.persistent

   .. autoattribute:: Accelerando.tweaks

.. autoclass:: Ritardando

   .. autosummary::
      :nosignatures:

      context
      hide
      markup
      persistent
      tweaks

   .. autosummary::
      :nosignatures:

      __str__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Ritardando.__copy__

   .. container:: inherited

      .. automethod:: Ritardando.__eq__

   .. container:: inherited

      .. automethod:: Ritardando.__format__

   .. container:: inherited

      .. automethod:: Ritardando.__hash__

   .. container:: inherited

      .. automethod:: Ritardando.__repr__

   .. automethod:: Ritardando.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Ritardando.context

   .. autoattribute:: Ritardando.hide

   .. autoattribute:: Ritardando.markup

   .. autoattribute:: Ritardando.persistent

   .. autoattribute:: Ritardando.tweaks