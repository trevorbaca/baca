.. _baca--SegmentMaker:

SegmentMaker
============

.. automodule:: baca.SegmentMaker

.. currentmodule:: baca.SegmentMaker

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.SegmentMaker

.. raw:: html

   <hr/>

.. rubric:: Managers
   :class: section-header

.. autosummary::
   :nosignatures:

   ~WellformednessManager

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

.. raw:: html

   <hr/>

.. rubric:: Segment-makers
   :class: section-header

.. autosummary::
   :nosignatures:

   ~SegmentMaker

.. autoclass:: SegmentMaker

   .. autosummary::
      :nosignatures:

      run

   .. autosummary::
      :nosignatures:

      allow_empty_selections
      breaks
      clock_time_override
      color_octaves
      color_out_of_range_pitches
      color_repeat_pitch_classes
      do_not_check_persistence
      do_not_include_layout_ly
      fermata_measure_staff_line_count
      final_bar_line
      final_markup
      final_markup_extra_offset
      first_measure_number
      first_segment
      ignore_out_of_range_pitches
      ignore_repeat_pitch_classes
      ignore_unpitched_notes
      ignore_unregistered_pitches
      instruments
      last_segment
      lilypond_file
      magnify_staves
      manifests
      margin_markups
      measure_count
      measures_per_stage
      metadata
      metronome_mark_measure_map
      metronome_marks
      midi
      nonfirst_segment_lilypond_include
      previous_metadata
      score_template
      skip_wellformedness_checks
      skips_instead_of_rests
      spacing
      stage_count
      test_container_identifiers
      time_signatures
      transpose_score
      validate_measure_count
      validate_stage_count
      voice_metadata
      wrappers

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: SegmentMaker.__call__

   .. container:: inherited

      .. automethod:: SegmentMaker.__eq__

   .. container:: inherited

      .. automethod:: SegmentMaker.__format__

   .. container:: inherited

      .. automethod:: SegmentMaker.__hash__

   .. container:: inherited

      .. automethod:: SegmentMaker.__illustrate__

   .. container:: inherited

      .. automethod:: SegmentMaker.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: SegmentMaker.run

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: SegmentMaker.allow_empty_selections

   .. autoattribute:: SegmentMaker.breaks

   .. autoattribute:: SegmentMaker.clock_time_override

   .. autoattribute:: SegmentMaker.color_octaves

   .. autoattribute:: SegmentMaker.color_out_of_range_pitches

   .. autoattribute:: SegmentMaker.color_repeat_pitch_classes

   .. autoattribute:: SegmentMaker.do_not_check_persistence

   .. autoattribute:: SegmentMaker.do_not_include_layout_ly

   .. container:: inherited

      .. autoattribute:: SegmentMaker.environment

   .. autoattribute:: SegmentMaker.fermata_measure_staff_line_count

   .. autoattribute:: SegmentMaker.final_bar_line

   .. autoattribute:: SegmentMaker.final_markup

   .. autoattribute:: SegmentMaker.final_markup_extra_offset

   .. autoattribute:: SegmentMaker.first_measure_number

   .. autoattribute:: SegmentMaker.first_segment

   .. autoattribute:: SegmentMaker.ignore_out_of_range_pitches

   .. autoattribute:: SegmentMaker.ignore_repeat_pitch_classes

   .. autoattribute:: SegmentMaker.ignore_unpitched_notes

   .. autoattribute:: SegmentMaker.ignore_unregistered_pitches

   .. autoattribute:: SegmentMaker.instruments

   .. autoattribute:: SegmentMaker.last_segment

   .. autoattribute:: SegmentMaker.lilypond_file

   .. autoattribute:: SegmentMaker.magnify_staves

   .. autoattribute:: SegmentMaker.manifests

   .. autoattribute:: SegmentMaker.margin_markups

   .. autoattribute:: SegmentMaker.measure_count

   .. autoattribute:: SegmentMaker.measures_per_stage

   .. autoattribute:: SegmentMaker.metadata

   .. autoattribute:: SegmentMaker.metronome_mark_measure_map

   .. autoattribute:: SegmentMaker.metronome_marks

   .. autoattribute:: SegmentMaker.midi

   .. autoattribute:: SegmentMaker.nonfirst_segment_lilypond_include

   .. autoattribute:: SegmentMaker.previous_metadata

   .. container:: inherited

      .. autoattribute:: SegmentMaker.score

   .. autoattribute:: SegmentMaker.score_template

   .. container:: inherited

      .. autoattribute:: SegmentMaker.segment_directory

   .. container:: inherited

      .. autoattribute:: SegmentMaker.segment_name

   .. autoattribute:: SegmentMaker.skip_wellformedness_checks

   .. autoattribute:: SegmentMaker.skips_instead_of_rests

   .. autoattribute:: SegmentMaker.spacing

   .. autoattribute:: SegmentMaker.stage_count

   .. autoattribute:: SegmentMaker.test_container_identifiers

   .. autoattribute:: SegmentMaker.time_signatures

   .. autoattribute:: SegmentMaker.transpose_score

   .. autoattribute:: SegmentMaker.validate_measure_count

   .. autoattribute:: SegmentMaker.validate_stage_count

   .. autoattribute:: SegmentMaker.voice_metadata

   .. autoattribute:: SegmentMaker.wrappers