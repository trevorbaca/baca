Bača API
========

.. toctree::
   :hidden:

   baca/index

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca <baca>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.leaf
   ~baca.leaves
   ~baca.lts
   ~baca.pleaves
   ~baca.plt
   ~baca.plts
   ~baca.ptail
   ~baca.ptails
   ~baca.rest
   ~baca.rests
   ~baca.run
   ~baca.skip
   ~baca.persistence.persistence

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.classes <baca--classes>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.classes.Counter
   ~baca.classes.Cursor
   ~baca.classes.PaddedTuple
   ~baca.classes.SchemeManifest
   ~baca.classes.Selection
   ~baca.classes.Sequence
   ~baca.classes.Tree

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.classes.select

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.commandclasses <baca--commandclasses>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.commandclasses.BCPCommand
   ~baca.commandclasses.ColorCommand
   ~baca.commandclasses.ContainerCommand
   ~baca.commandclasses.DetachCommand
   ~baca.commandclasses.GlissandoCommand
   ~baca.commandclasses.GlobalFermataCommand
   ~baca.commandclasses.IndicatorCommand
   ~baca.commandclasses.InstrumentChangeCommand
   ~baca.commandclasses.LabelCommand
   ~baca.commandclasses.MetronomeMarkCommand
   ~baca.commandclasses.PartAssignmentCommand

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.commands <baca--commands>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.commands.allow_octaves
   ~baca.commands.bcps
   ~baca.commands.close_volta
   ~baca.commands.color
   ~baca.commands.container
   ~baca.commands.cross_staff
   ~baca.commands.double_volta
   ~baca.commands.dynamic_down
   ~baca.commands.dynamic_up
   ~baca.commands.edition
   ~baca.commands.finger_pressure_transition
   ~baca.commands.flat_glissando
   ~baca.commands.fractions
   ~baca.commands.glissando
   ~baca.commands.global_fermata
   ~baca.commands.instrument
   ~baca.commands.invisible_music
   ~baca.commands.label
   ~baca.commands.markup
   ~baca.commands.metronome_mark
   ~baca.commands.one_voice
   ~baca.commands.open_volta
   ~baca.commands.parts
   ~baca.commands.previous_metadata
   ~baca.commands.untie
   ~baca.commands.voice_four
   ~baca.commands.voice_one
   ~baca.commands.voice_three
   ~baca.commands.voice_two

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.figuremaker <baca--figuremaker>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.figuremaker.Acciaccatura
   ~baca.figuremaker.Accumulator
   ~baca.figuremaker.Anchor
   ~baca.figuremaker.Assignment
   ~baca.figuremaker.Bind
   ~baca.figuremaker.Coat
   ~baca.figuremaker.Contribution
   ~baca.figuremaker.FigureMaker
   ~baca.figuremaker.Imbrication
   ~baca.figuremaker.LMR
   ~baca.figuremaker.Nest
   ~baca.figuremaker.RestAffix
   ~baca.figuremaker.Stack

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.figuremaker.anchor
   ~baca.figuremaker.anchor_after
   ~baca.figuremaker.anchor_to_figure
   ~baca.figuremaker.assign
   ~baca.figuremaker.bind
   ~baca.figuremaker.coat
   ~baca.figuremaker.extend_beam
   ~baca.figuremaker.figure
   ~baca.figuremaker.imbricate
   ~baca.figuremaker.lmr
   ~baca.figuremaker.nest
   ~baca.figuremaker.rests_after
   ~baca.figuremaker.rests_around
   ~baca.figuremaker.rests_before
   ~baca.figuremaker.resume
   ~baca.figuremaker.resume_after
   ~baca.figuremaker.skips_after
   ~baca.figuremaker.skips_around
   ~baca.figuremaker.skips_before
   ~baca.figuremaker.stack

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.indicatorcommands <baca--indicatorcommands>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.indicatorcommands.accent
   ~baca.indicatorcommands.alternate_bow_strokes
   ~baca.indicatorcommands.arpeggio
   ~baca.indicatorcommands.articulation
   ~baca.indicatorcommands.articulations
   ~baca.indicatorcommands.bar_line
   ~baca.indicatorcommands.breathe
   ~baca.indicatorcommands.clef
   ~baca.indicatorcommands.damp
   ~baca.indicatorcommands.double_flageolet
   ~baca.indicatorcommands.double_staccato
   ~baca.indicatorcommands.down_arpeggio
   ~baca.indicatorcommands.down_bow
   ~baca.indicatorcommands.espressivo
   ~baca.indicatorcommands.fermata
   ~baca.indicatorcommands.flageolet
   ~baca.indicatorcommands.hide_black_note_heads
   ~baca.indicatorcommands.laissez_vibrer
   ~baca.indicatorcommands.literal
   ~baca.indicatorcommands.long_fermata
   ~baca.indicatorcommands.marcato
   ~baca.indicatorcommands.margin_markup
   ~baca.indicatorcommands.mark
   ~baca.indicatorcommands.parenthesize
   ~baca.indicatorcommands.quadruple_staccato
   ~baca.indicatorcommands.rehearsal_mark
   ~baca.indicatorcommands.repeat_tie
   ~baca.indicatorcommands.short_fermata
   ~baca.indicatorcommands.snap_pizzicato
   ~baca.indicatorcommands.staccatissimo
   ~baca.indicatorcommands.staccato
   ~baca.indicatorcommands.staff_lines
   ~baca.indicatorcommands.start_markup
   ~baca.indicatorcommands.stem_tremolo
   ~baca.indicatorcommands.stop_on_string
   ~baca.indicatorcommands.stop_trill
   ~baca.indicatorcommands.stopped
   ~baca.indicatorcommands.tenuto
   ~baca.indicatorcommands.tie
   ~baca.indicatorcommands.triple_staccato
   ~baca.indicatorcommands.up_arpeggio
   ~baca.indicatorcommands.up_bow
   ~baca.indicatorcommands.very_long_fermata

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.indicators <baca--indicators>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.indicators.Accelerando
   ~baca.indicators.BarExtent
   ~baca.indicators.Ritardando
   ~baca.indicators.SpacingSection
   ~baca.indicators.StaffLines

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.mathx <baca--mathx>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.mathx.increase_elements
   ~baca.mathx.insert_and_transpose
   ~baca.mathx.negate_elements
   ~baca.mathx.overwrite_elements
   ~baca.mathx.partition_integer_into_halves
   ~baca.mathx.partition_nested_into_inward_pointing_parts
   ~baca.mathx.repeat_subruns_to_length

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.overrides <baca--overrides>`
   :class: section-header

Override library.

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.overrides.OverrideCommand

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.overrides.accidental_extra_offset
   ~baca.overrides.accidental_font_size
   ~baca.overrides.accidental_stencil_false
   ~baca.overrides.accidental_transparent
   ~baca.overrides.accidental_x_extent_false
   ~baca.overrides.accidental_x_offset
   ~baca.overrides.accidental_y_offset
   ~baca.overrides.bar_line_color
   ~baca.overrides.bar_line_extra_offset
   ~baca.overrides.bar_line_transparent
   ~baca.overrides.bar_line_x_extent
   ~baca.overrides.beam_positions
   ~baca.overrides.beam_stencil_false
   ~baca.overrides.beam_transparent
   ~baca.overrides.clef_extra_offset
   ~baca.overrides.clef_shift
   ~baca.overrides.clef_whiteout
   ~baca.overrides.clef_x_extent_false
   ~baca.overrides.dls_padding
   ~baca.overrides.dls_staff_padding
   ~baca.overrides.dls_up
   ~baca.overrides.dots_extra_offset
   ~baca.overrides.dots_stencil_false
   ~baca.overrides.dots_transparent
   ~baca.overrides.dots_x_extent_false
   ~baca.overrides.dynamic_text_color
   ~baca.overrides.dynamic_text_extra_offset
   ~baca.overrides.dynamic_text_parent_alignment_x
   ~baca.overrides.dynamic_text_self_alignment_x
   ~baca.overrides.dynamic_text_stencil_false
   ~baca.overrides.dynamic_text_transparent
   ~baca.overrides.dynamic_text_x_extent_zero
   ~baca.overrides.dynamic_text_x_offset
   ~baca.overrides.dynamic_text_y_offset
   ~baca.overrides.flag_extra_offset
   ~baca.overrides.flag_stencil_false
   ~baca.overrides.flag_transparent
   ~baca.overrides.glissando_thickness
   ~baca.overrides.hairpin_shorten_pair
   ~baca.overrides.hairpin_start_shift
   ~baca.overrides.hairpin_stencil_false
   ~baca.overrides.hairpin_to_barline
   ~baca.overrides.hairpin_transparent
   ~baca.overrides.laissez_vibrer_tie_down
   ~baca.overrides.laissez_vibrer_tie_up
   ~baca.overrides.mmrest_color
   ~baca.overrides.mmrest_text_color
   ~baca.overrides.mmrest_text_extra_offset
   ~baca.overrides.mmrest_text_padding
   ~baca.overrides.mmrest_text_parent_center
   ~baca.overrides.mmrest_text_staff_padding
   ~baca.overrides.mmrest_text_transparent
   ~baca.overrides.mmrest_transparent
   ~baca.overrides.no_ledgers
   ~baca.overrides.note_column_shift
   ~baca.overrides.note_head_color
   ~baca.overrides.note_head_duration_log
   ~baca.overrides.note_head_extra_offset
   ~baca.overrides.note_head_font_size
   ~baca.overrides.note_head_no_ledgers
   ~baca.overrides.note_head_stencil_false
   ~baca.overrides.note_head_style
   ~baca.overrides.note_head_style_cross
   ~baca.overrides.note_head_style_harmonic
   ~baca.overrides.note_head_style_harmonic_black
   ~baca.overrides.note_head_transparent
   ~baca.overrides.note_head_x_extent_zero
   ~baca.overrides.ottava_bracket_shorten_pair
   ~baca.overrides.ottava_bracket_staff_padding
   ~baca.overrides.rehearsal_mark_down
   ~baca.overrides.rehearsal_mark_extra_offset
   ~baca.overrides.rehearsal_mark_padding
   ~baca.overrides.rehearsal_mark_self_alignment_x
   ~baca.overrides.rehearsal_mark_y_offset
   ~baca.overrides.repeat_tie_down
   ~baca.overrides.repeat_tie_extra_offset
   ~baca.overrides.repeat_tie_stencil_false
   ~baca.overrides.repeat_tie_transparent
   ~baca.overrides.repeat_tie_up
   ~baca.overrides.rest_color
   ~baca.overrides.rest_down
   ~baca.overrides.rest_extra_offset
   ~baca.overrides.rest_position
   ~baca.overrides.rest_transparent
   ~baca.overrides.rest_up
   ~baca.overrides.rest_x_extent_zero
   ~baca.overrides.script_color
   ~baca.overrides.script_down
   ~baca.overrides.script_extra_offset
   ~baca.overrides.script_padding
   ~baca.overrides.script_staff_padding
   ~baca.overrides.script_up
   ~baca.overrides.script_x_extent_zero
   ~baca.overrides.slur_down
   ~baca.overrides.slur_up
   ~baca.overrides.span_bar_color
   ~baca.overrides.span_bar_extra_offset
   ~baca.overrides.span_bar_transparent
   ~baca.overrides.stem_color
   ~baca.overrides.stem_down
   ~baca.overrides.stem_extra_offset
   ~baca.overrides.stem_stencil_false
   ~baca.overrides.stem_transparent
   ~baca.overrides.stem_tremolo_extra_offset
   ~baca.overrides.stem_up
   ~baca.overrides.strict_note_spacing_off
   ~baca.overrides.sustain_pedal_staff_padding
   ~baca.overrides.text_script_color
   ~baca.overrides.text_script_down
   ~baca.overrides.text_script_extra_offset
   ~baca.overrides.text_script_font_size
   ~baca.overrides.text_script_padding
   ~baca.overrides.text_script_parent_alignment_x
   ~baca.overrides.text_script_self_alignment_x
   ~baca.overrides.text_script_staff_padding
   ~baca.overrides.text_script_up
   ~baca.overrides.text_script_x_offset
   ~baca.overrides.text_script_y_offset
   ~baca.overrides.text_spanner_left_padding
   ~baca.overrides.text_spanner_right_padding
   ~baca.overrides.text_spanner_staff_padding
   ~baca.overrides.text_spanner_stencil_false
   ~baca.overrides.text_spanner_transparent
   ~baca.overrides.text_spanner_y_offset
   ~baca.overrides.tie_down
   ~baca.overrides.tie_up
   ~baca.overrides.time_signature_extra_offset
   ~baca.overrides.time_signature_stencil_false
   ~baca.overrides.time_signature_transparent
   ~baca.overrides.trill_spanner_staff_padding
   ~baca.overrides.tuplet_bracket_down
   ~baca.overrides.tuplet_bracket_extra_offset
   ~baca.overrides.tuplet_bracket_outside_staff_priority
   ~baca.overrides.tuplet_bracket_padding
   ~baca.overrides.tuplet_bracket_shorten_pair
   ~baca.overrides.tuplet_bracket_staff_padding
   ~baca.overrides.tuplet_bracket_transparent
   ~baca.overrides.tuplet_bracket_up
   ~baca.overrides.tuplet_number_denominator
   ~baca.overrides.tuplet_number_extra_offset
   ~baca.overrides.tuplet_number_text
   ~baca.overrides.tuplet_number_transparent

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.path <baca--path>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.path.get_measure_profile_metadata

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.piecewise <baca--piecewise>`
   :class: section-header

