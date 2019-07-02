.. _baca--rhythmcommands:

rhythmcommands
==============

.. automodule:: baca.rhythmcommands

.. currentmodule:: baca.rhythmcommands

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.rhythmcommands

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~DurationMultiplierCommand
   ~RhythmCommand
   ~TieCorrectionCommand

.. autoclass:: DurationMultiplierCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      written_duration

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: DurationMultiplierCommand.__call__

   .. container:: inherited

      .. automethod:: DurationMultiplierCommand.__format__

   .. container:: inherited

      .. automethod:: DurationMultiplierCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: DurationMultiplierCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: DurationMultiplierCommand.deactivate

   .. container:: inherited

      .. autoattribute:: DurationMultiplierCommand.map

   .. container:: inherited

      .. autoattribute:: DurationMultiplierCommand.match

   .. container:: inherited

      .. autoattribute:: DurationMultiplierCommand.measures

   .. container:: inherited

      .. autoattribute:: DurationMultiplierCommand.runtime

   .. container:: inherited

      .. autoattribute:: DurationMultiplierCommand.scope

   .. container:: inherited

      .. autoattribute:: DurationMultiplierCommand.selector

   .. container:: inherited

      .. autoattribute:: DurationMultiplierCommand.tag

   .. container:: inherited

      .. autoattribute:: DurationMultiplierCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: DurationMultiplierCommand.tags

   .. autoattribute:: DurationMultiplierCommand.written_duration

.. autoclass:: RhythmCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      annotate_unpitched_music
      divisions
      left_broken
      multimeasure_rests
      parameter
      payload
      persist
      reference_meters
      repeat_ties
      rewrite_meter
      rhythm_maker
      right_broken
      split_measures
      state

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: RhythmCommand.__call__

   .. container:: inherited

      .. automethod:: RhythmCommand.__format__

   .. container:: inherited

      .. automethod:: RhythmCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: RhythmCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: RhythmCommand.annotate_unpitched_music

   .. container:: inherited

      .. autoattribute:: RhythmCommand.deactivate

   .. autoattribute:: RhythmCommand.divisions

   .. autoattribute:: RhythmCommand.left_broken

   .. container:: inherited

      .. autoattribute:: RhythmCommand.map

   .. container:: inherited

      .. autoattribute:: RhythmCommand.match

   .. container:: inherited

      .. autoattribute:: RhythmCommand.measures

   .. autoattribute:: RhythmCommand.multimeasure_rests

   .. autoattribute:: RhythmCommand.parameter

   .. autoattribute:: RhythmCommand.payload

   .. autoattribute:: RhythmCommand.persist

   .. autoattribute:: RhythmCommand.reference_meters

   .. autoattribute:: RhythmCommand.repeat_ties

   .. autoattribute:: RhythmCommand.rewrite_meter

   .. autoattribute:: RhythmCommand.rhythm_maker

   .. autoattribute:: RhythmCommand.right_broken

   .. container:: inherited

      .. autoattribute:: RhythmCommand.runtime

   .. container:: inherited

      .. autoattribute:: RhythmCommand.scope

   .. container:: inherited

      .. autoattribute:: RhythmCommand.selector

   .. autoattribute:: RhythmCommand.split_measures

   .. autoattribute:: RhythmCommand.state

   .. container:: inherited

      .. autoattribute:: RhythmCommand.tag

   .. container:: inherited

      .. autoattribute:: RhythmCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: RhythmCommand.tags

.. autoclass:: TieCorrectionCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      allow_rest
      direction
      repeat
      untie

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: TieCorrectionCommand.__call__

   .. container:: inherited

      .. automethod:: TieCorrectionCommand.__format__

   .. container:: inherited

      .. automethod:: TieCorrectionCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: TieCorrectionCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: TieCorrectionCommand.allow_rest

   .. container:: inherited

      .. autoattribute:: TieCorrectionCommand.deactivate

   .. autoattribute:: TieCorrectionCommand.direction

   .. container:: inherited

      .. autoattribute:: TieCorrectionCommand.map

   .. container:: inherited

      .. autoattribute:: TieCorrectionCommand.match

   .. container:: inherited

      .. autoattribute:: TieCorrectionCommand.measures

   .. autoattribute:: TieCorrectionCommand.repeat

   .. container:: inherited

      .. autoattribute:: TieCorrectionCommand.runtime

   .. container:: inherited

      .. autoattribute:: TieCorrectionCommand.scope

   .. container:: inherited

      .. autoattribute:: TieCorrectionCommand.selector

   .. container:: inherited

      .. autoattribute:: TieCorrectionCommand.tag

   .. container:: inherited

      .. autoattribute:: TieCorrectionCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: TieCorrectionCommand.tags

   .. autoattribute:: TieCorrectionCommand.untie

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~beam_divisions
   ~beam_everything
   ~beam_runs
   ~do_not_beam
   ~make_even_divisions
   ~make_fused_tuplet_monads
   ~make_monads
   ~make_multimeasure_rests
   ~make_notes
   ~make_repeat_tied_notes
   ~make_repeated_duration_notes
   ~make_rests
   ~make_rhythm
   ~make_single_attack
   ~make_skips
   ~make_tied_notes
   ~make_tied_repeated_durations
   ~repeat_tie_from
   ~repeat_tie_to
   ~rhythm
   ~set_duration_multiplier
   ~tacet
   ~tie_from
   ~tie_to
   ~untie_to

.. autofunction:: beam_divisions

.. autofunction:: beam_everything

.. autofunction:: beam_runs

.. autofunction:: do_not_beam

.. autofunction:: make_even_divisions

.. autofunction:: make_fused_tuplet_monads

.. autofunction:: make_monads

.. autofunction:: make_multimeasure_rests

.. autofunction:: make_notes

.. autofunction:: make_repeat_tied_notes

.. autofunction:: make_repeated_duration_notes

.. autofunction:: make_rests

.. autofunction:: make_rhythm

.. autofunction:: make_single_attack

.. autofunction:: make_skips

.. autofunction:: make_tied_notes

.. autofunction:: make_tied_repeated_durations

.. autofunction:: repeat_tie_from

.. autofunction:: repeat_tie_to

.. autofunction:: rhythm

.. autofunction:: set_duration_multiplier

.. autofunction:: tacet

.. autofunction:: tie_from

.. autofunction:: tie_to

.. autofunction:: untie_to

.. raw:: html

   <hr/>

.. rubric:: Rhythm-makers
   :class: section-header

.. autosummary::
   :nosignatures:

   ~SkipRhythmMaker

.. autoclass:: SkipRhythmMaker

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      __format__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: SkipRhythmMaker.__call__

   .. container:: inherited

      .. automethod:: SkipRhythmMaker.__eq__

   .. automethod:: SkipRhythmMaker.__format__

   .. container:: inherited

      .. automethod:: SkipRhythmMaker.__hash__

   .. container:: inherited

      .. automethod:: SkipRhythmMaker.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: SkipRhythmMaker.division_masks

   .. container:: inherited

      .. autoattribute:: SkipRhythmMaker.divisions

   .. container:: inherited

      .. autoattribute:: SkipRhythmMaker.duration_specifier

   .. container:: inherited

      .. autoattribute:: SkipRhythmMaker.previous_state

   .. container:: inherited

      .. autoattribute:: SkipRhythmMaker.specifiers

   .. container:: inherited

      .. autoattribute:: SkipRhythmMaker.state

   .. container:: inherited

      .. autoattribute:: SkipRhythmMaker.tag