.. _baca--WellformednessManager:

WellformednessManager
=====================

.. automodule:: baca.WellformednessManager

.. currentmodule:: baca.WellformednessManager

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.WellformednessManager

.. autoclass:: WellformednessManager

   .. autosummary::
      :nosignatures:

      is_well_formed
      tabulate_wellformedness

   .. autosummary::
      :nosignatures:

      __call__

   .. autosummary::
      :nosignatures:

      check_repeat_pitch_classes

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: WellformednessManager.__call__

   .. container:: inherited

      .. automethod:: WellformednessManager.__format__

   .. container:: inherited

      .. automethod:: WellformednessManager.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: WellformednessManager.check_discontiguous_spanners

   .. container:: inherited

      .. automethod:: WellformednessManager.check_duplicate_ids

   .. container:: inherited

      .. automethod:: WellformednessManager.check_empty_containers

   .. container:: inherited

      .. automethod:: WellformednessManager.check_misdurated_measures

   .. container:: inherited

      .. automethod:: WellformednessManager.check_misfilled_measures

   .. container:: inherited

      .. automethod:: WellformednessManager.check_mismatched_enchained_hairpins

   .. container:: inherited

      .. automethod:: WellformednessManager.check_mispitched_ties

   .. container:: inherited

      .. automethod:: WellformednessManager.check_misrepresented_flags

   .. container:: inherited

      .. automethod:: WellformednessManager.check_missing_parents

   .. container:: inherited

      .. automethod:: WellformednessManager.check_nested_measures

   .. container:: inherited

      .. automethod:: WellformednessManager.check_notes_on_wrong_clef

   .. container:: inherited

      .. automethod:: WellformednessManager.check_out_of_range_notes

   .. container:: inherited

      .. automethod:: WellformednessManager.check_overlapping_beams

   .. container:: inherited

      .. automethod:: WellformednessManager.check_overlapping_glissandi

   .. container:: inherited

      .. automethod:: WellformednessManager.check_overlapping_hairpins

   .. container:: inherited

      .. automethod:: WellformednessManager.check_overlapping_octavation_spanners

   .. container:: inherited

      .. automethod:: WellformednessManager.check_overlapping_ties

   .. container:: inherited

      .. automethod:: WellformednessManager.check_overlapping_trill_spanners

   .. container:: inherited

      .. automethod:: WellformednessManager.check_tied_rests

   .. automethod:: WellformednessManager.is_well_formed

   .. automethod:: WellformednessManager.tabulate_wellformedness

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. automethod:: WellformednessManager.check_repeat_pitch_classes

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: WellformednessManager.allow_percussion_clef