# -*- coding: utf-8 -*-
import abjad
import baca


def test_tools_ZaggedPitchClassMaker_01():
    r'''Same as helianthation when division ratios
    and grouping counts are both none.
    '''

    maker = baca.tools.ZaggedPitchClassMaker(
        pc_cells=[
            [0, 1, 2],
            [3, 4],
            ],
        division_ratios=None,
        grouping_counts=None,
        )

    pitch_class_tree = maker()

    assert pitch_class_tree == baca.tools.PitchClassTree(
        [
            [
                [
                    abjad.pitchtools.NumberedPitchClass(0),
                    abjad.pitchtools.NumberedPitchClass(1),
                    abjad.pitchtools.NumberedPitchClass(2),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(3),
                    abjad.pitchtools.NumberedPitchClass(4),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(4),
                    abjad.pitchtools.NumberedPitchClass(3),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(2),
                    abjad.pitchtools.NumberedPitchClass(0),
                    abjad.pitchtools.NumberedPitchClass(1),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(1),
                    abjad.pitchtools.NumberedPitchClass(2),
                    abjad.pitchtools.NumberedPitchClass(0),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(3),
                    abjad.pitchtools.NumberedPitchClass(4),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(4),
                    abjad.pitchtools.NumberedPitchClass(3),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(0),
                    abjad.pitchtools.NumberedPitchClass(1),
                    abjad.pitchtools.NumberedPitchClass(2),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(2),
                    abjad.pitchtools.NumberedPitchClass(0),
                    abjad.pitchtools.NumberedPitchClass(1),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(3),
                    abjad.pitchtools.NumberedPitchClass(4),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(4),
                    abjad.pitchtools.NumberedPitchClass(3),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(1),
                    abjad.pitchtools.NumberedPitchClass(2),
                    abjad.pitchtools.NumberedPitchClass(0),
                    ],
                ],
            ]
        )


def test_tools_ZaggedPitchClassMaker_02():
    r'''Groups helianthated cells.
    '''

    maker = baca.tools.ZaggedPitchClassMaker(
        pc_cells=[
            [0, 1, 2],
            [3, 4],
            ],
        division_ratios=None,
        grouping_counts=[1, 2],
        )

    pitch_class_tree = maker()

    assert pitch_class_tree == baca.tools.PitchClassTree(
        [
            [
                [
                    abjad.pitchtools.NumberedPitchClass(0),
                    abjad.pitchtools.NumberedPitchClass(1),
                    abjad.pitchtools.NumberedPitchClass(2),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(3),
                    abjad.pitchtools.NumberedPitchClass(4),
                    ],
                [
                    abjad.pitchtools.NumberedPitchClass(4),
                    abjad.pitchtools.NumberedPitchClass(3),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(2),
                    abjad.pitchtools.NumberedPitchClass(0),
                    abjad.pitchtools.NumberedPitchClass(1),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(1),
                    abjad.pitchtools.NumberedPitchClass(2),
                    abjad.pitchtools.NumberedPitchClass(0),
                    ],
                [
                    abjad.pitchtools.NumberedPitchClass(3),
                    abjad.pitchtools.NumberedPitchClass(4),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(4),
                    abjad.pitchtools.NumberedPitchClass(3),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(0),
                    abjad.pitchtools.NumberedPitchClass(1),
                    abjad.pitchtools.NumberedPitchClass(2),
                    ],
                [
                    abjad.pitchtools.NumberedPitchClass(2),
                    abjad.pitchtools.NumberedPitchClass(0),
                    abjad.pitchtools.NumberedPitchClass(1),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(3),
                    abjad.pitchtools.NumberedPitchClass(4),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(4),
                    abjad.pitchtools.NumberedPitchClass(3),
                    ],
                [
                    abjad.pitchtools.NumberedPitchClass(1),
                    abjad.pitchtools.NumberedPitchClass(2),
                    abjad.pitchtools.NumberedPitchClass(0),
                    ],
                ],
            ]
        )


def test_tools_ZaggedPitchClassMaker_03():
    r'''Divides every cell in half. Each cell is of length four prior to
    division. Each cell is of length two after division.
    '''

    maker = baca.tools.ZaggedPitchClassMaker(
        pc_cells=[
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            ],
        division_ratios=[[(1, 1)]],
        grouping_counts=None,
        )

    pitch_class_tree = maker()

    assert pitch_class_tree == baca.tools.PitchClassTree(
        [
            [
                [
                    abjad.pitchtools.NumberedPitchClass(0),
                    abjad.pitchtools.NumberedPitchClass(1),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(2),
                    abjad.pitchtools.NumberedPitchClass(3),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(4),
                    abjad.pitchtools.NumberedPitchClass(5),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(6),
                    abjad.pitchtools.NumberedPitchClass(7),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(7),
                    abjad.pitchtools.NumberedPitchClass(4),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(5),
                    abjad.pitchtools.NumberedPitchClass(6),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(3),
                    abjad.pitchtools.NumberedPitchClass(0),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(1),
                    abjad.pitchtools.NumberedPitchClass(2),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(2),
                    abjad.pitchtools.NumberedPitchClass(3),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(0),
                    abjad.pitchtools.NumberedPitchClass(1),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(6),
                    abjad.pitchtools.NumberedPitchClass(7),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(4),
                    abjad.pitchtools.NumberedPitchClass(5),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(5),
                    abjad.pitchtools.NumberedPitchClass(6),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(7),
                    abjad.pitchtools.NumberedPitchClass(4),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(1),
                    abjad.pitchtools.NumberedPitchClass(2),
                    ],
                ],
            [
                [
                    abjad.pitchtools.NumberedPitchClass(3),
                    abjad.pitchtools.NumberedPitchClass(0),
                    ],
                ],
            ]
        )
