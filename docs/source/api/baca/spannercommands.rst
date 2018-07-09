.. _baca--spannercommands:

spannercommands
===============

.. automodule:: baca.spannercommands

.. currentmodule:: baca.spannercommands

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.spannercommands

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~SpannerCommand

.. autoclass:: SpannerCommand

   .. autosummary::
      :nosignatures:

      detach_first
      left_broken
      right_broken
      selector
      spanner
      tweaks

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: SpannerCommand.__call__

   .. container:: inherited

      .. automethod:: SpannerCommand.__format__

   .. container:: inherited

      .. automethod:: SpannerCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: SpannerCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: SpannerCommand.runtime

   .. container:: inherited

      .. autoattribute:: SpannerCommand.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: SpannerCommand.deactivate

   .. autoattribute:: SpannerCommand.detach_first

   .. autoattribute:: SpannerCommand.left_broken

   .. container:: inherited

      .. autoattribute:: SpannerCommand.measures

   .. autoattribute:: SpannerCommand.right_broken

   .. autoattribute:: SpannerCommand.selector

   .. autoattribute:: SpannerCommand.spanner

   .. container:: inherited

      .. autoattribute:: SpannerCommand.tag

   .. container:: inherited

      .. autoattribute:: SpannerCommand.tags

   .. autoattribute:: SpannerCommand.tweaks

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~beam
   ~finger_pressure_transition
   ~glissando
   ~ottava
   ~ottava_bassa
   ~repeat_tie
   ~repeat_tie_repeat_pitches
   ~slur
   ~sustain_pedal
   ~tie
   ~tie_repeat_pitches
   ~trill_spanner

.. autofunction:: beam

.. autofunction:: finger_pressure_transition

.. autofunction:: glissando

.. autofunction:: ottava

.. autofunction:: ottava_bassa

.. autofunction:: repeat_tie

.. autofunction:: repeat_tie_repeat_pitches

.. autofunction:: slur

.. autofunction:: sustain_pedal

.. autofunction:: tie

.. autofunction:: tie_repeat_pitches

.. autofunction:: trill_spanner