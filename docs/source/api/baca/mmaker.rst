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
   ~PitchFirstRhythmCommand
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
      music_maker
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

   .. autoattribute:: MusicAccumulator.music_maker

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
      state_manifest
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

   .. autoattribute:: MusicContribution.state_manifest

   .. autoattribute:: MusicContribution.time_signature

.. autoclass:: MusicMaker

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      allow_repeats
      color_unregistered_pitches
      denominator
      show
      specifiers
      thread
      voice_names

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: MusicMaker.__call__

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

   .. autoattribute:: MusicMaker.denominator

   .. autoattribute:: MusicMaker.specifiers

   .. autoattribute:: MusicMaker.thread

   .. autoattribute:: MusicMaker.voice_names

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

.. autoclass:: PitchFirstRhythmCommand

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      pattern
      rhythm_maker

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: PitchFirstRhythmCommand.__call__

   .. container:: inherited

      .. automethod:: PitchFirstRhythmCommand.__format__

   .. container:: inherited

      .. automethod:: PitchFirstRhythmCommand.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PitchFirstRhythmCommand.get_tag

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmCommand.deactivate

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmCommand.map

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmCommand.match

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmCommand.measures

   .. autoattribute:: PitchFirstRhythmCommand.pattern

   .. autoattribute:: PitchFirstRhythmCommand.rhythm_maker

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmCommand.runtime

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmCommand.scope

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmCommand.selector

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmCommand.tag

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmCommand.tag_measure_number

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmCommand.tags

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

.. autofunction:: rests_after

.. autofunction:: rests_around

.. autofunction:: rests_before

.. autofunction:: resume

.. autofunction:: resume_after

.. autofunction:: skips_after

.. autofunction:: skips_around

.. autofunction:: skips_before

.. raw:: html

   <hr/>

.. rubric:: Rhythm-makers
   :class: section-header

.. autosummary::
   :nosignatures:

   ~PitchFirstRhythmMaker

.. autoclass:: PitchFirstRhythmMaker

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      acciaccatura_specifiers
      division_masks
      duration_specifier
      show
      talea
      time_treatments

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: PitchFirstRhythmMaker.__call__

   .. container:: inherited

      .. automethod:: PitchFirstRhythmMaker.__eq__

   .. container:: inherited

      .. automethod:: PitchFirstRhythmMaker.__format__

   .. container:: inherited

      .. automethod:: PitchFirstRhythmMaker.__hash__

   .. container:: inherited

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

   .. autoattribute:: PitchFirstRhythmMaker.division_masks

   .. autoattribute:: PitchFirstRhythmMaker.duration_specifier

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmMaker.previous_state

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmMaker.specifiers

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmMaker.state

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmMaker.tag

   .. autoattribute:: PitchFirstRhythmMaker.talea

   .. autoattribute:: PitchFirstRhythmMaker.time_treatments