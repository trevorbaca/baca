.. _baca--piecewise:

piecewise
=========

.. automodule:: baca.piecewise

.. currentmodule:: baca.piecewise

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.piecewise

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~IndicatorBundle
   ~PiecewiseIndicatorCommand

.. autoclass:: IndicatorBundle

   .. autosummary::
      :nosignatures:

      compound
      indicator_only
      simple
      spanner_start_only
      with_indicator
      with_spanner_start
      with_spanner_stop

   .. autosummary::
      :nosignatures:

      bookended_spanner_start
      enchained
      indicator
      indicators
      spanner_start
      spanner_stop

   .. autosummary::
      :nosignatures:

      __iter__
      __len__
      __repr__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: IndicatorBundle.__format__

   .. automethod:: IndicatorBundle.__iter__

   .. automethod:: IndicatorBundle.__len__

   .. automethod:: IndicatorBundle.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: IndicatorBundle.compound

   .. automethod:: IndicatorBundle.indicator_only

   .. automethod:: IndicatorBundle.simple

   .. automethod:: IndicatorBundle.spanner_start_only

   .. automethod:: IndicatorBundle.with_indicator

   .. automethod:: IndicatorBundle.with_spanner_start

   .. automethod:: IndicatorBundle.with_spanner_stop

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: IndicatorBundle.bookended_spanner_start

   .. autoattribute:: IndicatorBundle.enchained

   .. autoattribute:: IndicatorBundle.indicator

   .. autoattribute:: IndicatorBundle.indicators

   .. autoattribute:: IndicatorBundle.spanner_start

   .. autoattribute:: IndicatorBundle.spanner_stop

.. autoclass:: PiecewiseIndicatorCommand

   .. autosummary::
      :nosignatures:

      bookend
      bundles
      final_piece_spanner
      leak
      piece_selector
      remove_length_1_spanner_start
      right_broken
      selector

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PiecewiseIndicatorCommand.__call__

   .. container:: inherited

      .. automethod:: PiecewiseIndicatorCommand.__format__

   .. container:: inherited

      .. automethod:: PiecewiseIndicatorCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PiecewiseIndicatorCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: PiecewiseIndicatorCommand.map

   .. container:: inherited

      .. autoattribute:: PiecewiseIndicatorCommand.measures

   .. container:: inherited

      .. autoattribute:: PiecewiseIndicatorCommand.runtime

   .. container:: inherited

      .. autoattribute:: PiecewiseIndicatorCommand.scope

   .. container:: inherited

      .. autoattribute:: PiecewiseIndicatorCommand.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: PiecewiseIndicatorCommand.bookend

   .. autoattribute:: PiecewiseIndicatorCommand.bundles

   .. container:: inherited

      .. autoattribute:: PiecewiseIndicatorCommand.deactivate

   .. autoattribute:: PiecewiseIndicatorCommand.final_piece_spanner

   .. autoattribute:: PiecewiseIndicatorCommand.leak

   .. container:: inherited

      .. autoattribute:: PiecewiseIndicatorCommand.match

   .. autoattribute:: PiecewiseIndicatorCommand.piece_selector

   .. autoattribute:: PiecewiseIndicatorCommand.remove_length_1_spanner_start

   .. autoattribute:: PiecewiseIndicatorCommand.right_broken

   .. autoattribute:: PiecewiseIndicatorCommand.selector

   .. container:: inherited

      .. autoattribute:: PiecewiseIndicatorCommand.tag

   .. container:: inherited

      .. autoattribute:: PiecewiseIndicatorCommand.tags

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~dynamic
   ~hairpin
   ~make_dynamic
   ~parse_hairpin_descriptor
   ~text_spanner

.. autofunction:: dynamic

.. autofunction:: hairpin

.. autofunction:: make_dynamic

.. autofunction:: parse_hairpin_descriptor

.. autofunction:: text_spanner