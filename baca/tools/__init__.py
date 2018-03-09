# singletons
from .SchemeManifest import SchemeManifest
scheme = SchemeManifest()

# everything else
from .AcciaccaturaSpecifier import AcciaccaturaSpecifier
from .AccidentalAdjustmentCommand import AccidentalAdjustmentCommand
from .AnchorSpecifier import AnchorSpecifier
from .ArpeggiationSpacingSpecifier import ArpeggiationSpacingSpecifier
from .BreakMeasureMap import BreakMeasureMap
from .ChordalSpacingSpecifier import ChordalSpacingSpecifier
from .ClusterCommand import ClusterCommand
from .Coat import Coat
from .CollectionList import CollectionList
from .ColorCommand import ColorCommand
from .ColorFingeringCommand import ColorFingeringCommand
from .Command import Command
from .CommandWrapper import CommandWrapper
from .Constellation import Constellation
from .ConstellationCircuit import ConstellationCircuit
from .ContainerCommand import ContainerCommand
from .Counter import Counter
from .Cursor import Cursor
from .DesignMaker import DesignMaker
from .DiatonicClusterCommand import DiatonicClusterCommand
from .Division import Division
from .DivisionMaker import DivisionMaker
from .DivisionSequence import DivisionSequence
from .DivisionSequenceExpression import DivisionSequenceExpression
from .Expression import Expression
from .ExpressionGallery import ExpressionGallery
from .FlattenDivisionCallback import FlattenDivisionCallback
from .FuseByCountsDivisionCallback import FuseByCountsDivisionCallback
from .HairpinCommand import HairpinCommand
from .HorizontalSpacingSpecifier import HorizontalSpacingSpecifier
from .ImbricationCommand import ImbricationCommand
from .IndicatorCommand import IndicatorCommand
from .InstrumentChangeCommand import InstrumentChangeCommand
from .Interpolator import Interpolator
from .LBSD import LBSD
from .LMRSpecifier import LMRSpecifier
from .LabelCommand import LabelCommand
from .Loop import Loop
from .MapCommand import MapCommand
from .MarkupLibrary import MarkupLibrary
from .Matrix import Matrix
from .MetronomeMarkCommand import MetronomeMarkCommand
from .MetronomeMarkMeasureMap import MetronomeMarkMeasureMap
from .MicrotoneDeviationCommand import MicrotoneDeviationCommand
from .MusicAccumulator import MusicAccumulator
from .MusicContribution import MusicContribution
from .MusicMaker import MusicMaker
from .NestingCommand import NestingCommand
from .OctaveDisplacementCommand import OctaveDisplacementCommand
from .OverrideCommand import OverrideCommand
from .PageSpecifier import PageSpecifier
from .PartAssignmentCommand import PartAssignmentCommand
from .PartitionDivisionCallback import PartitionDivisionCallback
from .PersistentIndicatorTests import PersistentIndicatorTests
from .PiecewiseCommand import PiecewiseCommand
from .PitchArray import PitchArray
from .PitchArrayCell import PitchArrayCell
from .PitchArrayColumn import PitchArrayColumn
from .PitchArrayList import PitchArrayList
from .PitchArrayRow import PitchArrayRow
from .PitchClassSegment import PitchClassSegment
from .PitchClassSet import PitchClassSet
from .PitchCommand import PitchCommand
from .PitchFirstRhythmCommand import PitchFirstRhythmCommand
from .PitchFirstRhythmMaker import PitchFirstRhythmMaker
from .PitchSegment import PitchSegment
from .PitchSet import PitchSet
from .PitchSpecifier import PitchSpecifier
from .PitchTree import PitchTree
from .PitchTreeSpanner import PitchTreeSpanner
from .RangeDictionary import RangeDictionary
from .RegisterCommand import RegisterCommand
from .RegisterInterpolationCommand import RegisterInterpolationCommand
from .RegisterToOctaveCommand import RegisterToOctaveCommand
from .Registration import Registration
from .RegistrationComponent import RegistrationComponent
from .RegistrationDictionary import RegistrationDictionary
from .RestAffixSpecifier import RestAffixSpecifier
from .RhythmCommand import RhythmCommand
from .Scope import Scope
from .ScoreTemplate import ScoreTemplate
from .SegmentMaker import SegmentMaker
from .Selection import Selection
from .Sequence import Sequence
from .SettingCommand import SettingCommand
from .SingleStaffScoreTemplate import SingleStaffScoreTemplate
from .SpacingIndication import SpacingIndication
from .SpacingSection import SpacingSection
from .SpannerCommand import SpannerCommand
from .SplitByDurationsDivisionCallback import SplitByDurationsDivisionCallback
from .SplitByRoundedRatiosDivisionCallback import \
    SplitByRoundedRatiosDivisionCallback
from .StaffLines import StaffLines
from .StaffPositionCommand import StaffPositionCommand
from .StaffPositionInterpolationCommand import \
    StaffPositionInterpolationCommand
from .StageMeasureMap import StageMeasureMap
from .StringTrioScoreTemplate import StringTrioScoreTemplate
from .SuiteCommand import SuiteCommand
from .SystemSpecifier import SystemSpecifier
from .TieCorrectionCommand import TieCorrectionCommand
from .TimeSignatureGroups import TimeSignatureGroups
from .TimeSignatureMaker import TimeSignatureMaker
from .TimelineScope import TimelineScope
from .Tree import Tree
from .TwoVoiceStaffScoreTemplate import TwoVoiceStaffScoreTemplate
from .ViolinSoloScoreTemplate import ViolinSoloScoreTemplate
from .VoltaCommand import VoltaCommand
from .WellformednessManager import WellformednessManager
from .ZaggedPitchClassMaker import ZaggedPitchClassMaker

# library:
from .LibraryAF import LibraryAF
from .LibraryGM import LibraryGM
from .LibraryNS import LibraryNS
from .LibraryTZ import LibraryTZ


# MYPY:
#
# UNCOMMENT WHEN RUNNING MYPY AGAINST SCORES
#
# LEAVE COMMENTED-OUT WHEN BUILDING API
#
#### SELECTORS ###
#
#def phead(n):
#    return baca.select().phead(n)
#
#def pheads():
#    return baca.select().pheads()
#
#def pleaf(n):
#    return baca.select().pleaf(n)
#
#### LIBRARY A-F ###
#
#accents = LibraryAF.accents
#breaks = LibraryAF.breaks
#clef = LibraryAF.clef
#dynamic = LibraryAF.dynamic
#
#### LIBRARY G-M ###
#
#make_scopes = LibraryGM.make_scopes
#margin_markup = LibraryGM.margin_markup
#metronome_mark = LibraryGM.metronome_mark
#
#### LIBRARY N-S ###
#
#page = LibraryNS.page
#pitches = LibraryNS.pitches
#scope = LibraryNS.scope
#scorewide_spacing = LibraryNS.scorewide_spacing
#strict_quarter_divisions = LibraryNS.strict_quarter_divisions
#
#### LIBRARY T-Z ###
#
#trill_spanner_staff_padding = LibraryTZ.trill_spanner_staff_padding
#trill = LibraryTZ.trill
#untie_to = LibraryTZ.trill
