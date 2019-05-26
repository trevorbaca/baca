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

   ~baca.chead
   ~baca.cheads
   ~baca.chord
   ~baca.chords
   ~baca.clparts
   ~baca.cmgroups
   ~baca.enchain
   ~baca.grace
   ~baca.graces
   ~baca.group
   ~baca.group_by_measure
   ~baca.hleaf
   ~baca.hleaves
   ~baca.leaf
   ~baca.leaves
   ~baca.lleaf
   ~baca.lleak
   ~baca.lleaves
   ~baca.logical_ties
   ~baca.lparts
   ~baca.lt
   ~baca.ltleaf
   ~baca.ltleaves
   ~baca.ltqrun
   ~baca.ltqruns
   ~baca.ltrun
   ~baca.ltruns
   ~baca.lts
   ~baca.mgroups
   ~baca.mleaves
   ~baca.mmrest
   ~baca.mmrests
   ~baca.note
   ~baca.notes
   ~baca.ntrun
   ~baca.ntruns
   ~baca.omgroups
   ~baca.ompltgroups
   ~baca.phead
   ~baca.pheads
   ~baca.pleaf
   ~baca.pleaves
   ~baca.plt
   ~baca.plts
   ~baca.ptail
   ~baca.ptails
   ~baca.ptlt
   ~baca.ptlts
   ~baca.qrun
   ~baca.qruns
   ~baca.rest
   ~baca.rests
   ~baca.rleaf
   ~baca.rleak
   ~baca.rleaves
   ~baca.rmleaves
   ~baca.rrun
   ~baca.rruns
   ~baca.run
   ~baca.runs
   ~baca.skip
   ~baca.skips
   ~baca.tleaf
   ~baca.tleaves
   ~baca.top
   ~baca.tuplet
   ~baca.tuplets
   ~baca.wleaf
   ~baca.wleaves

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
   ~baca.classes.Expression
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

   ~baca.classes._select
   ~baca.classes._sequence

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.commands <baca--commands>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.commands.BCPCommand
   ~baca.commands.ColorCommand
   ~baca.commands.ContainerCommand
   ~baca.commands.GlissandoCommand
   ~baca.commands.GlobalFermataCommand
   ~baca.commands.IndicatorCommand
   ~baca.commands.InstrumentChangeCommand
   ~baca.commands.LabelCommand
   ~baca.commands.MetronomeMarkCommand
   ~baca.commands.PartAssignmentCommand
   ~baca.commands.TieCommand
   ~baca.commands.VoltaCommand

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.commands.allow_octaves
   ~baca.commands.bar_extent_persistent
   ~baca.commands.bcps
   ~baca.commands.color
   ~baca.commands.container
   ~baca.commands.cross_staff
   ~baca.commands.dynamic_down
   ~baca.commands.dynamic_up
   ~baca.commands.edition
   ~baca.commands.finger_pressure_transition
   ~baca.commands.flat_glissando
   ~baca.commands.glissando
   ~baca.commands.global_fermata
   ~baca.commands.instrument
   ~baca.commands.invisible_music
   ~baca.commands.label
   ~baca.commands.markup
   ~baca.commands.metronome_mark
   ~baca.commands.one_voice
   ~baca.commands.parts
   ~baca.commands.previous_metadata
   ~baca.commands.repeat_tie
   ~baca.commands.repeat_tie_repeat_pitches
   ~baca.commands.tie
   ~baca.commands.tie_repeat_pitches
   ~baca.commands.voice_four
   ~baca.commands.voice_one
   ~baca.commands.voice_three
   ~baca.commands.voice_two
   ~baca.commands.volta

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.divisions <baca--divisions>`
   :class: section-header

Division library.

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.divisions.Division
   ~baca.divisions.DivisionSequence
   ~baca.divisions.DivisionSequenceExpression
   ~baca.divisions.FuseByCountsDivisionCallback
   ~baca.divisions.SplitByDurationsDivisionCallback
   ~baca.divisions.SplitByRoundedRatiosDivisionCallback

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.divisions.compound_quarter_divisions
   ~baca.divisions.fuse_compound_quarter_divisions
   ~baca.divisions.split_by_durations
   ~baca.divisions.split_by_rounded_ratios
   ~baca.divisions.strict_quarter_divisions

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
   ~baca.indicatorcommands.breathe
   ~baca.indicatorcommands.clef
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
   ~baca.indicatorcommands.short_fermata
   ~baca.indicatorcommands.staccatissimo
   ~baca.indicatorcommands.staccato
   ~baca.indicatorcommands.staff_lines
   ~baca.indicatorcommands.start_markup
   ~baca.indicatorcommands.stem_tremolo
   ~baca.indicatorcommands.stop_on_string
   ~baca.indicatorcommands.stop_trill
   ~baca.indicatorcommands.stopped
   ~baca.indicatorcommands.tenuto
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
   ~baca.indicators.Markup
   ~baca.indicators.Ritardando
   ~baca.indicators.SpacingSection
   ~baca.indicators.StaffLines

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.markups <baca--markups>`
   :class: section-header

