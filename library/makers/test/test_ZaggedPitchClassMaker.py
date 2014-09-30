# -*- encoding: utf-8 -*-
from abjad import *
import baca


def test_ZaggedPitchClassMaker_01():
    r'''Same as helianthation when division ratios
    and grouping counts are both none.
    '''

    maker = baca.library.makers.ZaggedPitchClassMaker(
        pc_cells=[
            [0, 1, 2],
            [3, 4],
            ],
        division_ratios=None,
        grouping_counts=None,
        )

    pitch_class_tree = maker()

    assert pitch_class_tree == pitchtools.PitchClassTree(
        [
            [
                [
                    pitchtools.NumberedPitchClass(0),
                    pitchtools.NumberedPitchClass(1),
                    pitchtools.NumberedPitchClass(2),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(3),
                    pitchtools.NumberedPitchClass(4),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(4),
                    pitchtools.NumberedPitchClass(3),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(2),
                    pitchtools.NumberedPitchClass(0),
                    pitchtools.NumberedPitchClass(1),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(1),
                    pitchtools.NumberedPitchClass(2),
                    pitchtools.NumberedPitchClass(0),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(3),
                    pitchtools.NumberedPitchClass(4),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(4),
                    pitchtools.NumberedPitchClass(3),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(0),
                    pitchtools.NumberedPitchClass(1),
                    pitchtools.NumberedPitchClass(2),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(2),
                    pitchtools.NumberedPitchClass(0),
                    pitchtools.NumberedPitchClass(1),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(3),
                    pitchtools.NumberedPitchClass(4),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(4),
                    pitchtools.NumberedPitchClass(3),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(1),
                    pitchtools.NumberedPitchClass(2),
                    pitchtools.NumberedPitchClass(0),
                    ],
                ],
            ]
        )


def test_ZaggedPitchClassMaker_02():
    r'''Groups helianthated cells.
    '''

    maker = baca.library.makers.ZaggedPitchClassMaker(
        pc_cells=[
            [0, 1, 2],
            [3, 4],
            ],
        division_ratios=None,
        grouping_counts=[1, 2],
        )

    pitch_class_tree = maker()

    assert pitch_class_tree == pitchtools.PitchClassTree(
        [
            [
                [
                    pitchtools.NumberedPitchClass(0),
                    pitchtools.NumberedPitchClass(1),
                    pitchtools.NumberedPitchClass(2),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(3),
                    pitchtools.NumberedPitchClass(4),
                    pitchtools.NumberedPitchClass(4),
                    pitchtools.NumberedPitchClass(3),
                    ],
                [
                    pitchtools.NumberedPitchClass(2),
                    pitchtools.NumberedPitchClass(0),
                    pitchtools.NumberedPitchClass(1),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(1),
                    pitchtools.NumberedPitchClass(2),
                    pitchtools.NumberedPitchClass(0),
                    pitchtools.NumberedPitchClass(3),
                    pitchtools.NumberedPitchClass(4),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(4),
                    pitchtools.NumberedPitchClass(3),
                    ],
                [
                    pitchtools.NumberedPitchClass(0),
                    pitchtools.NumberedPitchClass(1),
                    pitchtools.NumberedPitchClass(2),
                    pitchtools.NumberedPitchClass(2),
                    pitchtools.NumberedPitchClass(0),
                    pitchtools.NumberedPitchClass(1),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(3),
                    pitchtools.NumberedPitchClass(4),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(4),
                    pitchtools.NumberedPitchClass(3),
                    pitchtools.NumberedPitchClass(1),
                    pitchtools.NumberedPitchClass(2),
                    pitchtools.NumberedPitchClass(0),
                    ],
                ],
            ]
        )


def test_ZaggedPitchClassMaker_03():
    r'''Divides every cell in half. Each cell is of length four prior to
    division. Each cell is of length two after division.
    '''

    maker = baca.library.makers.ZaggedPitchClassMaker(
        pc_cells=[
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            ],
        division_ratios=[[(1, 1)]],
        grouping_counts=None,
        )

    pitch_class_tree = maker()

    assert pitch_class_tree == pitchtools.PitchClassTree(
        [
            [
                [
                    pitchtools.NumberedPitchClass(0),
                    pitchtools.NumberedPitchClass(1),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(2),
                    pitchtools.NumberedPitchClass(3),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(4),
                    pitchtools.NumberedPitchClass(5),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(6),
                    pitchtools.NumberedPitchClass(7),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(7),
                    pitchtools.NumberedPitchClass(4),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(5),
                    pitchtools.NumberedPitchClass(6),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(3),
                    pitchtools.NumberedPitchClass(0),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(1),
                    pitchtools.NumberedPitchClass(2),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(2),
                    pitchtools.NumberedPitchClass(3),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(0),
                    pitchtools.NumberedPitchClass(1),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(6),
                    pitchtools.NumberedPitchClass(7),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(4),
                    pitchtools.NumberedPitchClass(5),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(5),
                    pitchtools.NumberedPitchClass(6),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(7),
                    pitchtools.NumberedPitchClass(4),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(1),
                    pitchtools.NumberedPitchClass(2),
                    ],
                ],
            [
                [
                    pitchtools.NumberedPitchClass(3),
                    pitchtools.NumberedPitchClass(0),
                    ],
                ],
            ]
        )