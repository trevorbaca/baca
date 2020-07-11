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
   ~BarExtent
   ~Markup
   ~Ritardando
   ~SpacingSection
   ~StaffLines

.. autoclass:: Accelerando

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __eq__
      __hash__
      __repr__
      __str__
      context
      hide
      markup
      parameter
      persistent
      tweaks

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Accelerando.__eq__

   .. automethod:: Accelerando.__hash__

   .. automethod:: Accelerando.__repr__

   .. automethod:: Accelerando.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Accelerando.context

   .. autoattribute:: Accelerando.hide

   .. autoattribute:: Accelerando.markup

   .. autoattribute:: Accelerando.parameter

   .. autoattribute:: Accelerando.persistent

   .. autoattribute:: Accelerando.tweaks

.. autoclass:: BarExtent

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __eq__
      __format__
      __repr__
      context
      hide
      line_count
      persistent

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: BarExtent.__eq__

   .. automethod:: BarExtent.__format__

   .. automethod:: BarExtent.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: BarExtent.context

   .. autoattribute:: BarExtent.hide

   .. autoattribute:: BarExtent.line_count

   .. autoattribute:: BarExtent.persistent

.. autoclass:: Markup

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      boxed

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Markup.__add__

   .. container:: inherited

      .. automethod:: Markup.__copy__

   .. container:: inherited

      .. automethod:: Markup.__eq__

   .. container:: inherited

      .. automethod:: Markup.__hash__

   .. container:: inherited

      .. automethod:: Markup.__lt__

   .. container:: inherited

      .. automethod:: Markup.__radd__

   .. container:: inherited

      .. automethod:: Markup.__repr__

   .. container:: inherited

      .. automethod:: Markup.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Markup.bold

   .. container:: inherited

      .. automethod:: Markup.box

   .. automethod:: Markup.boxed

   .. container:: inherited

      .. automethod:: Markup.bracket

   .. container:: inherited

      .. automethod:: Markup.caps

   .. container:: inherited

      .. automethod:: Markup.center_align

   .. container:: inherited

      .. automethod:: Markup.circle

   .. container:: inherited

      .. automethod:: Markup.dynamic

   .. container:: inherited

      .. automethod:: Markup.finger

   .. container:: inherited

      .. automethod:: Markup.fontsize

   .. container:: inherited

      .. automethod:: Markup.general_align

   .. container:: inherited

      .. automethod:: Markup.halign

   .. container:: inherited

      .. automethod:: Markup.hcenter_in

   .. container:: inherited

      .. automethod:: Markup.huge

   .. container:: inherited

      .. automethod:: Markup.italic

   .. container:: inherited

      .. automethod:: Markup.larger

   .. container:: inherited

      .. automethod:: Markup.normal_text

   .. container:: inherited

      .. automethod:: Markup.override

   .. container:: inherited

      .. automethod:: Markup.pad_around

   .. container:: inherited

      .. automethod:: Markup.pad_markup

   .. container:: inherited

      .. automethod:: Markup.pad_to_box

   .. container:: inherited

      .. automethod:: Markup.parenthesize

   .. container:: inherited

      .. automethod:: Markup.raise_

   .. container:: inherited

      .. automethod:: Markup.rotate

   .. container:: inherited

      .. automethod:: Markup.sans

   .. container:: inherited

      .. automethod:: Markup.scale

   .. container:: inherited

      .. automethod:: Markup.small

   .. container:: inherited

      .. automethod:: Markup.smaller

   .. container:: inherited

      .. automethod:: Markup.sub

   .. container:: inherited

      .. automethod:: Markup.super

   .. container:: inherited

      .. automethod:: Markup.tiny

   .. container:: inherited

      .. automethod:: Markup.translate

   .. container:: inherited

      .. automethod:: Markup.upright

   .. container:: inherited

      .. automethod:: Markup.vcenter

   .. container:: inherited

      .. automethod:: Markup.whiteout

   .. container:: inherited

      .. automethod:: Markup.with_color

   .. container:: inherited

      .. automethod:: Markup.with_dimensions

   .. container:: inherited

      .. automethod:: Markup.with_dimensions_from

   .. container:: inherited

      .. automethod:: Markup.with_literal

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Markup.abjad_metronome_mark

   .. container:: inherited

      .. automethod:: Markup.center_column

   .. container:: inherited

      .. automethod:: Markup.column

   .. container:: inherited

      .. automethod:: Markup.combine

   .. container:: inherited

      .. automethod:: Markup.concat

   .. container:: inherited

      .. automethod:: Markup.draw_circle

   .. container:: inherited

      .. automethod:: Markup.draw_line

   .. container:: inherited

      .. automethod:: Markup.filled_box

   .. container:: inherited

      .. automethod:: Markup.flat

   .. container:: inherited

      .. automethod:: Markup.fraction

   .. container:: inherited

      .. automethod:: Markup.hspace

   .. container:: inherited

      .. automethod:: Markup.left_column

   .. container:: inherited

      .. automethod:: Markup.line

   .. container:: inherited

      .. automethod:: Markup.make_improper_fraction_markup

   .. container:: inherited

      .. automethod:: Markup.musicglyph

   .. container:: inherited

      .. automethod:: Markup.natural

   .. container:: inherited

      .. automethod:: Markup.note_by_number

   .. container:: inherited

      .. automethod:: Markup.null

   .. container:: inherited

      .. automethod:: Markup.overlay

   .. container:: inherited

      .. automethod:: Markup.postscript

   .. container:: inherited

      .. automethod:: Markup.right_column

   .. container:: inherited

      .. automethod:: Markup.sharp

   .. container:: inherited

      .. automethod:: Markup.triangle

   .. container:: inherited

      .. automethod:: Markup.vspace

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: Markup.contents

   .. container:: inherited

      .. autoattribute:: Markup.direction

   .. container:: inherited

      .. autoattribute:: Markup.literal

   .. container:: inherited

      .. autoattribute:: Markup.tweaks

.. autoclass:: Ritardando

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __eq__
      __hash__
      __repr__
      __str__
      context
      hide
      markup
      parameter
      persistent
      tweaks

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Ritardando.__eq__

   .. automethod:: Ritardando.__hash__

   .. automethod:: Ritardando.__repr__

   .. automethod:: Ritardando.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Ritardando.context

   .. autoattribute:: Ritardando.hide

   .. autoattribute:: Ritardando.markup

   .. autoattribute:: Ritardando.parameter

   .. autoattribute:: Ritardando.persistent

   .. autoattribute:: Ritardando.tweaks

.. autoclass:: SpacingSection

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __eq__
      __hash__
      __repr__
      __str__
      duration
      from_string

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: SpacingSection.__eq__

   .. automethod:: SpacingSection.__hash__

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

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __eq__
      __format__
      __repr__
      context
      hide
      line_count
      persistent

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: StaffLines.__eq__

   .. automethod:: StaffLines.__format__

   .. automethod:: StaffLines.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: StaffLines.context

   .. autoattribute:: StaffLines.hide

   .. autoattribute:: StaffLines.line_count

   .. autoattribute:: StaffLines.persistent