Piecewise library.

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.piecewise.Bundle
   ~baca.piecewise.PiecewiseCommand

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.piecewise.bow_speed_spanner
   ~baca.piecewise.circle_bow_spanner
   ~baca.piecewise.clb_spanner
   ~baca.piecewise.covered_spanner
   ~baca.piecewise.damp_spanner
   ~baca.piecewise.dynamic
   ~baca.piecewise.hairpin
   ~baca.piecewise.half_clt_spanner
   ~baca.piecewise.make_dynamic
   ~baca.piecewise.material_annotation_spanner
   ~baca.piecewise.metric_modulation_spanner
   ~baca.piecewise.parse_hairpin_descriptor
   ~baca.piecewise.pitch_annotation_spanner
   ~baca.piecewise.pizzicato_spanner
   ~baca.piecewise.rhythm_annotation_spanner
   ~baca.piecewise.scp_spanner
   ~baca.piecewise.spazzolato_spanner
   ~baca.piecewise.string_number_spanner
   ~baca.piecewise.tasto_spanner
   ~baca.piecewise.text_spanner
   ~baca.piecewise.vibrato_spanner
   ~baca.piecewise.xfb_spanner

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.pitcharray <baca--pitcharray>`
   :class: section-header

Pitch array library.

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.pitcharray.PitchArray
   ~baca.pitcharray.PitchArrayCell
   ~baca.pitcharray.PitchArrayColumn
   ~baca.pitcharray.PitchArrayList
   ~baca.pitcharray.PitchArrayRow

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.pitchclasses <baca--pitchclasses>`
   :class: section-header