indicators.Markup library.

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.markups.FB
   ~baca.markups.FB_flaut
   ~baca.markups.MP_XFB_flaut
   ~baca.markups.OB
   ~baca.markups.OB_full_bow_strokes
   ~baca.markups.OB_no_pitch
   ~baca.markups.OB_terminate_abruptly
   ~baca.markups.OB_terminate_each_note_abruptly
   ~baca.markups.PO
   ~baca.markups.PO_FB_flaut
   ~baca.markups.PO_NBS
   ~baca.markups.PO_XFB_flaut
   ~baca.markups.PO_plus_non_vib
   ~baca.markups.PO_plus_poco_vib
   ~baca.markups.PO_scratch
   ~baca.markups.PO_slow_bow
   ~baca.markups.P_XFB_flaut
   ~baca.markups.XFB
   ~baca.markups.XFB_flaut
   ~baca.markups.XFB_plus_pochiss_pont
   ~baca.markups.XFB_plus_tasto
   ~baca.markups.XFB_sempre
   ~baca.markups.XP
   ~baca.markups.XP_FB
   ~baca.markups.XP_FB_flaut
   ~baca.markups.XP_XFB
   ~baca.markups.XP_XFB_flaut
   ~baca.markups.XP_full_bow_strokes
   ~baca.markups.XT
   ~baca.markups.accent_changes_of_direction
   ~baca.markups.airtone
   ~baca.markups.allow_bowing_to_convey_accelerando
   ~baca.markups.arco
   ~baca.markups.arco_ordinario
   ~baca.markups.attackless
   ~baca.markups.bass_drum
   ~baca.markups.bow_on_tailpiece
   ~baca.markups.bow_on_wooden_mute
   ~baca.markups.bowed_crotales
   ~baca.markups.castanets
   ~baca.markups.cir
   ~baca.markups.circles
   ~baca.markups.clicks_per_second
   ~baca.markups.col_legno_battuto
   ~baca.markups.column
   ~baca.markups.crine
   ~baca.markups.crotales
   ~baca.markups.damp
   ~baca.markups.delicatiss
   ~baca.markups.delicatissimo
   ~baca.markups.directly_on_bridge_bow_diagonally
   ~baca.markups.directly_on_bridge_very_slow_bow
   ~baca.markups.divisi_1_plus_3
   ~baca.markups.divisi_2_plus_4
   ~baca.markups.estr_sul_pont
   ~baca.markups.ext_pont
   ~baca.markups.fast_whisked_ellipses
   ~baca.markups.final_markup
   ~baca.markups.flaut
   ~baca.markups.flaut_partial_2
   ~baca.markups.flaut_possibile
   ~baca.markups.fluttertongue
   ~baca.markups.fractional_OB
   ~baca.markups.fractional_scratch
   ~baca.markups.full_bow_strokes
   ~baca.markups.glissando_lentissimo
   ~baca.markups.golden_tone
   ~baca.markups.grid_possibile
   ~baca.markups.gridato_possibile
   ~baca.markups.hair
   ~baca.markups.half_clt
   ~baca.markups.instrument
   ~baca.markups.keynoise
   ~baca.markups.kn_rasg
   ~baca.markups.knuckle_rasg
   ~baca.markups.leggieriss
   ~baca.markups.leggierissimo
   ~baca.markups.leggierissimo_off_string_bowing_on_staccati
   ~baca.markups.lh_damp
   ~baca.markups.lh_damp_plus_half_clt
   ~baca.markups.lhd_plus_half_clt
   ~baca.markups.lines
   ~baca.markups.loure
   ~baca.markups.lv_possibile
   ~baca.markups.make_instrument_name_markup
   ~baca.markups.markup
   ~baca.markups.molto_flautando
   ~baca.markups.molto_flautando_e_pont
   ~baca.markups.molto_gridato
   ~baca.markups.molto_overpressure
   ~baca.markups.molto_pont_plus_vib_molto
   ~baca.markups.molto_scratch
   ~baca.markups.nail_rasg
   ~baca.markups.nail_rasgueado
   ~baca.markups.non_flaut
   ~baca.markups.non_flautando
   ~baca.markups.non_flutt
   ~baca.markups.non_spazz
   ~baca.markups.nut
   ~baca.markups.off_string_bowing_on_staccati
   ~baca.markups.one_click_every
   ~baca.markups.ord
   ~baca.markups.ord_poco_scratch
   ~baca.markups.ord_senza_scratch
   ~baca.markups.ordinario
   ~baca.markups.overblow
   ~baca.markups.pP_XFB_flaut
   ~baca.markups.pT_XFB_flaut
   ~baca.markups.pizz
   ~baca.markups.plus_statement
   ~baca.markups.po_meno_scratch
   ~baca.markups.pochiss_pont
   ~baca.markups.pochiss_scratch
   ~baca.markups.pochiss_vib
   ~baca.markups.poco_overpressure
   ~baca.markups.poco_pont_plus_non_vib
   ~baca.markups.poco_pont_plus_sub_non_vib
   ~baca.markups.poco_pont_plus_sub_vib_mod
   ~baca.markups.poco_pont_plus_vib_mod
   ~baca.markups.poco_rasp_partial_2
   ~baca.markups.poco_scratch
   ~baca.markups.pont
   ~baca.markups.pont_XFB
   ~baca.markups.pont_XFB_flaut
   ~baca.markups.ponticello
   ~baca.markups.pos_ord
   ~baca.markups.pos_ord_XFB
   ~baca.markups.pos_ord_XFB_flaut
   ~baca.markups.pos_ord_poco_scratch
   ~baca.markups.pos_ord_senza_vib
   ~baca.markups.pos_ord_vib_poco
   ~baca.markups.pres_de_la_table
   ~baca.markups.put_reed_back_in
   ~baca.markups.rasp
   ~baca.markups.rasp_partial_2
   ~baca.markups.ratchet
   ~baca.markups.remove_staple
   ~baca.markups.repeat_count
   ~baca.markups.scraped_slate
   ~baca.markups.scratch_moltiss
   ~baca.markups.senza_pedale
   ~baca.markups.senza_scratch
   ~baca.markups.senza_vib
   ~baca.markups.short_instrument
   ~baca.markups.snare_drum
   ~baca.markups.sparse_clicks
   ~baca.markups.spazz
   ~baca.markups.spazzolato
   ~baca.markups.spazzolato_1_2_clt
   ~baca.markups.sponges
   ~baca.markups.still
   ~baca.markups.string_number
   ~baca.markups.string_numbers
   ~baca.markups.subito_non_armonichi_e_non_gridato
   ~baca.markups.subito_ordinario
   ~baca.markups.suspended_cymbal
   ~baca.markups.tailpiece
   ~baca.markups.tam_tam
   ~baca.markups.tamb_tr
   ~baca.markups.tasto
   ~baca.markups.tasto_FB
   ~baca.markups.tasto_FB_flaut
   ~baca.markups.tasto_NBS
   ~baca.markups.tasto_XFB
   ~baca.markups.tasto_XFB_flaut
   ~baca.markups.tasto_fractional_scratch
   ~baca.markups.tasto_half_scratch
   ~baca.markups.tasto_moltiss
   ~baca.markups.tasto_plus_non_vib
   ~baca.markups.tasto_plus_pochiss_scratch
   ~baca.markups.tasto_plus_poco_scratch
   ~baca.markups.tasto_plus_poco_vib
   ~baca.markups.tasto_plus_scratch_moltiss
   ~baca.markups.tasto_poss
   ~baca.markups.tasto_senza_vib
   ~baca.markups.tasto_slow_bow
   ~baca.markups.terminate_abruptly
   ~baca.markups.terminate_each_note_abruptly
   ~baca.markups.trans
   ~baca.markups.trem_flaut_tast
   ~baca.markups.vib_moltiss
   ~baca.markups.vib_pochiss
   ~baca.markups.vib_poco
   ~baca.markups.vibraphone
   ~baca.markups.xylophone

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.mmaker <baca--mmaker>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.mmaker.AcciaccaturaSpecifier
   ~baca.mmaker.AnchorSpecifier
   ~baca.mmaker.Coat
   ~baca.mmaker.ImbricationCommand
   ~baca.mmaker.LMRSpecifier
   ~baca.mmaker.MusicAccumulator
   ~baca.mmaker.MusicContribution
   ~baca.mmaker.MusicMaker
   ~baca.mmaker.NestingCommand
   ~baca.mmaker.PitchFirstRhythmCommand
   ~baca.mmaker.PitchSpecifier
   ~baca.mmaker.RestAffixSpecifier

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.mmaker.anchor
   ~baca.mmaker.anchor_after
   ~baca.mmaker.anchor_to_figure
   ~baca.mmaker.coat
   ~baca.mmaker.imbricate
   ~baca.mmaker.nest
   ~baca.mmaker.rests_after
   ~baca.mmaker.rests_around
   ~baca.mmaker.rests_before
   ~baca.mmaker.resume
   ~baca.mmaker.resume_after
   ~baca.mmaker.skips_after
   ~baca.mmaker.skips_around
   ~baca.mmaker.skips_before

