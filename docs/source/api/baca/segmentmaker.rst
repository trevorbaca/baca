.. _baca--segmentmaker:

segmentmaker
============

.. automodule:: baca.segmentmaker

.. currentmodule:: baca.segmentmaker

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.segmentmaker

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~SegmentMaker
   ~Wellformedness

.. autoclass:: SegmentMaker

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      allow_empty_selections
      breaks
      clock_time_override
      color_octaves
      color_out_of_range_pitches
      color_repeat_pitch_classes
      commands
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
      metadata
      metronome_marks
      midi
      nonfirst_segment_lilypond_include
      previous_metadata
      run
      score_template
      skip_wellformedness_checks
      skips_instead_of_rests
      spacing
      test_container_identifiers
      time_signatures
      transpose_score
      validate_measure_count
      voice_metadata

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

   .. autoattribute:: SegmentMaker.commands

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

   .. autoattribute:: SegmentMaker.metadata

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

   .. autoattribute:: SegmentMaker.test_container_identifiers

   .. autoattribute:: SegmentMaker.time_signatures

   .. autoattribute:: SegmentMaker.transpose_score

   .. autoattribute:: SegmentMaker.validate_measure_count

   .. autoattribute:: SegmentMaker.voice_metadata

.. autoclass:: Wellformedness

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      check_repeat_pitch_classes
      is_wellformed
      tabulate_wellformedness

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Wellformedness.__call__

   .. container:: inherited

      .. automethod:: Wellformedness.__format__

   .. container:: inherited

      .. automethod:: Wellformedness.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Wellformedness.check_discontiguous_spanners

   .. container:: inherited

      .. automethod:: Wellformedness.check_duplicate_ids

   .. container:: inherited

      .. automethod:: Wellformedness.check_empty_containers

   .. container:: inherited

      .. automethod:: Wellformedness.check_misdurated_measures

   .. container:: inherited

      .. automethod:: Wellformedness.check_misfilled_measures

   .. container:: inherited

      .. automethod:: Wellformedness.check_mispitched_ties

   .. container:: inherited

      .. automethod:: Wellformedness.check_misrepresented_flags

   .. container:: inherited

      .. automethod:: Wellformedness.check_missing_parents

   .. container:: inherited

      .. automethod:: Wellformedness.check_nested_measures

   .. container:: inherited

      .. automethod:: Wellformedness.check_notes_on_wrong_clef

   .. container:: inherited

      .. automethod:: Wellformedness.check_out_of_range_notes

   .. container:: inherited

      .. automethod:: Wellformedness.check_overlapping_beams

   .. container:: inherited

      .. automethod:: Wellformedness.check_overlapping_glissandi

   .. container:: inherited

      .. automethod:: Wellformedness.check_overlapping_octavation_spanners

   .. container:: inherited

      .. automethod:: Wellformedness.check_overlapping_trill_spanners

   .. container:: inherited

      .. automethod:: Wellformedness.check_unterminated_hairpins

   .. automethod:: Wellformedness.is_wellformed

   .. automethod:: Wellformedness.tabulate_wellformedness

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. automethod:: Wellformedness.check_repeat_pitch_classes

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: Wellformedness.allow_percussion_clef