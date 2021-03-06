.. _baca--segmentclasses:

segmentclasses
==============

.. automodule:: baca.segmentclasses

.. currentmodule:: baca.segmentclasses

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.segmentclasses

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~BreakMeasureMap
   ~HorizontalSpacingSpecifier
   ~LBSD
   ~PageSpecifier
   ~SystemSpecifier
   ~TimeSignatureMaker

.. autoclass:: BreakMeasureMap

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      __repr__
      bol_measure_numbers
      commands
      deactivate
      first_measure_number
      local_measure_numbers
      page_count
      partial_score
      tag
      tags

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: BreakMeasureMap.__call__

   .. automethod:: BreakMeasureMap.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: BreakMeasureMap.bol_measure_numbers

   .. autoattribute:: BreakMeasureMap.commands

   .. autoattribute:: BreakMeasureMap.deactivate

   .. autoattribute:: BreakMeasureMap.first_measure_number

   .. autoattribute:: BreakMeasureMap.local_measure_numbers

   .. autoattribute:: BreakMeasureMap.page_count

   .. autoattribute:: BreakMeasureMap.partial_score

   .. autoattribute:: BreakMeasureMap.tag

   .. autoattribute:: BreakMeasureMap.tags

.. autoclass:: HorizontalSpacingSpecifier

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      bol_measure_numbers
      breaks
      eol_measure_numbers
      fermata_measure_duration
      fermata_measure_numbers
      final_measure_number
      first_measure_number
      magic_lilypond_eol_adjustment
      measure_count
      measures
      minimum_duration
      multiplier
      override
      phantom

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: HorizontalSpacingSpecifier.__call__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: HorizontalSpacingSpecifier.override

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: HorizontalSpacingSpecifier.bol_measure_numbers

   .. autoattribute:: HorizontalSpacingSpecifier.breaks

   .. autoattribute:: HorizontalSpacingSpecifier.eol_measure_numbers

   .. autoattribute:: HorizontalSpacingSpecifier.fermata_measure_duration

   .. autoattribute:: HorizontalSpacingSpecifier.fermata_measure_numbers

   .. autoattribute:: HorizontalSpacingSpecifier.final_measure_number

   .. autoattribute:: HorizontalSpacingSpecifier.first_measure_number

   .. autoattribute:: HorizontalSpacingSpecifier.magic_lilypond_eol_adjustment

   .. autoattribute:: HorizontalSpacingSpecifier.measure_count

   .. autoattribute:: HorizontalSpacingSpecifier.measures

   .. autoattribute:: HorizontalSpacingSpecifier.minimum_duration

   .. autoattribute:: HorizontalSpacingSpecifier.multiplier

   .. autoattribute:: HorizontalSpacingSpecifier.phantom

.. autoclass:: LBSD

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      alignment_distances
      y_offset

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: LBSD.alignment_distances

   .. autoattribute:: LBSD.y_offset

.. autoclass:: PageSpecifier

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      number
      systems

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: PageSpecifier.number

   .. autoattribute:: PageSpecifier.systems

.. autoclass:: SystemSpecifier

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      distances
      measure
      y_offset

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: SystemSpecifier.distances

   .. autoattribute:: SystemSpecifier.measure

   .. autoattribute:: SystemSpecifier.y_offset

.. autoclass:: TimeSignatureMaker

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      count
      fermata_measures
      rotation
      run
      time_signatures

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: TimeSignatureMaker.run

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: TimeSignatureMaker.count

   .. autoattribute:: TimeSignatureMaker.fermata_measures

   .. autoattribute:: TimeSignatureMaker.rotation

   .. autoattribute:: TimeSignatureMaker.time_signatures

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~breaks
   ~minimum_duration
   ~page
   ~scorewide_spacing
   ~system

.. autofunction:: breaks

.. autofunction:: minimum_duration

.. autofunction:: page

.. autofunction:: scorewide_spacing

.. autofunction:: system