.. _baca:

baca
====

.. automodule:: baca

.. currentmodule:: baca

.. container:: svg-container

   .. inheritance-diagram:: baca
      :lineage: baca

.. raw:: html

   <hr/>

.. rubric:: Subpackages
   :class: section-header

.. toctree::
   :hidden:

   LibraryAF
   LibraryGM
   LibraryNS
   LibraryTZ
   SegmentMaker
   commandlib
   divisionlib
   dynamiclib
   evallib
   indicators
   library
   markuplib
   overridelib
   pitcharray
   pitchclasses
   pitchcommands
   rhythmlib
   segmentlib
   spannerlib
   templatelib

.. autosummary::
   :nosignatures:

   LibraryAF
   LibraryGM
   LibraryNS
   LibraryTZ
   SegmentMaker
   commandlib
   divisionlib
   dynamiclib
   evallib
   indicators
   library
   markuplib
   overridelib
   pitcharray
   pitchclasses
   pitchcommands
   rhythmlib
   segmentlib
   spannerlib
   templatelib

.. raw:: html

   <hr/>

.. rubric:: (2) Makers
   :class: section-header

.. toctree::
   :hidden:

   MusicAccumulator
   MusicContribution
   MusicMaker
   PersistentIndicatorTests

.. autosummary::
   :nosignatures:

   ~MusicAccumulator.MusicAccumulator
   ~MusicContribution.MusicContribution
   ~MusicMaker.MusicMaker
   ~PersistentIndicatorTests.PersistentIndicatorTests

.. raw:: html

   <hr/>

.. rubric:: (3) Specifiers
   :class: section-header

.. toctree::
   :hidden:

   AnchorSpecifier
   LMRSpecifier
   PitchSpecifier
   RestAffixSpecifier

.. autosummary::
   :nosignatures:

   ~AnchorSpecifier.AnchorSpecifier
   ~LMRSpecifier.LMRSpecifier
   ~PitchSpecifier.PitchSpecifier
   ~RestAffixSpecifier.RestAffixSpecifier

.. raw:: html

   <hr/>

.. rubric:: (5) Utilities
   :class: section-header

.. toctree::
   :hidden:

   Coat
   Counter
   Cursor
   Expression
   ExpressionGallery
   IndicatorBundle
   Interpolator
   SchemeManifest
   Selection
   Sequence
   TimeSignatureGroups
   Tree

.. autosummary::
   :nosignatures:

   ~Coat.Coat
   ~Counter.Counter
   ~Cursor.Cursor
   ~Expression.Expression
   ~ExpressionGallery.ExpressionGallery
   ~IndicatorBundle.IndicatorBundle
   ~Interpolator.Interpolator
   ~SchemeManifest.SchemeManifest
   ~Selection.Selection
   ~Sequence.Sequence
   ~TimeSignatureGroups.TimeSignatureGroups
   ~Tree.Tree

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. toctree::
   :hidden:

   ColorCommand
   ContainerCommand
   GlobalFermataCommand
   ImbricationCommand
   IndicatorCommand
   InstrumentChangeCommand
   LabelCommand
   MetronomeMarkCommand
   NestingCommand
   PaddedTuple
   PartAssignmentCommand
   PiecewiseIndicatorCommand

