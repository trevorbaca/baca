.. _baca--indicators:

indicators
==========

.. automodule:: baca.indicators

.. currentmodule:: baca.indicators

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.indicators

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~Accelerando
   ~Ritardando
   ~SpacingSection
   ~StaffLines

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

.. autoclass:: SpacingSection

   .. autosummary::
      :nosignatures:

      duration

   .. autosummary::
      :nosignatures:

      __eq__
      __hash__
      __str__

   .. autosummary::
      :nosignatures:

      from_string

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: SpacingSection.__eq__

   .. container:: inherited

      .. automethod:: SpacingSection.__format__

   .. automethod:: SpacingSection.__hash__

   .. container:: inherited

      .. automethod:: SpacingSection.__repr__

   .. automethod:: SpacingSection.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. automethod:: SpacingSection.from_string

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: SpacingSection.duration

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