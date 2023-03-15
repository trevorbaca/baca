import abjad
import baca


def test_Cursor___getitem__():
    source = [13, "da capo", abjad.Note("cs'8."), "rit."]
    cursor = baca.Cursor(source=source, cyclic=True)

    assert cursor[0] == 13
    assert cursor[:2] == (13, "da capo")
    assert cursor[-1] == "rit."


def test_Cursor___iter__():
    source = [13, "da capo", "cs'8.", "rit."]
    cursor = baca.Cursor(source=source)
    items = []
    for item in cursor:
        items.append(item)
    assert items == source

    source = [13, "da capo", "cs'8.", "rit."]
    cursor = baca.Cursor(source=source, cyclic=True)
    items = []
    for item in cursor:
        items.append(item)
    assert items == source


def test_Cursor___len__():
    source = [13, "da capo", "cs'8.", "rit."]
    cursor = baca.Cursor(source=source)
    assert len(cursor) == 4


def test_Cursor_exhausted():
    source = [13, "da capo", "cs'8.", "rit."]
    cursor = baca.Cursor(source=source)
    assert cursor.exhausted is False

    assert cursor.next() == [13]
    assert cursor.exhausted is False

    assert cursor.next() == ["da capo"]
    assert cursor.exhausted is False

    assert cursor.next() == ["cs'8."]
    assert cursor.exhausted is False

    assert cursor.next() == ["rit."]
    assert cursor.exhausted is True


def test_Cursor_next_01():
    """
    Gets elements one at a time.
    """

    source = [13, "da capo", "cs'8.", "rit."]
    cursor = baca.Cursor(source=source, cyclic=True)

    assert cursor.next() == [13]
    assert cursor.next() == ["da capo"]
    assert cursor.next() == ["cs'8."]
    assert cursor.next() == ["rit."]
    assert cursor.next() == [13]
    assert cursor.next() == ["da capo"]


def test_Cursor_next_02():
    """
    Gets different numbers of elements at a time.
    """

    source = [13, "da capo", "cs'8.", "rit."]
    cursor = baca.Cursor(source=source, cyclic=True)

    assert cursor.next(count=2) == [13, "da capo"]
    assert cursor.next(count=-1) == ["da capo"]
    assert cursor.next(count=2) == ["da capo", "cs'8."]
    assert cursor.next(count=-1) == ["cs'8."]
    assert cursor.next(count=2) == ["cs'8.", "rit."]
    assert cursor.next(count=-1) == ["rit."]


def test_Cursor_next_03():
    """
    Position starts at none by default.
    """

    source = [13, "da capo", "cs'8.", "rit."]
    cursor = baca.Cursor(source=source, cyclic=True)

    assert cursor.position is None
    assert cursor.next() == [13]
    assert cursor.next() == ["da capo"]
    assert cursor.next() == ["cs'8."]
    assert cursor.next() == ["rit."]

    source = [13, "da capo", "cs'8.", "rit."]
    cursor = baca.Cursor(
        source=source,
        cyclic=True,
        position=None,
    )

    assert cursor.position is None
    assert cursor.next(count=-1) == ["rit."]
    assert cursor.next(count=-1) == ["cs'8."]
    assert cursor.next(count=-1) == ["da capo"]
    assert cursor.next(count=-1) == [13]


def test_Cursor_next_04():
    """
    Position starting at 0:
    """

    source = [13, "da capo", "cs'8.", "rit."]
    cursor = baca.Cursor(
        source=source,
        cyclic=True,
        position=0,
    )

    assert cursor.position == 0
    assert cursor.next() == [13]
    assert cursor.next() == ["da capo"]
    assert cursor.next() == ["cs'8."]
    assert cursor.next() == ["rit."]

    source = [13, "da capo", "cs'8.", "rit."]
    cursor = baca.Cursor(
        source=source,
        cyclic=True,
        position=0,
    )

    assert cursor.position == 0
    assert cursor.next(count=-1) == ["rit."]
    assert cursor.next(count=-1) == ["cs'8."]
    assert cursor.next(count=-1) == ["da capo"]
    assert cursor.next(count=-1) == [13]

    """
    Position starting at -1:
    """

    source = [13, "da capo", "cs'8.", "rit."]
    cursor = baca.Cursor(
        source=source,
        cyclic=True,
        position=-1,
    )

    assert cursor.position == -1
    assert cursor.next() == ["rit."]
    assert cursor.next() == [13]
    assert cursor.next() == ["da capo"]
    assert cursor.next() == ["cs'8."]

    source = [13, "da capo", "cs'8.", "rit."]
    cursor = baca.Cursor(
        source=source,
        cyclic=True,
        position=-1,
    )

    assert cursor.position == -1
    assert cursor.next(count=-1) == ["cs'8."]
    assert cursor.next(count=-1) == ["da capo"]
    assert cursor.next(count=-1) == [13]
    assert cursor.next(count=-1) == ["rit."]


def test_Cursor_next_05():
    """
    Singletons Is true when cursor returns singletons not enclosed within a list.
    If false when cursor returns singletons enclosed within a list. Returns
    singletons enclosed within a list:
    """

    source = [13, "da capo", "cs'8.", "rit."]
    cursor = baca.Cursor(
        source=source,
        suppress_exception=True,
    )

    assert cursor.next() == [13]
    assert cursor.next() == ["da capo"]
    assert cursor.next() == ["cs'8."]
    assert cursor.next() == ["rit."]
    assert cursor.next() == []
    assert cursor.next() == []


def test_Cursor_next_06():
    """
    Returns singletons free of enclosing list.
    """

    source = [13, "da capo", "cs'8.", "rit."]
    cursor = baca.Cursor(
        source=source,
        singletons=True,
        suppress_exception=True,
    )

    assert cursor.next() == 13
    assert cursor.next() == "da capo"
    assert cursor.next() == "cs'8."
    assert cursor.next() == "rit."
    assert cursor.next() == []
    assert cursor.next() == []