.. autosummary::
   :nosignatures:

   ~ColorCommand.ColorCommand
   ~ContainerCommand.ContainerCommand
   ~GlobalFermataCommand.GlobalFermataCommand
   ~ImbricationCommand.ImbricationCommand
   ~IndicatorCommand.IndicatorCommand
   ~InstrumentChangeCommand.InstrumentChangeCommand
   ~LabelCommand.LabelCommand
   ~MetronomeMarkCommand.MetronomeMarkCommand
   ~NestingCommand.NestingCommand
   ~PaddedTuple.PaddedTuple
   ~PartAssignmentCommand.PartAssignmentCommand
   ~PiecewiseIndicatorCommand.PiecewiseIndicatorCommand

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~are_contiguous_logical_voice
   ~are_contiguous_same_parent
   ~are_leaves
   ~are_logical_voice
   ~chead
   ~cheads
   ~chord
   ~chords
   ~components
   ~count
   ~enchain
   ~filter
   ~filter_duration
   ~filter_length
   ~filter_pitches
   ~filter_preprolated
   ~flatten
   ~group
   ~group_by
   ~group_by_contiguity
   ~group_by_duration
   ~group_by_length
   ~group_by_measure
   ~group_by_measures
   ~group_by_pitch
   ~group_notes_by_measures
   ~index
   ~items
   ~leaf
   ~leaves
   ~lleaf
   ~lleak
   ~lleaves
   ~logical_ties
   ~lt
   ~ltqrun
   ~ltqruns
   ~ltrun
   ~ltruns
   ~lts
   ~nontrivial
   ~note
   ~notes
   ~ntrun
   ~ntruns
   ~partition_by_counts
   ~partition_by_durations
   ~partition_by_ratio
   ~phead
   ~pheads
   ~pleaf
   ~pleaves
   ~plt
   ~plts
   ~ptail
   ~ptails
   ~ptlt
   ~ptlts
   ~qrun
   ~qruns
   ~rest
   ~rests
   ~rleaf
   ~rleak
   ~rleaves
   ~rrun
   ~rruns
   ~run
   ~runs
   ~skip
   ~skips
   ~tleaf
   ~tleaves
   ~top
   ~tuplet
   ~tuplets
   ~with_next_leaf
   ~with_previous_leaf
   ~wleaf
   ~wleaves

.. autofunction:: are_contiguous_logical_voice

.. autofunction:: are_contiguous_same_parent

.. autofunction:: are_leaves

.. autofunction:: are_logical_voice

.. autofunction:: chead

.. autofunction:: cheads

.. autofunction:: chord

.. autofunction:: chords

.. autofunction:: components

.. autofunction:: count

.. autofunction:: enchain

.. autofunction:: filter

.. autofunction:: filter_duration

.. autofunction:: filter_length

.. autofunction:: filter_pitches

.. autofunction:: filter_preprolated

.. autofunction:: flatten

.. autofunction:: group

.. autofunction:: group_by

.. autofunction:: group_by_contiguity

.. autofunction:: group_by_duration

.. autofunction:: group_by_length

.. autofunction:: group_by_measure

.. autofunction:: group_by_measures

.. autofunction:: group_by_pitch

.. autofunction:: group_notes_by_measures

.. autofunction:: index

.. autofunction:: items

.. autofunction:: leaf

.. autofunction:: leaves

.. autofunction:: lleaf

.. autofunction:: lleak

.. autofunction:: lleaves

.. autofunction:: logical_ties

.. autofunction:: lt

.. autofunction:: ltqrun

.. autofunction:: ltqruns

.. autofunction:: ltrun

.. autofunction:: ltruns

.. autofunction:: lts

.. autofunction:: nontrivial

.. autofunction:: note

.. autofunction:: notes

.. autofunction:: ntrun

.. autofunction:: ntruns

.. autofunction:: partition_by_counts

.. autofunction:: partition_by_durations

.. autofunction:: partition_by_ratio

.. autofunction:: phead

.. autofunction:: pheads

.. autofunction:: pleaf

.. autofunction:: pleaves

.. autofunction:: plt

.. autofunction:: plts

.. autofunction:: ptail

.. autofunction:: ptails

.. autofunction:: ptlt

.. autofunction:: ptlts

.. autofunction:: qrun

.. autofunction:: qruns

.. autofunction:: rest

.. autofunction:: rests

.. autofunction:: rleaf

.. autofunction:: rleak

.. autofunction:: rleaves

.. autofunction:: rrun

.. autofunction:: rruns

.. autofunction:: run

.. autofunction:: runs

.. autofunction:: skip

.. autofunction:: skips

.. autofunction:: tleaf

.. autofunction:: tleaves

.. autofunction:: top

.. autofunction:: tuplet

.. autofunction:: tuplets

.. autofunction:: with_next_leaf

.. autofunction:: with_previous_leaf

.. autofunction:: wleaf

.. autofunction:: wleaves