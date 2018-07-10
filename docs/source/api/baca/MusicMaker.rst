.. _baca--musicmaker:

musicmaker
==========

.. automodule:: baca.musicmaker

.. currentmodule:: baca.musicmaker

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca.musicmaker

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

   .. autosummary::
      :nosignatures:

      durations
      lmr_specifier
      pattern

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: AcciaccaturaSpecifier.__call__

   .. container:: inherited

      .. automethod:: AcciaccaturaSpecifier.__format__

   .. container:: inherited

      .. automethod:: AcciaccaturaSpecifier.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: AcciaccaturaSpecifier.durations

   .. autoattribute:: AcciaccaturaSpecifier.lmr_specifier

   .. autoattribute:: AcciaccaturaSpecifier.pattern

.. autoclass:: AnchorSpecifier

   .. autosummary::
      :nosignatures:

      figure_name
      local_selector
      remote_selector
      remote_voice_name
      use_remote_stop_offset

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: AnchorSpecifier.__copy__

   .. container:: inherited

      .. automethod:: AnchorSpecifier.__eq__

   .. container:: inherited

      .. automethod:: AnchorSpecifier.__format__

   .. container:: inherited

      .. automethod:: AnchorSpecifier.__hash__

   .. container:: inherited

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

   .. autosummary::
      :nosignatures:

      argument

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Coat.__format__

   .. container:: inherited

      .. automethod:: Coat.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Coat.argument

.. autoclass:: ImbricationCommand

   .. autosummary::
      :nosignatures:

      allow_unused_pitches
      by_pitch_class
      extend_beam
      hocket
      segment
      selector
      specifiers
      truncate_ties
      voice_name

   .. autosummary::
      :nosignatures:

      __call__

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

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: ImbricationCommand.map

   .. container:: inherited

      .. autoattribute:: ImbricationCommand.runtime

   .. container:: inherited

      .. autoattribute:: ImbricationCommand.tag_measure_number

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

      .. autoattribute:: ImbricationCommand.measures

   .. autoattribute:: ImbricationCommand.segment

   .. autoattribute:: ImbricationCommand.selector

   .. autoattribute:: ImbricationCommand.specifiers

   .. container:: inherited

      .. autoattribute:: ImbricationCommand.tag

   .. container:: inherited

      .. autoattribute:: ImbricationCommand.tags

   .. autoattribute:: ImbricationCommand.truncate_ties

   .. autoattribute:: ImbricationCommand.voice_name

.. autoclass:: LMRSpecifier

   .. autosummary::
      :nosignatures:

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

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: LMRSpecifier.__call__

   .. container:: inherited

      .. automethod:: LMRSpecifier.__format__

   .. container:: inherited

      .. automethod:: LMRSpecifier.__repr__

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

   .. autosummary::
      :nosignatures:

      assemble
      populate_segment_maker

   .. autosummary::
      :nosignatures:

      music_maker
      score_template
      time_signatures

   .. autosummary::
      :nosignatures:

      __call__

   .. autosummary::
      :nosignatures:

      show

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: MusicAccumulator.__call__

   .. container:: inherited

      .. automethod:: MusicAccumulator.__format__

   .. container:: inherited

      .. automethod:: MusicAccumulator.__repr__

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

   .. autosummary::
      :nosignatures:

      print_color_selector_result

   .. autosummary::
      :nosignatures:

      anchor
      color_selector
      color_selector_result
      figure_name
      hide_time_signature
      selections
      state_manifest
      time_signature

   .. autosummary::
      :nosignatures:

      __getitem__
      __iter__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: MusicContribution.__copy__

   .. container:: inherited

      .. automethod:: MusicContribution.__eq__

   .. container:: inherited

      .. automethod:: MusicContribution.__format__

   .. automethod:: MusicContribution.__getitem__

   .. container:: inherited

      .. automethod:: MusicContribution.__hash__

   .. automethod:: MusicContribution.__iter__

   .. container:: inherited

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

   .. autosummary::
      :nosignatures:

      allow_repeats
      color_unregistered_pitches
      denominator
      specifiers
      thread
      voice_names

   .. autosummary::
      :nosignatures:

      __call__

   .. autosummary::
      :nosignatures:

      show

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: MusicMaker.__call__

   .. container:: inherited

      .. automethod:: MusicMaker.__format__

   .. container:: inherited

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

   .. autoattribute:: MusicMaker.denominator

   .. autoattribute:: MusicMaker.specifiers

   .. autoattribute:: MusicMaker.thread

   .. autoattribute:: MusicMaker.voice_names

