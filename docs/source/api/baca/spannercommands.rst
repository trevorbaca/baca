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
   ~SpannerIndicatorCommand

.. autoclass:: SpannerCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      detach_first
      left_broken
      right_broken
      selector
      spanner
      tweaks

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

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

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: SpannerCommand.deactivate

   .. autoattribute:: SpannerCommand.detach_first

   .. autoattribute:: SpannerCommand.left_broken

   .. container:: inherited

      .. autoattribute:: SpannerCommand.map

   .. container:: inherited

      .. autoattribute:: SpannerCommand.match

   .. container:: inherited

      .. autoattribute:: SpannerCommand.measures

   .. autoattribute:: SpannerCommand.right_broken

   .. container:: inherited

      .. autoattribute:: SpannerCommand.runtime

   .. container:: inherited

      .. autoattribute:: SpannerCommand.scope

   .. autoattribute:: SpannerCommand.selector

   .. autoattribute:: SpannerCommand.spanner

   .. container:: inherited

      .. autoattribute:: SpannerCommand.tag

   .. container:: inherited

      .. autoattribute:: SpannerCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: SpannerCommand.tags

   .. autoattribute:: SpannerCommand.tweaks

.. autoclass:: SpannerIndicatorCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      left_broken
      right_broken
      selector
      start_indicator
      stop_indicator
      tweaks

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: SpannerIndicatorCommand.__call__

   .. container:: inherited

      .. automethod:: SpannerIndicatorCommand.__format__

   .. container:: inherited

      .. automethod:: SpannerIndicatorCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: SpannerIndicatorCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: SpannerIndicatorCommand.deactivate

   .. autoattribute:: SpannerIndicatorCommand.left_broken

   .. container:: inherited

      .. autoattribute:: SpannerIndicatorCommand.map

   .. container:: inherited

      .. autoattribute:: SpannerIndicatorCommand.match

   .. container:: inherited

      .. autoattribute:: SpannerIndicatorCommand.measures

   .. autoattribute:: SpannerIndicatorCommand.right_broken

   .. container:: inherited

      .. autoattribute:: SpannerIndicatorCommand.runtime

   .. container:: inherited

      .. autoattribute:: SpannerIndicatorCommand.scope

   .. autoattribute:: SpannerIndicatorCommand.selector

   .. autoattribute:: SpannerIndicatorCommand.start_indicator

   .. autoattribute:: SpannerIndicatorCommand.stop_indicator

   .. container:: inherited

      .. autoattribute:: SpannerIndicatorCommand.tag

   .. container:: inherited

      .. autoattribute:: SpannerIndicatorCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: SpannerIndicatorCommand.tags

   .. autoattribute:: SpannerIndicatorCommand.tweaks

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