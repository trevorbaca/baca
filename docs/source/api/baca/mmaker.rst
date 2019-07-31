.. _baca--mmaker:

mmaker
======

.. automodule:: baca.mmaker

.. currentmodule:: baca.mmaker

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.mmaker

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~AcciaccaturaSpecifier
   ~Accumulator
   ~AnchorSpecifier
   ~Coat
   ~Contribution
   ~Imbrication
   ~LMRSpecifier
   ~Nesting
   ~PitchFirstAssignment
   ~PitchFirstRhythmMaker
   ~RestAffixSpecifier
   ~Stack

.. autoclass:: AcciaccaturaSpecifier

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
      lmr_specifier

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: AcciaccaturaSpecifier.__call__

   .. automethod:: AcciaccaturaSpecifier.__eq__

   .. automethod:: AcciaccaturaSpecifier.__format__

   .. automethod:: AcciaccaturaSpecifier.__hash__

   .. automethod:: AcciaccaturaSpecifier.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: AcciaccaturaSpecifier.durations

   .. autoattribute:: AcciaccaturaSpecifier.lmr_specifier

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

.. autoclass:: AnchorSpecifier

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

   .. automethod:: AnchorSpecifier.__eq__

   .. automethod:: AnchorSpecifier.__format__

   .. automethod:: AnchorSpecifier.__hash__

   .. automethod:: AnchorSpecifier.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: AnchorSpecifier.figure_name

   .. autoattribute:: AnchorSpecifier.local_selector

   .. autoattribute:: AnchorSpecifier.remote_selector

   .. autoattribute:: AnchorSpecifier.remote_voice_name

   .. autoattribute:: AnchorSpecifier.use_remote_stop_offset

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
      hocket
      segment
      selector
      specifiers
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

   .. autoattribute:: Imbrication.hocket

   .. autoattribute:: Imbrication.segment

   .. autoattribute:: Imbrication.selector

   .. autoattribute:: Imbrication.specifiers

   .. autoattribute:: Imbrication.truncate_ties

   .. autoattribute:: Imbrication.voice_name

.. autoclass:: LMRSpecifier

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
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

   .. automethod:: LMRSpecifier.__call__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: LMRSpecifier.left_counts

   .. autoattribute:: LMRSpecifier.left_cyclic

   .. autoattribute:: LMRSpecifier.left_length

   .. autoattribute:: LMRSpecifier.left_reversed

   .. autoattribute:: LMRSpecifier.middle_counts

   .. autoattribute:: LMRSpecifier.middle_cyclic

   .. autoattribute:: LMRSpecifier.middle_reversed

   .. autoattribute:: LMRSpecifier.priority

   .. autoattribute:: LMRSpecifier.right_counts

   .. autoattribute:: LMRSpecifier.right_cyclic

   .. autoattribute:: LMRSpecifier.right_length

   .. autoattribute:: LMRSpecifier.right_reversed

.. autoclass:: Nesting

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      lmr_specifier
      time_treatments

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Nesting.__call__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Nesting.lmr_specifier

   .. autoattribute:: Nesting.time_treatments

.. autoclass:: PitchFirstAssignment

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
      rhythm_maker
      thread

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: PitchFirstAssignment.__call__

   .. automethod:: PitchFirstAssignment.__eq__

   .. automethod:: PitchFirstAssignment.__format__

   .. automethod:: PitchFirstAssignment.__hash__

   .. automethod:: PitchFirstAssignment.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: PitchFirstAssignment.pattern

   .. container:: inherited

      .. autoattribute:: PitchFirstAssignment.remember_state_across_gaps

   .. autoattribute:: PitchFirstAssignment.rhythm_maker

   .. autoattribute:: PitchFirstAssignment.thread

.. autoclass:: PitchFirstRhythmMaker

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
      time_treatments

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: PitchFirstRhythmMaker.__call__

   .. automethod:: PitchFirstRhythmMaker.__eq__

   .. automethod:: PitchFirstRhythmMaker.__format__

   .. automethod:: PitchFirstRhythmMaker.__hash__

   .. automethod:: PitchFirstRhythmMaker.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: PitchFirstRhythmMaker.acciaccatura

   .. autoattribute:: PitchFirstRhythmMaker.affix

   .. autoattribute:: PitchFirstRhythmMaker.signature

   .. autoattribute:: PitchFirstRhythmMaker.spelling

   .. autoattribute:: PitchFirstRhythmMaker.talea

   .. autoattribute:: PitchFirstRhythmMaker.time_treatments

.. autoclass:: RestAffixSpecifier

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

   .. automethod:: RestAffixSpecifier.__call__

   .. automethod:: RestAffixSpecifier.__eq__

   .. automethod:: RestAffixSpecifier.__format__

   .. automethod:: RestAffixSpecifier.__hash__

   .. automethod:: RestAffixSpecifier.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: RestAffixSpecifier.pattern

   .. autoattribute:: RestAffixSpecifier.prefix

   .. autoattribute:: RestAffixSpecifier.skips_instead_of_rests

   .. autoattribute:: RestAffixSpecifier.suffix

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
   ~pitch_first
   ~pitch_first_rmaker
   ~rests_after
   ~rests_around
   ~rests_before
   ~resume
   ~resume_after
   ~skips_after
   ~skips_around
   ~skips_before

.. autofunction:: anchor

.. autofunction:: anchor_after

.. autofunction:: anchor_to_figure

.. autofunction:: coat

.. autofunction:: extend_beam

.. autofunction:: imbricate

.. autofunction:: lmr

.. autofunction:: nest

.. autofunction:: pitch_first

.. autofunction:: pitch_first_rmaker

.. autofunction:: rests_after

.. autofunction:: rests_around

.. autofunction:: rests_before

.. autofunction:: resume

.. autofunction:: resume_after

.. autofunction:: skips_after

.. autofunction:: skips_around

.. autofunction:: skips_before