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

   ~Bundle
   ~PiecewiseCommand

.. autoclass:: Bundle

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __iter__
      __len__
      __repr__
      bookended_spanner_start
      compound
      indicator
      indicator_only
      indicators
      simple
      spanner_start
      spanner_start_only
      spanner_stop

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Bundle.__iter__

   .. automethod:: Bundle.__len__

   .. automethod:: Bundle.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: Bundle.compound

   .. automethod:: Bundle.indicator_only

   .. automethod:: Bundle.simple

   .. automethod:: Bundle.spanner_start_only

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Bundle.bookended_spanner_start

   .. autoattribute:: Bundle.indicator

   .. autoattribute:: Bundle.indicators

   .. autoattribute:: Bundle.spanner_start

   .. autoattribute:: Bundle.spanner_stop

.. autoclass:: PiecewiseCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      autodetect_right_padding
      bookend
      bundles
      final_piece_spanner
      leak_spanner_stop
      pieces
      remove_length_1_spanner_start
      right_broken
      selector
      tweaks

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

   .. autoattribute:: PiecewiseCommand.autodetect_right_padding

   .. autoattribute:: PiecewiseCommand.bookend

   .. autoattribute:: PiecewiseCommand.bundles

   .. container:: inherited

      .. autoattribute:: PiecewiseCommand.deactivate

   .. autoattribute:: PiecewiseCommand.final_piece_spanner

   .. autoattribute:: PiecewiseCommand.leak_spanner_stop

   .. container:: inherited

      .. autoattribute:: PiecewiseCommand.map

   .. container:: inherited

      .. autoattribute:: PiecewiseCommand.match

   .. container:: inherited

      .. autoattribute:: PiecewiseCommand.measures

   .. autoattribute:: PiecewiseCommand.pieces

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

   .. autoattribute:: PiecewiseCommand.tweaks

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~bow_speed_spanner
   ~circle_bow_spanner
   ~clb_spanner
   ~covered_spanner
   ~damp_spanner
   ~dynamic
   ~hairpin
   ~half_clt_spanner
   ~make_dynamic
   ~material_annotation_spanner
   ~parse_hairpin_descriptor
   ~pitch_annotation_spanner
   ~rhythm_annotation_spanner
   ~scp_spanner
   ~spazzolato_spanner
   ~string_number_spanner
   ~tasto_spanner
   ~text_spanner
   ~vibrato_spanner
   ~xfb_spanner

.. autofunction:: bow_speed_spanner

.. autofunction:: circle_bow_spanner

.. autofunction:: clb_spanner

.. autofunction:: covered_spanner

.. autofunction:: damp_spanner

.. autofunction:: dynamic

.. autofunction:: hairpin

.. autofunction:: half_clt_spanner

.. autofunction:: make_dynamic

.. autofunction:: material_annotation_spanner

.. autofunction:: parse_hairpin_descriptor

.. autofunction:: pitch_annotation_spanner

.. autofunction:: rhythm_annotation_spanner

.. autofunction:: scp_spanner

.. autofunction:: spazzolato_spanner

.. autofunction:: string_number_spanner

.. autofunction:: tasto_spanner

.. autofunction:: text_spanner

.. autofunction:: vibrato_spanner

.. autofunction:: xfb_spanner