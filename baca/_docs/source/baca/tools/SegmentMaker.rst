.. currentmodule:: baca.tools.SegmentMaker

SegmentMaker
============

.. autoclass:: SegmentMaker

Bases
-----

- :py:class:`abjad.tools.segmenttools.SegmentMaker.SegmentMaker`

- :py:class:`abjad.tools.abctools.AbjadObject.AbjadObject`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~SegmentMaker.allow_empty_selections
      ~SegmentMaker.breaks
      ~SegmentMaker.clefs
      ~SegmentMaker.color_octaves
      ~SegmentMaker.color_out_of_range_pitches
      ~SegmentMaker.color_repeat_pitch_classes
      ~SegmentMaker.copy_rhythm
      ~SegmentMaker.do_not_check_persistence
      ~SegmentMaker.dynamics
      ~SegmentMaker.fermata_measure_staff_line_count
      ~SegmentMaker.final_bar_line
      ~SegmentMaker.final_markup
      ~SegmentMaker.final_markup_extra_offset
      ~SegmentMaker.first_measure_number
      ~SegmentMaker.first_segment
      ~SegmentMaker.ignore_repeat_pitch_classes
      ~SegmentMaker.ignore_unpitched_notes
      ~SegmentMaker.ignore_unregistered_pitches
      ~SegmentMaker.instruments
      ~SegmentMaker.last_segment
      ~SegmentMaker.manifests
      ~SegmentMaker.margin_markup
      ~SegmentMaker.measure_count
      ~SegmentMaker.measures_per_stage
      ~SegmentMaker.metadata
      ~SegmentMaker.metronome_mark_measure_map
      ~SegmentMaker.metronome_mark_stem_height
      ~SegmentMaker.metronome_marks
      ~SegmentMaker.midi
      ~SegmentMaker.previous_metadata
      ~SegmentMaker.print_timings
      ~SegmentMaker.range_checker
      ~SegmentMaker.rehearsal_letter
      ~SegmentMaker.run
      ~SegmentMaker.score
      ~SegmentMaker.score_template
      ~SegmentMaker.skip_wellformedness_checks
      ~SegmentMaker.skips_instead_of_rests
      ~SegmentMaker.spacing_specifier
      ~SegmentMaker.staff_lines
      ~SegmentMaker.stage_count
      ~SegmentMaker.stage_label_base_string
      ~SegmentMaker.time_signatures
      ~SegmentMaker.transpose_score
      ~SegmentMaker.validate_measure_count
      ~SegmentMaker.validate_measures_per_stage
      ~SegmentMaker.validate_stage_count
      ~SegmentMaker.wrappers
      ~SegmentMaker.__call__
      ~SegmentMaker.__eq__
      ~SegmentMaker.__format__
      ~SegmentMaker.__hash__
      ~SegmentMaker.__illustrate__
      ~SegmentMaker.__repr__

Read-only properties
--------------------

.. autoattribute:: SegmentMaker.allow_empty_selections

.. autoattribute:: SegmentMaker.breaks

.. autoattribute:: SegmentMaker.clefs

.. autoattribute:: SegmentMaker.color_octaves

.. autoattribute:: SegmentMaker.color_out_of_range_pitches

.. autoattribute:: SegmentMaker.color_repeat_pitch_classes

.. autoattribute:: SegmentMaker.do_not_check_persistence

.. autoattribute:: SegmentMaker.dynamics

.. autoattribute:: SegmentMaker.fermata_measure_staff_line_count

.. autoattribute:: SegmentMaker.final_bar_line

.. autoattribute:: SegmentMaker.final_markup

.. autoattribute:: SegmentMaker.final_markup_extra_offset

.. autoattribute:: SegmentMaker.first_measure_number

.. autoattribute:: SegmentMaker.first_segment

.. autoattribute:: SegmentMaker.ignore_repeat_pitch_classes

.. autoattribute:: SegmentMaker.ignore_unpitched_notes

.. autoattribute:: SegmentMaker.ignore_unregistered_pitches

.. autoattribute:: SegmentMaker.instruments

.. autoattribute:: SegmentMaker.last_segment

.. autoattribute:: SegmentMaker.manifests

.. autoattribute:: SegmentMaker.margin_markup

.. autoattribute:: SegmentMaker.measure_count

.. autoattribute:: SegmentMaker.measures_per_stage

.. autoattribute:: SegmentMaker.metadata

.. autoattribute:: SegmentMaker.metronome_mark_measure_map

.. autoattribute:: SegmentMaker.metronome_mark_stem_height

.. autoattribute:: SegmentMaker.metronome_marks

.. autoattribute:: SegmentMaker.midi

.. autoattribute:: SegmentMaker.previous_metadata

.. autoattribute:: SegmentMaker.print_timings

.. autoattribute:: SegmentMaker.range_checker

.. autoattribute:: SegmentMaker.rehearsal_letter

.. autoattribute:: SegmentMaker.score

.. autoattribute:: SegmentMaker.score_template

.. autoattribute:: SegmentMaker.skip_wellformedness_checks

.. autoattribute:: SegmentMaker.skips_instead_of_rests

.. autoattribute:: SegmentMaker.spacing_specifier

.. autoattribute:: SegmentMaker.staff_lines

.. autoattribute:: SegmentMaker.stage_count

.. autoattribute:: SegmentMaker.stage_label_base_string

.. autoattribute:: SegmentMaker.time_signatures

.. autoattribute:: SegmentMaker.transpose_score

.. autoattribute:: SegmentMaker.wrappers

Methods
-------

.. automethod:: SegmentMaker.copy_rhythm

.. automethod:: SegmentMaker.run

.. automethod:: SegmentMaker.validate_measure_count

.. automethod:: SegmentMaker.validate_measures_per_stage

.. automethod:: SegmentMaker.validate_stage_count

Special methods
---------------

.. automethod:: SegmentMaker.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: SegmentMaker.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: SegmentMaker.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: SegmentMaker.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: SegmentMaker.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: SegmentMaker.__repr__