.. raw:: html

   <hr/>

.. rubric:: Rhythm-makers
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.mmaker.PitchFirstRhythmMaker

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
   ~baca.overrides.accidental_stencil_false
   ~baca.overrides.accidental_transparent
   ~baca.overrides.accidental_x_extent_false
   ~baca.overrides.bar_extent
   ~baca.overrides.bar_extent_zero
   ~baca.overrides.bar_line_color
   ~baca.overrides.bar_line_extra_offset
   ~baca.overrides.bar_line_transparent
   ~baca.overrides.bar_line_x_extent
   ~baca.overrides.beam_positions
   ~baca.overrides.beam_stencil_false
   ~baca.overrides.beam_transparent
   ~baca.overrides.clef_extra_offset
   ~baca.overrides.clef_shift
   ~baca.overrides.clef_x_extent_false
   ~baca.overrides.dls_padding
   ~baca.overrides.dls_staff_padding
   ~baca.overrides.dls_up
   ~baca.overrides.dots_extra_offset
   ~baca.overrides.dots_stencil_false
   ~baca.overrides.dots_transparent
   ~baca.overrides.dynamic_text_color
   ~baca.overrides.dynamic_text_extra_offset
   ~baca.overrides.dynamic_text_parent_alignment_x
   ~baca.overrides.dynamic_text_self_alignment_x
   ~baca.overrides.dynamic_text_stencil_false
   ~baca.overrides.dynamic_text_transparent
   ~baca.overrides.dynamic_text_x_extent_zero
   ~baca.overrides.dynamic_text_x_offset
   ~baca.overrides.dynamic_text_y_offset
   ~baca.overrides.flag_stencil_false
   ~baca.overrides.flag_transparent
   ~baca.overrides.glissando_thickness
   ~baca.overrides.hairpin_shorten_pair
   ~baca.overrides.hairpin_start_shift
   ~baca.overrides.hairpin_stencil_false
   ~baca.overrides.hairpin_to_barline
   ~baca.overrides.hairpin_transparent
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
   ~baca.overrides.rest_down
   ~baca.overrides.rest_extra_offset
   ~baca.overrides.rest_position
   ~baca.overrides.rest_transparent
   ~baca.overrides.rest_up
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
   ~baca.overrides.stem_stencil_false
   ~baca.overrides.stem_transparent
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
   ~baca.overrides.tuplet_number_transparent

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.persistence <baca--persistence>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.persistence.PersistentIndicatorTests

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
   ~baca.piecewise.damp_spanner
   ~baca.piecewise.dynamic
   ~baca.piecewise.hairpin
   ~baca.piecewise.half_clt_spanner
   ~baca.piecewise.make_dynamic
   ~baca.piecewise.material_annotation_spanner
   ~baca.piecewise.parse_hairpin_descriptor
   ~baca.piecewise.pitch_annotation_spanner
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
   ~baca.pitchcommands.interpolate_staff_positions
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

