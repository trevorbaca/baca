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
   ~AnchorSpecifier
   ~Coat
   ~Imbrication
   ~LMRSpecifier
   ~MusicAccumulator
   ~MusicContribution
   ~MusicMaker
   ~Nesting
   ~PitchFirstAssignment
   ~PitchFirstCommand
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
      extend_beam
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

   .. autoattribute:: Imbrication.extend_beam

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

.. autoclass:: MusicAccumulator

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

   .. automethod:: MusicAccumulator.__call__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: MusicAccumulator.assemble

   .. automethod:: MusicAccumulator.populate_segment_maker

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: MusicAccumulator.score_template

   .. autoattribute:: MusicAccumulator.time_signatures

.. autoclass:: MusicContribution

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
      color_selector
      color_selector_result
      figure_name
      hide_time_signature
      print_color_selector_result
      time_signature
      voice_to_selection

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: MusicContribution.__getitem__

   .. automethod:: MusicContribution.__iter__

   .. automethod:: MusicContribution.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: MusicContribution.print_color_selector_result

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: MusicContribution.anchor

   .. autoattribute:: MusicContribution.color_selector

   .. autoattribute:: MusicContribution.color_selector_result

   .. autoattribute:: MusicContribution.figure_name

   .. autoattribute:: MusicContribution.hide_time_signature

   .. autoattribute:: MusicContribution.time_signature

   .. autoattribute:: MusicContribution.voice_to_selection

.. autoclass:: MusicMaker

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
      extend_beam
      figure_index
      figure_name
      signature
      tag

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: MusicMaker.__call__

   .. automethod:: MusicMaker.__eq__

   .. automethod:: MusicMaker.__format__

   .. automethod:: MusicMaker.__hash__

   .. automethod:: MusicMaker.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: MusicMaker.commands

   .. autoattribute:: MusicMaker.extend_beam

   .. autoattribute:: MusicMaker.figure_index

   .. autoattribute:: MusicMaker.figure_name

   .. autoattribute:: MusicMaker.signature

   .. autoattribute:: MusicMaker.tag

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
      commands
      tag

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

   .. autoattribute:: PitchFirstCommand.commands

   .. autoattribute:: PitchFirstCommand.tag

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
   ~imbricate
   ~lmr
   ~nest
   ~pitch_first
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

.. autofunction:: imbricate

.. autofunction:: lmr

.. autofunction:: nest

.. autofunction:: pitch_first

.. autofunction:: rests_after

.. autofunction:: rests_around

.. autofunction:: rests_before

.. autofunction:: resume

.. autofunction:: resume_after

.. autofunction:: skips_after

.. autofunction:: skips_around

.. autofunction:: skips_before