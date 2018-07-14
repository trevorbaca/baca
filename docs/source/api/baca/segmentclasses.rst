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
   ~StageMeasureMap
   ~SystemSpecifier
   ~TimeSignatureMaker

.. autoclass:: BreakMeasureMap

   .. autosummary::
      :nosignatures:

      bol_measure_numbers
      commands
      deactivate
      first_measure_number
      local_measure_numbers
      partial_score
      tag
      tags

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: BreakMeasureMap.__call__

   .. container:: inherited

      .. automethod:: BreakMeasureMap.__format__

   .. container:: inherited

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

   .. autoattribute:: BreakMeasureMap.partial_score

   .. autoattribute:: BreakMeasureMap.tag

   .. autoattribute:: BreakMeasureMap.tags

.. autoclass:: HorizontalSpacingSpecifier

   .. autosummary::
      :nosignatures:

      override

   .. autosummary::
      :nosignatures:

      bol_measure_numbers
      breaks
      eol_measure_numbers
      fermata_measure_duration
      fermata_measure_numbers
      first_measure_number
      last_measure_number
      magic_lilypond_eol_adjustment
      measure_count
      measures
      minimum_duration
      multiplier

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: HorizontalSpacingSpecifier.__call__

   .. container:: inherited

      .. automethod:: HorizontalSpacingSpecifier.__format__

   .. container:: inherited

      .. automethod:: HorizontalSpacingSpecifier.__repr__

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

   .. autoattribute:: HorizontalSpacingSpecifier.first_measure_number

   .. autoattribute:: HorizontalSpacingSpecifier.last_measure_number

   .. autoattribute:: HorizontalSpacingSpecifier.magic_lilypond_eol_adjustment

   .. autoattribute:: HorizontalSpacingSpecifier.measure_count

   .. autoattribute:: HorizontalSpacingSpecifier.measures

   .. autoattribute:: HorizontalSpacingSpecifier.minimum_duration

   .. autoattribute:: HorizontalSpacingSpecifier.multiplier

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

.. autoclass:: PageSpecifier

   .. autosummary::
      :nosignatures:

      number
      systems

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PageSpecifier.__format__

   .. container:: inherited

      .. automethod:: PageSpecifier.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: PageSpecifier.number

   .. autoattribute:: PageSpecifier.systems

.. autoclass:: StageMeasureMap

   .. autosummary::
      :nosignatures:

      item_type

   .. autosummary::
      :nosignatures:

      items

   .. autosummary::
      :nosignatures:

      __getitem__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: StageMeasureMap.__format__

   .. automethod:: StageMeasureMap.__getitem__

   .. container:: inherited

      .. automethod:: StageMeasureMap.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: StageMeasureMap.items

.. autoclass:: SystemSpecifier

   .. autosummary::
      :nosignatures:

      distances
      measure
      y_offset

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: SystemSpecifier.__format__

   .. container:: inherited

      .. automethod:: SystemSpecifier.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: SystemSpecifier.distances

   .. autoattribute:: SystemSpecifier.measure

   .. autoattribute:: SystemSpecifier.y_offset

.. autoclass:: TimeSignatureMaker

   .. autosummary::
      :nosignatures:

      run

   .. autosummary::
      :nosignatures:

      count
      fermata_measures
      rotation
      stage_measure_map
      time_signatures

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: TimeSignatureMaker.__call__

   .. container:: inherited

      .. automethod:: TimeSignatureMaker.__format__

   .. container:: inherited

      .. automethod:: TimeSignatureMaker.__repr__

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

   .. autoattribute:: TimeSignatureMaker.stage_measure_map

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