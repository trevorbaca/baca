import abjad
from .library import *
from .dynamics import *
from .overrides import *
from . import markups

# classes
from .Accelerando import Accelerando
from .AcciaccaturaSpecifier import AcciaccaturaSpecifier
from .AccidentalAdjustmentCommand import AccidentalAdjustmentCommand
from .AnchorSpecifier import AnchorSpecifier
from .ArpeggiationSpacingSpecifier import ArpeggiationSpacingSpecifier
from .BowContactPointCommand import BowContactPointCommand
from .BreakMeasureMap import BreakMeasureMap
from .ChordalSpacingSpecifier import ChordalSpacingSpecifier
from .ClusterCommand import ClusterCommand
from .Coat import Coat
from .CollectionList import CollectionList
from .ColorCommand import ColorCommand
from .ColorFingeringCommand import ColorFingeringCommand
from .Command import Command
from .Command import Map
from .Command import Suite
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
from .IndicatorBundle import IndicatorBundle
from .Expression import Expression
from .ExpressionGallery import ExpressionGallery
from .FlattenDivisionCallback import FlattenDivisionCallback
from .FuseByCountsDivisionCallback import FuseByCountsDivisionCallback
from .GlobalFermataCommand import GlobalFermataCommand
from .HarmonicSeries import HarmonicSeries
from .HorizontalSpacingSpecifier import HorizontalSpacingSpecifier
from .ImbricationCommand import ImbricationCommand
from .IndicatorCommand import IndicatorCommand
from .InstrumentChangeCommand import InstrumentChangeCommand
from .Interpolator import Interpolator
from .LBSD import LBSD
from .LMRSpecifier import LMRSpecifier
from .LabelCommand import LabelCommand
from .Loop import Loop
from .Markup import Markup
from .Matrix import Matrix
from .MeasureWrapper import MeasureWrapper
from .MetronomeMarkCommand import MetronomeMarkCommand
from .MetronomeMarkMeasureMap import MetronomeMarkMeasureMap
from .MicrotoneDeviationCommand import MicrotoneDeviationCommand
from .MusicAccumulator import MusicAccumulator
from .MusicContribution import MusicContribution
from .MusicMaker import MusicMaker
from .NestingCommand import NestingCommand
from .OctaveDisplacementCommand import OctaveDisplacementCommand
from .OverrideCommand import OverrideCommand
from .PaddedTuple import PaddedTuple
from .PageSpecifier import PageSpecifier
from .PartAssignmentCommand import PartAssignmentCommand
from .Partial import Partial
from .PartitionDivisionCallback import PartitionDivisionCallback
from .PersistentIndicatorTests import PersistentIndicatorTests
from .PiecewiseIndicatorCommand import PiecewiseIndicatorCommand
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
from .RegisterCommand import RegisterCommand
from .RegisterInterpolationCommand import RegisterInterpolationCommand
from .RegisterToOctaveCommand import RegisterToOctaveCommand
from .Registration import Registration
from .RegistrationComponent import RegistrationComponent
from .RestAffixSpecifier import RestAffixSpecifier
from .RhythmCommand import RhythmCommand
from .Ritardando import Ritardando
from .SchemeManifest import SchemeManifest
from .Scope import Scope
from .ScoreTemplate import ScoreTemplate
from .SegmentMaker import SegmentMaker
from .Selection import Selection
from .Sequence import Sequence
from .SettingCommand import SettingCommand
from .SingleStaffScoreTemplate import SingleStaffScoreTemplate
from .SkipRhythmMaker import SkipRhythmMaker
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

# expression constructors
from .PitchClassSegment import _pitch_class_segment as pitch_class_segment
from .PitchClassSet import _pitch_class_set as pitch_class_set
from .PitchSegment import _pitch_segment as pitch_segment
from .PitchSet import _pitch_set as pitch_set
from .Selection import _select as select
from .Sequence import _sequence as sequence

def _import_static_methods(class_):
    for name in dir(class_):
        if name.startswith('_'):
            continue
        statement = f'{name} = {class_.__name__}.{name}'
        exec(statement, globals())

def _publish_selectors(class_):
    for name in dir(class_):
        if name.startswith('_'):
            continue
        if name in ('map',):
            continue
        statement = f"""def {name}(*arguments, **keywords):
            return select().{name}(*arguments, **keywords)"""
        exec(statement, globals())

_import_static_methods(LibraryAF)
_import_static_methods(LibraryGM)
_import_static_methods(LibraryNS)
_import_static_methods(LibraryTZ)
_publish_selectors(Selection)
