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
   ~PiecewiseCommand

.. autoclass:: IndicatorBundle

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __iter__
      __len__
      bookended_spanner_start
      compound
      indicator
      indicator_only
      indicators
      simple
      spanner_start
      spanner_start_only
      spanner_stop
      with_indicator
      with_spanner_start
      with_spanner_stop

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: IndicatorBundle.__format__

   .. automethod:: IndicatorBundle.__iter__

   .. automethod:: IndicatorBundle.__len__

   .. container:: inherited

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

   .. autoattribute:: IndicatorBundle.indicator

   .. autoattribute:: IndicatorBundle.indicators

   .. autoattribute:: IndicatorBundle.spanner_start

   .. autoattribute:: IndicatorBundle.spanner_stop

.. autoclass:: PiecewiseCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

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

      .. automethod:: PiecewiseCommand.__call__

   .. container:: inherited

      .. automethod:: PiecewiseCommand.__format__

   .. container:: inherited

      .. automethod:: PiecewiseCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PiecewiseCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: PiecewiseCommand.bookend

   .. autoattribute:: PiecewiseCommand.bundles

   .. container:: inherited

      .. autoattribute:: PiecewiseCommand.deactivate

   .. autoattribute:: PiecewiseCommand.final_piece_spanner

   .. autoattribute:: PiecewiseCommand.leak

   .. container:: inherited

      .. autoattribute:: PiecewiseCommand.map

   .. container:: inherited

      .. autoattribute:: PiecewiseCommand.match

   .. container:: inherited

      .. autoattribute:: PiecewiseCommand.measures

   .. autoattribute:: PiecewiseCommand.piece_selector

   .. autoattribute:: PiecewiseCommand.remove_length_1_spanner_start

   .. autoattribute:: PiecewiseCommand.right_broken

   .. container:: inherited

      .. autoattribute:: PiecewiseCommand.runtime

   .. container:: inherited

      .. autoattribute:: PiecewiseCommand.scope

   .. autoattribute:: PiecewiseCommand.selector

   .. container:: inherited

      .. autoattribute:: PiecewiseCommand.tag

   .. container:: inherited

      .. autoattribute:: PiecewiseCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: PiecewiseCommand.tags

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