.. autoclass:: NestingCommand

   .. autosummary::
      :nosignatures:

      lmr_specifier
      time_treatments

   .. autosummary::
      :nosignatures:

      __call__

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

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: NestingCommand.map

   .. container:: inherited

      .. autoattribute:: NestingCommand.runtime

   .. container:: inherited

      .. autoattribute:: NestingCommand.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: NestingCommand.deactivate

   .. autoattribute:: NestingCommand.lmr_specifier

   .. container:: inherited

      .. autoattribute:: NestingCommand.measures

   .. container:: inherited

      .. autoattribute:: NestingCommand.selector

   .. container:: inherited

      .. autoattribute:: NestingCommand.tag

   .. container:: inherited

      .. autoattribute:: NestingCommand.tags

   .. autoattribute:: NestingCommand.time_treatments

.. autoclass:: PitchFirstRhythmCommand

   .. autosummary::
      :nosignatures:

      pattern
      rhythm_maker

   .. autosummary::
      :nosignatures:

      __call__

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

   .. rubric:: Read/write properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmCommand.map

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmCommand.runtime

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmCommand.tag_measure_number

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmCommand.deactivate

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmCommand.measures

   .. autoattribute:: PitchFirstRhythmCommand.pattern

   .. autoattribute:: PitchFirstRhythmCommand.rhythm_maker

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmCommand.selector

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmCommand.tag

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmCommand.tags

.. autoclass:: PitchSpecifier

   .. autosummary::
      :nosignatures:

      expressions
      remove_duplicate_pitch_classes
      remove_duplicates
      to_pitch_classes

   .. autosummary::
      :nosignatures:

      __call__
      __repr__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: PitchSpecifier.__call__

   .. container:: inherited

      .. automethod:: PitchSpecifier.__format__

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

   .. autosummary::
      :nosignatures:

      pattern
      prefix
      skips_instead_of_rests
      suffix

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: RestAffixSpecifier.__call__

   .. container:: inherited

      .. automethod:: RestAffixSpecifier.__copy__

   .. container:: inherited

      .. automethod:: RestAffixSpecifier.__eq__

   .. container:: inherited

      .. automethod:: RestAffixSpecifier.__format__

   .. container:: inherited

      .. automethod:: RestAffixSpecifier.__hash__

   .. container:: inherited

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

   .. autosummary::
      :nosignatures:

      acciaccatura_specifiers
      beam_specifier
      division_masks
      duration_specifier
      logical_tie_masks
      talea
      tie_specifier
      time_treatments
      tuplet_specifier

   .. autosummary::
      :nosignatures:

      __call__

   .. autosummary::
      :nosignatures:

      show

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: PitchFirstRhythmMaker.__call__

   .. container:: inherited

      .. automethod:: PitchFirstRhythmMaker.__copy__

   .. container:: inherited

      .. automethod:: PitchFirstRhythmMaker.__eq__

   .. container:: inherited

      .. automethod:: PitchFirstRhythmMaker.__format__

   .. container:: inherited

      .. automethod:: PitchFirstRhythmMaker.__hash__

   .. container:: inherited

      .. automethod:: PitchFirstRhythmMaker.__illustrate__

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

   .. autoattribute:: PitchFirstRhythmMaker.beam_specifier

   .. autoattribute:: PitchFirstRhythmMaker.division_masks

   .. autoattribute:: PitchFirstRhythmMaker.duration_specifier

   .. autoattribute:: PitchFirstRhythmMaker.logical_tie_masks

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmMaker.previous_state

   .. container:: inherited

      .. autoattribute:: PitchFirstRhythmMaker.state

   .. autoattribute:: PitchFirstRhythmMaker.talea

   .. autoattribute:: PitchFirstRhythmMaker.tie_specifier

   .. autoattribute:: PitchFirstRhythmMaker.time_treatments

   .. autoattribute:: PitchFirstRhythmMaker.tuplet_specifier