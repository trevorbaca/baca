# -*- coding: utf-8 -*-
import baca


def test_tools_Matrix_01():
    r'''Initializes from rows.
    '''

    matrix = baca.tools.Matrix((
        (0, 1, 2, 3),
        (10, 11, 12, 13),
        (20, 21, 22, 23),
        ))

    assert matrix.rows == (
        (0, 1, 2, 3), (10, 11, 12, 13), (20, 21, 22, 23))
    assert matrix.columns == (
        (0, 10, 20), (1, 11, 21), (2, 12, 22), (3, 13, 23))


def test_tools_Matrix_02():
    r'''Initializes from columns.
    '''

    matrix = baca.tools.Matrix(columns=(
        (0, 10, 20),
        (1, 11, 21),
        (2, 12, 22),
        (3, 13, 23),
        ))

    assert matrix.rows == (
        (0, 1, 2, 3), (10, 11, 12, 13), (20, 21, 22, 23))
    assert matrix.columns == (
        (0, 10, 20), (1, 11, 21), (2, 12, 22), (3, 13, 23))


def test_tools_Matrix_03():
    r'''Gets items.
    '''

    matrix = baca.tools.Matrix([
        [0, 1, 2, 3],
        [10, 11, 12, 13],
        [20, 21, 22, 23],
        ])

    assert matrix[:] == ((0, 1, 2, 3), (10, 11, 12, 13), (20, 21, 22, 23))
    assert matrix[2] == (20, 21, 22, 23)
    assert matrix[2][0] == 20


def test_tools_Matrix_04():
    r'''Gets columns.
    '''

    matrix = baca.tools.Matrix([
        [0, 1, 2, 3],
        [10, 11, 12, 13],
        [20, 21, 22, 23],
        ])

    assert matrix.columns == (
        (0, 10, 20), (1, 11, 21), (2, 12, 22), (3, 13, 23))
    assert matrix.columns[2] == (2, 12, 22)
    assert matrix.columns[2][0] == 2


def test_tools_Matrix_05():
    r'''Gets rows.
    '''

    matrix = baca.tools.Matrix([
        [0, 1, 2, 3],
        [10, 11, 12, 13],
        [20, 21, 22, 23],
        ])

    assert matrix.rows == ((0, 1, 2, 3), (10, 11, 12, 13), (20, 21, 22, 23))
    assert matrix.rows[2] == (20, 21, 22, 23)
    assert matrix.rows[2][0] == 20
