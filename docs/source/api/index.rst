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

.. rubric:: (2) Makers
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.MusicAccumulator.MusicAccumulator
   ~baca.MusicContribution.MusicContribution
   ~baca.MusicMaker.MusicMaker
   ~baca.PersistentIndicatorTests.PersistentIndicatorTests
   ~baca.SegmentMaker.SegmentMaker

.. raw:: html

   <hr/>

.. rubric:: (3) Specifiers
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.AnchorSpecifier.AnchorSpecifier
   ~baca.HorizontalSpacingSpecifier.HorizontalSpacingSpecifier
   ~baca.LMRSpecifier.LMRSpecifier
   ~baca.PitchSpecifier.PitchSpecifier
   ~baca.RestAffixSpecifier.RestAffixSpecifier

.. raw:: html

   <hr/>

.. rubric:: (4) Commands
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.AccidentalAdjustmentCommand.AccidentalAdjustmentCommand
   ~baca.BCPCommand.BCPCommand
   ~baca.ClusterCommand.ClusterCommand
   ~baca.ColorCommand.ColorCommand
   ~baca.ColorFingeringCommand.ColorFingeringCommand
   ~baca.CommandWrapper.CommandWrapper
   ~baca.ContainerCommand.ContainerCommand
   ~baca.DiatonicClusterCommand.DiatonicClusterCommand
   ~baca.GlobalFermataCommand.GlobalFermataCommand
   ~baca.ImbricationCommand.ImbricationCommand
   ~baca.IndicatorCommand.IndicatorCommand
   ~baca.InstrumentChangeCommand.InstrumentChangeCommand
   ~baca.LabelCommand.LabelCommand
   ~baca.MetronomeMarkCommand.MetronomeMarkCommand
   ~baca.MicrotoneDeviationCommand.MicrotoneDeviationCommand
   ~baca.NestingCommand.NestingCommand
   ~baca.OctaveDisplacementCommand.OctaveDisplacementCommand
   ~baca.PartAssignmentCommand.PartAssignmentCommand
   ~baca.PiecewiseIndicatorCommand.PiecewiseIndicatorCommand
   ~baca.PitchCommand.PitchCommand
   ~baca.RegisterCommand.RegisterCommand
   ~baca.RegisterInterpolationCommand.RegisterInterpolationCommand
   ~baca.RegisterToOctaveCommand.RegisterToOctaveCommand
   ~baca.SpannerCommand.SpannerCommand
   ~baca.StaffPositionCommand.StaffPositionCommand
   ~baca.StaffPositionInterpolationCommand.StaffPositionInterpolationCommand
   ~baca.TieCorrectionCommand.TieCorrectionCommand
   ~baca.VoltaCommand.VoltaCommand

.. raw:: html

   <hr/>

