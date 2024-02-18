import abjad
import baca


def test_dynamics():
    specifiers = baca.hairpins.parse_hairpin_descriptor("f")
    assert len(specifiers) == 1
    assert specifiers[0] == baca.hairpins.HairpinSpecifier(
        indicator=abjad.Dynamic("f"),
    )

    specifiers = baca.hairpins.parse_hairpin_descriptor('"f"')
    assert len(specifiers) == 1
    assert specifiers[0] == baca.hairpins.HairpinSpecifier(
        indicator=abjad.Dynamic(
            name='"f"',
            command="\\baca-effort-f",
        ),
    )


def test_start_hairpin():
    specifiers = baca.hairpins.parse_hairpin_descriptor("<")
    assert len(specifiers) == 1
    assert specifiers[0] == baca.hairpins.HairpinSpecifier(
        spanner_start=abjad.StartHairpin("<"),
    )

    specifiers = baca.hairpins.parse_hairpin_descriptor("o<|")
    assert len(specifiers) == 1
    assert specifiers[0] == baca.hairpins.HairpinSpecifier(
        spanner_start=abjad.StartHairpin("o<|"),
    )

    specifiers = baca.hairpins.parse_hairpin_descriptor("--")
    assert len(specifiers) == 1
    assert specifiers[0] == baca.hairpins.HairpinSpecifier(
        spanner_start=abjad.StartHairpin("--"),
    )


def test_single_hairpin_01():
    specifiers = baca.hairpins.parse_hairpin_descriptor("< !")
    assert len(specifiers) == 2
    assert specifiers[0] == baca.hairpins.HairpinSpecifier(
        spanner_start=abjad.StartHairpin("<"),
    )
    assert specifiers[1] == baca.hairpins.HairpinSpecifier(
        spanner_stop=abjad.StopHairpin(),
    )


def test_single_hairpin_02():
    specifiers = baca.hairpins.parse_hairpin_descriptor("p < f")
    assert len(specifiers) == 2
    assert specifiers[0] == baca.hairpins.HairpinSpecifier(
        indicator=abjad.Dynamic("p"),
        spanner_start=abjad.StartHairpin("<"),
    )
    assert specifiers[1] == baca.hairpins.HairpinSpecifier(
        indicator=abjad.Dynamic("f"),
    )


def test_single_hairpin_03():
    specifiers = baca.hairpins.parse_hairpin_descriptor("p <")
    assert len(specifiers) == 1
    assert specifiers[0] == baca.hairpins.HairpinSpecifier(
        indicator=abjad.Dynamic("p"),
        spanner_start=abjad.StartHairpin("<"),
    )


def test_single_hairpin_04():
    specifiers = baca.hairpins.parse_hairpin_descriptor("p < !")
    assert len(specifiers) == 2
    assert specifiers[0] == baca.hairpins.HairpinSpecifier(
        indicator=abjad.Dynamic("p"),
        spanner_start=abjad.StartHairpin("<"),
    )
    assert specifiers[1] == baca.hairpins.HairpinSpecifier(
        spanner_stop=abjad.StopHairpin(),
    )


def test_single_hairpin_05():
    specifiers = baca.hairpins.parse_hairpin_descriptor("< f")
    assert len(specifiers) == 2
    baca.hairpins.HairpinSpecifier(
        spanner_start=abjad.StartHairpin("<"),
    )
    baca.hairpins.HairpinSpecifier(
        indicator=abjad.Dynamic("f"),
    )


def test_single_hairpin_06():
    specifiers = baca.hairpins.parse_hairpin_descriptor("o< f")
    assert len(specifiers) == 2
    assert specifiers[0] == baca.hairpins.HairpinSpecifier(
        spanner_start=abjad.StartHairpin("o<"),
    )
    assert specifiers[1] == baca.hairpins.HairpinSpecifier(
        indicator=abjad.Dynamic("f"),
    )


def test_single_hairpin_07():
    specifiers = baca.hairpins.parse_hairpin_descriptor("f >")
    assert len(specifiers) == 1
    assert specifiers[0] == baca.hairpins.HairpinSpecifier(
        indicator=abjad.Dynamic("f"),
        spanner_start=abjad.StartHairpin(">"),
    )


def test_single_hairpin_08():
    specifiers = baca.hairpins.parse_hairpin_descriptor("f >o")
    assert len(specifiers) == 1
    assert specifiers[0] == baca.hairpins.HairpinSpecifier(
        indicator=abjad.Dynamic("f"),
        spanner_start=abjad.StartHairpin(">o"),
    )


def test_multiple_hairpins_01():
    specifiers = baca.hairpins.parse_hairpin_descriptor("p mp mf f")
    assert len(specifiers) == 4
    assert specifiers[0] == baca.hairpins.HairpinSpecifier(
        indicator=abjad.Dynamic("p"),
    )
    assert specifiers[1] == baca.hairpins.HairpinSpecifier(
        indicator=abjad.Dynamic("mp"),
    )
    assert specifiers[2] == baca.hairpins.HairpinSpecifier(
        indicator=abjad.Dynamic("mf"),
    )
    assert specifiers[3] == baca.hairpins.HairpinSpecifier(
        indicator=abjad.Dynamic("f"),
    )


def test_multiple_hairpins_02():
    specifiers = baca.hairpins.parse_hairpin_descriptor("p < f f > p")
    assert len(specifiers) == 4
    assert specifiers[0] == baca.hairpins.HairpinSpecifier(
        indicator=abjad.Dynamic("p"),
        spanner_start=abjad.StartHairpin("<"),
    )
    assert specifiers[1] == baca.hairpins.HairpinSpecifier(
        indicator=abjad.Dynamic("f"),
    )
    assert specifiers[2] == baca.hairpins.HairpinSpecifier(
        indicator=abjad.Dynamic("f"),
        spanner_start=abjad.StartHairpin(">"),
    )
    assert specifiers[3] == baca.hairpins.HairpinSpecifier(
        indicator=abjad.Dynamic("p"),
    )


def test_multiple_hairpins_03():
    specifiers = baca.hairpins.parse_hairpin_descriptor("f -- ! > p")
    assert len(specifiers) == 3
    assert specifiers[0] == baca.hairpins.HairpinSpecifier(
        indicator=abjad.Dynamic("f"),
        spanner_start=abjad.StartHairpin("--"),
    )
    assert specifiers[1] == baca.hairpins.HairpinSpecifier(
        spanner_start=abjad.StartHairpin(">"),
        spanner_stop=abjad.StopHairpin(),
    )
    assert specifiers[2] == baca.hairpins.HairpinSpecifier(
        indicator=abjad.Dynamic("p"),
    )


def test_multiple_hairpins_04():
    specifiers = baca.hairpins.parse_hairpin_descriptor("mf - o< p")
    assert len(specifiers) == 3
    assert specifiers[0] == baca.hairpins.HairpinSpecifier(
        indicator=abjad.Dynamic("mf"),
    )
    assert specifiers[1] == baca.hairpins.HairpinSpecifier(
        spanner_start=abjad.StartHairpin("o<"),
    )
    assert specifiers[2] == baca.hairpins.HairpinSpecifier(
        indicator=abjad.Dynamic("p"),
    )
