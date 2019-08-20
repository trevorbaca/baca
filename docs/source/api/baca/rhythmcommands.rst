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

.. autoclass:: RhythmCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      annotate_unpitched_music
      do_not_check_total_duration
      parameter
      persist
      rhythm_maker
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

   .. autoattribute:: RhythmCommand.do_not_check_total_duration

   .. container:: inherited

      .. autoattribute:: RhythmCommand.map

   .. container:: inherited

      .. autoattribute:: RhythmCommand.match

   .. container:: inherited

      .. autoattribute:: RhythmCommand.measures

   .. autoattribute:: RhythmCommand.parameter

   .. autoattribute:: RhythmCommand.persist

   .. autoattribute:: RhythmCommand.rhythm_maker

   .. container:: inherited

      .. autoattribute:: RhythmCommand.runtime

   .. container:: inherited

      .. autoattribute:: RhythmCommand.scope

   .. container:: inherited

      .. autoattribute:: RhythmCommand.selector

   .. autoattribute:: RhythmCommand.state

   .. container:: inherited

      .. autoattribute:: RhythmCommand.tag

   .. container:: inherited

      .. autoattribute:: RhythmCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: RhythmCommand.tags

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~make_even_divisions
   ~make_fused_tuplet_monads
   ~make_monads
   ~make_multimeasure_rests
   ~make_notes
   ~make_repeat_tied_notes
   ~make_repeated_duration_notes
   ~make_rests
   ~make_single_attack
   ~make_skips
   ~make_tied_notes
   ~make_tied_repeated_durations
   ~music
   ~rhythm
   ~skeleton
   ~tacet
   ~tag_selection

.. autofunction:: make_even_divisions

.. autofunction:: make_fused_tuplet_monads

.. autofunction:: make_monads

.. autofunction:: make_multimeasure_rests

.. autofunction:: make_notes

.. autofunction:: make_repeat_tied_notes

.. autofunction:: make_repeated_duration_notes

.. autofunction:: make_rests

.. autofunction:: make_single_attack

.. autofunction:: make_skips

.. autofunction:: make_tied_notes

.. autofunction:: make_tied_repeated_durations

.. autofunction:: music

.. autofunction:: rhythm

.. autofunction:: skeleton

.. autofunction:: tacet

.. autofunction:: tag_selection