Pitch library.

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.pitchclasses.ArpeggiationSpacingSpecifier
   ~baca.pitchclasses.ChordalSpacingSpecifier
   ~baca.pitchclasses.CollectionList
   ~baca.pitchclasses.Constellation
   ~baca.pitchclasses.ConstellationCircuit
   ~baca.pitchclasses.DesignMaker
   ~baca.pitchclasses.HarmonicSeries
   ~baca.pitchclasses.Partial
   ~baca.pitchclasses.PitchClassSegment
   ~baca.pitchclasses.PitchClassSet
   ~baca.pitchclasses.PitchSegment
   ~baca.pitchclasses.PitchSet
   ~baca.pitchclasses.PitchTree
   ~baca.pitchclasses.Registration
   ~baca.pitchclasses.RegistrationComponent
   ~baca.pitchclasses.ZaggedPitchClassMaker

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.pitchcommands <baca--pitchcommands>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.pitchcommands.AccidentalAdjustmentCommand
   ~baca.pitchcommands.ClusterCommand
   ~baca.pitchcommands.ColorFingeringCommand
   ~baca.pitchcommands.DiatonicClusterCommand
   ~baca.pitchcommands.Loop
   ~baca.pitchcommands.MicrotoneDeviationCommand
   ~baca.pitchcommands.OctaveDisplacementCommand
   ~baca.pitchcommands.PitchCommand
   ~baca.pitchcommands.RegisterCommand
   ~baca.pitchcommands.RegisterInterpolationCommand
   ~baca.pitchcommands.RegisterToOctaveCommand
   ~baca.pitchcommands.StaffPositionCommand
   ~baca.pitchcommands.StaffPositionInterpolationCommand

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.pitchcommands.bass_to_octave
   ~baca.pitchcommands.center_to_octave
   ~baca.pitchcommands.clusters
   ~baca.pitchcommands.color_fingerings
   ~baca.pitchcommands.deviation
   ~baca.pitchcommands.diatonic_clusters
   ~baca.pitchcommands.displacement
   ~baca.pitchcommands.force_accidental
   ~baca.pitchcommands.interpolate_pitches
   ~baca.pitchcommands.interpolate_staff_positions
   ~baca.pitchcommands.levine_multiphonic
   ~baca.pitchcommands.loop
   ~baca.pitchcommands.natural_clusters
   ~baca.pitchcommands.pitch
   ~baca.pitchcommands.pitches
   ~baca.pitchcommands.register
   ~baca.pitchcommands.soprano_to_octave
   ~baca.pitchcommands.staff_position
   ~baca.pitchcommands.staff_positions

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.rhythmcommands <baca--rhythmcommands>`
   :class: section-header

Rhythm commands.

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.rhythmcommands.RhythmCommand

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.rhythmcommands.make_even_divisions
   ~baca.rhythmcommands.make_fused_tuplet_monads
   ~baca.rhythmcommands.make_monads
   ~baca.rhythmcommands.make_multimeasure_rests
   ~baca.rhythmcommands.make_notes
   ~baca.rhythmcommands.make_repeat_tied_notes
   ~baca.rhythmcommands.make_repeated_duration_notes
   ~baca.rhythmcommands.make_rests
   ~baca.rhythmcommands.make_single_attack
   ~baca.rhythmcommands.make_skips
   ~baca.rhythmcommands.make_tied_notes
   ~baca.rhythmcommands.make_tied_repeated_durations
   ~baca.rhythmcommands.music
   ~baca.rhythmcommands.rhythm
   ~baca.rhythmcommands.skeleton
   ~baca.rhythmcommands.tacet
   ~baca.rhythmcommands.tag_selection

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.scoping <baca--scoping>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.scoping.Command
   ~baca.scoping.Scope
   ~baca.scoping.Suite
   ~baca.scoping.TimelineScope

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.scoping.chunk
   ~baca.scoping.compare_persistent_indicators
   ~baca.scoping.new
   ~baca.scoping.not_mol
   ~baca.scoping.not_parts
   ~baca.scoping.not_score
   ~baca.scoping.not_segment
   ~baca.scoping.only_mol
   ~baca.scoping.only_parts
   ~baca.scoping.only_score
   ~baca.scoping.only_segment
   ~baca.scoping.site
   ~baca.scoping.suite
   ~baca.scoping.tag
   ~baca.scoping.timeline

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.segmentclasses <baca--segmentclasses>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.segmentclasses.BreakMeasureMap
   ~baca.segmentclasses.HorizontalSpacingSpecifier
   ~baca.segmentclasses.LBSD
   ~baca.segmentclasses.PageSpecifier
   ~baca.segmentclasses.SystemSpecifier
   ~baca.segmentclasses.TimeSignatureMaker

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.segmentclasses.breaks
   ~baca.segmentclasses.minimum_duration
   ~baca.segmentclasses.page
   ~baca.segmentclasses.scorewide_spacing
   ~baca.segmentclasses.system

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.segmentmaker <baca--segmentmaker>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.segmentmaker.SegmentMaker

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.selectors <baca--selectors>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.selectors.clparts
   ~baca.selectors.cmgroups
   ~baca.selectors.leaf_after_each_ptail
   ~baca.selectors.leaf_in_each_rleak_run
   ~baca.selectors.leaf_in_each_run
   ~baca.selectors.leaf_in_each_tuplet
   ~baca.selectors.leaves
   ~baca.selectors.leaves_in_each_lt
   ~baca.selectors.leaves_in_each_plt
   ~baca.selectors.leaves_in_each_run
   ~baca.selectors.leaves_in_each_tuplet
   ~baca.selectors.leaves_in_exclude_tuplets
   ~baca.selectors.leaves_in_get_tuplets
   ~baca.selectors.lleaf
   ~baca.selectors.lparts
   ~baca.selectors.lt
   ~baca.selectors.ltleaves
   ~baca.selectors.ltleaves_rleak
   ~baca.selectors.ltqruns
   ~baca.selectors.lts
   ~baca.selectors.mgroups
   ~baca.selectors.mmrest
   ~baca.selectors.note
   ~baca.selectors.notes
   ~baca.selectors.ntruns
   ~baca.selectors.omgroups
   ~baca.selectors.phead
   ~baca.selectors.pheads
   ~baca.selectors.pleaf
   ~baca.selectors.pleaf_in_each_tuplet
   ~baca.selectors.pleaves
   ~baca.selectors.plts
   ~baca.selectors.ptail_in_each_tuplet
   ~baca.selectors.qruns
   ~baca.selectors.rleaf
   ~baca.selectors.rleak_runs
   ~baca.selectors.rleaves
   ~baca.selectors.runs
   ~baca.selectors.tleaves
   ~baca.selectors.tuplet
   ~baca.selectors.tuplets

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.spannercommands <baca--spannercommands>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.spannercommands.SpannerIndicatorCommand

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.spannercommands.beam
   ~baca.spannercommands.ottava
   ~baca.spannercommands.ottava_bassa
   ~baca.spannercommands.slur
   ~baca.spannercommands.sustain_pedal
   ~baca.spannercommands.trill_spanner

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.templates <baca--templates>`
   :class: section-header

