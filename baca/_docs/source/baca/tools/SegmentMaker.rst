.. currentmodule:: baca.tools

SegmentMaker
============

.. autoclass:: SegmentMaker

Bases
-----

- :py:class:`abjad.tools.segmenttools.SegmentMaker`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~baca.tools.SegmentMaker.SegmentMaker.allow_empty_selections
      ~baca.tools.SegmentMaker.SegmentMaker.allow_figure_names
      ~baca.tools.SegmentMaker.SegmentMaker.color_octaves
      ~baca.tools.SegmentMaker.SegmentMaker.color_out_of_range_pitches
      ~baca.tools.SegmentMaker.SegmentMaker.color_repeat_pitch_classes
      ~baca.tools.SegmentMaker.SegmentMaker.copy_rhythm
      ~baca.tools.SegmentMaker.SegmentMaker.design_checker
      ~baca.tools.SegmentMaker.SegmentMaker.final_bar_line
      ~baca.tools.SegmentMaker.SegmentMaker.final_markup
      ~baca.tools.SegmentMaker.SegmentMaker.final_markup_extra_offset
      ~baca.tools.SegmentMaker.SegmentMaker.hide_instrument_names
      ~baca.tools.SegmentMaker.SegmentMaker.ignore_repeat_pitch_classes
      ~baca.tools.SegmentMaker.SegmentMaker.ignore_unpitched_notes
      ~baca.tools.SegmentMaker.SegmentMaker.ignore_unregistered_pitches
      ~baca.tools.SegmentMaker.SegmentMaker.instruments
      ~baca.tools.SegmentMaker.SegmentMaker.label_clock_time
      ~baca.tools.SegmentMaker.SegmentMaker.label_stages
      ~baca.tools.SegmentMaker.SegmentMaker.layout_measure_map
      ~baca.tools.SegmentMaker.SegmentMaker.measure_count
      ~baca.tools.SegmentMaker.SegmentMaker.measures_per_stage
      ~baca.tools.SegmentMaker.SegmentMaker.metronome_mark_measure_map
      ~baca.tools.SegmentMaker.SegmentMaker.metronome_marks
      ~baca.tools.SegmentMaker.SegmentMaker.midi
      ~baca.tools.SegmentMaker.SegmentMaker.print_segment_duration
      ~baca.tools.SegmentMaker.SegmentMaker.print_timings
      ~baca.tools.SegmentMaker.SegmentMaker.range_checker
      ~baca.tools.SegmentMaker.SegmentMaker.rehearsal_letter
      ~baca.tools.SegmentMaker.SegmentMaker.run
      ~baca.tools.SegmentMaker.SegmentMaker.score_template
      ~baca.tools.SegmentMaker.SegmentMaker.skip_wellformedness_checks
      ~baca.tools.SegmentMaker.SegmentMaker.skips_instead_of_rests
      ~baca.tools.SegmentMaker.SegmentMaker.spacing_map
      ~baca.tools.SegmentMaker.SegmentMaker.spacing_specifier
      ~baca.tools.SegmentMaker.SegmentMaker.stage_count
      ~baca.tools.SegmentMaker.SegmentMaker.stage_label_base_string
      ~baca.tools.SegmentMaker.SegmentMaker.time_signatures
      ~baca.tools.SegmentMaker.SegmentMaker.transpose_score
      ~baca.tools.SegmentMaker.SegmentMaker.validate_measure_count
      ~baca.tools.SegmentMaker.SegmentMaker.validate_measures_per_stage
      ~baca.tools.SegmentMaker.SegmentMaker.validate_stage_count
      ~baca.tools.SegmentMaker.SegmentMaker.volta_measure_map
      ~baca.tools.SegmentMaker.SegmentMaker.wrappers
      ~baca.tools.SegmentMaker.SegmentMaker.__call__
      ~baca.tools.SegmentMaker.SegmentMaker.__eq__
      ~baca.tools.SegmentMaker.SegmentMaker.__format__
      ~baca.tools.SegmentMaker.SegmentMaker.__hash__
      ~baca.tools.SegmentMaker.SegmentMaker.__illustrate__
      ~baca.tools.SegmentMaker.SegmentMaker.__repr__

Read-only properties
--------------------

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.allow_empty_selections

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.allow_figure_names

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.color_octaves

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.color_out_of_range_pitches

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.color_repeat_pitch_classes

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.design_checker

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.final_bar_line

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.final_markup

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.final_markup_extra_offset

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.hide_instrument_names

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.ignore_repeat_pitch_classes

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.ignore_unpitched_notes

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.ignore_unregistered_pitches

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.instruments

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.label_clock_time

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.label_stages

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.layout_measure_map

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.measure_count

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.measures_per_stage

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.metronome_mark_measure_map

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.metronome_marks

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.midi

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.print_segment_duration

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.print_timings

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.range_checker

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.rehearsal_letter

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.score_template

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.skip_wellformedness_checks

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.skips_instead_of_rests

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.spacing_map

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.spacing_specifier

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.stage_count

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.stage_label_base_string

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.time_signatures

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.transpose_score

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.volta_measure_map

.. autoattribute:: baca.tools.SegmentMaker.SegmentMaker.wrappers

Methods
-------

.. automethod:: baca.tools.SegmentMaker.SegmentMaker.copy_rhythm

.. automethod:: baca.tools.SegmentMaker.SegmentMaker.run

.. automethod:: baca.tools.SegmentMaker.SegmentMaker.validate_measure_count

.. automethod:: baca.tools.SegmentMaker.SegmentMaker.validate_measures_per_stage

.. automethod:: baca.tools.SegmentMaker.SegmentMaker.validate_stage_count

Special methods
---------------

.. automethod:: baca.tools.SegmentMaker.SegmentMaker.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: baca.tools.SegmentMaker.SegmentMaker.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: baca.tools.SegmentMaker.SegmentMaker.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: baca.tools.SegmentMaker.SegmentMaker.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: baca.tools.SegmentMaker.SegmentMaker.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: baca.tools.SegmentMaker.SegmentMaker.__repr__