.. rubric:: (5) Utilities
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.BreakMeasureMap.BreakMeasureMap
   ~baca.Coat.Coat
   ~baca.Counter.Counter
   ~baca.Cursor.Cursor
   ~baca.DesignMaker.DesignMaker
   ~baca.Expression.Expression
   ~baca.ExpressionGallery.ExpressionGallery
   ~baca.HarmonicSeries.HarmonicSeries
   ~baca.IndicatorBundle.IndicatorBundle
   ~baca.Interpolator.Interpolator
   ~baca.LBSD.LBSD
   ~baca.Loop.Loop
   ~baca.MeasureWrapper.MeasureWrapper
   ~baca.MetronomeMarkMeasureMap.MetronomeMarkMeasureMap
   ~baca.PageSpecifier.PageSpecifier
   ~baca.Partial.Partial
   ~baca.Registration.Registration
   ~baca.RegistrationComponent.RegistrationComponent
   ~baca.SchemeManifest.SchemeManifest
   ~baca.Scope.Scope
   ~baca.Selection.Selection
   ~baca.Sequence.Sequence
   ~baca.SpacingIndication.SpacingIndication
   ~baca.SpacingSection.SpacingSection
   ~baca.StaffLines.StaffLines
   ~baca.StageMeasureMap.StageMeasureMap
   ~baca.SystemSpecifier.SystemSpecifier
   ~baca.TimeSignatureGroups.TimeSignatureGroups
   ~baca.TimeSignatureMaker.TimeSignatureMaker
   ~baca.TimelineScope.TimelineScope
   ~baca.Tree.Tree
   ~baca.WellformednessManager.WellformednessManager

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.Accelerando.Accelerando
   ~baca.PaddedTuple.PaddedTuple
   ~baca.Ritardando.Ritardando

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.are_contiguous_logical_voice
   ~baca.are_contiguous_same_parent
   ~baca.are_leaves
   ~baca.are_logical_voice
   ~baca.chead
   ~baca.cheads
   ~baca.chord
   ~baca.chords
   ~baca.components
   ~baca.count
   ~baca.enchain
   ~baca.filter
   ~baca.filter_duration
   ~baca.filter_length
   ~baca.filter_pitches
   ~baca.filter_preprolated
   ~baca.flatten
   ~baca.group
   ~baca.group_by
   ~baca.group_by_contiguity
   ~baca.group_by_duration
   ~baca.group_by_length
   ~baca.group_by_measure
   ~baca.group_by_measures
   ~baca.group_by_pitch
   ~baca.group_notes_by_measures
   ~baca.index
   ~baca.items
   ~baca.leaf
   ~baca.leaves
   ~baca.lleaf
   ~baca.lleak
   ~baca.lleaves
   ~baca.logical_ties
   ~baca.lt
   ~baca.ltqrun
   ~baca.ltqruns
   ~baca.ltrun
   ~baca.ltruns
   ~baca.lts
   ~baca.nontrivial
   ~baca.note
   ~baca.notes
   ~baca.ntrun
   ~baca.ntruns
   ~baca.partition_by_counts
   ~baca.partition_by_durations
   ~baca.partition_by_ratio
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
   ~baca.with_next_leaf
   ~baca.with_previous_leaf
   ~baca.wleaf
   ~baca.wleaves

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.Command <baca--Command>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: (4) Commands
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.Command.Command

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.Command.Map
   ~baca.Command.Suite

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.LibraryAF <baca--LibraryAF>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.LibraryAF.accent
   ~baca.LibraryAF.allow_octaves
   ~baca.LibraryAF.alternate_bow_strokes
   ~baca.LibraryAF.anchor
   ~baca.LibraryAF.anchor_after
   ~baca.LibraryAF.anchor_to_figure
   ~baca.LibraryAF.apply
   ~baca.LibraryAF.arpeggio
   ~baca.LibraryAF.articulation
   ~baca.LibraryAF.articulations
   ~baca.LibraryAF.bar_extent_persistent
   ~baca.LibraryAF.bass_to_octave
   ~baca.LibraryAF.bcps
   ~baca.LibraryAF.beam
   ~baca.LibraryAF.beam_divisions
   ~baca.LibraryAF.beam_everything
   ~baca.LibraryAF.beam_runs
   ~baca.LibraryAF.breaks
   ~baca.LibraryAF.breathe
   ~baca.LibraryAF.center_to_octave
   ~baca.LibraryAF.clef
   ~baca.LibraryAF.clusters
   ~baca.LibraryAF.coat
   ~baca.LibraryAF.color
   ~baca.LibraryAF.color_fingerings
   ~baca.LibraryAF.container
   ~baca.LibraryAF.cross_staff
   ~baca.LibraryAF.deviation
   ~baca.LibraryAF.diatonic_clusters
   ~baca.LibraryAF.displacement
   ~baca.LibraryAF.double_staccato
   ~baca.LibraryAF.down_arpeggio
   ~baca.LibraryAF.down_bow
   ~baca.LibraryAF.dynamic_down
   ~baca.LibraryAF.dynamic_up
   ~baca.LibraryAF.edition
   ~baca.LibraryAF.espressivo
   ~baca.LibraryAF.fermata
   ~baca.LibraryAF.finger_pressure_transition
   ~baca.LibraryAF.flageolet
   ~baca.LibraryAF.flags
   ~baca.LibraryAF.force_accidental

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.LibraryGM <baca--LibraryGM>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.LibraryGM.glissando
   ~baca.LibraryGM.global_fermata
   ~baca.LibraryGM.imbricate
   ~baca.LibraryGM.instrument
   ~baca.LibraryGM.interpolate_staff_positions
   ~baca.LibraryGM.label
   ~baca.LibraryGM.laissez_vibrer
   ~baca.LibraryGM.long_fermata
   ~baca.LibraryGM.loop
   ~baca.LibraryGM.marcato
   ~baca.LibraryGM.margin_markup
   ~baca.LibraryGM.metronome_mark
   ~baca.LibraryGM.minimum_duration
   ~baca.LibraryGM.mleaves

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.LibraryNS <baca--LibraryNS>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.LibraryNS.natural_clusters
   ~baca.LibraryNS.nest
   ~baca.LibraryNS.one_voice
   ~baca.LibraryNS.ottava
   ~baca.LibraryNS.ottava_bassa
   ~baca.LibraryNS.page
   ~baca.LibraryNS.parts
   ~baca.LibraryNS.pitch
   ~baca.LibraryNS.previous_metadata
   ~baca.LibraryNS.register
   ~baca.LibraryNS.rehearsal_mark
   ~baca.LibraryNS.repeat_tie
   ~baca.LibraryNS.repeat_tie_from
   ~baca.LibraryNS.repeat_tie_repeat_pitches
   ~baca.LibraryNS.repeat_tie_to
   ~baca.LibraryNS.rests_after
   ~baca.LibraryNS.rests_around
   ~baca.LibraryNS.rests_before
   ~baca.LibraryNS.resume
   ~baca.LibraryNS.resume_after
   ~baca.LibraryNS.rmleaves
   ~baca.LibraryNS.scorewide_spacing
   ~baca.LibraryNS.short_fermata
   ~baca.LibraryNS.skips_after
   ~baca.LibraryNS.skips_around
   ~baca.LibraryNS.skips_before
   ~baca.LibraryNS.slur
   ~baca.LibraryNS.soprano_to_octave
   ~baca.LibraryNS.staccatissimo
   ~baca.LibraryNS.staccato
   ~baca.LibraryNS.staff_lines
   ~baca.LibraryNS.staff_position
   ~baca.LibraryNS.staff_positions
   ~baca.LibraryNS.start_markup
   ~baca.LibraryNS.stem_tremolo
   ~baca.LibraryNS.stop_trill
   ~baca.LibraryNS.stopped
   ~baca.LibraryNS.sustain_pedal
   ~baca.LibraryNS.system

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.LibraryTZ <baca--LibraryTZ>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.LibraryTZ.tenuto
   ~baca.LibraryTZ.text_spanner
   ~baca.LibraryTZ.tie
   ~baca.LibraryTZ.tie_from
   ~baca.LibraryTZ.tie_repeat_pitches
   ~baca.LibraryTZ.tie_to
   ~baca.LibraryTZ.trill_spanner
   ~baca.LibraryTZ.untie_to
   ~baca.LibraryTZ.up_arpeggio
   ~baca.LibraryTZ.up_bow
   ~baca.LibraryTZ.very_long_fermata
   ~baca.LibraryTZ.voice_four
   ~baca.LibraryTZ.voice_one
   ~baca.LibraryTZ.voice_three
   ~baca.LibraryTZ.voice_two
   ~baca.LibraryTZ.volta

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.divisionlib <baca--divisionlib>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: (5) Utilities
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.divisionlib.Division

