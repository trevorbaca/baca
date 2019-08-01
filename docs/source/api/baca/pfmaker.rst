.. _baca--pfmaker:

pfmaker
=======

.. automodule:: baca.pfmaker

.. currentmodule:: baca.pfmaker

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.pfmaker

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~Acciaccatura
   ~Accumulator
   ~Anchor
   ~Coat
   ~Contribution
   ~Imbrication
   ~LMR
   ~Nest
   ~PitchFirstAssignment
   ~PitchFirstCommand
   ~PitchFirstMaker
   ~RestAffix
   ~Stack

.. autoclass:: Acciaccatura

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      __eq__
      __format__
      __hash__
      __repr__
      durations
      lmr

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Acciaccatura.__call__

   .. automethod:: Acciaccatura.__eq__

   .. automethod:: Acciaccatura.__format__

   .. automethod:: Acciaccatura.__hash__

   .. automethod:: Acciaccatura.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Acciaccatura.durations

   .. autoattribute:: Acciaccatura.lmr

.. autoclass:: Accumulator

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      assemble
      populate_segment_maker
      score_template
      time_signatures

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Accumulator.__call__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: Accumulator.assemble

   .. automethod:: Accumulator.populate_segment_maker

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Accumulator.score_template

   .. autoattribute:: Accumulator.time_signatures

.. autoclass:: Anchor

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __eq__
      __format__
      __hash__
      __repr__
      figure_name
      local_selector
      remote_selector
      remote_voice_name
      use_remote_stop_offset

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Anchor.__eq__

   .. automethod:: Anchor.__format__

   .. automethod:: Anchor.__hash__

   .. automethod:: Anchor.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Anchor.figure_name

   .. autoattribute:: Anchor.local_selector

   .. autoattribute:: Anchor.remote_selector

   .. autoattribute:: Anchor.remote_voice_name

   .. autoattribute:: Anchor.use_remote_stop_offset

.. autoclass:: Coat

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      argument

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Coat.argument

.. autoclass:: Contribution

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __getitem__
      __iter__
      __repr__
      anchor
      figure_name
      hide_time_signature
      time_signature
      voice_to_selection

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Contribution.__getitem__

   .. automethod:: Contribution.__iter__

   .. automethod:: Contribution.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Contribution.anchor

   .. autoattribute:: Contribution.figure_name

   .. autoattribute:: Contribution.hide_time_signature

   .. autoattribute:: Contribution.time_signature

   .. autoattribute:: Contribution.voice_to_selection

.. autoclass:: Imbrication

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      allow_unused_pitches
      by_pitch_class
      commands
      hocket
      segment
      selector
      truncate_ties
      voice_name

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Imbrication.__call__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Imbrication.allow_unused_pitches

   .. autoattribute:: Imbrication.by_pitch_class

   .. autoattribute:: Imbrication.commands

   .. autoattribute:: Imbrication.hocket

   .. autoattribute:: Imbrication.segment

   .. autoattribute:: Imbrication.selector

   .. autoattribute:: Imbrication.truncate_ties

   .. autoattribute:: Imbrication.voice_name

.. autoclass:: LMR

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      __eq__
      __format__
      __hash__
      __repr__
      left_counts
      left_cyclic
      left_length
      left_reversed
      middle_counts
      middle_cyclic
      middle_reversed
      priority
      right_counts
      right_cyclic
      right_length
      right_reversed

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: LMR.__call__

   .. automethod:: LMR.__eq__

   .. automethod:: LMR.__format__

   .. automethod:: LMR.__hash__

   .. automethod:: LMR.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: LMR.left_counts

   .. autoattribute:: LMR.left_cyclic

   .. autoattribute:: LMR.left_length

   .. autoattribute:: LMR.left_reversed

   .. autoattribute:: LMR.middle_counts

   .. autoattribute:: LMR.middle_cyclic

   .. autoattribute:: LMR.middle_reversed

   .. autoattribute:: LMR.priority

   .. autoattribute:: LMR.right_counts

   .. autoattribute:: LMR.right_cyclic

   .. autoattribute:: LMR.right_length

   .. autoattribute:: LMR.right_reversed

