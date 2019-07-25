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
   ~ImbricationCommand
   ~LMRSpecifier
   ~MusicAccumulator
   ~MusicContribution
   ~MusicMaker
   ~NestingCommand
   ~PitchFirstAssignment
   ~PitchFirstCommand
   ~PitchFirstRhythmMaker
   ~PitchSpecifier
   ~RestAffixSpecifier

.. autoclass:: AcciaccaturaSpecifier

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      durations
      lmr_specifier
      pattern

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: AcciaccaturaSpecifier.__call__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: AcciaccaturaSpecifier.durations

   .. autoattribute:: AcciaccaturaSpecifier.lmr_specifier

   .. autoattribute:: AcciaccaturaSpecifier.pattern

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

.. autoclass:: ImbricationCommand

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

   .. automethod:: ImbricationCommand.__call__

   .. container:: inherited

      .. automethod:: ImbricationCommand.__format__

   .. container:: inherited

      .. automethod:: ImbricationCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: ImbricationCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: ImbricationCommand.allow_unused_pitches

   .. autoattribute:: ImbricationCommand.by_pitch_class

   .. container:: inherited

      .. autoattribute:: ImbricationCommand.deactivate

   .. autoattribute:: ImbricationCommand.extend_beam

   .. autoattribute:: ImbricationCommand.hocket

   .. container:: inherited

      .. autoattribute:: ImbricationCommand.map

   .. container:: inherited

      .. autoattribute:: ImbricationCommand.match

   .. container:: inherited

      .. autoattribute:: ImbricationCommand.measures

   .. container:: inherited

      .. autoattribute:: ImbricationCommand.runtime

   .. container:: inherited

      .. autoattribute:: ImbricationCommand.scope

   .. autoattribute:: ImbricationCommand.segment

   .. autoattribute:: ImbricationCommand.selector

   .. autoattribute:: ImbricationCommand.specifiers

   .. container:: inherited

      .. autoattribute:: ImbricationCommand.tag

   .. container:: inherited

      .. autoattribute:: ImbricationCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: ImbricationCommand.tags

   .. autoattribute:: ImbricationCommand.truncate_ties

   .. autoattribute:: ImbricationCommand.voice_name

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
      show
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

   .. rubric:: Class & static methods
      :class: class-header

   .. automethod:: MusicAccumulator.show

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
      selections
      time_signature

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

   .. autoattribute:: MusicContribution.selections

   .. autoattribute:: MusicContribution.time_signature

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
      allow_repeats
      color_unregistered_pitches
      counts
      denominator
      exhaustive
      extend_beam
      figure_index
      figure_name
      hide_time_signature
      imbrication_map
      ordered_commands
      show
      specifiers
      tag
      talea_denominator
      thread
      time_treatments
      tuplet_denominator
      tuplet_force_fraction

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

   .. rubric:: Class & static methods
      :class: class-header

   .. automethod:: MusicMaker.show

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: MusicMaker.allow_repeats

   .. autoattribute:: MusicMaker.color_unregistered_pitches

   .. autoattribute:: MusicMaker.counts

   .. autoattribute:: MusicMaker.denominator

   .. autoattribute:: MusicMaker.exhaustive

   .. autoattribute:: MusicMaker.extend_beam

   .. autoattribute:: MusicMaker.figure_index

   .. autoattribute:: MusicMaker.figure_name

   .. autoattribute:: MusicMaker.hide_time_signature

   .. autoattribute:: MusicMaker.imbrication_map

   .. autoattribute:: MusicMaker.ordered_commands

   .. autoattribute:: MusicMaker.specifiers

   .. autoattribute:: MusicMaker.tag

   .. autoattribute:: MusicMaker.talea_denominator

   .. autoattribute:: MusicMaker.thread

   .. autoattribute:: MusicMaker.time_treatments

   .. autoattribute:: MusicMaker.tuplet_denominator

   .. autoattribute:: MusicMaker.tuplet_force_fraction

.. autoclass:: NestingCommand

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

   .. automethod:: NestingCommand.__call__

   .. container:: inherited

      .. automethod:: NestingCommand.__format__

   .. container:: inherited

      .. automethod:: NestingCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: NestingCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: NestingCommand.deactivate

   .. autoattribute:: NestingCommand.lmr_specifier

   .. container:: inherited

      .. autoattribute:: NestingCommand.map

   .. container:: inherited

      .. autoattribute:: NestingCommand.match

   .. container:: inherited

      .. autoattribute:: NestingCommand.measures

   .. container:: inherited

      .. autoattribute:: NestingCommand.runtime

   .. container:: inherited

      .. autoattribute:: NestingCommand.scope

   .. container:: inherited

      .. autoattribute:: NestingCommand.selector

   .. container:: inherited

      .. autoattribute:: NestingCommand.tag

   .. container:: inherited

      .. autoattribute:: NestingCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: NestingCommand.tags

   .. autoattribute:: NestingCommand.time_treatments

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
      acciaccatura_specifiers
      show
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

   .. rubric:: Class & static methods
      :class: class-header

   .. automethod:: PitchFirstRhythmMaker.show

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: PitchFirstRhythmMaker.acciaccatura_specifiers

   .. autoattribute:: PitchFirstRhythmMaker.spelling

   .. autoattribute:: PitchFirstRhythmMaker.talea

   .. autoattribute:: PitchFirstRhythmMaker.time_treatments

.. autoclass:: PitchSpecifier

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      __repr__
      expressions
      remove_duplicate_pitch_classes
      remove_duplicates
      to_pitch_classes

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: PitchSpecifier.__call__

   .. automethod:: PitchSpecifier.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: PitchSpecifier.expressions

   .. autoattribute:: PitchSpecifier.remove_duplicate_pitch_classes

   .. autoattribute:: PitchSpecifier.remove_duplicates

   .. autoattribute:: PitchSpecifier.to_pitch_classes

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