.. raw:: html

   <hr/>

.. rubric:: (6) Divisions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.divisionlib.DivisionMaker
   ~baca.divisionlib.DivisionSequence
   ~baca.divisionlib.DivisionSequenceExpression
   ~baca.divisionlib.FlattenDivisionCallback
   ~baca.divisionlib.FuseByCountsDivisionCallback
   ~baca.divisionlib.PartitionDivisionCallback
   ~baca.divisionlib.SplitByDurationsDivisionCallback
   ~baca.divisionlib.SplitByRoundedRatiosDivisionCallback

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.divisionlib.compound_quarter_divisions
   ~baca.divisionlib.fuse_compound_quarter_divisions
   ~baca.divisionlib.split_by_durations
   ~baca.divisionlib.strict_quarter_divisions

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.dynamiclib <baca--dynamiclib>`
   :class: section-header

Dynamics library.

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.dynamiclib.dynamic
   ~baca.dynamiclib.hairpin
   ~baca.dynamiclib.make_dynamic
   ~baca.dynamiclib.parse_hairpin_descriptor

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.library <baca--library>`
   :class: section-header

Function library.

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.library.apply_tweaks
   ~baca.library.lbsd
   ~baca.library.literal
   ~baca.library.map
   ~baca.library.markup
   ~baca.library.measures
   ~baca.library.not_parts
   ~baca.library.not_score
   ~baca.library.not_segment
   ~baca.library.only_parts
   ~baca.library.only_score
   ~baca.library.only_segment
   ~baca.library.pick
   ~baca.library.pitches
   ~baca.library.scope
   ~baca.library.suite
   ~baca.library.tag
   ~baca.library.timeline

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.markuplib <baca--markuplib>`
   :class: section-header

Markup library.

.. raw:: html

   <hr/>

.. rubric:: (5) Utilities
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.markuplib.Markup

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.markuplib.FB
   ~baca.markuplib.FB_flaut
   ~baca.markuplib.MP_XFB_flaut
   ~baca.markuplib.OB
   ~baca.markuplib.OB_full_bow_strokes
   ~baca.markuplib.OB_no_pitch
   ~baca.markuplib.OB_terminate_abruptly
   ~baca.markuplib.OB_terminate_each_note_abruptly
   ~baca.markuplib.PO
   ~baca.markuplib.PO_FB_flaut
   ~baca.markuplib.PO_NBS
   ~baca.markuplib.PO_XFB_flaut
   ~baca.markuplib.PO_plus_non_vib
   ~baca.markuplib.PO_plus_poco_vib
   ~baca.markuplib.PO_scratch
   ~baca.markuplib.PO_slow_bow
   ~baca.markuplib.P_XFB_flaut
   ~baca.markuplib.XFB
   ~baca.markuplib.XFB_flaut
   ~baca.markuplib.XFB_plus_pochiss_pont
   ~baca.markuplib.XFB_plus_tasto
   ~baca.markuplib.XFB_sempre
   ~baca.markuplib.XP
   ~baca.markuplib.XP_FB
   ~baca.markuplib.XP_FB_flaut
   ~baca.markuplib.XP_XFB
   ~baca.markuplib.XP_XFB_flaut
   ~baca.markuplib.XP_full_bow_strokes
   ~baca.markuplib.XT
   ~baca.markuplib.accent_changes_of_direction
   ~baca.markuplib.airtone
   ~baca.markuplib.allow_bowing_to_convey_accelerando
   ~baca.markuplib.arco
   ~baca.markuplib.arco_ordinario
   ~baca.markuplib.attackless
   ~baca.markuplib.bass_drum
   ~baca.markuplib.bow_on_tailpiece
   ~baca.markuplib.bow_on_wooden_mute
   ~baca.markuplib.bowed_crotales
   ~baca.markuplib.castanets
   ~baca.markuplib.cir
   ~baca.markuplib.circles
   ~baca.markuplib.clicks_per_second
   ~baca.markuplib.col_legno_battuto
   ~baca.markuplib.column
   ~baca.markuplib.crine
   ~baca.markuplib.crotales
   ~baca.markuplib.damp
   ~baca.markuplib.delicatiss
   ~baca.markuplib.delicatissimo
   ~baca.markuplib.directly_on_bridge_bow_diagonally
   ~baca.markuplib.directly_on_bridge_very_slow_bow
   ~baca.markuplib.divisi_1_plus_3
   ~baca.markuplib.divisi_2_plus_4
   ~baca.markuplib.estr_sul_pont
   ~baca.markuplib.ext_pont
   ~baca.markuplib.fast_whisked_ellipses
   ~baca.markuplib.final_markup
   ~baca.markuplib.flaut
   ~baca.markuplib.flaut_partial_2
   ~baca.markuplib.flaut_possibile
   ~baca.markuplib.fluttertongue
   ~baca.markuplib.fractional_OB
   ~baca.markuplib.fractional_scratch
   ~baca.markuplib.full_bow_strokes
   ~baca.markuplib.glissando_lentissimo
   ~baca.markuplib.golden_tone
   ~baca.markuplib.grid_possibile
   ~baca.markuplib.gridato_possibile
   ~baca.markuplib.hair
   ~baca.markuplib.half_clt
   ~baca.markuplib.instrument
   ~baca.markuplib.keynoise
   ~baca.markuplib.kn_rasg
   ~baca.markuplib.knuckle_rasg
   ~baca.markuplib.leggieriss
   ~baca.markuplib.leggierissimo
   ~baca.markuplib.leggierissimo_off_string_bowing_on_staccati
   ~baca.markuplib.lh_damp
   ~baca.markuplib.lh_damp_plus_half_clt
   ~baca.markuplib.lhd_plus_half_clt
   ~baca.markuplib.lines
   ~baca.markuplib.loure
   ~baca.markuplib.lv_possibile
   ~baca.markuplib.make_instrument_name_markup
   ~baca.markuplib.markup
   ~baca.markuplib.molto_flautando
   ~baca.markuplib.molto_flautando_e_pont
   ~baca.markuplib.molto_gridato
   ~baca.markuplib.molto_overpressure
   ~baca.markuplib.molto_pont_plus_vib_molto
   ~baca.markuplib.molto_scratch
   ~baca.markuplib.nail_rasg
   ~baca.markuplib.nail_rasgueado
   ~baca.markuplib.non_flaut
   ~baca.markuplib.non_flautando
   ~baca.markuplib.non_flutt
   ~baca.markuplib.non_spazz
   ~baca.markuplib.nut
   ~baca.markuplib.off_string_bowing_on_staccati
   ~baca.markuplib.one_click_every
   ~baca.markuplib.ord
   ~baca.markuplib.ord_poco_scratch
   ~baca.markuplib.ord_senza_scratch
   ~baca.markuplib.ordinario
   ~baca.markuplib.overblow
   ~baca.markuplib.pP_XFB_flaut
   ~baca.markuplib.pT_XFB_flaut
   ~baca.markuplib.pizz
   ~baca.markuplib.plus_statement
   ~baca.markuplib.po_meno_scratch
   ~baca.markuplib.pochiss_pont
   ~baca.markuplib.pochiss_scratch
   ~baca.markuplib.pochiss_vib
   ~baca.markuplib.poco_overpressure
   ~baca.markuplib.poco_pont_plus_non_vib
   ~baca.markuplib.poco_pont_plus_sub_non_vib
   ~baca.markuplib.poco_pont_plus_sub_vib_mod
   ~baca.markuplib.poco_pont_plus_vib_mod
   ~baca.markuplib.poco_rasp_partial_2
   ~baca.markuplib.poco_scratch
   ~baca.markuplib.pont
   ~baca.markuplib.pont_XFB
   ~baca.markuplib.pont_XFB_flaut
   ~baca.markuplib.ponticello
   ~baca.markuplib.pos_ord
   ~baca.markuplib.pos_ord_XFB
   ~baca.markuplib.pos_ord_XFB_flaut
   ~baca.markuplib.pos_ord_poco_scratch
   ~baca.markuplib.pos_ord_senza_vib
   ~baca.markuplib.pos_ord_vib_poco
   ~baca.markuplib.pres_de_la_table
   ~baca.markuplib.put_reed_back_in
   ~baca.markuplib.rasp
   ~baca.markuplib.rasp_partial_2
   ~baca.markuplib.ratchet
   ~baca.markuplib.remove_staple
   ~baca.markuplib.repeat_count
   ~baca.markuplib.scraped_slate
   ~baca.markuplib.scratch_moltiss
   ~baca.markuplib.senza_pedale
   ~baca.markuplib.senza_scratch
   ~baca.markuplib.senza_vib
   ~baca.markuplib.short_instrument
   ~baca.markuplib.snare_drum
   ~baca.markuplib.sparse_clicks
   ~baca.markuplib.spazz
   ~baca.markuplib.spazzolato
   ~baca.markuplib.spazzolato_1_2_clt
   ~baca.markuplib.sponges
   ~baca.markuplib.still
   ~baca.markuplib.string_number
   ~baca.markuplib.string_numbers
   ~baca.markuplib.subito_non_armonichi_e_non_gridato
   ~baca.markuplib.subito_ordinario
   ~baca.markuplib.suspended_cymbal
   ~baca.markuplib.tailpiece
   ~baca.markuplib.tam_tam
   ~baca.markuplib.tamb_tr
   ~baca.markuplib.tasto
   ~baca.markuplib.tasto_FB
   ~baca.markuplib.tasto_FB_flaut
   ~baca.markuplib.tasto_NBS
   ~baca.markuplib.tasto_XFB
   ~baca.markuplib.tasto_XFB_flaut
   ~baca.markuplib.tasto_fractional_scratch
   ~baca.markuplib.tasto_half_scratch
   ~baca.markuplib.tasto_moltiss
   ~baca.markuplib.tasto_plus_non_vib
   ~baca.markuplib.tasto_plus_pochiss_scratch
   ~baca.markuplib.tasto_plus_poco_scratch
   ~baca.markuplib.tasto_plus_poco_vib
   ~baca.markuplib.tasto_plus_scratch_moltiss
   ~baca.markuplib.tasto_poss
   ~baca.markuplib.tasto_senza_vib
   ~baca.markuplib.tasto_slow_bow
   ~baca.markuplib.terminate_abruptly
   ~baca.markuplib.terminate_each_note_abruptly
   ~baca.markuplib.trans
   ~baca.markuplib.trem_flaut_tast
   ~baca.markuplib.vib_moltiss
   ~baca.markuplib.vib_pochiss
   ~baca.markuplib.vib_poco
   ~baca.markuplib.vibraphone
   ~baca.markuplib.xylophone

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.overridelib <baca--overridelib>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: (4) Commands
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.overridelib.OverrideCommand

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.overridelib.accidental_stencil_false
   ~baca.overridelib.accidental_transparent
   ~baca.overridelib.accidental_x_extent_false
   ~baca.overridelib.bar_extent
   ~baca.overridelib.bar_extent_zero
   ~baca.overridelib.bar_line_transparent
   ~baca.overridelib.beam_positions
   ~baca.overridelib.beam_stencil_false
   ~baca.overridelib.beam_transparent
   ~baca.overridelib.clef_extra_offset
   ~baca.overridelib.clef_shift
   ~baca.overridelib.clef_x_extent_false
   ~baca.overridelib.dls_padding
   ~baca.overridelib.dls_staff_padding
   ~baca.overridelib.dls_up
   ~baca.overridelib.dots_stencil_false
   ~baca.overridelib.dots_transparent
   ~baca.overridelib.dynamic_shift
   ~baca.overridelib.dynamic_text_center
   ~baca.overridelib.dynamic_text_extra_offset
   ~baca.overridelib.dynamic_text_left
   ~baca.overridelib.dynamic_text_parent_alignment_x
   ~baca.overridelib.dynamic_text_right
   ~baca.overridelib.dynamic_text_stencil_false
   ~baca.overridelib.dynamic_text_transparent
   ~baca.overridelib.dynamic_text_x_extent_zero
   ~baca.overridelib.dynamic_text_x_offset
   ~baca.overridelib.dynamic_text_y_offset
   ~baca.overridelib.flag_stencil_false
   ~baca.overridelib.flag_transparent
   ~baca.overridelib.glissando_thickness
   ~baca.overridelib.hairpin_shorten_pair
   ~baca.overridelib.hairpin_start_shift
   ~baca.overridelib.hairpin_stencil_false
   ~baca.overridelib.hairpin_transparent
   ~baca.overridelib.mmrest_text_color
   ~baca.overridelib.mmrest_text_extra_offset
   ~baca.overridelib.mmrest_text_padding
   ~baca.overridelib.mmrest_text_parent_center
   ~baca.overridelib.mmrest_text_staff_padding
   ~baca.overridelib.no_ledgers
   ~baca.overridelib.note_column_shift
   ~baca.overridelib.note_head_color
   ~baca.overridelib.note_head_stencil_false
   ~baca.overridelib.note_head_style_cross
   ~baca.overridelib.note_head_style_harmonic
   ~baca.overridelib.note_head_transparent
   ~baca.overridelib.ottava_bracket_staff_padding
   ~baca.overridelib.rehearsal_mark_extra_offset
   ~baca.overridelib.rehearsal_mark_y_offset
   ~baca.overridelib.repeat_tie_down
   ~baca.overridelib.repeat_tie_stencil_false
   ~baca.overridelib.repeat_tie_transparent
   ~baca.overridelib.repeat_tie_up
   ~baca.overridelib.rest_down
   ~baca.overridelib.rest_extra_offset
   ~baca.overridelib.rest_position
   ~baca.overridelib.rest_transparent
   ~baca.overridelib.rest_up
   ~baca.overridelib.script_color
   ~baca.overridelib.script_down
   ~baca.overridelib.script_extra_offset
   ~baca.overridelib.script_padding
   ~baca.overridelib.script_staff_padding
   ~baca.overridelib.script_up
   ~baca.overridelib.slur_down
   ~baca.overridelib.slur_up
   ~baca.overridelib.span_bar_color
   ~baca.overridelib.span_bar_extra_offset
   ~baca.overridelib.span_bar_transparent
   ~baca.overridelib.stem_color
   ~baca.overridelib.stem_down
   ~baca.overridelib.stem_stencil_false
   ~baca.overridelib.stem_transparent
   ~baca.overridelib.stem_up
   ~baca.overridelib.strict_note_spacing_off
   ~baca.overridelib.sustain_pedal_staff_padding
   ~baca.overridelib.text_script_color
   ~baca.overridelib.text_script_down
   ~baca.overridelib.text_script_extra_offset
   ~baca.overridelib.text_script_font_size
   ~baca.overridelib.text_script_padding
   ~baca.overridelib.text_script_parent_center
   ~baca.overridelib.text_script_staff_padding
   ~baca.overridelib.text_script_up
   ~baca.overridelib.text_script_x_offset
   ~baca.overridelib.text_script_y_offset
   ~baca.overridelib.text_spanner_left_padding
   ~baca.overridelib.text_spanner_right_padding
   ~baca.overridelib.text_spanner_staff_padding
   ~baca.overridelib.text_spanner_stencil_false
   ~baca.overridelib.text_spanner_transparent
   ~baca.overridelib.text_spanner_y_offset
   ~baca.overridelib.tie_down
   ~baca.overridelib.tie_up
   ~baca.overridelib.time_signature_extra_offset
   ~baca.overridelib.time_signature_transparent
   ~baca.overridelib.tremolo_down
   ~baca.overridelib.trill_spanner_staff_padding
   ~baca.overridelib.tuplet_bracket_down
   ~baca.overridelib.tuplet_bracket_extra_offset
   ~baca.overridelib.tuplet_bracket_outside_staff_priority
   ~baca.overridelib.tuplet_bracket_padding
   ~baca.overridelib.tuplet_bracket_shorten_pair
   ~baca.overridelib.tuplet_bracket_staff_padding
   ~baca.overridelib.tuplet_bracket_up
   ~baca.overridelib.tuplet_number_denominator
   ~baca.overridelib.tuplet_number_extra_offset

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.pitcharraylib <baca--pitcharraylib>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: (5) Utilities
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.pitcharraylib.PitchArray
   ~baca.pitcharraylib.PitchArrayCell
   ~baca.pitcharraylib.PitchArrayColumn
   ~baca.pitcharraylib.PitchArrayList
   ~baca.pitcharraylib.PitchArrayRow

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.pitchlib <baca--pitchlib>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: (3) Specifiers
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.pitchlib.ArpeggiationSpacingSpecifier
   ~baca.pitchlib.ChordalSpacingSpecifier

.. raw:: html

   <hr/>

.. rubric:: (5) Utilities
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.pitchlib.CollectionList
   ~baca.pitchlib.Constellation
   ~baca.pitchlib.ConstellationCircuit
   ~baca.pitchlib.PitchClassSegment
   ~baca.pitchlib.PitchClassSet
   ~baca.pitchlib.PitchSegment
   ~baca.pitchlib.PitchSet
   ~baca.pitchlib.PitchTree
   ~baca.pitchlib.PitchTreeSpanner
   ~baca.pitchlib.ZaggedPitchClassMaker

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.rhythmlib <baca--rhythmlib>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: (2) Makers
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.rhythmlib.PitchFirstRhythmMaker

.. raw:: html

   <hr/>

.. rubric:: (3) Specifiers
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.rhythmlib.AcciaccaturaSpecifier

.. raw:: html

   <hr/>

.. rubric:: (4) Commands
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.rhythmlib.PitchFirstRhythmCommand
   ~baca.rhythmlib.RhythmCommand

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.rhythmlib.make_even_divisions
   ~baca.rhythmlib.make_fused_tuplet_monads
   ~baca.rhythmlib.make_multimeasure_rests
   ~baca.rhythmlib.make_notes
   ~baca.rhythmlib.make_repeat_tied_notes
   ~baca.rhythmlib.make_repeated_duration_notes
   ~baca.rhythmlib.make_rests
   ~baca.rhythmlib.make_rhythm
   ~baca.rhythmlib.make_single_attack
   ~baca.rhythmlib.make_skips
   ~baca.rhythmlib.make_tied_notes
   ~baca.rhythmlib.make_tied_repeated_durations
   ~baca.rhythmlib.rhythm

.. raw:: html

   <hr/>

.. rubric:: Rhythm-makers
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.rhythmlib.SkipRhythmMaker

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.settinglib <baca--settinglib>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: (4) Commands
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.settinglib.SettingCommand

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.templatelib <baca--templatelib>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: (5) Utilities
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.templatelib.ScoreTemplate
   ~baca.templatelib.SingleStaffScoreTemplate
   ~baca.templatelib.StringTrioScoreTemplate
   ~baca.templatelib.TwoVoiceStaffScoreTemplate
   ~baca.templatelib.ViolinSoloScoreTemplate