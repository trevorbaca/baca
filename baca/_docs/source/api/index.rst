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
   ~baca.group_by_pitch
   ~baca.index
   ~baca.items
   ~baca.leaf
   ~baca.leaves
   ~baca.lleak
   ~baca.lleaves
   ~baca.logical_ties
   ~baca.lt
   ~baca.ltqrun
   ~baca.ltqruns
   ~baca.ltrun
   ~baca.ltruns
   ~baca.lts
   ~baca.map
   ~baca.nontrivial
   ~baca.note
   ~baca.notes
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
   ~baca.rleak
   ~baca.rleaves
   ~baca.rrun
   ~baca.rruns
   ~baca.run
   ~baca.runs
   ~baca.skip
   ~baca.skips
   ~baca.tleaves
   ~baca.top
   ~baca.tuplet
   ~baca.tuplets
   ~baca.with_next_leaf
   ~baca.with_previous_leaf
   ~baca.wleaves

.. raw:: html

   <hr/>

.. rubric:: :ref:`baca.tools <baca--tools>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: (1) Library
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.tools.LibraryAF.LibraryAF
   ~baca.tools.LibraryGM.LibraryGM
   ~baca.tools.LibraryNS.LibraryNS
   ~baca.tools.LibraryTZ.LibraryTZ
   ~baca.tools.MarkupLibrary.MarkupLibrary
   ~baca.tools.SchemeManifest.SchemeManifest

.. raw:: html

   <hr/>

.. rubric:: (2) Makers
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.tools.MusicAccumulator.MusicAccumulator
   ~baca.tools.MusicContribution.MusicContribution
   ~baca.tools.MusicMaker.MusicMaker
   ~baca.tools.PersistentIndicatorTests.PersistentIndicatorTests
   ~baca.tools.PitchFirstRhythmMaker.PitchFirstRhythmMaker
   ~baca.tools.SegmentMaker.SegmentMaker

.. raw:: html

   <hr/>

.. rubric:: (3) Specifiers
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.tools.AcciaccaturaSpecifier.AcciaccaturaSpecifier
   ~baca.tools.AnchorSpecifier.AnchorSpecifier
   ~baca.tools.ArpeggiationSpacingSpecifier.ArpeggiationSpacingSpecifier
   ~baca.tools.ChordalSpacingSpecifier.ChordalSpacingSpecifier
   ~baca.tools.HorizontalSpacingSpecifier.HorizontalSpacingSpecifier
   ~baca.tools.LMRSpecifier.LMRSpecifier
   ~baca.tools.PitchSpecifier.PitchSpecifier
   ~baca.tools.RestAffixSpecifier.RestAffixSpecifier

.. raw:: html

   <hr/>

.. rubric:: (4) Commands
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.tools.AccidentalAdjustmentCommand.AccidentalAdjustmentCommand
   ~baca.tools.BowContactPointCommand.BowContactPointCommand
   ~baca.tools.ClusterCommand.ClusterCommand
   ~baca.tools.ColorCommand.ColorCommand
   ~baca.tools.ColorFingeringCommand.ColorFingeringCommand
   ~baca.tools.Command.Command
   ~baca.tools.CommandWrapper.CommandWrapper
   ~baca.tools.ContainerCommand.ContainerCommand
   ~baca.tools.DiatonicClusterCommand.DiatonicClusterCommand
   ~baca.tools.GlobalFermataCommand.GlobalFermataCommand
   ~baca.tools.HairpinCommand.HairpinCommand
   ~baca.tools.ImbricationCommand.ImbricationCommand
   ~baca.tools.IndicatorCommand.IndicatorCommand
   ~baca.tools.InstrumentChangeCommand.InstrumentChangeCommand
   ~baca.tools.LabelCommand.LabelCommand
   ~baca.tools.MapCommand.MapCommand
   ~baca.tools.MetronomeMarkCommand.MetronomeMarkCommand
   ~baca.tools.MicrotoneDeviationCommand.MicrotoneDeviationCommand
   ~baca.tools.NestingCommand.NestingCommand
   ~baca.tools.OctaveDisplacementCommand.OctaveDisplacementCommand
   ~baca.tools.OverrideCommand.OverrideCommand
   ~baca.tools.PartAssignmentCommand.PartAssignmentCommand
   ~baca.tools.PiecewiseCommand.PiecewiseCommand
   ~baca.tools.PitchCommand.PitchCommand
   ~baca.tools.PitchFirstRhythmCommand.PitchFirstRhythmCommand
   ~baca.tools.RegisterCommand.RegisterCommand
   ~baca.tools.RegisterInterpolationCommand.RegisterInterpolationCommand
   ~baca.tools.RegisterToOctaveCommand.RegisterToOctaveCommand
   ~baca.tools.RhythmCommand.RhythmCommand
   ~baca.tools.SettingCommand.SettingCommand
   ~baca.tools.SpannerCommand.SpannerCommand
   ~baca.tools.StaffPositionCommand.StaffPositionCommand
   ~baca.tools.StaffPositionInterpolationCommand.StaffPositionInterpolationCommand
   ~baca.tools.SuiteCommand.SuiteCommand
   ~baca.tools.TextSpannerCommand.TextSpannerCommand
   ~baca.tools.TieCorrectionCommand.TieCorrectionCommand
   ~baca.tools.VoltaCommand.VoltaCommand

.. raw:: html

   <hr/>

.. rubric:: (5) Utilities
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.tools.BreakMeasureMap.BreakMeasureMap
   ~baca.tools.Coat.Coat
   ~baca.tools.CollectionList.CollectionList
   ~baca.tools.Constellation.Constellation
   ~baca.tools.ConstellationCircuit.ConstellationCircuit
   ~baca.tools.Counter.Counter
   ~baca.tools.Cursor.Cursor
   ~baca.tools.DesignMaker.DesignMaker
   ~baca.tools.Division.Division
   ~baca.tools.Expression.Expression
   ~baca.tools.ExpressionGallery.ExpressionGallery
   ~baca.tools.HarmonicSeries.HarmonicSeries
   ~baca.tools.Interpolator.Interpolator
   ~baca.tools.LBSD.LBSD
   ~baca.tools.Loop.Loop
   ~baca.tools.Matrix.Matrix
   ~baca.tools.MetronomeMarkMeasureMap.MetronomeMarkMeasureMap
   ~baca.tools.PageSpecifier.PageSpecifier
   ~baca.tools.Partial.Partial
   ~baca.tools.PitchArray.PitchArray
   ~baca.tools.PitchArrayCell.PitchArrayCell
   ~baca.tools.PitchArrayColumn.PitchArrayColumn
   ~baca.tools.PitchArrayList.PitchArrayList
   ~baca.tools.PitchArrayRow.PitchArrayRow
   ~baca.tools.PitchClassSegment.PitchClassSegment
   ~baca.tools.PitchClassSet.PitchClassSet
   ~baca.tools.PitchSegment.PitchSegment
   ~baca.tools.PitchSet.PitchSet
   ~baca.tools.PitchTree.PitchTree
   ~baca.tools.PitchTreeSpanner.PitchTreeSpanner
   ~baca.tools.Registration.Registration
   ~baca.tools.RegistrationComponent.RegistrationComponent
   ~baca.tools.Scope.Scope
   ~baca.tools.ScoreTemplate.ScoreTemplate
   ~baca.tools.Selection.Selection
   ~baca.tools.Sequence.Sequence
   ~baca.tools.SingleStaffScoreTemplate.SingleStaffScoreTemplate
   ~baca.tools.SpacingIndication.SpacingIndication
   ~baca.tools.SpacingSection.SpacingSection
   ~baca.tools.StaffLines.StaffLines
   ~baca.tools.StageMeasureMap.StageMeasureMap
   ~baca.tools.StringTrioScoreTemplate.StringTrioScoreTemplate
   ~baca.tools.SystemSpecifier.SystemSpecifier
   ~baca.tools.TimeSignatureGroups.TimeSignatureGroups
   ~baca.tools.TimeSignatureMaker.TimeSignatureMaker
   ~baca.tools.TimelineScope.TimelineScope
   ~baca.tools.Tree.Tree
   ~baca.tools.TwoVoiceStaffScoreTemplate.TwoVoiceStaffScoreTemplate
   ~baca.tools.ViolinSoloScoreTemplate.ViolinSoloScoreTemplate
   ~baca.tools.WellformednessManager.WellformednessManager
   ~baca.tools.ZaggedPitchClassMaker.ZaggedPitchClassMaker

.. raw:: html

   <hr/>

.. rubric:: (6) Divisions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~baca.tools.DivisionMaker.DivisionMaker
   ~baca.tools.DivisionSequence.DivisionSequence
   ~baca.tools.DivisionSequenceExpression.DivisionSequenceExpression
   ~baca.tools.FlattenDivisionCallback.FlattenDivisionCallback
   ~baca.tools.FuseByCountsDivisionCallback.FuseByCountsDivisionCallback
   ~baca.tools.PartitionDivisionCallback.PartitionDivisionCallback
   ~baca.tools.SplitByDurationsDivisionCallback.SplitByDurationsDivisionCallback
   ~baca.tools.SplitByRoundedRatiosDivisionCallback.SplitByRoundedRatiosDivisionCallback