Score template library.

.. raw:: html

   <hr/>

.. rubric:: Score templates
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.templates.ScoreTemplate
   ~baca.templates.SingleStaffScoreTemplate
   ~baca.templates.StringTrioScoreTemplate
   ~baca.templates.ThreeVoiceStaffScoreTemplate
   ~baca.templates.TwoVoiceStaffScoreTemplate
   ~baca.templates.ViolinSoloScoreTemplate

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.tonality <baca--tonality>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.tonality.ChordExtent
   ~baca.tonality.ChordInversion
   ~baca.tonality.ChordQuality
   ~baca.tonality.ChordSuspension
   ~baca.tonality.RomanNumeral
   ~baca.tonality.RootedChordClass
   ~baca.tonality.RootlessChordClass
   ~baca.tonality.Scale
   ~baca.tonality.ScaleDegree

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.tonality.analyze_chords
   ~baca.tonality.analyze_incomplete_chords
   ~baca.tonality.analyze_incomplete_tonal_functions
   ~baca.tonality.analyze_neighbor_notes
   ~baca.tonality.analyze_passing_tones
   ~baca.tonality.analyze_tonal_functions
   ~baca.tonality.are_scalar_notes
   ~baca.tonality.are_stepwise_ascending_notes
   ~baca.tonality.are_stepwise_descending_notes
   ~baca.tonality.are_stepwise_notes