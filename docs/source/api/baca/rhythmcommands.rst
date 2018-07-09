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

   ~RhythmCommand
   ~TieCorrectionCommand

.. autoclass:: RhythmCommand

   .. autosummary::
      :nosignatures:

      division_expression
      division_maker
      left_broken
      multimeasure_rests
      parameter
      payload
      persist
      reference_meters
      repeat_ties
      rewrite_meter
      rewrite_rest_filled
      rhythm_maker
      right_broken
      split_at_measure_boundaries
      stages
      state

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

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

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: RhythmCommand.runtime

   .. container:: inherited

      .. autoattribute:: RhythmCommand.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: RhythmCommand.deactivate

   .. autoattribute:: RhythmCommand.division_expression

   .. autoattribute:: RhythmCommand.division_maker

   .. autoattribute:: RhythmCommand.left_broken

   .. container:: inherited

      .. autoattribute:: RhythmCommand.measures

   .. autoattribute:: RhythmCommand.multimeasure_rests

   .. autoattribute:: RhythmCommand.parameter

   .. autoattribute:: RhythmCommand.payload

   .. autoattribute:: RhythmCommand.persist

   .. autoattribute:: RhythmCommand.reference_meters

   .. autoattribute:: RhythmCommand.repeat_ties

   .. autoattribute:: RhythmCommand.rewrite_meter

   .. autoattribute:: RhythmCommand.rewrite_rest_filled

   .. autoattribute:: RhythmCommand.rhythm_maker

   .. autoattribute:: RhythmCommand.right_broken

   .. container:: inherited

      .. autoattribute:: RhythmCommand.selector

   .. autoattribute:: RhythmCommand.split_at_measure_boundaries

   .. autoattribute:: RhythmCommand.stages

   .. autoattribute:: RhythmCommand.state

   .. container:: inherited

      .. autoattribute:: RhythmCommand.tag

   .. container:: inherited

      .. autoattribute:: RhythmCommand.tags

.. autoclass:: TieCorrectionCommand

   .. autosummary::
      :nosignatures:

      direction
      repeat
      untie

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

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

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: TieCorrectionCommand.runtime

   .. container:: inherited

      .. autoattribute:: TieCorrectionCommand.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: TieCorrectionCommand.deactivate

   .. autoattribute:: TieCorrectionCommand.direction

   .. container:: inherited

      .. autoattribute:: TieCorrectionCommand.measures

   .. autoattribute:: TieCorrectionCommand.repeat

   .. container:: inherited

      .. autoattribute:: TieCorrectionCommand.selector

   .. container:: inherited

      .. autoattribute:: TieCorrectionCommand.tag

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
   ~flags
   ~make_even_divisions
   ~make_fused_tuplet_monads
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
   ~tie_from
   ~tie_to
   ~untie_to

.. autofunction:: beam_divisions

.. autofunction:: beam_everything

.. autofunction:: beam_runs

.. autofunction:: flags

.. autofunction:: make_even_divisions

.. autofunction:: make_fused_tuplet_monads

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

   .. autosummary::
      :nosignatures:

      tuplet_specifier

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

      .. automethod:: SkipRhythmMaker.__copy__

   .. container:: inherited

      .. automethod:: SkipRhythmMaker.__eq__

   .. automethod:: SkipRhythmMaker.__format__

   .. container:: inherited

      .. automethod:: SkipRhythmMaker.__hash__

   .. container:: inherited

      .. automethod:: SkipRhythmMaker.__illustrate__

   .. container:: inherited

      .. automethod:: SkipRhythmMaker.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: SkipRhythmMaker.beam_specifier

   .. container:: inherited

      .. autoattribute:: SkipRhythmMaker.division_masks

   .. container:: inherited

      .. autoattribute:: SkipRhythmMaker.duration_specifier

   .. container:: inherited

      .. autoattribute:: SkipRhythmMaker.logical_tie_masks

   .. container:: inherited

      .. autoattribute:: SkipRhythmMaker.previous_state

   .. container:: inherited

      .. autoattribute:: SkipRhythmMaker.state

   .. container:: inherited

      .. autoattribute:: SkipRhythmMaker.tie_specifier

   .. autoattribute:: SkipRhythmMaker.tuplet_specifier