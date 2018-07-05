.. _baca--SegmentMaker:

SegmentMaker
============

.. automodule:: baca.SegmentMaker

.. currentmodule:: baca.SegmentMaker

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.SegmentMaker

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
      do_not_attach_metronome_mark_spanner
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
      metronome_mark_stem_height
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

   .. autoattribute:: SegmentMaker.do_not_attach_metronome_mark_spanner

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

   .. autoattribute:: SegmentMaker.metronome_mark_stem_height

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