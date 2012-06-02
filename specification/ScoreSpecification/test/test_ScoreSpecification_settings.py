from abjad.tools import *
from baca.specification.ScoreSpecification import ScoreSpecification


def test_ScoreSpecification_settings_01():

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(1))
    assert not specification.settings


def test_ScoreSpecification_settings_02():

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(1))
    specification.append_segment('1')