.. autoclass:: Nest

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      __eq__
      __format__
      __hash__
      __repr__
      lmr
      treatments

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Nest.__call__

   .. automethod:: Nest.__eq__

   .. automethod:: Nest.__format__

   .. automethod:: Nest.__hash__

   .. automethod:: Nest.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Nest.lmr

   .. autoattribute:: Nest.treatments

.. autoclass:: PitchFirstAssignment

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __eq__
      __format__
      __hash__
      __repr__
      pattern
      rhythm_maker
      thread

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: PitchFirstAssignment.__eq__

   .. automethod:: PitchFirstAssignment.__format__

   .. automethod:: PitchFirstAssignment.__hash__

   .. automethod:: PitchFirstAssignment.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: PitchFirstAssignment.pattern

   .. autoattribute:: PitchFirstAssignment.rhythm_maker

   .. autoattribute:: PitchFirstAssignment.thread

.. autoclass:: PitchFirstCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      __eq__
      __format__
      __hash__
      __repr__
      assignments

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: PitchFirstCommand.__call__

   .. automethod:: PitchFirstCommand.__eq__

   .. automethod:: PitchFirstCommand.__format__

   .. automethod:: PitchFirstCommand.__hash__

   .. automethod:: PitchFirstCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: PitchFirstCommand.assignments

.. autoclass:: PitchFirstMaker

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      __eq__
      __format__
      __hash__
      __repr__
      acciaccatura
      affix
      signature
      spelling
      talea
      treatments

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: PitchFirstMaker.__call__

   .. automethod:: PitchFirstMaker.__eq__

   .. automethod:: PitchFirstMaker.__format__

   .. automethod:: PitchFirstMaker.__hash__

   .. automethod:: PitchFirstMaker.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: PitchFirstMaker.acciaccatura

   .. autoattribute:: PitchFirstMaker.affix

   .. autoattribute:: PitchFirstMaker.signature

   .. autoattribute:: PitchFirstMaker.spelling

   .. autoattribute:: PitchFirstMaker.talea

   .. autoattribute:: PitchFirstMaker.treatments

.. autoclass:: RestAffix

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      __eq__
      __format__
      __hash__
      __repr__
      pattern
      prefix
      skips_instead_of_rests
      suffix

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: RestAffix.__call__

   .. automethod:: RestAffix.__eq__

   .. automethod:: RestAffix.__format__

   .. automethod:: RestAffix.__hash__

   .. automethod:: RestAffix.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: RestAffix.pattern

   .. autoattribute:: RestAffix.prefix

   .. autoattribute:: RestAffix.skips_instead_of_rests

   .. autoattribute:: RestAffix.suffix

.. autoclass:: Stack

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      __eq__
      __format__
      __hash__
      __repr__
      commands

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Stack.__call__

   .. automethod:: Stack.__eq__

   .. automethod:: Stack.__format__

   .. automethod:: Stack.__hash__

   .. automethod:: Stack.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Stack.commands

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~anchor
   ~anchor_after
   ~anchor_to_figure
   ~coat
   ~extend_beam
   ~imbricate
   ~lmr
   ~nest
   ~pfassignment
   ~pfcommand
   ~pfmaker
   ~pitch_first_assignment
   ~pitch_first_assignment_command
   ~rests_after
   ~rests_around
   ~rests_before
   ~resume
   ~resume_after
   ~skips_after
   ~skips_around
   ~skips_before
   ~stack

.. autofunction:: anchor

.. autofunction:: anchor_after

.. autofunction:: anchor_to_figure

.. autofunction:: coat

.. autofunction:: extend_beam

.. autofunction:: imbricate

.. autofunction:: lmr

.. autofunction:: nest

.. autofunction:: pfassignment

.. autofunction:: pfcommand

.. autofunction:: pfmaker

.. autofunction:: pitch_first_assignment

.. autofunction:: pitch_first_assignment_command

.. autofunction:: rests_after

.. autofunction:: rests_around

.. autofunction:: rests_before

.. autofunction:: resume

.. autofunction:: resume_after

.. autofunction:: skips_after

.. autofunction:: skips_around

.. autofunction:: skips_before

.. autofunction:: stack