Rhythm library.

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.rhythmcommands.DurationMultiplierCommand
   ~baca.rhythmcommands.RhythmCommand
   ~baca.rhythmcommands.TieCorrectionCommand

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.rhythmcommands.beam_divisions
   ~baca.rhythmcommands.beam_everything
   ~baca.rhythmcommands.beam_runs
   ~baca.rhythmcommands.do_not_beam
   ~baca.rhythmcommands.make_even_divisions
   ~baca.rhythmcommands.make_fused_tuplet_monads
   ~baca.rhythmcommands.make_monads
   ~baca.rhythmcommands.make_multimeasure_rests
   ~baca.rhythmcommands.make_notes
   ~baca.rhythmcommands.make_repeat_tied_notes
   ~baca.rhythmcommands.make_repeated_duration_notes
   ~baca.rhythmcommands.make_rests
   ~baca.rhythmcommands.make_rhythm
   ~baca.rhythmcommands.make_single_attack
   ~baca.rhythmcommands.make_skips
   ~baca.rhythmcommands.make_tied_notes
   ~baca.rhythmcommands.make_tied_repeated_durations
   ~baca.rhythmcommands.repeat_tie_from
   ~baca.rhythmcommands.repeat_tie_to
   ~baca.rhythmcommands.rhythm
   ~baca.rhythmcommands.set_duration_multiplier
   ~baca.rhythmcommands.silence_first
   ~baca.rhythmcommands.silence_last
   ~baca.rhythmcommands.sustain_first
   ~baca.rhythmcommands.sustain_last
   ~baca.rhythmcommands.tacet
   ~baca.rhythmcommands.tie_from
   ~baca.rhythmcommands.tie_to
   ~baca.rhythmcommands.untie_to

.. raw:: html

   <hr/>

.. rubric:: Rhythm-makers
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.rhythmcommands.SkipRhythmMaker

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
   ~baca.scoping.not_parts
   ~baca.scoping.not_score
   ~baca.scoping.not_segment
   ~baca.scoping.only_parts
   ~baca.scoping.only_score
   ~baca.scoping.only_segment
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
   ~baca.templates.TwoVoiceStaffScoreTemplate
   ~baca.templates.ViolinSoloScoreTemplate